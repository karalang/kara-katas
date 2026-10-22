# 846. Hand of Straights

Alice has some cards, `hand[i]` being the value written on card `i`. She
wants to rearrange them into groups of `groupSize` cards each, every
group made of `groupSize` consecutive values. Given `hand` and
`groupSize`, return whether she can.

```
hand = [1,2,3,6,2,3,4,7,8], groupSize = 3  ->  true   ([1,2,3], [2,3,4], [6,7,8])
hand = [1,2,3,4,5], groupSize = 4          ->  false
```

**Constraints:** `1 <= hand.length <= 10^4`, `0 <= hand[i] <= 10^9`, `1
<= groupSize <= hand.length`. (LeetCode 1296 is the same problem.)

## Approaches

| file | mechanism |
|---|---|
| `is_n_straight_hand.kara` ★ | a `SortedMap` of counts, a whole run of groups at a time: the smallest card left must start a group, and if it appears `c` times, `c` groups start there, so each of the next `groupSize - 1` values must appear at least `c` times; take the smallest key and its count, subtract that count from the `groupSize` keys from it up, and fail if one has too few. O(n log n) |
| `is_n_straight_hand_sorted.kara` | sort the hand and count in a `Map`: walking the sorted cards, a card whose count is still positive is the smallest left and starts a group, taking one of it and one of each of the next `groupSize - 1` values. O(n log n) for the sort |
| `is_n_straight_hand_opened.kara` | sorted runs and a queue of open groups: walking the sorted hand's distinct values with their counts, `open` is how many groups still need the next value, so a value must be one more than the last and appear at least `open` times; its surplus starts new groups, which wait in a `VecDeque` until `groupSize` values later, when they are full. O(n log n) for the sort, then O(n) |
| `is_n_straight_hand_walkdown.kara` | walk down to a group's start, with no sort: from any card left, step down while the value below is still in the hand; the value reached starts groups, so deal all of them, step up one, and repeat until the card itself is gone. The walk passes only values still in the hand and uses each up on the way back, so O(n) expected with a hash `Map` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 27 lines: LeetCode's two examples; 17 more
(one card, repeats in groups of one, one group out of order, a gap, two
interleaved groups in groups of three and of two, a hand of six in
pairs, a value too few, two groups meeting at a shared value, a length
that is not a multiple, values two apart, overlapping groups, the values
0 and 10^9, the top three values, two groups of four, and a hand whose
counts pass every value but one); seven hands of LeetCode's most cards,
10^4: the values 0 to 9,999 shuffled, in one group of 10^4, in groups of
16, and in groups of 3, which do not divide 10^4; 2,500 overlapping
groups of four near 10^9, and the same with one card moved up by one;
and 10^4 sevens in groups of one and of two; and 600 random hands, with
how many split and a checksum. `is_n_straight_hand.py` mirrors the ★ arm
(a dict and its sorted keys, as Python has no sorted map) and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: some group holds the first card not yet dealt, so every
choice of `groupSize - 1` other undealt cards to go with it is tried,
the choices whose values are consecutive are kept, and the rest is dealt
the same way. Its 1,600 cases of up to 12 cards come in four kinds of
400: a whole number of groups' worth of values from 0 to 5; hands dealt
from groups and then left alone, or with one card changed, or with a run
of `groupSize` values taken out, which leaves counts that can pass every
value but one; values from 0 to 2, so many repeats; and up to 12 cards
of values from 0 to 7, any number of them, with groups of up to six. 665
of them split.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the hand shuffled gives the same answer |
| P3 | the same number, up to 999, added to every card gives the same answer |
| P4 | every card `x` turned to `10^9 - x` gives the same answer: the groups mirror |
| P5 | the hand and a copy of it 100 higher give the same answer: no group can reach across the gap |

