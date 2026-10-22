# 864. Shortest Path to Get All Keys

You are given an `m x n` grid `grid` where:

- `'.'` is an empty cell,
- `'#'` is a wall,
- `'@'` is the starting point,
- lowercase letters are keys,
- uppercase letters are locks.

You start at the starting point, and one move is one step in one of the
four directions. You cannot walk outside the grid or into a wall. If you
walk over a key, you pick it up, and you cannot walk over a lock unless
you have its key. For some `1 <= k <= 6`, there is exactly one lowercase
and one uppercase letter of the first `k` letters of the English
alphabet in the grid, so each key has exactly one lock, and the letters
used are the first `k`. Return the lowest number of moves to acquire all
keys, or `-1` if it is impossible.

```
grid = ["@.a..", "###.#", "b.A.B"]   ->  8
grid = ["@..aA", "..B#.", "....b"]   ->  6
grid = ["@Aa"]                       ->  -1
```

**Constraints:** `1 <= m, n <= 30`; `grid[i][j]` is an English letter,
`'.'`, `'#'` or `'@'`; there is exactly one `'@'`; the number of keys is
between 1 and 6, with exactly one lock for each.

## Approaches

| file | mechanism |
|---|---|
| `shortest_path_all_keys.kara` ★ | breadth-first search over states: where a walk can go next depends only on the cell it stands on and the keys it holds, so those pairs, `rows * cols * 2^k` of them, are the states. A step moves to a neighbouring cell that is not a wall and not a lock without its key, and picks up any key lying there; the search from the start meets the states in order of distance, and the first state holding every key ends the shortest walk. O(rows * cols * 2^k) |
| `shortest_path_all_keys_dijkstra.kara` | Dijkstra over (point, keys held), the points being the start and the keys: from a point, a breadth-first search over the cells that stops at every key not yet held gives the steps to each key that can come next, and a `PriorityQueue` takes the states in order of steps. O(2^k * k * rows * cols) for the searches |
| `shortest_path_all_keys_orders.kara` | a table over the order the keys are picked up in: between two keys a shortest walk passes only the locks of keys already held, so it is at least the sum of the breadth-first distances with exactly those locks open, and that sum is a real walk, since stepping on a key early only opens more. `best[held][last]` extends to each key not held, the sets in increasing order, as a travelling-salesman table does. O(2^k * k * rows * cols) |
| `shortest_path_all_keys_levels.kara` | the ★ arm's states packed into one integer each, `held * size + cell`, and searched a whole level at a time, the states seen kept in a `Set`; the cells are classified with `match` on byte ranges. O(rows * cols * 2^k) |
| `shortest_path_all_keys_astar.kara` | A* over the ★ arm's states: they leave a `PriorityQueue` in order of steps taken plus the largest Manhattan distance to a key not yet held. Every missing key must still be reached, so the guess never overestimates, and one step changes it by at most one, so a state first leaves the queue by its shortest walk. O(S log S), S states |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 17 lines: LeetCode's three examples; nine more
(a key beside the start on either side, a key behind its own lock, two
keys on either side of the start, a key out of reach, two keys around a
ring, six keys in a row with their locks below them, in both orders, and
two keys walled off); four random 30 x 30 grids, LeetCode's
largest, with six keys and walls on 0, 20, 30 and 40 cells in 100, the
last with no answer; and 1,000 random grids of up to 8 x 8 with one to
six keys, of which 711 have an answer, with the sum of the answers and a
checksum. `shortest_path_all_keys.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the set of (cell, keys held) states some walk can be in after
exactly t moves, found for t = 0, 1, 2, ... with no state ruled out for
having been seen before, and the first t whose set holds a state with
every key. Each set follows from the one before by a fixed rule, so once
a set repeats an earlier one the sets cycle, and if none so far held
every key, none ever will: the answer is -1. Its 4,000 grids are
LeetCode's three examples and random grids of up to 4 x 5 with one to
three keys; 3,148 of them have an answer, and the answers sum to 9,398.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the grid transposed gives the same answer |
| P3 | the grid turned half a turn gives the same answer |
| P4 | the keys renamed by a random permutation, each lock with its key, give the same answer |
| P5 | a lock opened never makes the answer longer (each lock in turn, no answer counting as longest) |
| P6 | a wall on an empty cell never makes the answer shorter (each empty cell in turn) |

It prints `4000 grids, 3148 with every key reached, moves sum to 9398,
183150 checks over 5 arms: 0 failures` under `karac __mir-run` and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a lock passed without its key | P1 846, P2 846, P3 846, P4 846, P6 1601 |
| M2 | ★: a key not picked up | P1 3148, P2 3148, P3 3148, P4 3148, P5 5141 |
| M3 | ★: walls walked through | P1 427, P2 427, P3 427, P4 427, P6 1944 |
| M4 | dijkstra: each leg one step too long | P1 3148, P2 3148, P3 3148, P4 3148, P5 5074 |
| M5 | dijkstra: a lock opened by any key | P1 194, P2 194, P3 194, P4 194, P6 481 |
| M6 | dijkstra: a shorter way to a state not kept | P1 58, P2 58, P3 58, P4 59, P5 172 |
| M7 | orders: every lock shut | P1 326, P2 326, P3 326, P4 326, P5 381 |
| M8 | orders: the first leg with every lock open | P1 739, P2 739, P3 739, P4 739, P6 1230 |
| M9 | orders: only orders ending at the last key | P1 707, P2 707, P3 707, P4 691, P5 1679 |
| M10 | levels: no step down from the second last row | P1 1109, P2 964, P3 1011, P4 1109, P5 2099 |
| M11 | levels: a key picked up as the next letter | P1 3148, P2 3148, P3 3148, P4 3148, P5 5141 |
| M12 | levels: the answer one level late | P1 3148, P2 3148, P3 3148, P4 3148, P5 4985 |
| M13 | astar: the guess the sum of the distances | P1 98, P2 98, P3 96, P4 98, P5 314 |
| M14 | astar: the steps taken left out of the order | P1 52, P2 48, P3 54, P4 52, P5 156 |
| M15 | astar: a step right jumps two cells | P1 1430, P2 1461, P3 1476, P4 1430, P5 1367, P6 2352 |

P1, P2, P3 and P4 each kill all fifteen. The mutations that make an arm
too permissive (M1, M3, M5, M8) are caught by P6 and not P5, and those
that make it too strict or too long by P5 and not P6; M15 does both
and fails both. M2 and M11 are one
fault, no walk ever holding every key, and fail every grid with an
answer. The A* mutations fail the fewest queries: an inadmissible guess
(M13) or a greedy order (M14) is still right on most small grids.

## Verification

Every arm prints the same output as `shortest_path_all_keys.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `3cbb08c045`. Under `karac
__mir-run` the arms take 1 to 4 s and the differential 26 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends run the ★, `dijkstra`, `orders` and `astar`
arms through `karac run --legacy --interp`, `karac run --legacy`, `karac
build` and a `KARAC_AUTO_PAR=1` build with the same output; the builds
of `orders` and `astar` warn that `cells` and `at` are moved and used
again, since legacy reads a bare parameter as owned and v2 borrows it.
They refuse the `levels` arm and the differential at a `*` on a `for`
element, saying the value is not a reference, where v2 yields a
reference. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: a random 30 x 30
grid, LeetCode's largest, with a wall on a cell with chance 20 in 100
and six keys and their locks, built once, and 1,000 rounds that each put
the start on a random open cell, write the grid out as 30 strings, and
find the shortest path. Every round searches up to 57,600 states. The C
and Go mirrors keep the queue in an array with a head and a tail, since
every state enters it at most once; Rust uses `VecDeque`, as Kāra does.
Every implementation prints `1000 starts on a 30 by 30 grid: 997 reach
every key, moves sum to 74954, checksum 99501171`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.74 to 0.84 s | 0.77 s |
| Rust (`rustc -O`) | 0.65 to 0.73 s | 0.70 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.96 to 1.03 s | 1.00 s |
| Go | 2.85 to 3.28 s | 2.94 s |
| Python | 24.7 s | |
| Kāra (`karac build --mir`) | 1.48 to 1.61 s | 1.55 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 863's does. The frozen legacy `karac build`
binary prints the same line in 0.84 to 0.88 s against v2's 1.52 to 1.55 s
over five interleaved runs each.

v2 takes 1.55 times Rust's median time under overflow checks, 2.0 times
C's, and 1.8 times legacy's. Under valgrind's cachegrind C runs 4.08
billion instructions, Rust with overflow checks 7.25 billion, legacy
7.59 billion and v2 15.77 billion. Most of the difference from legacy is
the list of four directions, which v2 allocates on the heap for every
state taken off the queue: callgrind counts 31.9 million `malloc` calls
from `main`, 64 bytes each, and a copy of the program that writes the
list `Array[...]` runs 11.30 billion instructions in 1.26 to 1.32 s. That
is kara B-2026-10-18-52, and the kata keeps the natural spelling. Most of
the rest is most likely the `VecDeque`'s `push_back` and `pop_front`,
which are runtime calls whose `memcpy` goes through the PLT (kara
B-2026-10-13-36, not traced further): v2 has 131 million indirect
branches where C and Rust have almost none. The comparison with C and
Rust waits until after M4.
