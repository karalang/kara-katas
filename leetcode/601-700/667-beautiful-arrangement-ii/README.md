# 667. Beautiful Arrangement II

Given `n` and `k`, return an arrangement of the numbers 1 to `n` whose
differences between neighbours take exactly `k` different values. Any
such arrangement is accepted.

```
n = 3, k = 1  ->  [1,2,3]   (differences 1 and 1)
n = 3, k = 2  ->  [1,3,2]   (differences 2 and 1)
```

**Constraints:** 1 <= `k` < `n` <= 10,000.

## Approaches

Every arm is `fn construct_array(n: i64, k: i64) -> Vec[i64]`. Since any
valid arrangement is accepted, the arms are chosen to build the same
one, the zigzag over 1 to k + 1 followed by the rest in order, so that
every arm prints the same output; they differ in how they build it.

| file | mechanism |
|---|---|
| `beautiful_arrangement_ii.kara` ★ | 1 to k + 1 taken alternately from the low end and the high end, then k + 2 to n in order; O(n) |
| `beautiful_arrangement_ii_formula.kara` | each place by a closed form: `i / 2 + 1` at an even place, `k + 1 - i / 2` at an odd one, `i + 1` past `k`; O(n), filled in place |
| `beautiful_arrangement_ii_steps.kara` | a walk from 1 by steps of k, k - 1, ..., 1, alternately up and down, then on to k + 2 and up by 1; O(n) |
| `beautiful_arrangement_ii_interleave.kara` | the lower half of 1 to k + 1 rising and the upper half falling, dealt out one from each in turn; O(n) |
| `differential.kara` | the four arms against a reference built by turning stretches of 1 to n back to front, four properties |

Every arm prints the same 12 lines: the two LeetCode examples; six small
cases (the smallest, `n` = 2; every difference from 1 to 5 at `n` =
6; one difference at `n` = 7; `k` odd and even at `n` = 8; and `n` =
12, `k` = 7), each with its arrangement; the problem's largest `n`,
10,000, with `k` at 1, 5,000 and 9,999, each with its ends and a
checksum; and how many of 1,000 random cases with `n` from 2 to 61 come
out with exactly `k` differences, with a checksum of every arrangement.
Each line also counts the differences. `beautiful_arrangement_ii.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and a reference that
reaches the same arrangement by another road: start from 1 to n in order
and, for each place `i` from 1 to k - 1, turn the stretch from `i` to
`k` back to front; O(n + k^2). The properties check the problem's own
conditions as well as agreement, by counting the differences afresh,
each against every earlier one. The 2,000 cases are every `k` for `n`
from 2 to 12, then random cases with `n` from 2 to 41 and `k` from 1 to
n - 1.

| | property |
|---|---|
| P1 | the answer holds each of 1 to n exactly once |
| P2 | its differences take exactly k values |
| P3 | it is the reference's arrangement |
| P4 | no difference is larger than k |

It prints `2000 cases (42527 numbers), 4 arms, 32000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the high end starting at k | P1 2000, P2 1732, P3 2000, P4 187 |
| M2 | ★: the tail starting at k + 1 | P1 2000, P2 242, P3 2000 |
| M3 | formula: the odd places counting down from k | P1 2000, P2 436, P3 2000, P4 187 |
| M4 | formula: the tail starting at place k | P1 1758, P2 262, P3 1758 |
| M5 | steps: the first step k - 1 | P1 2000, P2 1732, P3 2000, P4 187 |
| M6 | steps: the first step down | P1 2000, P2 1768, P3 2000, P4 1768 |
| M7 | interleave: the lower half one short | P1 926, P2 159, P3 926 |
| M8 | interleave: the upper half falling from k | P1 2000, P2 1732, P3 2000, P4 187 |
| E1 | ★: the tail starting after however many are out | 0 |
| E2 | formula: even places from (i + 1) / 2 | 0 |
| E3 | steps: up when an even number of steps are taken | 0 |
| E4 | interleave: a high one dealt while out is short of k + 1 | 0 |

P1, P2 and P3 kill all eight: every mutant leaves a number out or
repeats one, which P1 and P3 see in every case it touches, and P2 sees
whenever that changes how many differences there are. P4 sees five.
M6 walks below 1, taking long steps everywhere; M1, M3, M5 and M8 leave
out k + 1, and in the cases P4 sees, the step from the zigzag's last
number into the tail at k + 2 is then longer than k. M2, M4 and
M7 repeat or leave out a number without any step growing past k, so
P4 misses them. The four survivors cannot change an answer: the zigzag
is exactly k + 1 numbers long, so the tail starts at `out.len() +
1`; `(i + 1) / 2` and `i / 2` agree at even places; the steps go up
after an even number of steps taken; and a high number is dealt exactly
while fewer than k + 1 are out.

## Verification

Every arm prints the same output as `beautiful_arrangement_ii.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` for the debug build and `72739d54d6` for the release build
that runs `check` and `__mir-run`, with runtime archives newer than the
last `runtime/src` change.

The frozen legacy backends print the same output for every arm under the
interpreter, the JIT and `karac build`, with and without
`KARAC_AUTO_PAR=1`, and run the differential to the same line under the
interpreter, the JIT and `karac build`.

## Benchmarks

The bench program uses the ★ arm. Each of 10,000 rounds builds the
arrangement for the problem's largest `n`, 10,000, with `k` stepping
through 1 to 9,999 by the round, and puts every number of it into a
checksum. Every implementation prints `n = 10000, 10000 rounds: checksum
783821184`, the Kāra program under `karac __mir-run` included (in
170 s).

Each implementation is the same zigzag into a fresh array for each
round: Kāra's and Rust's a `Vec` grown by `push`, Go's a slice grown by
`append`, Python's a list grown by `append`, and C's one `malloc`ed
block of `n` numbers, which never grows. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.55 to 0.56 s |
| Rust (`rustc -O`) | 0.63 to 0.66 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.68 to 0.69 s |
| Go | 1.40 to 1.42 s |
| Python | 8.0 to 8.3 s |
| Kāra (`karac build --mir`) | 0.65 to 0.66 s |
| Kāra, legacy (`karac build`) | 0.62 to 0.78 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the frozen legacy `karac build` builds it too, and
its row is above. Under `karac __mir-llvm-run` the program prints the
same line in 2.5 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

So the v2 build is level with legacy and Rust and about a fifth behind
C, whose array is allocated once at its full size rather than grown. Go
is behind; it has not been profiled. The comparison with C and Rust
waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends.
