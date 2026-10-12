# 420. Strong Password Checker

A password is strong if it has 6 to 20 characters, at least one
lowercase letter, one uppercase letter and one digit, and no character
three times in a row. Given a password, return the fewest steps that
make it strong, where one step inserts, deletes or replaces one
character.

```
password = "a"         -> 5
password = "aA1"       -> 3
password = "1337C0d3"  -> 0
```

**Constraints:** `1 <= password.length <= 50`; letters, digits, `.`
and `!`.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `strong_password.kara` ★ | count the runs by length mod 3: one replacement breaks every 3 characters of a run and can supply a missing kind too. Under 6 characters, insertions cover both. Over 20, the `n - 20` deletions go first where they save a replacement soonest: one to each run of length 0 mod 3, then two to each run of length 1 mod 3, then three at a time | O(n) | O(1) |
| `strong_password_heap.kara` | the deletions one at a time from a smallest-first `PriorityQueue` of runs keyed by (length mod 3, length); a run below 3 leaves the queue, and the replacements are counted from what is left | O(n + d log r) | O(r) |
| `strong_password_scan.kara` | the same choice made by scanning the runs for each deletion | O(n + d r) | O(r) |
| `strong_password_knapsack.kara` | no greedy order: the deletions are shared among the runs in every way, by a knapsack over the runs whose value is the replacements still needed | O(n + d · sum of runs) | O(d) |
| `differential.kara` | the four arms on 1,500 random passwords, five properties, one of them a dynamic program over every insertion, deletion and replacement | — | — |

`d` is the number of deletions, `n - 20`, and `r` the number of runs of
3 or more.

Every arm prints the same 13 lines: the three LeetCode examples, nine
edge cases (a run of 3, a run of 6, two runs of 3, 21 characters
missing a lowercase letter, 21 `a`s, LeetCode's
`"bbaaaaaaaaaaaaaaacccccc"` and `"aaaabbbbccccddeeddeeddeedd"`, ten 1s,
twenty-one characters with no letter or digit at all), and for 2,000
random passwords of 1 to 40 characters from `aAbB1.` written in runs of
1 to 6, the total of the answers and a checksum. `strong_password.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. Each of 1,500
random cases writes a password of 1 to 28 characters from `aAbB1.` in
runs of 1 to 6:

| | property |
|---|---|
| P1 | on every third case, the answer is the fewest edits found by a dynamic program over the password's characters that deletes, keeps or replaces each one and may insert before it. Its state is the length written so far (at most 20), the last character written, how often it repeats, and the kinds seen; a character the edit chooses differs from its neighbours |
| P2 | the answer is at least each of: the kinds missing, the characters short of 6, the characters over 20 |
| P3 | the answer is at most those three added to one replacement for every 3 characters of every run, each fault fixed on its own |
| P4 | swapping the case of every letter, or reversing the password, gives the same answer |
| P5 | one letter written `k` times needs `max(2, 6 - k)` under 6 characters, `max(2, k / 3)` up to 20, and `k - 14` over 20 |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | mod: no deletion goes to a run of length 0 mod 3 first | P1 109, P5 251 |
| M2 | mod: from 6 to 20 characters, missing kinds are ignored | P1 8, P2 28 |
| M3 | heap: the queue pops the largest first | P1 130 |
| M4 | heap: a run shortened to 3 leaves the queue | P1 73 |
| M5 | scan: each deletion shortens the longest run | P1 107 |
| M6 | scan: the deletions are not counted | P1 137, P2 269, P5 726 |
| M7 | knapsack: a run takes at most one deletion | P1 85, P5 695 |
| M8 | knapsack: replacements are rounded up | P1 359, P3 428, P5 1113 |

M3, M4 and M5 put the deletions in the wrong runs, which costs a
replacement only on some passwords over 20 characters; only P1's exact
search sees them. M2 matters only on passwords of 6 to 20 characters
with fewer replacements than missing kinds, which runs of up to 6 make
rare. No mutant fails P4: every arm reads only the kinds and the runs,
which a change of case or a reversal keeps.

## Verification

All four arms print the same output as `strong_password.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run` and
`karac run --interp`, and `karac check` passes on every file. The
differential prints `30000 checks, 0 failures` on the same three; the
tree-walking interpreter takes 22 minutes for it, against 73 s under
`karac __mir-run` and 2 s under `karac __mir-llvm-run`.

LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac build` stop in the
frozen legacy codegen, which has no `bytes()` on a `Str` parameter
(`no handler for method 'bytes' on variable 'password'`), as in katas
402 to 419. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm on 10,000,000 slices of 1 to 50
characters (the problem's limit) of one text of 1,000,000 characters
from `aAbB1.` written in runs of 1 to 6. Each slice is a view, so no
call allocates; it folds the answers into a total and a checksum. Every
implementation prints `10000000 calls: total 114861519, checksum
220511577`; a 2,000-call cut of the Kāra program under `karac __mir-run`
prints the same as the C program cut the same way. Spot timings on a
shared 4-core container, three runs each (`bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| Rust (`rustc -O`) | 2.13 to 2.40 s |
| C (`clang -O3`) | 2.23 to 2.30 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.34 to 2.44 s |
| Go | 2.59 to 2.82 s |
| Python | 66 s |

No `karac build` time: the frozen legacy codegen has no `bytes()` on a
`Str` parameter (see Verification). The Kāra program prints the same
line under `karac __mir-llvm-run` in 6.4 s, compile included; that JITs
the MIR's IR without optimization passes, so it is not a benchmark.

## Compiler findings

No new findings.
