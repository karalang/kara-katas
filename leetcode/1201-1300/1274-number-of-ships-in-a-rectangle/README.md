# 1274. Number of Ships in a Rectangle

*(This problem is an interactive problem.)*

Each ship is located at an integer point on the sea represented by a
cartesian plane, and each integer point may contain at most 1 ship.

You have a function `Sea.hasShips(topRight, bottomLeft)` which takes two
points as arguments and returns `true` if there is at least one ship in
the rectangle represented by the two points, including on the boundary.

Given two points: the top right and bottom left corners of a rectangle,
return the number of ships present in that rectangle. It is guaranteed
that there are at most 10 ships in that rectangle.

Submissions making more than 400 calls to `hasShips` will be judged
Wrong Answer. Also, any solutions that attempt to circumvent the judge
will result in disqualification.

```
ships = [[1,1],[2,2],[3,3],[5,5]], topRight = [4,4], bottomLeft = [0,0]  ->  3
ships = [[1,1],[2,2],[3,3]], topRight = [1000,1000], bottomLeft = [0,0]  ->  3
```

**Constraints:** on the input, `ships` is only given to initialize the
map internally, and must be solved "blindfolded"; `0 <= bottomLeft[0] <=
topRight[0] <= 1000`; `0 <= bottomLeft[1] <= topRight[1] <= 1000`;
`topRight != bottomLeft`.

The judge is a `trait Sea { fn has_ships(self, top_right: Vec[i64],
bottom_left: Vec[i64]) -> bool; }`, and the harness's `Ocean` implements
it over a list of ships, counting the questions in a `shared struct` so
that the count survives the sea being passed by borrow. The arms are `fn
count_ships(sea: dyn Sea, top_right: Vec[i64], bottom_left: Vec[i64]) ->
i64`, or generic over `S: Sea` in one arm, and `run` reports the count
and whether it took at most 400 questions.

## Approaches

| file | mechanism |
|---|---|
| `count_ships.kara` ★ | by quarters: a rectangle with no ship counts none, a point with one counts one, and any other is cut at its middle both ways and its four quarters counted by recursion through the `dyn Sea`. O(ships × log 1000) questions |
| `count_ships_halves.kara` | by halves, generic over `S: Sea`: a rectangle cut across its longer side, the first half asked about, and the second asked only when the first holds no ship, since the whole is known to hold one |
| `count_ships_stack.kara` | by a work list: the rectangles still to look at kept as tuples in a `Vec`, each popped and asked about, and its quarters pushed when it holds a ship and is more than a point. No recursion |
| `count_ships_rect.kara` | by a `Rect` type: the rectangle a struct with methods saying whether it is empty or a point and handing out its quarters, and the count a `map` and `sum` over them |
| `count_ships_solution.kara` | a Rust solution as LeetCode's Rust users write it (`sea: &dyn Sea`, corners cloned into each call, `vec![..]` quarters, `Self::count_ships`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples (`(3, true)
(3, true)`); 1000 random rectangles in the sea with up to 10 ships in each
and 10 more outside (`1000 random rectangles: 5039 ships, 1000 within 400
questions, checksum 470434059`); and the constraints' top, the whole sea
with ten ships spread over it, ten in a corner and ten on one line (`(10,
true) (10, true) (10, true)`). `count_ships.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the four arms written in Kāra checked clean as first
written; the harness's `run` hands its ships to the `Ocean` it builds, and
`karac fix` gave that parameter its `own`. LeetCode's Rust signature takes
`i32` corners, and against the harness's `i64` trait that is E0200 at each
call, so the solution arm is written with `i64` corners. It then takes one
round of 28 fixes by `karac fix`'s count: `&dyn Sea` to `dyn Sea`,
`Vec<i64>` to brackets, `vec![..]` to `[..]`, `||` and `!` to `or` and
`not`, `Self::count_ships` to `Solution.count_ships`, `struct Solution;`
to `struct Solution {}`, and the `.clone()` on corners passed to its own
recursive calls dropped as redundant. The two clones passed to
`sea.has_ships` stay: the redundant-clone lint is not reported for an
argument to a method called through `dyn` or a generic bound
(B-2026-11-20-87, open).

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the ships whose point lies in the rectangle, its boundary
included, counted one by one. 2000 random seas, a third of the
rectangles at most 12 wide and high so that ships crowd them and sit on
their edges, each with up to 10 ships inside and up to 10 outside.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | at most 400 questions |
| P3 | 30 more ships outside the rectangle, the same count |
| P4 | the sea mirrored left to right, the same count |
| P5 | the rectangle cut in two at a random column, the halves' counts add up |
| P6 | the ★ arm's count |

All 60,000 checks pass on every arm: `2000 seas: checksum 987931247,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the same
checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the upper left quarter never counted | P1 1693, P4 838, P5 617, P6 6772 |
| S2 | ★: the upper right quarter starts a row late | P1 1142, P4 1056, P5 890, P6 4568 |
| H1 | halves: the second half assumed to hold a ship when the first holds one, not none | P1 1603, P2 1, P4 705, P5 679, P6 1603 |
| H2 | halves: the second half of a cut across the columns starts a row late | P1 742, P4 617, P5 522, P6 742 |
| K1 | stack: the upper right quarter never pushed | P1 1564, P4 1103, P5 854, P6 1564 |
| K2 | stack: a rectangle one row high taken as empty | P1 1819, P6 1819 |
| R1 | rect: a rectangle one wide or one high taken as a point | P1 340, P4 92, P5 212, P6 340 |
| R2 | rect: the upper left quarter dropped | P1 1693, P4 838, P5 617, P6 1693 |
| O1 | solution: a rectangle one wide taken as a point | P1 187, P4 41, P5 132, P6 187 |
| O2 | solution: the upper right quarter overlapping the lower right by a row | P1 1351, P2 40, P4 1217, P5 1138, P6 1351 |

All ten are caught, every one by P1, the statement read literally. P3,
more ships outside, catches none: every edit still asks only about the
rectangle, so ships beyond it never change an answer. P4, the sea
mirrored, and P5, the rectangle cut at a column, see the edits that lose
or double a part of the rectangle, and miss K2, whose one-row
rectangles stay one row high under both. P2, the 400 questions, sees
the two that ask about the same ships more than once (H1 and O2, which
counts a row twice). The first versions of S1 and O2 made a quarter as
large as its rectangle and recursed until the stack ran out; they were
replaced by these.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (divide and conquer by quarters through the sea's interface) on 500
random seas of 10 ships in the whole 1001-by-1001 square and 10 more in
a corner, drawn once, 30 rounds; every count, and the number of
questions asked, folded into a checksum. Every program prints `30 rounds
of 500 seas: checksum 640521592`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.472 to 0.527 s | 0.475 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.469 to 0.509 s | 0.478 s |
| Rust (`rustc -O`) | 0.781 to 0.856 s | 0.798 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.761 to 0.841 s | 0.772 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.754 to 0.842 s | 0.764 s |
| C (`clang -O3`) | 0.392 to 0.414 s | 0.396 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.420 to 0.448 s | 0.425 s |
| Go | 0.560 to 0.614 s | 0.573 s |
| Python | 12.37 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on takes about 1.6x Kāra's time. C is
about 17% ahead of Kāra (0.396 s against 0.478 s); Kāra is about 17%
ahead of Go (0.478 s against 0.573 s). Python takes about 26x Kāra's
time. No profile was taken.
