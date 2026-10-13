# 466. Count The Repetitions

We define `str = [s, n]` as the string `str` which consists of the
string `s` concatenated `n` times. We define that string `s1` can be
obtained from string `s2` if we can remove some characters from `s2`
such that it becomes `s1`. You are given two strings `s1` and `s2` and
two integers `n1` and `n2`. You have the two strings `str1 = [s1, n1]`
and `str2 = [s2, n2]`. Return the maximum integer `m` such that
`str = [str2, m]` can be obtained from `str1`.

```
s1 = "acb", n1 = 4, s2 = "ab", n2 = 2   ->  2
s1 = "acb", n1 = 1, s2 = "acb", n2 = 1  ->  1
```

**Constraints:** `1 <= s1.length, s2.length <= 100`; `s1` and `s2`
consist of lowercase English letters; `1 <= n1, n2 <= 10^6`.

## Approaches

Every arm is `fn get_max_repetitions(s1: String, n1: i64, s2: String,
n2: i64) -> i64`, and borrows both strings. Matching `s2` greedily as a
subsequence of `s1` written out `n1` times counts the most copies of
`s2` that fit, and the answer is that count divided by `n2`. Between
copies of `s1` the only state is where in `s2` the match stands.

| file | mechanism |
|---|---|
| `count_repetitions.kara` ★ | read copies of `s1` one by one, noting in a `Map` where the match stands after each; within `\|s2\| + 1` copies a place repeats, and the copies between are a cycle that completes the same number of `s2` copies each time. Jump over the whole cycles that fit and read the rest. O(\|s1\| × \|s2\|) |
| `count_repetitions_table.kara` | for each of the `\|s2\|` places, read one copy of `s1` up front to learn where the match ends and how many `s2` copies it completes; then step through the `n1` copies with that table. O(\|s1\| × \|s2\| + n1) |
| `count_repetitions_doubling.kara` | the same table, composed with itself for 2, 4, 8, ... copies, covering `n1` by its binary digits. O(\|s1\| × \|s2\| + \|s2\| log n1) |
| `count_repetitions_plain.kara` | the plain reference: read all `n1` copies a character at a time. O(n1 × \|s1\|) |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 11 lines: the two LeetCode examples, a letter
`s1` lacks, `"aa"` in `"aaa"`, five cases where `s2` straddles copies
of `s1` (`n1` up to 1,000,000, one with `s2` the reverse of `s1`), two
equal strings repeated 100,000 times, and for 300 random cases
(`s1` of 1 to 8 letters and `s2` of 1 to 4 from the first 2, 3 or 4
letters, `n1` up to 1,000, `n2` up to 5) the total of the answers and a
checksum. `count_repetitions.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases.

| | property |
|---|---|
| P1 | on `s1` of up to 5 letters and `n1` up to 6, the answer is brute force's: the largest `m` with `s2` written `n2 × m` times a subsequence of `s1` written `n1` times |
| P2 | the answer for `n2` is the answer for 1 divided by `n2` |
| P3 | `s2` written `r` times with `n2` gives the answer for `s2` with `r × n2` |
| P4 | `s1` written `r` times with `n1` gives the answer for `s1` with `r × n1` |
| P5 | `s2` a single letter of `s1`, found `c` times in it, gives `c × n1 / n2` |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the skipped cycles are read again | P1 338, P3 386, P4 622, P5 1430 |
| M2 | ★: each cycle is taken to repeat everything so far | P1 254, P3 373, P4 698, P5 1430 |
| M3 | table: every copy starts from the start of `s2` | P1 184, P3 372, P4 314 |
| M4 | table: every row is read from the start of `s2` | P1 184, P3 372, P4 314 |
| M5 | doubling: a doubled step counts its first half twice | P1 153, P3 522, P4 279 |
| M6 | doubling: the zero bits of `n1` are taken | P1 505, P4 580, P5 1453 |
| M7 | plain: one copy of `s1` too few | P1 415, P4 466, P5 1058 |
| M8 | plain: the division rounds up | P1 267, P2 367, P3 244, P5 573 |

P1, the only property with an independent answer, sees all eight. P2
sees only M8, the one mutant that touches the division. P5's one-letter
`s2` has a single place to stand, which the table mutants M3 and M4 and
the doubling mutant M5 cannot get wrong. M3 and M4 fail the same
checks: either way, every copy is counted as if the match started
afresh.

## Verification

All four arms print the same output as `count_repetitions.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends every arm and the differential match
under `karac run --interp`, LLJIT and `karac build` (also with
`KARAC_AUTO_PAR=1`). Legacy `karac build` warns that the harness moves
`s1` into its first call and uses it again, which under v2 is a borrow.
Legacy `karac build` rejects the bench program (see Benchmarks).
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 pairs once: `s1` of
100 letters from `a` to `z`, and `s2` of 1 to 100 letters each drawn
from `s1`, so that `s2` always fits. Each of 1,000 rounds runs every
pair with a random `n1` up to 10^6 and `n2` up to 100. Every
implementation prints `1000 rounds on 100 pairs: 759957187 repetitions
in all, checksum 403717988`, the Kāra program under `karac __mir-run`
included (in 36 s).

The legacy `karac build` rejects the bench program (it moves
`firsts[p]` out of the index, where v2 borrows it), so `bench.sh` builds
the Kāra program with `karac build --mir`, the v2 compiled backend.
That edit is by hand, on top of the `scripts/new-bench.sh` output.

Rust, Go and Python keep the places already seen in a hash map, like
the ★ arm's `Map`. C has no map, and since a place is below `|s2|`, its
mirror keeps them in an array indexed by the place, which is cheaper.
Spot timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`, array) | 0.10 to 0.13 s |
| Rust (`rustc -O`) | 0.22 to 0.24 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.22 to 0.25 s |
| Go | 0.21 to 0.23 s |
| Python | 3.2 to 3.4 s |
| Kāra (`karac build --mir`) | 0.33 to 0.38 s |

The `--mir` row is timed at kara `5f01de4c5c`. Under
`karac __mir-llvm-run` the program prints the same line in 2.9 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

No new findings.
