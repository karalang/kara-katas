# 2348. Number of Zero-Filled Subarrays

Given an integer array `nums`, return *the number of **subarrays**
filled with* `0`.

A **subarray** is a contiguous non-empty sequence of elements within an
array.

```
nums = [1,3,0,0,2,0,0,4]  ->  6
nums = [0,0,0,2,0,0]      ->  9
nums = [2,10,2019]        ->  0
```

**Constraints:** `1 <= nums.length <= 10^5`;
`-10^9 <= nums[i] <= 10^9`.

The zero-filled subarrays that end at a place are as many as the zeros
in the run ending there, so a run of `L` zeros holds `L (L + 1) / 2` of
them. `10^5` zeros hold `5000050000`, past `i32`, which is why
LeetCode's answer is an `i64`.

## Approaches

| file | mechanism |
|---|---|
| `zeros.kara` ★ | the length of the run of zeros ending at each place, summed at every place. O(n) |
| `zeros_runs.kara` | each maximal run of zeros found by its start and end, and a run of length `L` counted at once as `L (L + 1) / 2`. O(n) |
| `zeros_halves.kara` | divide and conquer: each half counted by recursion, and the subarrays that cross the middle as the zeros ending the left half times the zeros starting the right. O(n log n) |
| `zeros_last.kara` | the index of the last value that is not zero: at a zero `i`, `i` minus that index subarrays end there. O(n) |
| `zeros_iter.kara` | iterators: the run at each place by `scan`, and the runs summed by `sum` |
| `zeros_solution.kara` | LeetCode's Rust template: the slice split at every value that is not zero by `split(\|&x\| x != 0)`, each piece a run of `n` zeros counted as `n (n + 1) / 2` through `as i64`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples; one zero;
`10^5` zeros; zeros between every other value; `10^5` values with every
third one not zero; then 2000 random arrays of 1 to 40 values, each
zero with a chance of 1 in 2 to 1 in 5 and otherwise from `-10^9` to
`10^9`, with a checksum, the answers' sum and how many have no zero.
`zeros.py` mirrors the ★ arm and its output is byte-identical, and the
mirror was checked against every subarray on 3000 random arrays.

A fourth arm was first written from every start, extending each start
while the values stay zero, one subarray per step. Its work is the
answer itself, `5 * 10^9` steps on the line of `10^5` zeros, which no
backend finishes in minutes, so it was replaced by divide and conquer.
The differential's literal reading stands in for it on short arrays.

The iter arm was first written as Rust writes `scan`, the state written
in place through `*run = ...` and the item returned as `Some(*run)`.
`check` refuses that with a note that Kāra's `scan` closure takes the
state by value and returns `Some((next_state, item))`, and `karac fix`
rewrote the closure in one edit.

`karac fix` carries the template in one call, reporting 5 edits.
`check` first reports 2 errors and offers 3 edits for them: the two
brackets of `Vec<i32>` and the `&` of `|&x|` dropped. The other two
follow: `.into_iter()` put after `split`, which in Kāra returns the
pieces as a vector rather than an iterator, and the `as i64` on
`run.len()` dropped, since a length is already an `i64`. `split` with a
predicate, `map` and `sum` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every subarray, from every start to every end, checked value
by value for being all zeros. No runs. It checks 300 random cases of 1
to 20 values, each zero with a chance of 1 in 1 to 1 in 5 and otherwise
from `-10^9` to `10^9` but not 0; then 30 of up to 2000 values, zero
with a chance of 1 in 1 to 1 in 3; then 30 of up to 300 values from -2
to 2. All 360 are drawn before any arm answers; 37 hold no zero.

| | property |
|---|---|
| P1 | up to 20 values, the answer is the literal reading's |
| P2 | 0 exactly when there is no zero, and otherwise from the number of zeros `z` to `z (z + 1) / 2` |
| P3 | the values reversed: the same answer |
| P4 | every value that is not zero negated: the same answer |
| P5 | a zero appended: the answer plus one more than the zeros that end the array |
| P6 | each arm agrees with at least three of the other five |

P5 holds because the new zero ends exactly one more subarray than the
run before it is long, and no other subarray changes.

