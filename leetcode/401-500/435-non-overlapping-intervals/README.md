# 435. Non-overlapping Intervals

Given an array of intervals where `intervals[i] = [start_i, end_i]`,
return the minimum number of intervals you need to remove to make the
rest of the intervals non-overlapping. Intervals that only touch at a
point, such as `[1, 2]` and `[2, 3]`, are non-overlapping.

```
intervals = [[1,2],[2,3],[3,4],[1,3]]   ->  1    remove [1,3]
intervals = [[1,2],[1,2],[1,2]]         ->  2
intervals = [[1,2],[2,3]]               ->  0
```

**Constraints:** `1 <= intervals.length <= 10^5`;
`-5 * 10^4 <= start_i < end_i <= 5 * 10^4`.

## Approaches

Removing as few intervals as possible is keeping as many as possible
side by side, each ending at or before the next one starts. Every arm
takes the intervals as an owned `Vec[(i64, i64)]` and sorts it in
place.

| file | mechanism |
|---|---|
| `erase_overlap.kara` ★ | greedy by end: sort by end and keep each interval that starts at or after the end of the last one kept. The interval that ends first is always safe to keep, since any side-by-side set can swap its first interval for it. O(n log n) |
| `erase_overlap_start.kara` | greedy by start: sort by start and, when an interval starts before the end of the last one kept, remove whichever of the two ends later. O(n log n) |
| `erase_overlap_dp.kara` | the longest chain, sorted by start: the longest chain ending with interval i is one more than the longest ending with an earlier interval that ends by i's start. O(n^2) |
| `erase_overlap_search.kara` | the longest chain, sorted by end: best[i + 1] = max(best[i], 1 + best[k]), where k, the number of intervals before i that end by its start, comes from a binary search over the ends. The recurrence of weighted interval scheduling with unit weights. O(n log n) |
| `differential.kara` | the four arms on 1,500 random sets, five properties |

Every arm prints the same 10 lines: the three LeetCode examples, six
edge cases (one interval spanning the whole range, one long interval
over three short ones, a chain of intervals touching end to start,
intervals at both ends of the range, five that each overlap the next,
and an unsorted set where both greedy orders matter), and for 300
random sets of up to 40 intervals the total removed and a checksum of
the answers. `erase_overlap.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random sets of 0 to 40 intervals, each 1 to 3, 10 or 30 long,
starting in [-50, 50).

| | property |
|---|---|
| P1 | the answer is the reference's, a walk over the coordinates that never sorts: the most side-by-side intervals ending by x is the larger of the most ending by x - 1 and one more than the most ending by the start of an interval that ends at x |
| P2 | shuffling the intervals, shifting them all towards an end of the range, or mirroring them (`[a, b]` to `[-b, -a]`) changes nothing |
| P3 | at least depth - 1 intervals go, where depth is the most intervals over one point; at most n - 1; and none exactly when no two overlap |
| P4 | one more interval removes the same number or one more, and a second copy of every interval removes n more |
| P5 | k side-by-side unit intervals under m intervals that span them all lose the m, k intervals touching end to start lose none, m + 1 copies of one interval at the edge of the range lose m, and no intervals lose none |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | by end: an interval that starts where the last one ends overlaps it | P1 831, P3 28, P5 1432 |
| M2 | by end: sorted by start instead | P1 675, P2 635, P4 244, P5 1296 |
| M3 | by start: an overlap always keeps the later interval | P1 978, P2 585, P4 250, P5 1357 |
| M4 | by start: touching intervals overlap | P1 831, P3 28, P5 1432 |
| M5 | chain: a link must end before the next starts, not by its start | P1 831, P3 28, P5 1432 |
| M6 | chain: no chain grows from the first interval | P1 821, P2 549, P3 128, P4 821, P5 1432 |
| M7 | binary search: the prefix ends before the start, not by it | P1 831, P3 28, P5 1432 |
| M8 | binary search: every interval ends a chain | P1 650, P2 654, P4 372, P5 1357 |

M1, M4, M5 and M7 are the same mistake in each arm, treating touching
intervals as overlapping, and fail identically: they are still exact
for the problem with closed intervals, so shuffling, shifting,
mirroring and adding intervals all agree with them, and only P1, P3's
"none exactly when no two overlap" and P5's touching chain see it. The
touching chain was added to P5 for them; without it P5 missed all
four. P3's bounds hold for any answer between the true one and n - 1,
so it misses the mutants that remove too many only where something
overlaps (M2, M3, M8); M6 also removes one where nothing does.

## Verification

All four arms print the same output as `erase_overlap.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`,
and all four frozen legacy backends: `karac run --interp`, LLJIT,
`karac build` and `KARAC_AUTO_PAR=1 karac build`. `karac check` passes
on every file. The differential prints `30000 checks, 0 failures`
under `karac __mir-run`, `karac __mir-llvm-run` and
`karac run --interp`. The four arms and the differential also run
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

The legacy code generator does not compile the differential: it
refuses `[3, 10, 30][next_random(seed) % 3]`, an index into an array
literal ("Index operator applied to non-array type"). Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds a pool of 1,000,000 random
intervals once, starting anywhere in [-50000, 50000) and 1 to 200
long, then solves 100 windows of 100,000 consecutive intervals from it
(the problem's limit), each copied into a fresh vector that the arm
sorts in place. Every implementation prints `100 rounds of 100000
intervals: 9435562 removed, checksum 227161123`; a 3-round cut of the
Kāra program under `karac __mir-run` prints the same as the C program
cut the same way.

The time is the sort. Kāra's `sort_by_key` and Rust's are stable
sorts, as is Python's; C uses `qsort` and Go `slices.SortFunc`, which
are not, since the count does not depend on the order of intervals
with equal ends. C's `qsort` calls its comparison through a pointer,
which is most of why it trails. Spot timings on a shared 4-core
container, three runs each (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| Rust (`rustc -O -C overflow-checks=on`) | 0.39 to 0.41 s |
| Rust (`rustc -O`) | 0.44 to 0.51 s |
| Kāra (legacy `karac build`) | 1.22 to 1.31 s |
| Go | 1.81 to 1.85 s |
| C (`clang -O3`) | 1.96 to 2.13 s |
| Python | 4.4 to 4.7 s |

The two Rust builds are within noise of each other. The Kāra program
prints the same line under `karac __mir-llvm-run` in 8.7 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

## Compiler findings

No new findings.
