# 395. Longest Substring with At Least K Repeating Characters

Given a string `s` and an integer `k`, return the length of the longest
substring of `s` in which every character appears at least `k` times, or
0 if there is none.

```
s = "aaabb",  k = 3  -> 3   ("aaa")
s = "ababbc", k = 2  -> 5   ("ababb")
```

**Constraints:** `1 <= s.len() <= 10^4`; `s` holds lowercase English
letters only; `1 <= k <= 10^5`.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `longest_substring.kara` ★ | divide and conquer: a letter seen fewer than `k` times in a range is in no answer inside it, so split the range at every such letter and solve the pieces; a range with none is its own answer | O(26 n) | O(26) per level, depth at most 26 |
| `longest_substring_window.kara` | one sliding window for each number `u` of different letters from 1 to 26; fixing `u` gives the window a rule for when to shrink | O(26 n) | O(26) |
| `longest_substring_brute.kara` | every substring, extended one letter at a time from each start, with counts in a `Map[char, i64]` and two tallies | O(n^2) | O(26) |
| `longest_substring_stack.kara` | the ★ arm's splitting driven by an explicit stack of ranges, skipping ranges no longer than the best so far | O(26 n) | O(n) |
| `differential.kara` | the four arms on 3,000 random cases whose answers are known by construction, five properties | — | — |

Every arm prints the same 12 lines: the two LeetCode examples, nine edge
cases (one letter with `k` = 1 and 2, all letters different with `k` = 1
and 2, two good runs followed by rare letters, a string that has to
split twice before it finds its answer, no answer, every letter twice,
a long run with one rare letter at the end), and for 3,000 random strings (1 to 40 letters from `abcd`,
`k` from 1 to 5) the sum of the answers and a checksum.
`longest_substring.py` mirrors the ★ arm and its output is
byte-identical.

The window and brute-force arms first called their counter of different
letters `distinct`. The spec makes `distinct` a contextual keyword,
special only directly before `type` (`docs/design.md` § Keywords), but
`karac check` refuses it as a variable name, and `karac fix` rewrote
each use to `r#distinct` (kara `B-2026-10-12-11`). The arms now call it
`kinds`.

## Differential

`differential.kara` holds copies of the four arms. For each of 3,000
random cases, with `k` from 1 to 5:

| | property |
|---|---|
| P1 | a string in which each of up to four letters appears `k` to `k + 3` times, shuffled, is its own answer: every arm returns its length |
| P2 | with `k` = 1 every arm returns the length of a random string |
| P3 | with `k` larger than the string every arm returns 0 |
| P4 | a `z` that appears once splits the string: for `k` >= 2 the answer for `a + "z" + b` is the larger of the answers for `a` and `b` |
| P5 | reversing the string changes no answer |

It prints `3000 cases, 60000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | divide: a letter seen exactly `k` times also splits | P1 1477, P2 1112 |
| M2 | divide: a range with no rare letter counts one short | P1 3000, P2 3000 |
| M3 | divide: the piece after the last rare letter is dropped | P4 532, P5 327 |
| M4 | window: every occurrence past `k` counts again | P1 2748, P2 2809, P4 1520, P5 1180 |
| M5 | window: the window may hold one letter too many | P4 457, P5 283 |
| M6 | brute: a letter counts as enough one occurrence early | P1 589, P2 3000, P3 38, P4 726 |
| M7 | stack: the piece after the last rare letter is dropped | P4 532, P5 327 |
| M8 | stack: ranges one longer than the best so far are pruned | P1 31, P2 79, P4 35, P5 11 |

The first M4 dropped the window arm's `kinds == u` from its candidate
test, and no property caught it. It cannot change an answer: the window
never holds more than `u` letters, and `enough` counts some of them, so
`enough == u` already means `kinds == u`. That mutant is equivalent, and
the arm keeps the test because it states the condition. M3 and M7 are
one mistake in two arms and fail the same checks.

## Verification

All four arms print the same output as `longest_substring.py` under
`karac __mir-run` (the v2 MIR interpreter), and `karac check` passes on
every file. The divide, window and stack arms also match under
`karac run --interp`; the legacy interpreter has no `Option.cloned`,
which the brute-force arm uses. Under `karac __mir-llvm-run` every file
stops at the missing `String.as_str` native, as in katas 383, 385, 388,
389, 391 and 392; not filed. The legacy native backends stop in codegen
with `no handler for method 'bytes'` (or `'len'`) on a `Str` parameter,
as in kata 388, and the legacy typechecker refuses the differential's
`*c` on `Vec[char]` iterator items, as in katas 382 to 389. They are
frozen, so not filed.

## Benchmarks

The bench program uses the ★ arm. It builds a pool of 1,000,000 letters
once, skewed toward the start of the alphabet (each letter is the
smaller of two random ones), so some letters are common and others
rare. Then it makes 10,000 calls, each on a window of 10,000 letters
(the problem's limit) at a random place, with `k` from 1 to 30, and
folds the answers into a sum and a checksum. Every implementation
prints `10000 windows: total 50323003, checksum 249647419`; a 40-call
cut of the Kāra program under `karac __mir-run` prints the same as the C
program cut the same way. Spot timings on a shared 4-core container
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.43 s |
| Go | 0.47 s |
| Rust (`rustc -O`) | 0.54 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.55 s |
| Python | 25 s |

The Kāra program cannot run the full workload natively yet:
`karac __mir-llvm-run` stops at `String.as_str`, and the legacy
`karac build` has no `bytes` on a `Str` parameter. The MIR interpreter
takes 3.1 s for the 40-call cut.

## Compiler findings

- **Six of the spec's contextual keywords are still hard keywords**
  (kara `B-2026-10-12-11`). `distinct`, `shared`, `own`, `where`, `with`
  and `effect` are refused as identifiers (`let mut distinct = 0;`),
  where `docs/design.md` § Keywords says each is a keyword only in one
  position and an ordinary identifier everywhere else. Every other word
  in that table is accepted as a `let` name.
