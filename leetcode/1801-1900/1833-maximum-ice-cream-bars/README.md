# 1833. Maximum Ice Cream Bars

It is a sweltering summer day, and a boy wants to buy some ice cream
bars. At the store, there are `n` ice cream bars. You are given an array
`costs` of length `n`, where `costs[i]` is the price of the `i`th ice
cream bar in coins. The boy initially has `coins` coins to spend, and he
wants to buy as many ice cream bars as possible. The boy can buy the ice
cream bars in any order. Return the maximum number of ice cream bars the
boy can buy with `coins` coins. You must solve the problem by counting
sort.

```
costs = [1,3,2,4,1], coins = 7      ->  4
costs = [10,6,8,7,7,8], coins = 5   ->  0
costs = [1,6,3,1,2,5], coins = 20   ->  6
```

**Constraints:** `costs.length == n`, `1 <= n <= 10^5`, `1 <= costs[i]
<= 10^5`, `1 <= coins <= 10^8`.

The arms are `fn max_ice_cream(costs: Vec[i64], coins: i64) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `max_ice_cream.kara` ★ | by counting sort, as the problem asks: how many bars cost each price, counted up to the dearest, and the prices walked from the cheapest, buying at each as many of its bars as the coins left will pay for. O(n + M), M the dearest price |
| `max_ice_cream_sort.kara` | a copy of the costs sorted, and the cheapest bars bought one by one while the coins last. O(n log n) |
| `max_ice_cream_heap.kara` | the bars in a `PriorityQueue`, which pops the cheapest first, popped while the coins pay for them. O(n log n) |
| `max_ice_cream_prefix.kara` | a copy of the costs sorted and summed from the cheapest, so the bars bought are the prefix sums the coins cover, found by `partition_point`. O(n log n) |
| `max_ice_cream_solution.kara` | a Rust solution as LeetCode's Rust users write it (`mut costs` sorted in place with `sort_unstable`, and `mut coins` spent down), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples; five
edges, one bar the coins just pay for, one they do not, bars of one
price with coins for some of them, coins for every bar with one to
spare, and the dearest price once (`1 0 3 3 1`); the constraints' most,
10^5 bars of 1 to 10^5 coins, with 10^8 coins and with 1000 (`the most:
14180 48`); and 3000 random cases of 1 to 10 bars of 1 to 20 coins, with
1 to 60 coins (`3000 random cases: checksum 104930837`).
`max_ice_cream.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run`,
`karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★ arm checks clean as first written. The harness was
first written with `max_ice_cream(costs.clone(), ..)` before its last
use of `costs`; check warned that the copy is for a parameter that only
borrows it, and `karac fix` took the `.clone()` off, 1 fix. The sort and
prefix arms were first written `let mut sorted = costs; sorted.sort();`,
with `costs` a bare parameter, which borrows; check refused the sort,
and its message offers `costs: mut ref` with the call sites marked
`mut`, or `own`, or `.clone()` for a copy of the arm's own. `karac fix`
takes the first: it wrote `costs: mut ref Vec[i64]` and `mut` at the
harness's 11 calls, 15 fixes, so the arm sorts its caller's list
(B-2026-11-27-5). The arms take the copy, `let mut sorted =
costs.clone();`, and keep the signature the other arms share. The heap
arm was first written as Rust's, a `BinaryHeap` of the negated costs;
check named Kāra's `PriorityQueue`, which pops the smallest first, and
`karac fix` wrote `PriorityQueue.max_first_from(..)` over the negated
costs, keeping Rust's order, 2 fixes. The arm takes the queue's own
order instead, with no negation. The Rust solution takes 19 fixes by
`karac fix`'s count, and its diff is: `struct Solution {}` added above
the `impl`; `mut costs: Vec<i32>` to `costs: own Vec[i32]` with `let mut
costs = costs;` at the body's start, and `mut coins: i32` to `coins:
i32` with `let mut coins = coins;`; `costs.sort_unstable()` to
`costs.sort()`; `Solution::` to `Solution.` at the harness's 11 calls;
and the harness's `as i64` on the result taken off. `for c in costs`,
which uses the owned list up, is Kāra as it stands. The solution takes a
`Vec[i32]`, so its harness builds its lists as `Vec[i32]` and copies its
largest list for the first of the two calls on it. Every arm's output
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every set of bars the boy could buy, one bit of a mask to a
bar, and the most bars in a set the coins pay for. It runs 2000 random
cases of 1 to 10 bars of 1 to 20 coins, with 1 to 60 coins. Each arm
meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | from none to every bar, none exactly when the cheapest bar costs more than the coins |
| P3 | the bars in reverse order give the same count |
| P4 | more coins never buy fewer bars |
| P5 | a bar dearer than all the coins changes nothing |
| P6 | the ★ arm's answer |

It checks clean as first written. All 60,000 checks pass on every arm:
`2000 cases: checksum 616771581, 60000 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, over the same cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash. The heap
arm's second edit was first to skip a bar too dear and try the next; the
queue pops the bars cheapest first, so every bar after it is dearer
still, and the edit survived as an equivalent. It now buys a bar one
coin dearer than the coins left.

| | edit | failures by property |
|---|---|---|
| M1 | ★: one bar more bought at each price than the coins pay for | P1 174, P6 696 |
| M2 | ★: the dearest price never walked | P1 543, P2 172, P5 543, P6 2172 |
| M3 | sort: a bar costing every coin left not bought | P1 132, P2 20, P6 132 |
| M4 | sort: the bars taken in reverse of their order, unsorted | P1 969, P2 190, P3 788, P5 1684, P6 969 |
| M5 | heap: each bar paid for with one coin | P1 1143, P6 1143 |
| M6 | heap: a bar one coin dearer than the coins left bought | P1 146, P2 29, P5 97, P6 146 |
| M7 | prefix: a prefix costing every coin not bought | P1 132, P2 20, P6 132 |
| M8 | prefix: each prefix sum taken one bar short | P1 1482, P2 126, P5 518, P6 1482 |
| M9 | solution: each bar paid for one coin short | P1 360, P6 360 |
| M10 | solution: the dearest bars bought first | P1 1267, P2 392, P5 1482, P6 1267 |

## Benchmarks

The bench builds one list of 10^5 bars of 1 to 10^5 coins once and makes
1000 calls of the ★ arm on its first 50000 to 99999 bars, with 10^6 to
10^8 coins, each run's length and coins drawn from the checksum so far.
Each call copies its run, as the arm takes its list by value. It checks
clean as first written. Every implementation prints `1000 calls:
checksum 381869219`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.27 s against Rust's 0.25 s (0.27 s with overflow checks
on), C's 0.29 s and Go's 0.82 s; Python takes 4.7 s.
