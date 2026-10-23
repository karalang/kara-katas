# 926. Flip String to Monotone Increasing

A binary string is monotone increasing if it consists of some number of
`0`'s (possibly none), followed by some number of `1`'s (also possibly
none).

You are given a binary string `s`. You can flip `s[i]` changing it from
`0` to `1` or from `1` to `0`.

Return the minimum number of flips to make `s` monotone increasing.

```
s = "00110"     ->  1   (flip the last digit to get 00111)
s = "010110"    ->  2   (flip to get 011111, or alternatively 000111)
s = "00011000"  ->  2   (flip to get 00000000)
```

**Constraints:** `1 <= s.length <= 10^5`; `s[i]` is either `'0'` or
`'1'`.

## Approaches

A monotone string is all 0s up to some split and all 1s after it, so the
flips for a split are the 1s before it and the 0s after it.

| file | mechanism |
|---|---|
| `min_flips_mono_incr.kara` ★ | one pass, keeping the fewest flips for the prefix and its 1s: a 1 can always stay, and a 0 either flips, one more than before, or stays, and then every 1 before it flips. O(n), O(1) space |
| `min_flips_mono_incr_prefix.kara` | the 1s of every prefix counted into a `Vec` once, then every split from 0 to `n` tried, its 0s after found from the counts. O(n), O(n) space |
| `min_flips_mono_incr_states.kara` | two counts for the prefix, the flips that leave it all 0s and those that leave it monotone ending in a 1, each character updating both. O(n), O(1) space |
| `min_flips_mono_incr_split.kara` | the split moved along: before the first character every 0 flips, and passing a 0 saves a flip while passing a 1 adds one; the least cost seen wins. O(n), O(1) extra space |
| `min_flips_mono_incr_halves.kara` | divide and conquer: a `Stretch` struct holds a stretch's 0s, 1s and fewest flips, and two stretches side by side take the better of the left monotone with the right all 1s and the left all 0s with the right monotone. O(n), O(log n) deep |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's three examples and seven
more (a single 0 and a single 1, already monotone, one pair out of
order, the 1s first, and alternating from either digit); for 300 random
strings of 1 to 2,000 characters, leaning from 0 to 1, the answers' sum
(74,085) and a checksum; and three of LeetCode's largest, 100,000
characters: 1s then 0s, alternating, and random.
`min_flips_mono_incr.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: try every binary string of the same length, keep those that
are some 0s followed by some 1s, and take the fewest characters that
differ from `s`. It checks 3,200 random strings, each leaning toward 0
or 1 by a random amount: 3,000 of 1 to 10 characters against the
statement, and 200 of 1 to 2,000 against the other properties; 209,942
characters in all.

| | property |
|---|---|
| P1 | the statement's answer, on the small strings |
| P2 | at least 0 and at most the number of 0s or of 1s, whichever is smaller, since flipping all of either works |
| P3 | the same answer for the string reversed with every character flipped |
| P4 | the same answer with a 0 put in front or a 1 behind, by turns |
| P5 | for a second random string `t`, the answer for `s` followed by `t` is the smaller of the answer for `s` plus the 0s of `t` and the 1s of `s` plus the answer for `t` |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 strings, 209942 characters, answers summing to 55080,
95000 checks over 5 arms: 0 failures` under `karac __mir-run` (7 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a 0 always flipped | P1 1811, P2 1491, P3 2932, P4 1557, P5 1491, P6 1957 |
| M2 | ★: a 0 never flipped | P1 624, P2 586, P3 1351, P5 925, P6 747 |
| M3 | ★: the larger of the two choices | P1 2270, P2 2150, P3 2329, P4 1194, P5 2422, P6 2469 |
| M4 | prefix: the split before the first character never tried | P1 960, P2 1006, P3 2033, P4 476, P6 1006 |
| M5 | prefix: the 0s after a split counted one short | P1 3000, P2 1469, P6 3200 |
| M6 | prefix: the 1s before a split counted one character too far | P1 1744, P2 1146, P3 2363, P4 672, P5 443, P6 1886 |
| M7 | states: a 1 free in the all-0s state | P1 1536, P5 2087, P6 1731 |
| M8 | states: ending in a 1 only after ending in a 1 | P1 652, P4 1466, P5 650, P6 740 |
| M9 | states: the answer read from the all-0s state alone | P1 1744, P2 1441, P3 2932, P4 1643, P5 1452, P6 1886 |
| M10 | split: the starting cost counting the 1s, not the 0s | P1 2732, P2 2514, P3 2932, P4 3200, P5 2898, P6 2932 |
| M11 | split: passing a 0 saving two flips | P1 2098, P2 1784, P3 2977, P4 1557, P5 1647, P6 2265 |
| M12 | split: the least cost taken only after a 1 | P1 1811, P2 1217, P3 2363, P4 1384, P5 718, P6 1957 |
| M13 | halves: the left stretch all 0s counted by its 0s | P1 1825, P2 1149, P3 2620, P4 1281, P5 1917, P6 2005 |
| M14 | halves: a single 0 counted as a flip | P1 979, P2 1027, P3 2033, P4 532, P6 1027 |
| M15 | halves: the right stretch's 1s lost | P1 697, P3 904, P4 643, P5 1805, P6 891 |

P1 and P6 kill all fifteen, and P2, P3, P4 and P5 twelve each. M5 makes
every answer one less, which keeps P3, P4 and P5 (each side of P5 is one
less too) and fails P2 only where the true answer is 0. M7 makes every
answer 0, which every property but the statement, P5 and the other arms
allows. P4 misses M2, whose prefix answer is its count of 1s before the
last 0, unchanged by a 0 in front or a 1 behind, as well as M5 and M7.
P5 misses M5 and the two that leave out the split at one end, M4 the
split before the first character and M14 the split after the last,
since the two sides of P5 leave the same split out.

Eight other edits were tried and set aside. One is equivalent: split
also taking the least cost before each move, which only repeats a
comparison. One was sound but beyond three an arm (★ with the 1s
counted one short). Six failed exactly the same checks as another:
three more ways to make every answer 0 (states letting a 0 end in a 1
for free, split passing a 1 for free, halves leaving the right stretch
all 1s out) as M7; prefix never trying the split after the last
character, as halves' M14; split leaving the starting split out, as M4;
and split's starting cost one short, as M5.

## Verification

Every arm prints the same output as `min_flips_mono_incr.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 0.8 to 1.5 s each (halves, which
recurses down to every character, the longest) and the differential
7 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

Every arm and the differential print the same output under the frozen
legacy interpreter, the legacy JIT and both legacy builds, with and
without auto-par, except that the legacy interpreter did not finish the
halves arm within the 1,200 s limit; the builds of the halves arm and
the differential also warn that a vector is moved and then used again,
which v2's borrowing parameters make untrue. Legacy refuses the bench
program, which passes `strings[(r + i) % count]` straight to the
function: "cannot move ... out of an index", legacy's owned parameters,
where v2's parameter borrows it. An earlier draft of the differential
passed `next_random(mut seed)` as arguments beside `mut seed` itself, and
the legacy interpreter drew different strings from it (208,767
characters rather than 209,942), as in kata 921, so the differential now
draws those values first, which v2 prints the same for. Legacy is
frozen, so none of this is filed.

## Benchmarks

The bench program builds 100 strings of 100,000 characters once,
LeetCode's largest, leaning from 0 to 1, and in each of 20 rounds runs
the ★ arm on every string, each round starting from a different string.
Every implementation prints `20 rounds over 100 strings of 100000:
answers summing to 49943280, checksum 153719090`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.61 to 0.65 s | 0.62 s |
| Rust (`rustc -O`) | 0.60 to 0.64 s | 0.61 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.68 to 0.73 s | 0.69 s |
| Go | 0.75 to 0.84 s | 0.78 s |
| Python | 11.9 s | |
| Kāra (`karac build --mir`) | 0.71 to 0.82 s | 0.74 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about 19 times C's.

v2 takes 1.07 times Rust's median time under overflow checks and 1.19
times C's. Every character is a branch on a random digit, and under
valgrind's cachegrind all three mispredict 57.0 million branches, which
dominates; beside that, v2 runs 2.21 billion instructions and 0.63
billion branches, Rust with overflow checks 1.81 billion and 0.62
billion, and C 1.29 billion and 0.31 billion.
