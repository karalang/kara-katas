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

- **`shared struct TreeNode` (RC), read-only traversal** — both solvers walk the shared-node tree without mutating it; the recursion passes `Option[TreeNode]` **by value**. This kata's wrapper-delegates-to-helper shape (`is_balanced(root)` forwarding a `Ref` param to the recursive `check`) is what drove the **borrow-forward** relaxation (kara `B-2026-07-15-21` Part C); with it, `check`'s per-node retain/release is elided entirely (see the benchmark note — the sweep's former holdout, now folded in). Node type mirrors kata [#104](../104-maximum-depth-of-binary-tree/) / [#100](../../1-100/100-same-tree/).
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

> **Machine.** The canonical numbers below are the corpus's **Apple M5 Pro** run — [`bench/results.json`](bench/results.json) (fixed [kara `B-2026-07-15-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) karac). A shared **x86-64 Linux cloud-container** reference run is kept alongside in [`bench/results.container-x86.json`](bench/results.container-x86.json); absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. The hosts shift the vs-C ratio (container ~1.08×, M5 1.34×) — M5's faster cores favor the raw pointer-chase over kāra's per-node decode+check — while the like-for-like equal-safety-Rust ratio stays tight on both (0.99× / 1.12×); see the note below.

**Workload.** Build 8 balanced 31-node trees once, then **K = 3,000,000** reps of the bottom-up single-pass `is_balanced` on a **data-dependent-selected** tree (`idx = acc%8`, seeded by the running hash, so nothing hoists), folding each verdict into a rolling polynomial hash. The trees are balanced, so `check` runs the **full** post-order (no early -1) — a **read-only per-node traversal** (match `Option[shared]` + one field read per node, no allocation), so any per-node overhead *is* the whole cost. Each mirror uses its natural node: Kāra `shared` (RC, passed by value), C/Go raw pointer, **Rust `Box` + `&`-borrow**. All five compiled mirrors must agree on `539878958` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../../1-100/69-sqrtx/)'s discipline) — and it matters here: `min_depth`/`max_depth`/`check` each do a per-node add, so the overflow-check row is the honest equal-safety baseline (not a rounding effect).

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **Apple M5 Pro numbers** (canonical; sink `539878958` agreed by all five mirrors), on the fixed [kara `B-2026-07-15-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) karac. Per-sample variance runs ±5–6 % on this post-order workload, but the means are stable to ~1 ms across repeat runs:

| Implementation | Wall time | Node representation |
|---|---|---|
| c    is_balanced (clang -O3)                        | 121.4 ± 7.1 ms | `*Node` |
| go   is_balanced (GC `*Node`)                       | 139.3 ± 4.1 ms | `*Node` |
| rust is_balanced (rustc -O, overflow-checks=on)      | 144.7 ± 6.1 ms | `Box` + `&`-borrow |
| rust is_balanced (rustc -O)                         | 144.9 ± 6.3 ms | `Box` + `&`-borrow |
| **kāra is_balanced**                                | **162.0 ± 9.2 ms** | **`shared` (RC)** |

**This kata was the traversal sweep's *last holdout* — and closing it drove a third compiler fix.** When [kara `B-2026-07-15-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) Parts A/B landed, its four siblings ([#100](../../1-100/100-same-tree/) / [#104](../104-maximum-depth-of-binary-tree/) / [#111](../111-minimum-depth-of-binary-tree/) / [#112](../112-path-sum/)) closed to Rust parity but `is_balanced` stayed ~1.46× behind — its recursive `check` helper was excluded from RC-elision. **Why it was excluded, and how it got fixed:** the analysis's condition 1 required every call site to pass a **projection**, and the thin wrapper `fn is_balanced(root) -> bool { check(root) != -1 }` calls `check(root)` with a **bare identifier**, originally scored as a move. But `root` is a `Ref`-mode param (a read-only borrow), so its referent is kept alive by the caller for the whole call — forwarding it *is* a borrow. **Part C** relaxed condition 1 to accept exactly this **borrow-forward** (a bare identifier naming a `Ref` param), which folds `check` into the elided set: its by-value `Option[shared]` walk now carries **zero rc ops per node** (an earlier draft of this README wrongly called RC "free" here — the object code had shown the `incq`/`decq` pairs; they are *now* genuinely gone). Result (container, where the fix was profiled): **616 → 354 ms (1.74× faster)**, from last-place holdout to just ahead of the equal-safety Rust row. The **M5 canonical** run confirms the RC is elided: kāra **162 ms is 1.12× the equal-safety Rust** (`overflow-checks=on`, 145 ms) — the honest like-for-like — and 1.34× C, whose raw `-O3` skips the per-node height-add overflow check that kāra *and* equal-safety Rust both pay. M5's faster cores widen the vs-C ratio from the container's ~8% (the raw pointer-chase speeds up more than kāra's `Option[shared]` decode + check), so on M5 this is the sweep's widest read-only-walk gap — but still inside the C/Rust cluster and at near-parity with the like-for-like Rust. `check` combines both child heights (`1 + max(l, r)`), so there is no tail-call to loop-ify — the RC removal alone does it. So the whole read-only-traversal sweep now elides. Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`) over the run. Python is listed at **283 ms but ran K = 150,000 — 1/20 of the compiled iterations** (pure-Python recursion is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **2.5 MiB** peak RSS (above C's 1.5 MiB, Rust's 2.3 MiB, Go's 1.9 MiB — all within a tight band). The kāra binary measures **324 KiB** here — a build-linkage artifact of this container run (heap-growing programs retain the backtrace-symbolizer tree `--gc-sections` should strip; a correct build is ~15 KiB), independent of the runtime numbers, flagged for the M5 — vs C's 16 KiB and Go's 2.2 MiB.

**Flagged for the M5 re-bench** — the corpus has seen container tree-traversal orderings compress sharply on the M5's wider core (see [#97](../../1-100/97-interleaving-string/)), so treat the *margin* as a data point, not a verdict; the direction (Kāra trailing on a pure per-node walk) is robust across [#104](../104-maximum-depth-of-binary-tree/) / [#100](../../1-100/100-same-tree/), but the size may compress.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.json`](bench/results.json) (M5, canonical) and [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched read-only tree traversal (`shared` handle walk vs `Box` + `&`-borrow), the exposed RC/traversal regime shared with [#104](../104-maximum-depth-of-binary-tree/) / [#100](../../1-100/100-same-tree/). C's raw pointer chase is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
