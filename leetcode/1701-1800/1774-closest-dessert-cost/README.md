# 1774. Closest Dessert Cost

You would like to make dessert and are preparing to buy the ingredients.
You have `n` ice cream base flavors and `m` types of toppings to choose
from. You must follow these rules when making your dessert: there must
be exactly one ice cream base; you can add one or more types of topping
or have no toppings at all; there are at most two of each type of
topping. You are given three inputs: `baseCosts`, an integer array of
length `n`, where each `baseCosts[i]` represents the price of the `i`th
ice cream base flavor; `toppingCosts`, an integer array of length `m`,
where each `toppingCosts[i]` is the price of one of the `i`th topping;
and `target`, an integer representing your target price for dessert. You
want to make a dessert with a total cost as close to `target` as
possible. Return the closest possible cost of the dessert to `target`.
If there are multiple, return the lower one.

```
baseCosts = [1,7], toppingCosts = [3,4], target = 10       ->  10
baseCosts = [2,3], toppingCosts = [4,5,100], target = 18   ->  17
baseCosts = [3,10], toppingCosts = [2,5], target = 9       ->  8
```

**Constraints:** `n == baseCosts.length`, `m == toppingCosts.length`, `1
<= n, m <= 10`, `1 <= baseCosts[i], toppingCosts[i] <= 10^4`, and `1 <=
target <= 10^4`.

The arms are `fn closest_cost(base_costs: Vec[i32], topping_costs:
Vec[i32], target: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `closest_cost.kara` ★ | for each base, a depth-first search that adds each topping none, once or twice, keeping the closest cost seen, and stops adding once the cost has reached the target, since more can only take it further away. O(n 3^m) at most |
| `closest_cost_enumerate.kara` | every choice counted out: each number below 3^m, read in base 3, says how many of each topping to add, and every base is tried with every choice. O(n m 3^m) |
| `closest_cost_reach.kara` | the toppings' sums that can be made, as a table of flags up to 20000, since a cost beyond twice the largest target is further from it than any base alone; then each base is tried with every sum that can be made. O((m + n) 20000) |
| `closest_cost_sorted.kara` | every sum of the toppings listed and sorted once; for each base, `partition_point` finds the sums on either side of what the base leaves to reach the target. O(3^m m + n m) |
| `closest_cost_solution.kara` | a Rust solution as LeetCode's Rust users write it (a nested `fn dfs` with an `&mut i32` best, started at `i32::MAX`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples (`10 17
8`); five edges, every base above the target, one topping twice, a tie
with the cheaper kept, the target out of reach above, and the target
exact (`10 7 4 8 9`); the constraints' most, 10 bases and 10 toppings of
up to 10000 under targets of 10000 and 1, and the same bases with 10
toppings of 1 (`the most: 9992 3670 9528`); and 3000 random cases of 1
to 10 bases and 1 to 6 toppings (`3000 random cases: checksum
226137651`). `closest_cost.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the enumerate and reach arms check clean as first
written. The ★ arm's `for times in 0..3` made `times * toppings[i]` an
`i64`, since an operand beside an `i32` keeps a literal's default
(design.md §8 Literals), and the sum then went to an `i32` parameter;
`karac fix` wrote `0i32..3`, 1 fix. The sorted arm took the same fix on
`for k in 0..3`, and two `as i64` casts on `partition_point`'s answer,
already an `i64`, were dropped as redundant, 3 fixes. The Rust solution
takes one round of 27 fixes by `karac fix`'s count, and its diff is:
`struct Solution;` to `struct Solution {}`, `Vec<i32>` to `Vec[i32]`,
`i32::MAX` to `i32.MAX`, the nested `fn dfs` moved to the top level with
its `usize` index an `i64`, `&Vec<i32>` and `&mut i32` to `ref Vec[i32]`
and `mut ref i32`, `||` and `&&` to `or` and `and`, `0..3` to `0i32..3`,
`for &b in &base_costs` to `for b in ref base_costs`, the call's `&` and
`&mut` to plain and `mut` arguments, and `Solution::` to `Solution.`.
Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every dessert, one base and each topping none, once or twice,
its cost listed, and the list sorted by distance to the target and then
by cost. LeetCode's examples, the edges, and 1992 random cases of 1 to 6
bases and 1 to 5 toppings, costs from 1 to a bound of 5 to 5000 and the
target at most 5000, so that doubled it is still within the constraints.
Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | from the cheapest base to the dearest with every topping twice, and no further from the target than any base alone |
| P3 | the bases and the toppings each in reverse give the same cost |
| P4 | every cost and the target doubled give the cost doubled |
| P5 | the answer as the target gives itself |
| P6 | the ★ arm's answer |

The literal reading's sort key was first written `|c|
((c - target).abs(), *c)`, and `karac fix` dropped the `*`, since the
closure's item is a copied `i32`. All 60,000 checks pass on every arm:
`2000 cases: checksum 582310175, 60000 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, listing every dessert with `itertools.product`,
gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: of two as close, the dearer kept | P1 11, P6 44 |
| M2 | ★: each topping at most once | P1 604, P6 2416 |
| M3 | enumerate: each digit read as at most one of its topping | P1 604, P6 604 |
| M4 | enumerate: the choice read in base 2 | P1 504, P6 504 |
| M5 | reach: each topping's sums at most once | P1 604, P6 604 |
| M6 | reach: sums built on sums of the same topping, so any number of it | P1 563, P2 76, P6 563 |
| M7 | sorted: only the sum at or above the target looked at | P1 768, P2 213, P3 215, P6 768 |
| M8 | sorted: the sums never sorted | P1 737, P3 849, P5 219, P6 737 |
| M9 | solution: the last topping never added | P1 709, P3 748, P6 709 |
| M10 | solution: the best cost started at 0 | P1 183, P2 183, P6 183 |

## Benchmarks

The bench builds 100 menus of 10 bases up to 5000 and 8 toppings up to
1000 once, and makes 1000 calls of the ★ arm, each menu and target drawn
from the checksum so far. Every implementation prints `1000 calls over
100 menus: checksum 637676300`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.15 s against Rust's 0.13 s (0.16 s with overflow checks
on), C's 0.13 s and Go's 0.17 s; Python takes 10.2 s.
