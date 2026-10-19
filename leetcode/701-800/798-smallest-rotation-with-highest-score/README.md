# 798. Smallest Rotation with Highest Score

Given an array `nums`, rotating it by `k` gives `nums[k], nums[k + 1],
..., nums[n - 1], nums[0], ..., nums[k - 1]`. After the rotation every
number no greater than its index scores a point. Return the rotation `k`
with the highest score, the smallest one when several tie.

```
nums = [2, 3, 1, 4, 0]  ->  3   (rotation 3 is [4, 0, 2, 3, 1], scoring 4)
nums = [1, 3, 0, 2, 4]  ->  0   (every rotation scores 3)
```

**Constraints:** 1 to 100,000 numbers, each from 0 to `n - 1`.

## Approaches

| file | mechanism |
|---|---|
| `best_rotation.kara` ★ | rotating by `k` puts `nums[i]` at index `(i - k) mod n`, so it scores for the `k` from `i + 1` round to `i - nums[i]`, a run that may wrap past `n - 1`; add 1 over each run in a difference array, add it up and take the first `k` with the most; O(n) |
| `best_rotation_running.kara` | the next rotation moves the front number to the back, where it always scores, and every other number down one place, so the number then at the index equal to its value stops scoring: count those numbers for each `k` first, and each score is the one before less that count plus one; O(n) |
| `best_rotation_count.kara` | for each `k`, count the numbers whose index after the rotation is at least the number; O(n²) |
| `best_rotation_turn.kara` | keep the numbers in a double-ended queue, score them as they stand and move the front one to the back, `n` times; O(n²) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 9 lines: LeetCode's two examples; one number;
all zeros, where every rotation scores all; all `n - 1`, where every
rotation scores one; 0 to 4 in order and backwards; `[1, 0]`; and 300
random arrays of 1 to 60 numbers below a bound of 1 to `n`, with the
rotations added up and a checksum. `best_rotation.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
build each rotation as a new array, score it, and take the first of the
best. Its 1,600 cases have 1 to 40 numbers in four kinds of 400: numbers
anywhere below `n`, numbers below 3, numbers within 3 of `n - 1`, and
numbers all 0 or all 0 and `n - 1`, so that many rotations tie.

| | property |
|---|---|
| P1 | the rotation is the definition's |
| P2 | the best rotation of `nums` turned by `r`, taken back by `r`, scores the most for `nums` |
| P3 | lowering a number takes nothing from the best score, and the rotation found for the lowered array scores the most for it |
| P4 | the rotation is one of 0 to `n - 1` and scores at least the average over all rotations |

It prints `1600 cases (rotations adding up to 6143), 4 arms, 25600
checks, 0 failures` under `karac __mir-run` and `karac __mir-llvm-run`,
and the same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last rotation not looked at | P1 30, P2 23, P3 37, P4 9 |
| M2 | ★: each run one rotation short | P1 1194, P2 1189, P3 1188, P4 523 |
| M3 | ★: a tie going to the later rotation | P1 1309 |
| M4 | running: the front number not scoring at the back | P1 993, P2 992, P3 1007, P4 658 |
| M5 | running: numbers counted at i + nums[i] | P1 1069, P2 896, P3 904, P4 545 |
| M6 | running: the count read one rotation late | P1 1194, P2 1189, P3 1188, P4 523 |
| M7 | count: the index taken as (i + k) mod n | P1 850, P2 801, P3 816, P4 494 |
| M8 | count: a number scoring only below its index | P1 1194, P2 1189, P3 1188, P4 523 |
| M9 | count: a tie going to the later rotation | P1 1309 |
| M10 | turn: the ring turned the other way | P1 850, P2 801, P3 816, P4 494 |
| M11 | turn: a number scoring only below its index | P1 1194, P2 1189, P3 1188, P4 523 |
| M12 | turn: the rotation one after the best | P1 1556, P2 827, P3 821, P4 446 |

P1 kills all twelve. P2, P3 and P4 kill the ten that score the rotations
wrongly and miss the two that only break a tie the wrong way, since the
rotation they give scores the most all the same; a later rotation of a
tie is what P1 alone sees. Leaving out the last rotation is seen in few
cases, those whose only best rotation is `n - 1`.

Several edits that look like mutations are not, and were swapped for
these: leaving out the ★ arm's fix for a run that wraps, changing its
test for one, starting every run a rotation late, or counting the
running arm's first score with `<` for `<=`. Each changes every
rotation's score by the same amount, so the best rotation stays where it
was. The first two add or take 1 from the whole array for each run that
wraps; the third drops, for each number, the one rotation that puts it
at index `n - 1`, and every rotation puts exactly one number there.

## Verification

Every arm prints the same output as `best_rotation.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`101ab94117`, whose last compiler change is `f0ec11cf9d`. The runtime
archives were built after the last runtime change, `216d20e28a`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept the ★, running and count arms
unchanged and print the same output under the legacy interpreter (`karac
run --interp`), the legacy JIT (`karac run`), `karac build` and an
auto-par build. Legacy's checker refuses the turn arm and the
differential for the `*` on each number read from `nums.iter()`, which
it takes as a copied `i64`; copies without those `*`s print the same
output under all four, the differential's with a warning that `nums` is
moved and used again, which it runs right regardless. Legacy refuses the
bench program's `best_rotation(arrays[r % 16])` as a move out of an
index; a copy with `nums` written `ref Vec[i64]` and the array bound
with `ref arrays[r % 16]` first builds and prints the same line, and the
bench timing below is of it. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 16 arrays of
100,000 numbers, LeetCode's longest, are made once, each number below a
bound of 1 to 100,000 drawn for its array. Each of 4,000 rounds finds
the best rotation of the next one. Every implementation prints `4000
rounds of 100000 numbers: rotations adding up to 226410000, checksum
770050519`, the Kāra program under `karac __mir-run` included (in 480
s).

The bench measures two passes over a long array: one that scatters
increments into a second array at places set by the numbers, and one
that adds it up keeping the best. Spot timings on a shared 4-core
container, eight runs of each compiled program, five of them
interleaved, and two of Python (`bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 2.09 to 2.41 s |
| Rust (`rustc -O`) | 2.23 to 2.61 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.46 to 2.81 s |
| Go | 4.43 to 4.84 s |
| Python | 95.12 to 95.53 s |
| Kāra (`karac build --mir`) | 2.76 to 3.32 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 10.8 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 2.81 s,
against C's 2.24, Rust's 2.35 (2.53 under overflow checks) and Go's
4.59. Under valgrind's cachegrind v2 runs 27.9 billion instructions and
8.82 billion branches, against C's 15.1 billion and 4.20 billion and
Rust's 16.9 billion and 5.00 billion; all three mispredict the same 62
million branches. The legacy build of the copy ran 2.51 to 2.80 s, a
median of 2.70 s in the interleaved runs, so v2 takes 1.04 times legacy.
The comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new in v2.
