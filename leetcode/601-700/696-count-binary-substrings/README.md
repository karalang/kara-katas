# 696. Count Binary Substrings

Given a binary string `s`, return the number of non-empty substrings
that have the same number of 0's and 1's, with all the 0's and all the
1's in each substring grouped consecutively. Substrings that occur more
than once are counted each time they occur.

```
s = "00110011"  ->  6    ("0011", "01", "1100", "10", "0011", "01")
s = "10101"     ->  4    ("10", "01", "10", "01")
```

**Constraints:** 1 <= `s.length` <= 10^5; `s[i]` is '0' or '1'.

## Approaches

Every arm is `fn count_binary_substrings(s: String) -> i64`.

| file | mechanism |
|---|---|
| `count_binary_substrings.kara` ★ | a wanted substring sits across the border of two runs, and runs of lengths a and b hold min(a, b) of them; one pass keeps the run before and the current one; O(n) time, O(1) space |
| `count_binary_substrings_groups.kara` | the run lengths written into a `Vec` first, then min of each neighbouring pair added; O(n) time and space |
| `count_binary_substrings_center.kara` | from each border, step out one character each way while the left side repeats the character left of the border and the right side the one right of it; each step is one substring; O(n) |
| `count_binary_substrings_start.kara` | a wanted substring is fixed by where it starts: the run from there, a long, then a of the other character; each start gives one or none; O(n x longest run) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 7 lines: the two LeetCode examples;
`0`, `01` and `0000`; `000111` and `0001111`; 2,000 zeros then
2,000 ones, and 100,000 characters alternating; 100,000 characters in
random runs of 1 to 20; and 300 random strings of up to
2,000 characters, in runs of up to 1 to up to 50, with a checksum.
`count_binary_substrings.py` mirrors the ★ arm and its output is
byte-identical. The start arm is quadratic on a string of two long runs,
so the largest cases keep their runs short.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: go through every
substring and count it when it has an even length, its first half is one
character throughout and its second half the other. 3,000 random strings
of 1 to 30 characters are checked, each with its own chance of a run
going on, so some are all one run and some alternate at every step.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | 0s and 1s swapped, the answer is the same |
| P3 | read backwards, the answer is the same |
| P4 | every character written twice doubles the answer |

It prints `3000 strings, 4 arms, 48000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last border left out | P1 2612, P3 703 |
| M2 | ★: the longer of two runs added, not the shorter | P1 2612, P3 1734 |
| M3 | ★: the run before always taken as one long | P1 1517, P4 2612 |
| M4 | groups: the first run of each pair added whole | P1 2055, P3 1459 |
| M5 | groups: the first border skipped | P1 2612, P3 703 |
| M6 | groups: each run one too long | P1 2612, P4 2612 |
| M7 | center: the left side never checked | P1 1783, P3 1437 |
| M8 | center: growing from inside runs, not from borders | P1 2752, P4 3000 |
| M9 | center: the left side stepping two at a time | P1 1649, P3 1410, P4 2361 |
| M10 | start: no substring that ends the string | P1 1859, P3 1031, P4 1859 |
| M11 | start: the last character of the second half unchecked | P1 1800, P3 1137, P4 1800 |
| M12 | start: the second half tested for the same character | P1 2612 |

P1 kills all twelve; 2,612 of the strings have at least one border, so a
mutant wrong at every border fails all of them. P2 sees none: every arm
treats 0 and 1 alike, a mutant's included. P3 sees the mutants that
treat the two ends of the string or the two sides of a border unlike,
such as leaving out the last border (M1), which reversed becomes the
first. P4 sees the mutants whose error does not double along with the
runs: a run taken as one long (M3), a run one too long (M6), growing
from inside runs or two steps at a time on one side (M8, M9), and the
start arm's slips at the end of the string (M10, M11).

## Verification

Every arm prints the same output as `count_binary_substrings.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`f6a225c404` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives rebuilt after the last
`runtime/src` change.

The frozen legacy backends refuse all four arms at type checking, at
`next_random(mut seed)` inside the harness's `random_runs`, whose `seed`
is already a `mut ref`: legacy wants the marker dropped, while on v2 the
marked forward is the spelling (kara B-2026-10-14-25). They run the
differential, under `karac run --interp` and `karac build`, and build
the bench program as it is. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm, the same in all five languages. It
builds 20 strings of 100,000 characters once, the k-th in random runs of
1 to 2k + 1, then counts each string's substrings in each of 150 rounds,
putting each count into a checksum. Every implementation prints
`150 rounds of 20 strings of 100000: 212508600 substrings counted,
checksum 214711956`, the Kāra program under `karac __mir-run` included
(in 168 s).

Each implementation reads the bytes of a string it does not copy:
`s.bytes()` in Kāra is a view, as `as_bytes()` is in Rust. Spot timings
on a shared 4-core container, eight runs of each compiled program, five
of them interleaved, and two of Python (`bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.34 to 0.43 s |
| Rust (`rustc -O`) | 0.38 to 0.49 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.46 to 0.61 s |
| Go | 0.45 to 0.59 s |
| Python | 19.3 to 19.4 s |
| Kāra (`karac build --mir`) | 0.46 to 0.56 s |
| Kāra, legacy (`karac build`) | 0.42 to 0.59 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` builds the same file, and
its row is above. That edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 2.9 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

So the v2 build is level with legacy, Go and Rust with overflow checks
here, and a little behind C and plain Rust. The comparison with C and
Rust waits until after M4.

## Compiler findings

None. `karac check` passed all four arms, the harness, the differential
and the bench program as first written.
