# 1040. Moving Stones Until Consecutive II

There are some stones in different positions on the X-axis. You are
given an integer array `stones`, the positions of the stones.

Call a stone an **endpoint stone** if it has the smallest or largest
position. In one move, you pick up an endpoint stone and move it to an
unoccupied position so that it is no longer an endpoint stone.

In particular, if the stones are at say, `stones = [1,2,5]`, you cannot
move the endpoint stone at position `5`, since moving it to any position
(such as `0`, or `3`) will still keep that stone as an endpoint stone.

The game ends when you cannot make any more moves (i.e., the stones are
in consecutive positions).

Return an integer array `answer` of length `2` where `answer[0]` is the
minimum number of moves you can play, and `answer[1]` is the maximum
number of moves you can play.

```
stones = [7,4,9]                ->  [1,2]
stones = [6,5,4,3,10]           ->  [2,3]
stones = [100,101,104,102,103]  ->  [0,0]
```

**Constraints:** `3 <= stones.length <= 10^4`;
`1 <= stones[i] <= 10^9`; all the values of `stones` are unique.

## Approaches

Every arm rests on two facts about the sorted stones `s[0] < .. <
s[n - 1]`. The most moves: the first move gives up the empty slots at
one end (the stone at `s[0]` jumps past `s[1]`, or the one at `s[n -
1]` past `s[n - 2]`), and from then on each move can fill exactly one
empty slot, so the answer is the empty slots in the larger of `s[1]..s[n
- 1]` and `s[0]..s[n - 2]`. The fewest: the stones end in some window
of `n` slots and each stone outside it moves once, so the answer is `n`
less the most stones any such window holds. The one exception is `n -
1` stones already consecutive with the last one apart, which takes two
moves, not one: the stone cannot land at the window's open end without
staying an endpoint.

| file | mechanism |
|---|---|
| `moving_stones.kara` ★ | sorted, then a sliding window: the window's near end follows its far end along the sorted stones. O(n log n) for the sort, O(n) after |
| `moving_stones_bsearch.kara` | a binary search from each stone: `count_upto` finds how many stones lie in the `n` slots starting at `s[i]`. O(n log n) |
| `moving_stones_set.kara` | the stones in a `SortedSet`: each window counted with `range_inclusive(..).count()`, the ends and their neighbours read off the set. O(n k) for `k` the most stones in a window |
| `moving_stones_iter.kara` | the windows as iterators: `filter`, `count` and `max` over the sorted stones for each window, `min` over the windows. O(n^2) |
| `moving_stones_gaps.kara` | counted in gaps: the empty slots between neighbours, with running sums (prefix sums) driving the window's far end. O(n log n) for the sort, O(n) after |
| `differential.kara` | the five arms against the game played out move by move, five properties |

