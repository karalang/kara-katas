# 487. Max Consecutive Ones II

Given a binary array `nums`, return the maximum number of consecutive
1s in the array if you can flip at most one 0.

```
nums = [1,0,1,1,0]    ->  4
nums = [1,0,1,1,0,1]  ->  4
```

**Constraints:** `1 <= nums.length <= 10^5`; `nums[i]` is either `0`
or `1`.

**Follow-up:** what if the input numbers come in one by one as an
infinite stream, and you cannot store them all?

## Approaches

Every arm is `fn find_max_consecutive_ones(nums: Vec[i64]) -> i64`, and
borrows the array.

| file | mechanism |
|---|---|
| `max_consecutive_ones_ii.kara` ★ | two counts: the 1s since the last 0, and the run before that 0 plus the 0 itself; their sum is the best run ending here. One pass and two numbers of state, so it answers the follow-up |
| `max_consecutive_ones_ii_window.kara` | a window grown to the right, its left edge moved past the first 0 whenever it holds a second |
| `max_consecutive_ones_ii_states.kara` | the longest run ending here with no 0 flipped and with one: a 1 extends both, a 0 ends the first and starts the second after it |
| `max_consecutive_ones_ii_sides.kara` | for each index, the 1s just before it and just after it, in two arrays; each 0 flipped is the sum plus one, and an array with no 0 is its own length |
| `differential.kara` | the four arms on 1,500 random arrays, five properties |

Every arm prints the same 9 lines: the two LeetCode examples, a lone 0
and a lone 1, all 0s, all 1s, the two mixed arrays of kata 485, and for
300 random arrays (1 to 60 numbers, 1 with odds of 1 in 2, 3 in 4 or 15
in 16 in turn) the sum of the answers and a checksum.
`max_consecutive_ones_ii.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random arrays `a` of 1 to 25 numbers, with a second array `b` of
0 to 25, at the same three odds.

| | property |
|---|---|
| P1 | the answer is the longest slice with at most one 0, every slice checked |
| P2 | the array reversed gives the same answer |
| P3 | `a`, then two 0s, then `b` gives the larger of the answers for `a` then a 0 and for a 0 then `b` |
| P4 | one number flipped: a 1 turned to 0 never makes the answer larger, and a 0 turned to 1 never smaller |
| P5 | one more 1 at either end never lowers the answer, and raises it by at most 1 |

No slice with at most one 0 can reach across two 0s, which is why P3
splits there. It prints `1500 cases, 4 arms, 36000 checks, 0 failures`
under `karac __mir-run`, in 1.4 s, and a count for each property when
anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the count before the last 0 keeps growing past it | P1 892, P3 1500 |
| M2 | ★: the flipped 0 is not counted | P1 1164 |
| M3 | window: the window may hold two 0s | P1 892, P3 360 |
| M4 | window: the window is measured one short | P1 1500 |
| M5 | states: a 0 extends the flipped run | P1 892, P3 1500 |
| M6 | states: only the unflipped run is kept | P1 1164 |
| M7 | sides: the last number never counts among the 1s after a 0 | P1 411, P2 454 |
| M8 | sides: an array of 1s is one short | P1 336, P4 394 |

M1 and M5 both answer the array's length, which is wrong exactly for
the 892 arrays with two 0s or more and for every joined array in P3.
M2 and M6 are wrong exactly for the 1,164 arrays holding a 0: there the
true answer always uses one, and M2 answers one less while M6 answers
the longest run of 1s alone (kata 485). Neither moves under reversal,
joining, flipping or growing in a way the properties can see, and nor
does M4's constant one short; only P1, which knows the answer, catches
them. M7 forgets a 1 at the end of the array but not one at the start,
so reversing it shows. M8 is wrong only for arrays of 1s alone, and P4
sees it when flipping the last 0 of an array makes one.

## Verification

All four arms print the same output as `max_consecutive_ones_ii.py`
under `karac __mir-run` (the v2 MIR interpreter) and
`karac __mir-llvm-run`, and `karac check` passes on every file, the
bench program included. The differential prints `36000 checks, 0
failures` on both. The four arms and the differential also run clean
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer):
output identical, no error, no leak.

The frozen legacy backends get the random arrays wrong. Under
`karac run --interp`, LLJIT, legacy `karac build` and a
`KARAC_AUTO_PAR=1` build, all four arms print the eight fixed lines
right and then a different last line (`runs add up to 4210, checksum
382291214`): as on kata 475, legacy calls `next_random` twice for the
bound of `for _ in 0..1 + next_random(mut seed) % 60 { .. }`, so it
draws other arrays. Legacy `karac build` also warns that `nums` is
"moved here, used again here", where `show` lends the array to `list`
and then to the arm. The differential does not type-check on legacy,
which reads the items of `b.iter()` and `a.iter()` as `i64` and refuses
`*x`. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 20 arrays of 100,000
numbers (the problem's most), 1 at odds from 80 in 100 to 99 in 100,
once, then scans each 50 times. Every implementation prints `1000 scans
of 100000 numbers: runs add up to 186200, checksum 457617375`, the Kāra
program under `karac __mir-run` included (in 23 s).

Every mirror is the same loop over a plain array of 64-bit integers.
Spot timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.08 to 0.09 s |
| Rust (`rustc -O`) | 0.08 to 0.09 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.21 to 0.26 s |
| Go | 0.23 to 0.24 s |
| Python | 4.2 to 4.3 s |
| Kāra (`karac build`) | 0.23 to 0.27 s |
| Kāra (`karac build --mir`) | 0.21 to 0.24 s |

Both Kāra builds check every `run += 1` for overflow, as Rust does with
`overflow-checks=on`, and land beside that row rather than beside plain
`rustc -O` (inferred, not profiled). The legacy `karac build` builds and
runs this program correctly (its loops have constant bounds), so
`bench.sh` is the `scripts/new-bench.sh` output unchanged and times that
build. The `--mir` row is the v2 compiled backend, timed for
comparison. Both Kāra rows are timed at kara `aebbc5cf99`. Under
`karac __mir-llvm-run` the program prints the same line in 1.6 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

None. Every arm, the differential and the bench program ran first time
on the v2 backends.
