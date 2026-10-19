# 761. Special Binary String

A special binary string has as many 0s as 1s, and every prefix of it has
at least as many 1s as 0s. A move swaps two consecutive, non-empty
special substrings of a special string `s`. Return the lexicographically
largest string that moves can make.

```
"11011000"  ->  "11100100"
"10"        ->  "10"
```

**Constraints:** 1 <= `s.length` <= 50; `s` is a special binary string.

## Approaches

A special string is a run of mountains, each a 1, a special string and a
0. Moves can put the mountains at any one level in any order, so the
first three arms make each mountain's inside as large as it can be and
put the mountains in descending order.

| file | mechanism |
|---|---|
| `special_binary_string.kara` ★ | split `s` into its mountains, make each one's inside largest by recursion, sort them in descending order and join them; O(n^2) |
| `special_binary_string_stack.kara` | one pass with a stack of levels: a 1 opens a level, and a 0 sorts the level's mountains and wraps them as one mountain of the level below; no recursion |
| `special_binary_string_tree.kara` | parse `s` into a tree of mountains held in arrays, then give each node its largest form, children before parents |
| `special_binary_string_climb.kara` | make the moves: while swapping two consecutive special substrings would make the string larger, swap them; it stops only when no level has two neighbouring mountains out of order |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 9 lines: the two LeetCode examples; one
mountain inside another; two mountains in the wrong order; four equal
mountains; one mountain holding two; and two longer strings, one
reordered at two levels and one at the top level only; then 300 random
special strings of up to 50 characters, with the number whose answer
differs from the string itself and a checksum of the answers.
`special_binary_string.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which visits every string that moves can reach, breadth first, and keeps
the largest. 1,500 random special strings of up to 14 characters are
checked against it, and 300 of up to 50 against the other properties.

| | property |
|---|---|
| P1 | the answer is the definition's (the 1,500 short strings) |
| P2 | it is a special string as long as `s`, no smaller than `s`, and its own answer |
| P3 | one random move made first changes nothing |
| P4 | wrapping `s` in a 1 and a 0 wraps the answer the same way |

It prints `1800 strings (833 changed), 4 arms, 27600 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error; the count of changed strings is
the ★ arm's.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: mountains in ascending order | P1 739, P2 510 |
| M2 | ★: a mountain's inside not made largest | P1 163, P3 239, P4 680 |
| M3 | ★: each next mountain read from one character early | P1 654, P2 906, P3 498 |
| M4 | stack: a level's mountains sorted longest first | P3 2, P4 25 |
| M5 | stack: the bottom level left unsorted | P1 467, P3 575, P4 679 |
| M6 | stack: the bottom level sorted ascending | P1 589, P2 387, P4 813 |
| M7 | tree: a mountain's inside written after it | P1 1061, P2 1334, P4 1800 |
| M8 | tree: every child given its first sibling's form | P1 739, P2 983, P3 498 |
| M9 | tree: the last mountain never given its form | P1 1500, P2 1800, P3 611 |
| M10 | climbing: swaps that make the string smaller | P1 739, P2 510 |
| M11 | climbing: a special substring's end taken one short | P1 585, P3 814 |
| M12 | climbing: swaps only at the start | P1 176, P3 320, P4 653 |
| E1 | ★: a 1 tested as not a 0 | 0 |
| E2 | stack: sorted ascending, then reversed | 0 |
| E3 | climbing: no swap tried from the last character | 0 |

P1 kills all but M4, which sorts each level's mountains longest first.
That agrees with descending order unless a shorter mountain is the
larger, as `111000` is beside `11010100`, which takes 14 characters at
one level and so is rare among the short strings; P3 and P4 see it
27 times on the long ones. M1 and M10 fail identically, since both
arrive at the smallest string the moves can make, and M11 leaves every
string as it is, which P2 and P4 cannot tell from a largest one. The
first edit tried for M11 compared a swap only over the length of its
second part; it survived, presumably because the swaps it then misses
can be made in another order that it still finds (inferred, not proved),
so it was replaced. E1 tests for a 1 as not a 0, and the strings hold
nothing else; E2 sorts ascending and reverses, which is descending
order, since equal mountains are the same string; E3 tries no swap from
the last character, where no two special substrings, four characters at
least, can start.

## Verification

Every arm prints the same output as `special_binary_string.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`a62eacd307`, whose last compiler change is `7d736aae75`. This paragraph
said the runtime archives were built after the last runtime change,
`b09cd37112`; in fact they predated a later one, `176f59738b`, which
changed only the order in which the runtime's merge sort makes its
merges, so it could not change any result here. Every arm and the
differential were checked again at kara `8a2af7d554`, whose last
compiler change is `60d9973e03`, with the archives rebuilt after
`176f59738b`: each prints the same under `karac __mir-llvm-run` and
`karac __mir-llvm-asan` with no error, and the bench program built by
`karac build --mir` prints the same line. The timings below are from the
earlier build.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept the ★ and stack arms and the bench:
each arm prints the same output under the legacy interpreter, `karac
run`, `karac build` and an auto-par build. They refuse the tree and
climbing arms and the differential at a `*` over an element of `iter()`
(`form[*child]`, `out.push(*ch)`), which legacy gives by value where
v2 gives references. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages, on
200,000 random special strings of 50 characters, the most LeetCode
allows, adding up the leading 1s of the answers and a checksum. Every
implementation prints `200000 strings of 50 characters: 1516085 leading
1s, checksum 103558768`, the Kāra program under `karac __mir-run`
included (in 82 s). C builds each mountain in its own `malloc`'d buffer
and sorts with `qsort` and `strcmp`; Rust and Go build strings as the
Kāra program does.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.52 to 0.69 s |
| Rust (`rustc -O`) | 0.79 to 1.35 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.91 to 1.01 s |
| Go | 1.05 to 1.20 s |
| Python | 7.1 to 8.0 s |
| Kāra (`karac build --mir`) | 1.13 to 1.27 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
6.1 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 1.16 s,
against C's 0.54, Rust's 0.82 (0.94 under overflow checks) and Go's
1.15. Under valgrind's cachegrind v2 runs 9.4 billion instructions, Rust
6.8 billion and C 4.2 billion. The legacy build of the same program ran
0.97 to 1.19 s, a median of 0.99 s in the interleaved runs, so v2 takes
1.2 times as long as legacy, inside M2's limit of twice legacy; new
katas' benches are outside M2's frozen set in any case. The comparison
with C and Rust waits until after M4.

## Compiler findings

None new.
