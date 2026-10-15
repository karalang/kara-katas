# 689. Maximum Sum of 3 Non-Overlapping Subarrays

Given an integer array `nums` and an integer `k`, find three subarrays
of length `k` that do not overlap and have the largest sum together, and
return the starting index of each. If several answers have that sum,
return the one that is smallest in lexicographic order.

```
nums = [1,2,1,2,6,7,5,1],   k = 2  ->  [0, 3, 5]
nums = [1,2,1,2,1,2,1,2,1], k = 2  ->  [0, 2, 4]
```

**Constraints:** 1 <= `nums.length` <= 2 x 10^4; 1 <= `nums[i]` <
2^16; 1 <= `k` <= `nums.length` / 3, rounded down.

## Approaches

Every arm is `fn max_sum_of_three_subarrays(nums: Vec[i64], k: i64) ->
Vec[i64]`. Below, a window is a subarray of length k, named by where it
starts.

| file | mechanism |
|---|---|
| `max_sum_of_three_subarrays.kara` ★ | every window's sum once; for each index, the best window starting at or before it and the best at or after it, the earliest on a tie; then every window as the middle one, with the best ending before it and the best starting after it, a strictly larger total keeping the earliest answer; O(n) |
| `max_sum_of_three_subarrays_dp.kara` | a table from the right: the largest sum of t windows that all start at i or later is that for i + 1, or window i plus that of t - 1 windows from i + k; then forward from 0, three times the first start that keeps the best total reachable; O(3n) |
| `max_sum_of_three_subarrays_sliding.kara` | three adjacent windows slid together in one pass, keeping the best first window, the best pair ending at the middle one and the best three ending at the last, each replaced only by a strictly larger sum; O(n) time, O(1) space |
| `max_sum_of_three_subarrays_scan.kara` | every window as the middle one, with all windows on each side searched afresh for the best; O(n^2) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 12 lines: the two LeetCode examples; six
corners: exactly three windows, one value throughout, single values, a
tie between two answers where the smaller must win, a tie between taking
the best window and leaving it out, and the largest values; every array
of 3 to 8 values from 1 to 3 with every k that fits, 19,305 queries,
with a checksum; 300 random arrays of up to 300 values from 1 to
65535, with a checksum; 2,000 random values with k from 1 to 666, the
largest that fits; and 2,000 equal values.
`max_sum_of_three_subarrays.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: every three starts
a, b and c with b >= a + k and c >= b + k, in lexicographic order, each
window summed from scratch; the first with the largest sum. 1,500 random
arrays are checked, two thirds of 3 to 14 values and a third of 3 to
120, with values from 1 to at most 4, so that ties are common, except in
half the large ones, which go up to 1,000; the 1,000 small ones go
against the definition.

| | property |
|---|---|
| P1 | the answer is the definition's (up to 14 values) |
| P2 | the answer is three starts that fit, with a sum that three random starts never beat |
| P3 | every value raised by the same amount changes nothing |
| P4 | the reversed array's answer has the same sum |

It prints `1500 arrays (1000 against the definition), 4 arms,
22000 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a tie on the right taken at the later window | P1 423 |
| M2 | ★: the last middle window never tried | P1 260, P2 245, P4 199 |
| M3 | dp: the next window started one on, not k on | P1 457, P2 792, P4 155 |
| M4 | dp: the first window's sum left at 0 | P1 622, P2 51, P4 433 |
| M5 | sliding: a tie for the triple taken at the later one | P1 508 |
| M6 | sliding: the pair's second start one too early | P1 1000, P2 1007, P4 643 |
| M7 | scan: the left window just before the middle never tried | P1 117, P2 13, P4 173 |
| M8 | scan: the last window never tried | P1 134, P2 8, P4 227 |
| E1 | ★: the best total started at 0 | 0 |
| E2 | dp: a tie in the table taken too | 0 |
| E3 | sliding: the best first window started at -1 | 0 |
| E4 | scan: the left search started at 1 | 0 |

P1 kills all eight. M1 and M5 only break ties the other way, giving a
later answer with the same sum, so P1 alone sees them: P2 and P4 look
only at sums, and raising every value alike keeps every tie. P2 sees the
other six. M3 and M6 can answer windows that overlap, and M2, M4, M7 and
M8 leave some windows out, so a random three starts can beat them,
though seldom for M7 and M8, which lose only one window each. P4 sees
the same six: reversed, the windows a mutant leaves out are other
windows, so its sums differ. P3 sees none: raising every value by the
same amount raises every three windows' sum by the same 3k times it, so
no answer changes, a mutant's included. The four survivors change no
answer. Every sum is at least 1, so a best total or best first window
started at 0 or -1 is passed by the first one tried; a tie in the table
changes none of its values, since each is a maximum; and the left search
already starts with window 0 as its best, so starting the loop at 1 only
skips comparing window 0 with itself.

## Verification

Every arm prints the same output as `max_sum_of_three_subarrays.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. The differential prints its line under all three. `karac check`
passes all four arms, the differential and the bench program. All with
the compiler at kara `968707afd3` for both the debug build and the
release build that runs `check` and `__mir-run`, with runtime archives
rebuilt after the last `runtime/src` change.

The frozen legacy JIT, `karac build` and `KARAC_AUTO_PAR=1` build print
the same output for all four arms, and so does the legacy interpreter,
except on the scan arm, the O(n^2) one, where it was stopped at the
60-second limit. The legacy backends refuse the differential at type
checking, at `*s`, since legacy gives the items of `starts.iter()` by
value where v2 gives references. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 arrays of 20,000 values
from 1 to 65535 once, each with a k from 1 to 1,000, then answers every
array in each of 20 rounds, putting each answer into a checksum. Every
implementation prints `2000 arrays answered, checksum 106014349`, the
Kāra program under `karac __mir-run` included (in 49 s).

Each implementation is the same three passes over freshly allocated
arrays of window sums and best starts for each array. Spot timings on a
shared 4-core container, six runs each, three of them interleaved (two
for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.30 to 0.41 s |
| Rust (`rustc -O`) | 0.30 to 0.37 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.39 to 0.53 s |
| Go | 0.34 to 0.39 s |
| Python | 10.1 to 10.8 s |
| Kāra (`karac build --mir`) | 0.29 to 0.36 s |
| Kāra, legacy (`karac build`, a copy) | 0.25 to 0.43 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program at type checking: `max_sum_of_three_subarrays(arrays[c], ks[c])`
moves an element out of `arrays` under legacy, where a bare parameter is
owned, but v2 borrows it. That edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside the kata whose parameter
is `ref Vec[i64]` builds under legacy, and its row is above. Under
`karac __mir-llvm-run` the program prints the same line in 2.3 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is level with C, Rust, Go and legacy here, within the
spread of the runs. The comparison with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends.
