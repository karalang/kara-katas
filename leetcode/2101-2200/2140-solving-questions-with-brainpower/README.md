# 2140. Solving Questions With Brainpower

You are given a **0-indexed** 2D integer array `questions` where
`questions[i] = [points_i, brainpower_i]`.

The array describes the questions of an exam, where you have to
**process the questions in order** (i.e., starting from question `0`)
and make a decision whether to **solve** or **skip** each question.
Solving question `i` will **earn** you `points_i` points but you will be
**unable** to solve each of the next `brainpower_i` questions. If you
skip question `i`, you get to make the decision on the next question.

- For example, given `questions = [[3, 2], [4, 3], [4, 4], [2, 5]]`:
  - If question `0` is solved, you will earn `3` points but you will be
    unable to solve questions `1` and `2`.
  - If instead, question `0` is skipped and question `1` is solved, you
    will earn `4` points but you will be unable to solve questions `2`
    and `3`.

Return *the **maximum** points you can earn for the exam*.

```
questions = [[3,2],[4,3],[4,4],[2,5]]          ->  5
questions = [[1,1],[2,2],[3,3],[4,4],[5,5]]    ->  7
```

**Constraints:** `1 <= questions.length <= 10^5`;
`questions[i].length == 2`; `1 <= points_i, brainpower_i <= 10^5`.

The best from question i on is either the best from i + 1, skipping it,
or its points plus the best from the first question its brainpower
leaves free, past the end counting as nothing. Filled from the back,
each place is read once. O(n).

## Approaches

| file | mechanism |
|---|---|
| `brainpower.kara` ★ | the best from each question on, a `Vec.filled(n + 1, 0)` filled from the back, the place a solve resumes at clamped by `min` |
| `brainpower_forward.kara` | forward: the most points with question i the next one free, pushed on to i + 1 by a skip and past the brainpower by a solve; the answer is what reaches the end |
| `brainpower_fold.kara` | one `fold` over the questions from the back carrying a `VecDeque`, grown at its front by `push_front`, so the best from i + 1 + brainpower lies brainpower places into it |
| `brainpower_struct.kara` | a `struct Question` read `of` each pair and asked where the next solve may `resume` (`ref self`), and a `struct Exam` holding the questions and the table, each place filled by `settle` (`mut ref self`) |
| `brainpower_pairs.kara` | the questions as `(points, brainpower)` tuples walked by `rev().enumerate()` and destructured in the `for` pattern, the table built from the end by `push` and read at a distance from the end |
| `brainpower_solution.kara` | LeetCode's Rust template: `vec![0i64; n + 1]`, the brainpower read `as usize`; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one question, no brainpower anywhere, every question shutting out the
rest, and the best taken from the far end), each with its answer; then
the total and a checksum over 2000 random lists of 1 to 12 questions,
points of 1 to 10 or 1 to 100000, brainpower of 0 to 3 or 0 to 12, in
turn; then the constraints' largest, 100000 questions: no brainpower,
the most brainpower, and at random. The tests also ask brainpower 0,
below the constraints, where a solve shuts out nothing, as every arm
reads it. `brainpower.py` mirrors the ★ arm and its output is
byte-identical.

