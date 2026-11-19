# 1641. Count Sorted Vowel Strings

Given an integer `n`, return *the number of strings of length* `n` *that
consist only of vowels (`a`, `e`, `i`, `o`, `u`) and are
**lexicographically sorted**.*

A string `s` is **lexicographically sorted** if for all valid `i`,
`s[i]` is the same as or comes before `s[i+1]` in the alphabet.

```
n = 1    ->  5
n = 2    ->  15
n = 33   ->  66045
```

**Constraints:** `1 <= n <= 50`.

## Approaches

| file | mechanism |
|---|---|
| `vowels.kara` ★ | build the strings a letter at a time, keeping in an `Array[i64, 5]` how many sorted strings end in each vowel; a string can end in vowel v after any that ends in a vowel up to v, so the next counts are the running sums. O(5n) |
| `vowels_formula.kara` | the closed form: a sorted string is fixed by how many of each vowel it holds, five counts summing to n, and stars and bars counts those as C(n + 4, 4) = (n + 1)(n + 2)(n + 3)(n + 4) / 24. O(1) |
| `vowels_build.kara` | every string written out letter by letter, each no earlier than the one before, with a `Map[(i64, i64), i64]` memo on (letters left, smallest vowel allowed). O(25n) |
| `vowels_solution.kara` | LeetCode's Rust template: a table `dp[i][j]` of the strings of length i that start with vowel j or later. Carried by `karac fix` |
| `differential.kara` | the four arms on every n of the constraints, six properties |

Every arm prints the same 5 lines: LeetCode's three examples, then the
counts for every n from 1 to 50 summed (3478760, which is C(55, 5) - 1)
with a checksum, and n = 50 (316251). `vowels.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on every
n from 1 to 50. The statement read literally lists all 5^n strings as
base-5 numbers and counts the sorted ones, which is quick enough for n up
to 7.

| | property |
|---|---|
| P1 | the count is the statement read literally (n up to 7) |
| P2 | one letter more gives more strings |
| P3 | the count times n is the count for n - 1 times n + 4, as C(n + 4, 4) and C(n + 3, 4) stand |
| P4 | the count is the sum, over the vowel a string starts with, of the sorted strings of n - 1 letters over that vowel and the later ones, each listed literally (n up to 7) |
| P5 | the count is at least n + 1 and, for n up to 20, at most 5^n |
| P6 | each arm agrees with at least two of the other three |

The differential prints `50 problems: checksum 901492173, 1200 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. A formula off by one at n = 50 alone
(M4) is caught by only two checks: P3, which compares each n with the
one before, and P6. Building every letter from the first vowel (M7)
counts all 5^n strings and stops with Kāra's integer overflow check
once 5^n passes the `i64` range. The first M8 tried, the memo storing every answer under the
smallest vowel 0, survived and is equivalent: each (letters left, 0)
state is reached exactly once, down the chain of first vowels, so a
stale entry is never read. It was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the second vowel never takes the first's count | P1 6, P3 49, P4 6, P6 49 |
| M2 | ★: one letter too many | P1 7, P3 49, P4 7, P5 2, P6 50 |
| M3 | ★: a vowel's count only the one before plus one | P1 5, P2 48, P3 48, P4 5, P5 36, P6 48 |
| M4 | formula: one more at n = 50 | P3 1, P6 1 |
| M5 | formula: C(n + 3, 3), four vowels' worth | P1 7, P3 49, P4 7, P6 50 |
| M6 | build: each letter strictly after the one before | P1 7, P2 48, P3 4, P4 7, P5 47, P6 50 |
| M7 | build: the smallest vowel allowed never moves on | panics on both backends: integer overflow |
| M8 | build: each answer stored one letter short | P1 4, P3 47, P4 4, P6 47 |
| M9 | template: one string too few for each first vowel at one letter | P1 7, P3 49, P4 7, P6 50 |
| M10 | template: each row built from the next vowel's column | P1 6, P2 48, P3 5, P4 6, P5 46, P6 49 |

## Benchmarks

The bench draws 4000000 random n from 1 to 50, all of them first, then
counts each by the ★ arm in all five languages, five counters and up to
49 rounds of running sums per n. Every implementation prints `4000000
random n: counts sum to 277942583297, checksum 553624529`. The C build
also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

TIMINGS

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. PARNOTE

## Verification

All four arms print the same output as `vowels.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `SHA`.

## Writing it

The ★, formula and build arms checked clean as first written: the
`[1; 5]` array summed with `ending.iter().sum()`, and the build arm's
tuple-keyed memo.

LeetCode's Rust template takes one `karac fix` of 4 edits:
`n as usize` to `n as i64`, `vec![[0i32; 6]; n + 1]` to
`Vec.filled(n + 1, [0i32; 6])`, `Solution::` to `Solution.`, and the
harness wrapper's `as i64` dropped as lossless. The arm then checks and
agrees with no hand edit.
