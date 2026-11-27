# 1798. Maximum Number of Consecutive Values You Can Make

You own `n` coins, the `i`th worth `coins[i]`. You can make a value `x`
if some of your coins sum to `x`. Return the largest number of
consecutive integer values you can make, starting from and including
`0`. Several coins may have the same value.

```
coins = [1,3]           ->  2
coins = [1,1,1,4]       ->  8
coins = [1,4,10,3,1]    ->  20
```

**Constraints:** `coins.length == n`, `1 <= n <= 4 * 10^4`, and `1 <=
coins[i] <= 4 * 10^4`.

The arms are `fn get_maximum_consecutive(coins: Vec[i32]) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `get_maximum_consecutive.kara` ★ | greedy over the sorted coins: if every value from 0 to `reach` can be made, a coin `c` no larger than `reach + 1` extends that to `reach + c`, and a coin any larger leaves `reach + 1` out for good, every later coin being larger still. O(n log n) |
| `get_maximum_consecutive_heap.kara` | the same greedy taking the coins smallest first from a `PriorityQueue`, stopping at the first that leaves a gap. O(n log n) |
| `get_maximum_consecutive_count.kara` | the same greedy over a count of each coin value, walked upward: the coins of value `v` reach `reach + count * v` together if the first of them fits. O(n + largest coin) |
| `get_maximum_consecutive_scan.kara` | the same greedy as an iterator: `scan` threads the reach through the sorted coins and stops at the first that leaves a gap, and the last reach it yields is the answer less one. O(n log n) |
| `get_maximum_consecutive_solution.kara` | a Rust solution as LeetCode's Rust users write it (`mut coins`, `sort_unstable`, the answer kept one ahead of the reach), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples (`2 8 20`);
five edges, one coin of 1, one coin of 2, the powers of two, three ones,
and a coin too large after two ones (`2 1 16 4 3`); the constraints'
most, 40000 coins of 40000, 40000 ones, the coins 40000 down to 1, and
40000 coins at random (`the most: 1 40001 800020001 654557742`); and
3000 random cases of 1 to 15 coins (`3000 random cases: checksum
837857310`). `get_maximum_consecutive.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the count arm and the harness check clean as first
written. The ★ and heap arms start the reach as `let mut reach = 0;`,
and check refuses it, the literal having kept its default `i64` where an
`i32` is returned; `karac fix` writes `let mut reach: i32 = 0;`, 1 fix
each. The scan arm, `sorted.iter().scan(0, |reach, c| if c > reach + 1 {
None } else { Some((reach + c, reach + c)) }).last().unwrap_or(0)`, was
refused at `reach + 1` with "write an explicit 'as i32'" and no fix:
B-2026-11-27-25, the scan's seed traced to its literal only when the
closure ended in a bare `Some((s, s))` and the result was read with
`unwrap`. Fixed at a63d22b535: `karac fix` now writes `scan(0i32, ..)`,
1 fix. The Rust solution takes one round of 11 fixes by `karac fix`'s
count, and its diff is: `struct Solution;` to `struct Solution {}`, `mut
coins: Vec<i32>` to `coins: own Vec[i32]` with `let mut coins = coins;`
at the body's start, `sort_unstable()` to `sort()`, `let mut ans = 1;`
to `let mut ans: i32 = 1;`, the wrapper's `coins: Vec<i32>` to `coins:
own Vec[i32]`, and `Solution::` to `Solution.`. Every arm's output
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every subset of the coins summed, and the values made counted
up from 0 to the first one missing, while there are at most 14 coins.
LeetCode's examples, the five edges, 3000 coins at random and 3000 ones,
and 1990 random cases of 1 to 14 coins. Each arm meets six properties on
each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally, while there are at most 14 coins |
| P2 | the coins in reverse order give the same answer |
| P3 | one more coin of 1 raises the answer by at least 1 |
| P4 | one more coin worth the answer at least doubles it |
| P5 | one more coin above the sum of all of them plus 1 changes nothing |
| P6 | the ★ arm's answer |

The differential's literal reading was first written with `sum +=
coins[i] as i64`, and `karac fix` removed the cast, 1 fix. All 59,990
checks pass on every arm: `2000 cases: checksum 560055801, 59990 checks
over 5 arms: 0 failures`, under `karac __mir-run`, `karac run`, `karac
build` and `karac __mir-llvm-run`. Python, running the ★ arm's mirror
over the same cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a coin two above the reach taken as fitting | P1 491, P4 1964, P5 1539, P6 1964 |
| M2 | ★: the count of values one short, 0 left out | P1 1998, P4 7316, P6 8000 |
| M3 | heap: the coins taken largest first | P1 1122, P3 1789, P4 2000, P5 211, P6 1122 |
| M4 | heap: each coin taken as worth 1 | P1 918, P4 1205, P6 918 |
| M5 | count: each coin value counted once | P1 1063, P3 1333, P4 1064, P6 1064 |
| M6 | count: the largest coin value never walked | P1 1101, P3 211, P4 607, P5 1102, P6 1102 |
| M7 | scan: a coin one above the reach taken as leaving a gap | P1 1332, P3 2000, P4 2000, P6 1333 |
| M8 | scan: the reach taken as 1 when no coin fits | P1 666, P3 327, P4 327, P6 667 |
| M9 | solution: a coin equal to the answer taken as leaving a gap | P1 1332, P3 2000, P4 2000, P6 1333 |
| M10 | solution: the answer started at 0 | P1 1998, P3 2000, P6 2000 |

## Benchmarks

The bench builds 200 random lists of 2000 coins of 1 to 200 once, and
makes 20000 calls of the ★ arm, each list drawn from the checksum so
far; each call sorts its own copy. C sorts with `qsort` and a comparison
function. It checks clean as first written. Every implementation prints
`20000 calls over 200 lists of 2000 coins: checksum 827643326`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.47 s against Rust's 0.61 s (0.63 s with
overflow checks on), C's 3.3 s and Go's 2.0 s; Python takes 6.2 s.
