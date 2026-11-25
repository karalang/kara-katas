# 1395. Count Number of Teams

There are `n` soldiers standing in a line. Each soldier is assigned a
unique `rating` value.

You have to form a team of 3 soldiers amongst them under the following
rules: choose 3 soldiers with index (`i`, `j`, `k`) with rating
(`rating[i]`, `rating[j]`, `rating[k]`); a team is valid if (`rating[i]
< rating[j] < rating[k]`) or (`rating[i] > rating[j] > rating[k]`) where
(`0 <= i < j < k < n`).

Return the number of teams you can form given the conditions. (soldiers
can be part of multiple teams).

```
rating = [2,5,3,4,1]  ->  3
rating = [2,1,3]      ->  0
rating = [1,2,3,4]    ->  4
```

**Constraints:** `n == rating.length`, `3 <= n <= 1000`, `1 <= rating[i]
<= 10^5`, and all the integers in `rating` are unique.

Each arm is `fn num_teams(rating: Vec[i32]) -> i32`. The most teams,
C(1000, 3) = 166,167,000, fits an `i32`.

## Approaches

| file | mechanism |
|---|---|
| `num_teams.kara` ★ | each soldier taken as the middle of a team, the smaller and the larger ratings counted on each side of it; a rising team is a smaller one left and a larger one right, a falling team the other way round, so the soldier is the middle of `less_left * greater_right + greater_left * less_right` teams. O(n^2) |
| `num_teams_pairs.kara` | teams grown a soldier at a time: for each soldier, the rising and the falling pairs that end at it, and each later soldier larger than a rising pair's end, or smaller than a falling pair's end, finishes that many teams. O(n^2) |
| `num_teams_fenwick.kara` | the ★ arm's four counts by a Fenwick tree, a `struct` with `mut ref self` and `ref self` methods: the ratings ranked by sorting and `binary_search`, the tree counting the ranks to the left as the line is walked, and the counts on the right found by subtraction. O(n log n) |
| `num_teams_sorted.kara` | the soldiers to the left in one `SortedSet` and those to the right in another, which loses each soldier as the walk reaches it; `range(..).count()` gives the smaller ratings on each side. O(n^2), since each range is walked to be counted |
| `num_teams_solution.kara` | a Rust solution as LeetCode's Rust users write it (an index loop over `1..n - 1`, four counters bound in one `let (mut ll, mut lg, mut rl, mut rg)`, each side counted with `<` and `>`, and the products summed into `res`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples, one
falling team, and none (`3 0 4 1 0`); the constraints' most, 1000
soldiers rising, falling, and shuffled (`1000 soldiers: 166167000
166167000 54463993`); and 2000 random lines of 3 to 40 soldiers, 1 to n
shuffled and scaled by up to 100 (`2000 random lines: 1781702 teams in
all, checksum 213660859`). `num_teams.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the pairs and Fenwick arms check clean as first written.
The ★ arm declared its counters as Rust does, `let (mut less_left, mut
greater_left) = (0, 0);`; Kāra puts `mut` before the whole pattern, and
`karac fix` writes `let mut (less_left, greater_left) = (0, 0);`, 6
fixes by its count for the 4 errors. Its `let mut teams = 0;`, returned
as the `i32` answer, takes `i32` from the return, since a return fixes a
literal's type, and the counters added into it then take `i32` too
(design.md §8 Literals). The sorted arm counted with Rust's half-open
`left.range(..x)`; Kāra's `range` takes both ends, the diagnostic says
so and names `range(i32.MIN, x)` over `i32`, and `karac fix` writes it.
The Rust solution takes one round of 9 fixes by `karac fix`'s count,
from 7 errors: `struct Solution;` to `struct Solution {}`, `Vec<i32>` to
`Vec[i32]`, `let (mut ll, mut lg, mut rl, mut rg)` to `let mut (ll, lg,
rl, rg)`, and `Solution::` to `Solution.`. Its output matches on the
first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every three soldiers i < j < k tried, and those whose ratings
rise or fall all the way counted. LeetCode's three examples and 2000
lines of 3 to 14 soldiers, 1 to n shuffled and scaled by up to 100,
leaving room for P4 and P5 inside the constraints. Every case is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the line read from the other end: the same |
| P3 | each rating r made top + 1 - r, so rising is falling: the same |
| P4 | a soldier taller than all added at the end: one more team for each rising pair |
| P5 | every rating three times as large: the same |
| P6 | the ★ arm's answer |

All 60,090 checks pass on every arm: `2003 lines: checksum 358806165,
60090 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, trying every
three soldiers with `combinations`, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: falling teams not counted | P1 1664, P2 1812, P3 1812, P6 6656 |
| M2 | ★: each soldier counted among the larger to its own right | P1 1965, P2 1884, P3 1884, P4 2003, P6 7860 |
| M3 | pairs: a later soldier finishing its own rising pairs, not the earlier one's | P1 1965, P2 1946, P3 1932, P4 2003, P6 1965 |
| M4 | pairs: a soldier never paired with the one just before it | P1 1853, P4 1965, P6 1853 |
| M5 | Fenwick: the tree's update stepping by one, not by its lowest bit | P1 1678, P2 1801, P3 1823, P4 1942, P6 1678 |
| M6 | Fenwick: the larger on the right not reduced by the larger on the left | P1 1802, P2 1819, P6 1802 |
| M7 | sorted: each soldier left in the set to its right | P1 1965, P2 1928, P3 1884, P4 2003, P6 1965 |
| M8 | sorted: one too few larger on the left | P1 1972, P2 1884, P3 1884, P6 1972 |
| M9 | solution: the soldier second from the end never the middle | P1 1423, P2 1611, P4 1852, P6 1423 |
| M10 | solution: the larger on the right counted as smaller | P1 1854, P2 1812, P3 1896, P4 1884, P6 1854 |

P1 and P6 kill all ten, P2 nine, P3 and P4 seven each, and P5 none:
every arm only compares ratings, so tripling them changes nothing for
any arm, and no edit changes that. Reading the line from the other end
(P2) catches every edit but M4, whose missing pairs of neighbours are
missing from either end alike. Flipping the ratings (P3) turns rising
into falling, which M1, counting one kind only, fails; M4, M6 and M9
drop or miscount teams by place, not by kind, and pass it. A tallest
soldier added at the end (P4) finishes one team per rising pair, which
the edits that miscount a soldier's own place or the last places fail.

## Benchmarks

The bench lays 1000 soldiers, the constraints' most, rated 97 to 97,000
and shuffled, once. Then 300 rounds, each swapping two soldiers drawn
from the checksum so far and counting the teams. Every implementation
prints `300 rounds over 1000 soldiers: checksum 749306980`. The work is
the ★ arm's two scans of each side, 10^6 comparisons a round. Without
overflow checks, `rustc -O` and `clang -O3` turn each scan into vector
compares and counts, branch-free (`pcmpgtd` in their assembly), and run
some 15 times faster here. With them, as Kāra and `rustc -O -C
overflow-checks=on` both run, the assembly has no `pcmpgtd`, and each
comparison is a branch on a shuffled line, as it is in Go; the
equal-safety comparison is Kāra against the overflow-checked Rust.

BENCHTAB