Every arm prints the same 22 lines: the answers for eight sets of
stones, LeetCode's three examples among them, with two stones 10^9
apart and a set given in descending order; for every set of 3 to 12
stones from 1 to 12, by size, a total of `least + most` and a checksum;
the same for 300 random sets spread from 1 to 10^9 and 300 packed into
a stretch twice their number; and two of 2000 stones, one spread
(`[1998, 998646502]`) and the values 1 to 1999 with 3000 (`[2, 1000]`,
the exception at its largest). `moving_stones.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the game played
out: from the stones as a bit mask, it tries every legal move, the
lowest stone to an empty slot strictly between the second stone and the
highest, or the highest to one strictly between the lowest and the
second highest, and keeps the fewest and the most moves to a
consecutive set, with every position's answer kept in a memo. It checks
4617 sets: every set of 3 or more stones from 1 to 12 (4017), 400
random sets of 3 to 10 stones from 1 to 14, and 200 sets of 3 to 60
stones, 100 spread from 1 to 10^9 and 100 packed into a stretch twice
their number. The 4417 sets within 1 to 14 are played out.

| | property |
|---|---|
| P1 | the game played out, on the sets within 1 to 14 |
| P2 | shifting every stone by the same amount, staying within 1 to 10^9, changes nothing |
| P3 | the mirror image, `lo + hi - x` for each stone `x`, changes nothing |
| P4 | shuffling the stones changes nothing |
| P5 | `0 <= least <= most <= empty`, for `empty` the empty slots between the ends, and `least` is 0 exactly when nothing is empty |
| P6 | each arm agrees with at least two of the other four |

The differential prints `4617 sets (4417 played out): checksum
591795645, 137510 checks over 5 arms: 0 failures` under `karac
__mir-run` (24 s), `karac __mir-llvm-run` and `karac __mir-llvm-asan`
with no error, and the same line under `karac run` and from a `karac
build` binary. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with a 120 s limit.
Fifteen are kept, three to each arm. All fifteen are killed, each fails
the same way under both backends, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the exception taken as one move | P1 265, P6 266 |
| M2 | ★: the first stone never given up for the most | P1 4417, P5 4617, P6 4617 |
| M3 | ★: the smaller end kept for the most | P1 2928, P5 361, P6 3098 |
| M4 | bsearch: stones equal to the bound not counted | P1 2001, P5 398, P6 2039 |
| M5 | bsearch: the window's count one short | `index out of bounds` |
| M6 | bsearch: the last stone never counted | P1 952, P3 1800, P5 107, P6 960 |
| M7 | set: the exception's span one slot long | P1 1059, P5 164, P6 1062 |
| M8 | set: one move too many outside the exception | P1 4152, P5 682, P6 4351 |
| M9 | set: no window from the first stone | P1 943, P3 1800, P5 104, P6 956 |
| M10 | iter: the worst window kept | P1 4265, P5 2791, P6 4365 |
| M11 | iter: a window of `n + 1` slots | P1 1624, P3 252, P5 221, P6 1662 |
| M12 | iter: the last stone's jump one short | P1 1470, P3 3098, P5 88, P6 1541 |
| M13 | gaps: a window of `n + 1` slots | P1 1831, P5 221, P6 1869 |
| M14 | gaps: every `n - 1` stones taken as packed | P1 889, P5 259, P6 891 |
| M15 | gaps: always the first gap given up | P1 1470, P3 3098, P5 180, P6 1541 |

Of the fourteen that run to the end, P1 and P6 kill all fourteen, P5
thirteen and P3 five. P5 misses only M1, whose wrong answer of one
move still lies within the bounds. P3 sees the edits that treat the two
ends differently (M6, M9, M11, M12, M15), since the mirror swaps them.
P2 and P4 kill none of the thirty: every arm sorts its stones first and
works only on the differences between them, so no edit to what follows
the sort can see a shift or an order. One more edit shows P4 working:
the ★ arm's sort left out fails `P1 385, P3 4614, P4 4410, P5 440, P6
585` under `karac __mir-llvm-run`, with P1 low because the sets
enumerated from 1 to 12 are built in order. M5 prints its first ten
failures and then indexes before the start of the sorted stones, on a
window whose count it makes 0.

Fifteen other edits were set aside. Two are equivalent. The ★ arm's
fewest started at `n - 1` rather than `n` changes nothing, since every
window holds at least the stone it starts from. The gaps arm's guard
against its far end falling behind its near end never fired: stone `i`
alone spans one slot, so the loop always reaches it. The guard was
dropped from both copies of the arm. The other thirteen were killed
too, beyond three per arm. Three fail as M1 does: the bsearch arm
reading the window's last stone one high, and the iter arm taking the
exception as one move or reading the window's last stone as its first.
Two fail as M13 does: the ★ and bsearch arms with a window of `n + 1`
slots. One each fails as M2 (the set arm reading the second stone as
the first), M14 (the ★ arm's exception without its consecutive test),
M3 (the gaps arm giving up the larger end gap), M4 (the set arm's
window half-open), M9 (the bsearch arm with no window from the first
stone), M15 (the set arm measuring the last stone's jump from the
second) and M8 (the iter arm not counting the window's first stone).
The last, the gaps arm's running sums each a gap ahead, indexes past
the end of its gaps.

## Verification

Every arm prints the same output as `moving_stones.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with
no error. `karac run` and a `karac build` binary print the same output
for every arm and the differential. `karac check --output=json` reported
nothing on any file. The release build is kara `8876b6f720` (built
before a rebase beneath it that touched only the parser and
typechecker), with runtime archives built after the last runtime change
before it. Under `karac __mir-run` the arms take 0.56 s (★), 0.78 s
(bsearch) and 1.1 s (gaps) to 13.6 s (set) and 102 s (iter, which walks
every stone for each of 2000 windows in the two largest sets, over the
corpus's 60 s cap). Compiled, the harnesses run in about 10 ms (★,
bsearch, gaps), 35 ms (set) and 50 ms (iter), three runs each. No
correctness gap turned up; the iterator arm's interpreter time is kara
B-2026-11-03-9: an adaptor chain with a closure runs about 11 times the
hand loop's time there.

## Benchmarks

The bench builds 400 sets of 10000 stones (the problem's most) once in
all five languages, half spread with gaps of 1 to 100000 and half
packed with gaps of 1 to 3, each shuffled so the sort has work. Then it
solves every set 5 times with the ★ arm, which copies and sorts its
input before sliding the window, adding `least + most` to a total and
folding both into a checksum. The sort is each language's own: `sort`
in Kāra and Rust (both stable), `slices.Sort` in Go, `sorted` in
Python, and `qsort` with a comparison function in C. Every
implementation prints `400 sets of 10000 stones, 5 rounds: total
499984007365, checksum 338516767`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.389 to 0.454 s | 0.428 s |
| Kāra (`karac build`) | 0.398 to 0.473 s | 0.424 s |
| Rust (`rustc -O`) | 0.523 to 0.699 s | 0.591 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.551 to 0.687 s | 0.631 s |
| Go | 1.484 to 1.717 s | 1.582 s |
| C (`clang -O3`) | 2.017 to 2.220 s | 2.059 s |
| Python | 13.5 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(0.40 s real, 0.38 s user on one run) and runs as fast as the
sequential one.

Kāra took 0.68 times Rust's median time under overflow checks. The
window is O(n) after an O(n log n) sort, so the sort is most of the
work, and the order of the table is mostly the order of the sorts: C's
`qsort` calls its comparison through a pointer for every pair and comes
last (inferred from the sources, not profiled).
