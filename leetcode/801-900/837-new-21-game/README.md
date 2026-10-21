# 837. New 21 Game

Alice starts with 0 points and draws numbers while she has fewer than
`k` points. Each draw gains her an integer number of points chosen
uniformly at random from `[1, maxPts]`, independently of every other
draw. She stops drawing as soon as she has `k` or more points. Return
the probability that she ends with `n` or fewer points. Answers within
`10^-5` of the actual answer are accepted.

```
n = 10, k = 1, maxPts = 10  ->  1.00000
n = 6, k = 1, maxPts = 10   ->  0.60000
n = 21, k = 17, maxPts = 10 ->  0.73278
```

**Constraints:** `0 <= k <= n <= 10^4` and `1 <= maxPts <= 10^4`.

## Approaches

Every arm works with the chance of each total. Alice reaches a total
from one of the `maxPts` totals below it at which she still draws, with
chance `1 / maxPts` each, and stops at the first total of `k` or more.

| file | mechanism |
|---|---|
| `new21_game.kara` ★ | forward, with a sliding window: `p[i]`, the chance that her points are ever exactly `i`, is the sum of `p` over the last `maxPts` totals below `k` before `i`, over `maxPts`, that sum kept in a running window; the answer is the sum of `p[i]` for `i` from `k` to `n`. When `k` is 0, or even her largest possible stop `k - 1 + maxPts` is at most `n`, it returns 1 at once. O(n) |
| `new21_game_backward.kara` | backward, the chance of winning from each total: 1 at a stop of at most `n`, 0 past it, and below `k` the mean of the next `maxPts` totals' chances, filled from `k - 1` down to 0 with a sliding window. O(k + maxPts) |
| `new21_game_prefix.kara` | forward, with prefix sums: the same `p[i]` as the ★ arm, each window's sum the difference of two entries of a prefix-sum list, which also gives the answer. O(n) |
| `new21_game_push.kara` | pushing each total's chance forward: each total below `k` adds its share to the next `maxPts` totals through a difference list, and a running sum of it gives each `p[i]` in turn. O(n) |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 14 lines: LeetCode's three examples; ten more
(`k` of 0, an even chance, `maxPts` of 1, two games small enough to work
by hand, `k` and `maxPts` both at LeetCode's greatest, 10^4, with `n` at
10^4 and at 5,000 points to stop, two that always win at 10^4, and one
where the answer is a few in ten thousand); and 300 random games with
`n` up to 10^4, with the sum of their answers and the count above one
half. Every answer is printed to six places. `new21_game.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally. For games with `k` and `maxPts` at most 10, every sequence of
draws is played out, each draw one of `maxPts` equally likely numbers,
and the chances of the sequences that stop at `n` or less are added up.
For larger games, the chance of reaching each total is read straight
from the statement: the sum, over every draw `d`, of the chance of
reaching that total less `d` while still drawing, over `maxPts`, which
takes O(n maxPts). Its 1,600 cases come in four kinds of 400: small
games of any shape; small games with `n` in the band from `k` to `k -
1 + maxPts` where the answer is neither 0 nor 1; games with `n` and
`maxPts` up to 200; and games up to 200 in the band. Answers are
compared to within 10^-9.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | more room: the answer for `n + 1` is no smaller |
| P3 | the first draw: the answer is the mean, over the first draw `d`, of the answer for `n - d` and `k - d` when `d < k`, and of 1 or 0 for a stop at `d` |
| P4 | bounds: 1 when `k` is 0 or `n` is at least `k - 1 + maxPts`, otherwise between 0 and 1 |
| P5 | the gains shrink: above `k`, the answer gains no more from `n` to `n + 1` than from `n - 1` to `n` |

It prints `1600 cases, 32000 checks over 4 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a total of `k` taken as still drawing | P1 1059, P3 569, P5 77 |
| M2 | ★: the start, total 0, never dropped from the window | P1 646, P2 133, P3 646, P4 505, P5 99 |
| M3 | ★: the window starting empty | P1 1059, P2 554, P3 1059, P4 646, P5 368 |
| M4 | backward: a stop at exactly `n` counted as a loss | P1 1261, P3 427, P4 202 |
| M5 | backward: the window never dropping a total | P1 1011, P3 1011, P4 898, P5 15 |
| M6 | backward: the mean taken over `maxPts + 1` draws | P1 1478, P3 1462, P4 419 |
| M7 | prefix: totals of `k` or more taken as still drawing | P1 1259, P3 667, P4 738, P5 833 |
| M8 | prefix: the window one total short | P1 1124, P3 1033, P4 419 |
| M9 | prefix: a stop at exactly `k` left out of the answer | P1 1478, P3 747, P4 419 |
| M10 | push: each share ending one total early | P1 1124, P3 1033, P4 420 |
| M11 | push: a total of `k` taken as still drawing | P1 1310, P3 618, P4 251 |
| M12 | push: each share starting one total late | P1 1478, P3 1369, P4 419 |

