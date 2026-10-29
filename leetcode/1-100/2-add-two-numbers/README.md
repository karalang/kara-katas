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
<!-- bench-staleness -->

### How to run

```bash
brew install hyperfine    # also needs rustc, clang, go, karac
./bench/bench.sh
```

`bench/bench.sh` follows the [kara-katas bench protocol](../../../BENCH.md): builds same-algorithm mirrors in Kāra, Rust, C, Go (and Python, optional), checks they print the same stdout sink, then times them with hyperfine. Seq-only — each `add_two_numbers` call is independent but per-call work (~100 small heap allocs + linear walk) is too small to amortize par-dispatch, so the kata measures pure codegen quality.

| File | What it does |
|---|---|
| [`bench/iterative.kara`](bench/iterative.kara) | N=100 nine-digit lists built once; K=500_000 iterations of `add_two_numbers(l1, l2)` with sum-of-first-digit sink |
| [`bench/iterative.rs`](bench/iterative.rs) | Algorithmic mirror; uses `Rc<RefCell<ListNode>>` to mirror Kāra's `shared struct` reference semantics; compiled with `rustc -O` (and `-C overflow-checks=on` for the equal-safety row) |
| [`bench/iterative.c`](bench/iterative.c) | Algorithmic mirror; plain `malloc`/`free` per-node — no RC, no GC; compiled with `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | Algorithmic mirror; GC-managed pointer-linked nodes; compiled with `go build` |
| [`bench/iterative.py`](bench/iterative.py) | Algorithmic mirror — same N, K, sink |

All mirrors print `4000000` (500_000 × 8 — the units digit of 999…9 + 999…9 = 1999…98 is 8, and that's the first digit of the reversed-storage result).

### Runtime — seq lane

Snapshot — Apple M5 Pro (6P+12E), Darwin 25.6.0, measured 2026-10-29 (UTC), karac `0.1.0-dev.13686+g04628b0eb` — the v2/MIR backend, which replaced the legacy backend as the default codegen path on Oct 22. hyperfine `--warmup 5 --runs 30 --shell=none`, native binaries via `karac build`, `rustc -O` (rustc 1.95.0), `clang -O3` (Apple clang 21.0.0), `go build` (go 1.26.3). Since the v2 redesign `karac build` is sequential unless `KARAC_AUTO_PAR=1`, so the Kāra row is the seq lane by construction.

| Implementation | Wall time | User-CPU | Within-workload ratio |
|---|---|---|---|
| go   iterative                         | 455.6 ms ± 11.0 ms     | 468.4 ms  | 0.62× of Kāra |
| c    iterative (clang -O3)             | 592.0 ms ± 6.8 ms      | 586.5 ms  | 0.81× of Kāra |
| **kāra iterative (codegen)**           | **730.5 ms ± 13.3 ms** | 720.9 ms  | **1.00×** (baseline) |
| rust iterative (`-C overflow-checks=on`) | 1016.1 ms ± 14.5 ms  | 1007.6 ms | 1.39× of Kāra |
| rust iterative (`Rc<RefCell>`, `-O`)   | 1037.1 ms ± 29.3 ms    | 1022.6 ms | 1.42× of Kāra |

σ is tight across the board (≤2.9%), so the gaps are well outside noise.

**Kāra is 1.23× C on this lane, no longer at C parity.** The previous run (karac on the legacy backend) measured Kāra at 698.8 ms against C's 692.2 ms — 1.01×, parity. On this run Kāra is 730.5 ms against C's 592.0 ms. Part of that movement is C getting faster on this host, but part of it is a real Kāra regression: a matched same-commit instruction-count A/B on this kernel has the MIR backend executing 24.74 G instructions against the legacy backend's 21.45 G (+15%; cycles +17%). Tracked as B-2026-10-28-34. Kāra still runs ahead of both Rust rows — 0.70× of `rustc -O` and 0.72× of the equal-safety `rustc -O -C overflow-checks=on` (Kāra checks integer overflow by default) — and Go's bump-pointer young-generation allocator + amortized GC sweep leads the lane at 0.62× of Kāra.

#### Re-bench 2026-10-29 — what moved

| Metric | Previous run | This run | Change | Classification |
|---|---|---|---|---|
| Kāra runtime | 698.8 ms | 730.5 ms | +4.5% | **Regression** — MIR backend executes +15% instructions on this kernel; B-2026-10-28-34 |
| C runtime | 692.2 ms | 592.0 ms | −14.5% | Host drift (comparator) |
| Rust runtime (`-O`) | 1088.9 ms | 1037.1 ms | −4.8% | Host drift (comparator) |
| Go runtime | 445.0 ms | 455.6 ms | +2.4% | Host drift (comparator) |
| Kāra binary size | 34,312 B | 336,824 B | +302 KB | **Regression** — MIR binary floor; B-2026-10-28-36 |
| Kāra compile elapsed | 92.0 ms | 158.1 ms | +72% | **Regression** — rustc/clang flat (97.6 → 101.9 ms, 41.3 → 43.5 ms); B-2026-10-28-37 |
| Kāra compile peak RSS | 24.1 MiB | 67.8 MiB | +43.7 MiB | **Regression** — rustc/clang flat (31.8 → 31.6 MiB, 2.5 → 2.6 MiB); B-2026-10-28-37 |

The comparator moves are host drift: the same unchanged C, Rust and Go sources moved by −14.5% to +2.4% between runs. Kāra's runtime ratio against C moved from 1.01× to 1.23×; the instruction-count A/B is what separates the compiler's share of that from the host's.

How this kata got to parity in the first place — three generations of karac codegen work target exactly this `Option[shared T]` linked-list shape:

1. **Niche layout for `Option[shared T]` struct fields** (2026-05-22): the field stores a single nullable pointer (null = `None`, non-null = `Some`) instead of the conventional 4-i64 `{tag, w0, w1, w2}` enum. Per-node heap size for `ListNode { val: i64, mut next: Option[ListNode] }` drops from 48 bytes to 24 bytes — same shape Rust gets for free on `Option<Rc<T>>` but `Rc<RefCell<>>` doesn't (the `RefCell` borrow-counter inflates the inner type past pointer-sized).
2. **Iterative drop for self-referential single-field shapes** (2026-05-22): the drop function for a shared struct whose only heap-owning field is `Option[Self]` (niche-optimized) emits a while-loop with inlined rc-dec on the chain pointer instead of one recursive `dec_ref` call per link. For a 100-node chain freed 500K times that's 50M function calls collapsed into 50M loop iterations of straight-line IR. This is what closed the gap on Rust.
3. **RC elision — the headerless-chain ladder** (2026-06-06, karac `e6b810e0`): ownership analysis proves every `ListNode` in the program lives in a cluster its chain head solely owns — fresh literal links, builder-call adoption at the caller, borrowed-param walk families across `add_two_numbers`'s arguments — and a program-wide purity gate then drops the refcount word from the type's layout entirely. Nodes shrink 24 → 16 bytes (malloc size-class 32 → 16), builds are plain stores, walks are count-free, drops are a tag-guarded pointer-chase free loop. This is what closed the gap on C on the legacy backend.

The 1.23× C gap on this run is not a layout regression — peak RSS is still at C's figure (see below) — but extra instructions in the MIR backend's code for the same kernel (B-2026-10-28-34).

(Earlier history: a first snapshot reported 358 ms / 2.53× faster than Rust, but the runtime was leaking the result chain on every iteration — peak RSS climbed to 2.3 GiB. The memory-correct number was 832 ms / 1.06× faster than Rust; niche layout + iterative drop brought it to 545 ms / 1.62× on 2026-05-22, and the RC-elision ladder took it to C parity, with fork-point A/B probes attributing 531 → 403 ms (1.32× cumulative) to the ladder itself.)

### Runtime — long workloads (Python)

Python was not timed in this run — `bench/results.json` carries no Python row, so there is no current figure to report here. Run `./bench/bench.sh` with `python3` available to add it; on earlier snapshots CPython ran this shape roughly an order of magnitude slower than Kāra codegen.

### Compile elapsed (cold)

Same snapshot, hyperfine `--warmup 1 --runs 10 --shell=none` with `--prepare` deleting the artifact before each run:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `iterative` | **158.1 ± 6.1 ms** | 101.9 ± 1.5 ms | 43.5 ± 0.8 ms |

`karac build` is now **1.55× slower than `rustc -O`** on this file (and 3.63× clang). On the previous run it was 92.0 ms, faster than rustc's 97.6 ms; rustc and clang are flat across the two runs, so the +72% is Kāra's — tracked as B-2026-10-28-37. Multi-file projects (Go modules, Cargo) are deliberately excluded from this table — first-invocation `go build` and `cargo build` mix dep resolution + link and aren't comparable to a single-file `karac`/`rustc`/`clang` invocation.

### Binary size

| Implementation | Size |
|---|---|
| c    iterative | 32.9 KiB |
| **kāra iterative** | **328.9 KiB** |
| rust iterative | 456.3 KiB |
| go   iterative | 2434.1 KiB |

Kāra's binary is **336,824 bytes, up +302 KB** from the previous run, where it sat within a few hundred bytes of clang's 33,704. The kernel did not grow: the MIR backend links a larger fixed floor into every binary, tracked as B-2026-10-28-36. Kāra remains below Rust's `Rc`/`RefCell` static-link baseline. Go's ~2.4 MiB on every binary is the Go runtime + GC + reflection — a deliberate Go design choice, not workload-driven.

### Runtime memory (peak, RSS)

| Implementation | Peak |
|---|---|
| c    iterative | 1.0 MiB |
| **kāra iterative (codegen)** | **1.0 MiB** |
| rust iterative | 1.1 MiB |
| go   iterative | 9.3 MiB |

Kāra sits at **parity with C** on peak RSS (1,098,064 vs 1,098,040 bytes) and just under Rust — the per-iteration allocate-then-drop steady state the workload's algorithmic shape requires, with headerless 16-byte nodes. Go's baseline includes the runtime + GC. (Python is not in this run.)

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 iterative.c | 2.6 MiB |
| rustc -O iterative.rs | 31.6 MiB |
| karac build iterative.kara | 67.8 MiB |

`karac` now peaks at **~68 MiB** compiling this file — above rustc, up from 24.1 MiB on the previous run while rustc and clang are flat. Same regression as the compile-time row: B-2026-10-28-37. Go is omitted from the compile-memory row per BENCH.md — `go build`'s first invocation mixes module resolution + std-lib link and isn't comparable to a single-file invocation.

### Why this kata is in the harness

Add Two Numbers is the canonical "small-object allocator and reference-semantics" entry: a tight inner loop that walks one heap chain, builds another, and drops it. This is where `shared struct` vs `Rc<RefCell<>>` vs raw `malloc` vs GC actually show up — not in tight numeric kernels (where they all compile to the same instructions) but in workloads where heap discipline dominates. The seq lane here is the load-bearing reference-semantics measurement; the C row is what the same algorithm costs without RC at all.

## Calibration re-probe (2026-10-06)

Re-probed with new phrasings, on all four surfaces plus valgrind, as part of a ten-kata calibration batch (katas 1-49, against kata 352's probing). Gaps found, in the kara bug ledger:

- **B-2026-10-06-77** — a `let` bound to an `if` / `match` that chooses between two `ref` params is refused by `karac build`.
- **B-2026-10-06-78** — a `match` on a tuple literal of moved `shared` / heap-struct values leaks compiled (kata 23's merge-two-lists hit it again).
