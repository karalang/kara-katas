# 1014. Best Sightseeing Pair

You are given an integer array `values` where `values[i]` is the value of
the `i`-th sightseeing spot. Two spots `i < j` are `j - i` apart, and the
score of the pair is `values[i] + values[j] + i - j`: the sum of their
values minus the distance between them. Return the maximum score of a
pair of sightseeing spots.

```
values = [8,1,5,2,6]  ->  11    (i = 0, j = 2: 8 + 5 + 0 - 2)
values = [1,2]        ->  2
```

**Constraints:** `2 <= values.length <= 5 * 10^4`, `1 <= values[i] <= 1000`.

## Approaches

The score splits into one term per spot, `values[i] + i` for the first
and `values[j] - j` for the second, so the best pair takes the best
first term to the left of each second spot. The arms differ in how they
find it.

| file | mechanism |
|---|---|
| `sightseeing.kara` ★ | one pass: each `j` is scored against the largest `values[i] + i` seen so far, then joins it. O(n), O(1) space |
| `sightseeing_prefix.kara` | prefix maxima: a first pass stores the largest `values[i] + i` left of each `j`, a second scores each `j` against it. O(n) space |
| `sightseeing_suffix.kara` | suffix maxima: the same read from the other end, the largest `values[j] - j` right of each `i`, filled right to left. O(n) space |
| `sightseeing_decay.kara` | a fading view: seen from `j`, an earlier spot is worth `values[i] - (j - i)`, so the best earlier spot's worth is carried along, fading by one per step and replaced by the spot just passed when that one is worth more. O(1) space |
| `sightseeing_split.kara` | divide and conquer: the best pair of a range is in its left half, its right half, or crosses the middle, where it takes the best first term on the left and the best second term on the right. O(n log n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 20 lines: LeetCode's two examples and eleven
more (two equal ones, two 1000s, `[1,1000]`, values falling and rising
by one, equal ends far apart, `[1,3,1,3]`, a 7 and an 8 six apart,
`[2,2,2,2,2]`, `[10,1,1,10]` and `[1,1000,1,1,999,1000]`); the sum and a
checksum of the answers to 3,000 random arrays of 2 values up to 1,000,
3,000 of 8 up to 10, 1,000 of 60 up to 1,000, 200 of 1,000 up to 1,000,
6 of LeetCode's largest 50,000 up to 1,000 and 6 more up to 2; and 1,000
arrays of 2,000 values up to 10 with two 1000s planted a random gap
apart, of which 526 have the planted pair as their best (it scores
`2000 - gap`, and a planted spot beside a 10 scores 1009, so a wide gap
is beaten). `sightseeing.py` mirrors the ★ arm and its output is
byte-identical.

Every array has a pair of neighbours scoring at least `1 + 1 - 1 = 1`,
so 0 starts every running maximum safely, and the split arm scores a
range of one spot 0.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every pair `i < j`, scored as written. It checks 4,193
arrays: every array of 2 to 6 values from 1 to 3 (1,089), 2,000 random
of 2 to 12 values up to 10, 500 random of 13 to 200 values up to 1,000,
500 random of 2 to 60 values up to 3, 100 random of up to 2,000 values
up to 1,000, and 4 of 50,000.

| | property |
|---|---|
| P1 | the statement, for arrays of up to 200 values |
| P2 | the reversed array scores the same, distances being symmetric |
| P3 | the score lies between the best pair of neighbours and the two largest values one step apart |
| P4 | adding 1 to 5 to every value adds twice that to the score |
| P5 | a spot added at the end never lowers the score, and a 1000 there scores at least `999 + ` the last value |
| P6 | each arm agrees with at least two of the other four |

It prints `4193 arrays: checksum 556747742, 125315 checks over 5 arms: 0
failures` under `karac __mir-run` (16 s) and `karac __mir-llvm-run`, and
the same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-nine edits to the differential, each run under `karac __mir-run`
and `karac __mir-llvm-run`; fifteen are kept, three to each arm, all
fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a spot paired with itself (joins before it is scored) | P1 3872, P2 745, P3 3842, P6 3967 |
| M2 | ★: the second spot never at index 1 | P1 1111, P2 1453, P3 1039, P4 200, P5 62, P6 1111 |
| M3 | ★: the first spots lag one behind | P1 1758, P2 1258, P3 1770, P5 935, P6 1770 |
| M4 | prefix: a spot paired with itself | P1 3509, P2 1185, P3 3411, P6 3604 |
| M5 | prefix: the entry at index 2 never filled | P1 599, P2 872, P3 355, P4 20, P5 95, P6 599 |
| M6 | prefix: the first spot's index subtracted | P1 2800, P2 3342, P3 2430, P5 1640, P6 2895 |
| M7 | suffix: filled left to right | P1 1485, P2 968, P3 588, P4 822, P5 60, P6 1573 |
| M8 | suffix: a spot paired with itself | P1 3493, P2 1185, P3 3399, P5 70, P6 3588 |
| M9 | suffix: the first spot never scored | P1 795, P2 1142, P3 657, P4 200, P6 795 |
| M10 | decay: faded after scoring | P1 4098, P3 2096, P6 4193 |
| M11 | decay: the view always replaced by the spot passed | P1 983, P6 1064 |
| M12 | decay: one step too many | P1 4098, P3 3129, P5 1218, P6 4193 |
| M13 | split: a range of two scored 0 | P1 1077, P2 802, P3 1078, P4 200, P5 1112, P6 1078 |
| M14 | split: the last right spot skipped | P1 296, P2 314, P5 47, P6 304 |
| M15 | split: the right half never searched | P1 1716, P2 2353, P3 1445, P5 1507, P6 1808 |

P1 and P6 kill all fifteen, P3 thirteen, P2 twelve, P5 ten and P4 five.
P2 misses only the decay mutants, each of which is off by the same
amount from either end. P4 sees an edit only when it treats the first
spots differently from the rest, since lifting every value keeps every
comparison between pairs. The checks draw no random number that depends
on an answer, so every mutant sees the same arrays and their counts can
be compared.

Fourteen other edits were tried and set aside. Two change no answer: ★
starting its maximum at the first value rather than 0, which the pair
of the first two spots always reaches, and the split arm rounding its
middle up, any middle being a valid split. One failed exactly the same
checks as a kept one: suffix subtracting the first spot's index, as M6.
The other eleven were killed too, beyond three per arm: ★ leaving the
first spot out, adding the distance and dropping the first spot's
index; prefix leaving the first spot out and never scoring a second
spot at index 1; suffix dropping the last spot's index; decay never
fading, already fading the spot it passes and leaving the first spot
out; split skipping the last left spot and adding the first right
spot's index. Leaving the first spot out fails exactly alike in the
★, prefix and decay arms.

## Verification

Every arm prints the same output as `sightseeing.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with
no error; the differential prints its line under all three. `karac
check --output=json` reports no diagnostic for the five arms, the
differential and the bench program, so `karac fix` had nothing to do.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. The release build is kara `56c60bdf7c`, with
runtime archives rebuilt at `ce706dd131`, the last commit before it to
change the runtime. The bench binaries were built one compiler commit
earlier; a rebuild at `56c60bdf7c` emits the same `main`. Under `karac __mir-run` the
arms take 4.0 s (★, decay) to 16.6 s (split).

No compiler gap turned up writing this kata.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages on one array of 50,000
values from 1 to 1,000, drawn once; then 10,000 rounds each set one
random spot to a new random value, ask again, and fold the answer into
a sum and a checksum. Every implementation prints `10000 rounds over
50000 values: answers sum to 19935752, checksum 636087938`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.472 to 0.540 s | 0.493 s |
| Rust (`rustc -O`) | 0.459 to 0.639 s | 0.513 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.513 to 0.679 s | 0.538 s |
| Go | 0.459 to 0.563 s | 0.482 s |
| Python | 59.0 s | |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.579 to 0.604 s | 0.583 s |
| Kāra (`karac build`) | 0.579 to 0.616 s | 0.583 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. Python's run is about 101 times Kāra's. A plain
`karac build` parallelizes nothing here (its user time equals its real
time) and runs as fast as the sequential one: each round's scan carries
its running maximum from one spot to the next.

v2 took 1.08 times Rust's median time under overflow checks and 1.18
times C's. Under valgrind's cachegrind v2 ran 7,252 million
instructions and 1,500 million branches, Rust with overflow checks
7,502 million and 2,000 million, Rust without them 6,752 million and 250
million, and C 6,751 million and 250 million. Every version
mispredicted under 18,000 branches. v2's loop checks three additions
for overflow per spot where checked Rust checks four, and it runs fewer
instructions, yet it takes longer; we did not look into why.
