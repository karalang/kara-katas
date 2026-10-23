# 902. Numbers At Most N Given Digit Set

Given an array of `digits` which is sorted in non-decreasing order, you
can write numbers using each `digits[i]` as many times as you want. For
example, if `digits = ['1','3','5']`, we may write numbers such as
`'13'`, `'551'` and `'1351315'`.

Return the number of positive integers that can be generated that are
less than or equal to a given integer `n`.

```
digits = ["1","3","5","7"], n = 100         ->  20
digits = ["1","4","9"], n = 1000000000      ->  29523
digits = ["7"], n = 8                       ->  1
```

**Constraints:** `1 <= digits.length <= 9`, `digits[i].length == 1`,
`digits[i]` is a digit from `'1'` to `'9'`, all the values in `digits`
are unique and sorted in non-decreasing order, and `1 <= n <= 10^9`.

## Approaches

Every number with fewer digits than `n` is at most `n`, and there are
`d^k` with `k` digits for a set of `d` digits; the arms differ in how
they count the numbers as long as `n`.

| file | mechanism |
|---|---|
| `numbers_at_most_n.kara` ★ | lengths, then the digits of `n` from the left: a digit of the set below `n`'s digit can be followed by anything, `d^rest` ways; an equal digit keeps to `n`'s digits, and if `n`'s digit is not in the set nothing more matches. O(log n * d) |
| `numbers_at_most_n_dp.kara` | a table from the right: `ways[i]` counts the numbers as long as `n`'s digits from place `i` that are at most them, `ways[k] = 1`, a digit below followed by `d^(k - i - 1)` and an equal digit by `ways[i + 1]`. O(log n * d) |
| `numbers_at_most_n_bijective.kara` | bijective base `d`: with the set's digits ranked 1 to `d`, the numbers made of them in increasing order are exactly the numerals of bijective base `d`, so the count is the value of the largest such number at most `n`, built from `n`'s digits. O(log n * d) |
| `numbers_at_most_n_search.kara` | a binary search on the count: the `j`-th smallest number made of the set's digits is `j` written in bijective base `d`, so search the largest `j` whose number is at most `n`. O(log n * log n) |
| `numbers_at_most_n_recursive.kara` | choosing digits place by place, recursively, keeping whether the digits so far are `n`'s own; once below, the places left are counted at once. O(log n * d) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and six
more (a set of one equal to `n`, a set of one above `n`, every digit up
to `10^9`, `919` from `1` and `9`, `2468` from its own digits, and a
set of one above `n = 1`); and for 2,000 random cases, with sets of
every size and `n` up to `10^9`, half of them written with the set's
digits but one, the sum of the counts and a checksum.
`numbers_at_most_n.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every positive integer up to `n` tried, its digits read off
one by one and looked up in the set. It checks 3,200 random cases: 3,000
with `n` up to 1,000 against the statement and 200 with `n` up to
`10^9` against the other properties, with sets of every size, 16,103
digits in the sets in all, and `n` half of the time written with the
set's digits but one.

| | property |
|---|---|
| P1 | the statement's count, on the small cases |
| P2 | one more for `n + 1` exactly when `n + 1` is written with the set's digits, and otherwise the same |
| P3 | no more with a digit taken out of the set, and no fewer with a digit put in |
| P4 | `d + d^2 + ... + d^k` up to `k` nines, and the same up to `k` of the set's largest digit |
| P5 | `d * (count + 1)` up to `10n + 9`, and `d * (the count up to n - 1, plus 1)` up to `10n`, since a number of two places or more is a number up to `n` (or below it) with a digit of the set after it |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every case. It prints `3200 cases, 16103 digits
in the sets, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the one-digit numbers never counted | P1 2216, P2 102, P4 2843, P5 1450, P6 2393 |
| M2 | ★: a digit equal to `n`'s counted as below it | P1 1307, P2 702, P5 921, P6 1423 |
| M3 | ★: `n` itself never counted | P1 1086, P2 674, P4 3200, P5 1855, P6 1161 |
| M4 | dp: nothing after the last place | P1 1086, P2 674, P4 3200, P5 1855, P6 1161 |
| M5 | dp: a digit below followed by a place too many | P1 1684, P2 1153, P4 2743, P5 2003, P6 1823 |
| M6 | dp: a digit equal to `n`'s followed by one way only | P1 1326, P2 718, P4 2436, P5 2065, P6 1446 |
| M7 | bijective: the smallest digit never taken as the one below | P1 326, P2 192, P4 400, P5 264, P6 347 |
| M8 | bijective: one place fewer, every digit the smallest | P1 722, P2 96, P5 920, P6 740 |
| M9 | bijective: the places after filled with the second largest | P1 499, P2 146, P4 1221, P5 2260, P6 570 |
| M10 | search: each place's digit the next rank up | P1 1585, P2 514, P3 100, P5 46, P6 1716 |
| M11 | search: the numbers as long as `n` left out of the range | P1 1967, P2 1122, P4 3200, P5 744, P6 2125 |
| M12 | search: `n` itself taken as above `n` | P1 1086, P2 674, P4 3200, P5 1855, P6 1161 |
| M13 | recursive: `n`'s own digits never counted at the end | P1 1086, P2 674, P4 3200, P5 1855, P6 1161 |
| M14 | recursive: an equal digit freeing the rest | P1 1307, P2 702, P5 921, P6 1423 |
| M15 | recursive: the empty number counted | P1 3000, P4 3200, P5 2766, P6 3200 |

