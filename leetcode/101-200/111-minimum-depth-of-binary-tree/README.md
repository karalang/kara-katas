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

- **`shared struct TreeNode` (RC), read-only traversal** — both solvers walk the shared-node tree without mutating it; the DFS passes `Option[TreeNode]` **by value**. On a provably read-only, non-escaping walk the compiler now elides the per-node retain/release entirely (kara `B-2026-07-15-21`, default-ON) — a win this kata helped surface (see the benchmark note). Node type mirrors kata [#104](../104-maximum-depth-of-binary-tree/) / [#110](../110-balanced-binary-tree/).
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

> **Machine.** The canonical numbers below are the corpus's **Apple M5 Pro** run — [`bench/results.json`](bench/results.json) (fixed [kara `B-2026-07-15-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) karac). A shared **x86-64 Linux cloud-container** reference run is kept alongside in [`bench/results.container-x86.json`](bench/results.container-x86.json); absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. The margin compressed on the M5 as the container note predicted, but the *direction* held: kāra sits at parity with the equal-safety Rust row on both hosts (M5 1.00×, container 1.03×).

**Workload.** Build 8 balanced 31-node trees once, then **K = 3,000,000** reps of the recursive `min_depth` on a **data-dependent-selected** tree (`idx = acc%8`, seeded by the running hash, so nothing hoists), folding each minimum depth into a rolling polynomial hash. `min_depth` computes *both* subtree depths at every node, so on a balanced tree it runs the **full** post-order — a **read-only per-node traversal** (match `Option[shared]` + one field read per node, no allocation), so any per-node overhead *is* the whole cost. Each mirror uses its natural node: Kāra `shared` (RC, passed by value), C/Go raw pointer, **Rust `Box` + `&`-borrow**. All five compiled mirrors must agree on `768360140` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../../1-100/69-sqrtx/)'s discipline) — and it matters here: `min_depth`/`max_depth`/`check` each do a per-node add, so the overflow-check row is the honest equal-safety baseline (not a rounding effect).

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **Apple M5 Pro numbers** (canonical; sink `768360140` agreed by all five mirrors), on the fixed [kara `B-2026-07-15-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) karac:

| Implementation | Wall time | Node representation |
|---|---|---|
| c    min_depth (clang -O3)                          | 133.1 ± 5.8 ms | `*Node` |
| go   min_depth (GC `*Node`)                         | 134.6 ± 5.4 ms | `*Node` |
| rust min_depth (rustc -O)                           | 143.8 ± 3.6 ms | `Box` + `&`-borrow |
| **kāra min_depth**                                  | **157.1 ± 5.2 ms** | **`shared` (RC)** |
| rust min_depth (rustc -O, overflow-checks=on)        | 157.4 ± 5.7 ms | `Box` + `&`-borrow |

**This kata helped expose a real compiler gap that is now fixed — Kāra runs at parity with equal-safety Rust here.** Each rep is *only* `match` + a field-access + a per-node add down a full 31-node post-order: no allocation, so any per-node overhead *is* the entire cost, which made this (with [#100](../../1-100/100-same-tree/) / [#104](../104-maximum-depth-of-binary-tree/) / [#112](../112-path-sum/)) the exposed worst case that surfaced [kara `B-2026-07-15-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl). Disassembly showed the by-value `Option[shared]` walk was emitting **two retains + two releases per visited node** — refcount traffic that was *not* being elided (an earlier draft of this README wrongly claimed "RC is free / already elided"; the object code proved otherwise). The fix makes the RC-elision convention **default-ON** and additionally elides the `Some(n)`-binding pair, so the walk now carries **zero rc ops per node**. The decomposition against the fixed compiler:

- **Refcount traffic — eliminated.** What was ~½ the old gap is gone: on the M5 canonical run Kāra lands at **157.1 ms**, **1.00× the equal-safety Rust row (157.4 ms) — parity** (the container reference showed the same verdict at 1.03×), where before the fix the by-value walk's two-retains-two-releases-per-node left it well behind.
- **Overflow-checking safety — the honest remaining split vs *stock* Rust.** `min_depth` does a per-node add, so Kāra's default i64-overflow check is a real cost stock `rustc -O` (143.8 ms) skips; the like-for-like is the `overflow-checks=on` row (157.4 ms), where Kāra sits level. That check is also the whole of the **1.18× gap to C** (133.1 ms), which `-O3` wraps. Unlike the `and`/`or` short-circuit shapes ([#100](../../1-100/100-same-tree/) / [#112](../112-path-sum/)), `min_depth` **combines both** child results (`1 + min(l, r)`), so neither recursion is in tail position and LLVM cannot loop-ify it — the RC removal alone closes the gap, without the extra tail-call win those siblings get.

Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`) over the run. Python is listed at **206 ms but ran K = 150,000 — 1/20 of the compiled iterations** (pure-Python recursion is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **1.0 MiB** peak RSS (matching C, at Rust's level; Go 2.6 MiB). The M5 kāra binary is a clean **33.5 KiB** (C parity, 32.9 KiB) — confirming the container's flagged **324 KiB** was the backtrace-symbolizer linkage artifact `--gc-sections` strips, correctly lean here — vs Go's 2.4 MiB.

**M5 re-bench (done).** As the container note predicted, the margin compressed on the M5's wider core — **1.26× → 1.18× C** — while the direction held: Kāra trails C on a pure per-node walk (the overflow check C skips) yet sits at parity with the equal-safety Rust row, a pattern robust across [#104](../104-maximum-depth-of-binary-tree/) / [#110](../110-balanced-binary-tree/) / [#100](../../1-100/100-same-tree/).

Compile-cold, binary size, and peak-RSS records are in [`bench/results.json`](bench/results.json) (M5, canonical) and [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched read-only tree traversal (`shared` handle walk vs `Box` + `&`-borrow), the exposed RC/traversal regime shared with [#104](../104-maximum-depth-of-binary-tree/) / [#110](../110-balanced-binary-tree/). C's raw pointer chase is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
