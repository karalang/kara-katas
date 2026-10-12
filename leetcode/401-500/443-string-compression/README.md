# 443. String Compression

Given an array of characters `chars`, compress it in place: for each
group of consecutive repeating characters, write the character, then,
if the group is longer than 1, its length in decimal, one digit per
element. Return the new length; the first that many elements of
`chars` hold the result. Use only constant extra space.

```
chars = ["a","a","b","b","c","c","c"]  ->  6, "a2b2c3"
chars = ["a"]                          ->  1, "a"
chars = ["a","b","b",...,"b"] (12 b's) ->  4, "ab12"
```

**Constraints:** `1 <= chars.length <= 2000`; `chars[i]` is a
lowercase or uppercase English letter, a digit or a symbol.

## Approaches

Every arm is `fn compress(chars: mut ref Vec[char]) -> i64`. A group of
k characters compresses to at most k, so the writes can share the
array with the reads as long as they never pass them.

| file | mechanism |
|---|---|
| `compress.kara` ★ | reading and writing in place: read a group with one index, write the character and the count's text (`f"{count}"`) with another. O(n), the count's digits its only extra space |
| `compress_anchor.kara` | an anchor at the start of each group, closed when the next character differs; the count's digits are written lowest first and then reversed where they lie, so the count needs no text at all. O(n), O(1) extra space |
| `compress_runs.kara` | a list of runs, each a character and its length, written back over the array afterwards. O(n), O(number of runs) extra space |
| `compress_text.kara` | the plain reference: build the compressed text as a `String`, then copy it over the array. O(n), O(n) extra space |
| `differential.kara` | the four arms on 1,500 random strings, five properties |

Every arm prints the same 9 lines: the three LeetCode examples, six edge
cases (a count of exactly 10, no repeats, groups of digits, groups of
symbols, and a run of 100), and for 300 random strings of 1 to 300
characters, built from runs of a three-letter alphabet, the total
compressed length and a checksum. `compress.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random strings of 1 to 12 runs of a three-letter alphabet, runs
of up to 1, 3, 15, 120 or 1,200 letters, so counts reach four digits.

| | property |
|---|---|
| P1 | the compressed text is the one the generator wrote as it built the runs, merging a run that repeats the previous letter |
| P2 | expanding the compressed text gives back the string |
| P3 | the compressed text is no longer than the string, and as long as the generator's |
| P4 | compressing s + t, where t starts with a letter s does not end with, gives s's text followed by t's |
| P5 | a run of 1 to 1,001 copies of a digit, a symbol or a space, at or next to a power of ten, compresses to the character and its count |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed. Each was chosen so that it
never writes more characters than it has read, since a mutant that
did would run off the end of the array and stop the run.

| # | mutation | failures by property |
|---|---|---|
| M1 | pointers: the count is one short | P1 1422, P2 1422, P3 532, P5 1264 |
| M2 | pointers: runs are cut at 9 | P1 891, P3 877, P5 1015 |
| M3 | anchor: the last digit is left out of the reversal | P1 868, P2 868, P5 629 |
| M4 | anchor: a digit 9 is written as 0 | P1 480, P2 480, P5 358 |
| M5 | runs: the first character never joins a run | P1 1210, P3 1026, P4 1467, P5 1264 |
| M6 | runs: a run of two is written without its count | P1 457, P2 457, P3 457, P5 143 |
| M7 | text: counts of 1,000 or more are dropped | P1 245, P2 245, P3 245, P5 242 |
| M8 | text: a single last character is dropped | P1 286, P2 286, P3 286, P4 286, P5 236 |

P4 sees only mutants that treat the two ends of a string differently
(M5 and M8): a mutant that miscounts every group alike gets s + t
wrong in the same way as s and t apart. P2 misses M2 because cutting a
run at 9 still expands to the same letters, and M5 because a lone
first letter followed by the rest of its run does too; P1 and P3 see
both. M7 needs a count of four digits, which only the longest runs and
P5's runs near 1,000 reach.

## Verification

All four arms print the same output as `compress.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends every arm matches under
`karac run --interp`, and the differential prints `0 failures` there.
LLJIT and `karac build` stop in the legacy code generator on
`s.chars().collect()` from a `Str` parameter ("no handler for method
'len' on variable 's'"), in the arms' harness and the differential
alike; the bench program stops earlier, on an index into an array
literal. Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 1,000 random strings of
2,000 characters (runs of up to 1, 3, 15 or 120 letters) once, then 20
times copies each one and compresses the copy. Every implementation
prints `20 rounds on 1000 strings of 2000: compressed length 17709140,
checksum 140999877`, the Kāra program under `karac __mir-run` included
(in 36 s).

The mirrors keep the ★ arm's structure, with 32-bit characters
throughout (`char` in Rust, `rune` in Go, `uint32_t` in C). Each writes
the count through its own number-to-text routine: `count.to_string()`,
`strconv.Itoa`, `snprintf` and `str`. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.36 to 0.38 s |
| Rust (`rustc -O`) | 0.26 to 0.31 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.28 to 0.31 s |
| Go | 0.22 to 0.24 s |
| Python | 3.4 to 3.5 s |

C trails here, likely (not profiled) because `snprintf` costs more per
count than the other languages' integer-to-text routines. The frozen
legacy `karac build` cannot build the program (see Verification), so
there is no legacy time. The Kāra program prints the same line under
`karac __mir-llvm-run` in 3.7 s, compile included; that JITs the MIR's
IR without optimization passes, so it is not a benchmark.

## Compiler findings

Two new findings, filed as kara B-2026-10-12-24 and B-2026-10-12-25.

- **B-2026-10-12-24 (fixed).** The anchor arm reverses its digits with
  `chars[first..write].reverse()`. `karac check` and both MIR backends
  refused it: `Slice.reverse() requires a mutable slice`, on a
  `mut ref Vec[char]` parameter and on a `let mut` local alike.
  design.md says `v[a..b]` is a `mut Slice[T]` where a mutable view is
  needed, and passing `mut v[a..b]` to a `mut Slice[T]` parameter was
  accepted and ran. The arm swapped the digits with two indexes until
  kara 7cd5dfe673 fixed it; it is back to the one call, and mutants M3
  and M4, rerun on it, fail the same counts as before.
- **B-2026-10-12-25.** Trying `split_at_mut` for the same reversal:
  `karac check` accepts it, but `karac __mir-run` has no such function.
  (The row first said `karac __mir-llvm-run` lacked it too; that was a
  binary built before kara 010499d0d5, which already lowers it.)