P1, P5 and P6 kill all fifteen, and P2 all but M15, whose count is one
too many for every `n` alike, so the step from `n` to `n + 1` is
unchanged. Four mutants in four arms fail exactly the same cases (M3,
M4, M12, M13): each leaves `n` itself out when it is written with the
set's digits, which P4 sees on every case, since `k` nines or `k` of
the largest digit are always such a number. M2 and M14 fail the same
cases: both let a digit equal to `n`'s free the places after it, counting
numbers above `n`. P3 kills only M10, whose numbers are out of order
and so can count fewer with a digit more or more with a digit fewer;
every other mutant is wrong in a way that keeps a larger set's count at
least a smaller set's.

Two mutants were replaced. The first M7, a kept digit of rank 1 stepped
down to rank 0 rather than passed over, survived: a rank of 0 followed
by the largest digits has the same value in base `d` as the earlier
digit stepped down and the largest digits from there on, so the
arm's search back for a digit with a smaller one is not needed for the
value at all. The first M10, `j` written in plain base `d`, overflowed
for a set of one digit, and the first M13, the free places one short,
recursed without end; both were replaced by edits that run to the end.

## Verification

Every arm prints the same output as `numbers_at_most_n.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take under 0.2 s
each and the differential 26 s, most of it the statement read
literally.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy lanes split. The ★ and search arms print the same
output under the legacy interpreter; the legacy JIT and both legacy
builds, with and without auto-par, stop at codegen with `no handler for
method 'len' on variable 's' in digit_set`, the harness function that
turns `"1357"` into strings of one digit. Every legacy lane refuses the
dp, bijective and recursive arms and the differential (`*c` on an
element of `.iter()` is rejected, because legacy's iterator gives the
value itself), and the bench program (`E_INDEX_MOVE_NON_COPY` on
`sets[q % 511]` handed to the function). Legacy is frozen, so none of
this is filed.

## Benchmarks

The bench program uses the ★ arm on every one of the 511 sets of the
digits 1 to 9, built once as lists of one-digit strings, in turn,
8,000,000 times, each time with a random `n` from 1 to `10^9`. C keeps
the sets as arrays of string pointers and writes `n` out with
`snprintf`; the others use their own strings. Every implementation
prints `8000000 queries over the 511 digit sets: counts summing to
37122549621613, checksum 435293348`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.59 to 0.70 s | 0.67 s |
| Rust (`rustc -O`) | 0.44 to 0.55 s | 0.48 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.63 to 0.72 s | 0.69 s |
| Go | 0.82 to 1.04 s | 0.86 s |
| Python | 21.2 s | |
| Kāra (`karac build --mir`) | 0.85 to 0.96 s | 0.92 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 901's does. Legacy refuses the bench program
(above), so it has no row.

v2 takes 1.34 times Rust's median time under overflow checks and 1.37
times C's. Under valgrind's cachegrind C runs 7.49 billion instructions
and 774 million branches, Rust with overflow checks 5.35 billion and
1.20 billion, and v2 8.02 billion and 1.53 billion; C mispredicts 37
million, Rust 78 million and v2 80 million. C runs more instructions
than Rust, which suggests `snprintf` costs more than Rust's
`to_string`, though that was not profiled. v2 runs 1.50 times Rust's
instructions. Its source copies `n`'s digits once more than Rust's does
(`n.to_string().bytes().to_vec()` where Rust takes the string's bytes
with `into_bytes`), but where v2's extra instructions go was not
measured. The comparison with C and Rust waits until after M4.
