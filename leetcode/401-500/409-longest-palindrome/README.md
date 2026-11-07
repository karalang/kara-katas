# 409. Longest Palindrome

Given a string of lowercase and uppercase letters, return the length of
the longest palindrome that can be built with those letters. Letters are
case sensitive: `"Aa"` is not a palindrome.

```
s = "abccccdd"  -> 7   ("dccaccd")
s = "a"         -> 1
```

**Constraints:** `1 <= s.length <= 2000`; `s` holds only lowercase
and uppercase English letters.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `longest_palindrome.kara` ★ | letter counts: a letter seen `c` times gives `c / 2` pairs, one on each side of the middle, and if any count is odd one letter is left for the middle | O(n) | O(1) |
| `longest_palindrome_set.kara` | a `Set` of letters waiting for a partner: a letter already waiting leaves and makes a pair, any other joins; one letter still waiting can go in the middle | O(n) | O(k) for k distinct letters |
| `longest_palindrome_sort.kara` | sort the letters, then walk the runs of equal letters: a run gives its length rounded down to even, and a run of odd length leaves a letter for the middle | O(n log n) | O(n) |
| `longest_palindrome_odd.kara` | count the letters in a `Map`; every odd count has one letter that cannot be paired, so the answer is the length less the number of odd counts, plus one back for the middle if there were any | O(n) | O(k) |
| `differential.kara` | the four arms on 3,000 random cases, five properties, one of them a brute force over every set of positions | — | — |

Every arm prints the same 13 lines: the two LeetCode examples, ten edge
cases (`"Aa"`, two and three of one letter, three distinct letters, six
of one letter, three odd counts, a palindrome, eight letters that differ
only in case, 31 of one letter, a 68-letter sentence), and for 3,000
random strings of 1 to 60 letters from a, b, c, A, B and C, the total of
the answers and a checksum. `longest_palindrome.py` mirrors the ★ arm
and its output is byte-identical.

The odd arm walks its `Map` in hash order, which is random per process,
but only counts the odd entries, so its output does not depend on that
order.

## Differential

`differential.kara` holds copies of the four arms. Each of 3,000 random
cases makes a string of 1 to 30 letters, drawn from the first 1 to 9 of
`abcABCxyz` so that some strings repeat a few letters many times and
others hold many letters once:

| | property |
|---|---|
| P1 | the string followed by its reverse gives its whole length, and so does the same with one letter between the two |
| P2 | the answer is at most the length, and is odd exactly when some letter occurs an odd number of times, counted by a scan for each position |
| P3 | two more copies of any letter, inserted anywhere, add exactly 2 |
| P4 | the letters shuffled give the same answer |
| P5 | for the first 10 letters, the answer is the size of the largest set of positions whose letters have at most one odd count, found by trying all 2^n sets |

