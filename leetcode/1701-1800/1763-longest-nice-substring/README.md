# 1763. Longest Nice Substring

A string `s` is nice if, for every letter of the alphabet that `s`
contains, it appears both in uppercase and lowercase. For example,
`"abABB"` is nice because `'A'` and `'a'` appear, and `'B'` and `'b'`
appear. However, `"abA"` is not because `'b'` appears, but `'B'` does
not. Given a string `s`, return the longest substring of `s` that is
nice. If there are multiple, return the substring of the earliest
occurrence. If there are none, return an empty string.

```
s = "YazaAay"  ->  "aAa"
s = "Bb"       ->  "Bb"
s = "c"        ->  ""
s = "dDzeE"    ->  "dD"
```

**Constraints:** `1 <= s.length <= 100` and `s` consists of uppercase
and lowercase English letters.

The arms are `fn longest_nice_substring(s: String) -> String`.

## Approaches

| file | mechanism |
|---|---|
| `longest_nice_substring.kara` ★ | divide and conquer: a letter whose other case is missing from the string can be in no nice substring, so the string splits there and the longer of the two parts' answers wins, the earlier on a tie. O(n^2) |
| `longest_nice_substring_brute.kara` | every substring tried, longest first and earliest first within a length, each checked letter by letter with `contains` for its other case. O(n^3) |
| `longest_nice_substring_masks.kara` | for each start, the substring grown a letter at a time with a `u32` mask of the lowercase letters seen and one of the capitals; nice when the masks are equal. O(n^2) |
| `longest_nice_substring_window.kara` | a sliding window for each number `k` of distinct letters, 1 to 26, holding at most `k` letters, nice when all `k` appear in both cases. O(26 n) |
| `longest_nice_substring_solution.kara` | a Rust solution as LeetCode's Rust users write it (`Vec<char>`, `&chars[i..j]`, `sub.contains(&c.to_ascii_lowercase())`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's four examples (`"aAa" "Bb"
"" "dD"`); five edges, no letter with its pair, the whole string nice,
two nice halves split by a letter alone with the first kept on the tie,
a nice stretch at the end, and a pair far apart (`"" "aAbBcC" "aA" "Ee"
""`); the constraints' most, 100 letters from 3 letters, from 26, and
every letter beside its pair, as lengths (`100 letters: 100 2 100`); and
3000 random strings of 1 to 30 letters, each answer's length and place
(`3000 random strings: checksum 184176814`). `longest_nice_substring.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`.

The Mend loop: the ★ and brute arms check clean as first written. The
masks and window arms were first written with Rust's `let (mut a, mut b)
= ..`, and `karac fix` moved the `mut` before the pattern, in 6 fixes
for the masks arm's two lines and 7 for the window arm's two. The Rust
solution takes one round of 10 fixes by `karac fix`'s count, and its
diff is: `struct Solution;` to `struct Solution {}`, `Vec<char>` to
`Vec[char]`, `String::new()` to `String.new()`, `&chars[i..j]` to
`chars[i..j]`, the two `&` before `contains`'s arguments dropped, `&&`
to `and` twice, and `Solution::` to `Solution.`. Every arm's output
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every substring, nice when the `Set` of its lowercase letters
equals the `Set` of its capitals lowered, and the longest, the earliest
among the longest. LeetCode's examples, the edges, and 1991 random
strings of 1 to 14 letters from the first 1 to 5 of the alphabet, a
capital with a chance drawn for the string. Each arm meets six
properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | the answer is nice and a substring of `s` |
| P3 | every case swapped gives the answer with its cases swapped |
| P4 | each letter moved one on in the alphabet, `z` to `a`, gives an answer as long at the same place |
| P5 | a `z` at the end, which no case has as a capital, changes nothing |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 cases: checksum 351500421,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, reading every
substring, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the later part kept on a tie | P1 27, P6 108 |
| M2 | ★: each letter looked for in place of its other case | P1 1541, P2 1541, P5 2000, P6 6164 |
| M3 | brute: no substring of two letters tried | P1 232, P6 232 |
| M4 | brute: the latest start tried first | P1 27, P6 27 |
| M5 | masks: the later substring kept on a tie | P1 27, P6 27 |
| M6 | masks: lowercase letters merged in pairs | P1 823, P2 561, P3 828, P4 821, P6 823 |
| M7 | window: windows of one distinct letter never tried | P1 671, P6 671 |
| M8 | window: the later window kept on a tie | P1 27, P6 27 |
| M9 | solution: the later substring kept on a tie | P1 27, P6 27 |
| M10 | solution: no substring reaching the end | P1 580, P5 580, P6 580 |

## Benchmarks

The bench builds 1000 strings of 100 letters once, each from its own
number of letters, 1 to 12, and chance of a capital, and makes 500000
calls of the ★ arm, each on a string chosen from the checksum so far.
Each part of a split is a new string in every implementation, as the
Kāra arm's `s[..i].to_string()` makes one. Every implementation prints
`500000 calls over 1000 strings: checksum 685164114`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 1.5 s against Rust's 2.1 s (2.1 s with
overflow checks on), C's 2.0 s and Go's 1.7 s; Python takes 10.7 s.
