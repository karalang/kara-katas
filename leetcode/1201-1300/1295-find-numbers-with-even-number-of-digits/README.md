# 1295. Find Numbers with Even Number of Digits

Given an array `nums` of integers, return how many of them contain an
**even number** of digits.

```
nums = [12,345,2,6,7896]   ->  2     12 and 7896 have 2 and 4 digits
nums = [555,901,482,1771]  ->  1     only 1771
```

**Constraints:** `1 <= nums.length <= 500`, `1 <= nums[i] <= 10^5`.

The arms are `fn find_numbers(nums: Vec[i64]) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `find_numbers.kara` ★ | each number's digits counted by dividing by 10 until nothing is left, the even counts counted. O(n log max) |
| `find_numbers_string.kara` | each number written out with an f-string, and the even lengths counted by `filter` and `count` |
| `find_numbers_range.kara` | under the constraints a number has an even number of digits exactly when it is in `10..=99`, `1000..=9999` or is `100000`, so each is matched against those patterns. O(n) |
| `find_numbers_log.kara` | the number of digits is one more than `x.ilog10()`, the integer logarithm. O(n) |
| `find_numbers_recursive.kara` | the digits counted by recursion on the number without its last digit, and the even counts folded over the array |
| `find_numbers_solution.kara` | a Rust solution as LeetCode's Rust users write it (`nums.iter().filter(\|n\| n.to_string().len() % 2 == 0).count() as i32`), carried to Kāra by `karac fix` |
| `find_numbers_loop.kara` | a second Rust solution as LeetCode's Rust users write it (`for mut n in nums`, the digits counted by `n /= 10` on the moved number), carried to Kāra by `karac fix` |
| `differential.kara` | the seven arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, every number
on either side of a power of ten from 1 to `10^5`, `100000` alone and
`10` alone (`2 1 5 1 1`); then 3000 random arrays of 1 to 500 numbers,
each number's count of digits drawn first so that every count comes up
as often (`3000 random arrays: 377812 with an even number of digits,
checksum 189474389`). `find_numbers.py` mirrors the ★ arm, and its output
is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the five Kāra arms checked clean as first written. The two
Rust arms each take one round, 8 fixes and 10 by `karac fix`'s count:
`Vec<..>` to `Vec[..]`, `struct Solution;` to `struct Solution {}`, `::`
to `.`, the wrapper's `|&x|` to `|x|` and its `as i64` dropped as a
widening, and in the loop arm `for mut n in nums` to `for n in nums`
with `let mut n = n;` as the loop's first line. Both outputs match on
the first run. No gap was met.

## Differential

`differential.kara` holds copies of the seven arms and the statement read
literally: a number has d digits when it is at least `10^(d - 1)` and
below `10^d`, each power built by multiplying. 2000 arrays of 1 to 30
numbers in four kinds, 500 each: the count of digits drawn first, from 1
to 6; any number up to `10^5`; only numbers next to a power of ten (9,
10, 11, 99, 100, 101, ...); and one count of digits throughout. Every
array and split point is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the array reversed: the same count |
| P3 | the numbers below `10^4` each times 10, a digit longer: as many as were odd among them |
| P4 | the array split anywhere: the two counts add up |
| P5 | 10 and 100 appended: one more |
| P6 | the ★ arm's answer |

All 84,000 checks pass on every arm: `2000 arrays: checksum 822646075,
84000 checks over 7 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Fourteen edits to the differential, two to each arm, each run under both
`karac __mir-llvm-run` and `karac __mir-run`. Every one is killed, fails
the same way under both backends and not by a crash. Thirteen are kept;
the solution arm's count one short fails exactly as the recursive arm's
fold started from 1 does, one off on every array, and is left out.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: digits taken off two at a time | P1 1100, P3 1066, P6 6600 |
| M2 | ★: the odd counts counted | P1 1898, P6 11388 |
| M3 | string: lengths divisible by 4 counted | P1 1019, P3 1145, P5 2000, P6 1019 |
| M4 | string: the first number skipped | P1 733, P2 579, P3 1762, P4 595, P6 733 |
| M5 | range: 99 left out | P1 290, P3 290, P6 290 |
| M6 | range: `100000` left out | P1 792, P6 792 |
| M7 | log: the logarithm in base 2 | P1 1823, P3 1277, P6 1823 |
| M8 | log: digit counts divisible by 3 counted | P1 1538, P3 1504, P6 1538 |
| M9 | recursive: two-digit numbers counted as one digit | P1 1784, P3 967, P6 1784 |
| M10 | recursive: the fold started from 1 | P1 2000, P3 2000, P4 2000, P6 2000 |
| M11 | solution: each number's successor measured | P1 585, P3 579, P6 585 |
| M13 | loop: the leading 1 not counted as a digit | P1 1593, P6 1593 |
| M14 | loop: half the digits added for each even count | P1 1380, P3 1515, P6 1380 |

P1 and P6 kill all thirteen, P3 ten, P4 two, and P2 and P5 one each.
Counting the odd ones (M2) makes an arm answer the complement, and the
complement keeps P3: times 10 turns odd into even for it as well. M13
miscounts only the numbers that start with a 1, and a number times 10
starts with the same digit, so P3 holds for it too. P2 and P4 see only
the edits that treat one place or one call differently (M4, the first
number skipped; M10, the fold's start, which every call adds once). P5,
with 10 and 100 appended, sees only M3, which counts lengths of 4 and not
of 2. The range arm is right only within the constraints, so P3
multiplies only the numbers below `10^4`, and the differential's numbers
stay within `10^5`.

## Benchmarks

The bench builds 200 arrays of 500 numbers, the constraints' longest,
each number's count of digits drawn first, once from its own generator,
then makes 500 passes; each sets one number of every array from the
checksum so far, so no answer carries over, answers it with the ★ arm and
folds the count plus the pass into the checksum. Every implementation
prints `500 passes over 200 arrays of 500: checksum 68246356`.

BENCHTAB
