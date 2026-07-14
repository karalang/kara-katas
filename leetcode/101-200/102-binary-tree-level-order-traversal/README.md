# 102. Binary Tree Level Order Traversal

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Tree · Breadth-First Search · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/binary-tree-level-order-traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/)

Return the node values **grouped by depth** — row 0 is the root, row 1 its children left to right, row 2 their children, and so on down the tree.

```
      3               level order:
     / \                [3],
    9  20                [9, 20],
       / \               [15, 7]
      15  7
```

**Constraints:** `0 ≤ #nodes ≤ 2000`, node values fit `-1000 … 1000`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **DFS carrying the depth** ★ | [`level_order.kara`](level_order.kara) ✓ | [`level_order.py`](level_order.py) ✓ |
| **Level-by-level DFS (height + per-depth collect)** | [`level_order_bylevel.kara`](level_order_bylevel.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for both approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the two Kāra approaches agree with **each other** and with the Python mirror. An independent **ground-truth check** confirms the traversal: the DFS-with-depth level order equals a genuinely different **BFS** level order — a queue that dequeues a whole level per iteration — on a case battery **and on 20,000 randomised fuzz trees**, zero mismatches. Both solvers compile with zero diagnostics.

## Two ways to reach level order

Both produce the same `Vec[Vec[i64]]`; they differ in how they visit the tree.

**DFS carrying the depth** ([`level_order.kara`](level_order.kara), the ★): a single depth-first walk suffices if each node knows its depth. Keep one output row per depth; when a node at depth `d` is visited, append its value to row `d` (creating that row the first time depth `d` is reached). Because DFS visits a node before either child and the left child before the right, each row fills strictly left to right — exactly level order, in O(n) with no queue.

```
dfs(node, depth, result):
    node is None          -> return
    depth == result.len() -> result.push(new row)      // first time we reach this depth
    result[depth].push(node.val)
    dfs(node.left,  depth+1, result)
    dfs(node.right, depth+1, result)
```

**Level-by-level DFS** ([`level_order_bylevel.kara`](level_order_bylevel.kara)): first compute the tree's `height` by recursion, then for each depth `d` in `0 .. height` run a `collect_level(node, target=d, cur=0, row)` DFS that descends to exactly depth `d` and appends the nodes it finds there. A distinct mechanism — one pass *per level* that never grows rows on the fly — which must land on the identical grouping the depth-indexed single pass produces.

## Kāra features exercised

- **`shared struct TreeNode` (RC) with mutable fields** — `mut left` / `mut right`; the BST is built by `insert` threading shared handles, then walked read-only. Node type mirrors kata [#100](../../1-100/100-same-tree/) / [#99](../../1-100/99-recover-binary-search-tree/) / [#98](../../1-100/98-validate-binary-search-tree/).
- **`mut ref Vec[Vec[i64]]` accumulator, grown mid-recursion** — the DFS threads the nested result through recursive calls as a `mut ref`, pushing a fresh inner `Vec.new()` the first time each depth is reached and `result[depth].push(...)`-ing into it. Forwarding a `mut ref` parameter to the recursive calls **drops** the call-site `mut` marker (the value is already a mutable borrow in scope) — the natural nested-Vec-accumulator shape.
- **Nested `Vec` index + push** — `result[depth].push(n.val)` pushes onto an inner `Vec` reached by index of the outer `Vec`, the two-level container write at the heart of the problem.
- **`Option[shared]` niche match on the recursion** — each step matches the `Option[TreeNode]` child handle (`None` bottoms out, `Some(n)` descends), passing the shared node **by value** (a cheap RC-handle pass).

**v1 note.** Trees stay within the `≤ 2000`-node constraint. The sink folds each tree's level structure — level count, each level's size, and every value in order — into a running polynomial hash. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the BFS-equality + fuzz ground truth.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   level_order.kara
karac build level_order.kara && ./level_order

# The level-by-level variant (identical output):
karac run level_order_bylevel.kara

# Python
python3 level_order.py

# Verify they all agree
diff <(karac run level_order.kara) <(python3 level_order.py)              && echo OK
diff <(karac run level_order.kara) <(karac run level_order_bylevel.kara)  && echo OK

# Ground truth: DFS-with-depth level order == independent BFS level order (battery + 20k fuzz)
python3 ground_truth.py
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`level_order.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** The canonical numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json). The corpus's canonical **Apple M5 Pro** numbers ([`bench/results.json`](bench/results.json)) are folded in separately; absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. Re-run `bench.sh` on the M5 to refresh the canonical table.

**Workload.** Build 8 distinct 15-node BSTs once (rotating the insert order changes each shape), then **K = 1,500,000** reps of DFS-with-depth `level_order` on a **data-dependent-selected** tree (`idx = acc%8`, seeded by the running hash, so nothing hoists), folding the whole result — level count, each level's size, and every value — into a rolling polynomial hash. Unlike the read-only-traversal siblings, **each rep allocates a fresh nested result** (Kāra `Vec[Vec[i64]]`, C an array of `realloc`-grown rows freed per rep, Rust `Vec<Vec<i64>>`, Go `[][]int64`), so the workload is **allocation-bound** — the per-rep cost is dominated by building and tearing down the nested container, not the tree walk. Each mirror uses its natural node: Kāra `shared` (RC), C/Go raw pointer, **Rust `Box` + `&`-borrow** (the tree is never mutated or shared during traversal). All five compiled mirrors must agree on `959820311` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../../1-100/69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **x86-64 container numbers** (canonical M5 pending; see the machine note):

| Implementation | Wall time | Node / result representation |
|---|---|---|
| c    level_order (clang -O3)                        | 441.4 ± 15.0 ms | `malloc` pointer + `realloc` rows |
| **kāra level_order**                                | **589.7 ± 10.1 ms** | **`shared` (RC) + `Vec[Vec]`** |
| rust level_order (rustc -O, overflow-checks=on)      | 600.8 ± 13.0 ms | `Box` + `Vec<Vec>` |
| rust level_order (rustc -O)                         | 607.2 ± 16.8 ms | `Box` + `Vec<Vec>` |
| go   level_order (GC)                               | 1198.1 ± 34.0 ms | `*Node` + `[][]int64` (GC) |

**On an allocation-bound nested-container workload, Kāra lands second — ahead of both Rust and Go.** Every rep builds and tears down a fresh `Vec[Vec[i64]]`, so the per-rep cost is dominated by the nested-container churn, not the read-only walk. Against its semantic peer Rust — `Box` node walked by `&`-borrow, `Vec<Vec<i64>>` result — Kāra is **1.03× ahead** (590 vs 607 ms; 590 vs 601 with overflow-checks on): the two are the same shape (bump-allocate an outer vector of inner vectors, grow each inner on push, free the lot), and here Kāra's allocator path holds even with the per-node RC inc/decs the borrow-based Rust walk skips — because the *allocation* is the cost, and the RC traversal tax is small beside it (the inverse of read-only sibling [#100](../../1-100/100-same-tree/), where the walk *was* the whole cost and the RC tax showed). **Go is 2.03× behind Kāra** (1198 ms): its GC pays heavily on the 1.5 M × (outer slice + N inner slices) allocation churn — deferred collection is the wrong trade when the workload is nothing but short-lived nested allocations — and it is the *slowest* here, the mirror image of the read-only siblings where Go's GC pointer chase beat Kāra's RC. **C is the metal floor** at 441 ms (**1.34× ahead of Kāra**): raw `malloc`/`realloc`/`free` with no refcount and no GC. So the ordering is by allocator overhead on nested short-lived containers — raw malloc < **Kāra RC/Vec** < Rust `Box`/`Vec` < Go GC — a genuinely different regime from the read-only-traversal katas, and the alloc-heavy shape is exactly where Kāra's arena-friendly `Vec` growth pulls ahead of Rust. Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`) over the run. Python is listed at **314 ms but ran K = 75,000 — 1/20 of the compiled iterations** (pure-Python recursion is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **2.3 MiB** peak RSS (parity with Rust's 2.1 MiB, above C's 1.5 MiB) vs Go's **7.1 MiB**. The kāra binary measures **336 KiB** here — a build-linkage artifact of this container run (heap-growing programs retain the backtrace-symbolizer tree `--gc-sections` should strip; a correct build is ~15 KiB), independent of the runtime numbers, flagged for the M5 — vs C's 16 KiB and Go's 2.2 MiB.

**Flagged for the M5 re-bench** — Kāra's lead over Rust here is narrow (1.03×) and the corpus has seen container tree orderings shift on the M5's wider core (see [#97](../../1-100/97-interleaving-string/), [#99](../../1-100/99-recover-binary-search-tree/)), so treat the Kāra-ahead-of-Rust *margin* as a data point, not a verdict; the Go-slowest and C-floor signs are robust.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference) and, once folded in, [`bench/results.json`](bench/results.json) (M5, canonical).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched **nested-container allocation** (`Vec[Vec[i64]]` vs `Vec<Vec<i64>>`, both over a by-reference tree walk), the honest comparison for a build-a-fresh-grouping-per-rep workload. C's raw `malloc`/`realloc` is the metal floor, Go the GC data point (slowest here, on nested-slice churn), Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
