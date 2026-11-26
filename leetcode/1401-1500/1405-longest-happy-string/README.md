# 1405. Longest Happy String

A string `s` is called happy if it satisfies the following conditions:

`s` only contains the letters `'a'`, `'b'`, and `'c'`. `s` does not
contain any of `"aaa"`, `"bbb"`, or `"ccc"` as a substring. `s` contains
at most `a` occurrences of the letter `'a'`, at most `b` occurrences of
the letter `'b'`, and at most `c` occurrences of the letter `'c'`.

Given three integers `a`, `b`, and `c`, return the longest possible
happy string. If there are multiple longest happy strings, return any of
them. If there is no such string, return the empty string `""`.

```
a = 1, b = 1, c = 7  ->  "ccaccbcc"   "ccbccacc" is also correct
a = 7, b = 1, c = 0  ->  "aabaa"
```

**Constraints:** `0 <= a, b, c <= 100`, `a + b + c > 0`.

Each arm is `fn longest_diverse_string(a: i32, b: i32, c: i32) ->
String`. Any longest happy string is an answer, so the arms need not
agree on the string; they agree on its length, and every answer is
checked happy.

## Approaches

| file | mechanism |
|---|---|
| `longest_diverse_string.kara` ★ | greedy: the three letters with what is left of each, sorted by `sort_by` with the most left first before every letter placed, and the first that would not make three in a row, by `ends_with(f"{ch}{ch}")`, goes next; it stops when none can. O(a + b + c) |
| `longest_diverse_string_pick.kara` | the same greedy as a choice: the letter barred, if the last two letters are alike, and of the rest with any left the one with the most, by `filter(..).max_by_key(..)` over the indices, into a `Vec[char]` collected at the end. O(a + b + c) |
| `longest_diverse_string_heap.kara` | a `PriorityQueue.max_first()` of (left, letter): the most left is popped, and when it would make three in a row the next is placed instead and both go back. O((a + b + c) log 3) |
| `longest_diverse_string_recursive.kara` | recursion on the counts kept in order, the most first: up to two of the most, then one of the second if the most is not ahead by more than the second can keep up with, and the rest recursively, built by `repeat` and `+`. O(a + b + c) |
| `longest_diverse_string_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `BinaryHeap` of (count, letter) pairs, the barred letter put back behind the next, into a `Vec<char>` collected at the end), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: the lengths for LeetCode's two
examples and four more (`8 5 5 1 2 9`); the lengths at the constraints'
corners, all 100, one letter alone, one beside two 1s and beside 10, and
49 beside 100 (`corners: 300 2 2 8 32 149`); and every count from 0 to
12 each with 2000 drawn up to 100, the letters in all, a checksum of the
lengths and how many answers are not happy (`4196 cases: 333623 letters
in all, checksum 551842766, 0 not happy`). `longest_diverse_string.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`.

The Mend loop: the ★, pick and heap arms check clean as first written.
The recursive arm's `let second = if a - most >= b { 1 } else { 0 };` is
a join of literals, which stays open as a bare literal does (design.md
§8 Literals) and ends up an `i64`, the type `repeat(second)` takes;
`b - second` then passes an `i64` where an `i32` is wanted, so check
names `second: i32` and `karac fix` writes it, 1 fix. The Rust solution
takes one round of 10 fixes by `karac fix`'s count: the `use
std::collections::BinaryHeap;` line deleted, `struct Solution;` to
`struct Solution {}`, `BinaryHeap::new()` to
`PriorityQueue.max_first()`, the queue that pops the largest first as
Rust's `BinaryHeap` does, `Vec<char>` to `Vec[char]`, `Vec::new` to
`Vec.new`, `&&` to `and`, and `Solution::` to `Solution.`. Its output
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the longest string of `'a'`, `'b'` and `'c'` within the
counts with no three alike in a row, every way of going on tried,
memoized on what is left of each letter, the last letter and how many of
it end the string, for counts up to 10. LeetCode's examples and ten edge
cases (one letter alone, two alike, all equal, the constraints' corners)
and 1991 random counts, up to 10 each two times in three and else up to
100. The checksum folds the ★ arm's strings.

| | property |
|---|---|
| P1 | the length the statement read literally gives, every count up to 10 |
| P2 | happy: only `'a'`, `'b'` and `'c'`, no three alike in a row, no more of each than given |
| P3 | the letters' names do not matter: the counts turned round, (c, a, b), give a string as long |
| P4 | the length in closed form: with x >= y >= z the counts in order, the most common letter fits two to each of the y + z + 1 gaps the others leave, so min(x, 2(y + z + 1)) + y + z |
| P5 | one more `'a'` never makes it shorter |
| P6 | as long as the ★ arm's answer |

All 56,710 checks pass on every arm (P1 and P5 apply to some cases
only): `2003 cases: checksum 952823830, 56710 checks over 5 arms: 0
failures`, under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. Python, by the mirror of the ★ arm, gives the
same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: sorted with the fewest left first | P1 1335, P4 2003, P6 8012 |
| M2 | ★: only a fourth alike in a row barred, so three are let through | P1 108, P2 1488, P4 183, P6 732 |
| M3 | pick: no letter barred | P1 108, P2 1361, P4 183, P6 183 |
| M4 | pick: the letter with the fewest left picked, by `min_by_key` | P1 1282, P4 1948, P6 1948 |
| M5 | heap: the letter that waits a turn not put back | P1 708, P3 248, P4 1336, P5 112, P6 1336 |
| M6 | heap: a letter with two left dropped once one of them is placed | P1 1217, P3 72, P4 1810, P5 9, P6 1810 |
| M7 | recursive: one of the most common letter at a time, not up to two | P1 317, P4 619, P6 619 |
| M8 | recursive: the second letter placed only when the most is ahead by more than it, not as much | P2 1243 |
| M9 | solution: the barred letter pushed in place of the next | P1 708, P2 1336, P3 179, P4 1336, P5 75, P6 1336 |
| M10 | solution: the barred letter not put back | P1 708, P3 248, P4 1336, P5 112, P6 1336 |

M8 is caught by P2 alone: its strings are as long as they should be, but
some hold three alike in a row. M5 and M10 are the same edit to the two
heap arms and fail the same checks.

## Benchmarks

The bench runs the ★ arm on 20000 counts drawn up to 100 each, and folds
every letter of every answer into the checksum. Every implementation
prints `20000 strings of up to 300 letters: checksum 89173493`.

BENCHTAB
