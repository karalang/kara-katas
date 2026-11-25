# 1371. Find the Longest Substring Containing Vowels in Even Counts

Given the string `s`, return the size of the longest substring
containing each vowel an even number of times. That is, 'a', 'e', 'i',
'o', and 'u' must appear an even number of times.

```
s = "eleetminicoworoep"  ->  13   ("leetminicowor")
s = "leetcodeisgreat"    ->  5    ("leetc")
s = "bcbcbc"             ->  6
```

**Constraints:** `1 <= s.length <= 5 x 10^5`, `s` contains only
lowercase English letters.

Each arm is `fn find_the_longest_substring(s: Str) -> i32`; the Rust
solution's takes a `String`, as LeetCode's signature does.

## Approaches

A substring has every vowel an even number of times exactly when the
prefixes on either side of it have every vowel's count of the same
parity; with the five parities as five bits, the answer is the
furthest apart two prefixes with the same bits are.

| file | mechanism |
|---|---|
| `find_the_longest_substring.kara` ★ | the five parities as bits, each pattern's first prefix kept in a table of 32, the empty prefix at -1; each later prefix with a pattern already seen measures a substring. O(n) |
| `find_the_longest_substring_map.kara` | the same, with each pattern's first prefix in a `Map` and the vowels' bits looked up in a second `Map` |
| `find_the_longest_substring_twopass.kara` | a first pass writes every prefix's bits into a `Vec`; a second records each pattern's first and last prefix, and the answer is the widest such pair. O(n) |
| `find_the_longest_substring_brute.kara` | every start tried, the five counts kept as the substring grows a letter at a time, and the longest with every count even kept; a start too late to beat the best ends the search. O(n²) |
| `find_the_longest_substring_solution.kara` | a Rust solution as LeetCode's Rust users write it (`let mut pos = vec![-1i32; 32];`, a `usize` mask, `'a' => mask ^= 1 << 0`, each pattern's place stored as `i as i32 + 1`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, one
vowel, two of it, and 2000 letters cycling through the alphabet (`13 5
6 0 2 1981`); and 2000 random strings of 1 to 300 letters, drawn from
the first 1 to 10 of "aeioubcxyz" or from the whole alphabet, folded
into a checksum (`2000 random strings: lengths total 280058, checksum
622326442`). `find_the_longest_substring.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the ★ and twopass arms check clean. The map arm's
`bit.get(c).copied()` is refused, since an `Option[ref T]` copies its
item out with `.cloned()`, and `karac fix` writes that (1 fix). The
brute arm's `"aeiou".find(letters[end])` passes a `char` where `find`
takes a `Str`, and the fix writes `letters[end].to_string()` (1 fix).
The Rust solution takes 5 fixes: `struct Solution;` to `struct Solution
{}`, `vec![-1i32; 32]` to `Vec.filled(32, -1i32)`, `let mut ans = 0`,
compared with an `i32`, to `let mut ans: i32 = 0`, `Solution::` to
`Solution.`, and, because the solution takes a `String`, a
`.to_string()` on the test's call of it, where the examples are `Str`s.
`1 << 0`, `0usize` and `i as i32 + 1` stand as Rust wrote them. Every
arm matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every substring, every vowel counted in it letter by
letter, and the longest with every count even. It checks the examples,
1500 random strings of 1 to 20 letters and 500 of 1 to 40, drawn as
the arms' tests draw them.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the string reversed, the same length |
| P3 | every consonant made a z, the same length |
| P4 | the string twice over has every vowel an even number of times, so the answer is all of it |
| P5 | a consonant added at the end lengthens the answer by at most 1 |
| P6 | the ★ arm's length |

All 60,150 checks pass on every arm: `2005 cases: checksum 60847294,
60150 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, with the prefix bits in a
dictionary, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the empty prefix not recorded | P1 631, P2 699, P4 2005, P6 2524 |
| M2 | ★: u not a vowel | P1 485, P6 1940 |
| M3 | map: each pattern's latest place kept | P1 1248, P4 1656, P6 1248 |
| M4 | map: the empty prefix placed at 0 | P1 631, P2 642, P4 2005, P6 631 |
| M5 | twopass: only the patterns without u compared | P1 283, P2 454, P6 283 |
| M6 | twopass: o flips i's bit | P1 376, P6 376 |
| M7 | brute: the last start never tried | P1 36, P2 36, P5 36, P6 36 |
| M8 | brute: each length one short | P1 1852, P4 2005, P6 1852 |
| M9 | solution: e and a share a bit | P1 516, P6 516 |
| M10 | solution: a pattern's place one early | P1 1221, P2 642, P5 153, P6 1221 |

P1 and P6 kill all ten, P2 five, P4 four, P5 two, and P3 none. No arm
tells one consonant from another, so making them all z (P3) changes
nothing for any edit; it stands for an arm that would. Reversing the
string (P2) catches the edits that treat its two ends differently: the
empty prefix lost or misplaced (M1, M4), so a substring from the start
is missed or overcounted but one to the end is not, the last start
skipped (M7), a pattern's place one early (M10), and the patterns with
u's bit ignored (M5). The doubled string, all of which counts (P4),
catches the edits that cannot measure a substring from the very start
(M1, M4), that keep a pattern's latest place rather than its first
(M3), or that come up one short (M8). A consonant added at the end (P5)
catches the last start skipped (M7), which the new last start hides,
and the place one early (M10), which a new longest substring to the end
exposes. Treating u, or o, or e as some other vowel (M2, M6, M9) is
caught only by the literal reading and the ★ arm.

## Benchmarks

The bench builds 4 strings of 5 * 10^5 letters, the constraints' most,
drawn from "aeioubcxyz", once; then makes 80 rounds, each copying one
string with one letter changed, both drawn from the checksum so far,
and finding that string's longest substring with the ★ arm. Every
implementation prints `80 rounds over 4 strings of 500000 letters:
checksum 322158791`. The work is the copy and one pass over 5 * 10^5
letters, the same in every language.

BENCHTAB
