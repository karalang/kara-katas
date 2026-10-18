# 746. Min Cost Climbing Stairs

`cost[i]` is the cost of step `i` of a staircase. Once its cost is paid,
a climber on a step can climb one or two steps. The climb may start on
step 0 or step 1. Return the least cost of reaching the top, the
position just past the last step.

```
cost = [10, 15, 20]                          ->  15
cost = [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]  ->  6
```

**Constraints:** 2 to 1,000 steps; 0 <= `cost[i]` <= 999.

## Approaches

The cheapest way to any position comes from the cheaper of the two
positions below it, so one pass of dynamic programming suffices; the
arms differ in the direction of the pass and in what they keep.

| file | mechanism |
|---|---|
| `min_cost_climbing_stairs.kara` ★ | the least paid to stand at each position, from the cheaper of one step below plus that step's cost and two steps below plus that one's; only the last two totals are kept; O(n) time, O(1) space |
| `min_cost_climbing_stairs_table.kara` | a table of the least paid by a climb that stands on each step, its own cost included; the top comes from the cheaper of the last two steps |
| `min_cost_climbing_stairs_memo.kara` | the ★ arm's recurrence asked from the top down by recursion, each position's answer remembered in a `Vec` |
| `min_cost_climbing_stairs_down.kara` | backwards from the top: the least still to pay from each step, its own cost plus the cheaper of the two steps above; the answer is the cheaper of steps 0 and 1 |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 10 lines: the two LeetCode examples; two steps
that cost nothing, and two that cost 5 and 3; free steps with a dear one
at the top; free pairs between dear steps; five steps at the most a step
can cost; 1,000 random steps; 1,000 steps at 999; and 300 random
staircases of 2 to 15 steps, with the sum of their answers and a
checksum. `min_cost_climbing_stairs.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which tries every set of steps a climb could stand on, keeps the sets
that begin at step 0 or 1, never skip more than one step and end on one
of the last two steps, and takes the cheapest. 3,000 random staircases
are checked, each of 2 to 10 steps costing 0 to 9; their answers sum to
28,966.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the costs in reverse order give the same answer, since a climb read backwards is a climb |
| P3 | every cost tripled triples the answer |
| P4 | a step of cost 0 added at the top gives the same answer |

It prints `3000 stairs (costs sum to 28966), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a two-step climb paying for the wrong step | P1 2487, P2 2769, P4 117 |
| M2 | ★: stopping one position short of the top | P1 1772, P2 1922, P4 1772 |
| M3 | ★: the older total overwritten with the new one | P1 2358 |
| M4 | table: the climb made to stand on the last step | P1 1843, P2 2402, P4 1843 |
| M5 | table: step 1 reachable only through step 0 | P1 1812, P2 2402 |
| M6 | table: the dearer of the two steps below taken | P1 2347, P2 1536, P4 2565 |
| M7 | memo: the two starting positions charged their own step | P1 2516, P2 2138 |
| M8 | memo: a two-step climb paying for the wrong step | P1 2250, P2 2714, P4 1940 |
| M9 | memo: the one-step total remembered, not the best | P1 1766, P2 1270 |
| M10 | down: always one step up | P1 2795, P2 2714 |
| M11 | down: always starting on step 0 | P1 1812, P2 2402 |
| M12 | down: the last step left free | P1 1772, P2 1922, P4 1772 |
| E1 | ★: a tie going to the two-step climb | 0 |
| E2 | down: one more unused zero above the top | 0 |
| E3 | memo: one more unused entry | 0 |

P1 kills all twelve. Several are one mistake in two arms and fail
exactly the same checks: M2 and M12 both let the last step go free, the
★ arm by stopping one position short of the top; M5 and M11 both force
the climb to start on step 0. P2 sees most of them, since reversing the
stairs swaps the two ends, and an edit that treats the start and the top
unalike, or the step left behind and the step arrived at, then gives a
different answer: it misses only M3, which goes wrong the same way in
both directions. P4 sees the edits that change how the top is reached,
M1, M2, M4, M6, M8 and M12, since a free step at the top then changes
the answer. P3 sees none: every edit here is a choice of which costs to
add, which tripling every cost does not change. E1 lets a tie go to the
two-step climb, which costs the same; E2 and E3 add an entry that is
never read.

## Verification

Every arm prints the same output as `min_cost_climbing_stairs.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`1a5c083e3a`, whose last compiler change is `4655692faa`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept all four arms and the bench program:
every arm prints the same output under the legacy interpreter, `karac
run`, `karac build` and an auto-par build. They refuse the differential
at type checking, at a `*` over a vector's `iter()` (`*c` over the
costs), since legacy gives those by value where v2 gives references.
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes a
staircase of 1,000 steps costing 0 to 999 once, and in each of
300,000 rounds gives 5 random steps new costs and finds the least cost
again, 300 million steps of the recurrence in all. Every implementation
prints `300000 rounds on 1000 steps: least costs sum to
61423037150`, the Kāra program under `karac __mir-run` included (in
95 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.28 to 0.29 s |
| Rust (`rustc -O`) | 0.27 to 0.34 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.27 to 0.34 s |
| Go | 0.35 to 0.41 s |
| Python | 22.5 to 23.4 s |
| Kāra (`karac build --mir`) | 0.28 to 0.37 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
3.1 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build, C, Rust and Rust
under overflow checks are level (0.29 s, 0.28, 0.28 and 0.29), and Go is
a quarter behind (0.36). The work is one chain of additions and
comparisons, each step waiting on the last, so its time is set by that
chain's length and not by instruction count: under valgrind's cachegrind
v2 runs 5.4 billion instructions and 1.5 billion branches, five a step,
against C's and Rust's 1.6 billion and 0.10 billion, yet takes the same
time. The extra branches are presumably bounds and overflow checks, all
predicted (inferred, not read from the code). The legacy build of the
same program ran 0.23 to 0.29 s in the interleaved runs, a median of
0.29 s, so v2 takes as long as legacy, inside M2's limit of twice
legacy; new katas' benches are outside M2's frozen set in any case. The
comparison with C and Rust waits until after M4.

## Compiler findings

None new.
