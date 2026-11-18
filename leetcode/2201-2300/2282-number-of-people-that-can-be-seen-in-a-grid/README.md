# 2282. Number of People That Can Be Seen in a Grid

You are given an `m x n` **0-indexed** 2D array of positive integers
`heights` where `heights[i][j]` is the height of the person standing at
position `(i, j)`.

A person standing at position `(row1, col1)` can see a person standing
at position `(row2, col2)` if:

- The person at `(row2, col2)` is to the right **or** below the person
  at `(row1, col1)`. More formally, this means that either `row1 ==
  row2` and `col1 < col2` **or** `row1 < row2` and `col1 == col2`.
- Everyone in between them is shorter than **both** of them.

Return *an* `m x n` *2D array of integers* `answer` *where*
`answer[i][j]` *is the number of people that the person at position*
`(i, j)` *can see.*

```
heights = [[3,1,4,2,5]]          ->  [[2,1,2,1,0]]
heights = [[5,1],[3,1],[4,1]]    ->  [[3,1],[2,1],[1,0]]
```

**Constraints:** `1 <= heights.length <= 400`; `1 <= heights[i].length
<= 400`; `1 <= heights[i][j] <= 10^5`.

Rows and columns are separate lines, and along one line it is the
next-taller problem with a twist for ties. From the far end, a stack
keeps the people still in view, falling toward the near end. A person
sees everyone shorter that it pops, and the first one not shorter, if
any; when that one is the same height it is popped too, since no one
nearer can see past two people of one height. O(m n).

## Approaches

| file | mechanism |
|---|---|
| `seen.kara` ★ | `sightings` of one line by a stack from its far end; each row as it stands and each column read into a `Vec`, their counts added |
| `seen_naive.kara` | each person walks its row and its column, keeping the tallest in between and stopping at the first not shorter than itself; O(m n (m + n)) on a falling line |
| `seen_forward.kara` | a stack from the near end: each arriving person is seen by everyone shorter it pops and by the first not shorter, the credit going to the one looking |
| `seen_struct.kara` | `struct Lookout` of the heights in view; `look` (`mut ref self`) takes the next person toward the near end and answers how many it sees |
| `seen_iter.kara` | in chains: per person, `skip` past it, `scan` carrying the tallest in between, `take_while` it is shorter than the one looking, `filter` and `count`; the columns by a transpose of `map`s, added by `zip` |
| `seen_solution.kara` | LeetCode's Rust template: `Vec<Vec<i32>>` in and out; per row and per column a stack read by `while let Some(&top) = st.last()` and `if let Some(&top)`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and five
more (one person; three alike, `[1, 1, 0]`; a falling column, `[1, 1,
0]`; a rising row, `[1, 1, 0]`; a valley seen across, `[2, 1, 1, 0]`),
each with its answers; then 1000 random grids of 1 to 8 by 1 to 8 with
heights up to 3, 10 or 10^5, with a checksum; then three of the
constraints' largest, 400 by 400, each with the people seen summed:
random heights (629519), everyone alike (319200), and every row rising
(319200). `seen.py` mirrors the ★ arm and its output is byte-identical;
it was also checked against the brute reading on 2000 random grids.

The iter arm first passed `row.clone()` to `sightings`; `karac check`
warns that a bare parameter only borrows (`redundant_clone`), and
`karac fix` passes `row`.

