# 1462. Course Schedule IV

There are a total of `numCourses` courses you have to take, labeled from
`0` to `numCourses - 1`. You are given an array `prerequisites` where
`prerequisites[i] = [ai, bi]` indicates that you must take course `ai`
first if you want to take course `bi`. Prerequisites can also be
indirect: if course `a` is a prerequisite of course `b`, and course `b`
is a prerequisite of course `c`, then course `a` is a prerequisite of
course `c`. You are also given an array `queries` where `queries[j] =
[uj, vj]`. For the `jth` query, you should answer whether course `uj` is
a prerequisite of course `vj` or not. Return a boolean array `answer`,
where `answer[j]` is the answer to the `jth` query.

```
numCourses = 2, prerequisites = [[1,0]], queries = [[0,1],[1,0]]              ->  [false,true]
numCourses = 2, prerequisites = [], queries = [[1,0],[0,1]]                   ->  [false,false]
numCourses = 3, prerequisites = [[1,2],[1,0],[2,0]], queries = [[1,0],[1,2]]  ->  [true,true]
```

**Constraints:** `2 <= numCourses <= 100`, `0 <= prerequisites.length <=
(numCourses * (numCourses - 1) / 2)`, `prerequisites[i].length == 2`, `0
<= ai, bi <= numCourses - 1`, `ai != bi`, all the pairs `[ai, bi]` are
unique, the prerequisites graph has no cycles, `1 <= queries.length <=
10^4`, `0 <= ui, vi <= numCourses - 1`, and `ui != vi`.

The arms are `fn check_if_prerequisite(num_courses: i32, prerequisites:
Vec[Vec[i32]], queries: Vec[Vec[i32]]) -> Vec[bool]`.

## Approaches

