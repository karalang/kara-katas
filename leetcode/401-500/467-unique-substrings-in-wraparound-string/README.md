# 467. Unique Substrings in Wraparound String

We define the string `base` to be the infinite wraparound string of
`"abcdefghijklmnopqrstuvwxyz"`, so `base` looks like
`"...zabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcd...."`.
Given a string `s`, return the number of unique non-empty substrings of
`s` that are present in `base`.

```
s = "a"    ->  1
s = "cac"  ->  2
s = "zab"  ->  6
```

**Constraints:** `1 <= s.length <= 10^5`; `s` consists of lowercase
English letters.

## Approaches

Every arm is `fn find_substring_in_wrapround_string(s: String) -> i64`,
and borrows `s`. A substring of `base` is a run of letters, each the one
after the last (`"za"` included), so it is fixed by either end letter
and its length.

| file | mechanism |
|---|---|
| `unique_substrings.kara` ★ | for each letter, the longest run ending on it anywhere in `s`; every shorter run ending there is a suffix of it, and the runs ending on different letters are different. The answer is the sum of the 26 lengths. O(n) |
| `unique_substrings_start.kara` | the mirror image: read `s` from the right and keep the longest run starting on each letter. O(n) |
| `unique_substrings_runs.kara` | cut `s` into maximal runs; in a run of length `L`, the letter at offset `i` starts runs up to `L - i`, and offsets past 25 repeat a letter with a shorter run, so only the first 26 are looked at. O(n) |
| `unique_substrings_set.kara` | the plain reference: from every position extend while each letter follows the last, putting every substring met into a `Set[String]`, and count the set. O(n²) in the worst case |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 11 lines: the three LeetCode examples, the
whole alphabet, the alphabet backward, a repeated `"abc"`, a run across
the wrap (`"xyzabcxyz"`), one letter ten times, a run of 100 letters
from `z` (2,275), 1,000 letters broken into runs of 30 (780), and for
300 random strings (1 to 200 letters, each following the last with
probability 1/2, 3/4 or 15/16) the total of the answers and a checksum.
`unique_substrings.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases.

| | property |
|---|---|
| P1 | on up to 12 letters, the answer is brute force's: every substring of `s`, kept when each letter follows the last, counted once |
| P2 | shifting every letter along the alphabet keeps the answer |
| P3 | reversing `s` and mirroring every letter (`a` and `z`, `b` and `y`, ...) keeps it |
| P4 | a single run of `L >= 26` letters gives `26 L - 325` |
| P5 | writing every letter twice gives the number of different letters plus the number of different neighbouring pairs that are a run of two |

P4 holds because the run's last 26 letters are the 26 letters, ending
runs of `L - 25` to `L`. In P5 a doubled letter breaks every run, so
only single letters and the pairs straddling two copies are left.

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `z` is not followed by `a` | P1 227, P2 1082, P4 1499, P5 959 |
| M2 | ★: the last run ending on a letter is kept, not the longest | P1 156, P3 1193, P5 1476 |
| M3 | start: a run goes down the alphabet | P1 1329, P4 1500, P5 1474 |
| M4 | start: the last letter is never read | P1 1396, P3 931, P4 1500 |
| M5 | runs: only the first 25 offsets of a run are looked at | P3 82, P4 1500 |
| M6 | runs: every letter of a run is credited with its whole length | P1 1333, P4 1500, P5 1214 |
| M7 | set: a substring stops at the first letter that does follow | P1 1281, P4 1500, P5 1484 |
| M8 | set: no substring starts at the first letter | P1 1399, P3 931, P4 1500 |

P2 and P3 compare an arm with itself, so they see a mutant only when
the change of input moves its error. Shifting moves the wrap from
`z`-`a` to another pair, which is how P2 catches M1; reversing and
mirroring maps `za` to itself, so P3 does not. Reversing does move the
first and last letters, so P3 catches M4 and M8, and with them the
longest-versus-last mistake of M2. P1's strings are too short for M5,
which errs only on runs of 26 or more; P4's runs and the rare long runs
of P3's 80-letter strings find it. M4 drops the last letter and M8 the
first, and P3 swaps the two ends, so both fail P3 exactly when the
first and last letters count differently: 931 cases each.

## Verification

All four arms print the same output as `unique_substrings.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends every arm and the differential match
under `karac run --interp`. LLJIT and `karac build` stop in the legacy
code generator on the harness's index into an array literal ("Index
operator applied to non-array type"), and legacy `karac build` also
warns that `show` moves `s` into its first call and uses it again, which
under v2 is a borrow. Legacy `karac build` rejects the bench program
(see Benchmarks). Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 10 strings of 100,000
letters once, each letter following the last with probability 15/16 and
random otherwise. Each of 100 rounds appends one random letter to every
string and counts its substrings, so every round reads all 1,000,000
letters again. Every implementation prints `100 rounds on 10 strings:
3880200 substrings in all, checksum 564617195`, the Kāra program under
`karac __mir-run` included.

The legacy `karac build` rejects the bench program (it moves
`strings[k]` out of the index, where v2 borrows it), so `bench.sh`
builds the Kāra program with `karac build --mir`, the v2 compiled
backend. That edit is by hand, on top of the `scripts/new-bench.sh`
output.

Every mirror walks the string a character at a time, decoding as it
goes where the language does (Rust's `chars()`, Go's `range`); C reads
bytes. Go appends with `+=`, which copies the string, as Python's `+`
does; Rust, C and Kāra push in place. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.09 to 0.13 s |
| Rust (`rustc -O`) | 0.21 to 0.29 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.26 to 0.30 s |
| Go | 0.30 to 0.32 s |
| Python | 14.0 to 14.1 s |
| Kāra (`karac build --mir`) | 0.45 to 0.51 s |

The `--mir` row is timed at kara `6a0744358e`. Under
`karac __mir-llvm-run` the program prints the same line in 6.5 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark. Under `karac __mir-run` it takes 484 s,
because the MIR interpreter copies the whole string on every
`String.len()`, which the library's `chars()` calls at every step
(B-2026-10-13-2, below).

## Compiler findings

- **B-2026-10-13-2** (`karac __mir-run`, open): `String.len()` and
  `is_empty()` copy the whole text, so every `chars()` loop is
  quadratic in the MIR interpreter: the bench takes 484 s there, against
  14 s for Python. The compiled backends are not affected.
