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

**Surfaced [`B-2026-06-15-1`](../../../../kara/docs/bug-ledger.md)** (memory-safety, fixed `0f78fc4f`). `build_tree` builds a `Vec[TreeNode]` of shared structs and links them via `cur.left = Some(nodes[i])` — but a bare-`shared` Vec element read into an enum-ctor payload (`Some(nodes[i])`) wasn't rc-incremented, so the node was freed when the `Vec` dropped while still referenced as a tree child. Output was non-deterministic garbage / a crash (C / Rust / Go all correct), which is exactly how this kata caught it. The fix rc-incs the aliased element; the seq/iterative sinks are now the deterministic `2666665501`.

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

Snapshot — M5 Pro, 2026-06-05, hyperfine `--warmup 5 --runs 30 --shell=none`:

| Implementation | Recursive | Iterative |
|---|---|---|
| **kāra (codegen)** | **3.8 ± 0.2 ms** | **4.0 ± 0.1 ms** |
| rust              | 4.3 ± 0.0 ms | 4.1 ± 0.1 ms |
| c    (clang -O3)  | 3.9 ± 0.2 ms | 3.3 ± 1.7 ms † |
| go                | 4.1 ± 0.1 ms | 4.2 ± 0.1 ms |
| py                | 87.5 ± 1.5 ms *(05-25)* | 87.9 ± 1.2 ms *(05-25)* |

† load-contaminated batch in this snapshot (hyperfine flagged statistical outliers; the min anchors near the same-shape clean readings — c iterative reads close to its 3.3 ms mean).

> **First bench since the shared-struct refcount fixes.** The kāra binaries rebuilt at ~33.3 KiB but **not byte-identical** to the 2026-05-25 artifacts — expected: this kata's per-node `shared struct` traffic goes straight through the codegen paths changed by the four cursor-UAF refcount fixes (karac `a98149b9` + `fca1e3ea`, incl. per-branch flow-sensitive tail compensation). Wall time reproduces within σ on both approaches, so the corrected refcounting costs **nothing** on this tree workload.

Kāra matches Rust within σ on both approaches — the `shared struct` RC inc/dec on every node visit is the same kind of cost Rust's `Rc<RefCell<Node>>` carries; the two are at parity. C's clean column (iterative) wins by ~1.2× because manual pointer-based trees skip the RC bookkeeping entirely. Go's GC-driven walker is ~1.05× slower than Kāra on the same shape (clean columns). Python is **~22× slower than Kāra codegen** (2026-05-25 readings; the py mirrors are gated behind `KARA_BENCH_INCLUDE_PY=1` and were not re-run) — the per-node bytecode dispatch dominates everything else.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Recursive | Iterative |
|---|---|---|
| **karac build**       | **81.5 ± 0.6 ms** | **84.2 ± 0.7 ms** |
| rustc -O              | 135.0 ± 0.6 ms | 139.8 ± 1.6 ms |
| clang -O3             | 46.4 ± 0.2 ms | 50.2 ± 0.4 ms |

Kāra compiles **1.66× faster than `rustc -O`** and sits ~1.7× behind clang — same shape as kata [#88](../../1-100/88-merge-sorted-array/#compile-time-and-binary-size). (The 2026-05-25 snapshot read `karac build` at 64.0 / 66.2 ms against the karac installed at the time; the May-30 karac reinstall plus the 06-05 environment band account for today's 76.2 / 78.1 — the same +11–14 ms shift seen across every kata re-benched on 06-05. rustc and clang both rebuilt their binaries **byte-identical** to May's, anchoring the environment as stable; rustc's own walls moved ≤3 ms.)

### Binary size

| Implementation | Recursive | Iterative |
|---|---|---|
| c    | 32.8 KiB | 32.7 KiB |
| **kāra** | **33.3 KiB** | **33.3 KiB** |
| rust | 457.4 KiB | 457.3 KiB |
| go   | 2434.2 KiB | 2434.2 KiB |

Kāra is **within ~200 bytes of clang** — essentially at parity. The `shared struct` machinery (RC inc/dec, niche-optimized `Option[shared T]`, iterative drop walker) is statically linked but small; the cross-archive LTO + DCE pass strips runtime surface this workload doesn't reach (HTTP, JSON, tokio subgraph, `Map`, `String`, …). Rust pays the same `Rc`/`RefCell` static-link cost but at a much higher baseline. Go's ~2.4 MiB is the runtime + GC + reflection on every binary. The kāra binaries now sit at 33.3 KiB after the seq-alloc codegen fix; C and Rust sizes are unchanged from the 2026-05-25 snapshot.

### Runtime memory (peak, RSS)

| Implementation | Recursive | Iterative |
|---|---|---|
| c    | 1.2 MiB | 1.1 MiB |
| **kāra (codegen)** | **1.2 MiB** | **1.1 MiB** |
| rust | 1.2 MiB | 1.2 MiB |
| go   | 3.2 MiB | 3.3 MiB |
| py   | 9.4 MiB *(05-25)* | 9.4 MiB *(05-25)* |

Kāra is **at parity with C** in both columns (recursive: byte-identical 1,212,704 B single-shot readings; iterative: one 16 KiB page apart) and a page or two below Rust. These are single-shot `/usr/bin/time -l` readings, so individual cells wobble at page granularity between snapshots — the 05-25 sample read rust recursive a page higher and go ~0.2 MiB higher. The 2000-node tree allocates ~80 KiB of node memory; the rest is process baseline. Same shape as kata [#88](../../1-100/88-merge-sorted-array/#runtime-memory-peak).

### Compile memory (cold)

| Compiler invocation | Recursive | Iterative |
|---|---|---|
| `clang -O3`           |  2.6 MiB |  2.6 MiB |
| **`karac build`**     | **14.4 MiB** | **14.5 MiB** |
| `rustc -O`            | 34.0 MiB | 34.3 MiB |

Kāra's compile-memory footprint is ~5.5× clang's and ~2.4× lower than rustc's on this kata. (The karac compile-mem band sits at 14.4 / 14.5 in this snapshot — compiler-internal working set with no effect on emitted output; rustc and clang read flat.)

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../../1-100/1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), and on this kata the comparison is unusually direct — Kāra's `shared struct` and Rust's `Rc<RefCell<Node>>` are the same memory-management strategy, so the within-σ tie is RC-traffic parity, not coincidence. C calibrates the no-RC floor (~1.2×), Go is the cross-runtime data point, and Python is the ergonomic foil.