| file | mechanism |
|---|---|
| `check_if_prerequisite.kara` ★ | the closure by Floyd-Warshall over a `Vec.filled(n, Vec.filled(n, false))`, each course in turn a step between, the inner loop skipped when a course is not before the step, each table read through the `i32` course numbers themselves; the answers by `queries.iter().map(..).collect()`. O(n^3 + q) |
| `check_if_prerequisite_bfs.kara` | a breadth-first walk from every course over `Vec[Vec[i64]]` adjacency through a `VecDeque`, `while let` taking each course off, and each walk's `Vec[bool]` kept as that course's row. O(n(n + e) + q) |
| `check_if_prerequisite_topo.kara` | the courses taken in an order the prerequisites allow (Kahn's), a `Vec` of ready courses popped by `while let`, each course handing everything before it, itself too, to the courses that need it through `Set.union`; a query is `contains` on the later course's set. O(n^2 log n + q log n) |
| `check_if_prerequisite_memo.kara` | what each course leads to, worked out by a depth-first search the first time a query needs it and kept in a `Vec[Option[Vec[bool]]]` passed by `mut ref`, read back through `if let Some(row) = ref known[u]`. O(n(n + e) + q) |
| `check_if_prerequisite_solution.kara` | a Rust solution as LeetCode's Rust users write it (the closure by Floyd-Warshall over `vec![vec![false; n]; n]` with `usize` indices cast from each pair, `reach[i][j] = reach[i][j] \|\| (reach[i][k] && reach[k][j])`, and the answers mapped from the queries and collected), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples
(`[false,true] [false,false] [true,true]`); a chain of 100 courses asked
both ways along it, and 100 courses with no prerequisites (`chain: 99 of
198, checksum 645250627; none: 0 of 198, checksum 896462126`); the
constraints' most, 100 courses with each pair a prerequisite one time in
20 and 10^4 queries (`100 courses, 269 prerequisites, 10^4 queries: 1741
true, checksum 729912752`); and 1000 random cases of 2 to 30 courses,
each pair a prerequisite one time in 1 to 10, and 1 to 50 queries (`1000
random cases: 5173 true, checksum 279826554`).
`check_if_prerequisite.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★ arm checks clean as first written. The bfs and topo
arms pushed `p[1] as i64` onto a `Vec[i64]`, a cast `karac check` warns
is unnecessary since `i32` widens to `i64` here, and `karac fix` drops
it, 1 fix each. The memo arm was first written with Rust's borrows:
`&prerequisites` and `&queries` in its loops, `&next` and `&mut known`
as arguments, `&Vec[..]` and `&mut Vec[..]` parameters, `if let
Some(row) = &known[u]`, `for &v in &next[u]` and `(w, &yes)` patterns,
`vec![..; n]`, and `usize` indices with their casts; `karac fix` carries
it to Kāra in one round of 24 fixes by its count, the loops to `for p in
ref prerequisites`, the arguments to `next` and `mut known`, the
parameters to `ref` and `mut ref`, the patterns bare, `vec!` to
`Vec.filled`, and `usize` to `i64`. The Rust solution takes one round of
18 fixes: `struct Solution;` to `struct Solution {}`, `Vec<..>` to
`Vec[..]`, `as usize` to `as i64` and each index's cast dropped,
`vec![vec![false; n]; n]` to `Vec.filled(n, Vec.filled(n, false))`, and
`||` and `&&` to `or` and `and`. Every arm's output matches on the first
run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a prerequisite of a prerequisite is a prerequisite, added to
the direct ones in a `Set[(i32, i32)]` until no pair is new, while there
are at most 12 courses. LeetCode's examples, one more of two courses,
the chain and the 100 courses with none above, every pair of 30 courses
a prerequisite, the constraints' most, and 1995 random cases, half of 2
to 12 courses and half of 2 to 30.

| | property |
|---|---|
| P1 | the statement read literally, while there are at most 12 courses |
| P2 | every prerequisite and every query turned round gives the same answers |
| P3 | the courses renamed, c to (c + 1) % n, give the same answers |
| P4 | the prerequisites in another order give the same answers |
| P5 | no query is true both ways, and the true ones added as prerequisites change nothing |
| P6 | the ★ arm's answer |

All 56,740 checks pass on every arm: `2003 cases: checksum 819823695,
56740 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by a depth-first
search from each query's first course, gives the same checksum.

LeetCode's example lists are bound first under a `Vec[Vec[i32]]`
annotation, `let three: Vec[Vec[i32]] = [[1, 2].to_vec(),
..].to_vec();`, and then pushed. Pushed as written, `cases.push((3, [[1,
2].to_vec(), ..].to_vec(), ..))` into a `Vec[(i32, Vec[Vec[i32]],
Vec[Vec[i32]])]` is refused as `Vec[Vec[i64]]`, with no fix: the numbers
in a `.to_vec()` list keep the default `i64` there, as in
[B-2026-11-26-6](https://github.com/karalang/kara/blob/main/docs/bugs-v2.jsonl).
The annotation is the error's own advice.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: each prerequisite recorded the wrong way round | P1 1011, P5 1317, P6 6580 |
| M2 | ★: no step through another course ever added | P1 344, P6 3112 |
| M3 | bfs: only each course's direct prerequisites followed | P1 344, P6 778 |
| M4 | bfs: each query asked the wrong way round | P1 1011, P5 1317, P6 1645 |
| M5 | topo: a course never handed to those it is a prerequisite of, only its own prerequisites | P1 938, P6 1533 |
| M6 | topo: each query asked the wrong way round | P1 1011, P5 1517, P6 1645 |
| M7 | memo: a course's direct successors left out of what it leads to | P1 938, P6 1533 |
| M8 | memo: nothing a successor leads to added, only the successor itself | P1 344, P6 778 |
| M9 | solution: a step through k added when either half holds | P1 1106, P5 1780, P6 1772 |
| M10 | solution: each prerequisite recorded as a course before itself | P1 938, P6 1533 |

## Benchmarks

The bench draws 400 cases of 100 courses, the constraints' most, each
pair of courses a prerequisite one time in 20, and 10^4 queries each,
once, then answers each with the ★ arm and folds every answer into the
checksum. Each implementation keeps the closure as a table of `bool`s: a
`Vec` of `Vec`s in Kāra, Rust and Go, a static `char` array in C, and a
list of lists in Python. Every implementation prints `400 cases of 100
courses and 10^4 queries: checksum 889677287`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.50 s against Rust's 0.35 s (0.33 s with overflow checks
on), C's 0.09 s and Go's 0.53 s; Python takes 5.4 s.
