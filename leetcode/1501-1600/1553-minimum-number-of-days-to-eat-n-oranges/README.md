# 1553. Minimum Number of Days to Eat N Oranges

There are `n` oranges in the kitchen, and each day you can eat them in one
of these ways: eat one orange; if the number of remaining oranges `n` is
divisible by 2, eat `n / 2` of them; if it is divisible by 3, eat
`2 * (n / 3)` of them. You can choose only one action per day. Given `n`,
return the minimum number of days to eat all `n` oranges.

```
n = 10  ->  4   (eat 1, then 9 / 3 * 2 = 6, then 3 / 3 * 2 = 2, then 1)
n = 6   ->  3   (eat 3, then 3 / 3 * 2 = 2, then 1)
```

**Constraints:** `1 <= n <= 2 * 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `oranges.kara` ★ | eating one at a time is only worth it on the way to a pile that halves or thirds, so from `n` the best is `n % 2` single days and a halving, or `n % 3` single days and a thirding. The piles reached are `n / (2^a 3^b)`, few enough to keep every answer in a `Map` (an `if let` on `get`). O(log² n) piles |
| `oranges_bfs.kara` | the statement as a graph searched breadth first: each pile a state, each day one of up to three moves, a `VecDeque` of `(pile, day)` drained by `while let`, a `Set` so a pile is queued once; the first day the queue reaches 0 is the answer |
| `oranges_dijkstra.kara` | the ★ arm's reduced moves as a weighted graph, a halving costing `n % 2 + 1` days and a thirding `n % 3 + 1`: Dijkstra by a `PriorityQueue` (smallest first) of `(days, pile)`, a `Set` of settled piles |
| `oranges_solution.kara` | LeetCode's Rust template (`min_days(n: i32) -> i32`, the ★ arm with a `HashMap` passed down to an associated `Self::dfs`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's two examples, then `n` of
1, 2, 3, 4, 56, 820592, 10^9 and 2·10^9; then the total and a checksum of
the answers for 3000 random piles of up to 1000, 300 of up to 10^6 and
100 of up to 2·10^9. `oranges.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the fewest days for every pile from 0 up to 2000, each pile one
day more than the best of the piles its allowed moves reach. It checks
3000 piles of 1 to 2000, every random choice drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is from 1 to `n`, and `3^(answer - 1)` is at least `n`: no day leaves less than a third, and the last day eats 1 |
| P3 | one orange more needs at most one day more |
| P4 | twice or three times the pile needs at most one day more |
| P5 | six times the pile needs at most two days more |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 579799799, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` (the interpreter takes about
30 s on the differential, so the timeout here was 150 s). All ten are
killed, each the same way under both backends. Two first choices were
equivalent and were replaced: the ★ arm answering 1 for a pile of 0 (a
pile of 0 is only reached from 2 by a thirding, which the halving beats),
and the template stopping at `n <= 2` (a pile of 2 takes 2 days).

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the recursion stopping only at 0 | P1 3000, P2 3, P6 3000 |
| M2 | ★: a halving charged no single days | P1 2824, P6 2824 |
| M3 | ★: the worse of halving and thirding taken | P1 2999, P2 2, P3 2, P4 2723, P5 2723, P6 2999 |
| M4 | bfs: a thirding eats a third, not two thirds | P1 2948, P4 2497, P5 2497, P6 2948 |
| M5 | bfs: a halving only on piles divisible by 4 | P1 1346, P4 854, P5 846, P6 1346 |
| M6 | dijkstra: a thirding a day cheaper | P1 2997, P2 2210, P6 2997 |
| M7 | dijkstra: the last orange free | P1 3000, P2 59, P6 3000 |
| M8 | dijkstra: the queue largest first | P1 2995, P2 2, P3 113, P4 2648, P5 2501, P6 2995 |
| M9 | template: each answer kept under the half pile | P1 2486, P4 1451, P5 1246, P6 2486 |
| M10 | template: piles up to 3 answered by their size | P1 780, P4 1, P6 780 |

## Benchmarks

The bench draws 20000 piles of 1 to 2·10^9 once and asks each 3 times by
the ★ arm, with a fresh map per call, in all five languages. Kāra's `Map`
and Rust's `HashMap` are both SipHash-1-3, Go's is its own map, and C's
is an open-addressing table of 1024 slots, zeroed per call and hashed by
a multiply. Every implementation prints `3 passes over 20000 piles of up
to 2000000000: 1884543 days, checksum 86844006`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.174 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.844 s |
| Kāra (`karac build`) | 0.847 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.861 s |
| Rust (`rustc -O`) | 0.914 s |
| Go | 1.349 s |
| Python | 5.2 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (1.22 s and 1.25 s on one run).

Kāra is 1.02x Rust under overflow checks by median. Not traced. Every
call builds and drops a map of a few hundred entries, so hashing and
growing the map are most of every row; C's fixed table with a multiply
hash is why it leads by a factor of five.

## Verification

All four arms print the same output as `oranges.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The ★, BFS and Dijkstra arms were written in Kāra and checked as written.

The Rust template took 6 changed lines and the `use` removed, then 3 and
2, over three rounds: `use std::collections::HashMap` dropped,
`HashMap<i32, i32>` and `HashMap::new()` to `HashMap[i32, i32]` and
`HashMap.new()`, `&mut memo` to `mut memo` and `&mut HashMap<..>` to
`mut ref HashMap[..]`, `if let Some(&v) = memo.get(&n)` to
`if let Some(v) = memo.get(n).cloned()`, and every `Self::dfs` and
`Solution::` to `Solution.`; then `struct Solution {}` added and
`HashMap` to `Map` in both places; then `mut` added to both recursive
`memo` arguments (every argument to a mutating parameter is marked) and
the closing `as i64` dropped. It checks and agrees with no hand edit.
