# 2. Add Two Numbers

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Linked List, Math, Recursion &nbsp;·&nbsp; **Source:** [leetcode.com/problems/add-two-numbers](https://leetcode.com/problems/add-two-numbers/)

Two non-empty linked lists representing non-negative integers, digits stored in **reverse order** (least-significant first), one digit per node. Return the sum as a linked list in the same form. Lists may differ in length and the final carry can produce one extra leading digit.

**Constraints:** `1 ≤ digits in each list ≤ 100`, `0 ≤ Node.val ≤ 9`, leading digit non-zero unless the number is zero.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Iterative: walk both lists in lockstep, append digit-by-digit | O(max(m, n)) time, O(max(m, n)) space | [`iterative.kara`](iterative.kara) ✓ | [`iterative.py`](iterative.py) ✓ |
| Recursive: thread carry as explicit accumulator | O(max(m, n)) time, O(max(m, n)) space (stack) | [`recursive.kara`](recursive.kara) ✓ | [`recursive.py`](recursive.py) ✓ |

`✓` runs end-to-end today under both `karac run` and `karac build`.

## Why both?

Reverse-order digit storage makes addition local — no normalisation pass is needed. At each position you have at most three inputs (digit-of-a, digit-of-b, carry-from-below) summing into `[0, 27]`; emit `sum % 10`, propagate `sum / 10`. The iterative form expresses this with a dummy-head + `tail` cursor; the recursive form expresses the same recurrence directly as `add(a, b, carry) = cons(s % 10, add(a.next, b.next, s / 10))`. Recursive is tail-call-shaped but Kāra doesn't currently guarantee TCO — at the ≤100-digit constraint, stack depth is bounded and either is safe.

## Kāra features exercised

- **`shared struct ListNode { val: i64, mut next: Option[ListNode] }`** — self-referential RC-backed node with a mutable tail link, enabling left-to-right list construction via a `tail` cursor.
- **`Option[ListNode]` + `if let Some(n) = a`** — flat per-list peek without a four-arm `match (a, b)` (three of those arms would share code).
- **`String.push_str` accumulation** — `to_string` appends in place (`s.push_str(f"{node.val}")`), amortized O(1) per node. The pre-2026-06 form was f-string self-append (`s = f"{s}, {node.val}"`) — the only idiom before `push_str` landed (karac `7ef42b9`), but O(n²) since each append re-copies the whole buffer; kata [#71](../71-simplify-path/) measured and killed that shape. (`String + String` still doesn't typecheck — `+` is registered as arithmetic.)
- **Tail-recursive shape in `recursive.kara`** — recursive call sits in the `next` field; tail-position by source, not by codegen guarantee.

## Running

```bash
# Kāra (interpreter — works today)
karac run iterative.kara
karac run recursive.kara

# Python
python3 iterative.py
python3 recursive.py
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # also needs rustc, clang, go, karac
./bench/bench.sh
```

`bench/bench.sh` follows the [kara-katas bench protocol](../../../BENCH.md): builds same-algorithm mirrors in Kāra, Rust, C, Go (and Python, optional), checks they print the same stdout sink, then times them with hyperfine. Seq-only — each `add_two_numbers` call is independent but per-call work (~100 small heap allocs + linear walk) is too small to amortize par-dispatch, so the kata measures pure codegen quality.

| File | What it does |
|---|---|
| [`bench/iterative.kara`](bench/iterative.kara) | N=100 nine-digit lists built once; K=500_000 iterations of `add_two_numbers(l1, l2)` with sum-of-first-digit sink |
| [`bench/iterative.rs`](bench/iterative.rs) | Algorithmic mirror; uses `Rc<RefCell<ListNode>>` to mirror Kāra's `shared struct` reference semantics; compiled with `rustc -O` |
| [`bench/iterative.c`](bench/iterative.c) | Algorithmic mirror; plain `malloc`/`free` per-node — no RC, no GC; compiled with `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | Algorithmic mirror; GC-managed pointer-linked nodes; compiled with `go build` |
| [`bench/iterative.py`](bench/iterative.py) | Algorithmic mirror — same N, K, sink |

All mirrors print `4000000` (500_000 × 8 — the units digit of 999…9 + 999…9 = 1999…98 is 8, and that's the first digit of the reversed-storage result).

### Runtime — seq lane

Snapshot — M5 Pro, 2026-05-31, hyperfine `--warmup 5 --runs 30 --shell=none`, native binaries via `karac build`, `rustc -O`, `clang -O3`, `go build`. Kara binary verified seq via `nm -gU target/iterative_kara | grep karac_par_run` (no auto-par symbols present) per BENCH.md § Implicit auto-par. Earlier today this kata's default-build binary carried a wasteful 2-stmt par-group activation on the prologue (`let b = make_nines(n); let l1 = from_array(a.as_slice());`); the karac per-stmt cost gate landed at `1a26792` (see [`phase-7-codegen.md`](../../../../karac-rust/docs/implementation_checklist/phase-7-codegen.md) § "Auto-par `karac_par_run`") closed it cleanly — binary dropped 311.9 → 49.0 KiB and peak RSS 1.6 → 1.1 MiB (matching C/Rust parity). Wall-time difference was within σ on the 500 ms range (~7 ms dispatch overhead absorbed by measurement noise); the headline wins are the binary and memory footprint.

| Implementation | Wall time | User-CPU | Within-workload ratio |
|---|---|---|---|
| c    iterative (clang -O3)       | 472.7 ms ± 91.3 ms     | 444.1 ms | 0.79× of Kāra |
| go   iterative                   | 501.6 ms ± 24.3 ms     | 523.5 ms | 0.84× of Kāra |
| **kāra iterative (codegen)**     | **601.0 ms ± 69.2 ms** | 583.6 ms | **1.00×** (baseline) |
| rust iterative (`Rc<RefCell>`)   | 934.7 ms ± 81.8 ms     | 913.9 ms | 1.56× of Kāra |

This snapshot ran under heavier machine load than the prior one — note the wide σ (C at ±91 ms, ~19%); every absolute number is up from earlier runs while the deterministic metrics (binary, compile, RSS below) are unchanged. Read the *relative* ordering, not the third digit.

Allocator-bound + RC-discipline-bound shape: a hot inner loop walking and growing a chain of ~100 small heap nodes, then dropping the chain when the result goes out of scope. **Kāra is 1.56× faster than Rust's `Rc<RefCell<>>`**, and trails C and Go — which pay no per-node refcount cost — on this lane. The win over Rust comes from two karac codegen optimizations specifically targeting `Option[shared T]` linked-list shapes:

1. **Niche layout for `Option[shared T]` struct fields** (2026-05-22): the field stores a single nullable pointer (null = `None`, non-null = `Some`) instead of the conventional 4-i64 `{tag, w0, w1, w2}` enum. Per-node heap size for `ListNode { val: i64, mut next: Option[ListNode] }` drops from 48 bytes to 24 bytes — same shape Rust gets for free on `Option<Rc<T>>` but `Rc<RefCell<>>` doesn't (the `RefCell` borrow-counter inflates the inner type past pointer-sized).
2. **Iterative drop for self-referential single-field shapes** (2026-05-22): the drop function for a shared struct whose only heap-owning field is `Option[Self]` (niche-optimized) emits a while-loop with inlined rc-dec on the chain pointer instead of one recursive `dec_ref` call per link. For a 100-node chain freed 500K times that's 50M function calls collapsed into 50M loop iterations of straight-line IR. **This is what closed the gap on this kata.**

C still leads by 1.27× — that's the cost of `shared struct`'s refcount header (8 bytes per node + the inline dec arithmetic) vs C's single-owner `malloc`/`free`, on a workload where every alloc is paired with a drop and the chain head is the sole owner. Go's bump-pointer young-generation allocator + amortized GC sweep lands between C and Kāra. Python runs the same shape in a tree-walking interpreter ~9.7× slower than Kāra.

(An even earlier snapshot of this kata reported 358 ms / 2.53× faster than Rust; that number measured the kernel correctly but the `karac` runtime was leaking the result chain on every iteration — peak RSS climbed to 2.3 GiB. After closing that leak the memory-correct number was 832 ms / 1.06× faster than Rust; the niche-layout + iterative-drop pair brought it to the 545 ms / 1.62× number on 2026-05-22, and a higher-load 2026-05-31 snapshot lands at 601 ms / 1.56× faster than Rust — wider σ across all four languages but the relative story unchanged.)

### Runtime — long workloads (Python)

Same snapshot, hyperfine `--warmup 2 --runs 10 --shell=none`:

| Run | Mean ± σ |
|---|---|
| `py iterative` | 5.819 s ± 0.190 s |

Python is **9.7× slower** than Kāra codegen on this workload — the gap CPython opens against any compiled-with-codegen language at workload sizes where algorithm time dominates interpreter-startup floors.

### Compile elapsed (cold)

Snapshot — M5 Pro, 2026-05-31, hyperfine `--warmup 1 --runs 10 --shell=none` with `--prepare` deleting the artifact before each run:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `iterative` | **79.9 ± 1.8 ms** | 111.5 ± 2.4 ms | 47.0 ± 1.4 ms |

`karac build` is **1.40× faster than `rustc -O`** on this file, sitting between clang (the floor for an LLVM-backed single-file compile) and rustc (which carries more frontend work per file). Multi-file projects (Go modules, Cargo) are deliberately excluded from this table — first-invocation `go build` and `cargo build` mix dep resolution + link and aren't comparable to a single-file `karac`/`rustc`/`clang` invocation.

### Binary size

| Implementation | Size |
|---|---|
| c    iterative | 32.9 KiB |
| **kāra iterative** | **32.9 KiB** |
| rust iterative | 456.3 KiB |
| go   iterative | 2434.1 KiB |

Kāra now sits **within ~80 bytes of clang's binary** — essentially at parity. Down from 311.9 KiB → 49.0 KiB after the karac cost gate (`1a26792`) elided a wasteful 2-stmt par-group activation that was carrying ~263 KiB of `karac_par_run` machinery + thread-pool init, then down to 32.9 KiB after the `__TEXT,__jittmpl` segment re-scope (`e76f42b`, 2026-05-25) reclaimed an additional 16 KiB per Mach-O binary. The `shared struct` machinery (RC inc/dec, niche-optimized `Option[shared T]`, iterative drop walker) is still statically linked; Rust pays the same kind of `Rc`/`RefCell` static-link cost but at a higher baseline. Go's ~2.4 MiB on every binary is the Go runtime + GC + reflection — a deliberate Go design choice, not workload-driven.

### Runtime memory (peak, RSS)

| Implementation | Peak |
|---|---|
| c    iterative | 1.1 MiB |
| **kāra iterative (codegen)** | **1.1 MiB** |
| rust iterative | 1.1 MiB |
| py   iterative | 9.3 MiB |
| go   iterative | 9.4 MiB |

Kāra now sits at **parity with C and Rust** on peak RSS — down from 1.6 MiB pre-fix (the par-pool initialization paid by the wasteful `karac_par_run` activation). The karac cost gate at `1a26792` elides the activation at codegen so the pool init never runs, returning kara to the per-iteration allocate-then-drop steady-state footprint that the workload's algorithmic shape actually requires. Go's baseline includes the runtime + GC; Python's includes the CPython interpreter.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 iterative.c | 2.6 MiB |
| karac build iterative.kara | 11.1 MiB |
| rustc -O iterative.rs | 31.9 MiB |

`karac` compiles this file in **~11 MiB peak** — between clang and rustc, with no algorithmic blowup signature. Go is omitted from the compile-memory row per BENCH.md — `go build`'s first invocation mixes module resolution + std-lib link and isn't comparable to a single-file invocation.

### Why this kata is in the harness

Add Two Numbers is the canonical "small-object allocator and reference-semantics" entry: a tight inner loop that walks one heap chain, builds another, and drops it. This is where `shared struct` vs `Rc<RefCell<>>` vs raw `malloc` vs GC actually show up — not in tight numeric kernels (where they all compile to the same instructions) but in workloads where heap discipline dominates. The seq lane here is the load-bearing reference-semantics measurement; the C row is what the same algorithm costs without RC at all.
