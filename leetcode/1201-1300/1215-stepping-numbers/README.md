# 1215. Stepping Numbers

A stepping number is an integer such that all of its adjacent digits
have an absolute difference of exactly `1`.

- For example, `321` is a stepping number while `421` is not.

Given two integers `low` and `high`, return a sorted list of all the
stepping numbers in the inclusive range `[low, high]`.

```
low = 0, high = 21     ->  [0,1,2,3,4,5,6,7,8,9,10,12,21]
low = 10, high = 15    ->  [10,12]
```

**Constraints:** `0 <= low <= high <= 2 * 10^9`.

The arms are `fn count_stepping_numbers(low: i64, high: i64) ->
Vec[i64]`. The two Rust arms keep the method LeetCode gives Rust users,
on `i32`, inside `impl Solution`, and a one-line `count_stepping_numbers`
narrows the bounds, calls it and widens the answer.

## Approaches

| file | mechanism |
|---|---|
| `stepping_numbers.kara` ★ | a breadth-first search from the digits 1 to 9, each number followed by itself with one more digit, its last digit one less or one more; a level holds the numbers of one length in rising order, since their parents rise and each gives the lesser child first, so the numbers come out sorted and the search stops at the first past `high`. 0 is its own case. O(answer + the numbers up to `high`'s length) |
| `stepping_numbers_dfs.kara` | depth first: from each digit, a recursion that appends one less or one more than the last digit while the number stays within `high`, keeping those at least `low`; the numbers come out grouped by first digit, so they are sorted at the end |
| `stepping_numbers_table.kara` | a table: every stepping number with up to ten digits, 6237 of them whatever the range, built length by length, so the table rises; then the range cut out of it by two binary searches |
| `stepping_numbers_digits.kara` | as text: the numbers of each length up to `high`'s built as `String`s of digits, each extended by the digit one below or one above its last, then parsed with `i64.parse`; the strings of one length rise as the numbers do |
| `stepping_numbers_queue.kara` | a Rust solution as LeetCode's Rust users write it (the bounds widened to `i64`, a `VecDeque<i64>` started from `(1..=9).collect()`, drained by `while let Some(num) = q.pop_front()`, a number past `high` passed over with `continue`), carried to Kāra by `karac fix` |
| `stepping_numbers_nested.kara` | another Rust solution (a nested `fn dfs(num: i64, low: i64, high: i64, res: &mut Vec<i32>)` from each digit `0..=9`, and the answer put in order by `sort_unstable`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six more properties |

Every arm prints the same 12 lines: LeetCode's two examples; `[0, 0]`
(`[0]`); the digits `[1, 9]`; `[9, 10]`, both ends stepping; `[100,
120]` (`[101]`); `[2000000000, 2000000000]` (`[]`); `[1234567898,
2000000000]`, from the greatest stepping number in range to the top
(`[1234567898]`); 1000 random ranges of up to 5000 numbers below 105000
(`1000 small ranges: 7196 found, checksum 433522009`); and three at the
constraints' top: the whole range `[0, 2000000000]` (`3502 found`, the
last `1234567898`), its upper half from `1000000000` (`251 found`, the
first `1010101010`), and 20 random ranges up to `2000000000`, folded
into a checksum. `stepping_numbers.py` mirrors the ★ arm, and its output
is byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, dfs, table and digits arms check clean as written.
The queue arm takes one round of 7 fixes (among them the `use` line
dropped, `struct Solution;` to `struct Solution {}`, `Vec<i32>` to
`Vec[i32]`, `Vec::new()` to `Vec.new()`, and `VecDeque<i64>` to
`VecDeque[i64]`), and the nested arm one round of 15 (among them the
nested `fn dfs` moved to the top level, `res: &mut Vec<i32>` to `res:
mut ref Vec[i32]`, `vec![]` to `Vec.new()`, `dfs(d, low as i64, high as
i64, &mut res)` to `dfs(d, low, high, mut res)`, the `i32` bounds
widening to the `i64` parameters by themselves, and `sort_unstable()` to
`sort()`). Both outputs match.

## Gaps

None found.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every number from `low` to `high`, each one's digits looked
at in turn. 2000 random cases: a range of up to 300 numbers starting
below 100, below 100000, or anywhere up to the top; 728 of them hold a
stepping number, 9065 in all.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | rising, every number stepping and in range |
| P3 | the range split in two gives the two answers one after the other |
| P4 | the range one wider at each end holds the answer and at most two more |
| P5 | every number's digits reversed make a stepping number |
| P6 | the range from 0 to `high`, cut at `low`, gives the same |
| P7 | the ★ arm's answer |

All 84,000 checks pass on every arm: `2000 cases: checksum 14887410,
84000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. A Python reading of
the same cases, every number's digits compared in pairs, gives the same
checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: low itself left out | P1 160, P3 76, P6 160, P7 800 |
| S2 | ★: 9 never follows 8 | P1 551, P7 2755 |
| D1 | dfs: the answer never sorted | P1 591, P2 591, P3 462, P7 591 |
| D2 | dfs: 0 grown like any digit | P1 606, P2 606, P4 3, P7 606 |
| T1 | table: the search lands past an equal number | P1 197, P2 32, P6 160, P7 197 |
| T2 | table: high itself left out | P1 50, P3 62, P7 50 |
| G1 | digits: "0" extended like any number | P1 63, P2 63, P3 26, P7 63 |
| G2 | digits: high itself left out | P1 50, P3 62, P7 50 |
| Q1 | queue: 9 never a first digit | P1 602, P7 602 |
| Q2 | queue: the lesser child put at the front | P1 699, P2 699, P3 513, P7 699 |
| N1 | nested: the answer never sorted | P1 591, P2 591, P3 462, P7 591 |
| N2 | nested: 0 never follows 1 | P1 603, P7 603 |

A mutation of the ★ arm fails P7 on all six arms, the ★ arm against the
other five. D1 and N1 are one fault in two arms, the answer left grouped
by first digit, and fail alike; T2 and G2 are another, `high` itself
left out. P5, every number's digits reversed make a stepping number,
catches none: every mutation still gives only stepping numbers, and gets
wrong which of them are in range. P4 catches only D2, which gives every
stepping number that begins with 1 twice, the second time as if after a
leading 0, so a range one wider that reaches such a number gains it
twice. P6, the range taken from 0 and cut at `low`, catches S1 and T1,
the two that leave out `low` itself.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (a breadth-first search from the digits 1 to 9, each number followed
by itself with one more digit, stopping at the first number past `high`)
on 2000 random ranges inside the constraints' 0 to 2 * 10^9, drawn once;
then 20 rounds over the ranges, each answer's length and last number
folded into a checksum. Every program prints `20 rounds over 2000
ranges: checksum 377061262`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.412 to 0.566 s | 0.475 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.421 to 0.522 s | 0.463 s |
| Rust (`rustc -O`) | 0.428 to 0.546 s | 0.459 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.463 to 0.563 s | 0.495 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.478 to 0.585 s | 0.509 s |
| C (`clang -O3`) | 0.408 to 0.611 s | 0.435 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.333 to 0.466 s | 0.371 s |
| Go | 2.339 to 2.527 s | 2.439 s |
| Python | 30.87 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 6% ahead of Rust with overflow checks on (0.463 s
against 0.495 s), and the two ranges overlap. C is about 6% ahead of
Kāra (0.435 s against 0.463 s); Go takes about 5.3x Kāra's time. Python
takes about 67x Kāra's time. No profile was taken.
