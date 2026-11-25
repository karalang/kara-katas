# 1349. Maximum Students Taking Exam

Given an `m * n` matrix `seats` that represents seat distribution in a
classroom, a seat is broken if it is `'#'` and in good condition if it
is `'.'`. Students can see the answers of those sitting next to the left,
right, upper left and upper right, but cannot see the answers of the
student sitting directly in front or behind. Return the maximum number of
students that can take the exam together without any cheating being
possible. Students must be placed in seats in good condition.

```
["#.##.#",                        [".#",           ["#...#",
 ".####.",   ->  4                 "##",            ".#.#.",
 "#.##.#"]                         "#.",   ->  3    "..#..",   ->  10
                                   "##",            ".#.#.",
                                   ".#"]            "#...#"]
```

**Constraints:** `seats` contains only `'.'` and `'#'`, `1 <= m <= 8`,
`1 <= n <= 8`.

The arms are `fn max_students(seats: Vec[Vec[char]]) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `max_students.kara` ★ | a row's students as a bit mask; a row's mask must sit on good seats with no two side by side, and no student may sit diagonally behind one in the row in front, so `mask & (prev << 1)` and `mask & (prev >> 1)` must be empty. `best[mask]` is the most students so far with the last row seated as `mask`. O(m * 4^n) |
| `max_students_memo.kara` | the most students from a row on, given the mask seated in the row before, remembered in a `Map` by (row, mask); each row tries every subset of its good seats, walked as `sub = (sub - 1) & good` down to the empty row. O(m * 2^n * 2^g) for g good seats in a row |
| `max_students_matching.kara` | every clash joins a seat in an even column to one in an odd column, so the clashes form a bipartite graph, and the most students is its largest independent set: the good seats less a maximum matching (König), found by augmenting paths from each even-column seat (Kuhn). O(V * E) |
| `max_students_profile.kara` | the seats one at a time in reading order, the state the last n + 1 seats' occupancy; a student may sit if the seat is good and the seats to the left (1 back), upper left (n + 1 back) and upper right (n - 1 back) are empty. O(m * n * 2^(n+1)) |
| `max_students_solution.kara` | a Rust solution as LeetCode's Rust users write it (each row's good seats as a `usize` mask, `vec![vec![-1i32; 1 << n]; m + 1]` filled row by row over `1..=m`, the masks walked as `0..(1usize << n)` and tested with `&&`, and the answer `*dp[m].iter().max().unwrap()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples; one good
seat; every seat broken; and 8 by 8, the constraints' largest, every
seat good, and every seat good but the diagonal (`4 3 10 1 0 32 28`);
and 2000 random rooms of 1 to 8 rows and columns, each seat good with
probability 1/2, 3/4 or 1 (`2000 random rooms: 17613 students in all,
checksum 650260819`). `max_students.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the ★, matching and profile arms check clean. The memo
arm's `let mut best = 0;` keeps the default `i64` and is stored into a
`Map` of `i32` and returned as one; `karac check` refuses the narrowing
(E0200) and names the fix, `best: i32`, which `karac fix` applies. The
Rust solution takes one round of 10 fixes by `karac fix`'s count:
`struct Solution;` to `struct Solution {}`, `Vec<..>` to `Vec[..]`,
each `vec![x; n]` to `Vec.filled(n, x)`, and `&&` to `and`; its
`usize` masks and the `*` before `dp[m].iter().max().unwrap()` stand. Every arm matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every set of good seats tried, kept when no two students in
it sit side by side or one upper left or upper right of the other, and
the largest kept. 2000 rooms of at most 16 seats in four kinds, 500
each: 1 to 4 rows and columns with each seat good with probability 1/2;
with probability 3/4; every seat good; and 1 or 2 rows of 5 to 8 seats,
the constraints' widest, each good with probability 3/4. Every room is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the room mirrored left to right: the same answer |
| P3 | the room turned front to back: a clash runs both ways, so the same answer |
| P4 | one more seat broken: the same answer or one fewer |
| P5 | a row of broken seats after the first half of the rows: the two halves' answers added |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 rooms: checksum 194770679,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, searching seat by seat with
backtracking, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: students side by side allowed | P1 676, P6 2704 |
| M2 | ★: one diagonal against the row in front not tested | P1 73, P2 119, P3 119, P6 292 |
| M3 | memo: a row never left empty when it could seat someone | P1 39, P3 45, P4 24, P5 19, P6 39 |
| M4 | memo: an answer looked up by the row before's first seat only | P1 14, P2 17, P3 13, P6 14 |
| M5 | matching: paths started from odd columns too | P1 1474, P4 758, P6 1474 |
| M6 | matching: the clashes with the row behind left out | P1 87, P2 112, P3 164, P6 87 |
| M7 | profile: a broken seat taken | P1 928, P5 2000, P6 928 |
| M8 | profile: the seat in front taken for the upper left | P1 618, P2 425, P3 224, P6 618 |
| M9 | solution: a mask allowed when it touches a good seat | P1 624, P4 45, P6 624 |
| M10 | solution: the answer read one row early | P1 1778, P3 429, P5 1802, P6 1778 |

P1 and P6 kill all ten, P3 six, P2 four, P4 three and P5 three.
Mirroring the room (P2) and turning it front to back (P3) catch the
edits that see a clash one way but not the other: one diagonal left out
(M2), the row behind left out (M6), the seat in front taken for a
diagonal (M8), and a remembered answer keyed by the side the room starts
from (M4); turning it also catches the edits that treat the first and
last rows unlike the rest (M3, M10). One more broken seat (P4) catches
the edits whose answer can rise when a seat breaks: a row forced to seat
someone (M3), a matching that counts a clash twice (M5), and a mask on a
broken seat (M9). A row of broken seats cutting the room (P5) catches
the edits for which that row does not separate the halves (M7, M10) or
must seat someone (M3). Students side by side (M1) are caught only by
the statement and the other arms: mirrored, turned, with a seat broken
or cut in two, the edited ★ is wrong the same way.

## Benchmarks

The bench builds 20 rooms of 8 by 8 seats, the constraints' largest,
each seat good with probability 3/4, once; then makes 3000 rounds, each
turning one seat of one room, both drawn from the checksum so far, from
good to broken or back, so no answer carries over, answering that room
with the ★ arm's row masks and folding the answer plus the round into
the checksum. Every implementation prints `3000 rounds over 20 rooms of
8 by 8: checksum 235810182`.

BENCHTAB
