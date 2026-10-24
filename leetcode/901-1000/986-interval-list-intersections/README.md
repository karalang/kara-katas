# 986. Interval List Intersections

You are given two lists of closed intervals, `firstList` and
`secondList`, where `firstList[i] = [start_i, end_i]` and
`secondList[j] = [start_j, end_j]`. Each list of intervals is pairwise
disjoint and in sorted order.

Return the intersection of these two interval lists.

A closed interval `[a, b]` (with `a <= b`) denotes the set of real
numbers `x` with `a <= x <= b`. The intersection of two closed
intervals is a set of real numbers that are either empty or
represented as a closed interval.

```
firstList = [[0,2],[5,10],[13,23],[24,25]],
secondList = [[1,5],[8,12],[15,24],[25,26]]
  ->  [[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]
firstList = [[1,3],[5,9]], secondList = []  ->  []
```

**Constraints:** `0 <= firstList.length, secondList.length <= 1000`;
`firstList.length + secondList.length >= 1`;
`0 <= start_i < end_i <= 10^9`; `end_i < start_{i+1}`;
`0 <= start_j < end_j <= 10^9`; `end_j < start_{j+1}`.

## Approaches

The intervals are `(start, end)` tuples, and every arm returns the
intersections in order.

| file | mechanism |
|---|---|
| `interval_intersection.kara` ★ | two pointers: one interval from each list at a time, which meet from the later start to the earlier end when that is not empty; the one that ends first meets nothing further on, so it is the one passed over. O(n + m) |
| `interval_intersection_sweep.kara` | a sweep over the ends: every start and end becomes an event, sorted with starts before ends at the same place since the intervals are closed, and the count of intervals covering the place opens an intersection where it reaches two and closes it where it drops back. O((n + m) log(n + m)) |
| `interval_intersection_search.kara` | binary search: for each interval of the first list, `first_reaching` finds the first interval of the second that does not end before it starts, and every interval from there that starts by its end meets it. O(n log m + answer) |
| `interval_intersection_recursive.kara` | the first pair, then the rest: what the two first intervals share, if anything, then the answer with whichever ends first taken off the front, as a recursion on the two places. O(n + m) |
| `interval_intersection_merged.kara` | both lists in one: sorted together by start, keeping the furthest end reached so far; since one list's intervals never overlap, an interval starting before that end meets the other list's interval that reaches it, up to the nearer end. O((n + m) log(n + m)) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines. The first ten are LeetCode's two
examples and eight more: an empty first list; a list against itself;
two intervals meeting at one point; one long interval over three
short ones; two lists that interleave without meeting; LeetCode's
largest places, an interval ending at 10^9; and two pairs of
LeetCode's largest size, 1,000 intervals each, one of overlapping
steps and one of 1,000 short intervals inside a single long one. Then
the intersections' count, total length and checksum over random pairs:
300 of up to 6 intervals with gaps and lengths of up to 6, 3,000 of up
to 50 with up to 40, and three of 1,000 intervals with up to 499,999.
`interval_intersection.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: the points that lie in some interval of each list.
Every place is marked on a grid of half steps, so that intervals one
apart stay apart, and each run of points marked in both lists is one
closed interval of the answer. It checks 3,200 pairs: 3,000 of up to 5
intervals with gaps and lengths of up to 6 against the statement, and
200 of up to 300 intervals with up to 1,666,666, which reach toward
LeetCode's 10^9, against the other properties.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 pairs |
| P2 | the lists the other way round give the same answer |
| P3 | both lists moved along by the same random amount move the answer by it |
| P4 | the answer lies in both lists, so meeting either list gives it back, the answer first and second |
| P5 | every place tripled triples the answer |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 pairs of 74575 intervals: 23457 intersections covering
7749329384, checksum 504373393, 95000 checks over 5 arms: 0 failures`
under `karac __mir-run` (7.3 s) and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-eight edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the earlier start taken | P1 2022, P2 459, P4 1912, P6 2220 |
| M2 | ★: a meeting at one point dropped | P1 844, P6 844 |
| M3 | ★: the later end passed over | P1 1469, P6 1665 |
| M4 | sweep: an intersection opens at one | P1 1842, P4 1052, P6 2040 |
| M5 | sweep: the second list's intervals one longer | P1 1839, P2 2396, P4 2390, P5 2034, P6 2034 |
| M6 | sweep: the close counted before the check | P1 1988, P6 2186 |
| M7 | search: an interval ending at the start skipped | P1 491, P2 844, P4 532, P6 491 |
| M8 | search: a meeting at the end dropped | P1 532, P2 844, P4 491, P6 532 |
| M9 | search: only the first meeting kept | P1 616, P2 1052, P4 641, P6 803 |
| M10 | recursive: the first list's last interval never tried | P1 1165, P2 1760, P4 1785, P6 1240 |
| M11 | recursive: the earlier start taken | P1 1842, P4 803, P6 2040 |
| M12 | recursive: the later end taken | P1 1872, P4 987, P6 2070 |
| M13 | merged: the reach is the last end, not the furthest | P1 153, P6 334 |
| M14 | merged: an intersection runs to the far end | P1 1872, P4 1052, P6 2070 |
| M15 | merged: the reach starts at 0 | P1 805, P3 805, P4 805, P6 805 |

