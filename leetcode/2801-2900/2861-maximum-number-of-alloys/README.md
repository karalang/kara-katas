# 2861. Maximum Number of Alloys

You are the owner of a company that creates alloys using various types
of metals. There are `n` different types of metals available, and you
have access to `k` machines that can be used to create alloys. Each
machine requires a specific amount of each metal type to create an
alloy.

For the `ith` machine to create an alloy, it needs
`composition[i][j]` units of metal of type `j`. Initially, you have
`stock[i]` units of metal type `i`, and purchasing one unit of metal
type `i` costs `cost[i]` coins.

Given integers `n`, `k`, `budget`, a **1-indexed** 2D array
`composition`, and **1-indexed** arrays `stock` and `cost`, your goal
is to **maximize** the number of alloys the company can create while
staying within the budget of `budget` coins.

**All alloys must be created with the same machine.**

Return *the maximum number of alloys that the company can create*.

```
n = 3, k = 2, budget = 15, composition = [[1,1,1],[1,1,10]], stock = [0,0,0], cost = [1,2,3]    ->  2
n = 3, k = 2, budget = 15, composition = [[1,1,1],[1,1,10]], stock = [0,0,100], cost = [1,2,3]  ->  5
n = 2, k = 3, budget = 10, composition = [[2,1],[1,2],[1,1]], stock = [1,1], cost = [5,5]       ->  2
```

**Constraints:** `1 <= n, k <= 100`; `0 <= budget <= 10^8`;
`composition.length == k`; `composition[i].length == n`; `1 <=
composition[i][j] <= 100`; `stock.length == cost.length == n`; `0 <=
stock[i] <= 10^8`; `1 <= cost[i] <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `alloys.kara` ★ | for one machine the cost of x alloys, every metal's shortfall a·x - stock bought at its price, only grows with x, so the most it can make is found by binary search up to 2·10^8, the cost a closure over the machine; the best machine wins |
| `alloys_any.kara` | one binary search for all the machines: x alloys can be made when some machine makes them within the budget, each probe asking the machines in turn with `any` over a closure that returns early once the budget is passed |
| `alloys_slopes.kara` | no search: a metal costs nothing until x passes stock / a, so a machine's cost is a line that bends up at each such point; the metals sorted by it are taken in one at a time, the slope and offset growing, and when the line at the next bend is over budget the answer is (budget + offset) / slope |
| `alloys_gallop.kara` | a galloping search per machine: the step doubles from 1 while one more step stays within the budget, then halves, so the count climbs in O(log x) probes with no fixed upper bound |
| `alloys_solution.kara` | a Rust solution as LeetCode's Rust users write it: a binary search per machine from `let (mut lo, mut hi) = (0i64, 200_000_000i64)`, the cost summed in `i64` with `as i64` on every `i32` term, and a wrapper closure `to32` ending in `collect::<Vec<i32>>()`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 3 lines: LeetCode's three examples and
LeetCode's full size, 100 metals of 10^8 in stock and 100 machines
needing one of each at 1 a unit with 10^8 to spend; then 3000 random
cases of 1 to 4 metals and 1 to 3 machines with small amounts, and 30
of up to 100 of each over LeetCode's full ranges, as a total and a
checksum. `alloys.py` mirrors the ★ arm and its output is
byte-identical.

```
2 5 2 101000000
3000 small cases: 19100 alloys, checksum 466786546
30 large cases: 7854555 alloys, checksum 703521007
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: each machine tried with 0, 1, 2, ... alloys, the
metals it lacks bought at their prices, until the next count costs more
than the budget. It draws 2000 random cases of 1 to 4 metals and 1 to 3
machines with small amounts, then 50 of up to 100 of each over
LeetCode's full ranges, all before any arm answers; the literal reading
is asked only of the first 2000.

| | property |
|---|---|
| P1 | small amounts, the answer is the literal reading's |
| P2 | the machines in reverse order: the same answer |
| P3 | small amounts, every stock and the budget doubled: twice the answer, or one more |
| P4 | one more metal, its stock beyond any need: the same answer |
| P5 | one more machine needing twice the first one's metals: the same answer |
| P6 | each arm agrees with at least three of the other four |

P3 is asked only of the small cases because doubling the large ones
takes the stock and the budget past LeetCode's limits, and the answer
past the 2·10^8 the searches start from. The differential prints `2050
cases, 72986587 alloys: checksum 656902106, 61500 checks over 5 arms: 0
failures` under every lane in Verification, and a Python reading of the
same cases, the literal one for the first 2000, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. A first draft of M5 left every answer as it
was, equivalent to the arm, and was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a surplus of one metal paying for another | P1 891, P4 2050, P6 940 |
| M2 | ★: the search capped at 1000 | P6 50 |
| M3 | any: every machine asked to manage it | P1 1071, P5 1620, P6 1119 |
| M4 | any: the budget spent exactly not allowed | P1 291, P6 291 |
| M5 | slopes: the alloys one short when the budget divides evenly | P1 263, P3 6, P6 263 |
| M6 | slopes: the price left out of the offset | P1 1540, P3 55, P6 1590 |
| M7 | gallop: the step reset to 1, not halved | P1 708, P3 222, P6 758 |
| M8 | gallop: a metal in surplus still charged | P1 887, P3 369, P6 888 |
| M9 | solution: only the first machine tried | P1 591, P2 1004, P6 636 |
| M10 | solution: the stock counted twice | P1 1802, P6 1852 |

## Benchmarks

The bench draws 100 cases of 100 metals and 100 machines, LeetCode's
most, amounts over LeetCode's full ranges, all of them first, then
answers each 20 times by the ★ arm in all five languages; C keeps each
case's composition in one fixed 100 x 100 array. Every implementation
prints `100 cases of 100 by 100, 20 rounds: 180196580 alloys, checksum
144443746`.

BENCHTAB

## Verification

All five arms print the same output as `alloys.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written.

LeetCode's Rust template, with a wrapper in the same Rust, found a gap
in `karac fix`. The wrapper's `let to32 = |v: &Vec<i64>| v.iter().map(|&x|
x as i32).collect::<Vec<i32>>();` drew the turbofish diagnostic, whose
fix deleted `::<Vec<i32>>` and left a closure whose `collect` had no
type to collect into; `karac check` then refused it with E0516, "an
expression whose type does not lower (Type(UnknownParam("OutV"))) is
not lowered yet". The fix now writes the closure's type onto the
binding when the turbofish is on its tail, as it already did for a
Rust closure return type, and the line became `let to32: Fn(ref
Vec[i64]) -> Vec[i32] = |v: ref Vec[i64]| ..collect();` (kara 0d28296389, B-2026-11-21-204).

With that, the template took 37 `karac fix` edits in one run: `struct
Solution {}` added for the `impl`; `Vec<..>` became `Vec[..]`; `let
(mut lo, mut hi) = (0i64, 200_000_000i64)` became `let mut (lo, hi) =
(0, 200_000_000)`; the `as i64` widenings of `i32` values went,
`lossless_cast`, in the cost and the budget's comparison and on the
wrapper's result; `&Vec<i64>` became `ref Vec[i64]`; `|&x|` lost its
`&`; `&stock` and `&cost` lost theirs, and `Solution::` took `.`. `for
j in 0..n as usize` and `ans as i32` were accepted as written.
