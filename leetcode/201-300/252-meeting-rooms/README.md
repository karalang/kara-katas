# 252. Meeting Rooms

Given meeting time intervals, could one person attend them all? Only if no two
overlap.

```
[[0,30],[5,10],[15,20]]  -> false     [[7,10],[2,4]]  -> true
[[1,5],[5,10]]           -> true      [[1,10],[2,3]]  -> false
```

**Constraints:** `0 ≤ intervals.length ≤ 10⁴`; `0 ≤ start < end ≤ 10⁶`. That
`start < end` is strict, and this kata is largely about why that matters.

## Approaches

| file | idea | cost | relies on |
|---|---|---|---|
| `meeting_rooms.kara` ★ | sort by start, compare each to its predecessor | O(n log n) | an ordering argument |
| `meeting_rooms_sweep.kara` | sort starts and ends separately, count concurrent | O(n log n) | a sweep invariant |
| `meeting_rooms_pairwise.kara` | test every pair against the definition | O(n²) | nothing |
| `differential.kara` | 1,200 randomized sets, all three must agree | — | — |

## The mechanism

**Touching is not overlapping.** `[1,5]` and `[5,10]` are both attendable — one
ends exactly as the next begins — so every decider has to express a strict
boundary, and each does it differently. The ★ file tests `s[i].start <
s[i-1].end`; the sweep releases finished meetings with `ends[j] <= starts[k]`,
so a meeting ending now frees its slot before the next is counted; the pairwise
file writes `max(s₁,s₂) < min(e₁,e₂)`, which states the rule once with no second
place to get it wrong.

**The ★ file compares against its predecessor, not a running maximum end.** That
is what separates it from [#56](../../1-100/56-merge-intervals/): merging needs
`max(cur_end, e)` so a nested interval cannot shrink the running end, but here a
nested interval clashes at the adjacent test and returns early, so no running
maximum is needed.

**The sweep computes more than it reports.** Its `active` counter is the number
of concurrent meetings, and its maximum is exactly the answer to
[#253](https://leetcode.com/problems/meeting-rooms-ii/) (minimum rooms). This
file just stops as soon as it reaches 2.

## What the differential found: `start < end` is load-bearing

The first version of the generator drew durations from `0..4`, producing
zero-length meetings. **The three deciders disagreed on 8.9% of 8,000 cases.**

The reduction is three intervals:

```
(2,4) (0,2) (0,0)     sorted=false   sweep=true   pairwise=true
```

`(0,2)` and `(0,0)` share a start, so sorting by start alone may place them
adjacent in either order. With `(0,2)` first, the ★ test reads
`s[1].start < s[0].end` → `0 < 2` → clash. But by the definition there is no
clash: `max(0,0) < min(2,0)` is `0 < 0`, false.

The adjacent test is a *shorthand* for overlap that is only valid when intervals
are non-degenerate. Overlap really means `s[i].start < s[i-1].end` **and**
`s[i-1].start < s[i].end`; for a zero-length `s[i]` sharing its start, the second
conjunct fails and the shorthand reports a clash that is not there. The pairwise
file, which writes the definition out, is immune — which is exactly why it is in
the kata.

**LeetCode constrains `start < end`, so this input is out of spec**, and the fix
was to the generator, not to the algorithm. It is recorded here rather than
quietly corrected because the precondition is invisible in the ★ code: nothing in
`s[i].0 < s[i - 1].1` hints that it depends on every interval being non-empty.

For the same reason the unit tests carry **no** zero-length case. An earlier
draft included `[[2,2],[2,2]]`, which all three deciders happen to agree on —
keeping a degenerate case that passes would have implied the degenerate case is
handled.

## Generator design

A uniform draw is nearly useless here: scatter intervals widely and almost every
set contains an obvious clash, so every decider returns early and the
*attendable* path — the one that must scan to the end — is barely exercised.
Cases are drawn in three families instead:

- **packed** (~half) — laid end to end with usually-zero gaps. Attendable, and
  produces touching boundaries in bulk.
- **perturbed** — a packed set with one interval nudged back by exactly one,
  overlapping its neighbour by the smallest possible margin. A decider with a
  wrong boundary flips precisely here.
- **scattered** — the uniform draw, kept so the early-return path is covered.

Every case is shuffled before use, since two deciders sort and one does not;
pre-sorted input would hide an ordering assumption.

Over 1,200 cases: **842 attendable, 358 clashing, and 716 containing a touching
boundary** — the shape the problem turns on is present in 60% of cases rather
than by luck.

## Kāra features exercised

- **`Vec[(i64, i64)]` and `sort_by(|a, b| a.0.cmp(b.0))`** — sorting tuples by a
  primary key, the [#56](../../1-100/56-merge-intervals/) idiom.
- **`Vec[i64].sort()`** — the bare comparator-free sort, a different surface.
- **Tuple field access** (`.0` / `.1`) in comparisons, `if`-expression `max`/`min`,
  and tuple assignment back into a `Vec` slot (`out[victim] = (v.0 - 1i64, v.1)`).
- **`Array[(i64, i64), N]` literals** including the empty `Array[(i64, i64), 0]`.
- **Fisher-Yates shuffle** over a `Vec` of tuples.

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`, and the two
with mirrors match Python.

No compiler bugs found. Worth stating precisely: the differential's 8.9%
disagreement was **checked against the compiler first** — the interpreter and the
AOT build reported the identical mismatch count and digest, which ruled out a
codegen fault before the algorithm was examined.

## Running

```bash
karac run meeting_rooms.kara
karac run meeting_rooms_sweep.kara
karac run meeting_rooms_pairwise.kara

diff <(karac run meeting_rooms.kara) <(python3 meeting_rooms.py) && echo OK
diff <(karac run meeting_rooms.kara) <(karac run meeting_rooms_sweep.kara) && echo OK
diff <(karac run meeting_rooms.kara) <(karac run meeting_rooms_pairwise.kara) && echo OK

# 1,200 randomized sets, three deciders cross-checked, mirrored in Python
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

# run == build, on every program
for f in meeting_rooms meeting_rooms_sweep meeting_rooms_pairwise differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```
