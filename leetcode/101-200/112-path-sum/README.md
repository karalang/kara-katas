# 112. Path Sum

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Tree · Depth-First Search · Breadth-First Search · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/path-sum](https://leetcode.com/problems/path-sum/)

Given a binary tree and an integer `target`, return **true** iff the tree has a **root-to-leaf** path whose node values sum to `target`. A leaf is a node with no children.

```
        5              target = 22  ->  true
       / \             (5 → 4 → 11 → 2 = 22)
      4   8
     /   / \           target = 26  ->  false
    11  13  4          (no root-to-leaf path sums to 26; the
   /  \        \        internal-node partial sums don't count —
  7    2        1       a path must END at a leaf)
```

**Constraints:** `0 ≤ #nodes ≤ 5000`, node values fit `-1000 … 1000`, `target` fits `-10^9 … 10^9`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Recursive DFS, running remainder** ★ | [`path_sum.kara`](path_sum.kara) ✓ | [`path_sum.py`](path_sum.py) ✓ |
| **Iterative DFS, parallel `(node, remaining)` stacks** | [`path_sum_iter.kara`](path_sum_iter.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for both approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the two Kāra approaches agree with **each other** and with the Python mirror. An independent **ground-truth check** confirms the answer three ways: the recursive DFS equals an iterative `(node, remaining)` stack *and* a brute-force test of `target` against the set of **every** root-to-leaf path sum, on a case battery **and 20,000 randomised (tree, target) pairs**, zero disagreements. Both solvers compile with zero diagnostics and are valgrind-clean.

## The leaf rule

The subtlety is the **leaf** requirement: a path must end at a node with no children. Subtract each node's value from the remaining target as you descend; the answer is yes exactly when some **leaf** is reached with remainder zero. An internal node that happens to hit remainder zero does **not** count — the same "you must reach a leaf" discipline as minimum depth ([#111](../111-minimum-depth-of-binary-tree/)).

**Recursive DFS** ([`path_sum.kara`](path_sum.kara), the ★): OR the two child recursions with the reduced remainder; a missing child contributes `false`, and short-circuiting returns on the first satisfying path.

```
has_path_sum(node, target):
    node is None -> false
    rem = target - node.val
    node is a leaf -> rem == 0            # the path completes iff the remainder is exhausted
    else -> has_path_sum(left, rem) or has_path_sum(right, rem)
```

**Iterative DFS** ([`path_sum_iter.kara`](path_sum_iter.kara)): the same descent driven by two parallel worklists — a `Vec[TreeNode]` of nodes still to visit and a `Vec[i64]` of the target remaining when each was pushed. Pop a pair, subtract; if it is a leaf with remainder zero, return immediately; otherwise push each child with the reduced remainder. A distinct mechanism (explicit stack vs the call stack) landing on the identical verdict — and it exercises returning **early** while the `Vec[shared]` node stack still holds residual entries (the residual-worklist drop surface of kata [#111](../111-minimum-depth-of-binary-tree/), now clean).

## Kāra features exercised

- **`shared struct TreeNode` (RC), read-only traversal** — both solvers walk the shared-node tree without mutating it; the DFS passes `Option[TreeNode]` **by value**. On a provably read-only, non-escaping walk the compiler now elides the per-node retain/release entirely and (via the `or` short-circuit's tail position) loop-ifies the recursion (kara `B-2026-07-15-21`, default-ON) — the win this kata drove (see the benchmark note). Node type mirrors kata [#104](../104-maximum-depth-of-binary-tree/) / [#110](../110-balanced-binary-tree/) / [#111](../111-minimum-depth-of-binary-tree/).
- **Nested `Option[shared]` match to test leaf-ness** — the leaf rule is a two-way match on each of `(left, right)` being present or empty.
- **Two parallel `Vec` worklists advanced by `pop()`** — the iterative solver keeps nodes and remainders in lockstep, peeking the remainder (`rems[rems.len() - 1]`) then popping both; the node worklist is a `Vec[shared]` advanced by `stack.pop()` (the surface hardened by kara `a384971`).
- **Early `return` out of a loop with a live `Vec[shared]` worklist** — the iterative DFS returns the moment a satisfying leaf is found, dropping the still-populated node/remainder stacks; the residual `Vec[shared]` drop releases their elements cleanly (valgrind-clean).
- **Two construction shapes** — balanced trees (middle-pick) and skewed chains (ascending insert); an achievable target (a real leftmost-path sum) forces `true`, an out-of-range one forces `false`, so the verdict genuinely varies.

**v1 note.** Trees stay within the `≤ 5000`-node constraint. The sink folds each tree's boolean verdict into a running polynomial hash. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the iterative + brute-force ground truth, and are valgrind-clean.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   path_sum.kara
karac build path_sum.kara && ./path_sum

# The iterative-stack variant (identical output):
karac run path_sum_iter.kara

# Python
python3 path_sum.py

# Verify they all agree
diff <(karac run path_sum.kara) <(python3 path_sum.py)          && echo OK
diff <(karac run path_sum.kara) <(karac run path_sum_iter.kara) && echo OK

# Ground truth: DFS == iterative == brute-force set-membership (battery + 20k fuzz)
python3 ground_truth.py
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`path_sum.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** The canonical numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json). The corpus's canonical **Apple M5 Pro** numbers ([`bench/results.json`](bench/results.json)) are folded in separately; absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. Re-run `bench.sh` on the M5 to refresh the canonical table.

**Workload.** Build 8 balanced 31-node trees once, then **K = 6,000,000** reps of the recursive `has_path_sum` against an **unachievable** target (1e9, far above any 31-node path sum) on a **data-dependent-selected** tree (`idx = acc%8`, seeded by the running hash, so nothing hoists), folding each verdict into a rolling polynomial hash. With no satisfying path, the OR recursion explores the **whole** tree — a **read-only per-node traversal** (match `Option[shared]` + one field read + a subtract per node, no allocation), so any per-node overhead *is* the whole cost. Each mirror uses its natural node: Kāra `shared` (RC, passed by value), C/Go raw pointer, **Rust `Box` + `&`-borrow**. All five compiled mirrors must agree on `380360184` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../../1-100/69-sqrtx/)'s discipline). Here the per-node work is a single subtract whose check the branch predictor hides — the two Rust rows sit within noise of each other, so overflow-safety is essentially free on this shape, and the `overflow-checks=on` row is the honest baseline to read Kāra against.

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **x86-64 container numbers** (canonical M5 pending; see the machine note):

| Implementation | Wall time | Node representation |
|---|---|---|
| c    path_sum (clang -O3)                          | 260.2 ± 10.3 ms | `*Node` |
| **kāra path_sum**                                  | **285.1 ± 6.9 ms** | **`shared` (RC)** |
| rust path_sum (rustc -O, overflow-checks=on)        | 299.2 ± 4.9 ms | `Box` + `&`-borrow |
| rust path_sum (rustc -O)                            | 309.4 ± 14.6 ms | `Box` + `&`-borrow |
| go   path_sum (GC `*Node`)                          | 392.1 ± 10.4 ms | `*Node` |

**This kata found a real compiler gap, and it got fixed — Kāra now lands *second, ahead of both Rust builds*, on a pure read-only tree walk.** This is the dogfooding loop working end to end. Each rep is *only* `match` + a field-read + a subtract per node down a full 31-node descent — no allocation, so any per-node overhead *is* the entire cost, which made this (and its siblings [#100](../../1-100/100-same-tree/) / [#104](../104-maximum-depth-of-binary-tree/) / [#111](../111-minimum-depth-of-binary-tree/)) the exposed worst case. Disassembly of the hot loop surfaced two real defects, both now fixed under [kara `B-2026-07-15-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl):

- **Refcount traffic that was *not* being elided.** The by-value `Option[shared]` walk was emitting **two retains + two releases per visited node** (an earlier draft of this README claimed "RC is free / already elided" — that was wrong; the object code showed the `incq`/`decq` pairs). The fix makes the RC-elision convention (`rc_elide.rs`) **default-ON**: for a provably read-only, non-escaping borrowed `shared`/`Option[shared]` param the balanced retain/release pair is skipped — sound by construction (four conditions + a payload-escape guard), validated leak-clean on the LSan gate.
- **A blocked tail-call.** The surviving `Some(n)`-binding release ran *after* the recursive call, keeping it out of tail position — so Kāra made two real calls per node where C makes one call and loops the tail child's spine. Eliding that release too (Part B) unblocks LLVM's `tailcallelim`: the recursion now **loop-ifies**, matching C's structure. The hot function ends up with **zero rc ops per node** and a `jne` back-edge instead of the second `call`.

Net: **556 → 285 ms**, from **1.8× behind Rust to *ahead* of equal-safety Rust** (299 ms) and stock `rustc -O` (309 ms), sitting **1.10× behind C** — the sole remaining difference being the per-node overflow-check `jo` that C omits (the deliberate safety tax). Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`). Python is listed at **642 ms but ran K = 300,000 — 1/20 of the compiled iterations** (pure-Python recursion is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **2.3 MiB** peak RSS (level with Rust's 2.2 MiB, above C's 1.5 MiB and Go's 1.8 MiB — all within a tight band). The kāra binary measures **324 KiB** here — a build-linkage artifact of this container run (heap-growing programs retain the backtrace-symbolizer tree `--gc-sections` should strip; a correct build is ~15 KiB), independent of the runtime numbers, flagged for the M5 — vs C's 16 KiB and Go's 2.2 MiB.

**Flagged for the M5 re-bench** — the corpus has seen container tree-traversal orderings compress sharply on the M5's wider core (see [#97](../../1-100/97-interleaving-string/)), so treat the *margin* as a data point; the direction (Kāra now at C/Rust parity on a pure per-node walk, post-fix) should hold, but the size may shift.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference) and, once folded in, [`bench/results.json`](bench/results.json) (M5, canonical).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched read-only tree traversal (`shared` handle walk vs `Box` + `&`-borrow). This is exactly the regime that exposed [kara `B-2026-07-15-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) (unelided per-node refcount traffic + a blocked tail-call), shared with [#100](../../1-100/100-same-tree/) / [#104](../104-maximum-depth-of-binary-tree/) / [#111](../111-minimum-depth-of-binary-tree/); with that fixed the `shared`-handle walk now runs at-or-ahead of the equal-safety `Box`+`&`-borrow. C's raw pointer chase is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
