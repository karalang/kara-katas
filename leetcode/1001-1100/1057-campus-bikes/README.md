# 1057. Campus Bikes

On a campus represented as a 2D grid, there are `n` workers and `m` bikes,
with `n <= m`. Each worker and bike is a 2D coordinate on this grid.

Assign a bike to each worker. Among the available bikes and workers, choose
the `(worker_i, bike_j)` pair with the shortest **Manhattan distance**
between each other and assign the bike to that worker. If there are
multiple `(worker_i, bike_j)` pairs with the same shortest distance, choose
the pair with the smallest worker index; if there are still several, the
one with the smallest bike index. Repeat until there are no available
workers.

Return an array `answer` of length `n`, where `answer[i]` is the index
(0-indexed) of the bike that the `i`-th worker is assigned to.

The Manhattan distance between two points `p1` and `p2` is
`|p1.x - p2.x| + |p1.y - p2.y|`.

```
workers = [[0,0],[2,1]], bikes = [[1,2],[3,3]]              ->  [1,0]
workers = [[0,0],[1,1],[2,0]], bikes = [[1,0],[2,2],[2,1]]  ->  [0,2,1]
```

**Constraints:** `1 <= n <= m <= 1000`; `0 <= x, y < 1000`; all worker
places are distinct, and so are all bike places.

The arms do not rely on the places being distinct, and the harness puts
several workers, or several bikes, at one place.

## Approaches

The statement's order of choice is the order of the tuples `(distance,
worker, bike)`. The pair it chooses at each step comes first among the
pairs still free, and every pair before it has lost its worker or its bike
already. So walking every pair in that order, and taking each one whose
worker and bike are both still free, makes the statement's choices.

| file | mechanism |
|---|---|
| `campus_bikes.kara` ★ | each pair pushed into the bucket of its distance, at most 1998 on this campus; the workers and bikes walked in order, so each bucket is already in the order of worker and bike. O(n m + D) for distances up to D |
| `campus_bikes_sort.kara` | every pair as `(distance, worker, bike)`, sorted. O(n m log(n m)) |
| `campus_bikes_heap.kara` | each worker's bikes sorted, and a `PriorityQueue` of each free worker's nearest bike not yet ruled out; a worker refused moves on to its next bike. O(n m log m) |
| `campus_bikes_iter.kara` | the pairs by `flat_map` over a `map`, `sort_by_key`, and `for_each` to assign. O(n m log(n m)) |
| `campus_bikes_map.kara` | a `SortedMap` from each distance to its pairs, read in key order. O(n m log D) |
| `differential.kara` | the five arms against the statement read literally, seven properties |

Every arm prints the same 12 lines: the answers for LeetCode's two examples
and six more; the total distance ridden and a checksum of every answer for
3000 random campuses of 1 to 8 workers on 6 by 6, and for 20 of 1 to 200 on
1000 by 1000; and two answers at the limit, 1000 workers and 1000 bikes,
and 200 workers at one place with 1000 bikes. `campus_bikes.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: until every worker has a bike, every free worker and free bike
are tried, and the pair that comes first in the statement's order is
assigned. It checks 3000 random campuses: 2000 of 1 to 6 workers on 4 by 4,
where distances tie often, and 1000 of 1 to 20 on 30 by 30 or 1000 by
1000, each with up to three more bikes than workers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every worker gets a bike, and no two the same one |
| P3 | no worker and bike would both rather have each other: a worker whose pair with a bike comes before its own finds that bike ridden by a worker whose pair with it comes earlier still |
| P4 | the campus turned a quarter round, or moved, leaves the answer |
| P5 | a bike nobody rides taken away leaves everyone's bike |
| P6 | the worker whose pair is chosen last, taken away with its bike, leaves everyone else's bike |
| P7 | each arm agrees with at least two of the other four |

