# 451. Sort Characters By Frequency

Given a string `s`, sort it in decreasing order of the frequency of its
characters. The frequency of a character is the number of times it
appears in the string. If there are several answers, return any of
them.

```
s = "tree"    ->  "eert"    ("eetr" is also valid)
s = "cccaaa"  ->  "aaaccc"  ("cccaaa" is also valid; "cacaca" is not)
s = "Aabb"    ->  "bbAa"    ("bbaA" is also valid; 'A' and 'a' differ)
```

**Constraints:** `1 <= s.length <= 5 * 10^5`; `s` consists of
uppercase and lowercase English letters and digits.

## Approaches

Every arm is `fn frequency_sort(s: Str) -> String`. Ties may come out
in any order, so every arm breaks them the same way, the smaller
character first, which makes the answer unique and lets the arms be
compared byte for byte.

| file | mechanism |
|---|---|
| `frequency_sort.kara` ★ | count each character in a map, sort the distinct characters by (count descending, character), and write each as many times as it occurs. O(n + k log k) for k distinct characters |
| `frequency_sort_buckets.kara` | count in an array of 128 (the characters are ASCII), put each character in the bucket of its count, walking the codes upward, and write the buckets from the largest count down. O(n), no sort |
| `frequency_sort_sorted.kara` | count in a map, then sort every character of the string by its count and itself, which brings each character's copies together. O(n log n) |
| `frequency_sort_heap.kara` | count in a map, push (count, negated character) pairs into a `PriorityQueue.max_first()`, and pop them in turn. O(n + k log k) |
| `differential.kara` | the four arms on 1,500 random strings, five properties |

Every arm prints the same 9 lines: the three LeetCode examples, the
empty string, one character, all characters distinct, digits mixed
with letters, and `mississippi`, each with the answer and whether it is
a correct one by an independent check; then, for 300 random strings of
0 to 200 characters drawn from the first 1, 3, 10 or all 62 digits and
letters, the total length, whether every answer was correct, and a
checksum of the answers. The empty string is outside the constraints
and every arm returns it. `frequency_sort.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random strings of 0 to 60 characters drawn from the first 1, 3,
10 or all 62 digits and letters.

| | property |
|---|---|
| P1 | the answer is a correct one: the same characters, each character's copies together, and runs never growing longer |
| P2 | the answer is brute force's, ties broken by the smaller character first |
| P3 | the same characters in another order give the same answer |
| P4 | renaming the characters through a shuffle of the alphabet keeps the run lengths |
| P5 | the string written twice gives every run doubled, in the same order |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | map: the least frequent characters come first | P1 1479, P2 1479 |
| M2 | map: each count starts at 1 | P1 1479, P2 1479, P5 1479 |
| M3 | buckets: the bucket of a count equal to the length is never read | P1 400, P2 400 |
| M4 | buckets: the code of `z` is never read | P1 147, P2 147, P4 234 |
| M5 | sorted: smaller counts sort first | P1 992, P2 992 |
| M6 | sorted: ties go to the larger character first | P2 853 |
| M7 | heap: the queue pops the smallest first | P1 992, P2 1079 |
| M8 | heap: runs are cut at 9 | P1 598, P2 598, P5 930 |

P3 sees none of them: each mutant depends only on the counts, which the
order of the input does not change. M6 still gives a correct answer,
only not the one the arms agree on, so only P2 sees it. P4 sees only
M4, which loses `z` whichever character the renaming turns into it, so
the run lengths change. P5 sees M2 and M8, the mutants that get a run's
length wrong, since doubling the string doubles the true lengths but
not the wrong ones; the others write each run in full, in the same
wrong order both times. M3 fails only on strings of one repeated
character, where the count equals the length.

## Verification

All four arms print the same output as `frequency_sort.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends every arm matches under
`karac run --interp`, and the differential prints `0 failures` there.
LLJIT and `karac build` panic in the legacy code generator
(`src/codegen/control_flow_for.rs:582`) on `for c in s.chars()` over
the `Str` parameter, in every arm, the differential and the bench
program. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 20 random strings of
200,000 characters once, from the first 3, 10, 30 or all 62 digits and
letters in turn, then sorts each 5 times; a checksum folds in each
answer's length and its first, middle and last characters. Every
implementation prints `5 rounds on 20 strings of 200000: 20000000
characters, checksum 880222650`, the Kāra program under
`karac __mir-run` included (in 23 s).

The mirrors keep the ★ arm's structure: a hash map from character to
count, the distinct characters sorted, each written out in a run.
Rust's `HashMap` hashes with SipHash, as Kāra's `Map` does; Go uses
its built-in map. C has no hash map, so it counts in an array of 128
indexed by the code, which is cheaper per character. The Kāra program
reads the three sample characters through `out.bytes()`, which copies
the answer into a `Vec[u8]`; the mirrors index the answer in place.
Spot timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.02 s |
| Rust (`rustc -O`) | 0.21 to 0.23 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.20 to 0.22 s |
| Go | 0.27 to 0.31 s |
| Python | 1.9 to 2.3 s |

C's array of counts is not a like-for-like mirror: its 20,000,000
counting steps are array increments, where the others hash every
character, which likely accounts for its lead (not measured
separately). The legacy
`karac build` cannot build the bench program (the panic above), so
there is no compiled Kāra time. The Kāra program prints the same line
under `karac __mir-llvm-run` in 10 s, compile included; that JITs the
MIR's IR without optimization passes, so it is not a benchmark.

## Compiler findings

No new findings.
