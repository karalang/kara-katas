# 1839. Longest Substring Of All Vowels in Order

A string is considered beautiful if it satisfies the following
conditions: each of the 5 English vowels (`'a'`, `'e'`, `'i'`, `'o'`,
`'u'`) must appear at least once in it, and the letters must be sorted
in alphabetical order (i.e. all `'a'`s before `'e'`s, all `'e'`s before
`'i'`s, etc.). For example, strings `"aeiou"` and `"aaaaaaeiiiioou"` are
considered beautiful, but `"uaeio"`, `"aeoiu"`, and `"aaaeeeooo"` are
not beautiful. Given a string `word` consisting of English vowels,
return the length of the longest beautiful substring of `word`. If no
such substring exists, return `0`. A substring is a contiguous sequence
of characters in a string.

```
word = "aeiaaioaaaaeiiiiouuuooaauuaeiu"  ->  13
word = "aeeeiiiioooauuuaeiou"            ->  5
word = "a"                               ->  0
```

**Constraints:** `1 <= word.length <= 5 * 10^5`, `word` consists of
characters `'a'`, `'e'`, `'i'`, `'o'`, and `'u'`.

The arms are `fn longest_beautiful_substring(word: String) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `longest_beautiful_substring.kara` ★ | one walk of the word, holding the length of the run of letters in order that ends at each letter and how many vowels it has; a letter before the one ahead of it starts a new run, a letter after it adds a vowel, and a run with all five is beautiful. O(n) |
| `longest_beautiful_substring_runs.kara` | the word cut into runs of one letter, each its letter and length; a beautiful substring is five runs in a row whose letters are a, e, i, o and u, all of each, and its length their sum. O(n) |
| `longest_beautiful_substring_states.kara` | a machine of six states: none, and the vowel a run in order has reached, its place in "aeiou". Each letter is the reached vowel again, the next vowel, or else breaks the run, and an `a` that breaks it starts the next. O(n) |
| `longest_beautiful_substring_scan.kara` | from each `a` that starts a run of `a`s, the word scanned on while its letters are in order, and the stretch kept when its runs, deduplicated, are five letters. Each scan stops where the letters fall back, before the next start, so the word is walked once. O(n) |
| `longest_beautiful_substring_solution.kara` | a Rust solution as LeetCode's Rust users write it (the ★ arm's run length and vowel count over `word.as_bytes()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples; six edges,
the five vowels once, out of order, one vowel missing, a run in order
that starts past its `a`, two beautiful runs with the second longer, and
a run that falls back to an `a` part of the way (`5 0 0 5 10 6`); the
constraints' most, `5 * 10^5` vowels drawn at random, and one beautiful
run of 10^5 of each vowel (`the most: 60 500000`); and 3000 random words
of 1 to 30 vowels (`3000 random words: checksum 373198482`). The words
are drawn a vowel at a time, each the one before it again, the next
vowel, an `a`, or any vowel, so that runs in order are common.
`longest_beautiful_substring.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, runs and scan arms and the harness check clean as
first written. The states arm was first written with
`"aeiou".chars().collect::[Vec[char]]()`, Rust's turbofish; check
refused it, naming the turbofish and the annotated binding Kāra writes
in its place, and `karac fix` wrote `let order: Vec[char] =
"aeiou".chars().collect();`, 2 fixes. The Rust solution takes 17 fixes
by `karac fix`'s count, and its diff is: `struct Solution {}` added
above the `impl`; `word.as_bytes()` to `word.bytes()`; `let mut ans = 0`
and `let mut len = 1` to `let mut ans: i32 = 0` and `let mut len: i32 =
1`, the answer returned as an `i32`; `Solution::` to `Solution.` at the
harness's 12 calls; and the harness's `as i64` on the result taken off.
The solution's `word: String` is Kāra as it stands. Every arm's output
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every substring, kept when it has each of the five vowels and
its letters are in alphabetical order, and the longest kept. It runs
2000 random words of 1 to 25 vowels, drawn as the harness draws them.
Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | none, or from 5 to the whole word |
| P3 | every letter written twice doubles the length |
| P4 | a `u` put before the word changes nothing |
| P5 | "aeiou" put after the word gives at least 5, and no less |
| P6 | the ★ arm's answer |

Check warned that the solution's call was first written `word.clone()`
for a parameter that only borrows it, and `karac fix` took the
`.clone()` off, 1 fix. All 60,000 checks pass on every arm: `2000 cases:
checksum 138850638, 60000 checks over 5 arms: 0 failures`, under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.
Python, over the same cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a run with four vowels counted beautiful | P1 602, P2 26, P6 2408 |
| M2 | ★: a second `u` in a row starting a new run | P1 406, P3 577, P6 1624 |
| M3 | runs: a run of one letter cut after three | P1 323, P3 471, P6 323 |
| M4 | runs: `o` and `u` taken in the wrong order | P1 580, P5 1995, P6 580 |
| M5 | states: the `a` that starts a run not counted in its length | P1 577, P2 18, P3 577, P5 1071, P6 577 |
| M6 | states: the run never reaching `u` | P1 577, P5 2000, P6 577 |
| M7 | scan: a letter the same as the one before it ending the scan | P1 559, P3 141, P6 559 |
| M8 | scan: each stretch taken one short | P1 577, P2 18, P3 577, P5 1071, P6 577 |
| M9 | solution: every letter in order counted as a new vowel | P1 1531, P3 1815, P4 1, P6 1531 |
| M10 | solution: a letter that falls back keeping the run's length | P1 336, P3 362, P4 12, P6 336 |

## Benchmarks

The bench builds 40 words of 10^5 vowels once, drawn as the harness
draws them, and makes 1000 calls of the ★ arm, each call's word drawn
from the checksum so far. The arm reads the word's bytes where they are,
so no call copies one. It checks clean as first written. Every
implementation prints `1000 calls: checksum 177021567`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.54 s against Rust's 0.28 s (0.58 s with overflow checks
on), C's 0.16 s and Go's 0.39 s; Python takes 12.0 s.
