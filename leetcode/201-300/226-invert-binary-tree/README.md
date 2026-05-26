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

**Workload.** N = 2000-node balanced tree built once at startup; K = 10 outer iterations, each invokes `invert(root)` and then a `bfs_sink(root)` walk over the inverted tree to keep the work observable. The per-iter sink (`bfs_sink`) prevents the optimizer from eliding the K loop, and the alternating invert/sink pattern keeps cache footprint bounded. The sink line — one integer, the sum of all node values seen across iterations — must agree across all eight binaries (kara/rust/c/go × recursive/iterative) before timing starts; `bench.sh` fails loudly on mismatch.

### Runtime

Snapshot — M5 Pro, 2026-05-25, hyperfine `--warmup 5 --runs 30 --shell=none`:

| Implementation | Recursive | Iterative |
|---|---|---|
| **kāra (codegen)** | **2.5 ± 0.2 ms** | **2.5 ± 0.2 ms** |
| rust              | 2.6 ± 0.1 ms | 2.6 ± 0.2 ms |
| c    (clang -O3)  | 2.1 ± 0.1 ms | 2.2 ± 0.2 ms |
| go                | 3.2 ± 0.1 ms | 3.3 ± 0.3 ms |
| py                | 87.5 ± 1.5 ms | 87.9 ± 1.2 ms |

Kāra matches Rust within σ and runs ~1.2× of clang's O3 — the gap is the inherent cost of the `shared struct` RC inc/dec on every node visit (Rust's `Rc<RefCell<Node>>` carries the same kind of cost; the two are at parity). C wins by ~20% because manual pointer-based trees skip the RC bookkeeping entirely. Go's GC-driven walker is ~30% slower than Kāra on the same shape. Python is **~35× slower than Kāra codegen** — the per-node bytecode dispatch dominates everything else.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Recursive | Iterative |
|---|---|---|
| **karac build**       | **64.0 ± 1.0 ms** | **66.2 ± 0.5 ms** |
| rustc -O              | 126.6 ± 0.8 ms | 130.7 ± 0.8 ms |
| clang -O3             | 43.8 ± 0.9 ms | 47.5 ± 1.1 ms |

Kāra compiles **1.97× faster than `rustc -O`** and sits ~1.4× behind clang — same shape as kata [#88](../../1-100/88-merge-sorted-array/#compile-time-and-binary-size).

### Binary size

| Implementation | Recursive | Iterative |
|---|---|---|
| c    | 32.8 KiB | 32.7 KiB |
| **kāra** | **32.9 KiB** | **32.9 KiB** |
| rust | 457.4 KiB | 457.3 KiB |
| go   | 2434.2 KiB | 2434.2 KiB |

Kāra is **within ~100 bytes of clang** — essentially at parity. The `shared struct` machinery (RC inc/dec, niche-optimized `Option[shared T]`, iterative drop walker) is statically linked but small; the cross-archive LTO + DCE pass strips runtime surface this workload doesn't reach (HTTP, JSON, tokio subgraph, `Map`, `String`, …). Rust pays the same `Rc`/`RefCell` static-link cost but at a much higher baseline. Go's ~2.4 MiB is the runtime + GC + reflection on every binary.

### Runtime memory (peak, RSS)

| Implementation | Recursive | Iterative |
|---|---|---|
| c    | 1.2 MiB | 1.2 MiB |
| **kāra (codegen)** | **1.2 MiB** | **1.2 MiB** |
| rust | 1.3 MiB | 1.2 MiB |
| go   | 3.3 MiB | 3.4 MiB |
| py   | 9.4 MiB | 9.4 MiB |

Kāra is **at parity with C** and ~100 KiB below Rust on the recursive variant. The 2000-node tree allocates ~80 KiB of node memory; the rest is process baseline. Same shape as kata [#88](../../1-100/88-merge-sorted-array/#runtime-memory-peak).

### Compile memory (cold)

| Compiler invocation | Recursive | Iterative |
|---|---|---|
| `clang -O3`           |  2.6 MiB |  2.6 MiB |
| **`karac build`**     | **9.8 MiB** | **10.1 MiB** |
| `rustc -O`            | 34.3 MiB | 34.4 MiB |

Kāra's compile-memory footprint is ~3.8× clang's and ~3.4× lower than rustc's on this kata.
