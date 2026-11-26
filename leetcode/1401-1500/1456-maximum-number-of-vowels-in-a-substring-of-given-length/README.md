# 1456. Maximum Number of Vowels in a Substring of Given Length

Given a string `s` and an integer `k`, return the maximum number of
vowel letters in any substring of `s` with length `k`. Vowel letters in
English are `'a'`, `'e'`, `'i'`, `'o'`, and `'u'`.

```
s = "abciiidef", k = 3  ->  3
s = "aeiou", k = 2      ->  2
s = "leetcode", k = 3   ->  2
```

**Constraints:** `1 <= s.length <= 10^5`, `s` consists of lowercase
English letters, and `1 <= k <= s.length`.

Each arm is `fn max_vowels(s: String, k: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `max_vowels.kara` ★ | a window of k letters slid along the string's `Vec[char]`, its vowels counted as a letter comes in and another goes out, each letter tested by `"aeiou".contains(c.to_string())`. O(n) |
| `max_vowels_prefix.kara` | the vowels before each place as prefix sums over `s.bytes()`, each byte tested by a `match` on byte literals, and each window's vowels the difference of two of them, the most by `map(..).max()`. O(n) |
| `max_vowels_table.kara` | each byte looked up in a table of the 26 letters, `[0; 26]` with 1 for a vowel, and the window's count kept as it slides. O(n) |
| `max_vowels_zip.kara` | the first window's vowels by `take(k).filter(..).count()`, then the letters coming in, `s.chars().skip(k)`, zipped with the letters going out, each pair's change folded in by `scan` and the most by `fold`. O(n) |
| `max_vowels_solution.kara` | a Rust solution as LeetCode's Rust users write it (`s.as_bytes()`, a closure `is_vowel` over a `match` on byte literals, `k as usize`, and the window's count by `+=` with `i32::max`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 8 lines: LeetCode's three examples and three
more, one letter, no vowel, and the window the whole string, a line each
(`3`, `2`, `2`, `1`, `0`, `5`); the constraints' most, 10^5 letters, a
vowel one time in 3, with windows of 1, of 1000 and of the whole string
(`10^5 letters: 1 390 33423`); and 2000 random cases of 1 to 60 letters,
a vowel one time in 1 to 5, with a window of 1 to the whole string
(`2000 random cases: 15617 vowels, checksum 730304789`). `max_vowels.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`.

The Mend loop, each count by `karac fix`'s own: the ★ arm tested a
letter by `"aeiou".contains(c)`, which `karac check` refuses, `contains`
taking a `Str` pattern, and `karac fix` writes `c.to_string()`; with the
count declared `count: i32`, 2 fixes. The prefix arm wrote `matches!(b,
b'a' | ..)`, which is refused, Kāra having no macros, and `karac fix`
writes `match b { b'a' | .. => true, _ => false }`; with `k as usize` to
`k as i64`, 4 fixes. The table arm cast each index, `table[(v - b'a') as
i64]`, which `karac check` warns is a widening it makes itself, and
`karac fix` drops the three casts; with `count: i32` and `best: i32`, 5
fixes. The zip arm wrote `matches!` too, `k as usize`, `vowel(*c)` for a
`filter`'s borrowed char, and Rust's `scan(first, \|count, (inn, out)\|
{ *count += ..; Some(*count) })`, which `karac fix` writes as Kāra's
`scan`, the state passed in and handed back, `let count = count + (..);
Some((count, count))`, 6 fixes. The Rust solution takes one round of 6
fixes: `struct Solution;` to `struct Solution {}`, `s.as_bytes()` to
`s.bytes()`, `k as usize` to `k as i64`, `cur: i32`, `i32::max` to
`i32.max`, and `Solution::` to `Solution.`. The harness passed the long
string as `long.clone()` to an arm that only borrows it, which `karac
check` warns of, and `karac fix` passes `long`. Every arm's output
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every substring of k letters, its vowels counted one by one,
and the most of them, while n k is at most 10^6. LeetCode's examples,
the three edge cases above, the constraints' most three ways, and 1994
random cases drawn as the harness draws them.

| | property |
|---|---|
| P1 | the statement read literally, while n k is at most 10^6 |
| P2 | the string backwards gives the same |
| P3 | a window one longer gives the same or one more |
| P4 | a vowel put in front gives the same or one more, while the string stays within 10^5 letters |
| P5 | from 0 to k and at most the string's vowels, and all of them when k is the string's length |
| P6 | the ★ arm's answer |

All 59,210 checks pass on every arm: `2003 cases: checksum 188634237,
59210 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by prefix sums
of the vowels, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the letter going out taken one place late | P1 482, P2 491, P6 1928 |
| M2 | ★: the first window's count left out of the best | P1 248, P2 247, P3 109, P4 93, P5 129, P6 996 |
| M3 | prefix: each window one letter short | P1 1055, P2 235, P5 77, P6 1057 |
| M4 | prefix: `u` not taken for a vowel | P1 1116, P5 69, P6 1118 |
| M5 | table: the first window never counted | P1 248, P2 247, P3 109, P4 93, P5 129, P6 249 |
| M6 | table: a vowel counted twice | P1 1920, P3 778, P4 410, P5 1772, P6 1922 |
| M7 | zip: the letters going out paired one place early | P1 552, P2 641, P3 295, P4 237, P5 76, P6 553 |
| M8 | zip: the first window's count left out of the best | P1 248, P2 247, P3 109, P4 93, P5 129, P6 249 |
| M9 | solution: the letters going out never taken off | P1 1479, P5 787, P6 1480 |
| M10 | solution: the first letter left out of the first window | P1 908, P2 630, P4 853, P5 77, P6 910 |

## Benchmarks

The bench draws 200 strings of 10^5 letters, a vowel one time in 3,
once, then asks each for a window of 1 to 10^5 letters 5 times with the
★ arm, folding the answers to a checksum. Each implementation collects
the letters as its characters and tests each with its library's search
of "aeiou": Rust's `contains` on a `char`, C's `strchr`, Go's
`strings.ContainsRune` and Python's `in`. Every implementation prints
`1000 windows of 10^5 letters: checksum 483954448`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 1.86 s against Rust's 1.66 s (1.98 s with overflow checks
on), C's 1.51 s and Go's 2.8 s; Python takes 18 s.