No compiler gap was met. `karac fix` carries the template in three
rounds of 13, 2 and 3 edits: Rust's spellings (`<..>` to `[..]`, the
adapter's `|&v|` to `|v|`, `struct Solution;` to `struct Solution {}`,
the adapter's `&Vec` to `ref Vec`, `Solution::` to `.`); then
`vec![0i64; n + 1]` to `vec![0; n + 1]`, since an `i64` is a bare
literal's own type, and `as usize` to `as i64`; then `vec![0; n + 1]` to
`Vec.filled(n + 1, 0)`, the `as i64` dropped, since an `i32` widens in
`i + 1 + ..`, and the `ref` dropped from the adapter's parameter, which
borrows already. The template's `questions[i][0] as i64` stays: it makes
a binding's type.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every set of questions to solve is tried, and a set counts
when no question in it lies within the brainpower of an earlier one in
it; the most points over the sets that count is the answer. No table is
built. It checks 300 random lists of 1 to 10 questions, points of 1 to
9, brainpower of 0 to 3; then 30 with brainpower of 0 to 10; then 30
with every brainpower 0. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the points are the statement read literally |
| P2 | a question of 0 points and brainpower 0 added at the end: the same |
| P3 | every point doubled: twice the points |
| P4 | every brainpower 0: every point |
| P5 | a question of 0 points added at the front, of any brainpower: the same |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 lists: checksum 945803739, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
lists by the same search. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Twenty-seven edits to the differential, four to six to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the brainpower not skipped | P1 287, P6 287 |
| M3 | ★: never skipping | P1 171, P5 276, P6 171 |
| M5 | ★: the brainpower read as the points | P1 356, P3 322, P4 360, P5 154, P6 356 |
| M7 | forward: the answer at the last question | P1 360, P2 182, P4 360, P6 360 |
| M8 | forward: a solve landing one short | P1 286, P4 360, P6 286 |
| M9 | forward: a solve overwriting | P1 147, P2 244, P6 147 |
| M10 | fold: the deque grown at its back | P1 360, P4 360, P6 360 |
| M11 | fold: the solve read one place on | P1 245, P4 329, P6 245 |
| M13 | fold: the questions folded from the front | P1 240, P6 240 |
| M15 | exam: the questions settled from the front | P1 297, P4 329, P5 360, P6 297 |
| M16 | exam: a question read with its pair swapped | P1 354, P3 322, P4 360, P5 285, P6 354 |
| M26 | exam: the skip read two on | P1 133, P5 282, P6 133 |
| M18 | pairs: the table read from the start | P1 310, P2 200, P4 329, P6 310 |
| M20 | pairs: one question too few skipped | P1 207, P6 207 |
| M21 | pairs: the answer over one question fewer | P1 248, P4 360, P5 248, P6 248 |
| M24 | solution: the adapter dropping the first question | P1 217, P2 31, P4 329, P5 217, P6 217 |
| M25 | solution: the adapter's brainpower doubled | P1 158, P6 158 |

P1 and P6 kill all seventeen, P4 ten, P5 seven, P2 four and P3 two. P4
takes the brainpower away, so every point counts; it sees an edit that
loses a question or a place even with nothing shut out: a solve landing
off its place (M8, M11), the table grown or read at the wrong end (M10,
M18), the questions settled from the front (M15), the answer read one
place off (M7, M21), the brainpower or the pair read as points (M5,
M16), and the adapter's lost first question (M24). P5 puts a question
of 0 points at the front; it sees an edit that treats the first
question unlike the rest or that a front question changes: never
skipping (M3), the brainpower or the pair read as points (M5, M16), the
questions settled from the front (M15), the skip read two on (M26), the
answer over one question fewer (M21), and the lost first question
(M24). P2 adds a question of 0 points at the end, which changes no
answer; it sees an edit that reads the end as an answer or a bound: the
answer at the last question (M7), a solve overwriting the most that
reaches a place (M9), the table read from the start (M18), and the
adapter's lost first question (M24). P3 doubles every point; it sees an
edit that reads the brainpower as points (M5, M16), which doubling does
not double.

Of the twenty-seven, ten were not kept. None is equivalent and none
fails by a crash. Nine fail as a kept one does: the struct arm's resume
ignoring the brainpower, as M1; the ★ arm's one question too many
skipped, as M11; the struct arm's skip read at the question itself and
the template never skipping, as M3; the ★ arm's answer from the second
question, as M21; the template's points read as brainpower, as M5; the
fold arm's skip only and the struct arm's points counted twice, as M10;
and the pairs walked from the front, as M13. One is killed with checks
of its own but was left out because its arm keeps its share: the
forward arm's skip never carried (P1 103, P6 103).

## Verification

Every arm prints the same output as `brainpower.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.4 s to 3.9 s and the
differential 1.4 s.

## Benchmarks

The bench builds 10 lists of 100000 questions once, points of 1 to
100000 and brainpower of 0 to 20; then solves every list 20 times, one
question redrawn before each solve so that no solve repeats one before,
with the ★ arm in all five languages. C holds each question as its own
two-value allocation, as a `Vec[Vec[i64]]` does. Every implementation
prints `200 solves: 73781285718 points in all, checksum 66167467`.

BENCHTAB
