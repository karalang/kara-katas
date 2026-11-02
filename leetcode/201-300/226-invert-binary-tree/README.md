# 226. Invert Binary Tree

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Tree, DFS, BFS &nbsp;·&nbsp; **Source:** [leetcode.com/problems/invert-binary-tree](https://leetcode.com/problems/invert-binary-tree/)

Given the root of a binary tree, invert the tree (mirror every node's two children) and return its root.

**Constraints:** `0 ≤ nodes ≤ 100`, `-100 ≤ Node.val ≤ 100`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Recursive DFS (post-order swap) | O(n) time, O(h) stack | [`recursive.kara`](recursive.kara) ✓ via `karac run` | [`recursive.py`](recursive.py) ✓ |
| Iterative BFS (queue + in-place swap) | O(n) time, O(w) queue | [`iterative.kara`](iterative.kara) ✓ via `karac run` | [`iterative.py`](iterative.py) ✓ |

`✓` runs end-to-end today. `h` is tree height; `w` is max width.

### Why both?

Recursive DFS is the textbook formulation — three lines if you let the language carry the stack. Iterative BFS is the "what if `n = 10⁵` and the tree degenerates to a chain" answer: a queue caps memory at `O(w)` instead of letting the call stack grow to `O(n)`. Both are O(n) wall-clock; the choice is which auxiliary space you'd rather spend.

The two approaches also exercise different Kāra surface area — recursive uses self-call + Option pattern matching; iterative uses `VecDeque`, in-place field mutation through `shared struct` reference semantics, and a `loop { match queue.pop_front() { ... } }` drain idiom.

## Kāra features exercised

- **`shared struct` with mutable fields** — RC-backed reference semantics; `node.left = …` mutates through the shared handle without `Rc<RefCell<…>>`.
- **Recursive types via `Option[Self]`** — no `Box[T]` needed; `shared` already implies heap indirection.
- **Pattern matching on `Option`** — `match` plus `if let Some(x) = …` shorthand.
- **`VecDeque`** — `push_back`, `pop_front`, and the `loop { match pop_front() { … } }` drain idiom.

## Bug ledger

**Surfaced [`B-2026-06-15-1`](../../../../kara/docs/bug-ledger.md)** (memory-safety, fixed `0f78fc4f`). `build_tree` builds a `Vec[TreeNode]` of shared structs and links them via `cur.left = Some(nodes[i])` — but a bare-`shared` Vec element read into an enum-ctor payload (`Some(nodes[i])`) wasn't rc-incremented, so the node was freed when the `Vec` dropped while still referenced as a tree child. Output was non-deterministic garbage / a crash (C / Rust / Go all correct), which is exactly how this kata caught it. The fix rc-incs the aliased element; the seq/iterative sinks became the deterministic `2666665501` (superseded — see below).

## Benchmark workload — corrected 2026-08-12

`bench/`'s tree generator branched on the low bit of a power-of-two-modulus LCG. With an odd multiplier and odd increment that bit is **guaranteed** to alternate with period 2 — a property of the recurrence, not of the seed — so the "random walk" descended left, right, left, right forever and built a **zig-zag path of depth 1000 and BFS width 2**, not the balanced tree `results.json` claimed. The kata was measuring a 1000-deep linked-list walk, and its recursive variant was recursing 1000 frames deep.

Fixed by branching on bit 16, the convention katas #26/#27/#238 already use (#238's comment calls out this exact hazard). The tree is now **depth 14, max width 602**, and the sink moved `2666665501` → **`2494362254`**.

All five languages carried the same defect and were corrected together, so the cross-language comparison was never unfair — but the kata was not exercising what it documented. Verified byte-identical across C, Rust, Go, Python and Kāra on all three Kāra surfaces (`karac run`, `karac run --interp`, `karac build` default auto-par, and `KARAC_AUTO_PAR=0`).

**The committed bench numbers predate this change and are not comparable.** A canonical-host re-measure is required; until then the changed workload+sink makes `scripts/bench-compare.py` exclude #226 from every ratio by design.

*2026-11-02: re-measured on the canonical host (M5 Pro, karac g6697158fa) on the corrected workload — see § Benchmarks.*

## Running

```bash
# Kāra
karac run recursive.kara
karac run iterative.kara

# Python (3.10+ for PEP 604 union syntax)
python3 recursive.py
python3 iterative.py
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`recursive.{kara,rs,c}` / `iterative.{kara,rs,c}`, `go-seq/main.go`). The Python mirror is gated behind `KARA_BENCH_INCLUDE_PY=1`.

**Workload.** N = 2000-node random BST (bit-16 LCG; depth 14, max width 602) built once at startup; K = 10 outer iterations, each invokes `invert(root)` and then a `bfs_sink(root)` walk over the inverted tree to keep the work observable. The per-iter sink (`bfs_sink`) prevents the optimizer from eliding the K loop, and the alternating invert/sink pattern keeps cache footprint bounded. The sink line — one integer, the sum of all node values seen across iterations — must agree across all eight binaries (kara/rust/c/go × recursive/iterative) before timing starts; `bench.sh` fails loudly on mismatch.

### Runtime

M5 Pro, 2026-11-02, karac g6697158fa (0.9.0-dev.14057, the v2/MIR backend), sequential lane (`KARAC_AUTO_PAR=0`), hyperfine `--warmup 5 --runs 30 --shell=none`:

| Implementation | Recursive | Iterative |
|---|---|---|
| c    (clang -O3)  | 1.34 ± 0.07 ms | 1.35 ± 0.10 ms |
| rust              | 1.54 ± 0.06 ms | 1.59 ± 0.07 ms |
| rust (`-C overflow-checks=on`, equal-safety) | 1.59 ± 0.08 ms | 1.59 ± 0.17 ms |
| **kāra (codegen)** | **1.84 ± 0.13 ms** | **1.82 ± 0.11 ms** |
| go                | 2.05 ± 0.10 ms | 2.06 ± 0.09 ms |
| py                | 87.5 ± 1.5 ms *(last measured 2026-05-25, not re-run)* | 87.9 ± 1.2 ms *(last measured 2026-05-25, not re-run)* |

Kāra reads 1.19× / 1.15× `rustc -O` (recursive / iterative), 1.15× / 1.14× the equal-safety Rust row, 1.37× / 1.35× C, and 0.90× / 0.88× Go. These are whole-process timings of 1.3–2.1 ms, of which the 2000-node × 10-pass tree work is a small part, so the run is startup-dominated and the gaps between languages are mostly process start, not tree traversal. For the same reason the move against the 2026-07-28 feed (Kāra/Rust 1.14× → 1.19× recursive, 1.01× → 1.15× iterative, from the legacy backend and the pre-2026-08-12 zig-zag workload) is flat within noise. The Python rows are 2026-05-25 readings on the old workload (the py mirrors are gated behind `KARA_BENCH_INCLUDE_PY=1` and were not re-run).

> **2026-06-05 snapshot, first bench since the shared-struct refcount fixes.** The kāra binaries rebuilt at ~33.3 KiB but **not byte-identical** to the 2026-05-25 artifacts — expected: this kata's per-node `shared struct` traffic goes straight through the codegen paths changed by the four cursor-UAF refcount fixes (karac `a98149b9` + `fca1e3ea`, incl. per-branch flow-sensitive tail compensation). Wall time reproduced within σ on both approaches, so the corrected refcounting cost **nothing** on this tree workload.

The `shared struct` RC inc/dec on every node visit is the same kind of cost Rust's `Rc<RefCell<Node>>` carries; C's manual pointer-based trees skip the RC bookkeeping entirely. At this workload size neither effect is separable from process startup.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`, 2026-11-02:

| Compiler | Recursive | Iterative |
|---|---|---|
| clang -O3             | 52.8 ± 0.9 ms | 56.3 ± 0.6 ms |
| **karac build**       | **140.4 ± 2.1 ms** | **146.8 ± 2.7 ms** |
| rustc -O              | 145.7 ± 3.7 ms | 151.6 ± 4.3 ms |

`karac build` is ~1.03× faster than `rustc -O` and ~2.6× behind clang on this kata.

### Binary size

| Implementation | Recursive | Iterative |
|---|---|---|
| c    | 32.8 KiB | 32.7 KiB |
| **kāra** | **295.8 KiB** | **295.8 KiB** |
| rust | 457.4 KiB | 457.3 KiB |
| go   | 2434.2 KiB | 2434.2 KiB |

Every v2/MIR Kāra binary is ~300–390 KB where the legacy backend's were ~34 KB (this kata's were 33.3 KiB, within ~200 bytes of clang), tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). Rust pays the `Rc`/`RefCell` static-link cost at a higher baseline. Go's ~2.4 MiB is the runtime + GC + reflection on every binary.

