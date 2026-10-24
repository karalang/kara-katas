# 991. Broken Calculator

There is a broken calculator that has the integer `startValue` on its
display initially. In one operation, you can:

- multiply the number on display by `2`, or
- subtract `1` from the number on display.

Given two integers `startValue` and `target`, return *the minimum
number of operations needed to display* `target` *on the calculator*.

```
startValue = 2, target = 3   ->  2    (double, then decrement)
startValue = 5, target = 8   ->  2    (decrement, then double)
startValue = 3, target = 10  ->  3    (double, decrement, double)
```

**Constraints:** `1 <= startValue, target <= 10^9`.

## Approaches

Forwards there are two choices at every press and no obvious end, but
backwards the keys become "add 1" and "halve an even number", and the
greedy choice is forced: above the start, an even value is halved and
an odd one made even. Two arms run that greedy, two work out the
answer from the binary digits of the overshoot, and one plans the
presses forwards and carries them out.

| file | mechanism |
|---|---|
| `broken_calc.kara` ★ | greedy from the target back: while the target is above the start, halve it when it is even and add 1 when it is odd, counting each step; then add 1 up to the start. O(log target) |
| `broken_calc_recursive.kara` | the same greedy as a recursion: the presses to t are start - t when t is not above the start, and otherwise one more than for t / 2 or t + 1. O(log target), as deep |
| `broken_calc_doublings.kara` | forwards, by the number of doublings: with d doublings the overshoot D = start · 2^d - target is paid with D / 2^d decrements before any doubling and one for each binary 1 of D mod 2^d; the answer is the cheapest d from 0 to 32. O(log² target) |
| `broken_calc_closed.kara` | in closed form: the greedy halves h times, rounding up, and lands on c = ceil(target / 2^h); the answer is h, plus the binary 1s of c · 2^h - target, the roundings, plus start - c. O(log target) |
| `broken_calc_replay.kara` | the presses carried out forwards: with the fewest doublings that reach the target, the overshoot's bits are read as a plan of decrements around the doublings; the arm runs the plan on a value, counts the presses, and stops with an error unless the value ends on the target. O(log target) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 16 lines. The first twelve are LeetCode's
three examples and nine more: a start already on the target; a target
below the start, where the answer is the gap; LeetCode's extremes, 1
to 10^9 and back, and 10^9 to itself; 7 to 10^9; 999,999,999 to 10^9,
where halving down to 500,000,000 and climbing back costs 500,000,000
presses; a target that is the start times a power of 2; and
536,870,913, one more than 2^29, from 1. Then totals over random
pairs: 300 up to 20, 3,000 up to 1,000, 3,000 up to 10^9, and 300 with
the start up to 1,000 and the target up to 10^9, so the target is
nearly always the larger. `broken_calc.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a breadth-first search from the start over the values the
display can show, one press per step, gives the fewest presses to the
target. The search keeps to values from 1 to four times the larger of
the two; a cap of twice the larger, or 64 times, gives the same
answer on every pair up to 40, checked by a Python copy of the
search. It checks 3,200 random pairs: 3,000 up to 40 against the
statement, and 200 with the target up to 10^9 and the start up to
10^9 and up to 1,000 in turn, against the other properties.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 pairs |
| P2 | a target one higher takes at most one press fewer, and a target twice as high at most one press more: a Decrement or a Double at the end |
| P3 | the gap when the target is not above the start; otherwise at least the fewest doublings that reach the target, and at most twice those plus the start |
| P4 | a start one higher takes at most one press more: a Decrement first |
| P5 | the start times 2^k takes exactly k presses, for a random k that stays within 10^9 |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 pairs: 23172188481 operations, checksum 32140808,
95000 checks over 5 arms: 0 failures` under `karac __mir-run` (2.2 s)
and `karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan`
with no error.

## Mutation testing

