# 1796. Second Largest Digit in a String

Given an alphanumeric string `s`, return the second largest digit that
appears in `s`, or `-1` if there is none. An alphanumeric string is made
of lowercase English letters and digits.

```
s = "dfa12321afd"  ->  2
s = "abc1111"      ->  -1
```

**Constraints:** `1 <= s.length <= 500`, and `s` holds only lowercase
English letters and digits.

The arms are `fn second_highest(s: String) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `second_highest.kara` ★ | one pass keeping the largest digit and the largest below it: a digit above the largest pushes the largest down to second, and one between the two becomes the second. O(n) |
| `second_highest_seen.kara` | the digits marked in an array of ten, then read from 9 down to the second one marked. O(n) |
| `second_highest_set.kara` | the digits gathered in a `SortedSet`, the largest popped from its end, and the next one popped is the answer. O(n) |
| `second_highest_sort.kara` | the digit bytes filtered out, sorted and deduplicated, and the one before the last taken. O(n log n) |
| `second_highest_solution.kara` | a Rust solution as LeetCode's Rust users write it (`filter_map(\|c\| c.to_digit(10))` into a `BTreeSet`, then `.iter().rev().nth(1)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`2 -1`); six
edges, one letter, no digit, one digit over and over, 0 and 9, every
digit, and the digits falling between letters (`-1 -1 -1 0 8 8`); the
constraints' most, 500 nines, a 9 then 499 eights, and 500 characters at
random (`the most: -1 8 8`); and 3000 random strings of 1 to 20
characters, each a digit with a chance of 0 to 9 in 10 (`3000 random
strings: checksum 694916957`). `second_highest.py` mirrors the ★ arm,
and its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★ and set arms and the harness check clean as first
written. The seen arm indexes its array with `seen[d as i64]`, and check
warns the cast is unnecessary, a `u32` widening to `i64` by itself;
`karac fix` removes it, 1 fix. The sort arm was first written with
Rust's `s.bytes().filter(..)`; check said `bytes()` gives a `Slice`,
whose adaptors need an explicit `.iter()`, and warned of an unnecessary
`as i32` on a `u8`; `karac fix` wrote `s.bytes().iter().filter(..)` and
removed the cast, 2 fixes. The Rust solution takes one round of 7 fixes
by `karac fix`'s count, and its diff is: the `use` line dropped, `struct
Solution;` to `struct Solution {}`, `BTreeSet<u32>` to `SortedSet[u32]`,
`|&d|` to `|d|`, and `Solution::` to `Solution.`. Every arm's output
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the largest digit of `s` that some other digit of `s` is
larger than. LeetCode's examples, eight edges, the constraints' most,
and 1987 random strings of 1 to 30 characters. Each arm meets six
properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | the string reversed gives the same answer |
| P3 | the letters removed give the same answer, while a digit is left |
| P4 | the string twice over gives the same answer |
| P5 | a digit one above the largest, appended, makes the largest the answer, while the largest is below 9 |
| P6 | the ★ arm's answer |

The differential was first written with `let top =
digits_of(s).iter().max().unwrap_or(-1);`, and check refused it: `top`
keeps a reference into the `Vec` that `digits_of` returns, a temporary
dropped at the `;`. `karac fix` bound the temporary first, `let top_src
= digits_of(s);`, 2 fixes. All 54,075 checks pass on every arm: `2000
cases: checksum 436922698, 54075 checks over 5 arms: 0 failures`, under
`karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, running the ★ arm's mirror over the same cases,
gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a digit equal to the largest taken as the second | P1 603, P4 1112, P6 2412 |
| M2 | ★: the old largest never pushed down to second | P1 511, P2 1082, P4 511, P5 815, P6 2044 |
| M3 | seen: the first digit marked from 9 down returned | P1 1715, P5 1100, P6 1715 |
| M4 | seen: the digits read from 0 up | P1 1347, P5 658, P6 1347 |
| M5 | set: the largest never popped first | P1 1715, P5 1100, P6 1715 |
| M6 | set: the smallest taken after the largest is popped | P1 1350, P5 665, P6 1350 |
| M7 | sort: the digits never deduplicated | P1 603, P4 1112, P6 603 |
| M8 | sort: every 9 left out | P1 882, P5 331, P6 882 |
| M9 | solution: the largest taken | P1 1715, P5 1100, P6 1715 |
| M10 | solution: the digits read from the smallest up | P1 1347, P5 658, P6 1347 |

## Benchmarks

The bench builds 1000 random strings of 100 characters once, each a
digit with a chance of 1 to 9 in 10, and makes 1000000 calls of the ★
arm, each string drawn from the checksum so far. Kāra, Rust and Go walk
the characters, and C walks the bytes; every string is ASCII. It checks
clean as first written. Every implementation prints `1000000 calls over
1000 strings: checksum 461216015`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.56 s against Rust's 0.43 s (0.43 s with overflow checks
on), C's 0.41 s and Go's 0.60 s; Python takes 8.1 s.
