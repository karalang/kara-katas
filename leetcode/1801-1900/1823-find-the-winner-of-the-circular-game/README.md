# 1823. Find the Winner of the Circular Game

There are `n` friends that are playing a game. The friends are sitting
in a circle and are numbered from `1` to `n` in clockwise order. Moving
clockwise from the `i`th friend brings you to the `(i+1)`th friend for
`1 <= i < n`, and moving clockwise from the `n`th friend brings you to
the `1`st friend. The rules of the game are as follows: start at the
`1`st friend; count the next `k` friends in the clockwise direction,
including the friend you started at, wrapping around the circle, and
possibly counting some friends more than once; the last friend you
counted leaves the circle and loses the game; if there is still more
than one friend in the circle, go back to the second step starting from
the friend immediately clockwise of the friend who just lost, and
repeat; else, the last friend in the circle wins the game. Given the
number of friends, `n`, and an integer `k`, return the winner of the
game.

```
n = 5, k = 2  ->  3
n = 6, k = 5  ->  1
```

**Constraints:** `1 <= k <= n <= 500`.

The arms are `fn find_the_winner(n: i64, k: i64) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `find_the_winner.kara` ★ | Josephus's recurrence, with no circle kept: once the `k`-th friend leaves, the game goes on as a circle of one fewer started `k` places on, so the winner's place among `i` friends is `k` on from its place among `i - 1`. O(n) |
| `find_the_winner_simulate.kara` | the game played out on a list of the friends: the friend `k - 1` places on from the last one to leave is removed, until one is left. O(n^2) |
| `find_the_winner_queue.kara` | the circle as a `VecDeque`: the first `k - 1` friends counted go to the back, and the `k`-th leaves. O(n k) |
| `find_the_winner_recursive.kara` | the ★ arm's recurrence as it is stated, by recursion on the number of friends. O(n) |
| `find_the_winner_solution.kara` | a Rust solution as LeetCode's Rust users write it (the simulate arm's `Vec` and `remove`, with a `usize` index), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples; four edges,
one friend, a count of 1 so the last friend is left, two friends, and a
count that goes round the whole circle (`1 7 1 5`); the constraints'
most, 500 friends counting 500, 1 and 2 (`the most: 69 500 489`); and
3000 random circles of 1 to 40 friends, each with a count from 1 to its
size (`3000 random circles: checksum 493296200`). `find_the_winner.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`.

The Mend loop: every arm and the harness check clean as first written.
The Rust solution takes 17 fixes by `karac fix`'s count, and its diff
is: `struct Solution {}` added above the `impl`; `Vec<i32>` to
`Vec[i32]`; `let mut idx = 0usize` to `let mut idx = 0`, and `idx + k as
usize - 1` to `idx + k - 1`, an `i32` widening to the `i64` index
without a cast; `Solution::` to `Solution.` at the harness's 10 calls;
and the harness's `as i64` on the result taken off. `(1..=n).collect()`
and `friends.remove(idx)` are Kāra as they stand. The solution takes
`i32`s, so its harness passes `n as i32` and `k as i32`. Every arm's
output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the friends 1 to `n` in a circle, each marked in or out; from
the starting friend, `k` friends still in are counted clockwise, the
starting one among them, the last counted leaves, and the friend
clockwise of it starts the next count. It runs 2000 random circles of 1
to 30 friends, each with a count from 1 to its size. Each arm meets six
properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | the winner is one of the friends |
| P3 | the winner among `n` is `k` places on from the winner among `n - 1`, counted from the one who leaves first |
| P4 | counting 1, the last friend is left |
| P5 | counting 2, the winner among `2m` is `2w - 1` and among `2m + 1` is `2w + 1`, `w` the winner among `m` |
| P6 | the ★ arm's answer |

It checks clean as first written. All 60,000 checks pass on every arm:
`2000 cases: checksum 736340880, 60000 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, over the same cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: each circle taken one friend larger | P1 1680, P2 130, P3 800, P5 1800, P6 6720 |
| M2 | ★: the winner's place given from 0 | P1 2000, P2 306, P3 204, P4 2000, P5 1800, P6 8000 |
| M3 | simulate: one friend too many counted | P1 1771, P3 1749, P4 1741, P5 1800, P6 1771 |
| M4 | simulate: the game stopped at two friends | P1 1041, P3 598, P4 1938, P6 1041 |
| M5 | queue: the k-th friend sent back, not out | P1 1771, P3 1749, P4 1741, P5 1800, P6 1771 |
| M6 | queue: the friend before the count's start leaves | P1 1796, P3 1749, P4 1938, P5 950, P6 1796 |
| M7 | recursive: one friend alone placed at 1 | P1 2000, P2 62, P4 2000, P6 2000 |
| M8 | recursive: one friend too few counted | P1 1796, P3 1749, P4 1938, P5 950, P6 1796 |
| M9 | solution: two friends too many counted | P1 1737, P3 1716, P4 1723, P5 1800, P6 1737 |
| M10 | solution: the count started one friend on | P1 1938, P3 279, P4 1938, P5 1800, P6 1938 |

## Benchmarks

The bench makes 200000 calls of the ★ arm on circles of 250 to 499
friends, each circle's size and count drawn from the checksum so far.
Each call is one loop of `n` remainders. It checks clean as first
written. Every implementation prints `200000 calls: checksum 399631271`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.43 s against Rust's 0.43 s (0.43 s with
overflow checks on), C's 0.43 s and Go's 0.59 s; Python takes 2.5 s.
