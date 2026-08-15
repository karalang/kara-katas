# 272. Closest Binary Search Tree Value II

Given a BST, a floating-point `target` and an integer `k`, return the **k values
closest to the target**. LeetCode accepts any order; this corpus returns them
**ascending**, so three independent solvers can be compared directly. When two
values are equally close, the **smaller** one wins — the same rule as
[#270](../270-closest-binary-search-tree-value/).

```
[4,2,5,1,3]  target 3.714286  k=2  ->  [3,4]
[4,2,5,1,3]  target 3.714286  k=4  ->  [2,3,4,5]
[4,2,5,1,3]  target 2.5       k=1  ->  [2]        tied with 3 — the smaller wins
[4,2,5,1,3]  target 2.5       k=3  ->  [1,2,3]    and again at the third slot
[4,2,5,1,3]  target -10.0     k=3  ->  [1,2,3]    target below every value
[4,2,5,1,3]  target 3.5       k=9  ->  [1,2,3,4,5]   k past the node count
```

**Constraints:** `1 ≤ n ≤ 10⁴`; `1 ≤ k ≤ n`; `0 ≤ Node.val ≤ 10⁹`;
`-10⁹ ≤ target ≤ 10⁹`. The solvers here also accept `k > n` and return
everything, because the harness generates that case on purpose.

## Approaches

| file | mechanism | cost |
|---|---|---|
| `closest_bst_values.kara` ★ | two partial in-order iterators, merged by distance | O(h + k) |
| `closest_bst_values_window.kara` | flatten in-order, binary-search, grow a window | O(n) |
| `closest_bst_values_rank.kara` | order every value by an explicit (distance, value) key | O(n²) |
| `differential.kara` | 4,000 randomized trees, three solvers cross-checked | — |
| `bench/k_closest.kara` | the ★ merge as a benchmark kernel, five languages | — |

The tree is parallel arrays — `val`, `left`, `right`, `-1` for a missing child —
so every mirror is identical and the algorithm is the traversal, not the
representation. Same shape as #270.

## The k closest values are contiguous, and that is the whole problem

In sorted order the values fall either side of the target: predecessors running
down away from it, successors running up away from it. Each of those sequences
is **already sorted by distance** — a predecessor further back is strictly
further away, and likewise forward. So the answer is a merge of two sorted
streams, and it is necessarily a **contiguous range** of the sorted values.

The ★ solver exploits that without ever materializing the sorted array. Two
stacks act as partial in-order iterators: descending from the root, a node below
the target goes on the predecessor stack and the walk continues right; a node at
or above it goes on the successor stack and the walk continues left. One descent
seeds both — O(h) — and afterwards the top of each stack is that side's nearest
value, with popping it advancing that iterator one step. Then k comparisons.
No full traversal, no sort, and no value examined that was not a candidate.

The window solver states the contiguity claim outright instead of leaning on it:
flatten, binary-search the insertion point, and grow the range `(lo, hi)`
outward k times. It costs a full O(n) flatten to save nothing asymptotically —
but it is a second reason to believe the same output, arrived at by index
arithmetic rather than by walking two iterators.

## The tie rule is decided by structure — in two solvers, and not in the third

The rule is "equal distance, smaller value." Both structural solvers get it for
**free**, because the smaller candidate is always the same one:

```kara
take_pred = dp <= ds;      // ★ : the predecessor is below the target
take_lo   = dl <= dh;      // window : `lo` is below `hi`
```

That is the entire tie-break. There is no value comparison to get wrong — one
character, `<=` versus `<`, is the whole rule. Which is exactly the problem:
**the same one-character mistake is available in both solvers, and it produces
the same wrong answer in both.**

The ranking solver has no structure to lean on. It compares two arbitrary nodes
and must say it outright:

```kara
if d < best_d or (d == best_d and vals[j] < vals[best]) { ... }
```

Exact `==` on `f64` is not a smell: a tie arises when the target sits at the
midpoint of two integers, and both distances are then the same representable
value, computed by the same subtraction.

## What the injected bugs did — and the one that proves the point

Scored against the 4,000-case harness:

| injection | mismatches |
|---|---:|
| window: start the range at `hi` instead of `hi - 1` | 3149 |
| ★ merge: `<` instead of `<=` (tie goes to the larger value) | 189 |
| window: `<` instead of `<=` — the same mistake, the other solver | 189 |
| **both structural solvers lose the tie rule at once** | **189** |
| ranking: drop the value tie-break from the key | 97 |

The fourth row is the one worth reading. Breaking **both** structural solvers
scores exactly what breaking either alone scores — because they now agree with
each other, and every one of those 189 detections is coming from the ranking
solver. Remove it from the comparison and the same doubly-broken harness reports:

```
mismatches 0
```

Two independently-written solvers, agreeing perfectly, both wrong. This is
[#270](../270-closest-binary-search-tree-value/)'s finding reproduced in a second
setting, and here it is a *measured* claim rather than an argument: the third
solver has to disagree about **method**, not merely about code, or a shared
mistake passes clean.

## The harness nearly disabled its own third check

The ranking solver was first fed the in-order array, because the harness already
had one. That quietly destroyed it. A selection sort scanning an **ascending**
array with a strict `<` keeps the first minimum it meets — which is already the
smaller value — so the explicit `(distance, value)` key is redundant and deleting
it costs nothing:

| ranking solver's input | tie-break deleted, mismatches |
|---|---:|
| the in-order (sorted) array | **0** |
| the DFS order the standalone solver actually uses | 97 |

Same shape as [#269](../269-alien-dictionary/)'s shared-helper defect: a harness
convenience that reads like tidying up, and takes a solver's independence with
it. The harness now hands the ranking solver the DFS order its own file uses.

## Two "obvious mistakes" that are not mistakes at all

Both boundary choices in this problem are genuine degrees of freedom, and the
harness says so with a byte-identical digest rather than merely a zero:

| variant | digest | mismatches |
|---|---|---:|
| as written | 836880122 | 0 |
| ★ descent sends a node **equal** to the target left instead of right | 836880122 | 0 |
| window uses `upper_bound` instead of `lower_bound` | 836880122 | 0 |
| both flipped at once | 836880122 | 0 |

A node exactly on the target has distance 0, so whichever stack or side it lands
on, it is taken first — and the stack invariant (predecessors below, successors
at or above) survives either placement. Worth knowing before "fixing" one of
them.

## Generator design

**Random float targets never tie.** Two values are equidistant only when the
target sits exactly at their midpoint, which a uniform draw hits with
probability zero — so a naive harness exercises the tie rule *zero* times and the
`<` that silently depends on visit order passes forever. The midpoints are
therefore constructed: one family targets exactly between two adjacent values,
another nudges that midpoint a hair each way so the boundary is probed from both
sides rather than only landed on. Two more families sit exactly on a value and
outside the range entirely.

`k` is its own axis — 1, a small draw, about half the tree, exactly `n`, and
`n + 2` — so the window running off both ends and `k` exceeding the node count
are hit on purpose rather than by luck.

And the counter is **decision steps**, not values: "a tie exists somewhere in
this tree" is not the same as "the algorithm had to rule on one." Only the
latter can change an answer, so only the latter is counted.

```
cases 4000
nodes built 83402
cases where a DECISION STEP saw a tie 844
targets outside the value range 1103
cases with k > n 851
digest 836880122
mismatches 0
```

## Benchmark

`bench/` builds one **30,000-node BST and 100,000 f64 targets** once, then
answers the `k=8` closest query for every target **10 times** — 1,000,000
queries. Sink `634219761`, reproduced by all four compiled mirrors and by Python.

**This is the corpus's stack-walk lane.** Per query the work is one root-to-leaf
descent that partitions the path into two iterator stacks, then k merge steps,
each popping a stack and pushing a subtree spine back onto it.
[#270](../270-closest-binary-search-tree-value/) already benches a plain BST
descent whose inner step is float arithmetic and a child choice; this one keeps
that and adds the part #270 does not have — an explicit stack whose depth varies
per step, written and read inside the loop the branches depend on.

Three parity decisions taken up front. **The stacks are hoisted** as flat arrays
with integer tops in every mirror, so nothing allocates once the punch loop
starts ([#267](../267-palindrome-permutation-ii/) measured what happens
otherwise). **Absolute value is each language's own** — `.abs()`, `fabs`,
`f64::abs`, `math.Abs`; #270 measured that hand-writing it in all five, on the
theory that a shared spelling was parity-safe, cost C 23% by itself. And
**targets span the value range**, which the program prints next to the sink
rather than leaving to be assumed — #270's other fault was a generator that put
every target below every node and turned 2.2M descents into 2.2M left-spine
walks:

```
634219761
nodes 30000 values 8..999982 targets 0..999994
```

### Runtime — sequential lane

Apple M5 Pro (6P+12E), 2026-08-15, `karac 0.1.0-dev.6106+g50267795a`, hyperfine
30 runs, `KARAC_AUTO_PAR=0`, every lane 99% CPU. This is the canonical host —
`bench/results.json`.

| Impl | Mean ± σ | vs Kāra |
|---|---|---|
| C `clang -O3` | 194.8 ± 5.8 ms | 0.93× |
| Rust `-O` | 200.7 ± 8.5 ms | 0.96× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 203.3 ± 7.4 ms | 0.97× |
| **Kāra (codegen)** | **209.7 ± 8.2 ms** | 1.00× |
| Go | 213.7 ± 4.7 ms | 1.02× |

**All five languages land inside a 1.10× band** with σ of 2.2–4.2%, so most of
the ordering here is not resolvable. Kāra is 1.08× behind C — down from the
container's 1.13× — and **level with equal-safety Rust** at 1.03×, which is
inside the noise and is the honest reading.

The container ranked Kāra last of five; so does this host, but the spread has
narrowed from 1.17× to 1.10× and the gap to equal-safety Rust is no longer
outside σ. A stack-driven tree walk with a bounded window is a shape Kāra runs at
the field's pace.

### The x86 corroboration run

| lang | mean (ms) | σ |
|---|---|---|
| C (`-march=x86-64-v3`) | 431.9 ± 10.4 | 2.4% |
| C | 447.5 ± 10.3 | 2.3% |
| Go | 465.4 ± 7.2 | 1.5% |
| Rust (checked, equal-safety) | 486.2 ± 8.5 | 1.8% |
| Rust (checked + `target-cpu=v3`) | 488.7 ± 11.9 | 2.4% |
| Rust | 498.4 ± 13.0 | 2.6% |
| **Kāra** | **504.3 ± 14.2** | 2.8% |

**The whole field spans 1.17×**, which is the tightest lane in the corpus so far.
Kāra is 1.04× behind the equal-safety Rust — the apples-to-apples column, since
Kāra checks integer overflow by default and plain `rustc -O` wraps — and 1.17×
behind C.

All three Rust builds land inside 2.5% of one another, and the ordering among
them flips between runs: `rust_ovf` came out *ahead* of plain `rust` here, which
is not a real inversion but a reminder that a 2% gap at σ 2% is not a ranking.
The honest statement is that overflow checking costs nothing measurable on this
workload, which makes sense — the arithmetic is a pointer chase, and the one
modular fold per query is a small fraction of it.

### The tight field was probed, and the obvious explanation failed

A ~703 KiB tree walked by ~15 dependent random loads per query looks
latency-bound, and if it were, codegen differences would wash out — so shrinking
the tree until it fits L1 should pull the languages apart. Moving only
`node_count` across a 150× range:

| tree | working set | Kāra / C |
|---|---|---:|
| 2,000 nodes | ~46 KiB | 1.21× |
| 30,000 nodes | ~703 KiB | 1.12× |
| 300,000 nodes | ~7 MiB | 1.23× |

Roughly flat, not monotone — **the hypothesis is wrong.** The compression is not
a cache effect; the languages are simply close on this workload, and the
remaining 1.1–1.2× is the ordinary bounds-check gap (C indexes unchecked; Kāra,
Rust and Go all check, on every tree load and every stack push and pop).

What the sweep *does* confirm is [#261](../261-graph-valid-tree/)'s lesson about
measurement stability: Kāra's σ goes 1.3% → 1.1% → **7.2%** across those three
sizes, and at 7 MiB the run-to-run variance exceeds the entire gap between the
languages. That is why the lane is sized where it is. Full write-up in
[`bench/probe/`](bench/probe/).

## Kāra features exercised

- **`mut ref Vec[i64]` parameters** — the two stack iterators are advanced in
  place by `advance_pred` / `advance_succ`, with `mut` written at the call site.
- **`f64.abs()`** — the native one. #270's bench learned the hard way that
  hand-writing `if x < 0.0 { 0.0 - x }` is the unnatural spelling in every
  language that has an absolute value, Kāra included.
- **`as f64` on an integer node value**, and exact `f64` equality where it is
  actually exact.
- **`bool` locals and `== false`** as loop and branch state.
- **`Vec[i64]` returned by value** from a function, and reversed in place.

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`; the ★ solver
and the differential match their Python mirrors.

The bench kernel is checked under the JIT and both AOT modes at full size, and
across all four surfaces plus Python at a reduced size (2,000 targets, 1 round) —
the tree-walk interpreter is not asked to run 1,000,000 queries.

The solvers found no compiler bug. **Trying to add a parallel bench lane found
one** — [`B-2026-08-15-19`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.md).

### Why this kata has no parallel lane

Its punch loop is embarrassingly parallel: 100,000 independent queries against a
read-only tree, folded into an order-invariant sink. [#270](../270-closest-binary-search-tree-value/)
and [#273](../273-integer-to-english-words/) have the same shape and both now
carry one.

Here `#[par_order_free]` is **silently ignored**. No fan-out, no diagnostic, and
`karac query concurrency` does not even list the loop among the declined ones —
it is absent from `loop_reductions` entirely. Timing confirms it: 568.9 ms with
the attribute against 569.3 ms without.

Bisecting from a body that does fan out toward one that does not:

| body | fans out |
|---|---|
| trivial | yes |
| + the read-only descent | yes |
| + two `Array[i64, 256]` locals written by the descent | yes |
| + the double-indexed distance reads `val[pred[pt - 1]]` and `.abs()` | yes |
| **+ the k-step merge loop** | **no** |

and from the failing shape, three simplifications that do *not* restore it:
dropping the nested spine-push `while`s, simplifying the compound `while a and
(b or c)` guard, and swapping the `Array` locals for `Vec`s. So it is none of
those individually — what the failing shape adds is a loop whose bound depends on
state an earlier loop in the same body mutated.

The classification gap may be reasonable; **the silence is not**. A loop the user
has explicitly annotated is the one case where the compiler knows parallelism was
expected, and the machinery to say "considered, declined, because X" already
exists on the disjoint-write path. Filed as a diagnostics defect rather than a
missing feature for that reason.

The lane will be built when the attribute either fans out or explains itself.

## Running

```bash
karac run closest_bst_values.kara
karac run closest_bst_values_window.kara
karac run closest_bst_values_rank.kara

diff <(karac run closest_bst_values.kara) <(python3 closest_bst_values.py) && echo OK

# 4,000 randomized trees, three solvers cross-checked
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in closest_bst_values closest_bst_values_window closest_bst_values_rank differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done

# cross-language benchmark (needs hyperfine, rustc, clang, go)
bash bench/bench.sh
```
