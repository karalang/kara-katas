# 964. Least Operators to Express Number

Given a single positive integer `x`, we will write an expression of the
form `x (op1) x (op2) x (op3) x ...` where each operator `op1`, `op2`,
etc. is either addition, subtraction, multiplication, or division
(`+`, `-`, `*`, or `/`). For example, with `x = 3`, we might write
`3 * 3 / 3 + 3 - 3` which is a value of 3.

When writing such an expression, we adhere to the following
conventions: the division operator (`/`) returns rational numbers;
there are no parentheses placed anywhere; we use the usual order of
operations, multiplication and division happen before addition and
subtraction; it is not allowed to use the unary negation operator
(`-`). For example, "`x - x`" is a valid expression as it only uses
subtraction, but "`-x + x`" is not because it uses negation.

We would like to write an expression with the least number of operators
such that the expression equals the given `target`. Return *the least
number of operators used*.

```
x = 3,   target = 19         ->  5   (3 * 3 + 3 * 3 + 3 / 3)
x = 5,   target = 501        ->  8   (5 * 5 * 5 * 5 - 5 * 5 * 5 + 5 / 5)
x = 100, target = 100000000  ->  3   (100 * 100 * 100 * 100)
```

**Constraints:** `2 <= x <= 100`; `1 <= target <= 2 * 10^8`.

Without parentheses an expression is a sum of signed terms, each a
power of x: `x^k` costs k operators for k >= 1 (its k - 1
multiplications and the sign in front of it), and `1 = x / x` costs 2.
The first term needs no sign, so every arm takes one operator off the
total. Every arm and the differential's reading leave out terms with
negative powers (`x / x / x`): they only add up to a whole number in
groups of x, and such a group costs more than the `x / x` it makes.

## Approaches

| file | mechanism |
|---|---|
| `least_ops_express_target.kara` ★ | a digit DP from the lowest digit: target in base x, each digit d at place k made either as d copies of x^k or as x - d copies subtracted from one more x^(k+1) carried upward; `pos` is the cheapest cost so far with no carry and `neg` with one. O(log target) |
| `least_ops_express_target_memo.kara` | memoised places: the cheapest way to make t copies of x^i, its lowest digit r made as r copies (leaving t / x copies of x^(i+1)) or as x - r subtracted (leaving one more), the answers in a `Map` keyed by (i, t). O(log target) states |
| `least_ops_express_target_msd.kara` | a digit DP from the highest digit: with N the number the digits read so far make, the cheapest ways to make N * x^i and (N + 1) * x^i, each next digit reached from either by adding or subtracting copies of the next power. O(log target) |
| `least_ops_express_target_dijkstra.kara` | a shortest path from target down to 0: from t with highest power p = x^k, take one p away or step over to x^(k+1) and keep x^(k+1) - t to subtract, each value settled once, cheapest first, from a `PriorityQueue` |
| `least_ops_express_target_relax.kara` | the same moves as dijkstra, settled by relaxation: a `VecDeque` of values whose best cost just fell, re-tried until no cost falls, the costs in a `Map` |
| `differential.kara` | the five arms against the statement read as a shortest path over sums of powers, six properties |

Every arm prints the same 22 lines: LeetCode's three examples and nine
more (1 and 2 with x = 2, 2 with x = 3, 1, 99 and 50 with x = 100, 3
with x = 2, and 343 and 342 with x = 7); the total of the answers and a
checksum over every target from 1 to 300 for every x from 2 to 12, and
over 300 random cases with x from 2 to 100 and target up to 2 * 10^8;
and eight cases at LeetCode's largest targets and exact powers (2 *
10^8 with x = 2 and 100, 199999999 with x = 99, 2^27 and one less, 3^17,
and 10^8 and one less). `least_ops_express_target.py` mirrors the ★ arm
and its output is byte-identical.

The memo arm first branched both ways on every digit and overflowed the
stack on `x = 2, target = 2`: a digit of 0 subtracted as x copies
leaves the same 2 one place up, forever. `karac __mir-run` reported it
as `fatal runtime error: stack overflow` with a note naming the likely
recursion. A digit of 0 is never cheaper subtracted (x copies of x^i
cost more than one x^(i+1)), so the arm now takes the second way only
for a digit above 0.

## Differential

`differential.kara` holds copies of the five arms and the statement read
as a shortest path: the integers from 0 to target walked by adding or
subtracting powers of x at their costs, cheapest first by distance
buckets, every partial sum kept within x * (target + 2) of 0. It checks
3,200 random cases: 3,000 with x from 2 to 9 and target from 1 to 100
against that reading, and 200 with x from 2 to 100 and target up to 2 *
10^8 against the other properties.

