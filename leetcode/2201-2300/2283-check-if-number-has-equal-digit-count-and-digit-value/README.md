# 2283. Check if Number Has Equal Digit Count and Digit Value

You are given a **0-indexed** string `num` of length `n` consisting of
digits.

Return `true` *if for **every** index* `i` *in the range* `0 <= i < n`*,
the digit* `i` *occurs* `num[i]` *times in* `num`*, otherwise return*
`false`.

```
num = "1210"  ->  true
num = "030"   ->  false
```

**Constraints:** `n == num.length`; `1 <= n <= 10`; `num` consists of
digits.

Count each digit once, then check every place against the count of its
own index. O(n). A string that holds describes itself, and they are
rare: one or two for each length from 4 to 10 (`1210` and `2020`,
`21200`, `3211000`, `42101000`, `521001000`, `6210001000`), and none
shorter. Since every place counts the digits of one index, the digits
of a true string sum to its length.

## Approaches

| file | mechanism |
|---|---|
| `digits.kara` ★ | an `Array[i64, 10]` of counts over `chars()`, then each place by `enumerate` against the count of its index |
| `digits_naive.kara` | the digits as a `Vec[i64]`, and for each index a walk of all of them counting that digit |
| `digits_map.kara` | a `Map[char, i64]` of counts, each place looking up the character of its own index, an absent one counting 0 |
| `digits_struct.kara` | `struct Tally` of the ten counts, built by `of`; `says` answers for one place, and the string holds when every place's does |
| `digits_iter.kara` | one chain: `enumerate` and `all`, each place's count by `filter` and `count` over the string again |
| `digits_solution.kara` | LeetCode's Rust template: `String` in, `bool` out; `[0usize; 10]` counted over `num.bytes()`, then `enumerate().all(..)`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 16 lines: LeetCode's two examples, the other
six strings that hold, and six near misses (`0`, `1`, `10`, `1211`,
`2120`, `6210001001`), each with its answer; then 5000 random strings
of 1 to 10 digits, each below 3, at most the length, or any, with a
checksum and the 6 that hold; then every string of 4 digits each below
5, of which `1210` and `2020` hold. `digits.py` mirrors the ★ arm and
its output is byte-identical.

The naive arm first collected `to_digit(10).unwrap()` straight into a
`Vec[i64]`. `to_digit` gives a `u32`, and `collect` does not convert its
items; `karac check` says so and `karac fix` widens each in the `map`
with `as i64`.

`karac fix` carries the template in one round, reporting 5 edits:
`num.bytes().enumerate()` to `num.bytes().iter().enumerate()`, since
`bytes()` is a `Vec[u8]`, the `as usize` on the compared digit dropped,
`struct Solution;` to `struct Solution {}`, and in the adapter `&str` to
`Str` and `Solution::` to `Solution.`. The `[0usize; 10]` and the index's
`as usize` stay as written.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every index, the occurrences of its digit found by
splitting the string on it, against the digit standing there. No counts
table. It checks 300 random strings of 1 to 10 digits, each below 3, at
most the length, or any; then 30 self-describing strings with one place
changed or not; then 30 strings whose digits sum to their length, the
near misses the sum alone cannot rule out. All 360 are drawn before any
arm answers; 15 of them hold.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | true only when the digits sum to the length |
| P3 | a true string with its first digit below 9 raised by one: false |
| P4 | true exactly when the string is its own description, the count of each index's digit written in place |
| P5 | a true string shorter than 10 with a 0 appended: false |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 926138464, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading by
`collections.Counter`. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last place never checked | P1 31, P2 18, P3 27, P4 31, P5 13, P6 31 |
| M2 | ★: the first digit never counted | P1 30, P2 15, P4 30, P6 30 |
| M6 | ★: the answer from the first place alone | P1 32, P2 29, P4 32, P6 32 |
| M7 | naive: the count from 1 | P1 31, P2 3, P4 31, P6 31 |
| M8 | naive: the count against the index | P1 47, P2 19, P3 25, P4 47, P6 47 |
| M10 | naive: every other place checked | P1 4, P2 4, P4 4, P6 4 |
| M12 | map: each place asking for the next digit | P1 41, P2 13, P3 10, P4 41, P5 26, P6 41 |
| M13 | map: an absent digit counted once | P1 29, P2 1, P4 29, P6 29 |
| M14 | map: presence for count | P1 16, P2 1, P4 16, P5 1, P6 16 |
| M17 | struct: the place never moved | P1 15, P4 15, P6 15 |
| M18 | struct: says inverted | P1 146, P2 108, P3 99, P4 146, P5 36, P6 146 |
| M20 | struct: each digit tallied twice | P1 18, P2 1, P4 18, P6 18 |
| M22 | iter: any place for all | P1 214, P2 175, P3 197, P4 214, P5 192, P6 214 |
| M23 | iter: a count at most the digit | P1 121, P2 105, P3 114, P4 121, P5 48, P6 121 |
| M25 | iter: the first place skipped | P1 52, P2 36, P3 40, P4 52, P5 47, P6 52 |
| M27 | solution: the zeros never counted | P1 29, P2 14, P4 29, P5 14, P6 29 |
| M28 | solution: a count at least the digit | P1 19, P2 19, P3 4, P4 19, P5 34, P6 19 |

P1, P4 and P6 kill all seventeen, P2 sixteen, P5 nine, and P3 eight.
P4 fails exactly where P1 does: the description is the statement in
another form, built with no literal reading's split. P2, P3 and P5 are
the sum argument, tested only on strings an arm calls true. P2 misses
only the struct arm's place never moved, which checks every digit
against the count of zeros and so calls no string true at all. P3 and
P5 ask more, a second string the arm must call false, and catch the
edits that turn many false strings true: a test inverted, any for all,
a count at most or at least the digit, places shifted or skipped,
presence for count, and the zeros never counted.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Twelve fail as a kept one does: the ★ arm's test
inverted (M3) as the struct arm's says inverted (M18); the ★ arm's
each count one more and the map and iter arms' each place's own digit
counted (M4, M16, M26) as the naive arm's count from 1 (M7); the ★ and
struct arms' place and digit swapped, the naive arm's count against the
mirror place (M5, M21, M11) as the struct arm's place never moved
(M17); the naive arm's digits from the index up counted (M9) as the map
arm's absent digit counted once (M13); the map arm's first place never
checked (M15) as the iter arm's first place skipped (M25); and the
struct arm's places from 1, the iter arm's each place counting the next
digit and the template's each place reading the next count (M19, M24,
M29) as the map arm's each place asking for the next digit (M12). Two
fail in ways of their own and are left out because the template keeps
enough: each digit read modulo 4 and digits from 5 counted 5 less (M30,
M31).

One edit of the first draft passed every check: the template's only the
first five places, since no drawn string holds in its first five places
and fails after them. It is now M30.

## Verification

Every arm prints the same output as `digits.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.3 s and the differential 0.4
s.

## Benchmarks

The bench builds 10^5 strings once, every eighth a self-describing one
and the rest 1 to 10 random digits each at most the length, then makes
100 passes over all of them counting those that hold, with the ★ arm in
all five languages. Every implementation prints `100 passes over 10^5
strings: checksum 686052963`. C keeps the strings as NUL-terminated
arrays of 11 bytes. The Rust twin first left `check` unannotated: its
literal defaulted to `i32`, `check * 31` wrapped silently under `-O`,
and the checksum differed; it is declared `i64`.

BENCHTAB
