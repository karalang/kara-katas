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

No compiler bugs found.

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
```
