# 2735. Collecting Chocolates

You are given a **0-indexed** integer array `nums` of size `n`
representing the cost of collecting different chocolates. The cost of
collecting the chocolate at the index `i` is `nums[i]`. Each chocolate is
of a different type, and initially, the chocolate at the index `i` is of
`i`-th type.

In one operation, you can do the following with an incurred **cost** of
`x`:

- Simultaneously change the chocolate of `i`-th type to `((i + 1) mod
  n)`-th type for all chocolates.

Return *the minimum cost to collect chocolates of all types, given that
you can perform as many operations as you would like.*

```
nums = [20, 1, 15], x = 5  ->  13
nums = [1, 2, 3],   x = 4  ->  6
```

**Constraints:** `1 <= nums.length <= 1000`, `1 <= nums[i] <= 10^9`,
`1 <= x <= 10^9`.

## Approaches

After k operations, the chocolate of type t can have been bought at any
of the k + 1 prices `nums[t]`, `nums[t - 1]`, ..., `nums[t - k]`, round
the circle, so the cost with k operations is k x plus the sum of each
type's cheapest among those. The answer is the least over k = 0 to
n - 1, since a whole circle of operations can only add cost.

| file | mechanism |
|---|---|
| `chocolates.kara` ★ | each type's cheapest so far kept in a vector and narrowed one operation at a time, the total taken after each. O(n^2) |
| `chocolates_table.kara` | a table `low[t][k]` of each type's cheapest within k operations, filled row by row as a running minimum, then each column summed by nested `map` and `sum` and the least taken by `min`. O(n^2) time and space |
| `chocolates_sparse.kara` | the prices written twice, so that every stretch of the circle is a plain range, and a sparse table of range minimums over them; each type's cheapest within k operations is two overlapping table reads. O(n log n) to build, O(n^2) reads |
| `chocolates_shift.kara` | the prices themselves turned one place an operation with `rotate_right`, as the statement turns the chocolates, and the running cheapest narrowed by `zip` and `min`. O(n^2) |
| `chocolates_solution.kara` | a Rust solution as LeetCode's Rust users write it, `i32` prices widened into a `Vec<i64>` of running minimums narrowed by `nums[(i + k) % n]`, the window looking forward rather than back, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; one
chocolate; operations too dear to take; operations so cheap that every
type is bought at the cheapest price; 2000 random cases of 1 to 20
chocolates priced up to 100 with operations up to 100; and 20 of 1000
chocolates, LeetCode's most, priced up to `10^9`, each batch with the
sum of its answers and a checksum. `chocolates.py` mirrors the ★ arm and
its output is byte-identical.

```
13
6
7
24
11
2000 small cases: costs sum to 608421, checksum 105818710
20 cases of 1000 chocolates: costs sum to 573575073174, checksum 138693319
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: Dijkstra's shortest path over the states (types bought as a
mask, operations taken mod n), where one step buys the chocolate at an
index for its price, getting the type it has now, and another turns
every chocolate on for x; no windows of prices. It draws 1000 random
cases of 1 to 6 chocolates priced up to 20 with operations up to 20,
then 300 of up to 60 chocolates priced up to `10^9`, all before any arm
answers; the literal reading is asked only of the first 1000.

| | property |
|---|---|
| P1 | up to 6 chocolates, the answer is the literal reading's |
| P2 | the prices rotated by 0 to n - 1 places: the same answer |
| P3 | the prices reversed: the same answer |
| P4 | the answer is at least n times the cheapest price and at most the sum of the prices |
| P5 | operations dearer by d: an answer no smaller, and at most (n - 1) d more |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1300 cases: checksum 719668618, 39000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same shortest path over `heapq` gives
the same checksum. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M4 and M6 fail the same checks: both charge
one operation too many at every k.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: n - 1 operations never tried | P1 143, P6 163 |
| M2 | ★: the window one place off | P1 487, P6 770 |
| M3 | table: each row started at the next type's price | P1 441, P3 213, P6 722 |
| M4 | table: one operation too many charged | P1 1000, P4 752, P5 261, P6 1300 |
| M5 | sparse: only the first half of each range read | P1 133, P6 340 |
| M6 | sparse: an operation charged even with none | P1 1000, P4 752, P5 261, P6 1300 |
| M7 | shift: two places an operation | P1 384, P6 657 |
| M8 | shift: the last k kept, not the best | P1 650, P4 654, P6 922 |
| M9 | solution: one operation too few charged | P1 835, P6 1127 |
| M10 | solution: type 0 never narrowed | P1 294, P2 549, P3 654, P6 526 |

## Benchmarks

The bench draws 100 cases of 1000 chocolates, LeetCode's most, priced up
to `10^9`, with operations up to `10^7` so that the best answer takes
many of them, all first, then answers each 3 times by the ★ arm in all
five languages. Every implementation prints `100 cases of 1000
chocolates, 3 rounds: costs sum to 900071089629, checksum 943334264`.

BENCHTAB

## Verification

All five arms print the same output as `chocolates.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 13 edits, the wrapper
included: `struct Solution {}` added, `Vec<i32>` and `Vec<i64>` became
`Vec[i32]` and `Vec[i64]`, the `&v` patterns dropped their `&`,
`f.iter().sum::<i64>() + k as i64 * x as i64` became `f.iter().sum() + k
* x`, since the sum's type follows from `ans` and `i32` widens by
itself, and `Solution::` became `Solution.`.
