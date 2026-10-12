# 392. Is Subsequence

Given strings `s` and `t`, return true if `s` is a subsequence of `t`:
`s` can be made from `t` by deleting some (or no) characters without
changing the order of the rest.

```
s = "abc", t = "ahbgdc"  -> true
s = "axc", t = "ahbgdc"  -> false
```

**Constraints:** `0 <= s.len() <= 100`; `0 <= t.len() <= 10^4`; both
hold lowercase English letters only.

**Follow-up:** many `s` (10^9 of them) against one `t`. The `_next` and
`_search` arms are the two usual answers: they build an index of `t`
once and then match each `s` in time that depends on `s` alone.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `is_subsequence.kara` ★ | two pointers: walk `t`, and each byte that equals the next unmatched byte of `s` moves the pointer into `s` on | O(\|t\|) | O(1) |
| `is_subsequence_dp.kara` | `s` is a subsequence exactly when the longest common subsequence is all of `s`; the LCS table is filled one row at a time | O(\|s\| · \|t\|) | O(\|t\|) |
| `is_subsequence_next.kara` | a next-occurrence table, `next[i][c]` the first position at or after `i` holding byte `c`; matching `s` is one jump per letter | O(256 · \|t\|) to build, O(\|s\|) per query | O(256 · \|t\|) |
| `is_subsequence_search.kara` | each letter's sorted positions in `t`, in a `Map[char, Vec[i64]]`; each letter of `s` binary-searches for its first position after the last match | O(\|t\|) to build, O(\|s\| log \|t\|) per query | O(\|t\|) |
| `differential.kara` | the four arms on 3,000 random strings `t` and pairs built from them whose answers are known, five properties | — | — |

Every arm prints the same 11 lines: the two LeetCode examples, eight edge
cases (both empty, an empty `s`, an empty `t`, equal strings, `s` longer
than `t`, a repeated letter, the same letters out of order, gaps), and
for 3,000 random pairs over the letters `a` to `c` (`t` of 0 to 40
letters, `s` of 0 to 15) how many are subsequences, with a checksum.
`is_subsequence.py` mirrors the ★ arm and its output is byte-identical.

The harness passes `String` values straight to the `Str` parameters. A
first draft wrote `is_subsequence(s.as_str(), t.as_str())`, but the
library gives `as_str` "for places other than call boundaries"
(`docs/library/strings.md`), since a `String` argument already passes
as `Str`. The legacy interpreter has no `as_str` at all, so the first
draft also failed there.

## Differential

`differential.kara` holds copies of the four arms. For each of 3,000
random strings `t` of 0 to 40 letters from `abc`:

| | property |
|---|---|
| P1 | every arm says true for `s` made by keeping a random subset of `t`'s letters in order |
| P2 | every arm says false for that `s` with a `z`, which `t` never holds, put in at a random place |
| P3 | every arm says false for `t` with one more letter put in, which is longer than `t` |
| P4 | for a random `s`, putting up to five more letters into `t` never turns a true answer false |
| P5 | reversing both strings changes no answer |

P4 is checked only where the arm's answer was true, so the number of
checks depends on the answers. It prints `3000 strings, 53692 checks,
0 failures` under `karac __mir-run` and `karac run --interp`, and a
count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | pointers: one unmatched letter of `s` is let through | P2 527, P3 435, P5 208 |
| M2 | pointers: every byte of `t` moves the pointer | P2 2853 |
| M3 | dp: a match extends the cell above, not the diagonal | P3 1471 |
| M4 | dp: a mismatch ignores the cell to the left | P1 2624, P4 23, P5 128 |
| M5 | next: the next letter may reuse the position just matched | P3 1471 |
| M6 | next: each row starts empty instead of copying the one after it | P1 2629, P4 14, P5 128 |
| M7 | search: a position equal to the last match counts as after it | P3 1471 |
| M8 | search: a letter absent from `t` is skipped | P2 3000, P3 219, P4 69 |

M3, M5 and M7 are one mistake in three arms (a letter of `t` used twice)
and fail the same 1471 checks: only P3 makes `s` need more letters than
`t` has. M2 turns the pointers arm into a length comparison, which only
P2's `z` exposes.

## Verification

All four arms print the same output as `is_subsequence.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac run --interp`, and
`karac check` passes on every file. Under `karac __mir-llvm-run` every
file stops at the missing `String.as_str` native, as in katas 383, 385, 388,
389 and 391; not filed. The legacy native backends (LLJIT, `karac build`,
`KARAC_AUTO_PAR=1 karac build`) stop in codegen: `no handler for method
'bytes'` on a `Str` parameter (as in kata 388), and the search arm
panics in `src/codegen/control_flow_for.rs`. They are frozen, so not
filed.

## Benchmarks

The bench program uses the ★ arm. It builds a pool of 1,000,000 random
letters once, then checks 20,000 pairs read out of it without copying:
`s` a window of 100 letters (the problem's limit) and `t` a window of 0
to 10,000 letters (the limit), each at a random place, about 93 million
bytes of `t` in all. A random `t` of a few thousand letters holds a
random `s` of 100 about as often as not, so both answers are common.
Every implementation prints `20000 pairs: 13558 subsequences, checksum
751607689`; a 300-pair cut of the Kāra program under `karac __mir-run`
prints the same as the C program cut the same way. Spot timings on a
shared 4-core container (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| Go | 0.08 s |
| C (`clang -O3`) | 0.16 s |
| Rust (`rustc -O`) | 0.16 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.17 s |
| Python | 2.7 s |

The Kāra program cannot run the full workload yet. `karac __mir-run`
keeps every `bytes()` copy until exit (kara `B-2026-10-12-8`): the
300-pair cut peaks at 120 MB, so the full run would need several GB.
`karac __mir-llvm-run` stops at `String.as_str`, and the legacy
`karac build` has no `bytes` on a `Str` parameter.

## Compiler findings

No new findings. The gaps this kata runs into are already known: the
MIR interpreter's `bytes()` copies (kara `B-2026-10-12-8`), the
`String.as_str` native on `karac __mir-llvm-run`, and the frozen legacy
backends.
