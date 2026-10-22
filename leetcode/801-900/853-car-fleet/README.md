# 853. Car Fleet

`n` cars drive along a one-lane road to a destination `target` miles
away: car `i` starts at `position[i]` and drives at `speed[i]` miles per
hour. A car can never pass the car ahead of it, but it can catch it up
and then drive bumper to bumper at the slower car's speed. A car fleet
is a car, or a set of cars driving together at the same position and
speed; a car that catches a fleet exactly at the destination still joins
it. Return the number of fleets that arrive at the destination.

```
target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3]  ->  3
target = 10, position = [3], speed = [3]                   ->  1
target = 100, position = [0,2,4], speed = [4,2,1]          ->  1
```

**Constraints:** `1 <= n <= 10^5`, `0 < target <= 10^6`, `0 <=
position[i] < target`, every position is distinct, and `0 < speed[i] <=
10^6`.

## Approaches

| file | mechanism |
|---|---|
| `car_fleet.kara` ★ | closest to the target first: a car can only be held up by the cars ahead, so taking the cars from the closest to the target back, one that would arrive no later than the fleet ahead on its own joins it, and one that would arrive later leads a new fleet. Times `(target - p) / s` are compared as fractions, `(target - p1) * s2` against `(target - p2) * s1`, so no rounding can merge or split two fleets. O(n log n) time |
| `car_fleet_stack.kara` | a stack of fleets, from the back: taking the cars from the farthest forward, a car pops every fleet on the stack that would arrive no later than it, since those fleets are behind it and cannot pass, and is pushed; what is left is one entry a fleet. O(n log n) time |
| `car_fleet_slots.kara` | one slot for each position: positions are distinct and below `target`, so each car's speed goes in its position's slot and the slots are walked from the target back, with no sort. O(n + target) time |
| `car_fleet_fold.kara` | the distances to the target and speeds zipped, sorted, and folded over from the target back, carrying the slowest arrival so far and the count: a car leads a fleet exactly when it would arrive later than every car ahead of it. O(n log n) time |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 15 lines: LeetCode's three examples; eight
more (three cars that all meet, a faster car behind that cannot catch up
before the target, a car catching another exactly at the target and one
that does not, four cars at one speed and four that close up, a slow car
in the middle holding one up, and the farthest car at the highest speed
catching the slowest at the target); three roads of LeetCode's most
cars, 10^5, with a target of 10^6: all at one speed, each faster than
the one ahead, and at random places and speeds; and 600 random roads of
up to 30 miles and 12 cars, with the sum of their fleets and a checksum.
`car_fleet.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally, as a simulation: time runs in steps of 1/60 of an hour, so
that a car with a speed of 1 to 6 moves a whole number of sixtieths of a
mile each step; a car moves its speed but never past the car ahead of
it, so a faster car closes up and then moves with it; cars stop at the
target, and the cars reaching it at the same step arrive as one fleet.
Its 1,600 cases of 2 to 25 miles and 1 to 9 cars at distinct places come
in four kinds of 400: any speeds from 1 to 6, two speeds, 1 and 3, so
that many cars arrive together, faster further back, so that most cars
close up, and slower further back, so that few meet. Their fleets sum to
5,108.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the cars listed in reverse order give the same answer |
| P3 | the road and every position stretched by the same factor, 1 to 5, give the same answer |
| P4 | every car faster by the same factor, 1 to 5, gives the same answer |
| P5 | a car added a mile behind the rest, on a road a mile longer, adds no fleet or one |

It prints `1600 cases, fleets sum to 5108, 32000 checks over 4 arms: 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

