# 1776. Car Fleet II

There are `n` cars traveling at different speeds in the same direction
along a one-lane road. You are given an array `cars` of length `n`,
where `cars[i] = [position_i, speed_i]`: `position_i` is the distance in
meters between the `i`th car and the beginning of the road, and it is
guaranteed that `position_i < position_i+1`; `speed_i` is the initial
speed of the `i`th car in meters per second. For simplicity, cars can be
considered as points moving along the number line. Two cars collide when
they occupy the same position. Once a car collides with another car,
they unite and form a single car fleet. The cars in the formed fleet
will have the same position and the same speed, which is the initial
speed of the slowest car in the fleet. Return an array `answer`, where
`answer[i]` is the time, in seconds, at which the `i`th car collides
with the next car, or `-1` if the car does not collide with the next
car. Answers within `10^-5` of the actual answers are accepted.

```
cars = [[1,2],[2,1],[4,3],[7,2]]  ->  [1.00000,-1.00000,3.00000,-1.00000]
cars = [[3,4],[5,4],[6,3],[9,1]]  ->  [2.00000,1.00000,1.50000,-1.00000]
```

**Constraints:** `1 <= cars.length <= 10^5`, `1 <= position_i, speed_i
<= 10^6`, and `position_i < position_i+1`.

The arms are `fn get_collision_times(cars: Vec[Vec[i32]]) -> Vec[f64]`.

## Approaches

| file | mechanism |
|---|---|
| `get_collision_times.kara` ★ | from the right, a stack of the cars ahead: a car ahead is popped when it is no slower, or when it joins its own fleet before this car could reach it, and the car left on top is the one this car runs into. O(n) |
| `get_collision_times_jump.kara` | from the right, each car looks at the car just ahead, and while it cannot reach that car before the car joins its own fleet, moves on to the car that one runs into, kept in a `hit` list |
| `get_collision_times_skip.kara` | a scan over every car ahead: the first slower car that this car reaches before that car has joined a fleet is the one it runs into. O(n^2) |
| `get_collision_times_tuples.kara` | the stack holds each car ahead as a tuple of its position, its speed and the time it joins a fleet, so a car's turn reads only the stack, never the answers. O(n) |
| `get_collision_times_solution.kara` | a Rust solution as LeetCode's Rust users write it (`vec![-1.0; n]`, `Vec<usize>`, `while let Some(&j) = st.last()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`[1.00000,
-1.00000, 3.00000, -1.00000] [2.00000, 1.00000, 1.50000, -1.00000]`);
five edges, one car, two at one speed, the faster behind, a car ahead
that joins its fleet first so that the car behind runs into the fleet,
and every car slower than the one behind it (`[-1.00000] [-1.00000,
-1.00000] [1.00000, -1.00000] [1.50000, 1.00000, -1.00000] [1.00000,
1.00000, 1.00000, -1.00000]`); the constraints' most, 100000 cars at
random and 100000 each a step ahead at one less speed, each answer
digested to five places (`the most: 618674824 49871256`); and 3000
random cases of 1 to 20 cars (`3000 random cases: checksum 45707243`).
`get_collision_times.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the jump, skip and tuples arms check clean as first
written. The ★ arm was first written with `while let Some(&j) =
stack.last()` and `if let Some(&j) = stack.last()`; check named the `&`
before a pattern as Rust syntax that copies the value out of a borrowed
`Some`, and `karac fix` wrote `Some(j) = stack.last().cloned()` for
both, 4 fixes by its count. The Rust solution takes one round of 23
fixes, and its diff is: `struct Solution;` to `struct Solution {}`,
`Vec<Vec<i32>>` and `Vec<f64>` to `Vec[Vec[i32]]` and `Vec[f64]` in both
signatures, `vec![-1.0; n]` to `Vec.filled(n, -1.0)`, `Vec<usize>` and
`Vec::new()` to `Vec[i64]` and `Vec.new()`, both `Some(&j) = st.last()`
to `Some(j) = st.last().cloned()`, `||` to `or`, `&&` to `and`, and
`Solution::` to `Solution.`.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the road run catch by catch, each time taking the earliest
catch between two neighbouring fleets, worked out in whole numbers,
setting the time of the car that catches up and merging it into the
fleet ahead, until no fleet is faster than the one in front. LeetCode's
examples, six edges, and 1992 random cases of 1 to 12 cars. Each arm
meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | -1 exactly for a car with no slower car ahead, and every other time above 0 |
| P3 | each time is the earliest at which the car would catch a slower car ahead running free |
| P4 | every car moved on by the same distance gives the same times |
| P5 | every gap doubled gives every time doubled |
| P6 | the ★ arm's answer |

The differential checks clean as first written. All 60,000 checks pass
on every arm: `2000 cases: checksum 227530995, 60000 checks over 5 arms:
0 failures`, under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. Python, running the road catch by catch, gives
the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a car that never joins a fleet popped as though it had | P1 1474, P2 1474, P3 1474, P6 5896 |
| M2 | ★: a car that joins a fleet never put on the stack | P1 588, P3 588, P6 2352 |
| M3 | jump: the last car's time never worked out | P1 1099, P2 1099, P3 1099, P6 1099 |
| M4 | jump: the closing speed taken as the two speeds' sum | P1 1474, P3 1474, P6 1474 |
| M5 | skip: the scan going on past the car it runs into | P1 1191, P3 1191, P6 1191 |
| M6 | skip: the car just ahead never looked at | P1 1474, P2 1023, P3 1474, P6 1474 |
| M7 | tuples: every car ahead taken never to join a fleet | P1 398, P3 398, P6 398 |
| M8 | tuples: the closing speed taken as the car's own | P1 1474, P3 1474, P6 1474 |
| M9 | solution: the closing speed taken as the car's own | P1 1474, P3 1474, P6 1474 |
| M10 | solution: a car joining its fleet within the first second kept on the stack | P1 190, P3 190, P5 100, P6 190 |

## Benchmarks

The bench builds 20 lists of 100000 cars once, half at speeds up to
1000000 and half up to 100, and makes 200 calls of the ★ arm, each list
and the time read from it drawn from the checksum so far. Every
implementation prints `200 calls over 20 lists: checksum 801492013`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.57 s against Rust's 0.49 s (0.50 s with overflow checks
on), C's 0.35 s and Go's 0.66 s; Python takes 14.0 s.
