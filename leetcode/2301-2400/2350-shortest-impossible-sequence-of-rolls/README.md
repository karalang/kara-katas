# 2350. Shortest Impossible Sequence of Rolls

You are given an integer array `rolls` of length `n` and an integer
`k`. You roll a `k` sided dice numbered from `1` to `k`, `n` times,
where the result of the `i`th roll is `rolls[i]`.

Return *the length of the **shortest** sequence of rolls so that
there's no such subsequence in* `rolls`.

A **sequence of rolls** of length `len` is the result of rolling a `k`
sided dice `len` times.

```
rolls = [4,2,1,2,3,3,2,4,1], k = 4  ->  3
rolls = [1,1,2,2], k = 2            ->  2
rolls = [1,1,3,2,2,2,3,3], k = 4    ->  1
```

**Constraints:** `n == rolls.length`; `1 <= n <= 10^5`;
`1 <= rolls[i] <= k <= 10^5`.

Cut the rolls greedily into pieces that each hold every face from 1 to
`k`, each piece ending as soon as its last new face appears. With `m`
whole pieces, any sequence of length `m` can be taken, one roll from
each piece. And some sequence of length `m + 1` cannot: its first roll
is the face the first piece ends on, which appears nowhere earlier, and
so on piece by piece, until the last roll is a face the leftover part
lacks.

## Approaches

| file | mechanism |
|---|---|
| `rolls.kara` ★ | a table of the faces seen in the current piece and their count; the piece closes when the count reaches `k`, and the table is made afresh. O(n + k m) for m pieces |
| `rolls_set.kara` | the current piece's faces in a `Set`, cleared once it holds all `k`. O(n) |
| `rolls_stamp.kara` | no clearing: each face keeps the number of the last piece it appeared in, so a face is new to the current piece when its stamp is older. O(n + k) |
| `rolls_jumps.kara` | the places of every face listed in order; from a place, each face's next place by binary search, and the latest of them is as far as one more roll can be forced; the answer is how many jumps stay inside the rolls, plus one. O(n + m k log n) |
| `rolls_iter.kara` | iterators: a `fold` whose state is the current piece's faces as a `SortedSet` and the count of whole pieces, a full set closing the piece |
| `rolls_solution.kara` | LeetCode's Rust template: a `HashSet` of the current piece's faces, compared with `k as usize` and cleared once full; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples; one face
rolled `10^5` times; `10^5` rolls cycling through 1000 faces; `10^5`
faces each rolled once, from the last; then 2000 random cases of 1 to
40 rolls of a die with 1 to 6 faces, with a checksum and the answers'
sum. `rolls.py` mirrors the ★ arm and its output is byte-identical, and
the mirror was checked against every sequence up to the answer's
length on 1500 random cases.

The jumps arm was first written with the next place of every face from
every place in one `n + 1` by `k + 1` table. On the line of `10^5` faces
that is `10^{10}` cells; the interpreter grew past 13 GB and was killed
for memory, so the arm now keeps each face's places and searches them.

`karac fix` carries the template in one call, reporting 8 edits.
`check` first reports 3 errors and offers 4 edits for them: the
`use std::collections::HashSet;` line deleted; the two brackets of
`Vec<i32>`; and `HashSet::new` to `HashSet.new`. The other four follow
from those: `HashSet` to `Set`; `k as usize` to `k as i64`, as `usize`
is for FFI, and then that cast dropped, as `i32` widens to `i64` on its
own; and the wrapper's `as i64` on the `i32` answer dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each length from 1 up, every sequence of that length
over the faces 1 to `k` is tried in turn, each matched against the
rolls from the left, and the first length with a sequence the rolls do
not hold is the answer. No pieces. It checks 300 random cases of 1 to
10 rolls of a die with 1 to 3 faces; then 30 of up to 300 rolls of a
die with up to 20 faces; then 30 of up to 300 rolls of a die with up to
3. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 10 rolls, the answer is the literal reading's |
| P2 | from 1 to `n / k + 1`, and 1 exactly when some face is never rolled |
| P3 | the rolls reversed: the same answer |
| P4 | every face `f` made `k + 1 - f`: the same answer |
| P5 | the faces 1 to `k` rolled once more at the end: one more |
| P6 | each arm agrees with at least three of the other five |

P3 holds because a sequence is held by the rolls exactly when its
reverse is held by them reversed. P5 holds because the added faces
close the last, partial piece, at whichever face it lacked last, and
leave fewer than `k` after it.

