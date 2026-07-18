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
| **BFS frontier queue (`current = next`)** | [`level_order_bfs.kara`](level_order_bfs.kara) ✓ | — |
| **Level-by-level DFS (height + per-depth collect)** | [`level_order_bylevel.kara`](level_order_bylevel.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for all three approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the three Kāra approaches agree with **each other** and with the Python mirror. An independent **ground-truth check** confirms the traversal: the DFS-with-depth level order equals a genuinely different **BFS** level order — a queue that dequeues a whole level per iteration — on a case battery **and on 20,000 randomised fuzz trees**, zero mismatches. All three solvers compile with zero diagnostics and are valgrind-clean.

## Three ways to reach level order

All three produce the same `Vec[Vec[i64]]`; they differ in how they visit the tree.

**DFS carrying the depth** ([`level_order.kara`](level_order.kara), the ★): a single depth-first walk suffices if each node knows its depth. Keep one output row per depth; when a node at depth `d` is visited, append its value to row `d` (creating that row the first time depth `d` is reached). Because DFS visits a node before either child and the left child before the right, each row fills strictly left to right — exactly level order, in O(n) with no queue.

```
dfs(node, depth, result):
    node is None          -> return
    depth == result.len() -> result.push(new row)      // first time we reach this depth
    result[depth].push(node.val)
    dfs(node.left,  depth+1, result)
    dfs(node.right, depth+1, result)
```

**BFS frontier queue** ([`level_order_bfs.kara`](level_order_bfs.kara)): the textbook breadth-first solution. Hold the current level as a `Vec[TreeNode]` frontier, emit its values as one row, then build the *next* level by collecting every child of the frontier left-to-right and advancing `current = next`. Each outer iteration is exactly one tree level, so the rows come out in level order with no depth bookkeeping — the most direct statement of "level order" there is.

**Level-by-level DFS** ([`level_order_bylevel.kara`](level_order_bylevel.kara)): first compute the tree's `height` by recursion, then for each depth `d` in `0 .. height` run a `collect_level(node, target=d, cur=0, row)` DFS that descends to exactly depth `d` and appends the nodes it finds there. A distinct mechanism — one pass *per level* that never grows rows on the fly — which must land on the identical grouping the depth-indexed single pass produces.

## Kāra features exercised

- **`shared struct TreeNode` (RC) with mutable fields** — `mut left` / `mut right`; the BST is built by `insert` threading shared handles, then walked read-only. Node type mirrors kata [#100](../../1-100/100-same-tree/) / [#99](../../1-100/99-recover-binary-search-tree/) / [#98](../../1-100/98-validate-binary-search-tree/).
- **`mut ref Vec[Vec[i64]]` accumulator, grown mid-recursion** — the DFS threads the nested result through recursive calls as a `mut ref`, pushing a fresh inner `Vec.new()` the first time each depth is reached and `result[depth].push(...)`-ing into it. Forwarding a `mut ref` parameter to the recursive calls **drops** the call-site `mut` marker (the value is already a mutable borrow in scope) — the natural nested-Vec-accumulator shape.
- **Nested `Vec` index + push** — `result[depth].push(n.val)` pushes onto an inner `Vec` reached by index of the outer `Vec`, the two-level container write at the heart of the problem.
- **`Option[shared]` niche match on the recursion** — each step matches the `Option[TreeNode]` child handle (`None` bottoms out, `Some(n)` descends), passing the shared node **by value** (a cheap RC-handle pass).
- **`Vec[TreeNode]` frontier with `current = next` reassignment** — the BFS solver holds the current level as a `Vec` of shared node handles and advances the frontier by overwriting the whole variable (`current = next`). Reassigning a `Vec[shared]` local must release the shared elements the old frontier held before dropping it — the exact surface of compiler bug B-2026-07-12-30 (see below).

### A codegen bug this kata surfaced (now fixed)

The BFS solver's frontier advance — `current = next`, overwriting a `Vec[TreeNode]` local with the next level — originally **leaked** on `karac build`: reassigning a `Vec` whose elements are shared (RC) nodes freed the old buffer but skipped the per-element rc-dec, so the whole overwritten frontier leaked (`definitely lost`, x86-visible; interp was clean). Per the repo's "never route around — fix or file it" rule, that gap was filed as [`B-2026-07-12-30`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) with a minimal repro and a clean counterpart. It is **fixed** as of kara [`924cd05`](https://github.com/karalang/kara/commit/924cd05): the `Assign` identifier-target path now runs the old value's element-releasing walk before the store when the element carries a non-trivial per-element drop (rc-dec for a shared struct/enum, tag-guarded `karac_drop_Option_<payload>` for `Option[shared]`), matching the scope-exit drop exactly and never double-releasing. So [`level_order_bfs.kara`](level_order_bfs.kara) — the most natural statement of the problem — now compiles and runs leak-clean, byte-identical to the two DFS solvers across every surface. The kata initially shipped the two queue-free DFS forms while the bug was open; the BFS form joins them now that the fix has landed.

**v1 note.** Trees stay within the `≤ 2000`-node constraint. The sink folds each tree's level structure — level count, each level's size, and every value in order — into a running polynomial hash. All three solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the BFS-equality + fuzz ground truth, and are valgrind-clean.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   level_order.kara
karac build level_order.kara && ./level_order

# The BFS-frontier and level-by-level variants (identical output):
karac run level_order_bfs.kara
karac run level_order_bylevel.kara

# Python
python3 level_order.py

# Verify they all agree
diff <(karac run level_order.kara) <(python3 level_order.py)              && echo OK
diff <(karac run level_order.kara) <(karac run level_order_bfs.kara)     && echo OK
diff <(karac run level_order.kara) <(karac run level_order_bylevel.kara)  && echo OK

# Ground truth: DFS-with-depth level order == independent BFS level order (battery + 20k fuzz)
python3 ground_truth.py
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`level_order.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** The canonical numbers below are the corpus's **Apple M5 Pro** run — [`bench/results.json`](bench/results.json) (fixed [kara `B-2026-07-15-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) karac). A shared **x86-64 Linux cloud-container** reference run is kept alongside in [`bench/results.container-x86.json`](bench/results.container-x86.json); absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. The re-bench confirmed the flag below: on this **allocation-bound** workload the M5's wider core compressed kāra's narrow container lead over Rust into a **dead tie** (0.97× → 1.00×), and Go — 2× behind on the container — closed to 1.15×; C stays the floor.

**Workload.** Build 8 distinct 15-node BSTs once (rotating the insert order changes each shape), then **K = 1,500,000** reps of DFS-with-depth `level_order` on a **data-dependent-selected** tree (`idx = acc%8`, seeded by the running hash, so nothing hoists), folding the whole result — level count, each level's size, and every value — into a rolling polynomial hash. Unlike the read-only-traversal siblings, **each rep allocates a fresh nested result** (Kāra `Vec[Vec[i64]]`, C an array of `realloc`-grown rows freed per rep, Rust `Vec<Vec<i64>>`, Go `[][]int64`), so the workload is **allocation-bound** — the per-rep cost is dominated by building and tearing down the nested container, not the tree walk. Each mirror uses its natural node: Kāra `shared` (RC), C/Go raw pointer, **Rust `Box` + `&`-borrow** (the tree is never mutated or shared during traversal). All five compiled mirrors must agree on `959820311` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../../1-100/69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **Apple M5 Pro numbers** (canonical; sink `959820311` agreed by all five mirrors), on the fixed [kara `B-2026-07-15-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) karac:

| Implementation | Wall time | Node / result representation |
|---|---|---|
| c    level_order (clang -O3)                        | 332.4 ± 7.5 ms | `malloc` pointer + `realloc` rows |
| rust level_order (rustc -O)                         | 423.8 ± 5.2 ms | `Box` + `Vec<Vec>` |
| **kāra level_order**                                | **424.9 ± 6.0 ms** | **`shared` (RC) + `Vec[Vec]`** |
| rust level_order (rustc -O, overflow-checks=on)      | 428.2 ± 5.0 ms | `Box` + `Vec<Vec>` |
| go   level_order (GC)                               | 491.1 ± 3.0 ms | `*Node` + `[][]int64` (GC) |

**On an allocation-bound nested-container workload, Kāra sits at parity with Rust — behind the C floor, ahead of Go.** Every rep builds and tears down a fresh `Vec[Vec[i64]]`, so the per-rep cost is dominated by the nested-container churn, not the read-only walk. Against its semantic peer Rust — `Box` node walked by `&`-borrow, `Vec<Vec<i64>>` result — Kāra is **level**: 424.9 vs 423.8 ms stock (1.00×), and it just **edges the equal-safety Rust** row (428.2 ms, 0.99×). The two are the same shape (bump-allocate an outer vector of inner vectors, grow each inner on push, free the lot), and Kāra's allocator path keeps pace even carrying the per-node RC inc/decs the borrow-based Rust walk skips — because the *allocation* is the cost and the RC traversal tax is small beside it (the inverse of read-only sibling [#100](../../1-100/100-same-tree/), where the walk *was* the whole cost and the RC tax showed). **Go is 1.15× behind Kāra** (491 ms): its GC pays on the 1.5 M × (outer slice + N inner slices) allocation churn — and carries a **9.2 MiB** RSS to Kāra's 1.06 MiB — though on the M5's wider core it closed most of the 2× gap it showed on the container. **C is the metal floor** at 332 ms (**1.28× ahead of Kāra**): raw `malloc`/`realloc`/`free`, no refcount, no GC. So the M5 ordering is raw malloc (C) < **Kāra ≈ Rust** < Go GC — the container's kāra-*ahead*-of-Rust margin compressed to a tie exactly as the flag warned, but the regime verdict holds: on alloc-heavy nested containers Kāra is Rust-class and beats Go, the inverse of the read-only-traversal katas. Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`) over the run. Python is listed at **146 ms but ran K = 75,000 — 1/20 of the compiled iterations** (pure-Python recursion is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **1.06 MiB** peak RSS (parity with Rust's 1.09 MiB and C's 1.09 MiB) vs Go's **9.2 MiB**. The M5 kāra binary is a clean **33.6 KiB** (C parity, 33.0 KiB) — confirming the container's flagged **336 KiB** was the backtrace-symbolizer linkage artifact `--gc-sections` strips, correctly lean here — vs Go's 2.4 MiB.

**M5 re-bench (done).** The flag was right: kāra's narrow container lead over Rust (1.03×) compressed to a **dead tie** on the M5's wider core — 1.00× stock, 0.99× equal-safety — and Go closed from 2.03× to 1.15× behind. The robust signs held (C the floor, Go the slowest, Go's GC RSS ~9×), and the regime verdict stands: on alloc-bound nested containers Kāra is Rust-class and ahead of Go, the inverse of the pure read-only walks where the per-node RC tax showed.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.json`](bench/results.json) (M5, canonical) and [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched **nested-container allocation** (`Vec[Vec[i64]]` vs `Vec<Vec<i64>>`, both over a by-reference tree walk), the honest comparison for a build-a-fresh-grouping-per-rep workload. C's raw `malloc`/`realloc` is the metal floor, Go the GC data point (slowest here, on nested-slice churn), Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