P3 holds because when a worker's pair with a better bike came up, the
worker was still free, so the bike was not: a worker whose pair comes
earlier had it. It is also enough. Every worker and every bike ranks the
other side by the same order of pairs, so only one assignment has no such
worker and bike, and P3 alone pins the answer. P5 and P6 hold because the
pairs taken away were never the first free pair at any step before the
last, so every earlier choice is made again. P4 holds because turning and
moving keep every distance.

The differential prints `3000 campuses: checksum 798498666, 114145 checks
over 5 arms: 0 failures` under `karac __mir-run` (53 s), `karac
__mir-llvm-run` and `karac __mir-llvm-asan` with no error, and the same
line under `karac run` and from a `karac build` binary. On a failure it
prints the first ten and then the count by property. P2 failing skips the
other checks of that arm on that campus.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Fifteen are kept, three to each arm.
Twenty-eight are killed and two are equivalent, each fails the same way
under both backends, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the distance the larger of the two | P1 1658, P3 1658, P7 1658 |
| M2 | ★: the farthest pairs first | P1 2836, P3 2836, P7 2836 |
| M3 | ★: a worker with bike 0 taken as free | P1 1545, P2 1545, P5 23, P6 84 |
| M4 | sort: sorted farthest first | P1 2841, P3 2841, P7 2841 |
| M5 | sort: a pair taken when either is free | P1 2435, P2 2435 |
| M6 | sort: the bike's x for its y | P1 2461, P3 2461, P4 4710, P7 2461 |
| M7 | heap: each worker's bikes in index order | P1 2477, P3 2477, P6 96, P7 2477 |
| M8 | heap: each worker's first offer farther by its index | P1 990, P3 990, P6 47, P7 990 |
| M9 | heap: a worker's later offers one nearer | P1 177, P3 177, P7 177 |
| M10 | iter: sorted by worker first | P1 1487, P3 1487, P7 1487 |
| M11 | iter: the worker's index for the bike's in the taken check | P1 2415, P2 2415, P5 32, P6 2 |
| M12 | iter: bike 0 never marked taken | P1 1334, P2 1334, P5 29, P6 68 |
| M13 | map: distances taken modulo 50 | P1 602, P3 602, P7 602 |
| M14 | map: the sum's size, not the sizes' sum | P1 2356, P3 2356, P4 2637, P7 2356 |
| M15 | map: a worker with bike 0 taken as free | P1 2160, P2 470, P3 1690, P5 426, P6 23, P7 1690 |

P1 kills all fifteen, P3 and P7 eleven, P6 six, P2 five, P5 four and P4
two. P3 and P7 kill exactly the edits whose answer stays an assignment;
P2 kills the rest, which give a bike twice or leave a worker without one,
and stop the arm's other checks. P4 sees only the two edits that measure a
distance in a way turning or moving changes (M6, M14). P5 and P6 see the
edits that let a worker or a bike be taken again, and the heap edits that
change which pair is chosen last. M3 and M15 make the same edit, a worker on bike 0
taking a second bike, but the ★ arm counts the workers left, so the second
bike ends its walk early and leaves a worker without one; the map arm
walks every pair and usually still gives an assignment.

The other fifteen fail as others do or not at all. One fails exactly as a
kept one: the map arm taking the farthest distance first, as M2. Nine fail
in groups with no kept member: a bike given twice (★, heap) and a bike
never marked taken (heap); the count of workers left falling by two (★)
and the sort stopping one worker short; each bucket in reverse order (★,
map); and the first bike never offered (sort, iter). Three fail in ways of
their own: the heap popping the largest first, each pair's bike the
worker's index (iter), and each bike counted farther by its index (map).

Two are equivalent: the sort arm sorting by distance alone, stably, and
the iter arm breaking ties by bike before worker. Both change only the
order of pairs at one distance, and in both orders a worker meets its
bikes in index order and a bike meets its workers in index order. That is
all P3 asks, and P3 pins the answer. A Python check of the two orders on
200000 random sets of pairs found no difference.

## Verification

