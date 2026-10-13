# 485. Max Consecutive Ones

Given a binary array `nums`, return the maximum number of consecutive
1s in the array.

```
nums = [1,1,0,1,1,1]  ->  3
nums = [1,0,1,1,0,1]  ->  2
```

**Constraints:** `1 <= nums.length <= 10^5`; `nums[i]` is either `0`
or `1`.

## Approaches

Every arm is `fn find_max_consecutive_ones(nums: Vec[i64]) -> i64`, and
borrows the array.

| file | mechanism |
|---|---|
| `max_consecutive_ones.kara` ★ | a running count of the current run of 1s, reset at every 0, and the largest count kept |
| `max_consecutive_ones_zeros.kara` | the run ending at index `i` starts after the last 0, so its length is `i` minus that 0's index (-1 before the array); `iter().enumerate()` and `max` |
| `max_consecutive_ones_fold.kara` | the whole scan as one `fold`, carrying the pair (current run, best) and destructuring it in the closure's parameter |
| `max_consecutive_ones_jump.kara` | run by run: from each 1 that starts a run, walk to its end, measure it, and carry on from there |
| `differential.kara` | the four arms on 1,500 random arrays, four properties |

Every arm prints the same 9 lines: the two LeetCode examples, a lone 0
and a lone 1, all 0s, all 1s, two mixed arrays (one with two longest
runs), and for 300 random arrays (1 to 60 numbers, 1 with odds of 1 in
2, 3 in 4 or 15 in 16 in turn) the sum of the answers and a checksum.
`max_consecutive_ones.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random arrays `a` of 1 to 25 numbers, with a second array `b` of
0 to 25, at the same three odds.

| | property |
|---|---|
| P1 | the answer is the longest slice of 1s, every slice checked |
| P2 | the array reversed gives the same answer |
| P3 | `a`, then a 0, then `b` gives the larger of `a`'s and `b`'s answers |
| P4 | one number flipped: a 1 turned to 0 never makes the answer larger, and a 0 turned to 1 never smaller |

It prints `1500 cases, 4 arms, 24000 checks, 0 failures` under
`karac __mir-run`, in 1.2 s, and a count for each property when
anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a 0 halves the run instead of ending it | P1 399, P2 410, P3 378 |
| M2 | ★: the best moves only when the run passes it by two | P1 789 |
| M3 | zeros: the 0 before the array is at index 0, not -1 | P1 596, P2 502, P3 259 |
| M4 | zeros: each run is measured one short | P1 1475 |
| M5 | fold: a 0 keeps the run going instead of ending it | P1 1000, P3 1384 |
| M6 | fold: the best lags one step behind the run | P1 1475 |
| M7 | jump: each run is measured one short | P1 1475 |
| M8 | jump: the walk goes on two past the end of a run | P1 367, P2 472, P3 229, P4 49 |

Only P1, which knows the right answer, sees M2, M4, M6 and M7. M4, M6
and M7 answer one less than the truth wherever it is not 0, and M2
rounds it down to an even number: each is a nondecreasing function of
the true answer, so reversing, joining and flipping move it the way
they move the true one. M5 counts
every 1 in the array, which reversal does not change, so P2 is blind to
it too. M8 skips the number just after the 0 that ends a run, and is
the only mutant P4 sees: flipping that skipped number to 1 can lose a
run that started there.

Two first drafts of M8 were equivalent and were replaced: going on from
one past the start of the run rather than from its end (`i += 1`) only
measures the run's own tails again, all shorter, and going on from one
past the end (`i = end + 1`) skips only the 0 that ended the run.

## Verification

All four arms print the same output as `max_consecutive_ones.py`
under `karac __mir-run` (the v2 MIR interpreter) and
`karac __mir-llvm-run`, and `karac check` passes on every file, the
bench program included. The differential prints `24000 checks, 0
failures` on both. The four arms and the differential also run clean
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer):
output identical, no error, no leak.

The frozen legacy backends get the random arrays wrong. Under
`karac run --interp`, LLJIT, legacy `karac build` and a
`KARAC_AUTO_PAR=1` build, the ★ and jump arms print the eight fixed
lines right and then a different last line (`runs add up to 3221,
checksum 737722949`): as on kata 475, legacy calls `next_random` twice
for the bound of `for _ in 0..1 + next_random(mut seed) % 60 { .. }`,
so it draws other arrays. Legacy `karac build` also warns that `nums`
is "moved here, used again here" on those two arms, where `show` lends
the array to `list` and then to the arm. The zeros and fold arms and the
differential do not type-check on legacy, which reads the items of
`nums.iter()` as `i64` and refuses `*x`. Legacy is frozen, so this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 20 arrays of 100,000
numbers (the problem's most), 1 at odds from 80 in 100 to 99 in 100,
once, then scans each 50 times. Every implementation prints `1000 scans
of 100000 numbers: runs add up to 151000, checksum 810313350`, the Kāra
program under `karac __mir-run` included (in 18 s).

Every mirror is the same loop over a plain array of 64-bit integers.
Spot timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.12 s |
| Rust (`rustc -O`) | 0.12 to 0.13 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.22 to 0.29 s |
| Go | 0.25 to 0.27 s |
| Python | 3.2 to 3.5 s |
| Kāra (`karac build`) | 0.21 to 0.24 s |
| Kāra (`karac build --mir`) | 0.21 to 0.24 s |

Both Kāra builds check every `run += 1` for overflow, as Rust does with
`overflow-checks=on`, and land beside that row rather than beside plain
`rustc -O` (inferred, not profiled). The legacy `karac build` builds and
runs this program correctly (its loops have constant bounds), so
`bench.sh` is the `scripts/new-bench.sh` output unchanged and times that
build. The `--mir` row is the v2 compiled backend, timed for
comparison. Both Kāra rows are timed at kara `b0b1557b39`. Under
`karac __mir-llvm-run` the program prints the same line in 0.93 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

None. Every arm, the differential and the bench program ran first time
on the v2 backends.
