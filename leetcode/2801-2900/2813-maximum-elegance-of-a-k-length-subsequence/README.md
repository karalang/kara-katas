# 2813. Maximum Elegance of a K-Length Subsequence

You are given a **0-indexed** 2D integer array `items` of length `n` and
an integer `k`.

`items[i] = [profit_i, category_i]`, where `profit_i` and `category_i`
denote the profit and category of the `i`th item respectively.

Let's define the **elegance** of a **subsequence** of `items` as
`total_profit + distinct_categories^2`, where `total_profit` is the sum
of all profits in the subsequence, and `distinct_categories` is the
number of **distinct** categories from all the categories in the
selected subsequence.

Your task is to find the **maximum elegance** from all subsequences of
size `k` in `items`.

Return *an integer denoting the maximum elegance of a subsequence of*
`items` *with size exactly* `k`.

```
items = [[3,2],[5,1],[10,1]],       k = 2  ->  17
items = [[3,1],[3,1],[2,2],[5,3]],  k = 3  ->  19
items = [[1,1],[2,1],[3,1]],        k = 3  ->  7
```

**Constraints:** `1 <= items.length == n <= 10^5`; `items[i].length == 2`;
`items[i][0] == profit_i`; `items[i][1] == category_i`;
`1 <= profit_i <= 10^9`; `1 <= category_i <= n`; `1 <= k <= n`.

## Approaches

| file | mechanism |
|---|---|
| `elegance.kara` ★ | the items sorted dearest first by `sort_by`, the k dearest taken, the profits of those whose category was already taken kept on a stack; each later item of a new category swaps in for the top of the stack, the cheapest repeat, and the best total plus the distinct count squared is the answer |
| `elegance_heap.kara` | the same swap with the repeats in a smallest-first `PriorityQueue` and the categories taken marked in a `Vec[bool]` indexed by category, sorted by `sort_by_key` on the profit negated |
| `elegance_counts.kara` | by the number of categories: each category's dearest item its head, the rest tails, kept in a `Map`; for each count d the d dearest heads and the k - d dearest tails by prefix sums, plus d squared, the best over every d both lists can fill |
| `elegance_prefix.kara` | the swap laid out as two lists over tuples sorted and reversed: the repeats among the k dearest and the first item of each new category after them, every number of swaps scored at once by a running sum |
| `elegance_solution.kara` | a Rust solution as LeetCode's Rust users write it, `mut items` sorted by `sort_unstable_by`, a `HashSet` whose `insert` answers whether the category is new and a `Vec` of repeats, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples; 1000
items of one category with the 500 dearest taken; 1000 items of 1000
categories, every one taken; 3000 random cases of 1 to 8 items with
profits up to 10 and categories up to the count; and 50 of up to 1000
items with profits up to 10^9, the last two as checksums.
`elegance.py` mirrors the ★ arm and its output is byte-identical.

```
17
19
7
375250000001
1000001000000
3000 small cases: checksum 446161120
50 large cases: checksum 465056052
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every choice of k of the items, as a bit mask, scored as its
total profit plus the square of how many categories it holds, counted
with a `Set`; no sort, no swap and no heads. It draws 2000 random cases
of 1 to 8 items with profits up to 10 and categories up to the count,
then 50 of up to 1000 items with profits up to 10^9, all before any arm
answers; the literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 8 items, the answer is the literal reading's |
| P2 | at least the k dearest profits plus 1, at most them plus k squared |
| P3 | the items in reverse: the same answer |
| P4 | every profit 1000 more: the answer 1000 k more |
| P5 | k the whole count: every profit plus the categories squared |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 479842993, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the cheapest repeat taken from the bottom of the stack | P1 58, P3 20, P6 58 |
| M2 | ★: the swaps stop at the first item of a taken category | P1 64, P3 36, P6 64 |
| M3 | heap: a largest-first queue of repeats | P1 58, P3 20, P6 58 |
| M4 | heap: the newcomer's category never marked | P1 3, P3 4, P6 3 |
| M5 | counts: a category's head its cheapest item | P1 918, P2 271, P6 968 |
| M6 | counts: every count of heads scored with no room check | killed under both: runtime error: index out of bounds |
| M7 | prefix: the first repeat traded first | P1 60, P6 60 |
| M8 | prefix: the last swap never scored | P1 306, P6 306 |
| M9 | solution: the dearest sorted last | P1 1302, P2 948, P6 1352 |
| M10 | solution: the best scored before the swaps only | P1 313, P3 80, P6 313 |

## Benchmarks

The bench draws 10 cases of 10^5 items, LeetCode's most, with profits
up to 10^9, categories up to 30000 and k from 1 to 10^5, all of them
first, then answers each 5 times by the ★ arm in all five languages,
each answer sorting a fresh copy: Rust by its stable `sort_by`, Go by
`slices.SortStableFunc`, C by `qsort`; C marks the categories in an
array indexed by category where the others hash them. Every
implementation prints `10 cases of 100000, 5 rounds: elegance sums to
1832741593352785, checksum 969933058`.

BENCHTAB

## Verification

All five arms print the same output as `elegance.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms and the harness checked clean as first written.

LeetCode's Rust template took 29 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `use` line; the
`mut items` parameter became `items: own Vec[Vec[i32]]` and a `let mut
items = items;`; `sort_unstable_by` became `sort_by`, Kāra's sort being
stable, and `cmp(&a[0])` lost its `&`; `HashSet::new()` became
`Set.new()`, and `Vec::new` and `Solution::` took `.`; `k as usize`
became `k as i64`; `!` became `not`; the `as i64` widenings went, an
`i32` widening implicitly; and `Vec<..>` became `Vec[..]`.
