# 674. Longest Continuous Increasing Subsequence

Given an unsorted array of integers `nums`, return the length of its
longest continuous strictly increasing subsequence: the longest stretch
of neighbouring numbers in which each is larger than the one before.

```
[1, 3, 5, 4, 7]  ->  3   ([1, 3, 5])
[2, 2, 2, 2, 2]  ->  1   (each [2] alone)
```

**Constraints:** 1 <= `nums.length` <= 10,000; -10^9 <= `nums[i]` <=
10^9.

## Approaches

Every arm is `fn find_length_of_lcis(nums: Vec[i64]) -> i64`. The rising
stretches never overlap and between them cover the array, so every arm
finds them in one pass.

| file | mechanism |
|---|---|
| `longest_continuous_increasing_subsequence.kara` ★ | one pass keeping the length of the run that ends at each place; O(n) |
| `longest_continuous_increasing_subsequence_starts.kara` | from each run's start, a scan to its end, and the next run starts there; O(n) |
| `longest_continuous_increasing_subsequence_lengths.kara` | a table of the run length ending at each place, the largest taken with a fold and a closure; O(n) time and space |
| `longest_continuous_increasing_subsequence_breaks.kara` | the places where a run breaks, with both ends, and the widest gap between neighbours; O(n) |
| `differential.kara` | the four arms against every stretch checked pair by pair, five properties |

Every arm prints the same 16 lines: the two LeetCode examples and
thirteen corners, among them one and two numbers, rising and falling
runs, repeats, a run in the middle and one at the end, the problem's
extreme values, and 10,000 numbers, the problem's longest, rising,
falling, and climbing 0 to 99 over and over; and a checksum of
1,000 random arrays of up to 1,000 numbers, spread over 3, 30 or the
whole range, with the longest answer among them.
`longest_continuous_increasing_subsequence.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which checks every stretch from `i` to `j` pair by pair and keeps the
longest that rises throughout. 3,000 random arrays of up to 30 numbers,
spread over 3, 10 or 1,000 values so that repeats range from common to
rare, are all held to it and to four more properties.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | it is between 1 and the array's length |
| P3 | the array reversed and negated has the same answer |
| P4 | cut in two at a random place, the answer is at least the larger half's and at most the two halves' added |
| P5 | a number no larger than the last, appended, leaves the answer |

It prints `3000 arrays, 4 arms, 60000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an equal number extends the run | P1 1290, P5 261 |
| M2 | ★: a new run starts at 0 | P1 3000, P2 223, P4 143 |
| M3 | starts: the scan begins a place late | P1 1706, P2 111, P3 979, P4 139 |
| M4 | starts: a run counted one short | P1 3000, P2 223, P4 143 |
| M5 | lengths: the first pair never compared | P1 245, P3 355, P4 14 |
| M6 | lengths: the last entry taken, not the largest | P1 2119, P3 1603, P4 601, P5 1217 |
| M7 | breaks: the end break one place early | P1 329, P2 111, P3 355, P4 130, P5 329 |
| M8 | breaks: an equal number not a break | P1 1290, P5 261 |
| E1 | ★: the run starts at 1 | 0 |
| E2 | starts: every place tried as a start | 0 |
| E3 | lengths: one entry too many in the table | 0 |
| E4 | breaks: the start break listed twice | 0 |

P1 kills all eight, each on hundreds of arrays or more. M1 and M8 let an
equal number continue a run, and P5 sees them too, since an equal number
appended can then lengthen the last run. P3, the mirror, sees the
mutants that treat the two ends differently: M5 skips the array's first
comparison and M3 every run's, M6 takes the run at the end, and M7 cuts
the last run short. M2 and M4, which count every run one short, break
P2 and P4 only where the answer falls to 0 or the halves add up wrong.
The four survivors cannot change an answer: the ★ arm's first place sets
the run to 1 whatever it started at; trying every place as a start finds
every run, only more slowly; a spare entry of 1 is never larger than the
answer, which is at least 1; and a break listed twice makes a gap of 0.

## Verification

Every arm prints the same output as
`longest_continuous_increasing_subsequence.py` under `karac __mir-run`
(the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs clean
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer):
output identical, no error, no leak. The differential prints its line
under all three. `karac check` passes all four arms, the differential
and the bench program. All with the compiler at kara `8d40e1a762` for
the debug build and `85dccd703c` for the release build that runs `check`
and `__mir-run`, with runtime archives newer than the last `runtime/src`
change.

The frozen legacy backends print the same output for every arm under the
interpreter, the JIT and `karac build`, with and without
`KARAC_AUTO_PAR=1`; `karac build` warns that `nums` is moved into `show`
and used again, and builds anyway. They run the differential to the same
line under the interpreter, the JIT and `karac build`.

## Benchmarks

The bench program uses the ★ arm. It builds 100 arrays of
10,000 numbers, the problem's longest, each number below 1,000 from the
same generator in every language, once. Each of 20,000 rounds sets one
number of one array, so that no round repeats an earlier one, and then
measures that array; each answer goes into a checksum. Every
implementation prints `20000 rounds over 100 arrays of 10000: checksum
772275678`, the Kāra program under `karac __mir-run` included (in 96 s).

Each implementation is the same pass, a comparison, an increment and a
maximum per number, over arrays built once, so this measures that loop.
Spot timings on a shared 4-core container, three runs each, the two Kāra
rows and checked Rust on a quiet machine (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.17 to 0.20 s |
| Rust (`rustc -O`) | 0.17 to 0.19 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.96 to 1.00 s |
| Go | 0.97 to 1.05 s |
| Python | 29.6 to 30.5 s |
| Kāra (`karac build --mir`) | 0.95 to 0.99 s |
| Kāra, legacy (`karac build`, a copy) | 0.98 to 1.06 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program at type checking: `find_length_of_lcis(all[a])` moves an element
out of `all`, because under legacy a bare parameter is owned, where
v2 borrows it. That edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside the kata whose parameter
is `ref Vec[i64]` builds under legacy, and its row is above. Under
`karac __mir-llvm-run` the program prints the same line in 3.6 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is level with legacy, with Rust under
`overflow-checks=on` and with Go, and about five times plain Rust and C.
That checked Rust lands with Kāra suggests the checked increment of the
run length is what costs it, the equal-safety tie BENCHMARKS.md
describes; but Go checks nothing and is as slow, so that is inferred,
not shown, and nothing here has been profiled. The comparison with C and
Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends.