`karac fix` carries the template in one round, reporting 33 edits:
`Vec<Vec<i32>>` and `Vec<i32>` to brackets, `vec![vec![0; n]; m]` to
`Vec.filled(m, Vec.filled(n, 0))`, `Vec::new()` to `Vec.new()`, each
`Some(&top) = st.last()` to `Some(top) = st.last().cloned()`, `struct
Solution;` to `struct Solution {}`, and in the adapter `&Vec<Vec<i64>>`
to a bare `Vec[Vec[i64]]`, `|&x|` to `|x|` and `Solution::` to
`Solution.`. The adapter's `x as i64` on the way out stays: it widens
the answers.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each person, every person to the right in its row and
below in its column, seen when everyone in between is shorter than
both. No stacks and no early stops. It checks 300 random grids of 1 to
6 by 1 to 6 with heights up to 2, 4 or 100; then 30 single rows falling
to a valley and rising again; then 30 grids of people all alike. All
360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answers are the literal reading's |
| P2 | the grid transposed: the answers transposed |
| P3 | every height tripled and raised by 10^4: the same answers |
| P4 | each answer at least one for each neighbour to the right and below, and at most the people to the right and below |
| P5 | a column of people taller than all added at the right: each answer one more exactly when the person is taller than everyone to its right, and in the new column 1 for each but the last, which sees no one |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 700768989, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that tests
every pair with `all` over the people between. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the first not shorter never counted | P1 329, P4 329, P5 360, P6 329 |
| M5 | ★: each line looked along from the near end | P1 346, P4 346, P5 360, P6 346 |
| M6 | ★: each column read from row 0 | P1 153, P2 213, P6 153 |
| M9 | naive: the tallest not reset for the column | P1 231, P2 184, P4 231, P5 276, P6 231 |
| M10 | naive: the column walk from the person itself | P1 360, P2 346, P4 360, P5 360, P6 360 |
| M11 | naive: an equal in a column not blocking | P1 91, P2 120, P6 91 |
| M12 | forward: the equal one never dropped | P1 123, P5 178, P6 123 |
| M13 | forward: the shorter never credited | P1 285, P4 285, P5 360, P6 285 |
| M14 | forward: the first not shorter never credited | P1 335, P4 330, P5 276, P6 335 |
| M17 | struct: one lookout for every row | P1 276, P2 335, P4 276, P5 276, P6 276 |
| M19 | struct: an equal kept in view | P1 122, P6 122 |
| M20 | struct: the columns looked down from the top | P1 276, P2 346, P4 276, P5 276, P6 276 |
| M22 | iter: the tallest in between never carried | P1 305, P5 327, P6 305 |
| M24 | iter: every person before the block seen | P1 196, P6 196 |
| M25 | iter: the line from the person itself | P1 360, P4 360, P5 360, P6 360 |
| M27 | solution: an equal never dropped along a row | P1 86, P2 120, P6 86 |
| M30 | solution: an equal popped as shorter along a row | P1 89, P2 122, P5 178, P6 89 |

P1 and P6 kill all seventeen, P5 twelve, P4 nine, P2 eight, and P3
none. P3 cannot fail here: every arm compares heights only with one
another, never with a number of its own. P2 catches the edits that
treat rows and columns unalike, which transposing swaps: a column read
from row 0, a walk or a reset in one direction only, a lookout or a
stack carried from row to row, a direction reversed in columns only,
and the template's tie handled wrong along rows alone. P4 catches the
edits that miss a neighbour or count past the line: the first not
shorter never counted or credited, a line read from the wrong end, a
walk from the person itself. P5 catches an edit whose count does not
rise by exactly one for the people taller than everything to their
right, or that miscounts the new column of people alike. The ties are
the hard part: three edits that keep or drop an equal wrongly (M11,
M19, M27) fail nothing but the literal reading, agreement, and in two
of them the transpose.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Ten fail as a kept one does: the ★ arm's equal
never dropped and the forward arm's equal popped as shorter (M1, M15)
as the struct arm's equal kept in view (M19); the ★ arm's equal popped
as shorter and the iter arm's equal in between not blocking (M3, M23)
as the forward arm's equal one never dropped (M12); the ★ arm's columns
never added, the forward arm's column credits upside down and the
template's columns looked down from the top (M4, M16, M28) as the
struct arm's columns looked down from the top (M20); the struct arm's
every look one more and the template's every answer from 1 (M18, M29)
as the iter arm's line from the person itself (M25); and the template's
one stack for every row (M31) as the struct arm's one lookout (M17).
Four fail in ways of their own and are left out because their arms keep
enough: the naive arm's tallest in a row never kept and its seen when
shorter than the one looking only (M7, M8), alike; the struct arm's
only one shorter taken from view (M21); and the iter arm's columns read
from their mirror (M26).

## Verification

Every arm prints the same output as `seen.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the differential takes 2.5 s, the naive arm 2.8
s, the forward arm 2.9 s, the ★ arm 3.4 s, the struct arm 4.2 s, the
template 5.2 s, and the iter arm 22.6 s, a chain of four adapters for
every person of the three 400 by 400 grids. The naive arm is quick only
because the large grids stop each walk early; a falling line would make
it quadratic.

## Benchmarks

The bench answers 40 grids of the constraints' largest, 400 by 400,
heights 1 to 10^5, summing the people seen in each, with the ★ arm in
all five languages. Every implementation prints `40 grids of 400 by
400: checksum 525316389`. C keeps each grid in one `m * n` block and
reads a column with a stride of `n`; the others copy each column into a
list.

BENCHTAB
