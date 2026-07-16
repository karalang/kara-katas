# 113. Path Sum II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Backtracking · Tree · Depth-First Search · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/path-sum-ii](https://leetcode.com/problems/path-sum-ii/)

Given a binary tree and an integer `target`, return **every** root-to-leaf path whose node values sum to `target` — each path as the list of values from the root down to the leaf. The collect-all sibling of [#112](../112-path-sum/) (which only asks *whether* such a path exists).

```
        5              target = 22  ->  [[5,4,11,2], [5,8,4,5]]
       / \
      4   8            two distinct root-to-leaf paths sum to 22;
     /   / \           #112 would return just `true`, #113 returns both
    11  13  4
   /  \      \
  7    2      5   1
```

**Constraints:** `0 ≤ #nodes ≤ 5000`, node values fit `-1000 … 1000`, `target` fits `-10^9 … 10^9`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Backtracking DFS, `mut ref` accumulator** ★ | [`path_sum_ii.kara`](path_sum_ii.kara) ✓ | [`path_sum_ii.py`](path_sum_ii.py) ✓ |
| **Return-based, prepend on the way up** | [`path_sum_ii_return.kara`](path_sum_ii_return.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for both approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the two Kāra approaches agree with **each other** and with the Python mirror. An independent **ground-truth check** confirms the answer three ways: the backtracking DFS equals the return-based collect *and* a brute-force enumerate-every-root-to-leaf-path-then-filter, **path for path, in the same order**, on a case battery **and 20,000 randomised (tree, target) pairs**, zero disagreements. Both solvers compile with zero diagnostics and are valgrind-clean.

## Two mechanisms for collecting the paths

The leaf rule is the same as [#112](../112-path-sum/) (only a leaf completes a path); the new work is **collecting** every hit, not just detecting one.

**Backtracking DFS** ([`path_sum_ii.kara`](path_sum_ii.kara), the ★): thread one running `path` and one `out` list through the recursion as **`mut ref`** accumulators. Push the node's value descending, snapshot `path` into `out` when a leaf exhausts the remainder, and **pop on the way back up** — one shared buffer each, mutated in place, with an allocation only for the snapshot on a hit.

```
dfs(node, target, mut ref path, mut ref out):
    path.push(node.val)
    node is a leaf and rem == 0  ->  out.push(copy of path)
    else                          ->  dfs(left, rem, path, out); dfs(right, rem, path, out)
    path.pop()                       # backtrack
```

**Return-based** ([`path_sum_ii_return.kara`](path_sum_ii_return.kara)): purely functional — each call *returns* the list of qualifying paths rooted at its node. A leaf that hits the target returns `[[val]]`; an internal node collects its children's lists and **prepends its own value** to each. No shared mutable state; a distinct mechanism (return-and-prepend vs a backtracking accumulator) that must land on the identical set, in the identical left-to-right order — and it exercises nested `Vec[Vec[i64]]` construction and indexing (`sub[i][k]`, `sub[i].len()`) instead of in-place mutation.

## Kāra features exercised

- **`mut ref Vec[i64]` and `mut ref Vec[Vec[i64]]` accumulators** — the ★ solver threads two mutable borrows through the whole recursion; the call-site marker rule applies (`dfs(root, target, mut path, mut out)` marks the fresh owned bindings at the top call, while the recursive `dfs(n.left, rem, path, out)` forwards the already-`mut ref` bindings without re-marking). Same `mut ref Vec[Vec[i64]]` shape as [#48](../../1-100/48-rotate-image/) / [#73](../../1-100/73-set-matrix-zeroes/).
- **Backtracking via `Vec.push` / `Vec.pop`** — one buffer grown and shrunk in place; `path.pop()` returns `Option[i64]`, matched-and-discarded. The snapshot copies `path` element-by-element into a fresh `Vec[i64]` pushed onto `out`.
- **Nested `Vec[Vec[i64]]` return + indexing** — the return-based solver builds and reads nested vectors (`res.push(np)`, `sub[i][k]`, `sub[i].len()`), a distinct allocation shape from the accumulator.
- **`shared struct TreeNode` (RC), read-only traversal** — both solvers walk the shared-node tree without mutating it; on this non-escaping read-only walk the compiler elides the per-node retain/release (kara `B-2026-07-15-21`, default-ON). Node type mirrors kata [#112](../112-path-sum/).
- **Two construction shapes** — perfect uniform trees (one target collects *many* identical paths — 4/8/16 of them) and balanced distinct-value trees (one target, one content-varied path), so the verdict spans both multiplicity and content.

**v1 note.** Trees stay within the `≤ 5000`-node constraint. The sink folds each tree's path count and a rolling hash of every path (in DFS order) into a running accumulator. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the return-based + brute-force ground truth, and are valgrind-clean.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   path_sum_ii.kara
karac build path_sum_ii.kara && ./path_sum_ii

# The return-based variant (identical output):
karac run path_sum_ii_return.kara

# Python
python3 path_sum_ii.py

# Verify they all agree
diff <(karac run path_sum_ii.kara) <(python3 path_sum_ii.py)              && echo OK
diff <(karac run path_sum_ii.kara) <(karac run path_sum_ii_return.kara)   && echo OK

# Ground truth: backtracking == return-based == brute-force (battery + 20k fuzz)
python3 ground_truth.py
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`path_sum_ii.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** The canonical numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json). The corpus's canonical **Apple M5 Pro** numbers ([`bench/results.json`](bench/results.json)) are folded in separately; absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. Re-run `bench.sh` on the M5 to refresh the canonical table.

**Workload.** Build 8 **perfect depth-5** trees once (16 leaves each, distinct per-tree value so nothing hoists), then **K = 300,000** reps of the backtracking `path_sum` collecting **all 16** root-to-leaf paths on a **data-dependent-selected** tree (`idx = acc%8`, target `5*(idx+1)` hits every leaf), folding the returned `Vec[Vec[i64]]` into a rolling hash. Unlike [#112](../112-path-sum/)'s read-only bool walk, this is **alloc-bound**: each rep allocates 16 inner `Vec[i64]` path snapshots (plus the outer `Vec`) and the backtracking path buffer — the collect-and-copy regime. Each mirror uses its natural node: Kāra `shared` (RC) + a `mut ref` accumulator, C raw `*Node` + a growable path list, Go a GC slice accumulator, **Rust `Box` + `&mut Vec<Vec<i64>>`**. All five compiled mirrors (C/Rust/Rust-ovf/Go/kāra) must agree on `715901966` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../../1-100/69-sqrtx/)'s discipline) — the honest baseline to read Kāra against on the hash fold.

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **x86-64 container numbers** (canonical M5 pending; see the machine note):

| Implementation | Wall time | Node representation |
|---|---|---|
| c    path_sum_ii (clang -O3)                        | 275.8 ± 12.7 ms | `*Node` + growable list |
| rust path_sum_ii (rustc -O)                         | 328.4 ± 34.8 ms | `Box` + `&mut Vec<Vec>` |
| rust path_sum_ii (rustc -O, overflow-checks=on)      | 341.3 ± 18.4 ms | `Box` + `&mut Vec<Vec>` |
| **kāra path_sum_ii**                                | **345.2 ± 20.2 ms** | **`shared` (RC) + `mut ref`** |
| go   path_sum_ii (GC slices)                        | 678.1 ± 73.1 ms | `*Node` + GC slices |

**An alloc-bound workload, and Kāra sits at equal-safety-Rust parity — the collect-and-copy regime, not the read-only-walk one.** Every rep builds 16 five-element path snapshots plus the outer vector, so allocation and the copy dominate, not the per-node pointer chase. Kāra lands **1.01× the equal-safety Rust row** (341 ms), **1.05× stock `rustc -O`** (328 ms), and **1.25× behind C** (276 ms) — inside the fast-language band, and comfortably **ahead of Go** (678 ms), whose per-rep slice allocation feeds the GC (7.1 MiB RSS, ~2× everyone else). This is the same bracket as the corpus's other alloc-bound siblings ([#107](../107-binary-tree-level-order-traversal-ii/) / [#108](../108-convert-sorted-array-to-binary-search-tree/) / [#109](../109-convert-sorted-list-to-binary-search-tree/)), where allocation dominates and Kāra's RC nodes + `Vec` growth land at-or-ahead of Rust — the mirror image of the pure read-only walks ([#100](../../1-100/100-same-tree/) / [#112](../112-path-sum/)), where there is nothing *but* the per-node tax. Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`) over the run. Python is listed at **237 ms but ran K = 15,000 — 1/20 of the compiled iterations** (pure-Python is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **2.4 MiB** peak RSS (above C's 1.5 MiB and Rust's 2.2 MiB, but a third of Go's 7.1 MiB). The kāra binary measures **324 KiB** here — a build-linkage artifact of this container run (heap-growing programs retain the backtrace-symbolizer tree `--gc-sections` should strip; a correct build is ~15 KiB), independent of the runtime numbers, flagged for the M5 — vs C's 16 KiB and Go's 2.1 MiB.

**Flagged for the M5 re-bench** — the corpus has seen container orderings shift on the M5's wider core (see [#97](../../1-100/97-interleaving-string/)), so treat the *margins* as data points; the direction (Kāra at Rust parity on an alloc-bound collect) is robust across the alloc-bound siblings, but the sizes may shift.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference) and, once folded in, [`bench/results.json`](bench/results.json) (M5, canonical).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched **alloc-bound** path collection (`shared` RC + a `mut ref` accumulator vs `Box` + `&mut Vec<Vec<i64>>`), where Kāra reaches equal-safety parity as allocation dominates the per-node tax. C's raw pointer + hand-rolled list is the metal floor, Go the GC data point (and the clear outlier here, on per-rep slice churn), Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
