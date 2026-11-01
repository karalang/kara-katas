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

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`768360140`). Workload: build 8 balanced 31-node trees once, then K=3000000 reps of recursive min_depth on a data-dependent-selected tree (idx=acc%8), folding each minimum depth into a rolling polynomial hash; read-only per-node post-order traversal (no allocation), the exposed RC/traversal regime.

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-11-01, karac g6697158fa (v2/MIR backend) (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Go | 148.2 ms | 0.80× |
| C `clang -O3` | 159.1 ms | 0.86× |
| Rust `-O` | 169.9 ms | 0.91× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 185.3 ms | 1.00× |
| **Kāra (codegen)** | 185.9 ms | 1.00× |

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

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

> ✅ **M5 re-bench (2026-11-01).** The canonical numbers below are the corpus's **Apple M5 Pro** run (6P+12E, Darwin 25.6.0; **karac g6697158fa** (0.9.0-dev.14057, the v2/MIR backend; the legacy backend was deleted 2026-10-23), `rustc 1.95.0`, Apple clang 21.0.0, `go 1.26.3`, hyperfine 1.20) — [`bench/results.json`](bench/results.json). Against the 2026-07-27 legacy-backend snapshot kāra is flat against every comparator (each move under this session's ~10 % noise band): kāra/Rust 1.07× → 1.09×, kāra/equal-safety Rust 0.99× → 1.00×, kāra/C 1.19× → 1.17×, kāra/Go 1.19× → 1.25×. A shared **x86-64 Linux cloud-container** reference run is kept alongside in [`bench/results.container-x86.json`](bench/results.container-x86.json); absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. History: the margin compressed on the M5 as the container note predicted, but the *direction* held: kāra sits at parity with the equal-safety Rust row on both hosts (M5 1.00× on the 2026-07-15 legacy run and again 1.00× on 2026-11-01; container 1.03×).

**Workload.** Build 8 balanced 31-node trees once, then **K = 3,000,000** reps of the recursive `min_depth` on a **data-dependent-selected** tree (`idx = acc%8`, seeded by the running hash, so nothing hoists), folding each minimum depth into a rolling polynomial hash. `min_depth` computes *both* subtree depths at every node, so on a balanced tree it runs the **full** post-order — a **read-only per-node traversal** (match `Option[shared]` + one field read per node, no allocation), so any per-node overhead *is* the whole cost. Each mirror uses its natural node: Kāra `shared` (RC, passed by value), C/Go raw pointer, **Rust `Box` + `&`-borrow**. All five compiled mirrors must agree on `768360140` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../../1-100/69-sqrtx/)'s discipline) — and it matters here: `min_depth`/`max_depth`/`check` each do a per-node add, so the overflow-check row is the honest equal-safety baseline (not a rounding effect).

`--warmup 5 --runs 30 --shell=none`. All single-threaded, ~99 % CPU (the default build emits no call of `karac_mir_task_spawn`, verified in the emitted IR (`KARAC_MIR_LL`), same as its `KARAC_AUTO_PAR=0` twin). **Apple M5 Pro numbers, karac g6697158fa, 2026-11-01** (canonical; sink `768360140` agreed by all five mirrors):

| Implementation | Wall time | Node representation |
|---|---|---|
| go   min_depth (GC `*Node`)                         | 148.2 ± 7.6 ms | `*Node` |
| c    min_depth (clang -O3)                          | 159.1 ± 8.1 ms | `*Node` |
| rust min_depth (rustc -O)                           | 169.9 ± 7.7 ms | `Box` + `&`-borrow |
| rust min_depth (rustc -O, overflow-checks=on)        | 185.3 ± 8.9 ms | `Box` + `&`-borrow |
| **kāra min_depth**                                  | **185.9 ± 12.5 ms** | **`shared` (RC)** |

**This kata helped expose a real compiler gap that is now fixed — Kāra runs at parity with equal-safety Rust here.** Each rep is *only* `match` + a field-access + a per-node add down a full 31-node post-order: no allocation, so any per-node overhead *is* the entire cost, which made this (with [#100](../../1-100/100-same-tree/) / [#104](../104-maximum-depth-of-binary-tree/) / [#112](../112-path-sum/)) the exposed worst case that surfaced [kara `B-2026-07-15-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl). Disassembly showed the by-value `Option[shared]` walk was emitting **two retains + two releases per visited node** — refcount traffic that was *not* being elided (an earlier draft of this README wrongly claimed "RC is free / already elided"; the object code proved otherwise). The fix makes the RC-elision convention **default-ON** and additionally elides the `Some(n)`-binding pair, so the walk now carries **zero rc ops per node**. The decomposition against the fixed compiler:

- **Refcount traffic — eliminated.** What was ~½ the old gap is gone: on the M5 canonical run (2026-11-01, v2/MIR) Kāra lands at **185.9 ms**, **1.00× the equal-safety Rust row (185.3 ms) — parity** (the 2026-07-15 legacy M5 run and the container reference showed the same verdict, at 1.00× and 1.03×), where before the fix the by-value walk's two-retains-two-releases-per-node left it well behind.
- **Overflow-checking safety — the honest remaining split vs *stock* Rust.** `min_depth` does a per-node add, so Kāra's default i64-overflow check is a real cost stock `rustc -O` (169.9 ms, Kāra 1.09×) skips; the like-for-like is the `overflow-checks=on` row (185.3 ms), where Kāra sits level. That check is also the whole of the **1.17× gap to C** (159.1 ms), which `-O3` wraps; Go (148.2 ms) leads this run, Kāra 1.25× behind it. Unlike the `and`/`or` short-circuit shapes ([#100](../../1-100/100-same-tree/) / [#112](../112-path-sum/)), `min_depth` **combines both** child results (`1 + min(l, r)`), so neither recursion is in tail position and LLVM cannot loop-ify it — the RC removal alone closes the gap, without the extra tail-call win those siblings get.

Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`) over the run. Python is listed at **206 ms (last measured 2026-07-15, not re-run 2026-11-01) but ran K = 150,000 — 1/20 of the compiled iterations** (pure-Python recursion is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **1.05 MiB** peak RSS (C 1.02, Rust 1.06; Go 2.7 MiB). Binary size: c 32.9 KiB, **kāra 295.8 KiB**, rust 456.3 KiB, go 2.38 MiB; every MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (the legacy M5 kāra binary here was 33.4 KiB), tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). Compile-cold on the M5 is clang 46.2 ms < rustc 91.5 ms < **karac 120.2 ms** (2.6× clang, 1.31× rustc).

**M5 re-bench (2026-07-15, legacy backend; history).** As the container note predicted, the margin compressed on the M5's wider core — **1.26× → 1.18× C** — while the direction held: Kāra trails C on a pure per-node walk (the overflow check C skips) yet sits at parity with the equal-safety Rust row, a pattern robust across [#104](../104-maximum-depth-of-binary-tree/) / [#110](../110-balanced-binary-tree/) / [#100](../../1-100/100-same-tree/). (2026-11-01 note: on the v2/MIR backend the pattern still holds — 1.17× C, 1.00× equal-safety Rust.)

Compile-cold, binary size, and peak-RSS records are in [`bench/results.json`](bench/results.json) (M5, canonical) and [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched read-only tree traversal (`shared` handle walk vs `Box` + `&`-borrow), the exposed RC/traversal regime shared with [#104](../104-maximum-depth-of-binary-tree/) / [#110](../110-balanced-binary-tree/). C's raw pointer chase is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