Thirty-one edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an odd target taken down by one | P1 831, P2 435, P6 953 |
| M2 | ★: the start's gap left out | P1 2579, P3 1529, P6 2777 |
| M3 | ★: the odd test flipped | P1 839, P2 2399, P3 61, P5 3017, P6 920 |
| M4 | recursive: an odd step not counted | P1 950, P6 1084 |
| M5 | recursive: the base case counts the whole start | P1 3000, P3 1605, P5 3200, P6 3200 |
| M6 | recursive: an even step counted twice | P1 1446, P2 2399, P3 77, P5 3017, P6 1595 |
| M7 | doublings: the overshoot all paid before doubling | P1 1297, P2 2259, P3 534, P4 1277, P6 1446 |
| M8 | doublings: the ones of the whole overshoot | P1 2579, P2 774, P3 1529, P4 1524, P6 2777 |
| M9 | doublings: every binary digit counted | P1 281, P2 1084, P6 393 |
| M10 | closed: h counted with rounding down | P1 194, P3 101, P6 194 |
| M11 | closed: one halving too many | P1 1446, P2 804, P5 3017, P6 1595 |
| M12 | closed: c rounded down | P1 283, P6 394 |
| M13 | replay: a Double not counted | P1 1446, P3 330, P5 3017, P6 1595 |
| M14 | replay: one doubling too many when it lands exactly | P1 140, P3 76, P5 3200, P6 140 |
| M15 | replay: a Decrement counted at the value it takes off | P1 444, P2 1084, P3 206, P6 564 |

P1 and P6 kill all fifteen, P3 ten, P2 eight, P5 six and P4 two. P5's
targets, the start times a power of 2, are reached by doubling alone,
so it sees only the mutants that miscount a run of halvings: M3, M5,
M6, M11, M13 and M14. M4, which gets an odd step for free, never meets
an odd value there, and its answers, a little low, still sit inside
P3's bounds and keep P2's and P4's one-press steps, so only P1 and P6
see it; M12 likewise. P4 sees only M7 and M8, which pay for decrements
as if each came before the first doubling, so a start one higher,
whose overshoot is bigger at every doubling, can cost many presses
more (inferred, not traced).

Sixteen other edits were tried and set aside. Nine failed exactly the
same checks as a kept one: recursive taking an odd target down, as
M1, flipping the even test, as M3, and rounding an odd target up and
halving it in one press, as M4; doublings trying no d of 0, as M5;
closed leaving out the rounding presses, as M4, and counting every
binary digit, as M9; replay not counting the first decrements, as M2,
not counting a Decrement between doublings, as M4, and counting a
Double twice, as M6. One was sound but beyond three an arm: ★ reading
the gap the other way. Two survived and are equivalent: doublings
keeping the first d that reaches the target, which is the choice the
closed form and the replay make, and the number of halvings the
greedy, which is right, ends up making; and closed without its early
return, whose formula gives the gap anyway when the target is not
above the start.

Four crashed, the same way in both lanes. ★ going on round its loop at
the start never stops when the start is 1, as 1 becomes 2 and halves
back to 1: the interpreter stops at its step limit and the compiled
lane runs until the harness kills it after 300 s. Recursive without
the start as a base case recurses the same way until the stack
overflows. Closed halving on while the rounded-up value is at the
start does the same with a start of 1 until `power` overflows, which
Kāra checks. Replay pressing Decrement on a 0 bit misses the target,
and its own check stops it with "the plan missed the target".

## Verification

Every arm prints the same output as `broken_calc.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `395f71ae05`, the runtime
archives rebuilt at `d867340a02`, whose runtime sources are the same.
Under `karac __mir-run` the arms take 0.15 s, except doublings at
0.75 s, which tries all 33 numbers of doublings for every pair, and
the differential 2.0 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. The program draws
1,000 random pairs once, each start up to 1,000 and each target up to
10^9. In each of 5,000 rounds it runs the arm on every target, paired
with a start that moves on by one each round, and folds every answer
into a checksum. Every implementation prints `5000 rounds over 1000
pairs: 835294140 operations, checksum 236654435`. Each call walks the
target down to the start, about 30 steps of a parity test and an add
or a halving; there is no allocation anywhere in the timed loop.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `395f71ae05`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.496 to 0.596 s | 0.532 s |
| Rust (`rustc -O`) | 0.509 to 0.600 s | 0.561 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.540 to 0.610 s | 0.571 s |
| Go | 0.354 to 0.417 s | 0.381 s |
| Python | 12.4 s | |
| Kāra (`karac build --mir`) | 0.622 to 0.674 s | 0.641 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 19 times
Kāra's.

v2 took 1.12 times Rust's median time under overflow checks and 1.20
times C's. Go was the fastest. Under valgrind's cachegrind v2 ran
2,272 million instructions and 529 million branches with 55.3 million
mispredicted, Rust with overflow checks 2,030 million, 544 million and
55.4 million, C 1,783 million, 312 million and 54.8 million, and Go
2,328 million, 166 million and 5.0 million. The parity of the target
at each step is as good as random, so a branch on it is missed about
half the time: C, Rust and Kāra branch on it and miss about 11 times a
call, where Go misses about once, at the loop's end, which fits Go
choosing between `t + 1` and `t / 2` without a branch (inferred from
the counts, not read from its code).