The differential prints `360 cases: checksum 322861133, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tries every sequence from `itertools.product`. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the table never cleared | P1 149, P5 295, P6 203 |
| M2 | ★: face 1 counted twice | P1 229, P2 224, P3 116, P4 205, P5 286, P6 283 |
| M4 | ★: every roll counted as new | P1 112, P2 34, P6 158 |
| M7 | set: the set never cleared | P1 120, P2 150, P3 127, P5 220, P6 165 |
| M9 | set: the length started at 0 | P1 300, P2 157, P6 360 |
| M11 | set: two counted per piece | P1 237, P2 224, P5 360, P6 295 |
| M12 | stamp: every stamp started at the first piece | P1 237, P2 295, P5 360, P6 295 |
| M13 | stamp: the last roll never read | P1 146, P2 30, P3 70, P5 79, P6 163 |
| M15 | stamp: the next piece started with one face counted | P1 189, P2 91, P3 96, P5 249, P6 243 |
| M17 | jumps: a face found only after the place | P1 181, P2 38, P3 50, P5 91, P6 219 |
| M18 | jumps: one roll skipped after each jump | P1 122, P5 93, P6 159 |
| M21 | jumps: a face's last place never found | P1 224, P2 86, P3 29, P5 92, P6 268 |
| M24 | iter: two more than the pieces | P1 300, P2 236, P6 360 |
| M25 | iter: face `k` read as `k - 1` | P1 135, P2 180, P5 245, P6 180 |
| M26 | iter: the first roll skipped | P1 159, P2 38, P3 70, P6 181 |
| M30 | solution: faces merged in pairs | P1 50, P2 86, P5 136, P6 86 |
| M31 | solution: a piece closed at two faces | P1 176, P2 212, P5 187, P6 227 |

P1 and P6 kill all seventeen, P2 fifteen, P5 thirteen, P3 seven and P4
one. P2 misses the table never cleared and one roll skipped after each
jump, which only ever answer too few, never below 1 and never 1 while
every face is rolled. P5 misses the edits whose error does not change
with one more piece: every roll counted as new, the length started at
0, two more than the pieces, the first roll skipped. P3, the rolls
reversed, fails the edits that treat one end of the rolls or of a piece
unlike the other: face 1 counted twice, the set never cleared, the last
or first roll never read, the next piece started with one face counted,
a face found only after the place, its last place never found. P4,
the faces relabelled, fails only face 1 counted twice: every other edit
treats the faces alike, or, merging faces or reading one as another,
can never close a piece whatever the labels. The first round had no
such edit and P4 killed nothing, so the ★ arm's count never reset,
which failed as its table never cleared, was replaced by face 1 counted
twice.

Of the thirty-one, fourteen were not kept. A piece closed one face
early in the ★ (M3) and set (M8) arms and the template (M29) fail
alike and apart from every kept one. The ★ arm's pieces not one more
(M5) and the template's answer started at 0 (M27) fail as the set
arm's length started at 0 (M9); face 1 never counted in the ★ arm (M6)
and a piece closed only past `k` in the stamp (M16) and iter (M22)
arms as the stamp arm's every stamp started at the first piece (M12);
the set arm's faces merged in pairs (M10) as the template's (M30); the
stamp arm's piece number stepped by two (M14) as the set arm's two
counted per piece (M11); the jumps arm's each face looked for one place
on (M19) as its face found only after the place (M17); its length
started at 2 (M20) as the iter arm's two more than the pieces (M24);
and the set never cleared in the iter arm (M23) and the template (M28)
as in the set arm (M7). The stamp arm's no face stamped and count never
reset failed as M4 and M1, and were replaced by the last roll never
read (M13) and the next piece started with one face counted (M15); a
first replacement for M13, a face new only when stamped two pieces
back, failed as M12. The template's fifth edit was first a piece
counted as `k`, `ans += k`, which `check` refuses, since a compound
assignment with an `i32` operand leaves the literal `ans` at `i64`
(design.md §8 Literals); it was replaced by a piece closed at two faces
(M31).

## Verification

Every arm prints the same output as `rolls.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.5 to 1.4 s but the iter arm,
14.3 s. Its `SortedSet` takes the `10^5` faces from the last, each
insert at the front, and the interpreter's sorted table shifts every
later entry and its key index on each insert, so the line is quadratic
there; under `karac __mir-llvm-run` it is not (B-2026-11-21-50). The differential
takes 0.77 s under `karac __mir-run` and 0.41 s under `karac
__mir-llvm-run`.

## Benchmarks

The bench builds 10 arrays of `10^5` rolls once from the harness's
generator, of dice with 2, 3, 6, 10, 20, 50, 100, 1000, 3000 and
`10^4` faces, then makes 50 passes, pass `p` folding each answer plus
`p` into the checksum, with the ★ arm in all five languages. Every
implementation prints `50 passes over 10 arrays of 10^5 rolls: checksum
602125513`. Each makes its table of seen faces afresh at the end of
every piece, as the ★ arm does: Kāra with `Vec.filled`, Rust with
`vec!`, Go with `make`, C with `calloc`, Python with a list.

BENCHTAB
