# 1297. Maximum Number of Occurrences of a Substring

Given a string `s`, return the maximum number of occurrences of **any**
substring under the following rules:

- The number of unique characters in the substring must be less than or
  equal to `maxLetters`.
- The substring size must be between `minSize` and `maxSize` inclusive.

```
s = "aababcaab", maxLetters = 2, minSize = 3, maxSize = 4  ->  2    "aab" twice
s = "aaaa",      maxLetters = 1, minSize = 3, maxSize = 3  ->  2    "aaa" twice, overlapping
```

**Constraints:** `1 <= s.length <= 10^5`, `1 <= maxLetters <= 26`,
`1 <= minSize <= maxSize <= min(26, s.length)`, and `s` holds only
lowercase English letters.

The arms are `fn max_freq(s: Str, max_letters: i64, min_size: i64,
max_size: i64) -> i64`.

## Approaches

A substring that occurs k times has its first `minSize` letters occur at
least k times, with no more distinct letters, so only the substrings of
`minSize` need counting; every arm but the every-size one rests on that.

| file | mechanism |
|---|---|
| `max_freq.kara` ★ | one window of `minSize` letters slid along the string with its letter counts and number of distinct letters; each window with few enough letters counted in a `Map[Str, i64]` by its text. O(n minSize) |
| `max_freq_every.kara` | the statement as written: every substring of every size from `minSize` to `maxSize`, its distinct letters counted in a `Set`, kept in a `Map` from its text to its count when there are few enough. O(n maxSize^2) |
| `max_freq_hash.kara` | the windows of `minSize`, each kept by two polynomial hashes of its letters rolled along in O(1) a step, the pair as the `Map` key; the distinct letters by a sliding count. O(n) |
| `max_freq_windows.kara` | the windows of `minSize` as byte slices from `windows(minSize)`, each whose letters fit in a `Set` of at most `maxLetters` counted in a `Map[Vec[u8], i64]`, the largest count found with `max`. O(n minSize) |
| `max_freq_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `HashMap<&str, i32>` keyed by `&s[i..i + k]`, the distinct letters of each window counted by a `[0; 26]` array refilled per window, `map.entry(..).or_insert(0)` and `ans.max(*e)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, a window as
long as the string, no substring with few enough letters, and one letter
repeated (`2 2 1 0 10`); then 200 random strings of 1 to 600 letters over
the first 2 to 26 letters, with random limits within the constraints
(`200 random strings: occurrences total 1855, checksum 717261866`).
`max_freq.py` mirrors the ★ arm, and its output is byte-identical. Every
arm gives the same output under `karac __mir-run`, `karac run` and `karac
__mir-llvm-run`. The every-size arm takes 22 to 28 s under `karac
__mir-run`, as its O(n maxSize^2) substrings would suggest, which is why
the strings stop at 600 letters.

The Mend loop: each arm's harness first built its letters with Rust's
`char::from_u32(..)`; Kāra has `char.try_from(..)`, which gives a
`Result`, and `karac fix` wrote `char.try_from(..).ok().unwrap()` in all
five. Beyond that the every-size arm checked clean; the ★ and hash arms
wrote Rust's `s.as_bytes()`, which `karac fix` made `s.bytes()` (2 fixes
each); and the windows arm wrote `s.bytes().collect()`, but `bytes()`
gives a `Slice[u8]`, which has no `collect`, and `karac fix` put the
`iter()` in (2 fixes). The Rust arm takes one round of 16 fixes by
`karac fix`'s count: the `use std::collections::HashMap;` line deleted,
`HashMap<&str, i32>` to `Map[Str, i32]` and `HashMap::new()` to
`Map.new()`, `struct Solution;` to `struct Solution {}`, `as usize` to
`as i64`, `as_bytes()` to `bytes()`, `let mut ans = 0` to `let mut ans:
i32 = 0`, `entry(&s[..])` to `entry(s[..])`, `::` to `.`, and the
wrapper's `as i64` dropped as a widening. Its output matches on the first
run. No gap was met.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every substring of every size from `minSize` to `maxSize`, its
distinct letters counted by looking back for an earlier copy of each, and
for each one with few enough, every place in the string compared letter by
letter for a copy; the answer is the most copies of any. 2000 strings of 1
to 14 letters over the first 1 to 4 letters, so that substrings repeat,
with `minSize`, `maxSize` and `maxLetters` drawn within the constraints
(`maxLetters` up to 4). Every string, limit and renaming is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the letters renamed one for one: the same answer |
| P3 | the string reversed: the same answer |
| P4 | `maxSize` as large as it may be, `min(26, n)`: the same answer |
| P5 | one more letter allowed: no fewer occurrences |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 strings: checksum 523641121,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under both
`karac __mir-llvm-run` and `karac __mir-run`. Every one is killed, fails
the same way under both backends and not by a crash. Nine are kept; the
solution arm skipping the last window fails exactly as the every-size
arm's leaving out the substrings from the first letter does, and is left
out.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the leaving letter taken off a step late | P1 73, P3 93, P6 292 |
| M2 | ★: a window with exactly `maxLetters` letters refused | P1 519, P6 2076 |
| M3 | every: the size `minSize` skipped | P1 1364, P4 319, P6 1364 |
| M4 | every: no substring from the first letter | P1 959, P3 182, P6 959 |
| M5 | hash: the leaving letter's weight left out of one hash | P1 471, P6 471 |
| M6 | hash: a letter's last copy leaving not seen | P1 354, P3 198, P6 354 |
| M7 | windows: windows of `maxSize` | P1 656, P4 468, P6 656 |
| M8 | windows: the least count taken | P1 299, P5 22, P6 299 |
| M9 | solution: a letter's second copy counted as new | P1 483, P6 483 |

P1 and P6 kill all nine, P3 three, P4 two and P5 one; P2 kills none.
Every edit treats all letters alike, so renaming them (P2) cannot reach
any of them. The edits that treat the two ends of the string or of a
window differently (M1, M4, M6) give a different answer once the string is
reversed (P3). Widening `maxSize` (P4) changes nothing for an arm that
looks only at windows of `minSize`, so it sees only the edits that count
other sizes: M3, which starts past `minSize`, and M7, which counts windows
of `maxSize`. P5 sees only M8: allowing one more letter lets more windows
in, and the least count among them can fall.

## Benchmarks

The bench builds 10 strings of `10^5` letters, the constraints' longest,
over the first 2 to 6 letters, once from its own generator, then makes 20
passes; each sets one letter of every string, `minSize` and `maxLetters`
from the checksum so far, so no answer carries over, answers it with the ★
arm (`maxSize` is `minSize`; the ★ arm never reads it) and folds the count
plus the pass into the checksum. The counts are keyed by the window's text
in every language: a `Map[Str, i64]` of slices in Kāra, a
`HashMap<&str, i64>` in Rust, a `map[string]int64` in Go and a dict in
Python; C has no map and keeps an open-addressing table, fresh per call,
of where each window starts, hashed by FNV-1a over its letters and
compared with `memcmp`. Every implementation prints `20 passes over 10
strings of 10^5: checksum 108354509`.

BENCHTAB
