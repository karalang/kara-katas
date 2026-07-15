# 111. Minimum Depth of Binary Tree

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Tree · Depth-First Search · Breadth-First Search · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/minimum-depth-of-binary-tree](https://leetcode.com/problems/minimum-depth-of-binary-tree/)

Return the **minimum depth** — the number of nodes on the shortest path from the root down to the nearest **leaf** (a node with no children). The mirror of [#104](../104-maximum-depth-of-binary-tree/), with one crucial twist.

```
    1          min depth = 2         1          min depth = 3, NOT 1
   / \         (root → 2, a leaf)     \          (the root's empty left side has
  2   3                                2          no leaf; you must descend the
                                        \         chain to the leaf at depth 3)
                                         3
```

**Constraints:** `0 ≤ #nodes ≤ 10^5`, node values fit `-1000 … 1000`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Recursive DFS** ★ | [`min_depth.kara`](min_depth.kara) ✓ | [`min_depth.py`](min_depth.py) ✓ |
| **BFS, stop at the first leaf** | [`min_depth_bfs.kara`](min_depth_bfs.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for both approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the two Kāra approaches agree with **each other** and with the Python mirror. An independent **ground-truth check** confirms the answer three ways: the recursive DFS equals a BFS first-leaf depth *and* a brute-force shortest root-to-leaf path length, on a case battery **and 20,000 randomised trees**, zero disagreements. Both solvers compile with zero diagnostics and are valgrind-clean.

## The one-child subtlety

Unlike maximum depth ([#104](../104-maximum-depth-of-binary-tree/)), you cannot naively take `1 + min(depth(left), depth(right))`: a node with only one child would report depth 1 (the empty side), but there is no leaf on the empty side, so the real shortest path must descend the *non-empty* side. Both solvers handle it.

**Recursive DFS** ([`min_depth.kara`](min_depth.kara), the ★): compute both subtree depths; an empty subtree's depth of 0 means "no leaf this way", so if one side is 0 take the other, otherwise take the smaller.

```
min_depth(node):
    node is None -> 0
    ld = min_depth(left);  rd = min_depth(right)
    ld == 0 -> 1 + rd          # only the right side has a leaf (or node is a leaf: 1+0)
    rd == 0 -> 1 + ld          # only the left side has a leaf
    else    -> 1 + min(ld, rd)
```

**BFS, stop at the first leaf** ([`min_depth_bfs.kara`](min_depth_bfs.kara)): breadth-first search reaches nodes in nondecreasing depth order, so the **first leaf it dequeues is at the minimum depth** — read the answer off and return immediately, never exploring deeper. A `Vec[TreeNode]` frontier, one depth bump per level, short-circuiting on the first childless node. A distinct mechanism (early-terminating level queue vs full post-order) landing on the identical number — and it exercises returning **early** while the frontiers still hold residual nodes (the residual-worklist drop surface of kata [#100](../../1-100/100-same-tree/), now clean).

## Kāra features exercised

- **`shared struct TreeNode` (RC), read-only traversal** — both solvers walk the shared-node tree without mutating it; the DFS passes `Option[TreeNode]` **by value** (a cheap RC-handle pass that rc-inc/decs each visited node). Node type mirrors kata [#104](../104-maximum-depth-of-binary-tree/) / [#110](../110-balanced-binary-tree/).
- **Nested `Option[shared]` match on both children** — the one-child subtlety is exactly a four-way case on `(left, right)` being present or empty.
- **Early `return` out of nested loops with a live `Vec[shared]` frontier** — the BFS returns the moment it finds a leaf, dropping the still-populated `current`/`next` frontiers; the residual `Vec[shared]` drop releases their elements cleanly (valgrind-clean).
- **Two construction shapes** — balanced trees (middle-pick) and skewed chains (ascending insert); the chains give `min_depth = chain length`, exercising the subtlety, so the verdict genuinely varies.

**v1 note.** Trees stay within the `≤ 10^5`-node constraint. The sink folds each tree's minimum depth into a running polynomial hash. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the BFS + brute-force fuzz ground truth, and are valgrind-clean.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   min_depth.kara
karac build min_depth.kara && ./min_depth

# The BFS-first-leaf variant (identical output):
karac run min_depth_bfs.kara

# Python
python3 min_depth.py

# Verify they all agree
diff <(karac run min_depth.kara) <(python3 min_depth.py)         && echo OK
diff <(karac run min_depth.kara) <(karac run min_depth_bfs.kara) && echo OK

# Ground truth: DFS == BFS-first-leaf == brute-force shortest path (battery + 20k fuzz)
python3 ground_truth.py
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`min_depth.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** The canonical numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json). The corpus's canonical **Apple M5 Pro** numbers ([`bench/results.json`](bench/results.json)) are folded in separately; absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. Re-run `bench.sh` on the M5 to refresh the canonical table.

**Workload.** Build 8 balanced 31-node trees once, then **K = 3,000,000** reps of the recursive `min_depth` on a **data-dependent-selected** tree (`idx = acc%8`, seeded by the running hash, so nothing hoists), folding each minimum depth into a rolling polynomial hash. `min_depth` computes *both* subtree depths at every node, so on a balanced tree it runs the **full** post-order — a **read-only per-node traversal** (match `Option[shared]` + one field read per node, no allocation), so any per-node overhead *is* the whole cost. Each mirror uses its natural node: Kāra `shared` (RC, passed by value), C/Go raw pointer, **Rust `Box` + `&`-borrow**. All five compiled mirrors must agree on `768360140` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../../1-100/69-sqrtx/)'s discipline) — though on a pure-traversal loop the fold's `acc*131` is the only arithmetic, so the overflow-check row barely moves.

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **x86-64 container numbers** (canonical M5 pending; see the machine note):

| Implementation | Wall time | Node representation |
|---|---|---|
| rust min_depth (rustc -O)                           | 274.9 ± 4.1 ms | `Box` + `&`-borrow |
| c    min_depth (clang -O3)                          | 317.9 ± 6.6 ms | `*Node` |
| go   min_depth (GC `*Node`)                         | 340.2 ± 6.4 ms | `*Node` |
| rust min_depth (rustc -O, overflow-checks=on)        | 343.8 ± 6.3 ms | `Box` + `&`-borrow |
| **kāra min_depth**                                  | **504.2 ± 7.1 ms** | **`shared` (RC)** |

**A pure read-only traversal again, and Kāra trails on it — the same exposed RC regime as [#104](../104-maximum-depth-of-binary-tree/) / [#110](../110-balanced-binary-tree/).** Each rep is *only* `match` + one field-access per node down a full 31-node post-order: no allocation, no compute beyond a couple of comparisons, so any per-node overhead *is* the entire cost. Kāra runs **1.83× behind Rust**, **1.59× behind C**, and **1.48× behind Go** — the three fast languages cluster (275–340 ms) on the same raw pointer/borrow chase while Kāra sits apart. The gap has two contributors, both real codegen headroom, both isolated in [#100](../../1-100/100-same-tree/)'s profiled analysis of this identical read-only shape: passing `Option[TreeNode]` **by value** rc-inc/decs every visited node (a per-node reference count the borrow/pointer walks skip — #100 measured this at ~11 % of its gap via a `ref` borrow variant), and Kāra's per-node **`Option[shared]` traversal lowering** — decoding the niche, matching it, GEP-ing the shared field is heavier than C/Rust's raw null-check-and-deref (the dominant remainder). Both are flagged as headroom, not waved off: RC-retain *elision* on a non-escaping borrow, and leaner `Option[shared]` match/field lowering. The alloc-bound siblings ([#107](../107-binary-tree-level-order-traversal-ii/) / [#108](../108-convert-sorted-array-to-binary-search-tree/) / [#109](../109-convert-sorted-list-to-binary-search-tree/)) bracket this from the other side, landing Kāra at-or-ahead of Rust because allocation dominates; here, as in [#104](../104-maximum-depth-of-binary-tree/) / [#110](../110-balanced-binary-tree/), there is nothing *but* the per-node tax. Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`) over the run. Python is listed at **403 ms but ran K = 150,000 — 1/20 of the compiled iterations** (pure-Python recursion is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **2.5 MiB** peak RSS (above C's 1.5 MiB, Rust's 2.3 MiB, Go's 1.9 MiB — all within a tight band). The kāra binary measures **324 KiB** here — a build-linkage artifact of this container run (heap-growing programs retain the backtrace-symbolizer tree `--gc-sections` should strip; a correct build is ~15 KiB), independent of the runtime numbers, flagged for the M5 — vs C's 16 KiB and Go's 2.2 MiB.

**Flagged for the M5 re-bench** — the corpus has seen container tree-traversal orderings compress sharply on the M5's wider core (see [#97](../../1-100/97-interleaving-string/)), so treat the *margin* as a data point; the direction (Kāra trailing on a pure per-node walk) is robust across [#104](../104-maximum-depth-of-binary-tree/) / [#110](../110-balanced-binary-tree/) / [#100](../../1-100/100-same-tree/), but the size may compress.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference) and, once folded in, [`bench/results.json`](bench/results.json) (M5, canonical).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched read-only tree traversal (`shared` handle walk vs `Box` + `&`-borrow), the exposed RC/traversal regime shared with [#104](../104-maximum-depth-of-binary-tree/) / [#110](../110-balanced-binary-tree/). C's raw pointer chase is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
