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

- **`shared struct TreeNode` (RC), read-only traversal** — both solvers walk the shared-node tree without mutating it; the recursive form passes `Option[TreeNode]` **by value** — a cheap RC-handle pass whose retain/release is *elided* on this non-escaping walk (see the benchmark note). Node type mirrors kata [#102](../102-binary-tree-level-order-traversal/) / [#100](../../1-100/100-same-tree/).
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

> **Machine.** The canonical numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json). The corpus's canonical **Apple M5 Pro** numbers ([`bench/results.json`](bench/results.json)) are folded in separately; absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. Re-run `bench.sh` on the M5 to refresh the canonical table.

**Workload.** Build 8 distinct 15-node BSTs once, then **K = 4,000,000** reps of recursive `max_depth` on a **data-dependent-selected** tree (`idx = acc%8`, seeded by the running hash, so nothing hoists), folding each depth into a rolling polynomial hash. Unlike the alloc-heavy tree siblings, this is a **read-only per-node traversal** — each rep only matches `Option[shared]` and reads a field per node, no allocation — so any per-node overhead *is* the whole cost. Each mirror uses its natural node: Kāra `shared` (RC, passed by value), C/Go raw pointer, **Rust `Box` + `&`-borrow**. All five compiled mirrors must agree on `123882095` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../../1-100/69-sqrtx/)'s discipline) — and it matters here: `min_depth`/`max_depth`/`check` each do a per-node add, so the overflow-check row is the honest equal-safety baseline (not a rounding effect).

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **x86-64 container numbers** (canonical M5 pending; see the machine note):

| Implementation | Wall time | Node representation |
|---|---|---|
| rust max_depth (rustc -O)                           | 269.6 ± 4.8 ms | `Box` + `&`-borrow |
| c    max_depth (clang -O3)                          | 295.2 ± 15.4 ms | `*Node` |
| go   max_depth (GC `*Node`)                         | 297.1 ± 4.8 ms | `*Node` |
| rust max_depth (rustc -O, overflow-checks=on)        | 301.9 ± 14.7 ms | `Box` + `&`-borrow |
| **kāra max_depth**                                  | **477.0 ± 11.7 ms** | **`shared` (RC)** |

**This is the corpus's most-exposed traversal, and Kāra trails on it — the read-only-walk twin of [#100](../../1-100/100-same-tree/).** Each rep is *only* `match` + one field-access per node: no allocation, no compute, no strings, so any per-node overhead *is* the entire cost, with nothing to hide it behind. Kāra runs **1.77× behind Rust**, **1.62× behind C**, and **1.61× behind Go** — and the three fast languages cluster tightly (270–302 ms), all bounded by the same raw pointer/borrow chase, while Kāra sits apart. A later probe decomposes this gap ([kara `B-2026-07-15-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl)), and **refcounting is not a contributor**: the compiler's borrow-elision already drops the retain/release on a non-escaping walk, so a by-value traversal times *identically* to a `ref`-borrow one (this supersedes the earlier "~11% RC" estimate — RC is free here). What remains is two things. First, **overflow-checking safety** — Kāra checks i64 overflow by default while stock `rustc -O` wraps, so the honest like-for-like is the `overflow-checks=on` row (302 ms), which absorbs part of the raw gap. Second, and the one genuine codegen item, **per-node `Option[shared]` lowering** — decoding the niche, matching it, and GEP-ing the shared field across the two child recursions is heavier than C/Rust's raw null-check-and-deref; against the equal-safety Rust baseline Kāra is ~1.6×, flagged as real headroom (leaner `Option[shared]` match/field lowering). The compute- and alloc-bound siblings bracket this from the other side — [#105](../105-construct-binary-tree-from-preorder-and-inorder-traversal/) and [#103](../103-binary-tree-zigzag-level-order-traversal/) land Kāra within a few percent of Rust because allocation or arithmetic dominates and the per-node tax is amortized; here there is nothing *but* the per-node tax. Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`) over the run. Python is listed at **444 ms but ran K = 200,000 — 1/20 of the compiled iterations** (pure-Python recursion is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **2.5 MiB** peak RSS (above C's 1.5 MiB, Rust's 2.3 MiB, and Go's 1.9 MiB — all within a tight band). The kāra binary measures **336 KiB** here — a build-linkage artifact of this container run (heap-growing programs retain the backtrace-symbolizer tree `--gc-sections` should strip; a correct build is ~15 KiB), independent of the runtime numbers, flagged for the M5 — vs C's 16 KiB and Go's 2.2 MiB.

**Flagged for the M5 re-bench** — the corpus has seen container tree-traversal orderings compress sharply on the M5's wider core (see [#97](../../1-100/97-interleaving-string/)), so treat the *margin* as a data point, not a verdict; the direction (Kāra trailing on a pure per-node walk) should carry, but the size may not.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference) and, once folded in, [`bench/results.json`](bench/results.json) (M5, canonical).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched read-only tree traversal (`shared` handle walk vs `Box` + `&`-borrow), the most-exposed RC/traversal regime (the read-only-walk analogue of [#100](../../1-100/100-same-tree/)). C's raw pointer chase is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