### Runtime memory (peak, RSS)

| Implementation | Recursive | Iterative |
|---|---|---|
| c    | 1.1 MiB | 1.2 MiB |
| **kāra (codegen)** | **1.3 MiB** | **1.3 MiB** |
| rust | 1.2 MiB | 1.3 MiB |
| go   | 2.8 MiB | 3.2 MiB |
| py   | 9.4 MiB *(last measured 2026-05-25, not re-run)* | 9.4 MiB *(last measured 2026-05-25, not re-run)* |

Kāra sits 10 / 8 16-KiB pages above C (recursive 1,327,440 B vs 1,163,576 B; iterative 1,343,824 B vs 1,212,728 B), 5 pages above Rust on recursive, and level with Rust on iterative (1,343,824 B vs 1,343,800 B). These are single-shot `/usr/bin/time -l` readings, so individual cells wobble at page granularity between snapshots. The 2000-node tree allocates ~80 KiB of node memory; the rest is process baseline. Same shape as kata [#88](../../1-100/88-merge-sorted-array/#runtime-memory-peak).

### Compile memory (cold)

| Compiler invocation | Recursive | Iterative |
|---|---|---|
| `clang -O3`           |  2.6 MiB |  2.5 MiB |
| `rustc -O`            | 34.1 MiB | 34.3 MiB |
| **`karac build`**     | **61.9 MiB** | **62.3 MiB** |

`karac build` peaks at ~1.8× `rustc -O` and ~24× clang on this kata (the 2026-06-05 snapshot read 14.4 / 14.5 MiB, below rustc).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../../1-100/1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), and on this kata the comparison is unusually direct — Kāra's `shared struct` and Rust's `Rc<RefCell<Node>>` are the same memory-management strategy. C calibrates the no-RC floor, Go is the cross-runtime data point, and Python is the ergonomic foil.