It prints `3000 cases, 4 arms, 60000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | counts: no letter goes in the middle | P1 3000, P2 2664, P5 2459 |
| M2 | counts: a letter's whole count is used, odd or even | P1 3000, P2 2664, P5 2459 |
| M3 | set: a paired letter keeps waiting | P1 3000, P2 2342, P3 1409, P5 2374 |
| M4 | set: the middle needs two letters waiting | P1 3000, P2 727, P5 305 |
| M5 | sort: the letters are not sorted | P1 2776, P2 144, P3 2074, P4 1729, P5 2106 |
| M6 | sort: only a run of one letter leaves one for the middle | P1 1387, P2 1135, P3 80, P5 461 |
| M7 | odd: no letter goes back in the middle | P1 3000, P2 2664, P5 2459 |
| M8 | odd: only a letter seen once counts as odd | P2 1024, P3 265, P5 1496 |

M1, M2 and M7 fail exactly the same checks: each is wrong on every
string with an odd count and right on every other, M1 and M7 by one and
M2 by the number of odd counts. None of the three fails P3 or P4,
because two more of a letter or a shuffle moves them by the same amount
as the right answer. Only M5 fails P4: it is the one mutant whose answer
depends on the order of the letters, since unsorted letters break into
more runs. M8 passes P1, whose strings have at most one odd count; with
none seen, the odd arm answers the whole length anyway.

## Verification

All four arms print the same output as `longest_palindrome.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run` and
`karac run --interp`, and `karac check` passes on every file. The
differential prints `60000 checks, 0 failures` under all three.

Every arm and the differential run under `karac __mir-llvm-run` since
compiler commit 62f5f6de04 added the `String.as_str` native: every arm
takes a `Str` and the harness passes it string literals and `String`s.
The frozen legacy codegen panics in `control_flow_for.rs` on
`for b in s.bytes()` over a `Str` parameter in three arms, and reports
no `len()` on a `Str` parameter in the sort arm, which stops LLJIT,
`karac build` and `KARAC_AUTO_PAR=1 karac build`. Neither is filed.

## Benchmarks

The bench program uses the ★ arm on 300,000 random slices of 1,000 to
2,000 letters (the problem's limit) of one text of 2,000,000 letters
from a to z and A to Z, built from an LCG; each slice starts at a
random place, so no compiler can hoist one answer out of the loop. It
folds the answers into a total and a checksum. Every implementation
prints `300000 slices of a 2000000-letter text: total 441569340,
checksum 999460780`, and so does the Kāra program under
`karac __mir-run`. Each language passes its slice without copying it:
a `Str` view in Kāra, `&str` in Rust, a string slice in Go, a pointer
and a length in C; Python copies it.

### Apple M5 Pro, 2026-11-07

30 runs each, 5 warmups, on the Apple M5 Pro, karac `0.8.0-dev.14781+g3dc7786b7`
(g3dc7786b7, the v2/MIR backend), measured 2026-11-07, with the Kāra binary built
`KARAC_AUTO_PAR=0`. This is the kata's first M5 measurement; Python was not run.
The last column is Kāra's mean over that row's mean.

| implementation | mean | Kāra / this |
|---|---|---|
| c `clang -O3` | 118.0 ms ± 1.1 | 1.33× |
| rust `-O` | 150.2 ms ± 1.4 | 1.05× |
| **kāra `karac build`, seq** | **157.2 ms ± 6.4** | **—** |
| rust `-O -C overflow-checks=on` (equal-safety) | 161.7 ms ± 9.6 | 0.97× |
| go `go build` | 163.1 ms ± 1.6 | 0.96× |

Kāra is 1.05× `rustc -O`, 0.97× equal-safety Rust, 1.33× C and 0.96× Go. The gaps were not investigated on this host.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 55.8 ms ± 0.5 | 32.9 KiB | 2.9 MiB |
| rust | 115.6 ms ± 1.8 | 474.1 KiB | 3.1 MiB |
| kāra | 119.7 ms ± 1.3 | 83.1 KiB | 3.0 MiB |
| go | — | 2450.9 KiB | 7.2 MiB |

`karac build` is 2.1× clang's cold compile and 1.0× rustc's. Kāra's
85,104-byte binary is 2.5× clang's and 5.7× smaller than rustc's. Raw numbers are in
[`bench/results.json`](bench/results.json). The sink matches across the Kāra,
Rust, C and Go builds (`300000 slices of a 2000000-letter text: total 441569340, checksum 999460780`).

### Container x86-64 history

Spot timings on a shared 4-core
container (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.24 to 0.30 s |
| Rust (`rustc -O`) | 0.25 to 0.44 s |
| Go | 0.27 to 0.33 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.33 to 0.70 s |
| Python | 16 to 18 s |

The bench passes `text[start..start + len]`, a `Str` view of a
`String`. The Kāra program also prints the same line under
`karac __mir-llvm-run` in 2.9 s, compile included; that JITs the MIR's
IR without optimization passes, so it is not a benchmark.
The legacy `karac build` panics on it, as above.

## Compiler findings

No new findings.
