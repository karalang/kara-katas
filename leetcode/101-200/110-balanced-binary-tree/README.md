# 110. Balanced Binary Tree

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Tree · Depth-First Search · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/balanced-binary-tree](https://leetcode.com/problems/balanced-binary-tree/)

Decide whether a binary tree is **height-balanced** — at every node, the two subtrees' heights differ by at most one.

```
    3          balanced          1              NOT balanced
   / \         (true)            \              (true, the whole tree,
  9  20                           2              is skewed: the root's left
     / \                          \              height 0 vs right height 3)
    15  7                          3
                                    \
                                     4
```

**Constraints:** `0 ≤ #nodes ≤ 5000`, node values fit `-10^4 … 10^4`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Bottom-up single pass** ★ | [`is_balanced.kara`](is_balanced.kara) ✓ | [`is_balanced.py`](is_balanced.py) ✓ |
| **Top-down height recompute (naive O(n²))** | [`is_balanced_topdown.kara`](is_balanced_topdown.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for both approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the two Kāra approaches agree with **each other** and with the Python mirror. An independent **ground-truth check** confirms the verdict three ways: the bottom-up single pass equals a top-down height-recompute *and* a brute-force check (`|height(left) − height(right)| ≤ 1` at **every** node), on a case battery **and 20,000 randomised trees**, zero disagreements. Both solvers compile with zero diagnostics and are valgrind-clean.

## Two ways to check balance

**Bottom-up single pass** ([`is_balanced.kara`](is_balanced.kara), the ★): the elegant O(n) form. A single post-order recursion `check` returns each subtree's **height** — or the sentinel **-1** the instant any subtree is found unbalanced. The -1 propagates straight up and short-circuits the rest of the walk; `is_balanced` is just `check(root) != -1`. Each node is visited once.

```
check(node):
    node is None -> 0
    lh = check(left);   if lh == -1 -> -1
    rh = check(right);  if rh == -1 -> -1
    |lh - rh| > 1       -> -1
    else                -> 1 + max(lh, rh)
```

**Top-down height recompute** ([`is_balanced_topdown.kara`](is_balanced_topdown.kara)): the textbook definition transcribed literally — a node is balanced when its two subtree heights differ by at most one **and** both subtrees are balanced, with `height` computed by a *separate* walk. Because every ancestor re-measures a node, it is O(n²) in the worst case (a skewed tree). A genuinely different mechanism (two cooperating recursions vs one sentinel pass) that must return the identical verdict.

## Kāra features exercised

- **`shared struct TreeNode` (RC), read-only traversal** — both solvers walk the shared-node tree without mutating it; the recursion passes `Option[TreeNode]` **by value** (a cheap RC-handle pass that rc-inc/decs each visited node). Node type mirrors kata [#104](../104-maximum-depth-of-binary-tree/) / [#100](../../1-100/100-same-tree/).
- **Sentinel return + early `return`** — the bottom-up `check` returns `-1` up the stack the moment a subtree is unbalanced, short-circuiting the remaining walk (Kāra's `return` inside a `match` arm).
- **`and` short-circuit** — the top-down `is_balanced` stops at the first unbalanced subtree (`is_balanced(left) and is_balanced(right)`).
- **Two independent construction shapes** — the harness builds *balanced* trees by middle-pick and *skewed* chains by ascending insert, so the verdict is a genuine 4-true / 4-false mix.

**v1 note.** Trees stay within the `≤ 5000`-node constraint. The sink folds each tree's balanced/not verdict into a running polynomial hash (order-sensitive). Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the top-down + brute-force fuzz ground truth, and are valgrind-clean.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   is_balanced.kara
karac build is_balanced.kara && ./is_balanced

# The top-down (naive O(n^2)) variant (identical output):
karac run is_balanced_topdown.kara

# Python
python3 is_balanced.py

# Verify they all agree
diff <(karac run is_balanced.kara) <(python3 is_balanced.py)           && echo OK
diff <(karac run is_balanced.kara) <(karac run is_balanced_topdown.kara) && echo OK

# Ground truth: bottom-up == top-down == brute-force (battery + 20k fuzz)
python3 ground_truth.py
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`is_balanced.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** The canonical numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json). The corpus's canonical **Apple M5 Pro** numbers ([`bench/results.json`](bench/results.json)) are folded in separately; absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. Re-run `bench.sh` on the M5 to refresh the canonical table.

**Workload.** Build 8 balanced 31-node trees once, then **K = 3,000,000** reps of the bottom-up single-pass `is_balanced` on a **data-dependent-selected** tree (`idx = acc%8`, seeded by the running hash, so nothing hoists), folding each verdict into a rolling polynomial hash. The trees are balanced, so `check` runs the **full** post-order (no early -1) — a **read-only per-node traversal** (match `Option[shared]` + one field read per node, no allocation), so any per-node overhead *is* the whole cost. Each mirror uses its natural node: Kāra `shared` (RC, passed by value), C/Go raw pointer, **Rust `Box` + `&`-borrow**. All five compiled mirrors must agree on `539878958` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../../1-100/69-sqrtx/)'s discipline) — though on a pure-traversal loop the fold's `acc*131` is the only arithmetic, so the overflow-check row barely moves.

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **x86-64 container numbers** (canonical M5 pending; see the machine note):

| Implementation | Wall time | Node representation |
|---|---|---|
| c    is_balanced (clang -O3)                        | 324.5 ± 11.3 ms | `*Node` |
| rust is_balanced (rustc -O)                         | 326.4 ± 8.8 ms | `Box` + `&`-borrow |
| go   is_balanced (GC `*Node`)                       | 338.9 ± 3.5 ms | `*Node` |
| rust is_balanced (rustc -O, overflow-checks=on)      | 354.9 ± 8.0 ms | `Box` + `&`-borrow |
| **kāra is_balanced**                                | **600.0 ± 14.4 ms** | **`shared` (RC)** |

**Another pure read-only traversal, and Kāra trails on it — the same exposed RC regime as [#104](../104-maximum-depth-of-binary-tree/).** Each rep is *only* `match` + one field-access per node down a full 31-node post-order: no allocation, no compute beyond a height comparison, so any per-node overhead *is* the entire cost, with nothing to hide it behind. Kāra runs **1.85× behind C**, **1.84× behind Rust**, and **1.77× behind Go** — and the three fast languages cluster tightly (325–339 ms), all bounded by the same raw pointer/borrow chase, while Kāra sits apart. The gap has two contributors, both real codegen headroom and both isolated in [#100](../../1-100/100-same-tree/)'s profiled analysis of the identical read-only shape: passing `Option[TreeNode]` **by value** rc-inc/decs every visited node (a per-node reference count the borrow/pointer walks skip — #100 measured this at ~11 % of its gap via a `ref` borrow variant), and Kāra's per-node **`Option[shared]` traversal lowering** — decoding the niche, matching it, and GEP-ing the shared field is heavier than C/Rust's raw null-check-and-deref (the dominant remainder). Both are flagged as headroom, not waved off: RC-retain *elision* on a non-escaping borrow, and leaner `Option[shared]` match/field lowering. The alloc- and compute-bound siblings bracket this from the other side — [#107](../107-binary-tree-level-order-traversal-ii/) and [#108](../108-convert-sorted-array-to-binary-search-tree/) land Kāra at-or-ahead of Rust because allocation dominates and the per-node tax is amortized; here, as in [#104](../104-maximum-depth-of-binary-tree/), there is nothing *but* the per-node tax. Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`) over the run. Python is listed at **544 ms but ran K = 150,000 — 1/20 of the compiled iterations** (pure-Python recursion is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **2.5 MiB** peak RSS (above C's 1.5 MiB, Rust's 2.3 MiB, Go's 1.9 MiB — all within a tight band). The kāra binary measures **324 KiB** here — a build-linkage artifact of this container run (heap-growing programs retain the backtrace-symbolizer tree `--gc-sections` should strip; a correct build is ~15 KiB), independent of the runtime numbers, flagged for the M5 — vs C's 16 KiB and Go's 2.2 MiB.

**Flagged for the M5 re-bench** — the corpus has seen container tree-traversal orderings compress sharply on the M5's wider core (see [#97](../../1-100/97-interleaving-string/)), so treat the *margin* as a data point, not a verdict; the direction (Kāra trailing on a pure per-node walk) is robust across [#104](../104-maximum-depth-of-binary-tree/) / [#100](../../1-100/100-same-tree/), but the size may compress.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference) and, once folded in, [`bench/results.json`](bench/results.json) (M5, canonical).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched read-only tree traversal (`shared` handle walk vs `Box` + `&`-borrow), the exposed RC/traversal regime shared with [#104](../104-maximum-depth-of-binary-tree/) / [#100](../../1-100/100-same-tree/). C's raw pointer chase is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
