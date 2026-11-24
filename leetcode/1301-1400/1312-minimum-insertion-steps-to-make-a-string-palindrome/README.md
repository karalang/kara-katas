# 1312. Minimum Insertion Steps to Make a String Palindrome

Given a string `s`. In one step you can insert any character at any index
of the string.

Return the minimum number of steps to make `s` palindrome.

A **Palindrome String** is one that reads the same backward as well as
forward.

```
s = "zzazz"     ->  0
s = "mbadm"     ->  2
s = "leetcode"  ->  5
```

**Constraints:** `1 <= s.length <= 500`, `s` consists of lowercase
English letters.

The arms are `fn min_insertions(s: String) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `min_insertions.kara` ★ | the fewest insertions for every piece `s[i..=j]`, a matching pair of ends costing what the inside costs and a mismatch one more than the cheaper of dropping either end, kept in one row: the row for i made from the row for i + 1, read before it is overwritten. O(n^2) time, O(n) space |
| `min_insertions_table.kara` | the same interval costs, but every one kept in an n by n table filled by the length of the piece, shortest first. O(n^2) time and space |
| `min_insertions_lcs.kara` | the letters left alone form the longest palindrome inside the string, which is the longest common subsequence of the string and its reverse; every other letter needs a partner inserted. The common subsequence by the usual two-row table. O(n^2) time, O(n) space |
| `min_insertions_memo.kara` | top down: the cost of `s[i..=j]` asked of a recursive call, which looks at the two ends and asks for the inside, or for both one-end-shorter pieces, each answer remembered in a table so that it is worked out once. O(n^2) time and space, n calls deep |
| `min_insertions_solution.kara` | a Rust solution as LeetCode's Rust users write it (the bytes by `s.as_bytes()`, a `vec![vec![0; n]; n]` table filled `for len in 2..=n` and `for i in 0..=n - len`, a mismatch costing `1 + dp[i + 1][j].min(dp[i][j - 1])`, the answer `dp[0][n - 1] as i32`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, one
letter, two different letters, four different letters, each but one
needing a partner, and a palindrome with one letter taken out of one side
(`0 2 5 0 1 3 1`); then 600 random strings of 1 to 500 letters, the
constraints' longest, over 2, 4 or 26 letters, every other one a
palindrome with up to 20 letters taken out (`600 random strings:
insertions total 34891, checksum 557433160`). `min_insertions.py` mirrors
the ★ arm, and its output is byte-identical. Every arm gives the same
output under `karac __mir-run`, `karac run` and `karac __mir-llvm-run`.
Each arm takes 20 to 40 s under `karac __mir-run`, a quarter of a million
steps for each of the longest strings.

The Mend loop: the ★ and table arms checked clean as first written. The
other two Kāra arms took one fix each, both from `s.bytes()` being a
`Slice[u8]`, not a `Vec[u8]`: the subsequence arm's `let a: Vec[u8] =
s.bytes();` and the top-down arm's call passing it to a `Vec[u8]`
parameter. `karac fix` wrote `.to_vec()` in both places; for the call, the
diagnostic also offered a `Slice[u8]` parameter, which would take both
without the copy. The Rust arm takes one round of 6 fixes by `karac fix`'s
count, from 2 errors: `struct Solution;` to `struct Solution {}`, `::` to
`.`, then `s.as_bytes()` to `s.bytes()`, `vec![vec![0; n]; n]` to
`Vec.filled(n, Vec.filled(n, 0))`, and the wrapper's `as i64` dropped as a
widening. Its output matches on the first run. No gap was met.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every set of letters to leave alone tried, as a bit mask; when
they read the same both ways, each other letter can be matched by
inserting its twin at the mirror place, and nothing less will do, so the
answer is the letters outside the largest such set. 2000 strings of 1 to
12 letters in four kinds, 500 each: over 2 letters, over 3, and over all
26; and a palindrome over 3 letters with up to 3 letters taken out. Every
string, renaming and extra letter is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the string reversed: the same answer |
| P3 | the letters renamed one for one, each moved the same number of places round the alphabet: the same answer |
| P4 | one more letter at the end: an answer at most one away |
| P5 | one letter put at both ends: the same answer |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 strings: checksum 973646857,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Twelve edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. Two are left out: the table arm
never filling the whole string and the Rust arm skipping the last piece of
each length both answer 0 for every string, failing exactly the checks
the subsequence arm comparing the string with itself fails. The ten kept,
two to each arm, are each killed, fail the same way under both backends
and not by a crash, and no two fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the inside of a matching pair always free | P1 819, P4 105, P5 1042, P6 3276 |
| M2 | ★: a mismatch dropping the dearer end | P1 1031, P4 482, P6 4124 |
| M3 | table: two equal letters costing one | P1 630, P6 630 |
| M4 | table: a mismatch reading the inside, not the piece without its right end | P1 699, P2 287, P4 252, P6 699 |
| M5 | subsequence: the row being filled never read | P1 692, P2 784, P4 97, P5 581, P6 692 |
| M6 | subsequence: the string compared with itself, not its reverse | P1 1424, P6 1424 |
| M7 | top-down: a matching pair dropping only its left end | P1 938, P2 229, P4 8, P5 1380, P6 938 |
| M8 | top-down: a remembered cost handed back one too high | P1 225, P2 300, P4 261, P6 225 |
| M9 | solution: a mismatch always dropping its left end | P1 605, P2 789, P4 517, P6 605 |
| M10 | solution: a mismatch costing two | P1 1424, P4 1619, P6 1424 |

P1 and P6 kill all ten, P4 eight, P2 five and P5 three; P3 kills none.
No arm looks at which letter is which, only at whether two are equal, so
renaming them (P3) reaches no edit. One more letter at the end (P4) can
cost one insertion more or save one, and misses M6, which always answers
0, and M3. Reversing the string (P2) catches the edits that treat its two
ends differently: M4 and M9 on a mismatch, M7 on a matching pair, M5,
whose two rows no longer play the same part for the string and its
reverse, and M8, whose extra one lands on whichever pieces the recursion
meets a second time. Wrapping the string in one letter (P5) adds a
matching pair round everything, and catches M1 and M7, which mishandle a
matching pair, and M5.

## Benchmarks

The bench builds 20 strings of 500 letters, the constraints' longest,
over 2, 4 or 26 letters, once from its own generator; then makes 50
passes, each setting one letter of every string from the checksum so far,
so no answer carries over, answering it with the ★ arm and folding the
answer plus the pass into the checksum. Each call takes a fresh string
and a fresh row in every language, a `malloc` in C. Every implementation
prints `50 passes over 20 strings of 500: checksum 613983456`.

BENCHTAB
