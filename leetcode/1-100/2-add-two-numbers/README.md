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

Snapshot — M5 Pro, 2026-06-06, hyperfine `--warmup 5 --runs 30 --shell=none`, native binaries via `karac build`, `rustc -O`, `clang -O3`, `go build`. Kara binary verified seq via `nm -gU target/iterative_kara | grep karac_par_run` (no auto-par symbols present) per BENCH.md § Implicit auto-par. This is the post-RC-elision-ladder re-bench: karac `e6b810e0` (2026-06-06) completed the eight-phase RC-elision program (see [`phase-7-codegen.md`](../../../../kara/docs/implementation_checklist/phase-7-codegen.md) § Phase C) — `ListNode` is 16 bytes/node here, down from 24, with zero refcount operations anywhere in the binary.

| Implementation | Wall time | User-CPU | Within-workload ratio |
|---|---|---|---|
| c    iterative (clang -O3)       | 397.3 ms ± 8.0 ms      | 394.5 ms | 0.98× of Kāra |
| **kāra iterative (codegen)**     | **404.1 ms ± 7.6 ms**  | 401.4 ms | **1.00×** (baseline) |
| go   iterative                   | 453.6 ms ± 5.8 ms      | 468.0 ms | 1.12× of Kāra |
| rust iterative (`Rc<RefCell>`)   | 804.7 ms ± 10.1 ms     | 800.4 ms | 1.99× of Kāra |

Light-load snapshot — σ is tight across the board (≤2.5%), so the absolute numbers are trustworthy this time. The C and Kāra distributions overlap (C 388.8–424.5 ms, Kāra 393.5–420.2 ms): **statistical parity**.

Allocator-bound + RC-discipline-bound shape: a hot inner loop walking and growing a chain of ~100 small heap nodes, then dropping the chain when the result goes out of scope. **Kāra is at parity with C (1.02 ± 0.03×) and 1.99× faster than Rust's `Rc<RefCell<>>`** on this lane. Three generations of karac codegen work target exactly this `Option[shared T]` linked-list shape:

1. **Niche layout for `Option[shared T]` struct fields** (2026-05-22): the field stores a single nullable pointer (null = `None`, non-null = `Some`) instead of the conventional 4-i64 `{tag, w0, w1, w2}` enum. Per-node heap size for `ListNode { val: i64, mut next: Option[ListNode] }` drops from 48 bytes to 24 bytes — same shape Rust gets for free on `Option<Rc<T>>` but `Rc<RefCell<>>` doesn't (the `RefCell` borrow-counter inflates the inner type past pointer-sized).
2. **Iterative drop for self-referential single-field shapes** (2026-05-22): the drop function for a shared struct whose only heap-owning field is `Option[Self]` (niche-optimized) emits a while-loop with inlined rc-dec on the chain pointer instead of one recursive `dec_ref` call per link. For a 100-node chain freed 500K times that's 50M function calls collapsed into 50M loop iterations of straight-line IR. This is what closed the gap on Rust.

3. **RC elision — the headerless-chain ladder** (2026-06-06, karac `e6b810e0`): ownership analysis proves every `ListNode` in the program lives in a cluster its chain head solely owns — fresh literal links, builder-call adoption at the caller, borrowed-param walk families across `add_two_numbers`'s arguments — and a program-wide purity gate then drops the refcount word from the type's layout entirely. Nodes shrink 24 → 16 bytes (malloc size-class 32 → 16), builds are plain stores, walks are count-free, drops are a tag-guarded pointer-chase free loop. No rc word and no count traffic anywhere in this binary. **This is what closed the gap on C.**

The C gap is closed: the refcount header and its maintenance were the remaining 1.27×, and the elision ladder removed both — same per-node bytes as C's `struct ListNode`, same malloc/free traffic, same walk. Go's bump-pointer young-generation allocator + amortized GC sweep now trails by 1.12×. Python runs the same shape in a tree-walking interpreter 13.2× slower than Kāra.

