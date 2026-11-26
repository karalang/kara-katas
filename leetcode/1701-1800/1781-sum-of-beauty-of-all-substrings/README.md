# 1781. Sum of Beauty of All Substrings

The beauty of a string is the difference in frequencies between the most
frequent and least frequent characters. For example, the beauty of
`"abaacc"` is `3 - 1 = 2`. Given a string `s`, return the sum of beauty
of all of its substrings.

```
s = "aabcb"    ->  5
s = "aabcbaa"  ->  17
```

**Constraints:** `1 <= s.length <= 500`, and `s` consists of only
lowercase English letters.

The arms are `fn beauty_sum(s: String) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `beauty_sum.kara` ★ | from each start, the letters' counts in a 26-slot array grown one letter at a time, and each substring's most and fewest counts read off the 26. O(26 n^2) |
| `beauty_sum_iter.kara` | the counts grown from each start over the string's bytes, the counts above 0 collected, and `max` and `min` over them. O(26 n^2) |
| `beauty_sum_prefix.kara` | a table of prefix counts, one row per letter, so that each substring's count of a letter is a difference of two entries. O(26 n^2) |
| `beauty_sum_buckets.kara` | how many letters have each count, kept as the substring grows, so that the most only rises and the fewest moves only when its own count empties or a new letter comes. O(n^2) |
| `beauty_sum_solution.kara` | a Rust solution as LeetCode's Rust users write it (`s.as_bytes()`, `[0; 26]`, `b'a'`, `filter(\|&&x\| x > 0)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`5 17`);
five edges, one letter, one letter repeated, every letter once, two
letters alternating, and one letter far more often than another (`0 0 0
12 10`); the constraints' most, 500 letters at random from all 26, 500
from two, and 500 of one (`the most: 1106465 1089778 0`); and 3000
random cases of 1 to 20 letters from the first 1 to 6 (`3000 random
cases: checksum 567276161`). `beauty_sum.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the buckets arm checks clean as first written. The ★ arm
was first written with `let mut total = 0`, `[0; 26]` and `let mut most
= 0`, and `karac fix` wrote `total: i32`, `[0i32; 26]` and `most: i32`,
since an operator or a method does not fix a literal's type (design.md
§8 Literals), 3 fixes. That left `total += most - fewest` an `i64` going
into the `i32` total, because `fewest` starts at `n`, the string's
length, an `i64`; check has no machine fix for a narrowing, and asks for
an explicit `as i32`, written by hand as `(most - fewest) as i32`. A
second `karac fix` then dropped the index's `as i64`, which the
`lossless_cast` lint found widening implicitly, 1 fix. The iter arm was
first written with Rust's `s.as_bytes()`; check named Kāra's
`s.bytes()`, and `karac fix` wrote it, with `total: i32` and the index's
`as i64` dropped, 3 fixes. The prefix arm took `here: i32`, `total: i32`
and `most: i32`, 3 fixes. The Rust solution takes one round of 4 fixes
by `karac fix`'s count, and its diff is: `struct Solution;` to `struct
Solution {}`, `s.as_bytes()` to `s.bytes()`, `filter(|&&x| x > 0)` to
`filter(|x| x > 0)`, since a Kāra pattern already matches through a
reference, and `Solution::` to `Solution.`. Its `[0; 26]`, `b'a'` and
`as usize` stay. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every substring, each of its letters counted on its own with
a `filter` over the substring, and the most frequent count less the
least, summed. LeetCode's examples, six edges, and 1992 random words of
1 to 12 letters from the first 1 to 5 of the alphabet. Each arm meets
six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | 0 for one letter repeated, and never more than the sum over substrings of each one's length less 2 |
| P3 | the string reversed gives the same sum |
| P4 | the letters rotated one on in the alphabet give the same sum |
| P5 | one more letter at the end never lowers the sum |
| P6 | the ★ arm's answer |

The literal reading was first written with `letters.slice(i, j)`; check
named the range index `letters[i..j]`, and `karac fix` wrote it, 1 fix.
All 60,000 checks pass on every arm: `2000 cases: checksum 725378950,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, counting every
substring's letters, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: absent letters counted, so the fewest is 0 | P1 2000, P2 1696, P6 8000 |
| M2 | ★: each start's own letter left out of its substrings | P1 1283, P3 926, P6 5132 |
| M3 | iter: absent letters' counts of 0 kept | P1 2000, P2 1696, P6 2000 |
| M4 | iter: the fewest taken to be 1 | P1 1585, P2 630, P6 1585 |
| M5 | prefix: every letter, present or not, counted one more | P1 2000, P2 1696, P6 2000 |
| M6 | prefix: each letter counted twice | P1 1283, P2 446, P6 1283 |
| M7 | buckets: the fewest moved up while other letters keep its count | P1 1225, P3 1106, P6 1225 |
| M8 | buckets: a letter's new count never recorded | P1 1585, P2 630, P6 1585 |
| M9 | solution: the last letter never ends a substring | P1 1283, P3 926, P6 1283 |
| M10 | solution: a count set to 1 rather than raised | P1 1283, P6 1283 |

## Benchmarks

The bench builds 48 strings of 500 letters once, from the first 2 to 24
letters of the alphabet, and sums the beauty of each with the ★ arm.
Every implementation prints `48 strings of 500 letters: checksum
941896430`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.19 s against Rust's 0.09 s (0.09 s with overflow checks
on), C's 0.16 s and Go's 0.14 s; Python takes 9.4 s.