| | property |
|---|---|
| P1 | the statement's answer, on the small cases |
| P2 | target + 1 costs at most 2 more or 2 fewer |
| P3 | x^k alone, for a random k with x^k up to 2 * 10^8, costs k - 1 |
| P4 | target + m, for a random m up to 1000, costs at most target's cost plus m's plus one |
| P5 | x * target costs at most twice target's cost plus one |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 cases: 47287 operators, checksum 931994406, 95000 checks
over 5 arms: 0 failures` under `karac __mir-run` (22 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Twenty-nine edits to the differential, each run under
`karac __mir-llvm-run`; fifteen are kept, three to each arm, and all
fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: x / x costed as one operator | P1 2291, P6 2485 |
| M2 | ★: no carry out of the top digit | P1 648, P2 79, P6 690 |
| M3 | ★: the carried digit not counted | P1 1193, P2 5, P4 65, P6 1362 |
| M4 | memo: a single copy costed as its place | P1 30, P2 25, P4 16, P5 30, P6 30 |
| M5 | memo: a digit of 1 never subtracted | P1 123, P2 24, P4 1, P6 128 |
| M6 | memo: the subtraction leaving no carry | P1 1673, P2 159, P4 74, P6 1856 |
| M7 | msd: one more than nothing costing nothing | P1 1256, P2 3, P4 164, P6 1305 |
| M8 | msd: one more made only by adding | P1 611, P2 176, P4 15, P6 723 |
| M9 | msd: one copy too few subtracted | P1 1939, P2 11, P4 85, P6 2127 |
| M10 | dijkstra: the step over one operator cheap | P1 1767, P4 60, P6 1955 |
| M11 | dijkstra: no step over | P1 1413, P2 526, P6 1599 |
| M12 | dijkstra: the first sign not taken off | P1 3000, P3 3200, P6 3200 |
| M13 | relax: a cost never lowered | P1 241, P2 241, P4 16, P6 244 |
| M14 | relax: the step over one operator dear | P1 1413, P2 473, P4 9, P6 1599 |
| M15 | relax: a power taken away at its place, x / x free | P1 2291, P4 169, P5 1353, P6 2485 |

P1 and P6 kill all fifteen, P2 eleven (M2 to M9, M11, M13, M14), P4
eleven (M3 to M10, M13 to M15), P5 two (M4, M15) and P3 one (M12). P3
only sees a single power, which every arm but a miscounted sign gets
right, and P5's bound is loose enough that only answers far too low
break it.

Fourteen other edits were tried and set aside. Seven failed exactly the
same checks as a kept one: memo, msd and relax costing x / x as one
operator, as M1; relax not taking the first sign off and starting the
target at cost 1, as M12; and relax with no step over, as M11. Four
were sound but beyond three an arm: ★ not taking the first sign off,
falling one copy short on a carry into a carry, and costing each copy
one operator more; and msd skipping the top digit.

Three were equivalent. Memo storing each answer a place up: the answer
is then never found again, so every state is recomputed and the result
is the same. And dijkstra and relax missing an exact power as the
highest: for t = x^(k+1) they take x^k as the highest power, and the
step over to x^(k+1) leaves 0 at cost k + 1, the same as taking x^(k+1)
away.

## Verification

Every arm prints the same output as `least_ops_express_target.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `cb8ffcccec`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` ★ takes
0.18 s, msd 0.20 s, memo 0.33 s, relax 1.3 s and dijkstra 2.2 s, and
the differential 22 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program runs the ★ arm on every x from 2 to 100 and 2000
targets spread below LeetCode's largest, `2 * 10^8 - 99991 j`, in each
of 80 rounds, each round's targets one lower than the last's, and folds
the answers into a checksum: 15.84 million calls, each reading 5 to 28
base-x digits. Every implementation prints `80 rounds over x from 2 to
100 and 2000 targets: 2193562003 operators, checksum 691505553`.
Nothing is allocated.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.35 to 0.44 s | 0.37 s |
| Rust (`rustc -O`) | 0.35 to 0.42 s | 0.38 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.39 to 0.51 s | 0.42 s |
| Go | 0.42 to 0.53 s | 0.45 s |
| Python | 21.0 s | |
| Kāra (`karac build --mir`) | 0.41 to 0.52 s | 0.45 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 57 times
C's.

v2 takes 1.07 times Rust's median time under overflow checks and 1.22
times C's. Under valgrind's cachegrind v2 runs 4.79 billion
instructions and 1.03 billion branches with 15.9 million mispredicted,
Rust with overflow checks 3.93 billion, 0.99 billion and 15.9 million,
and C 3.18 billion, 0.21 billion and 5.9 million. Those were not traced
to the instructions, but every digit costs a division and a remainder,
and C's far lower branch count suggests it turns the two `min`s into
conditional moves where Rust and v2 branch.
