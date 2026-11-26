# 1494. Parallel Courses II

You are given an integer `n`, which indicates that there are `n` courses
labeled from `1` to `n`. You are also given an array `relations` where
`relations[i] = [prevCourse_i, nextCourse_i]`, representing a
prerequisite relationship between course `prevCourse_i` and course
`nextCourse_i`: course `prevCourse_i` has to be taken before course
`nextCourse_i`. Also, you are given the integer `k`.

In one semester, you can take at most `k` courses as long as you have
taken all the prerequisites in the previous semesters for the courses
you are taking. Return the minimum number of semesters needed to take
all courses. The testcases will be generated such that it is possible to
take every course.

```
n = 4, relations = [[2,1],[3,1],[1,4]], k = 2        ->  3
n = 5, relations = [[2,1],[3,1],[4,1],[1,5]], k = 2  ->  4
```

**Constraints:** `1 <= n <= 15`, `1 <= k <= n`, `0 <= relations.length
<= n * (n-1) / 2`, the relations are all different, and the graph is a
directed acyclic graph.

The arms are `fn min_number_of_semesters(n: i32, relations:
Vec[Vec[i32]], k: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `min_number_of_semesters.kara` ★ | a DP over the sets of courses taken: from each set reached, the courses whose prerequisites it holds are open, and a semester takes all of them when they are no more than k, else every k of them, walked as the subsets of the open mask. O(3^n) at worst |
| `min_number_of_semesters_bfs.kara` | a breadth-first search over the same sets, one level a semester; the level that first reaches every course is the answer. O(3^n) at worst |
| `min_number_of_semesters_memo.kara` | recursion on the set taken, each set's answer kept: one semester more than the best of the sets it can reach. O(3^n) at worst |
| `min_number_of_semesters_pick.kara` | the ★ arm's DP, each semester's k courses chosen by recursion over the list of open courses, take this one or leave it, rather than by walking the subsets of a mask. O(3^n) at worst |
| `min_number_of_semesters_solution.kara` | a Rust solution as LeetCode's Rust users write it (`usize` masks, every subset of at most k open courses tried), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`3 4`); six
edges, one course, 15 free courses one at a time and all at once, a
chain of 15, one course every other one needs, taken two at a time, and
chains of 3, 2, 2 and 2 courses taken two at a time (`1 15 1 15 4 5`);
the constraints' most, 15 courses with few, some and many relations
taken 2, 3 and 4 at a time (`15 courses: [8, 5, 4, 8, 5, 4, 8, 9, 11]`);
and 1000 random cases of 1 to 11 courses (`1000 random cases: checksum
755839910`). `min_number_of_semesters.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, bfs and memo arms check clean as first written.
The pick arm was first written `(0..n).filter(...).collect()` into a
`Vec[i64]` with `n` the `i32` parameter, so the range gives `i32`s;
`collect` does not convert its items, and `karac fix` added the
`.map(|x| x as i64)` check asked for. The Rust solution takes one round
of 20 fixes by `karac fix`'s count, and its diff is: `struct Solution;`
to `struct Solution {}`, each `Vec<i32>` to `Vec[i32]`, `n as usize` to
`n as i64` and the other `usize`s dropped, each `vec![x; n]` to
`Vec.filled(n, x)`, `for r in &relations` to `for r in ref relations`,
`i32::MAX` to `i32.MAX`, `&&` to `and` and `Solution::` to `Solution.`.
The harness walks `for k in [2, 3, 4]` and passes `k` as the `i32`
argument; check refuses it, since a `for` over an array literal settles
its literals before the body can fix them (B-2026-11-26-2), and the
harness keeps the `2i32` that `karac fix` writes. Every arm's output
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the fewest semesters in some schedule that gives each course
a semester, each prerequisite an earlier one, and no semester more than
k courses, found by placing the courses one at a time in an order that
puts each after its prerequisites, for 1 semester, then 2, and so on.
LeetCode's examples, the edges, and 1993 random cases of 1 to 8 courses,
each pair joined with a chance of up to one in two. Each arm meets six
properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | no fewer than n / k rounded up or the longest chain, and no more than n |
| P3 | a course more each semester takes no more semesters |
| P4 | the courses numbered the other way round take the same |
| P5 | one prerequisite fewer takes no more semesters |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 cases: checksum 688929572,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, searching
breadth first with every set of up to k open courses a semester, gives
the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: k + 1 courses taken when no more are open | P1 557, P2 551, P5 35, P6 2228 |
| M2 | ★: every set below the open courses tried, not only the open ones | P1 24, P2 17, P3 17, P4 2, P6 96 |
| M3 | bfs: a course open once any of its prerequisites is taken | P1 305, P2 298, P5 12, P6 305 |
| M4 | bfs: the count of semesters started at 1 | P1 2000, P2 720, P6 2000 |
| M5 | memo: each set's kept answer one semester short | P1 457, P2 451, P3 62, P4 74, P5 1, P6 457 |
| M6 | memo: every course taken still needs a semester | P1 2000, P2 720, P6 2000 |
| M7 | pick: the first k open courses always taken, never another k | P1 64, P4 100, P5 16, P6 64 |
| M8 | pick: one course a semester | P1 1280, P6 1280 |
| M9 | solution: at most k - 1 courses a semester | P1 1278, P2 671, P6 1278 |
| M10 | solution: the empty set starts at one semester | P1 2000, P2 720, P6 2000 |

## Benchmarks

The bench makes 300 calls of the ★ arm on 15 courses, each call's
relations, every pair joined with a chance below one in twelve, and its
k, from 2 to 5, drawn from a generator seeded by the checksum so far.
Every implementation prints `300 calls on 15 courses: checksum
196706867`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.47 s against Rust's 0.89 s (0.91 s with
overflow checks on), C's 1.5 s and Go's 0.80 s; Python takes 85.6 s. The
gap is the popcount: `karac build` targets x86-64-v2 by default, which
has the `popcnt` instruction, while `rustc -O` and `clang -O3` target
plain x86-64 and count a mask's bits in software. Given `popcnt` alone
(`-C target-feature=+popcnt`, `-mpopcnt`), Rust takes 0.45 s and C 0.45
s; built for x86-64-v2, Rust takes 0.47 s (0.44 s with overflow checks
on) and C 0.48 s. `bench.sh` adds matched-ISA rows built for x86-64-v3.