The differential prints `360 cases: checksum 78780803, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tests each slice with `any`. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the run never reset | P1 191, P2 245, P3 239, P5 245, P6 245 |
| M4 | ★: the run reset to 1 | P1 240, P2 208, P3 135, P5 295, P6 295 |
| M5 | ★: the run grown by two | P1 264, P2 191, P5 360, P6 323 |
| M7 | runs: a run counted as half its square | P1 264, P2 201, P5 259, P6 323 |
| M8 | runs: a negative value inside a run taken for a zero | P1 146, P2 104, P3 192, P4 234, P5 41, P6 200 |
| M10 | runs: the value after one that is not zero skipped | P1 156, P2 152, P3 165, P5 190, P6 210 |
| M12 | halves: a single value always counted | P1 240, P2 180, P6 295 |
| M13 | halves: the crossing subarrays added, not multiplied | P1 259, P2 166, P3 119, P5 326, P6 318 |
| M14 | halves: the left half's first value never reached | P1 148, P3 103, P5 189, P6 206 |
| M19 | last: a negative value taken for a zero | P1 218, P2 188, P4 279, P5 125, P6 273 |
| M20 | last: the last index set one too early | P1 192, P2 76, P3 135, P5 295, P6 246 |
| M21 | last: the first value skipped | P1 174, P2 44, P3 162, P5 15, P6 204 |
| M22 | iter: the run started at 1 | P1 138, P2 77, P3 135, P5 65, P6 159 |
| M24 | iter: one counted at every place | P1 291, P2 167, P5 156, P6 351 |
| M25 | iter: the longest run, not the sum | P1 227, P2 209, P5 323, P6 286 |
| M29 | solution: single zeros dropped | P1 187, P2 157, P5 270, P6 241 |
| M30 | solution: split at the zeros | P1 291, P2 266, P5 360, P6 351 |

P1 and P6 kill all seventeen, P2 and P5 sixteen each, P3 nine and P4
two. P2 misses only the halves arm's left half's first value never
reached, which loses some subarrays that cross the middle but never so
many that fewer than the zeros are left. P5 misses only its single
value always counted, which counts a value that is not zero as one
subarray wherever it stands, so a zero appended still adds what it
should. P3, the values reversed, fails the edits that treat one end of
an array or a run unlike the other: the run never reset or reset to 1,
a negative inside a run taken for a zero, the value after a non-zero
skipped, the crossing subarrays added, the left half's first value
never reached, the last index set one too early, the first value
skipped, the run started at 1. P4, the values that are not zero
negated, fails only the two edits that take a negative value for a
zero.

Of the thirty-one, fourteen were not kept. The run never reset in the
iter arm (M23) fails as in the ★ arm (M1); a negative value taken for a
zero in the ★ arm (M3) and the template's split only at positive values
(M27) as in the last arm (M19); and the run grown by two in the ★ arm
(M5) as the template's run counted twice over (M31). Each zero counted
once in the ★ arm (M2) and each run counted as its zeros in the runs
arm (M11) fail alike; so do the first value skipped in the ★ arm (M6)
and the last value that is not zero started at 0 in the last arm
(M17); and the run's last zero left out in the runs arm (M9), one
subarray fewer at each zero in the last arm (M18) and a run counted as
its pairs in the template (M28). Those three groups fail apart from
every kept one, as do the halves arm's right half's last value never
reached (M15) and right half never counted (M16) and the iter arm's
positive value taken for a zero (M26); they were left out to keep three
to an arm and two to the template.

## Verification

Every arm prints the same output as `zeros.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.4 to 1 s but the template,
1.6 s, which builds the pieces of every split as vectors. The
differential takes 1.7 s there and 0.56 s under `karac
__mir-llvm-run`.

## Benchmarks

The bench builds 10 arrays of `10^5` values once from the harness's
generator, array `a` holding a value that is not zero with a chance of
1 in `a + 2`, then makes 60 passes, pass `p` folding each answer plus
`p` into the checksum, with the ★ arm in all five languages. Every
implementation prints `60 passes over 10 arrays of 10^5 values:
checksum 38788071`. No implementation allocates in the counted loop.

BENCHTAB
