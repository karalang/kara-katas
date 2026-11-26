# 1409. Queries on a Permutation With Key

Given the array `queries` of positive integers between `1` and `m`,
process all `queries[i]` (from `i = 0` to `i = queries.length - 1`)
according to the following rules: in the beginning you have the
permutation `P = [1, 2, 3, ..., m]`; for the current `i`, find the
position of `queries[i]` in the permutation `P` (indexing from 0) and
then move it to the beginning of `P`. The position of `queries[i]` in
`P` is the result for `queries[i]`. Return an array containing the
result for the given `queries`.

```
queries = [3, 1, 2, 1], m = 5     ->  [2, 1, 2, 1]
queries = [4, 1, 2, 2], m = 4     ->  [3, 1, 2, 0]
queries = [7, 5, 5, 8, 3], m = 8  ->  [6, 5, 0, 7, 5]
```

**Constraints:** `1 <= m <= 10^3`, `1 <= queries.length <= m`, `1 <=
queries[i] <= m`.

Each arm is `fn process_queries(queries: Vec[i32], m: i32) -> Vec[i32]`.

## Approaches

| file | mechanism |
|---|---|
| `process_queries.kara` ★ | the permutation itself: each query found with `position`, and the part of P up to it turned one place with `p[..=at].rotate_right(1)`, which brings it to the front. O(n m) |
| `process_queries_fenwick.kara` | a Fenwick tree of which slots are taken: the numbers start in slots n + 1 to n + m, and the k-th query moves its number to slot n - k, before every slot used so far, so a position is the count of taken slots before its own. O((n + m) log(n + m)) |
| `process_queries_positions.kara` | where each number is: the one queried goes to 0, and every number that was before it moves one place back. O(n m) |
| `process_queries_deque.kara` | P in a `VecDeque`, each number taken out where it is with `remove` and put back with `push_front`. O(n m) |
| `process_queries_solution.kara` | a Rust solution as LeetCode's Rust users write it (`position(|&x| x == q)`, then `remove` and `insert(0, q)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and two
more (`[2,1,2,1] [3,1,2,0] [6,5,0,7,5] [0] [4,4,4,4,4]`); the
constraints' most, m = 10^3 with 10^3 queries of the largest each time,
rising, and drawn, each answer summed (`m = 10^3: 999 499500 495689`);
and 2000 random cases of m up to 40 with 1 to m queries (`2000 random
cases: 276359 in all, checksum 892141705`). `process_queries.py` mirrors
the ★ arm, and its output is byte-identical. Every arm gives the same
output under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★, positions and deque arms check clean as first
written. The Fenwick arm takes one round of 2 fixes: its `let mut sum =
0` summed `i32` counts into an `i64`, since an operator does not fix a
literal's type (design.md §8), and `karac fix` declares `sum: i32`; and
`Vec.filled(n + m as i64 + 1, 0)` carries a cast the widening makes
unneeded, which the fix drops. The Rust solution takes one round of 18
fixes by `karac fix`'s count: `struct Solution;` to `struct Solution
{}`, `Vec<i32>` to `Vec[i32]`, `Vec::with_capacity` to
`Vec.with_capacity`, the closure's `|&x|` to `|x|`, and `Solution::` to
`Solution.`. Its output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: P built as 1 to m, each query's place counted by a walk over
all of P, and P rebuilt as the query followed by the rest of P without
it. LeetCode's examples, four edge cases (m = 1, every number once
falling and rising, one number again and again) and the constraints'
most, and 1995 random cases, m up to 12 two times in three and up to 200
otherwise, with 1 to m queries.

The cases are written `[3i32, 1, 2, 1].to_vec()`. Written `[3, 1, 2,
1].to_vec()`, as the arms' callers write a bare `[3, 1, 2, 1]`, check
refuses `cases.push(([3, 1, 2, 1].to_vec(), 5))` into a `Vec[(Vec[i32],
i32)]` as a `Vec[i64]`, with no fix, while the same literal given a
`let` annotation or a parameter's type takes `i32`: B-2026-11-26-6,
found at kata 1406. The suffix is the error's own advice.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | one answer for each query, each a place in P, 0 to m - 1 |
| P3 | a query seen for the first time is at q - 1 plus how many distinct numbers larger than q were queried before it |
| P4 | a repeated query is at how many distinct numbers were queried since its last time |
| P5 | a query right after the same query is at 0 |
| P6 | the ★ arm's answer |

All 234,920 checks pass on every arm: `2003 cases: checksum 275138257,
234920 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by `list.index`
and `insert`, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the part up to the query turned the other way, `rotate_left(1)` | P1 1405, P3 24657, P4 10206, P5 628, P6 5620 |
| M2 | ★: each place answered one too high | P1 2003, P2 887, P3 29581, P4 10587, P5 807, P6 8012 |
| M3 | Fenwick: the count of taken slots taken through the query's own slot | P1 2003, P2 887, P3 29581, P4 10587, P5 807, P6 2003 |
| M4 | Fenwick: the slot a number leaves not freed | P1 1417, P2 1057, P3 25702, P4 6196, P6 1417 |
| M5 | positions: the number m never moved back | P1 142, P4 481, P6 142 |
| M6 | positions: the number queried left where it was, not put at 0 | P1 1129, P3 14658, P4 10491, P5 766, P6 1129 |
| M7 | deque: the number queried put at the back | P1 1647, P3 27578, P4 10542, P5 807, P6 1647 |
| M8 | deque: the number queried swapped with the front, not moved there | P1 1357, P3 24743, P4 9589, P6 1357 |
| M9 | solution: the number queried pushed at the back | P1 1647, P3 27578, P4 10542, P5 807, P6 1647 |
| M10 | solution: P starting from m down to 1 | P1 1863, P3 28935, P6 1863 |

A first M1, the part before the query turned (`p[..at]`), was killed by
a panic, `rotate_right` refusing a turn longer than an empty slice, and
a first M5, a number at the queried place moved back too, changed
nothing, since the queried number is then put at 0 anyway; both were
replaced.

## Benchmarks

The bench runs the ★ arm on 300 rounds of 10^3 queries with m = 10^3,
each round's queries drawn from the checksum so far, folding every
answer. Every implementation prints `300 rounds of 10^3 queries:
checksum 172148327`.

BENCHTAB

Kāra runs at about three and a half times Rust's time here, and the
overflow checks are not why: Rust with `-C overflow-checks=on` is as
fast. The search compiles to the same loop as C's; the turn is the
difference. Kāra's `rotate_right` turns the slice by three reversals of
element swaps, where Rust's moves the elements once with a `memmove`, as
the C mirror does by hand: B-2026-11-26-7.