P5 first added the car at a free place anywhere on the road, with the
answer allowed to grow by at most one, and all four arms failed it in 70
cases each: a slow car added in front of several fleets holds them all
up and makes them one, so the count can fall. Added behind every other
car, it can only lead a fleet of its own or join the last one.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a car arriving with the fleet ahead leading its own | P1 219 |
| M2 | ★: the cars taken from the back | P1 1175, P5 182 |
| M3 | ★: the fleet ahead's speed taken as 1 | P1 803, P4 665 |
| M4 | stack: a fleet arriving with the car not popped | P1 219 |
| M5 | stack: the cars taken from the target back | P1 1175, P5 182 |
| M6 | stack: at most one fleet popped for each car | P1 313 |
| M7 | slots: the slots walked away from the target | P1 1175, P5 182 |
| M8 | slots: a new leader's distance one short | P1 371, P3 172 |
| M9 | slots: a car of speed 1 taken for an empty slot | P1 781, P4 620 |
| M10 | fold: the cars folded from the far end | P1 1175, P5 182 |
| M11 | fold: a new fleet not becoming the one ahead | P1 685 |
| M12 | fold: the count starting at one | P1 1600 |

P1 kills all twelve. M2, M5, M7 and M10 are one mistake in four arms,
the cars taken in the wrong direction, and fail the same cases, as M1
and M4, which both split cars arriving together, fail as many. P2 kills
nothing, since every arm sorts the cars or places them by position
before it looks at them. P3 sees the one edit that depends on the road's
scale, M8, and P4 the two that depend on the speeds' scale, M3 and M9;
P5 sees only the wrong direction (M2, M5, M7, M10).

## Verification

Every arm prints the same output as `car_fleet.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its lines under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `b8bf6e5772`, and the runtime archives are
current with them. Under `karac __mir-run` the arms take 1.8 to 5.5 s
and the differential 4.3 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends run the ★, stack and slots arms through
`karac run --interp`, `karac run` and `karac build` with the same
output. A `KARAC_AUTO_PAR=1` build of those three differs in the last
two lines, the random road of 10^5 cars (23 fleets for 15) and the 600
random roads, which are the lines whose cars come from calls that share
`seed`; most likely the auto-parallel build runs those calls in another
order (not traced). The fold arm runs under `karac run --interp`, but
`karac run` and `karac build` stop at its `fold` on a method chain ("no
handler for method 'fold' on non-identifier receiver"), and so does
`karac build` of the differential, which `karac run --interp` runs to `0
failures` in 86 s. Legacy refuses the bench program as moving a road's
positions out of an index, which v2's borrowing parameters do not do.
Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
roads once, each of LeetCode's most cars, 10^5, at distinct random
places below a target of 10^6: road `g` draws its speeds from 1 to `1 +
(g % 8) * 142857`, from all cars at speed 1, each its own fleet, to
speeds up to 10^6. Each of 150 rounds asks the next road. Every
implementation prints `150 rounds of 64 roads: fleets sum to 1903056,
checksum 873726600`, the Kāra program under `karac __mir-run` included,
in 82 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 3.19 to 3.43 s |
| Rust (`rustc -O`) | 0.82 to 1.21 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.85 to 1.22 s |
| Go | 2.48 to 3.02 s |
| Python | 16.1 to 16.9 s |
| Kāra (`karac build --mir`) | 2.31 to 2.49 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

Nearly all the time is the sort of 10^5 cars a round. At the medians of
the interleaved runs v2 takes 2.39 s, against Rust's 0.96 (0.92 under
overflow checks), C's 3.38 and Go's 2.68: 2.60 times Rust's time under
overflow checks, 0.71 times C's and 0.89 times Go's. Under valgrind's
cachegrind Rust runs 7.48 billion instructions and 1.40 billion
branches, with 25 million mispredicted; v2 runs 11.81 billion, 2.19
billion and 111 million, and C 13.72 billion, 3.60 billion and 148
million. 522 million of v2's branches are indirect, close to C's 483
million, which are `qsort`'s calls to its comparator; most likely v2's
sort also compares the cars through a call it cannot inline, which
Rust's sort, made for `(i64, i64)`, does not (not traced). Built for
`x86-64-v3`, the target `karac build` uses, C takes 2.95 to 3.41 s and
Rust with overflow checks 0.79 to 0.94 s, against v2's 2.26 to 2.48 s in
the same five interleaved runs. Python takes 16.5 s, about 5 times C's
time. The comparison with C and Rust waits until after M4.
