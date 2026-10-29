# 1024. Video Stitching

A sporting event lasting `time` seconds was recorded as a list of video
clips, which may overlap and vary in length. Clip `clips[i] = [start,
end]` runs from `start` to `end`, and a clip can be cut into segments
freely: `[0, 7]` can become `[0, 1] + [1, 3] + [3, 7]`. Return the
fewest clips that can be cut into segments covering the whole event
`[0, time]`, or `-1` if no choice of clips can.

```
clips = [[0,2],[4,6],[8,10],[1,9],[1,5],[5,9]], time = 10  ->  3   ([0,2], [1,9], [8,10])
clips = [[0,1],[1,2]], time = 5                            -> -1
clips = [[0,1],[6,8],[0,2],[5,6],[0,4],[0,3],[6,7],[1,3],[4,7],[1,4],[2,5],[2,6],[3,4],[4,5],[5,7],[6,9]], time = 9  ->  3
```

**Constraints:** `1 <= clips.length <= 100`, `0 <= start <= end <= 100`,
`1 <= time <= 100`.

## Approaches

Every second `[t, t + 1]` of the event has to lie inside some clip
taken, so a set of clips works exactly when it leaves no such second
uncovered.

| file | mechanism |
|---|---|
| `video_stitching.kara` ★ | a greedy jump: note for each start the furthest end of a clip starting there, then walk the seconds keeping how far the clips taken reach and how far one more clip could reach from any second already covered; at the end of what is covered, take the clip that reaches furthest, and if nothing reaches past a second, there is a gap. O(n + time) |
| `video_stitching_sort.kara` | sorted clips: sort by start with `sort_by_key`; while the video is covered up to `end`, read on through the clips starting no later than `end` and take the one that reaches furthest, or answer -1 if none reaches past `end`. O(n log n) |
| `video_stitching_dp.kara` | the fewest clips to each second: `fewest[t]` is one more than the least `fewest[s]` over the clips `[s, e]` with `s < t <= e`, with `i64.MAX` for a second no clips reach. O(time * n) |
| `video_stitching_bfs.kara` | shortest path: "covered up to `x`" is a place and a clip with `start <= x < end` a step from `x` to `end`, cut to `time`; breadth first from 0 over a `VecDeque` finds the fewest steps to `time`. O(time * n) |
| `video_stitching_memo.kara` | recursion with a memo: the fewest clips covering `[x, time]` is none once `x` reaches `time`, otherwise one clip containing `x` and running past it plus the fewest from its end, the best over all such clips, each `x` solved once and kept in a `Map`. O(time * n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: the answers for eight cases,
LeetCode's three examples among them; and for six groups of random cases
(4 to 100 clips, a video of up to 10 to 100 seconds, each clip starting
anywhere in the video and up to 6 to 100 seconds long, cut at 100),
how many clips the cases that can be covered take, how many cannot be
covered, and a checksum of the answers. `video_stitching.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: of every set of the clips, the fewest clips in one that
covers each second `[t, t + 1]` of the event, and -1 when not even all of
them together do. It checks 4,629 cases: every non-empty set of the ten
distinct clips within the seconds 0 to 3 for a video of 1 to 3 seconds
(3,069), then 1,500 random cases with a video of up to 20 seconds and
60 with one of up to 100. Three random cases in four start from a chain
of clips from 0 to the end, each overlapping the last by up to 2
seconds, and every random case then gets up to 5 clips anywhere (up to
80 for the long videos), each put in at a random place. The 4,578 cases
of at most 12 clips are searched in full. Each case is also asked with
its clips in the opposite order, with one more random clip, played
backwards, each clip `[s, e]` becoming `[time - e, time - s]` once cut to
the video, and with every second counted twice.

| | property |
|---|---|
| P1 | the statement read literally, on the cases of at most 12 clips |
| P2 | the order of the clips does not matter |
| P3 | one more clip never makes it worse: a video that could be covered still can, with no more clips |
| P4 | played backwards it takes as many clips |
| P5 | with every second counted twice it takes as many clips |
| P6 | each arm agrees with at least two of the other four |

The differential prints `4629 cases (4578 searched in full): checksum
235558564, 138615 checks over 5 arms: 0 failures` under `karac
__mir-run` (5.3 s) and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Thirty-one edits to the differential, each run under `karac __mir-run`
and `karac __mir-llvm-run`; fifteen are kept, three to each arm, all
fifteen are killed, each fails the same checks under both, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last clip at each start kept, not the furthest | P1 160, P2 2367, P3 664, P4 1511, P6 173 |
| M2 | ★: a gap noticed a second late | P1 532, P3 25, P4 333, P5 532, P6 532 |
| M3 | ★: a clip taken for every second | P1 2685, P5 3822, P6 2734 |
| M4 | sort: sorted by end | P1 1842, P2 1615, P3 196, P4 1923, P6 1890 |
| M5 | sort: the last clip read, not the furthest | P1 341, P2 2343, P3 672, P4 1587, P6 379 |
| M6 | sort: stopping a second short | P1 1844, P4 851, P5 1848, P6 1848 |
| M7 | dp: a clip's last second left out | P1 2323, P4 1826, P6 2340 |
| M8 | dp: the last clip read, not the fewest | P1 1594, P2 1678, P3 401, P4 1559, P6 1643 |
| M9 | dp: 0 for no answer | P1 805, P3 160, P6 807 |
| M10 | bfs: only clips starting exactly where the cover has reached | P1 666, P6 699 |
| M11 | bfs: a clip past the end not cut to it | index out of bounds panic, exit 101 |
| M12 | bfs: a stack for the queue | P1 41, P2 154, P3 9, P4 134, P6 65 |
| M13 | memo: a cover reaching exactly `time` not taken as done | P1 1784, P4 2568, P6 1789 |
| M14 | memo: the most clips, not the fewest | P1 1804, P3 268, P4 1571, P6 1853 |
| M15 | memo: a dead end taken for done | P1 193, P3 66, P4 483, P6 193 |

P1 and P6 kill the fourteen that finish, P4 eleven, P3 nine, P2 five
and P5 three; M11 is killed by its own bounds check, indexing `steps`
past the end of the video. P2 sees only the edits whose answer depends
on the order the clips come in: the three that keep the last clip read
where they should keep the best (M1, M5, M8), sort ordering by end (M4)
and bfs searching depth first (M12). P5 sees only the edits that are a
second out. With every second counted twice every clip's ends are even,
so a gap of one second becomes two, which M2 then notices; a cover
stopping a second short cannot end on an odd second, so M6 then reaches
the end; and M3's count of seconds doubles. M10, which takes only the
clips starting exactly where the cover has reached, is seen only by the
statement and the other arms. The checks draw a random number for every
case whatever the answers, so every mutant sees the same cases and
their counts can be compared.

Sixteen other edits were tried and set aside. Five change no answer.
★ leaving out the clips starting at `time`: such a clip covers no second
of the video, and the walk never reads its entry. Sort starting each
round's best reach from 0 instead of `end`: that differs only when no
clip read in a round reaches past `end`, where `end` then moves back
instead of the answer being -1, but every clip starting no later than
the old `end` has been read, so the rounds after read none and come to
-1 anyway. Sort reading every clip again each round: the clips read
before reach no further than the current `end`. Dp counting a clip that
starts at `t` for `t`: it offers `fewest[t] + 1`, never less than
`fewest[t]`. Bfs updating a place reached again by a shorter path:
breadth first reaches each place first by a shortest path. The other
eleven were killed too, beyond three per arm. Seven get every answer
that exists wrong and fail exactly the same checks: ★ taking one clip
too many, sort leaving out a clip starting where the cover ends (which
leaves every video uncovered), dp making second 0 cost a clip, dp never
filling the last second, bfs leaving the start unmarked, memo counting
a clip at the end and memo not counting the clip taken. ★ never
checking the last second and bfs stopping a second short fail as M6.
And two fail on their own: ★ reading only the clips starting at the
current second, and memo starting from 1000 where there is no answer,
which fails M9's checks but P3's, since one more clip can only lower
its stand-in.

## Verification

Every arm prints the same output as `video_stitching.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error; the differential prints its line under all three. `karac check
--output=json` reports no diagnostic for the five arms, the
differential and the bench program, so `karac fix` had nothing to do.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. The release build is kara `56c60bdf7c`, with
runtime archives rebuilt at `ce706dd131`, the last commit before it to
change the runtime. Under `karac __mir-run` the arms take
0.7 s (sort) to 3.6 s (dp). No compiler gap turned up.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench builds 2,000 random cases once in all five languages, each a
video of 50 to 100 seconds covered by a chain of clips 1 to 10 seconds
long, each overlapping the last by up to 2 seconds, with random clips up
to 20 seconds long put in at random places until there are up to 100,
115,053 clips in all. It answers every case 500 times with the ★ arm,
folding the answers into a sum and a checksum: every case can be
covered, with 7.24 clips on average. Every language uses 64-bit
integers. Rust takes the clips as `&[Vec<i64>]` and Go as a slice of
slices, both allocating the table of furthest ends per call, as Kāra
does with `Vec.filled`; C keeps each case's clips as an array of pairs
and `calloc`s the table. Every implementation prints `2000 cases, 115053
clips, 500 rounds: sum 7240000, checksum 246122836`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.280 to 0.381 s | 0.306 s |
| Rust (`rustc -O`) | 0.435 to 0.501 s | 0.460 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.463 to 0.678 s | 0.508 s |
| Go | 0.867 to 0.947 s | 0.909 s |
| Python | 11.1 s | |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.486 to 0.594 s | 0.546 s |
| Kāra (`karac build`) | 0.440 to 0.572 s | 0.516 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(its user time stays below its real time) and runs as fast as the
sequential one.

v2 took 1.08 times Rust's median time under overflow checks and 1.78
times C's. Rust's own time is 1.5 times C's; we did not measure where
either gap goes. Go's user time, 1.20 s at the median, is above its
real time, so it ran on more than one core; we did not measure what
for.
