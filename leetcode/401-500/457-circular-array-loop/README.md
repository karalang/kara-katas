# 457. Circular Array Loop

You are playing a game involving a circular array of non-zero integers
`nums`. Each `nums[i]` is the number of indices to move from index `i`:
forward if it is positive, backward if negative. Moving forward from
the last element puts you on the first, and backward from the first on
the last. A cycle is a sequence of indices `seq` of length `k` where
following the movement rules goes round `seq[0] -> ... -> seq[k - 1] ->
seq[0]`, every `nums[seq[j]]` is either all positive or all negative,
and `k > 1`. Return `true` if there is a cycle in `nums`.

```
nums = [2,-1,1,2,2]         ->  true   (0 -> 2 -> 3 -> 0)
nums = [-1,-2,-3,-4,-5,6]   ->  false  (the only cycle has length 1)
nums = [1,-1,5,1,4]         ->  true   (3 -> 4 -> 3)
```

**Constraints:** `1 <= nums.length <= 5000`; `-1000 <= nums[i] <= 1000`;
`nums[i] != 0`.

## Approaches

Every arm is `fn circular_array_loop(nums: Vec[i64]) -> bool`. A step is
*valid* when it moves to another index whose step points the same way.
Since each index has one step out, a cycle of valid steps is exactly
what the problem asks for.

| file | mechanism |
|---|---|
| `circular_loop.kara` ★ | from each start not yet ruled out, a slow pointer and a fast one along valid steps; if they meet in a loop longer than one index, done, and otherwise every index on the path is zeroed in a copy and never started from again. O(n) |
| `circular_loop_colour.kara` | walk from each unvisited index along valid steps, colouring each index with its walk's start; coming back to the walk's own colour closes a cycle, and running into an earlier colour ends the walk. O(n) |
| `circular_loop_graph.kara` | keep only the valid steps, count the ways into each index, and peel off indices nothing leads to; whatever survives lies on a cycle. O(n) |
| `circular_loop_walk.kara` | the plain reference: from each start, try `n` valid steps; surviving them means having gone round a cycle. O(n²) |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 12 lines: the three LeetCode examples, one
index, two indices both ways, two indices facing each other, a
three-index loop, a self-loop beside a two-index loop, the LeetCode
case `[-2,1,-1,-2,-2]`, steps of 1,000, and for 300 random arrays of 1
to 200 steps (of size up to 3, 10 or 1,000, forward with probability
1/2, 3/4, 15/16 or 1) how many have a loop and a checksum.
`circular_loop.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases.

| | property |
|---|---|
| P1 | on 1 to 6 steps of size 1 to 3, the answer is brute force's: from every index, walk until on a cycle of the whole step graph (valid steps or not), then check that the cycle is longer than one index and keeps one direction |
| P2 | on 1 to 60 steps, rotating the array keeps the answer |
| P3 | reversing the array and negating every step keeps it |
| P4 | lengthening steps by whole turns of the array keeps it |
| P5 | two neighbours set to 1 and `n - 1`, which step onto each other, give `true` when `n > 1` (and a single step stays `false`) |

Reversing alone, or negating alone, does not keep the answer: each
turns the steps around relative to the indices, and only the two
together put them back. A first draft of the differential got that
wrong, and every arm failed it the same way.

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a one-index loop counts | P1 581, P5 29 |
| M2 | ★: the fast pointer's second step may turn around | P1 56, P2 152, P3 222 |
| M3 | colour: meeting any earlier walk counts as a loop | P1 327, P2 27, P3 42 |
| M4 | colour: a step onto itself is followed | P1 581, P5 29 |
| M5 | graph: a step onto itself is kept | P1 581, P5 29 |
| M6 | graph: steps that turn around are kept | P1 369 |
| M7 | walk: a walk of `n / 2` steps is taken as a loop | P1 543, P5 29 |
| M8 | walk: every walk must go forward | P1 78, P3 687 |

P1, the only property with an independent answer, sees all eight. P4
sees none: a whole turn lands every step where it did, mutated or not.
P5's 29 are its one-index arrays, which the self-loop mutants call a
loop. M2 and M3 depend on where a walk starts, which rotating or
reversing the array changes, so P2 and P3 see them; M8 is caught by P3,
which turns a forward loop into a backward one.

## Verification

All four arms print the same output as `circular_loop.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends every arm matches under
`karac run --interp`, and the differential prints `0 failures` there.
LLJIT and `karac build` stop in the legacy code generator on the
harness's index into an array literal ("Index operator applied to
non-array type"), in every arm and the differential. Legacy
`karac build` also rejects the bench program (see Benchmarks). Legacy
is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 10 arrays of 1,000,000
random steps of 1 to 1,000, each way equally likely, once; none of
them has a loop. Each of 5 rounds, for every array, sets one step to 1
and the next to `n - 1` half the time, a loop of two forward steps,
then checks the array and puts the two steps back. Each check copies
its array; one without a loop walks all of it, and one with a loop
stops when a start reaches the planted pair. Every implementation
prints `5 rounds on 10 arrays of 1000000: 29 with a loop, checksum
314563514`, the Kāra program under `karac __mir-run` included (in
116 s).

The legacy `karac build` rejects the bench program (it moves `all[a]`
out of the index, where v2 borrows it), so `bench.sh` builds the Kāra
program with `karac build --mir`, the v2 compiled backend. That edit is
by hand, on top of the `scripts/new-bench.sh` output.

The mirrors keep the ★ arm's structure, including the copy and the
clearing walk; the Python mirror writes the step function inline.
Spot timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.57 to 0.61 s |
| Rust (`rustc -O`) | 0.89 to 1.00 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.87 to 0.95 s |
| Go | 1.71 to 1.81 s |
| Python | 12.5 to 13.0 s |
| Kāra (`karac build --mir`) | 1.15 to 1.24 s |

Under `karac __mir-llvm-run` the
program prints the same line in 2.7 s, compile included; that JITs the
MIR's IR without optimization passes, so it is not a benchmark.

## Compiler findings

No new findings.
