# 2825. Make String a Subsequence Using Cyclic Increments

You are given two **0-indexed** strings `str1` and `str2`.

In an operation, you select a **set** of indices in `str1`, and for
each index `i` in the set, increment `str1[i]` to the next character
**cyclically**. That is `'a'` becomes `'b'`, `'b'` becomes `'c'`, and
so on, and `'z'` becomes `'a'`.

Return `true` *if it is possible to make* `str2` *a subsequence of*
`str1` *by performing the operation **at most once***, *and* `false`
*otherwise*.

**Note:** A subsequence of a string is a new string that is formed from
the original string by deleting some (possibly none) of the characters
without disturbing the relative positions of the remaining characters.

```
str1 = "abc", str2 = "ad"  ->  true
str1 = "zc",  str2 = "ad"  ->  true
str1 = "ab",  str2 = "d"   ->  false
```

**Constraints:** `1 <= str1.length <= 10^5`; `1 <= str2.length <=
10^5`; `str1` and `str2` consist of only lowercase English letters.

## Approaches

One operation may increment any set of indices, so each letter of str1
is free to stay or to move on by one; str2 is then matched greedily,
each letter of str1 taking str2's next letter when it can, which never
costs a later match.

| file | mechanism |
|---|---|
| `cyclic.kara` ★ | two pointers over the bytes, `b'z'` wrapped to `b'a'` by an `if` |
| `cyclic_chars.kara` | str2's `chars()` walked by a `peekable` iterator, each char of str1 consuming the char peeked when it is that char or its predecessor, the successor computed through `u32` arithmetic and `char.try_from` |
| `cyclic_jumps.kara` | a jump table built from the back, a `Vec` of `Array[i64, 26]` giving every position's next index of each letter; each letter of str2 jumps to the nearer of its own next occurrence and its predecessor's |
| `cyclic_find.kara` | one search a letter: `position` on the rest of str1's bytes for the letter or its predecessor, str1 resuming after it |
| `cyclic_solution.kara` | a Rust solution as LeetCode's Rust users write it: `as_bytes` on both `String`s, `for &c in s1`, and the increment as `(c - b'a' + 1) % 26 + b'a'` in `u8`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples; str2
longer than str1; 'z' to 'a'; 10^5 'z's under 10^5 'a's; 99999 'a's
under 10^5 'b's; 3000 random pairs of str1 of 1 to 10 letters and str2
of 1 to 5 from the four letters 'y' to 'b', and 50 of 10^4 letters with
str2 of up to 5000 from six, as counts and checksums. `cyclic.py`
mirrors the ★ arm and its output is byte-identical.

```
true
true
false
false
true
true
false
3000 short pairs: 1333 true, checksum 970205883
50 long pairs: 30 true, checksum 805291970
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every set of indices of str1 by a bit mask, each
incremented once, 'z' to 'a', and each result asked by a plain
subsequence test whether str2 is in it. It draws 2000 random pairs of
str1 of 1 to 10 letters and str2 of 1 to 5 from the four letters 'y'
to 'b', then 50 of up to 3000 letters with str2 of up to 1500 from six,
all before any arm answers; the literal reading is asked only of the
first 2000.

| | property |
|---|---|
| P1 | up to 10 letters, the answer is the literal reading's |
| P2 | true: str2 without its last letter is true too |
| P3 | every letter of both strings one further round the alphabet: the same answer |
| P4 | true: str1 with an 'a' put at the front, and with a 'z' at the end, is true too |
| P5 | str1 against itself, and against itself with every letter incremented: true |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, 900 true: checksum 519396955,
61500 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python reading of the same cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: 'z' never wrapped to 'a' | P1 131, P3 207, P5 1480, P6 132 |
| M2 | ★: only the incremented letter matched | P1 532, P5 2050, P6 543 |
| M3 | chars: the successor two letters on | P1 303, P5 2050, P6 304 |
| M4 | chars: str1 running out read as a failure even when str2 is done | P1 146, P5 2050, P6 146 |
| M5 | jumps: the predecessor's occurrence never tried | P1 337, P5 2050, P6 342 |
| M6 | jumps: the search resumed at the letter matched | P1 352, P6 357 |
| M7 | find: the predecessor of 'a' read as '`' | P1 131, P3 207, P5 1480, P6 132 |
| M8 | find: the rest of str1 started at the letter matched | P1 352, P6 357 |
| M9 | solution: or turned to and | P1 889, P5 2050, P6 900 |
| M10 | solution: j moved on every letter of str1 | P1 739, P6 762 |

## Benchmarks

The bench draws 100 pairs of str1 of 10^5 letters, LeetCode's most, and
str2 of up to 50000, from the six letters 'x' to 'c', all of them
first, then answers each 50 times by the ★ arm in all five languages.
Every implementation prints `100 pairs of 100000, 50 rounds: 2650
true, checksum 310942247`.

BENCHTAB

## Verification

All five arms print the same output as `cyclic.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

Three of the four own arms checked clean as first written. The chars
arm reached for Rust's `char.from_u32`, and `karac check` reported
E0236, no such function, naming `char.try_from(n).ok()` as the Option
it returns; `karac fix` wrote exactly that. It also warned W0278 on
`want.next();`, a discarded `Option`, which Kāra treats as
`#[must_use]` where Rust does not; `karac fix` offers no edit for it
by design (the repair depends on intent, `src/cli/diag_json.rs`), and
the arm writes `let _ = want.next();`, design.md's escape for a
deliberate discard.

LeetCode's Rust template took 8 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`;
`as_bytes()` became `bytes()`; `for &c in s1` lost its `&`; `||`
became `or`; `&str` became `Str` and `Solution::` took `.`.
