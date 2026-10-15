# 672. Bulb Switcher II

A room has `n` bulbs, numbered from 1 and all on, and four buttons: one
flips every bulb, one the even-numbered, one the odd-numbered, and one
those numbered `3k + 1`. Return how many different states the bulbs can
be in after exactly `m` presses.

```
n = 1, m = 1  ->  2   ([off], [on])
n = 2, m = 1  ->  3   ([off,off], [on,off], [off,on])
n = 3, m = 1  ->  4
```

**Constraints:** 1 <= `n` <= 1,000; 0 <= `m` <= 1,000.

## Approaches

Every arm is `fn flip_lights(n: i64, m: i64) -> i64`. Presses commute
and a button pressed twice undoes itself, so only which buttons are
pressed an odd number of times matters: 16 sets at most. The buttons'
patterns repeat every 6 bulbs, so the first 6 decide the rest.

| file | mechanism |
|---|---|
| `bulb_switcher_ii.kara` ★ | the answers worked out by hand: 1 with no presses, 2 for one bulb, 3 or 4 for two, and 4, 7 or 8 from three bulbs on; O(1) |
| `bulb_switcher_ii_presses.kara` | the states of the first 6 bulbs as 6-bit numbers, pressed m times over, keeping the distinct results, stopping once the sets repeat every other press; O(64 * 4) a press |
| `bulb_switcher_ii_subsets.kara` | each set of buttons whose size k has k <= m and m - k even, applied to the first 6 bulbs, distinct results counted; O(16 * 6) |
| `bulb_switcher_ii_whole.kara` | the same sets applied to all n bulbs, no shortcut, the results compared whole; O(16 * 16 * n) |
| `differential.kara` | the four arms against every sequence of presses played out, five properties |

Every arm prints the same 16 lines: the three LeetCode examples; a table
of the answers for `n` from 1 to 8 and `m` from 0 to 6, a line for each
`n`; the problem's largest, 1,000 bulbs with 1,000 presses, and three of
its corners; and a checksum of 1,000 random cases up to 1,000 bulbs and
1,000 presses. `bulb_switcher_ii.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which plays out every sequence of exactly m presses, all 4^m of them, on
all n bulbs, and counts the distinct results. That is affordable for
every `n` from 1 to 10 with every `m` from 0 to 6, which all 70 are
checked against it. A further 1,000 random cases, `n` and `m` up to
1,000, are held to the other four properties.

| | property |
|---|---|
| P1 | the answer is the definition's (small cases only) |
| P2 | from 6 bulbs on, the answer is the same as with 6 |
| P3 | it is at most 8, and at most 2^n |
| P4 | one more bulb gives no fewer states |
| P5 | two more presses give no fewer states, since a pair of presses can undo itself |

It prints `1070 cases (70 against the definition), 4 arms, 17400 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: two bulbs and one press counted as four | P1 1 |
| M2 | ★: two presses counted as eight | P1 8 |
| M3 | presses: the 3k + 1 button on the 3k bulbs | P1 1 |
| M4 | presses: one press fewer played out | P1 27 |
| M5 | subsets: any set of up to m buttons allowed | P1 17 |
| M6 | subsets: only the first 2 bulbs looked at | P1 48 |
| M7 | whole: a set pressed exactly m times only | P1 47, P5 40 |
| M8 | whole: every state counted, repeats included | P1 12, P3 11 |
| E1 | subsets: the first 4 bulbs looked at | 0 |
| E2 | presses: the parity of the presses left ignored | 0 |
| E3 | subsets: the parity tested by a remainder of the sum | 0 |
| E4 | whole: the sets counted down | 0 |

P1 kills all eight, some on a single case of the 70: M1 changes only two
bulbs with one press, and M3, the fourth button moved onto bulbs
3, 6, 9 and so on, changes only one count. The answers take so few
values, 1 to 8, that the other properties seldom see a wrong one.
P5 sees M7, which allows a set of buttons only when it has exactly m of
them, so more presses can give fewer states; P3 sees M8, which counts
repeats and so can pass 8. P2 and P4 see none. The four survivors cannot
change an answer: the first 4 bulbs decide the rest as well as the first
6 do, since the first 3 already do; `m + k` and `m - k` are odd
together; the order in which the sets are tried does not matter; and,
the most interesting, once the presses arm's sets repeat every other
press, both of the two alternating sets hold the same number of states,
so the correction for the parity of the presses left changes which
states are reachable but never how many.

## Verification

Every arm prints the same output as `bulb_switcher_ii.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` for the debug build and `85dccd703c` for the release build
that runs `check` and `__mir-run`, with runtime archives newer than the
last `runtime/src` change.

The frozen legacy backends print the same output for every arm under the
interpreter, the JIT and `karac build`, with and without
`KARAC_AUTO_PAR=1`, and run the differential to the same line under the
interpreter, the JIT and `karac build`.

## Benchmarks

The bench program uses the ★ arm. It asks 100,000,000 questions over the
problem's whole range, the `i`-th about `1 + i % 1000` bulbs and `i /
1000 % 1001` presses, and puts each answer into a checksum. Every
implementation prints `100000000 queries: checksum 865212110`, the Kāra
program under `karac __mir-run` included (in 57 s).

Each implementation is the same few comparisons, with no allocation, so
this measures little beyond the loop, the division and the checksum.
Spot timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.54 to 0.56 s |
| Rust (`rustc -O`) | 0.55 to 0.58 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.56 to 0.58 s |
| Go | 0.51 to 0.57 s |
| Python | 18.8 to 19.3 s |
| Kāra (`karac build --mir`) | 0.53 to 0.54 s |
| Kāra, legacy (`karac build`) | 0.53 to 0.55 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the frozen legacy `karac build` builds it too, and
its row is above. Under `karac __mir-llvm-run` the program prints the
same line in 2.5 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

So the v2 build is level with legacy, C, Rust and Go: all five are the
same loop of comparisons and a division. The comparison with C and Rust
waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends.