Every arm prints the same output as `campus_bikes.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
file. The runs used a release build of kara `a3df76e55c`. Under `karac
__mir-run` the arms take 5.9 s (sort) to 17.4 s (iter).

The ★ arm was written in Kāra and checked clean. The other four were
written the way Rust writes them. The sort, iter and map arms reach a clean
check through `karac fix` alone (`Vec<..>` to `Vec[..]`, `&T` to `ref T`,
`::` to `.`, `!` to `not`, `&&` to `and`, `&` patterns dropped, `move`
dropped, and `use std::collections::BTreeMap` deleted with `BTreeMap`
renamed `SortedMap`). The heap arm met three gaps, two fixed in kara
`52c81c1375` and `7b8a0de80f`, and one filed and since fixed:

- `Vec<(i64, usize)>`, which `karac fix` spelled `Vec[(i64, usize)]`, drew
  `i64`/`usize` coercion errors with no fix (kara B-2026-11-06-3, from kata
  1055). A `usize` written in a type that meets `i64` now gets a fix to
  `i64`, since Kāra keeps `usize` for FFI (design.md §5); one that meets
  nothing, like the arm's `Vec.filled(n, 0usize)`, draws nothing.
- `heap.push(Reverse((d, i, j)))` drew "undefined name 'Reverse'" with a
  did-you-mean `Release`, and `use std::cmp::Reverse;` was deleted with a
  message that claimed a prelude `Reverse`. Rust's `Reverse` makes a
  `BinaryHeap` pop the smallest first, which Kāra's `PriorityQueue` does
  already. The fix now writes `heap.push((d, i, j))` and `Some((_, i, j))`,
  and the heap's constructor becomes `PriorityQueue.new()` rather than the
  largest-first `PriorityQueue.max_first()`. A `Reverse` anywhere else, a
  sort key say, gets no fix and a message naming `sort_by(|a, b| b.cmp(a))`.
- `let mut heap = PriorityQueue.new();`, fixed by the `push` after it, was
  refused with "cannot infer type parameter 'T'". `Vec.new()` and the other
  built-in collections were inferred from a later use, but a declared
  generic constructor or function whose parameter only its return type
  names was not. Filed as kara B-2026-11-06-7, and fixed by Thread C in kara
  `2783b8c546`; until then the arm wrote `PriorityQueue[(i64, i64, i64)]` by
  hand. The heap arm and the differential's copy of it now write the bare
  `PriorityQueue.new()`, and both print the same output on every lane under
  kara `931da0cb10`.

## Benchmarks

The bench builds 20 campuses of 300 workers and 400 bikes on 1000 by 1000
once in all five languages, then runs the ★ arm on each 8 times. Every
implementation prints `20 campuses of 300 workers and 400 bikes, 8 rounds:
2315952 ridden, checksum 829372281`. The work is 19.2 million pairs pushed
into 2000 growable buckets, which are allocated and freed on every call,
and then walked in order.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `a3df76e55c` on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.207 to 0.249 s | 0.214 s |
| Kāra (`karac build`) | 0.210 to 0.258 s | 0.215 s |
| C (`clang -O3`) | 0.357 to 0.403 s | 0.375 s |
| Rust (`rustc -O`) | 0.376 to 0.428 s | 0.387 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.488 to 0.512 s | 0.506 s |
| Go | 0.704 to 0.772 s | 0.745 s |
| Python | 5.92 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.209 s) is below its real time.

Kāra's lead is the allocator, not the loop. C and both Rust builds spend
0.12 to 0.16 s of each run in the kernel, with about 100000 minor page
faults: glibc gives the freed buckets back to the system at the end of each
call and faults them in again on the next. Kāra's runtime raises glibc's
trim and mmap thresholds before `main` (`runtime/src/lib.rs`,
`malloc_tuning`), so the memory is kept, and the run takes about 1000
faults. With the same thresholds set through `MALLOC_TRIM_THRESHOLD_` and
`MALLOC_MMAP_THRESHOLD_`, C takes 0.210 s, Rust 0.227 s and Rust under
overflow checks 0.330 s, against Kāra's 0.214 s; with
`KARAC_MALLOC_TUNE=0`, Kāra takes 0.354 s (medians of five runs).
