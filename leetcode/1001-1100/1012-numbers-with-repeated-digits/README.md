# 1012. Numbers With Repeated Digits

Given an integer `n`, return the number of positive integers in the
range `[1, n]` that have at least one repeated digit.

```
n = 20    ->  1     (11)
n = 100   ->  10    (11, 22, 33, 44, 55, 66, 77, 88, 99 and 100)
n = 1000  ->  262
```

**Constraints:** `1 <= n <= 10^9`.

## Approaches

Counting the numbers with a repeat directly is awkward, because a
repeat can appear anywhere; the numbers whose digits are all different
are easy to count by arrangements, and four arms count those and
subtract. The arms differ in how they walk `n`'s digits and how they
count the completions of a prefix.

| file | mechanism |
|---|---|
| `num_dup_digits.kara` ★ | arrangements: the numbers shorter than `n` are 9 * 9 * 8 * ... by length; one of `n`'s length first falls below `n` at some position, where it puts a smaller unused digit and fills the rest from the unused digits in any order. The walk stops at the first digit of `n` that repeats. O(log^2 n) |
| `num_dup_digits_dp.kara` | digit DP that counts the repeats directly: recursion over the digits from the left with the set of digits used, whether one has repeated, whether the prefix still equals `n`'s and whether the number has started; below `n`, a repeat makes every completion count, and the other states are remembered by position and set. O(log n * 2^10 * 10) |
| `num_dup_digits_sets.kara` | by the set of digits used: a set of k digits makes k! orders less the (k - 1)! that start with 0, all shorter than `n` when k is; each set as large as `n`'s length counts its orders at most `n` by walking `n`'s digits. O(2^10 * log n) |
| `num_dup_digits_table.kara` | a table of digit sets, position by position: how many prefixes with distinct digits, already below `n`'s prefix, use each set; each extends by an unused digit, the prefix equal to `n`'s adds the smaller digits, and a shorter number starts at every later position. O(log n * 2^10 * 10) |
| `num_dup_digits_blocks.kara` | three digits at a time: `n` read in base 1,000, each block's digits read off as a set, and a number of `n`'s length first falling below `n` in some block, with a smaller block whose digits are distinct and avoid the earlier blocks'. O(log n * 1000) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 20 lines: LeetCode's three examples and
twelve more (1, 10, 11, 99, 101, 110, 1,022, 98,765, 123,456,789,
987,654,321, 999,999,999 and LeetCode's largest, 10^9); the count just
below each power of ten up to 10^9; totals over every `n` up to 5,000;
and totals over random `n`: 1,000 up to a thousand, 1,000 up to a
million and 200 up to a billion. `num_dup_digits.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: a number has a repeated digit when two of the
characters it is written with are the same, and the count up to `n` is
taken one number at a time, for every `n` up to 200,000. It checks
4,150 values of `n`: every one up to 3,000, then 1,000 random up to
200,000 and 150 random up to 10^9.

| | property |
|---|---|
| P1 | the statement's count, for `n` up to 200,000 |
| P2 | one more number adds at most one to the count: `f(n) - f(n - 1)` is 0 or 1 |
| P3 | none of 1 to 9 repeats, and only 8,877,690 positive numbers have distinct digits at all: `0 <= f(n) <= n - min(n, 9)` and `n - f(n) <= 8877690` |
| P4 | a block of 10^k numbers sharing `n`'s leading digits holds, when those digits are distinct, the arrangements of the unused digits in its last k places and repeats in the rest, and repeats everywhere when they are not: `f(a * 10^k + 10^k - 1) - f(a * 10^k - 1)` is `10^k - P(10 - d, k)` or `10^k` |
| P5 | a window of up to 300 numbers ending at `n` holds as many repeats as the statement finds in it one number at a time |
| P6 | each arm agrees with at least two of the other four |

P1 is the statement where the table reaches, and P5 carries it, a
window at a time, to `n` up to 10^9. P4 is the counting argument the
★ arm rests on, checked with the arm's own answers at the two ends of
the block; the block size k is drawn at random below `n`'s length.

It prints `4150 values of n: checksum 249563523, 123700 checks over 5
arms: 0 failures` under `karac __mir-run` (125 s, most of it the DP
arm and the statement's table) and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Thirty-two edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a leading zero allowed | P1 4000, P2 4, P3 750, P4 535, P5 388, P6 4150 |
| M2 | ★: the smaller digit not taken out of the unused | P1 3931, P2 214, P3 67, P4 3598, P5 3644, P6 4080 |
| M3 | ★: digits reused in the arrangements | P1 3799, P2 31, P3 145, P4 2522, P5 2866, P6 3949 |
| M4 | dp: leading zeros recorded as digits | P1 3900, P2 2, P4 525, P5 308, P6 4050 |
| M5 | dp: states still equal to `n` remembered too | P1 2355, P2 187, P3 37, P4 1788, P5 3017, P6 2505 |
| M6 | dp: the prefix taken as equal to `n` again below it | P1 3788, P2 3219, P3 137, P4 1341, P5 3915, P6 3938 |
| M7 | sets: one place too many after a smaller digit | P1 3931, P2 290, P3 2776, P4 3651, P5 3644, P6 4080 |
| M8 | sets: `n`'s digit not taken out of the set | P1 3822, P2 2381, P3 158, P4 1831, P5 3787, P6 3972 |
| M9 | sets: the sets of `n`'s length counted as shorter | P1 3977, P2 4, P3 3201, P4 3511, P5 3708, P6 4123 |
| M10 | table: no number starts at the second digit | P1 3991, P2 3, P3 9, P4 535, P5 388, P6 4141 |
| M11 | table: a used digit placed again | P1 3981, P2 289, P3 148, P4 3651, P5 3651, P6 4131 |
| M12 | table: `n`'s repeat never ends its prefix | P1 2005, P2 95, P4 1784, P5 2721, P6 2153 |
| M13 | blocks: the block's own digits not taken out | P1 1973, P2 2, P3 122, P4 964, P5 274, P6 2122 |
| M14 | blocks: the earlier blocks' digits not avoided | P1 2763, P2 190, P4 2150, P5 2809, P6 2876 |
| M15 | blocks: only the last block's digits remembered | P4 18, P5 35, P6 33 |

P4, P5 and P6 kill all fifteen, P1 and P2 fourteen each, and P3
eleven. The checks draw no random number that depends on an answer, so
every mutant sees the same values of `n` and their counts can be
compared. M15 is the one edit the statement misses: it forgets only
the digits of blocks before the last, so it needs three blocks, `n` of
at least 1,000,000, and the table stops at 200,000. The 150 values up
to 10^9 find it, through the window and the block checks. P3 misses
the four edits that only move some counts within their bounds.

Seventeen other edits were tried and set aside. One changes no answer:
the sets arm dropping the orders that start with 1 instead of with 0,
which by symmetry are as many. Three failed exactly the same checks as
a kept one: allowing a leading zero in the sets, table and blocks arms,
as M1. The other thirteen were killed too, beyond three per arm: ★
counting `n`'s own length as shorter, never counting `n` itself,
counting a repeating `n` as distinct, and making shorter numbers one
digit longer; dp counting the distinct numbers, one place fewer after a
repeat, and never placing a 9 below `n`; sets never counting `n`;
table letting a shorter number start with 0 and always counting `n`;
and blocks missing a repeat inside a block, never counting `n`, and
three places too many after a smaller block.

## Verification

Every arm prints the same output as `num_dup_digits.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer)
with no error; the differential prints its line under all three.
`karac check` passes all five arms, the differential and the bench
program. `karac run` and a `karac build` binary print the same output
for every arm and the differential. The release build is at kara
`8b6e8a9088` with the `v.iter()` fix of `70e887275e`, the runtime
archives rebuilt at `8b6e8a9088`. Under `karac __mir-run` the arms take
0.3 s (★) to 26 s (dp).

