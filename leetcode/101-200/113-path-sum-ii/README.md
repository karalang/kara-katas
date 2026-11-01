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

<!-- placement-caveat -->
**Measurement caveat — code placement.** This kata's runtime moves by up to **6%** with code placement alone: rebuilt with its machine code sitting at a different address, the same program, same compiler and same input runs that much faster or slower. That is wider than the **1.2%** margin against `clang -O3` quoted below, so read that comparison as a tie rather than as a result. Measured across four code placements against a same-binary control — see [`placement-spread.json`](../../../placement-spread.json) and [BENCHMARKS.md](../../../BENCHMARKS.md#code-placement-arm64).

## Benchmarks
Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`path_sum_ii.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5 re-bench (2026-11-01).** The canonical numbers below are the corpus's **Apple M5 Pro** run (6P+12E, Darwin 25.6.0; **karac g6697158fa** (0.9.0-dev.14057, the v2/MIR backend; the legacy backend was deleted 2026-10-23), `rustc 1.95.0`, Apple clang 21.0.0, `go 1.26.3`, hyperfine 1.20) — [`bench/results.json`](bench/results.json). Against the 2026-07-27 legacy-backend M5 snapshot kāra **improved against every comparator**: kāra/Rust 1.07× → 0.86×, kāra/equal-safety Rust 1.05× → 0.86×, kāra/C 1.24× → 1.01× (now tied), kāra/Go 1.23× → 0.91×. An earlier shared **x86-64 Linux cloud-container** run, which this section originally reported as canonical, is kept below as history; absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal.

**Workload.** Build 8 **perfect depth-5** trees once (16 leaves each, distinct per-tree value so nothing hoists), then **K = 300,000** reps of the backtracking `path_sum` collecting **all 16** root-to-leaf paths on a **data-dependent-selected** tree (`idx = acc%8`, target `5*(idx+1)` hits every leaf), folding the returned `Vec[Vec[i64]]` into a rolling hash. Unlike [#112](../112-path-sum/)'s read-only bool walk, this is **alloc-bound**: each rep allocates 16 inner `Vec[i64]` path snapshots (plus the outer `Vec`) and the backtracking path buffer — the collect-and-copy regime. Each mirror uses its natural node: Kāra `shared` (RC) + a `mut ref` accumulator, C raw `*Node` + a growable path list, Go a GC slice accumulator, **Rust `Box` + `&mut Vec<Vec<i64>>`**. All five compiled mirrors (C/Rust/Rust-ovf/Go/kāra) must agree on `715901966` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../../1-100/69-sqrtx/)'s discipline) — the honest baseline to read Kāra against on the hash fold.

`--warmup 5 --runs 30 --shell=none`. Single-threaded mirrors, ~99.5 % CPU (the default kāra build emits no call of `karac_mir_task_spawn`, verified in the emitted IR (`KARAC_MIR_LL`), same as its `KARAC_AUTO_PAR=0` twin; Go's runtime runs at 131 % CPU, 223.8 ms user). **Apple M5 Pro numbers, karac g6697158fa, 2026-11-01** (canonical; sink `715901966` agreed by all five mirrors):

| Implementation | Wall time | Node representation |
|---|---|---|
| c    path_sum_ii (clang -O3)                        | 197.8 ± 6.8 ms | `*Node` + growable list |
| **kāra path_sum_ii**                                | **200.3 ± 7.4 ms** | **`shared` (RC) + `mut ref`** |
| go   path_sum_ii (GC slices)                        | 221.1 ± 1.4 ms | `*Node` + GC slices |
| rust path_sum_ii (rustc -O)                         | 231.6 ± 7.3 ms | `Box` + `&mut Vec<Vec>` |
| rust path_sum_ii (rustc -O, overflow-checks=on)      | 232.2 ± 7.4 ms | `Box` + `&mut Vec<Vec>` |

**On the M5 (2026-11-01, v2/MIR) Kāra ties C and leads Rust and Go on this alloc-bound collect.** It runs at **0.86× stock and equal-safety Rust** (231.6 / 232.2 ms), **0.91× Go** (221.1 ms wall; also ahead on user-CPU, 198.6 vs 223.8 ms), and **1.01× C** (197.8 ms) — the 2.5 ms C gap is well inside either side's ~7 ms σ, so read it as a tie. kāra holds **1.09 MiB** peak RSS (C 1.08, Rust 1.13) vs Go's **9.25 MiB**. Binary size: c 33.0 KiB, **kāra 295.8 KiB**, rust 456.5 KiB, go 2.38 MiB; every MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (the legacy M5 kāra binary here was 33.6 KiB), tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). Compile-cold on the M5 is clang 48.5 ms < rustc 108.9 ms < **karac 127.2 ms** (2.6× clang, 1.17× rustc).

**x86-64 container numbers** (history: the earlier, undated container run this section first reported; [`bench/results.container-x86.json`](bench/results.container-x86.json) now holds a later 2026-10-30 container run, not reproduced here):

| Implementation | Wall time | Node representation |
|---|---|---|
| c    path_sum_ii (clang -O3)                        | 275.8 ± 12.7 ms | `*Node` + growable list |
| rust path_sum_ii (rustc -O)                         | 328.4 ± 34.8 ms | `Box` + `&mut Vec<Vec>` |
| rust path_sum_ii (rustc -O, overflow-checks=on)      | 341.3 ± 18.4 ms | `Box` + `&mut Vec<Vec>` |
| **kāra path_sum_ii**                                | **345.2 ± 20.2 ms** | **`shared` (RC) + `mut ref`** |
| go   path_sum_ii (GC slices)                        | 678.1 ± 73.1 ms | `*Node` + GC slices |

**On this container run: an alloc-bound workload, and Kāra sits at equal-safety-Rust parity — the collect-and-copy regime, not the read-only-walk one.** Every rep builds 16 five-element path snapshots plus the outer vector, so allocation and the copy dominate, not the per-node pointer chase. Kāra lands **1.01× the equal-safety Rust row** (341 ms), **1.05× stock `rustc -O`** (328 ms), and **1.25× behind C** (276 ms) — inside the fast-language band, and comfortably **ahead of Go** (678 ms), whose per-rep slice allocation feeds the GC (7.1 MiB RSS, ~2× everyone else). This is the same bracket as the corpus's other alloc-bound siblings ([#107](../107-binary-tree-level-order-traversal-ii/) / [#108](../108-convert-sorted-array-to-binary-search-tree/) / [#109](../109-convert-sorted-list-to-binary-search-tree/)), where allocation dominates and Kāra's RC nodes + `Vec` growth land at-or-ahead of Rust — the mirror image of the pure read-only walks ([#100](../../1-100/100-same-tree/) / [#112](../112-path-sum/)), where there is nothing *but* the per-node tax. Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`) over the run. Python is listed at **237 ms (earlier container run, not re-run 2026-11-01) but ran K = 15,000 — 1/20 of the compiled iterations** (pure-Python is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **2.4 MiB** peak RSS (above C's 1.5 MiB and Rust's 2.2 MiB, but a third of Go's 7.1 MiB). The kāra binary measures **324 KiB** here — a build-linkage artifact of this container run (heap-growing programs retain the backtrace-symbolizer tree `--gc-sections` should strip; a correct build is ~15 KiB), independent of the runtime numbers, flagged for the M5 — vs C's 16 KiB and Go's 2.1 MiB.

**Flagged for the M5 re-bench** — the corpus has seen container orderings shift on the M5's wider core (see [#97](../../1-100/97-interleaving-string/)), so treat the *margins* as data points; the direction (Kāra at Rust parity on an alloc-bound collect) is robust across the alloc-bound siblings, but the sizes may shift. (2026-11-01 note: on the M5 v2/MIR run Kāra is ahead of Rust, 0.86×, and Go, 0.91×, and tied with C; see the M5 table above.)

Compile-cold, binary size, and peak-RSS records are in [`bench/results.json`](bench/results.json) (M5, canonical) and [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched **alloc-bound** path collection (`shared` RC + a `mut ref` accumulator vs `Box` + `&mut Vec<Vec<i64>>`), where Kāra reaches equal-safety parity (container) or better (0.86× on the 2026-11-01 M5 run) as allocation dominates the per-node tax. C's raw pointer + hand-rolled list is the metal floor, Go the GC data point (and the clear outlier here, on per-rep slice churn), Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
