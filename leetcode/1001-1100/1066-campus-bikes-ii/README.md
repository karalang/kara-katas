# 1066. Campus Bikes II

On a campus grid there are `n` workers and `m` bikes, `n <= m`. Give
each worker a different bike so that the sum of the Manhattan distances
between each worker and their bike is as small as possible, and return
that sum. The Manhattan distance between `p1` and `p2` is `|p1.x - p2.x|
+ |p1.y - p2.y|`.

```
workers = [[0,0],[2,1]], bikes = [[1,2],[3,3]]              ->  6
workers = [[0,0],[1,1],[2,0]], bikes = [[1,0],[2,2],[2,1]]  ->  4
workers = [[0,0],[1,0],[2,0],[3,0],[4,0]],
bikes = [[0,999],[1,999],[2,999],[3,999],[4,999]]           ->  4995
```

**Constraints:** `1 <= n <= m <= 10`; `0 <= x, y < 1000`; every worker
and bike stands at a different point.

The workers take bikes in order, so a set of bikes taken says how many
workers are done and which one is next: its size. At most 2^10 sets, each
reached by adding one bike, make a table small enough to fill whole.

The arms take the points as `Slice[(i64, i64)]` and return the sum as an
`i64`.

## Approaches

| file | mechanism |
|---|---|
| `campus_bikes.kara` ★ | a table over the sets of bikes taken (`Vec.filled(1 << m, i64.MAX)`), filled in increasing order of the set: the next worker, `mask.count_ones()`, tries every free bike. The answer is the least total over the sets of size `n`. O(2^m * m) |
| `campus_bikes_memo.kara` | top down: the least total for the workers still to come, given the bikes taken, remembered by that set (`memo: mut ref Vec[i64]`, -1 for not known). O(2^m * m) |
| `campus_bikes_bound.kara` | branch and bound (`struct Search` with `fn go(mut ref self, ..)`): each worker tries the free bikes nearest first, and a branch is cut once its total reaches the best complete one. Exponential in the worst case |
| `campus_bikes_dijkstra.kara` | Dijkstra over the sets taken (`PriorityQueue[(i64, i64)]` of total and set, smallest first): the first set of size `n` taken off the queue holds the answer |
| `campus_bikes_hungarian.kara` | the Hungarian algorithm: each worker added by a shortest augmenting path over reduced costs, with potentials on the workers and the bikes. O(n^2 * m), no exponent |
| `campus_bikes_solution.kara` | LeetCode's Rust template (`struct Solution;`, `Vec<Vec<i32>>`, `vec![i32::MAX; 1 << m]`, `0..(1usize << m)`, `count_ones() as usize`, `Solution::`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: the answers for LeetCode's three
examples and four more; the sum and a checksum of the answers for 2000
problems of 1 to 4 workers and up to 6 bikes on a 10 by 10 grid, and 100
of 1 to 8 workers and up to 10 bikes on 1000 by 1000; and the answers
for 10 workers and 10 bikes at random (3252), on a line with each bike 5
past its worker (50), and shifted so that each bike is nearest the
wrong worker (655). `campus_bikes.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to give each worker a different bike, tried one by
one, and the least total. It checks 2000 problems: 1000 of 1 to 4
workers and up to 6 bikes on a 10 by 10 grid, and 1000 of 1 to 5 workers
and up to 7 bikes on 30 by 30. Every random choice of a problem is drawn
before any arm answers, so a wrong arm cannot change the problems the
others see.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer lies between the sum of each worker's nearest bike and the total of the workers taking the nearest free bike in turn |
| P3 | every point turned (x and y swapped) and moved leaves the answer, and so do the workers and the bikes both in reverse order |
| P4 | every coordinate doubled doubles the answer |
| P5 | a bike added never raises the answer, and a worker and a bike added far from the rest, some distance apart, raise it by that distance |
| P6 | each arm agrees with at least three of the other five |

The differential prints `2000 problems: checksum 261754846, 96000 checks
over 6 arms: 0 failures` under every lane in Verification; a Python
reading of the same 2000 problems gives the same checksum. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Fifteen are kept, two or three to
each arm. All thirty are killed, each fails the same way under both
backends, none by a crash, and no two kept ones fail the same checks.
Three first edits crashed and were replaced: the ★ arm never taking the
last bike, the memo arm offering a worker only the bikes from its own
index on, and the bound arm trying only the two nearest bikes. Each
leaves some problem with no way to give every worker a bike, so the arm
answers `i64.MAX` and the sum after it, or P4's doubling, overflows.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last full set taken, not the least | P1 1274, P2 1195, P3 1457, P5 1561, P6 1274 |
| M2 | ★: each worker charged its own index's bike | P1 1673, P2 1600, P3 1484, P5 2000, P6 1673 |
| M3 | ★: the answer read one worker short | P1 2000, P2 1818, P3 1396, P6 2000 |
| M4 | memo: a remembered total read one high | P1 711, P2 383, P3 664, P4 706, P5 1548, P6 711 |
| M5 | memo: the memo starts known at 0 | P1 2000, P2 2000, P5 1890, P6 2000 |
| M6 | memo: remembered under the set without its lowest bike | P1 1016, P2 711, P3 939, P5 1445, P6 1016 |
| M7 | bound: a bike never given back | P1 491, P3 775, P6 491 |
| M8 | bound: a branch cut one short of the best | P1 36, P3 59, P4 36, P5 3, P6 36 |
| M9 | Dijkstra: each set queued at its last distance only | P1 1548, P2 1528, P3 1389, P5 1908, P6 1548 |
| M10 | Dijkstra: the largest total taken off first | P1 1895, P2 1884, P3 735, P5 3585, P6 1895 |
| M11 | Dijkstra: a taken bike given back | P1 6, P3 11, P6 6 |
| M12 | Hungarian: the whole path given to the new worker | P1 509, P2 251, P3 793, P5 35, P6 509 |
| M13 | Hungarian: a bike's potential raised | P1 158, P2 98, P3 228, P5 8, P6 158 |
| M14 | solution: a bike's y read as its x | P1 1838, P2 1541, P3 1934, P6 1838 |
| M15 | solution: the set of every bike never visited | P1 451, P2 451, P4 451, P5 426, P6 451 |

P1 and P6 kill all fifteen, P3 thirteen, P2 twelve, P5 eleven and P4
three. P3 reverses the workers and the bikes, which changes which worker
goes first and which bike is tried first, and a wrong total is rarely
wrong the same way in the other order, so it sees all but two edits: the
memo known at 0 from the start, which answers 0 in any order (M5), and
the solution's full set never visited (M15). P2's bounds miss the edits that land between them:
the bound arm's bike never given back (M7) answers the first descent,
which is the greedy total, and M8 and M11 stay within it. P4 sees only an
edit that is not linear in the distances: a total read one high (M4), a
cut one short (M8), which doubled distances, all even, never meet, and
the solution answering `i32::MAX` when every bike is needed (M15). Every
other edit computes a wrong total from the distances alone, which doubles
with them.

Of the fifteen not kept, the ★ arm's sets overwritten fails as the
solution's, the same edit. The bound arm never charging the last worker,
Dijkstra's answer one worker early and the solution's read one worker
short fail as M3, and the bound arm giving each worker its nearest free
bike and the Hungarian worker's potential lowered fail as M7 (inferred
from the counts: each answers the greedy total). The ★ arm's distances
halved, the memo arm counting each complete assignment one more and
remembering by how many bikes are taken, the bound arm marking a bike by
its rank, Dijkstra begun with bike 0 taken, the Hungarian slack never
reduced and the last bike's worker not counted, and the solution's
workers swapped crossing to `i32` each fail in a way of their own.

## Verification

Every arm prints the same output as `campus_bikes.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file. Under `karac __mir-run` the arms take 0.4 s (Hungarian) to 1.6 s (bound)
and the differential 19.2 s.