P1 and P3 kill all twelve. P3 checks an arm against itself one draw
later, so an edit that is wrong in the same way at every size can pass
it where the error carries through, which is why it falls short of P1 on
most of them, on M1 and M4 by more than half. P2, more room, sees only
the ★ arm's window edits that let the answer fall as `n` grows (M2, M3).
P5 sees five, M7 most of all, which keeps adding chance past `k`. P4
sees every edit but M1: the others all miss 1 on some of the 419 cases
where the answer must be 1.

M2 was first tried as a total of exactly `k` dropped from the window
when it falls `maxPts` behind. That is an equivalent mutant: the ★ arm
returns 1 at once whenever `n` reaches `k - 1 + maxPts`, so its loop
never gets as far as `k + maxPts`, the only total at which that edit
acts, and it survived every case.

## Verification

Every arm prints the same output as `new21_game.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `d4ba0a00ad`, and the runtime archives are
current with them. Under `karac __mir-run` each arm takes 0.6 to 2.0 s
and the differential 12 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends print the same output for all four arms under
`karac run --interp`, `karac run`, `karac build` and an auto-parallel
build, and run the bench program. The differential prints its line under
the legacy interpreter, but built by legacy `karac build` it reports 805
failures for each arm, all of them P1: the arms agree with each other
and the statement does not. 805 is about the number of small games,
which the statement plays out with a recursive `play` that adds to a
`mut ref f64`, so most likely the legacy compiled backend loses those
additions (not traced). Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
games once, each with `n` from 5,000 to 10^4, `k` from `n / 2` to `n`,
and `maxPts` large enough that Alice can go past `n`, so that no game
takes the early return. Each of 25,000 rounds plays the next game. Every
implementation prints `25000 rounds of 64 games: sum 13787.631764`, the
Kāra program under `karac __mir-run` included, in 107 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.96 to 0.98 s |
| Rust (`rustc -O`) | 0.95 to 1.00 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.95 to 1.42 s |
| Go | 1.20 to 1.40 s |
| Python | 14.0 to 14.7 s |
| Kāra (`karac build --mir`) | 1.23 to 1.32 s |
| Kāra legacy (`karac build`) | 0.96 to 0.99 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 1.26 s, against C's
0.97, Rust's 0.98 (0.96 under overflow checks), Go's 1.22 and the frozen
legacy backend's 0.98: 1.3 times C's time and legacy's. The three
compiled programs measured under valgrind's cachegrind do about the same
work, C 5.2 billion instructions and 2.2 billion branches, Rust 4.8 and
2.1 billion and v2 5.4 and 2.6 billion, none of them mispredicting. The
loop is a chain of dependent floating-point operations, each total's
chance a division of the window and then added back into it, so its time
is the chain's latency more than its instruction count; most likely v2
puts one more step on that chain than C does (not traced). Built for
`x86-64-v3`, the target `karac build` uses, C takes 0.96 to 0.98 s and
Rust with overflow checks 0.96 to 0.98 s, against v2's 1.23 to 1.32 s in
the same five interleaved runs. Python takes 14 s, about 15 times C's
time. The comparison with C and Rust waits until after M4.

## Compiler findings

None on v2: every arm, the differential and the bench program pass
`karac check` and run on both v2 backends as written, and the six-place
`f64` output matches Python's to the last digit.
