# 1745. Palindrome Partitioning IV

Given a string `s`, return `true` *if it is possible to split the string*
`s` *into three **non-empty** palindromic substrings. Otherwise, return*
`false`.

A string is said to be palindrome if it the same string when reversed.

```
s = "abcbdd"   ->  true     "a" + "bcb" + "dd"
s = "bcbddxy"  ->  false
```

**Constraints:** `3 <= s.length <= 2000`; `s` consists only of lowercase
English letters.

## Approaches

| file | mechanism |
|---|---|
| `palin.kara` ★ | `is[i][j]` says whether `s[i..=j]` is a palindrome: its ends match and the inside, two shorter, is one; filling from the last row up makes the inside's entry ready when it is read. Then every pair of cuts is tried. O(n^2) |
| `palin_expand.kara` | every palindrome grows out from a centre, a letter or a gap, one matching pair at a time; growing each of the 2n - 1 centres until its ends differ marks the table. The cuts are tried with nested `any`. O(n^2) |
| `palin_memo.kara` | whether a range is a palindrome is worked out only when a cut needs it, recursively from its ends inwards, and kept in a `Vec[Vec[Option[bool]]]` memo. O(n^2) |
| `palin_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `vec![vec![false; n]; n]` table over `s.as_bytes()` filled from the last row up, then every pair of cuts with `!dp[0][i - 1]` skipping a first piece that is not one, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's two examples, then three
letters, four of one letter, a palindrome of five with a letter after
it, and 19 letters with no split; then how many strings split and a
checksum for 3000 random strings of up to 10 letters from 2, 1000 of up
to 40 from 3, and 20 of up to 2000, LeetCode's limit, from all 26. Half
of each batch is three random palindromes put together and half random
letters. `palin.py` mirrors the ★ arm and its output is byte-identical.

```
true
false
true
true
false
false
3000 strings of up to 10 letters from 2: 2912 split, checksum 486592630
1000 strings of up to 40 letters from 3: 572 split, checksum 181545620
20 strings of up to 2000 letters from 26: 10 split, checksum 30062948
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every way to cut the string into three non-empty pieces, each
piece compared with itself reversed. It checks 3000 random strings of 3
to 11 letters from the first 1 to 3 letters of the alphabet. Every case
is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the string reversed gives the same answer |
| P3 | the letters renamed one for one give the same answer |
| P4 | the first letter three times can always be split |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 952032623, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading, every pair of cuts with each piece compared with its reverse,
gives the same checksum. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: two matching letters not counted a palindrome without the inside | P1 1234, P5 1234 |
| M2 | ★: the first piece at least two letters | P1 662, P2 432, P4 3000, P5 662 |
| M3 | ★: the middle or the last piece a palindrome, not both | P1 466, P5 466 |
| M4 | expand: only the centres on a letter grown | P1 1234, P5 1234 |
| M5 | expand: growth stopped once the left end reaches the second letter | P1 225, P2 295, P5 225 |
| M6 | expand: the first piece at least two letters | P1 662, P2 432, P4 3000, P5 662 |
| M7 | memo: every two-letter range taken as a palindrome | P1 363, P5 363 |
| M8 | memo: every range worked out kept as a palindrome | P1 314, P2 89, P5 314 |
| M9 | solution: the test on the first piece reversed | P1 1906, P2 259, P4 3000, P5 1906 |
| M10 | solution: the middle piece at least two letters | P1 652, P4 3000, P5 652 |

## Benchmarks

The bench draws 20 random strings of 2000 letters, LeetCode's longest,
from `a` and `b`, half of them three random palindromes put together,
all of them first, then answers each 5 times by the ★ arm in all five
languages; each answer fills its `2000 * 2000` table anew. Kāra, Rust and
Go keep the table as a vector of rows, C as one block. Every
implementation prints `20 strings of 2000 letters, 5 rounds: 50 split,
checksum 551750626`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `21cdf88b69` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.200 s |
| Kāra (`karac build`) | 0.245 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.271 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.389 s |
| Rust (`rustc -O`) | 0.432 s |
| Go | 0.511 s |
| Python | 17 s |

The sequential Kāra build is 37% faster than Rust and 30% faster than Rust with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C is the fastest here at 0.200 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.257 s and
0.262 s on one run).

## Verification

All four arms print the same output as `palin.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★ arm was first written `let b = s.bytes().collect::[Vec[u8]]()`,
Rust's turbofish in Kāra's brackets, and took one `karac fix`: the type
moved to the binding, `let b: Vec[u8] = ..`, and an `.iter()` went in
before `collect`, since `bytes()` is a `Slice`, not an iterator. The
centre and memo arms took the same `.iter()` from one `karac fix` each.

LeetCode's Rust template took one `karac fix` of 8 edits: `struct
Solution {}` added, `s.as_bytes()` written `s.bytes()`, `vec![vec![false;
n]; n]` written `Vec.filled(n, Vec.filled(n, false))`, `&&` and `||`
written `and` and `or`, and `!` written `not`. The `(0..n).rev()` fill
and the `continue` carried over as written.

The bench first passed `s.clone()` to the borrowing parameter, and one
`karac fix` passed `s`. The differential checked clean as generated.