Every file went through `karac fix`, which applies the style lints that
`karac check` leaves at allow. In the differential it moved the two
closures' return types, which a closure cannot write, onto their
bindings (`let moved: Fn(Slice[(i64, i64)]) -> Vec[(i64, i64)] = |ps|
..`). The Rust arm reaches a clean check in two rounds: the syntax
(`struct Solution {}`, `Vec[Vec[i32]]`, `i32.MAX`, `Solution.`), then
`vec![v; n]` to `Vec.filled(1 << m, i32.MAX)`, the `1usize` suffix and
the `as usize` on `count_ones()`, the inner `vec![..]` to a list literal
and the bridge's `as i64` the widening return no longer needs. Nothing
was left by hand, and the kata met no compiler gap.

## Benchmarks

The bench builds 5000 problems of 8 to 10 workers and 10 bikes on a 1000
by 1000 grid once, in all five languages, then answers each with the ★
arm's table over the 1024 sets of bikes taken: about 5 million sets
filled, each trying up to 10 bikes. Rust counts the set with
`count_ones()`, C with `__builtin_popcountll`, Go with `bits.OnesCount`
and Python with `bin(mask).count("1")`. Every implementation prints
`5000 calls: answers sum 13536821, checksum 738474277`.

Timings on a 4-core container, twelve interleaved runs of each compiled
program and one of Python, with kara `47832f8867` on LLVM 22:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 0.165 to 0.192 s | 0.173 s |
| C (`clang -O3`) | 0.179 to 0.223 s | 0.186 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.217 to 0.236 s | 0.227 s |
| Kāra (`karac build`) | 0.223 to 0.259 s | 0.235 s |
| Go | 0.253 to 0.279 s | 0.264 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.372 to 0.448 s | 0.383 s |
| Python | 8.3 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.231 s) is below its real time.

Kāra takes 0.59x the time of Rust under overflow checks and 1.31x the
time of plain Rust. The difference is `abs()`. Rust under overflow checks
must panic on `i64::MIN`, and it compiles each `abs()` in the distance
to a branch on the difference's sign (`sub; jo; jns`), which random
points take half the time, so it mispredicts. Kāra negates with an
overflow branch that is never taken and picks the sign with `cmovns`,
with no branch on the data. Under callgrind the two run nearly the same
number of instructions (1.30 and 1.28 billion), so the gap is
mispredictions, not work (inferred, not measured with counters). Plain
Rust runs 1.11 billion: Kāra's extra are the overflow checks on the
subtractions, the negations and the sums, and a check of the worker's
index against the length that stays in the inner loop. Kāra counts the
set with `popcnt`, and Rust, built for baseline x86-64, with a sequence
of shifts and masks once per set, which is outside the inner loop.