P1 and P6 kill all fifteen, P4 eleven, P2 six, and P3 and P5 one each.
Moving and tripling every place keep the order of every start and end,
which is all that thirteen of the mutants compare, so those two
properties see only a mutant that uses a fixed number: M15's reach
starting at 0 meets an interval starting at 0 that moving takes away,
and M5's intervals one longer do not grow by three when tripled. P2
sees only the mutants that treat the two lists differently. M2, M3, M6
and M13 pass P4 as well: met with a list of disjoint intervals that it
lies inside, each gives the answer back unchanged.

Thirteen other edits were tried and set aside. Five failed exactly the
same checks as a kept one: sweep never sorting the events, as M6;
recursive passing over the later end, as M3; recursive dropping a
meeting at one point, as M2; merged missing a start at the reach, as
M2; and merged leaving the second list out, as M6. Six were sound but
beyond three an arm: ★ taking the later end; sweep closing an
intersection one place early; search starting the walk one too far;
search keeping the wrong half; recursive never trying the second
list's last interval; recursive testing a meeting from the earlier
start. Two survived and are equivalent: ★ passing over the first list
on a tie, and recursive passing over both on a tie. When two intervals
end at the same place, the next interval of each list starts after it,
so either can be passed over, or both.

## Verification

Every arm prints the same output as `interval_intersection.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `395f71ae05`, the runtime
archives rebuilt at `d867340a02`, whose runtime sources are the same.
Under `karac __mir-run` the arms take 0.8 s (★) to 1.1 s (sweep), and
the differential 7.3 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. The program makes 21
random lists of LeetCode's largest size, 1,000 intervals with gaps and
lengths of up to 499,999, once. In each of 1,000 rounds it runs the arm
on the 20 pairs of neighbouring lists, each round starting from a
different pair, and folds each answer's size and middle intersection
into a checksum. Every implementation prints `1000 rounds over 20 pairs
of 1000 intervals: 19761000 intersections, checksum 156843050`. Each
call borrows the two lists and builds a fresh list for its answer.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `395f71ae05`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.270 to 0.325 s | 0.288 s |
| Rust (`rustc -O`) | 0.273 to 0.311 s | 0.275 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.270 to 0.310 s | 0.284 s |
| Go | 0.595 to 0.648 s | 0.615 s |
| Python | 9.5 s | |
| Kāra (`karac build --mir`) | 0.325 to 0.358 s | 0.340 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 28 times
Kāra's.

v2 took 1.20 times Rust's median time under overflow checks and 1.18
times C's. Under valgrind's cachegrind v2 ran 1,487 million
instructions and 304 million branches with 34.4 million mispredicted,
Rust with overflow checks 1,398 million, 146 million and 16.1 million,
and C 1,285 million, 105 million and 16.2 million. The step that passes
over one list or the other is close to a coin toss on random lists,
and C and Rust mispredict about once in every two or three of the
loop's 40 million steps; v2 runs twice their conditional branches and
mispredicts twice as often, which fits its branching on a second of
the loop's random tests where they select without a branch (inferred,
not traced).