It prints `1600 cases, 665 that split, 32000 checks over 4 arms: 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a group one long | P1 649 |
| M2 | ★: one card taken from each value, not one per group | P1 40, P4 41, P5 1 |
| M3 | ★: a repeated card counted once | P1 222, P5 5 |
| M4 | sorted: the hand not sorted | P1 148, P2 108, P4 132 |
| M5 | sorted: a used card starting a group | P1 269 |
| M6 | sorted: a group one long | P1 649 |
| M7 | opened: a gap allowed | P1 99, P5 60 |
| M8 | opened: a value too short for the open groups | P1 24, P4 10, P5 15 |
| M9 | opened: groups staying open a value too long | P1 649 |
| M10 | walkdown: walking down only through repeated values | P1 88, P2 113, P4 167 |
| M11 | walkdown: the card's own groups never dealt | P1 189, P4 82, P5 31 |
| M12 | walkdown: one group per start | P1 34, P2 44, P4 76 |

P1 kills all twelve. A group one long, in either arm, and groups left
open a value too long (M1, M6, M9) each fail 649 cases, at P1 alone. P2
sees the edits that depend on the order the cards come in: M4 walks them
unsorted, and the walk-down arm starts from each card in turn (M10,
M12). P4 sees the edits whose mistake depends on which end of the hand
is low, which mirroring swaps, and P5 those that the second copy, out of
reach across the gap, catches reaching too far or ending too early (M7's
gap most of all).

P3 kills nothing, and cannot here: every arm, and every edit, compares
cards only by their differences, which adding the same number to every
card keeps.

Two first drafts of the edits were replaced. The ★ arm's check loosened
to `have < 1` survived, and is equivalent: a value too few for its
groups goes below zero, nothing afterwards raises it, and once it is the
smallest key its own count fails that check. And a group one short
there, for groups of one, takes no card at all and never ends.

## Verification

Every arm prints the same output as `is_n_straight_hand.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its lines under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `0cf32f3e6f`, and the runtime archives are
current with them. Under `karac __mir-run` the ★ arm takes 1.8 s, the
other three 0.2 to 0.5 s, and the differential 3.9 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends run the open-groups arm right: `karac run
--interp`, `karac run`, `karac build` and a `KARAC_AUTO_PAR=1` build all
print the same output. They refuse the other three arms and the
differential at `*card`, a card read through `hand.iter()`: legacy types
the loop variable as an `i64`, not a reference, though `karac check`
accepts it on v2. Legacy refuses the bench program as moving a hand out
of an index, which v2's borrowing parameters do not do. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The ★ arm keeps its counts in a `SortedMap`, which C does not have, so
the bench program uses the open-groups arm, the same algorithm in all
five languages. It draws 64 hands once, each of LeetCode's most cards,
10^4: hand `g` deals groups of size 1, 2, 4, 5, 10, 16, 100 or 1,000 (by
`g % 8`) whose starts lie in a window near 10^9, so they overlap, and
shuffles them; every fourth hand then has one card moved up by one, and
those do not split. Each of 3,000 rounds sorts a copy of the next hand
and walks it. Every implementation prints `3000 rounds of 64 hands: 2250
split, checksum 78890369`, the Kāra program under `karac __mir-run`
included, in 42 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 2.81 to 3.27 s |
| Rust (`rustc -O`) | 0.60 to 0.80 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.61 to 0.79 s |
| Go | 2.00 to 2.27 s |
| Python | 6.0 to 6.3 s |
| Kāra (`karac build --mir`) | 0.60 to 0.75 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 0.69 s, against Rust's
0.62 (0.68 under overflow checks), C's 2.88 and Go's 2.17: 1.01 times
Rust's time under overflow checks, a quarter of C's and a third of Go's.
The sort is most of the work, and the languages sort differently: C
calls the library's `qsort`, which reaches its comparison through a
function pointer for every pair it compares, and Go's `slices.Sort` is
generic, where Rust's `sort` and Kāra's are compiled for `i64`. Under
valgrind's cachegrind C runs 12.3 billion instructions and 2.78 billion
branches, 405 million of them indirect, the comparison calls; Rust 6.31
billion and 1.03 billion, and v2 6.92 billion and 978 million. C
mispredicts 227 million branches, Rust 40 million and v2 24 million.
Most likely the indirect comparison and its mispredicts are what put C
behind (not traced). Built for `x86-64-v3`, the target `karac build`
uses, C takes 2.83 to 2.96 s and Rust with overflow checks 0.60 to 0.67
s, against v2's 0.58 to 0.67 s in the same five interleaved runs.
Python, whose `sorted` is native code, takes 6.2 s, about 2.1 times C's
time. The comparison with C and Rust waits until after M4.
