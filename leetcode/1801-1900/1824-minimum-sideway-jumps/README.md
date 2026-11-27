# 1824. Minimum Sideway Jumps

There is a 3 lane road of length `n` that consists of `n + 1` points
labeled from `0` to `n`. A frog starts at point `0` in the second lane
and wants to jump to point `n`. However, there could be obstacles along
the way. You are given an array `obstacles` of length `n + 1` where each
`obstacles[i]` (ranging from 0 to 3) describes an obstacle on the lane
`obstacles[i]` at point `i`. If `obstacles[i] == 0`, there are no
obstacles at point `i`. There will be at most one obstacle in the 3
lanes at each point. The frog can only travel from point `i` to point
`i + 1` on the same lane if there is not an obstacle on the lane at point
`i + 1`. To avoid obstacles, the frog can also perform a side jump to
jump to another lane (even if they are not adjacent) at the same point
if there is no obstacle on the new lane. Return the minimum number of
side jumps the frog needs to reach any lane at point `n` starting from
lane 2 at point 0. There will be no obstacles on points `0` and `n`.

```
obstacles = [0,1,2,3,0]    ->  2
obstacles = [0,1,1,3,3,0]  ->  0
obstacles = [0,2,1,0,3,0]  ->  2
```

**Constraints:** `obstacles.length == n + 1`, `1 <= n <= 5 * 10^5`, `0
<= obstacles[i] <= 3`, `obstacles[0] == obstacles[n] == 0`.

The arms are `fn min_side_jumps(obstacles: Vec[i64]) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `min_side_jumps.kara` ★ | the fewest side jumps that put the frog in each of the three lanes at the point reached, carried forward a point at a time in an `Array` of three: a lane with an obstacle there cannot be stood in, and any other can be reached from the best lane with one jump. O(n) |
| `min_side_jumps_greedy.kara` | greedy: the frog runs on until the point ahead is blocked, then jumps to the free lane whose next obstacle is farthest off; where each lane's next obstacle lies, from every point, is found by one walk back along the road. O(n) |
| `min_side_jumps_bfs.kara` | a shortest path over the (point, lane) places: a step forward costs nothing and a side jump costs one, so a `VecDeque` searched front first, a free move pushed to the front and a jump to the back, finds each place's fewest jumps. O(n) |
| `min_side_jumps_table.kara` | the ★ arm's recurrence kept whole, a `Vec` of one `Array` of three per point, each point's row read from the row before it. O(n) |
| `min_side_jumps_solution.kara` | a Rust solution as LeetCode's Rust users write it (the ★ arm's three counts, `i32::MAX / 2` for a lane blocked), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples; four
edges, a road of one step, the frog's lane blocked at once and to the
end, obstacles that send it from lane to lane, and a road with none (`0
1 5 0`); the constraints' most, a road of 5 * 10^5 steps with an
obstacle in every lane in turn, and one with none (`the most: 499998
0`); and 3000 random roads of 1 to 20 steps, an obstacle at half the
points in a lane drawn at random (`3000 random roads: checksum
653759167`). `min_side_jumps.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: every arm and the harness check clean as first written.
The Rust solution takes 16 fixes by `karac fix`'s count, and its diff
is: `struct Solution {}` added above the `impl`; `Vec<i32>` to
`Vec[i32]`; `for &o in obstacles.iter().skip(1)` to `for o in ..`, a
Kāra pattern matching through the reference; `i32::MAX` to `i32.MAX`;
`Solution::` to `Solution.` at the harness's 10 calls; and the harness's
`as i64` on the result taken off. `dp[(o - 1) as usize]`,
`*dp.iter().min().unwrap()` and `j as i32 != o - 1` are Kāra as they
stand. The solution takes a `Vec[i32]`, so its harness builds its roads
as `Vec[i32]`. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the places the frog can stand with no jump, then with one
more jump at a time, each set run forward as far as the lane is clear,
until one of them stands at the end of the road. It runs 2000 random
roads of 1 to 15 steps, an obstacle at half the points in a lane drawn
at random. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | no more jumps than obstacles, each passed with one at most |
| P3 | lanes 1 and 3 swapped give the same answer, the frog starting between them |
| P4 | with nothing in lane 2 the frog never jumps |
| P5 | every point given twice gives the same answer |
| P6 | the ★ arm's answer |

It checks clean as first written. All 60,000 checks pass on every arm:
`2000 cases: checksum 512238938, 60000 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, over the same cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash. The bfs arm's
second edit was first to stop the search one point short of the end; the
last point is never blocked, so a place one short always runs on to it,
and the edit survived as an equivalent. It now allows a jump into a lane
with an obstacle at that point.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a side jump counted as two | P1 671, P2 12, P6 2684 |
| M2 | ★: the frog free to start in any lane | P1 937, P6 3748 |
| M3 | greedy: the nearer obstacle's lane taken | P1 699, P6 699 |
| M4 | greedy: the jump made one point late | P1 176, P6 176 |
| M5 | bfs: the search started from lane 1 | P1 2000, P2 2000, P4 2000, P5 2000, P6 2000 |
| M6 | bfs: a jump into an obstacle's lane allowed | P1 176, P6 176 |
| M7 | table: the frog free to start in any lane | P1 937, P6 937 |
| M8 | table: each step forward counted as a jump | P1 2000, P2 2000, P4 2000, P5 2000, P6 2000 |
| M9 | solution: every lane set to a jump from the best | P1 2000, P2 2000, P4 2000, P5 2000, P6 2000 |
| M10 | solution: the first point past the start skipped | P1 175, P5 175, P6 175 |

## Benchmarks

The bench builds one road of 5 * 10^5 steps with an obstacle at half its
points once and makes 50 calls of the ★ arm on roads of its first 250000
to 499999 steps, each road's length drawn from the checksum so far and
its last point cleared. Each call is handed its own copy of the road. It
checks clean as first written. Every implementation prints `50 calls:
checksum 994466298`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.18 s against Rust's 0.20 s (0.20 s with
overflow checks on), C's 0.19 s and Go's 0.41 s; Python takes 7.0 s.
