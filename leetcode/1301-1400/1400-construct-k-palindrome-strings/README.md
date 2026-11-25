# 1400. Construct K Palindrome Strings

Given a string `s` and an integer `k`, return `true` if you can use all
the characters in `s` to construct non-empty `k` palindrome strings or
`false` otherwise.

```
s = "annabelle", k = 2  ->  true     "anna" + "elble"
s = "leetcode", k = 3   ->  false
s = "true", k = 4       ->  true     each letter its own palindrome
```

**Constraints:** `1 <= s.length <= 10^5`, `s` consists of lowercase
English letters, and `1 <= k <= 10^5`.

Each arm is `fn can_construct(s: String, k: i32) -> bool`. A palindrome
holds at most one letter an odd number of times, its middle, and letters
in pairs can go to any palindrome, so k palindromes can be made exactly
when s has at least k letters and at most k letters that appear an odd
number of times.

## Approaches

| file | mechanism |
|---|---|
| `can_construct.kara` ★ | the length checked first, then the letters counted in a `Vec` of 26 indexed by `b - b'a'` over `bytes()`, and the odd counts found by `filter(..).count()`. O(n) |
| `can_construct_map.kara` | the letters counted in a `Map[char, i64]` over `chars()`, and the odd counts among its values |
| `can_construct_bits.kara` | only each count's parity matters, so one bit a letter in a `u32`, flipped with `^=`, and the odd letters are its set bits, counted by `count_ones()` |
| `can_construct_sorted.kara` | the letters sorted so each letter is a run, and the runs of odd length counted. O(n log n) |
| `can_construct_solution.kara` | a Rust solution as LeetCode's Rust users write it (`s.len() < k as usize` first, a `[0; 26]` array indexed by `(c as u8 - b'a') as usize`, and the odd counts by `filter(\|&&x\| x % 2 == 1).count()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples, more
palindromes than letters, one letter, and the alphabet as 26 palindromes
(`true false true false true true`); the constraints' most, 10^5 letters
from the whole alphabet and from 3 letters against k from 1 to 30, and k
= 10^5 and 10^5 + 1 (`10^5 letters: 46 of 60 true, true false`); and
2000 random cases of 1 to 20 letters from the first 1 to 26, k from 1 to
25 (`2000 random cases: 558 true, checksum 93600154`).
`can_construct.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run`,
`karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, map, bits and sorted arms check clean as first
written; an `i32` k compares with an `i64` length or a `u32` count of
bits as it is, since both widen. The Rust solution takes one round of 18
fixes by `karac fix`'s count, and its output matches on the first run:
`struct Solution;` to `struct Solution {}`, the `as usize` dropped from
`s.len() < k as usize` and `odd <= k as usize`, since lengths and counts
are `i64` in Kāra and `usize` is for FFI (design.md §5), `c as u8` to `c
as u32 as u8`, since a `char` does not fit 8 bits and Rust's `as u8`
truncates (B-2026-11-09-18), the `&&` dropped from `|&&x|`, and
`Solution::` to `Solution.`. The index keeps its `as usize`: check names
it for dropping only while the program mixes `usize` with `i64`
(B-2026-11-08-49), and that round's other fixes end the mixing, while
its own edit, on the same span as the `char` cast's, waits for a second
round that check, now clean, never asks for.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every split of the letters into k non-empty groups tried,
each once, until one whose every group has at most one letter an odd
number of times, which is the groups that can be laid out as
palindromes. LeetCode's three examples and 2000 random cases of 1 to 8
letters from the first 1 to 5, k from 1 to 9. Every case is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the letters read backwards: the same |
| P3 | k palindromes that can be made leave k + 1 possible while there are letters enough, since one can split off its middle or its ends |
| P4 | two more of the first letter, which can wrap any palindrome, change nothing while there are k letters already |
| P5 | every letter its own palindrome: k = n can be made, and k = n + 1 cannot |
| P6 | the ★ arm's answer |

All 60,090 checks pass on every arm: `2003 cases: checksum 516357626,
60090 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, trying the same
splits, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: k palindromes refused when there are exactly k letters | P1 251, P3 161, P4 251, P5 2003, P6 1004 |
| M2 | ★: the odd letters held to fewer than k | P1 161, P5 478, P6 644 |
| M3 | map: the length never checked | P1 992, P5 2003, P6 992 |
| M4 | map: the even counts counted, not the odd | P1 146, P6 146 |
| M5 | bits: each letter's bit set, not flipped | P1 116, P6 116 |
| M6 | bits: one odd letter more than k allowed | P1 93, P6 93 |
| M7 | sorted: the letters not sorted, so a letter's runs are counted apart | P1 178, P6 178 |
| M8 | sorted: the first letter of each next run skipped | P1 114, P4 6, P6 114 |
| M9 | solution: each letter's count set to 1, not counted up | P1 116, P6 116 |
| M10 | solution: one letter fewer than k allowed | P1 215, P5 2003, P6 215 |

P1 and P6 kill all ten, P5 four, P4 two, P3 one, and P2 none: every arm
counts letters, so no edit sees their order. The edits to the length
check (M1, M3, M10) fail at k = n or k = n + 1 (P5) in every case. The
edits that miscount the odd letters (M4 to M9) keep the length check
right, so only the literal reading and the ★ arm catch them; two more of
a letter (P4) catch M8 only, whose skipped letter can be the one added.
Growing k by one (P3) catches M1, which refuses k = n after allowing k =
n - 1.

## Benchmarks

The bench runs the ★ arm on 10^5 letters drawn from the whole alphabet,
one letter and k changed, at places drawn from the checksum so far,
before each of 3000 rounds, so each round counts 10^5 letters. Every
implementation prints `3000 rounds over 10^5 letters: checksum
733427516`. Each round makes a fresh `String` from the letters, as
`String.from_utf8` does in Kāra and Rust, a `string` conversion in Go
and a copy in C.

BENCHTAB
