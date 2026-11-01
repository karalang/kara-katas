# 104. Maximum Depth of Binary Tree

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Tree · Depth-First Search · Breadth-First Search · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/maximum-depth-of-binary-tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/)

Return the **maximum depth** of a binary tree — the number of nodes along the longest path from the root down to the farthest leaf.

```
      3            max depth = 3
     / \           (root → 20 → 15, or root → 20 → 7)
    9  20
       / \
      15  7
```

**Constraints:** `0 ≤ #nodes ≤ 10^4`, node values fit `-100 … 100`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Recursive DFS** ★ | [`max_depth.kara`](max_depth.kara) ✓ | [`max_depth.py`](max_depth.py) ✓ |
| **Iterative BFS level count** | [`max_depth_bfs.kara`](max_depth_bfs.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for both approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the two Kāra approaches agree with **each other** and with the Python mirror. An independent **ground-truth check** confirms the answer three ways: the recursive DFS depth equals a BFS level count *and* the longest explicit root-to-leaf path, on a case battery **and 20,000 randomised fuzz trees**, zero mismatches. Both solvers compile with zero diagnostics and are valgrind-clean.

## Two ways to measure depth

**Recursive DFS** ([`max_depth.kara`](max_depth.kara), the ★): the textbook recurrence — an empty tree has depth 0, and a non-empty node's depth is 1 plus the deeper of its two subtrees. One visit per node, O(n).

```
max_depth(node):
    node is None -> 0
    else         -> 1 + max(max_depth(node.left), max_depth(node.right))
```

**Iterative BFS level count** ([`max_depth_bfs.kara`](max_depth_bfs.kara)): the depth is just the number of *levels* in a breadth-first walk. Hold the current level as a `Vec[TreeNode]` frontier; each time it is non-empty, bump the depth and advance to the next level (all children of the frontier), until the frontier empties. A distinct mechanism (an explicit level-by-level queue vs the depth recurrence) landing on the identical number, and it exercises the `Vec[shared]` frontier + `current = next` advance the tree katas [#102](../102-binary-tree-level-order-traversal/)/[#103](../103-binary-tree-zigzag-level-order-traversal/) share.

## Kāra features exercised

- **`shared struct TreeNode` (RC), read-only traversal** — both solvers walk the shared-node tree without mutating it; the recursive form passes `Option[TreeNode]` **by value**. On a provably read-only, non-escaping walk the compiler now elides the per-node retain/release entirely (kara `B-2026-07-15-21`, default-ON) — a win this kata helped surface (see the benchmark note). Node type mirrors kata [#102](../102-binary-tree-level-order-traversal/) / [#100](../../1-100/100-same-tree/).
- **`match` on `Option[shared]` returning a value** — the recurrence is a `match` whose arms yield `i64`, the shared-node analogue of a simple fold.
- **`Vec[TreeNode]` frontier with `current = next`** — the BFS solver advances the shared-node frontier by whole-variable reassignment; the frontier drains to empty, so its scope-exit drop is clean (the surface hardened by kara `924cd05`).

**v1 note.** Trees stay within the `≤ 10^4`-node constraint. The sink folds each tree's max depth into a running polynomial hash. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the BFS + longest-path fuzz ground truth, and are valgrind-clean.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   max_depth.kara
karac build max_depth.kara && ./max_depth

# The BFS-level-count variant (identical output):
karac run max_depth_bfs.kara

# Python
python3 max_depth.py

# Verify they all agree
diff <(karac run max_depth.kara) <(python3 max_depth.py)         && echo OK
diff <(karac run max_depth.kara) <(karac run max_depth_bfs.kara) && echo OK

# Ground truth: DFS depth == BFS level count == longest root-to-leaf path (battery + 20k fuzz)
python3 ground_truth.py
```

## Benchmarks
Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`max_depth.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5 re-bench (2026-11-01).** The canonical numbers below are the corpus's **Apple M5 Pro** run (6P+12E, Darwin 25.6.0; **karac g6697158fa** (0.9.0-dev.14057, the v2/MIR backend; the legacy backend was deleted 2026-10-23), `rustc 1.95.0`, Apple clang 21.0.0, `go 1.26.3`, hyperfine 1.20) — [`bench/results.json`](bench/results.json). Against the 2026-07-18 legacy-backend snapshot kāra is flat against every comparator (each move under this session's ~10 % noise band): kāra/Rust 1.02× → 1.08×, kāra/equal-safety Rust 0.99× → 1.04×, kāra/C 1.13× → 1.17×, kāra/Go 1.01× → 1.08×. A shared **x86-64 Linux cloud-container** reference run is kept alongside in [`bench/results.container-x86.json`](bench/results.container-x86.json); absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. History: the M5's wider core tightened the margins — kāra went from 1.13× the equal-safety Rust row on the container to 0.99× (just ahead) on the 2026-07-18 legacy-backend M5 run, and from 1.19× to 1.13× C.

**Workload.** Build 8 distinct 15-node BSTs once, then **K = 4,000,000** reps of recursive `max_depth` on a **data-dependent-selected** tree (`idx = acc%8`, seeded by the running hash, so nothing hoists), folding each depth into a rolling polynomial hash. Unlike the alloc-heavy tree siblings, this is a **read-only per-node traversal** — each rep only matches `Option[shared]` and reads a field per node, no allocation — so any per-node overhead *is* the whole cost. Each mirror uses its natural node: Kāra `shared` (RC, passed by value), C/Go raw pointer, **Rust `Box` + `&`-borrow**. All five compiled mirrors must agree on `123882095` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../../1-100/69-sqrtx/)'s discipline) — and it matters here: `min_depth`/`max_depth`/`check` each do a per-node add, so the overflow-check row is the honest equal-safety baseline (not a rounding effect).

`--warmup 5 --runs 30 --shell=none`. All single-threaded, ~99.5 % CPU (the default build emits no call of `karac_mir_task_spawn`, verified in the emitted IR (`KARAC_MIR_LL`), same as its `KARAC_AUTO_PAR=0` twin). **Apple M5 Pro numbers, karac g6697158fa, 2026-11-01** (canonical; sink `123882095` agreed by all five mirrors):

| Implementation | Wall time | Node representation |
|---|---|---|
| c    max_depth (clang -O3)                          | 146.1 ± 2.6 ms | `*Node` |
| rust max_depth (rustc -O)                           | 157.7 ± 2.7 ms | `Box` + `&`-borrow |
| go   max_depth (GC `*Node`)                         | 158.1 ± 2.0 ms | `*Node` |
| rust max_depth (rustc -O, overflow-checks=on)        | 164.1 ± 4.8 ms | `Box` + `&`-borrow |
| **kāra max_depth**                                  | **171.0 ± 3.0 ms** | **`shared` (RC)** |

**The corpus's most-exposed traversal — which surfaced a real compiler gap that is now fixed.** Each rep is *only* `match` + a field-access + a per-node add: no allocation, so any per-node overhead *is* the entire cost, which made this (with [#100](../../1-100/100-same-tree/) / [#111](../111-minimum-depth-of-binary-tree/) / [#112](../112-path-sum/)) the worst case that exposed [kara `B-2026-07-15-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl). Disassembly showed the by-value `Option[shared]` walk was emitting **two retains + two releases per visited node** — refcount traffic that was *not* being elided (an earlier draft of this README wrongly claimed "RC is free / already elided"; the object code proved otherwise). The fix makes RC-elision **default-ON** (plus the `Some(n)`-binding pair), so the walk carries **zero rc ops per node**. Against the fixed compiler:

- **Refcount traffic — eliminated.** On the M5 canonical run (2026-11-01, v2/MIR) Kāra lands at **171.0 ms — 1.04× the equal-safety Rust row (164.1 ms)**, 1.08× stock Rust and 1.08× Go (158.1 ms), so it is now the slowest of the five by a few percent (on the 2026-07-18 legacy run it was just ahead of equal-safety Rust, 0.99×; the move is inside this session's noise band); the container measured the fix's effect at 477 → 319 ms, from ~1.8× behind Rust to inside the fast-language band. Before the fix the by-value walk's two-retains-two-releases-per-node left it well behind.
- **Overflow-checking safety — most of the residual vs *stock* Rust / C.** `max_depth` does a per-node add, so the honest like-for-like is `overflow-checks=on` (164.1 ms), which itself sits 1.12× behind C; Kāra's **1.17× gap to C** (146.1 ms) is that per-node check, which `-O3` wraps, plus a ~4 % residual over the equal-safety Rust row. Note `max_depth` **combines both** child depths (`1 + max(l, r)`), so neither recursion is in tail position and LLVM cannot loop-ify it — the RC removal alone closes the gap, without the extra tail-call win the `and`/`or` short-circuit siblings ([#100](../../1-100/100-same-tree/) / [#112](../112-path-sum/)) get.

The compute- and alloc-bound siblings bracket this from the other side — [#105](../105-construct-binary-tree-from-preorder-and-inorder-traversal/) and [#103](../103-binary-tree-zigzag-level-order-traversal/) are dominated by allocation or arithmetic rather than the per-node walk (on the 2026-11-01 M5 run #103 puts Kāra 0.81× Rust, ahead, and #105 1.11× Rust). Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`) over the run. Python is listed at **142 ms (last measured 2026-07-18, not re-run 2026-11-01) but ran K = 200,000 — 1/20 of the compiled iterations** (pure-Python recursion is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **1.05 MiB** peak RSS (C 1.02, Rust 1.08; Go 2.6 MiB). Binary size: c 32.9 KiB, **kāra 295.8 KiB**, rust 456.5 KiB, go 2.38 MiB; every MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (the legacy M5 kāra binary here was 33.6 KiB), tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). Compile-cold on the M5 is clang 48.9 ms < rustc 97.1 ms < **karac 121.5 ms** (2.5× clang, 1.25× rustc).

**M5 re-bench (2026-07-18, legacy backend; history).** As the container note predicted, the margins compressed on the M5's wider core — the vs-equal-safety-Rust ratio went from 1.13× to **0.99× (Kāra just ahead)** and the vs-C from 1.19× to 1.13× — while the direction held: on a pure per-node walk Kāra sits level with the safety-matched competitors, trailing only C's unchecked pointer-chase by the overflow check. (2026-11-01 note: on the v2/MIR backend kāra trails every mirror by a few percent — 1.04× equal-safety Rust, 1.08× Go and stock Rust, 1.17× C — see the table above.)

Compile-cold, binary size, and peak-RSS records are in [`bench/results.json`](bench/results.json) (M5, canonical) and [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched read-only tree traversal (`shared` handle walk vs `Box` + `&`-borrow), the most-exposed RC/traversal regime (the read-only-walk analogue of [#100](../../1-100/100-same-tree/)). C's raw pointer chase is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