(An even earlier snapshot of this kata reported 358 ms / 2.53× faster than Rust; that number measured the kernel correctly but the `karac` runtime was leaking the result chain on every iteration — peak RSS climbed to 2.3 GiB. After closing that leak the memory-correct number was 832 ms / 1.06× faster than Rust; the niche-layout + iterative-drop pair brought it to the 545 ms / 1.62× number on 2026-05-22, and a higher-load 2026-05-31 snapshot landed at 601 ms / 1.56× faster than Rust. The RC-elision ladder then took it to C parity — fork-point A/B probes attribute 531 → 403 ms (1.32× cumulative) to the ladder itself, with the headerless-layout rung alone worth 1.20 ± 0.03× — and the 2026-06-06 low-load snapshot above measures 404.1 ms ± 7.6 against C's 397.3 ms ± 8.0 in the same run.)

### Runtime — long workloads (Python)

Same snapshot, hyperfine `--warmup 2 --runs 10 --shell=none`:

| Run | Mean ± σ |
|---|---|
| `py iterative` | 5.334 s ± 0.064 s |

Python is **13.2× slower** than Kāra codegen on this workload — the gap CPython opens against any compiled-with-codegen language at workload sizes where algorithm time dominates interpreter-startup floors.

### Compile elapsed (cold)

Snapshot — M5 Pro, 2026-06-06, hyperfine `--warmup 1 --runs 10 --shell=none` with `--prepare` deleting the artifact before each run:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `iterative` | **69.7 ± 1.3 ms** | 98.2 ± 1.1 ms | 43.6 ± 0.6 ms |

`karac build` is **1.41× faster than `rustc -O`** on this file, sitting between clang (the floor for an LLVM-backed single-file compile) and rustc (which carries more frontend work per file). Multi-file projects (Go modules, Cargo) are deliberately excluded from this table — first-invocation `go build` and `cargo build` mix dep resolution + link and aren't comparable to a single-file `karac`/`rustc`/`clang` invocation.

### Binary size

| Implementation | Size |
|---|---|
| c    iterative | 32.9 KiB |
| **kāra iterative** | **32.9 KiB** |
| rust iterative | 456.3 KiB |
| go   iterative | 2434.1 KiB |

Kāra's binary is now **byte-for-byte the same size as clang's** (33,704 bytes each — the elision ladder's free-walk loop added 48 bytes that landed exactly on clang's figure; equal size, not merely equal KiB rounding). Down from 311.9 KiB → 49.0 KiB after the karac cost gate (`1a26792`) elided a wasteful 2-stmt par-group activation that was carrying ~263 KiB of `karac_par_run` machinery + thread-pool init, then down to 32.9 KiB after the `__TEXT,__jittmpl` segment re-scope (`e76f42b`, 2026-05-25) reclaimed an additional 16 KiB per Mach-O binary. Since the elision ladder, this binary carries no RC machinery at all for `ListNode` (the purity gate passed program-wide — headerless nodes, free-walk drop); Rust still pays its `Rc`/`RefCell` static-link cost at a much higher baseline. Go's ~2.4 MiB on every binary is the Go runtime + GC + reflection — a deliberate Go design choice, not workload-driven.

### Runtime memory (peak, RSS)

| Implementation | Peak |
|---|---|
| c    iterative | 1.0 MiB |
| **kāra iterative (codegen)** | **1.1 MiB** |
| rust iterative | 1.1 MiB |
| py   iterative | 9.5 MiB |
| go   iterative | 9.6 MiB |

Kāra now sits at **parity with C and Rust** on peak RSS — down from 1.6 MiB pre-fix (the par-pool initialization paid by the wasteful `karac_par_run` activation). The karac cost gate at `1a26792` elides the activation at codegen so the pool init never runs, returning kara to the per-iteration allocate-then-drop steady-state footprint that the workload's algorithmic shape actually requires. Go's baseline includes the runtime + GC; Python's includes the CPython interpreter.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 iterative.c | 2.5 MiB |
| karac build iterative.kara | 12.1 MiB |
| rustc -O iterative.rs | 31.9 MiB |

`karac` compiles this file in **~12 MiB peak** — between clang and rustc, with no algorithmic blowup signature. (Up ~1 MiB from the 2026-05-31 snapshot — the known fixed-floor karac compile-memory growth, probe-confirmed workload-independent; output binary unchanged in behavior.) Go is omitted from the compile-memory row per BENCH.md — `go build`'s first invocation mixes module resolution + std-lib link and isn't comparable to a single-file invocation.

### Why this kata is in the harness

Add Two Numbers is the canonical "small-object allocator and reference-semantics" entry: a tight inner loop that walks one heap chain, builds another, and drops it. This is where `shared struct` vs `Rc<RefCell<>>` vs raw `malloc` vs GC actually show up — not in tight numeric kernels (where they all compile to the same instructions) but in workloads where heap discipline dominates. The seq lane here is the load-bearing reference-semantics measurement; the C row is what the same algorithm costs without RC at all.
