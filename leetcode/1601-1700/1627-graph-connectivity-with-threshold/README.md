# 1627. Graph Connectivity With Threshold

We have `n` cities labeled from `1` to `n`. Two different cities with
labels `x` and `y` are directly connected by a bidirectional road if and
only if `x` and `y` share a common divisor **strictly greater** than some
`threshold`. More formally, cities with labels `x` and `y` have a road
between them if there exists an integer `z` such that all of the
following are true:

- `x % z == 0`,
- `y % z == 0`, and
- `z > threshold`.

Given the two integers, `n` and `threshold`, and an array of `queries`,
you must determine for each `queries[i] = [ai, bi]` if cities `ai` and
`bi` are connected directly or indirectly. (i.e. there is some path
between them).

Return *an array* `answer`*, where* `answer.length == queries.length`
*and* `answer[i]` *is* `true` *if for the* `ith` *query, there is a path
between* `ai` *and* `bi`*, or* `answer[i]` *is* `false` *if there is no
path.*

```
n = 6, threshold = 2, queries = [[1,4],[2,5],[3,6]]              ->  [false,false,true]
n = 6, threshold = 0, queries = [[4,5],[3,4],[3,2],[2,6],[1,3]]  ->  [true,true,true,true,true]
n = 5, threshold = 1, queries = [[4,5],[4,5],[3,2],[2,3],[3,4]]  ->  [false,false,false,false,false]
```

**Constraints:** `2 <= n <= 10^4`; `0 <= threshold <= n`;
`1 <= queries.length <= 10^5`; `queries[i].length == 2`;
`1 <= ai, bi <= cities`; `ai != bi`.

## Approaches

| file | mechanism |
|---|---|
| `cities.kara` ★ | two cities sharing a divisor z above the threshold are both multiples of z, and all of z's multiples share it, so each such z joins its multiples into one group: a union-find with path compression joins z to 2z, 3z, ... (`(2 * z..=n).step_by(z)`), and the queries are mapped to root checks in a closure that writes the parent list. O(n log n · α(n)) |
| `cities_flood.kara` | no union-find: each unlabelled city starts a group and a breadth-first flood over a `VecDeque`; a city reaches its divisors above the threshold, found by trial division, and each divisor, the first time it is reached, reaches all its multiples. O(n sqrt n) |
| `cities_dsu.kara` | a `struct Dsu` with `find` (path halving), `union` (by rank) and `connected` methods; each z joins each multiple to the one before it, a chain rather than a star, and only the z up to n / 2 are walked. O(n log n · α(n)) |
| `cities_solution.kara` | LeetCode's Rust template: a recursive `find` nested in the method, over `usize`. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples, one city
asked about itself, and a threshold of n, which joins nothing; then the
connected answers counted and a checksum for 2000 random problems of up
to 20 cities and 10 queries, 200 of up to 1000 cities and 100 queries,
and 5 of up to 10000 cities and 10000 queries, the threshold anywhere
from 0 to n / 2 (above that nothing is joined). The examples and the
random queries also ask a city about itself, which LeetCode's
`ai != bi` rules out; the answer is `true`. `cities.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: an edge between every two cities whose greatest common
divisor is above the threshold, and each query a flood from its first
city over those edges. It checks 3000 random problems of 1 to 8 queries,
every other one of 1 to 12 cities and the rest of 1 to 30, the threshold
anywhere from 0 to n. Every random choice is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | every query written the other way round gives the same answer |
| P3 | a pair connected under threshold + 1 is connected under threshold |
| P4 | a city is connected to itself, and under threshold 0 every pair is connected |
| P5 | a pair connected among n cities is connected among n + 1 |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 660675984, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. P4's threshold of 0 is what most of
them trip: it is the case where every z joins.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first z joined is threshold + 2 | P1 549, P4 2397, P6 549 |
| M2 | ★: the multiples stop before n | P1 370, P4 1600, P6 370 |
| M3 | ★: the multiple itself hung under z's root, not its root | P1 189, P6 189 |
| M4 | flood: a divisor equal to the threshold also floods | P1 514, P6 514 |
| M5 | flood: trial division stops below the square root | P1 232, P4 1618, P6 232 |
| M6 | flood: a divisor floods from its second multiple, not itself | P1 141, P3 49, P5 3, P6 141 |
| M7 | dsu: the z walked stop before n / 2 | P1 222, P4 327, P6 222 |
| M8 | dsu: two roots of equal rank are not joined | P1 624, P3 14, P4 2696, P5 42, P6 624 |
| M9 | template: z, not z's root, hung under the other root | P1 457, P4 2512, P5 220, P6 457 |
| M10 | template: a query compares parents, not roots | P1 333, P3 3, P4 1471, P5 69, P6 333 |

## Benchmarks

The bench draws 100 thresholds from 0 to 99 and 100000 queries over
10000 cities, all of them first, then answers every query under every
threshold by the ★ arm in all five languages: a build of the groups, then
100000 punches. Every implementation prints `100 problems of 10000
cities and 100000 queries: 3161356 connected, checksum 373034236`. The C
build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `60902ec48` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.092 s |
| Rust (`rustc -O`) | 0.122 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.123 s |
| Go | 0.141 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.160 s |
| Kāra (`karac build`) | 0.163 s |
| Python | 3.6 s |

Kāra is the slowest compiled lane here, a third behind Rust and 1.7
times C. The work is about two million root walks, each a chain of
dependent loads through the parent list; why Kāra's are slower was not
looked into.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.146 s and
0.154 s on one run).

## Verification

All four arms print the same output as `cities.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`60902ec48`.

## Writing it

The ★ and flood arms checked clean as first written: city numbers as
`i32` indexing a `Vec` directly, `(2 * z..=n).step_by(z)` with an `i32`
step, and a `map` closure that writes the parent list through
`find(mut parent, ..)`. The `Dsu` arm's `dsu.connected(q[0] as i64,
q[1] as i64)` drew two `lossless_cast` warnings, which `karac fix`
removed.

LeetCode's Rust template takes one `karac fix` of 19 edits: the nested
`fn find` moved above the `impl` (Kāra has no nested items), the
`&mut Vec<usize>` parameter to `mut ref Vec[usize]` and its calls to
`find(mut parent, ..)`, the `Vec<..>` types to `Vec[..]`,
`struct Solution {}`, and `Solution::` to `Solution.`. It then checks and
agrees with no hand edit. Moving the nested `fn` used to leave behind the
blank line that had followed it, so the method opened on a blank line;
kara `a15d8a822` takes that line too, and the arm is as that fix leaves
it.
