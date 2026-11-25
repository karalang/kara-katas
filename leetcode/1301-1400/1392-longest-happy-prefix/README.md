# 1392. Longest Happy Prefix

A string is called a happy prefix if it is a non-empty prefix which is
also a suffix (excluding itself).

Given a string `s`, return the longest happy prefix of `s`. Return an
empty string `""` if no such prefix exists.

```
s = "level"   ->  "l"
s = "ababab"  ->  "abab"
```

**Constraints:** `1 <= s.length <= 10^5` and `s` contains only lowercase
English letters.

Each arm is `fn longest_prefix(s: String) -> String`. The letters are
ASCII, so a byte offset is a letter's place, and every arm that works on
`s.bytes()` slices `s` at the offset it finds.

## Approaches

| file | mechanism |
|---|---|
| `longest_prefix.kara` ★ | the prefix function, Knuth, Morris and Pratt's failure table, over the bytes: each entry the longest border of the prefix ending there, found by falling back along the borders of the entry before; the answer is the whole string's border. O(n) |
| `longest_prefix_hash.kara` | rolling hashes modulo 10^9 + 7: the hash of the prefix of each length grown at its end, the hash of the suffix of the same length grown at its front, and the lengths whose hashes agree kept; the longest of them whose prefix and suffix are really equal, compared as `Str` views, is the answer. O(n) unless hashes collide |
| `longest_prefix_z.kara` | the Z-function: for each place, the longest prefix that starts there, found inside a window already matched; the first place whose match runs to the end starts the longest border. O(n) |
| `longest_prefix_plain.kara` | the statement tried directly: each length from the longest down, `s.starts_with(s[n - len..])`, and the first that holds returned. O(n^2) at worst, as for `"aaa...ab"` |
| `longest_prefix_solution.kara` | a Rust solution as LeetCode's Rust users write it (`s.as_bytes()`, an `lps` table from `vec![0; n]` filled by a `while` loop over `len` and `i`, and `String::from_utf8(s[..lps[n - 1]].to_vec()).unwrap()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples, one letter,
one letter four times, a border of two and none (`"l" "abab" "" "aaa"
"ab" ""`); the constraints' most, the border lengths of five strings of
10^5 letters, one letter throughout, one letter and a different last, a
period of 7, two letters at random, and a block of three letters
repeated with one letter then changed (`10^5 letters: 99999 0 99993 1
99994`); and 2000 random strings of 1 to 60 letters from the first 1 to
3 of the alphabet, every other one a repeated block (`2000 random
strings: 32907 letters in all, checksum 610601567`). `longest_prefix.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. The plain arm's worst case is among them, the
second string of 10^5 letters, whose every comparison runs nearly to its
end; it takes the plain arm 0.41 s under `karac __mir-llvm-run`, against
0.30 to 0.35 s for the others.

The Mend loop: the ★, Z and plain arms check clean as first written. The
hash arm checks clean with two warnings, `unnecessary cast: 'u8' widens
to 'i64' implicitly here`, on its `b[len - 1] as i64` and `b[n - len] as
i64`; `karac fix` drops both casts. The Rust solution takes one round of
5 fixes by `karac fix`'s count, from 3 errors: `struct Solution;` to
`struct Solution {}`, `String::from_utf8` and `Solution::longest_prefix`
to `.` paths, `s.as_bytes()` to `s.bytes()`, and `vec![0; n]` to
`Vec.filled(n, 0)`; `s[..lps[n - 1]].to_vec()` and the `unwrap` stay.
Its output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every length shorter than the string tried letter by letter,
and the longest whose prefix is also the suffix kept. LeetCode's two
examples, one letter, and 2000 strings of 1 to 12 letters from the first
1 to 3 of the alphabet, every other one a block of 1 to 8 letters
repeated, with one letter then changed half the time, so that long
borders are common. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | shorter than the string, and both its prefix and its suffix |
| P3 | the string reversed: the answer reversed |
| P4 | a, b and c renamed c, a and b: the answer renamed |
| P5 | a z, found nowhere else, put at each end: `"z"` |
| P6 | the ★ arm's answer |

All 60,090 checks pass on every arm: `2003 strings: checksum 859210030,
60090 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, comparing every
prefix with its suffix, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a mismatch falls back to no border at all | P1 46, P3 91, P6 184 |
| M2 | ★: the table started at its third entry | P1 759, P3 54, P6 3036 |
| M3 | hash: the suffix hashed back to front | P1 234, P6 234 |
| M4 | hash: the shortest agreeing length taken | P1 843, P6 843 |
| M5 | Z: the match carried over from the window the larger of the two bounds, not the smaller | P1 249, P2 249, P3 406, P6 249 |
| M6 | Z: a match one letter short of the end accepted | P1 595, P2 595, P3 720, P6 595 |
| M7 | plain: lengths tried from the shortest up | P1 843, P6 843 |
| M8 | plain: the suffix compared without its last letter | P1 595, P2 595, P3 720, P6 595 |
| M9 | solution: a mismatch falls back one letter, not along the borders | P1 113, P2 113, P3 215, P6 113 |
| M10 | solution: the table's last entry never filled | P1 1369, P5 2003, P6 1369 |

P1 and P6 kill all ten, P3 six, P2 four, P5 one, and P4 none. No arm
asks which letters it holds, only whether two are equal, and no edit
changes that, so renaming the letters (P4) cannot tell. Four edits
return a string that is not a border at all (P2): M5 and M6 accept a
match that does not run to the end, M8 one that is a letter short, and
M9 a fallback that skips the check. The rest return a real border that
is not the longest, which only P1, P3 and P6 can see: M4 and M7 the
shortest, M1, M2 and M3 one found by a search that misses the longest.
With a z at each end (P5) the only border is `"z"`, which every edit but
M10 still finds.

## Benchmarks

The bench lays 10^5 letters, the constraints' most, a block of 7
repeated, `abacaba`, so the string's border is long. Then 2000 rounds,
each changing one letter, drawn from the checksum so far, building the
string afresh, asking for its longest happy prefix, and putting the
letter back. Every implementation prints `2000 rounds over 10^5 letters:
checksum 101235491`. The work is one pass of the prefix function over
10^5 letters and a copy of the string, a round. Rust builds each string
with `String::from_utf8` of a clone; C copies into a fresh buffer and
returns a copy of the prefix; Go converts its byte slice to a `string`;
Python decodes a `bytearray`.

BENCHTAB