The sets arm compares `set.count_ones()` with a length, and `count_ones`
returns a `u32` while lengths are `i64`, so it is written
`set.count_ones() as i64`: `karac check` refuses the mixed comparison
and `karac fix` offers no repair, though the widening cast loses nothing
(kara B-2026-10-29-16). That the bit-count methods return `u32` at all,
where design.md says Kāra code uses `i64` for every count, is
B-2026-10-29-17.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages: 100,000 values of `n`
up to 10^9, drawn once, and 40 rounds that count every value shifted by
its own amount, folding each count into a checksum. The C version keeps
the digits and the used marks in arrays on the stack; Rust, Go, Python
and Kāra allocate them per call, as the arm does. Every implementation
prints `40 rounds over 100000 values of n: checksum 488236215`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `8b6e8a9088` plus
`70e887275e`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.606 to 0.744 s | 0.666 s |
| Rust (`rustc -O`) | 1.054 to 1.221 s | 1.135 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.119 to 1.198 s | 1.159 s |
| Go | 1.320 to 1.395 s | 1.343 s |
| Python | 30.2 s | |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.874 to 1.031 s | 0.923 s |
| Kāra (`karac build`) | 0.890 to 0.990 s | 0.950 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. Python's run is about 33 times Kāra's. A plain
`karac build` parallelizes nothing here and its binary runs the same
instructions as the sequential one.

v2 took 0.80 times Rust's median time under overflow checks and 1.39
times C's. Under valgrind's cachegrind v2 ran 9,465 million
instructions with 151 million branches mispredicted, Rust with overflow
checks 12,326 million and 166 million, Rust without them 13,820 million
and 132 million, and C 7,473 million and 99 million. C keeps its two
small arrays on the stack; every other version allocates them on each
call. Rust ran more instructions than Kāra under either build; we did
not look into why. Every version mispredicts the loop over the smaller digits, whose
length is the digit of `n` at that place.
