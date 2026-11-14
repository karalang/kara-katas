# 2158. Amount of New Area Painted Each Day

There is a long and thin painting that can be represented by a number
line. You are given a **0-indexed** 2D integer array `paint` of length
`n`, where `paint[i] = [start_i, end_i]`. This means that on the `i`-th
day you need to paint the area **between** `start_i` and `end_i`.

Painting the same area multiple times will create an uneven painting so
you only want to paint each area of the painting at most **once**.

Return *an integer array* `worklog` *of length* `n`*, where*
`worklog[i]` *is the amount of **new** area that you painted on the*
`i`-th *day*.

```
paint = [[1,4],[4,7],[5,8]]  ->  [3,3,1]
paint = [[1,4],[5,8],[4,7]]  ->  [3,3,1]
paint = [[1,5],[2,4]]        ->  [4,0]
```

**Constraints:** `1 <= paint.length <= 10^5`; `paint[i].length == 2`;
`0 <= start_i < end_i <= 5 * 10^4`.

The area is made of units, `[x, x + 1)`, and each unit is new paint
once, on the first day whose segment covers it. Each unit points at the
first unpainted unit at or after it, so a day walks only the units it
paints, jumping the rest. O((n + w) α), w the wall's length.

## Approaches

| file | mechanism |
|---|---|
| `painted.kara` ★ | a `Vec` of pointers, each unit at the first unpainted unit at or after it; a painted unit points at the next one, and the walk halves its path as it goes |
| `painted_runs.kara` | the unpainted stretches in a `SortedMap` from start to end; a day takes the stretch reaching in from before it by `floor` and those beginning inside it by `range`, and puts back what sticks out |
| `painted_sweep.kara` | a sweep along the wall, each day opening at its start and closing at its end; the days covering a unit held in a `SortedSet`, and the unit paid to the earliest, its `min` |
| `painted_struct.kara` | a `struct Wall` whose `free` finds the first unpainted unit by recursion and points the whole path at it, and whose `paint` points each unit it paints at the day's end (`mut ref self`); the log by `map` and `collect` |
| `painted_tree.kara` | a segment tree of painted counts; a day enters only nodes that overlap it and are not full, and fills a node it covers whole at once, its children never entered again |
| `painted_solution.kara` | LeetCode's Rust template: a `line` of `i32`s where a painted unit holds the end of its block, `vec![0; 50001]`, `start as usize`, each jump stretching the block it passes to the day's end; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples and four
more (one day, the same segment twice, segments that grow around each
other, and segments that only touch), each with its log; then the total
and a checksum over 2000 random lists of 1 to 8 segments within 10, 30
or 100 units in turn; then the constraints' largest, 100000 days on a
wall of 50000 units, of segments of up to 50 units, of any length, and
of the whole wall every day. `painted.py` mirrors the ★ arm and its
output is byte-identical.

No compiler gap was met. `karac fix` carries the template in three
rounds of 21, 1 and 2 edits: Rust's spellings (`<..>` to `[..]`,
`Vec::with_capacity` to `Vec.with_capacity`, `let (mut start, end)` to
`let mut (start, end)`, `struct Solution;` to `struct Solution {}`, the
adapter's `&Vec` to `ref Vec`, `|&x|` and `|&a|` to `|x|` and `|a|`,
`Solution::` to `.`); then `vec![0; 50001]` given the `i32` that Rust
infers from `line[..] = end`, as `vec![0i32; 50001]`; then that to
`Vec.filled(50001, 0i32)`, and the `ref` dropped from the adapter's
parameter, which borrows already.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a wall of units, each day's segment walked unit by unit, the
units not yet painted counted and then painted; no jumps, sets or
trees. It checks 300 random lists of 1 to 8 segments within 10, 30 or
100 units in turn; then 30 whose segments all start at 0; then 30 of
segments one unit long. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the log is the statement read literally |
| P2 | every segment moved 7 units on: the same log |
| P3 | the wall turned end for end: the same log |
| P4 | every day's segment painted again the next day: each day's area followed by a 0 |
| P5 | every unit made two: every day's area doubled |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 lists: checksum 629636597, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
lists by the same walk. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Twenty-three edits to the differential, two to five to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a painted unit left pointing at itself | P1 291, P4 360, P6 291 |
| M2 | ★: the walk started a unit late | P1 360, P5 360, P6 360 |
| M20 | ★: the walk stepping a unit at a time, never jumping | P1 179, P3 210, P6 179 |
| M4 | runs: a stretch beginning at the start taken twice | P1 186, P2 175, P3 320, P6 186 |
| M5 | runs: the part sticking out past the end dropped | P1 231, P3 279, P6 231 |
| M6 | runs: the part sticking out before the start dropped | P1 211, P3 279, P6 211 |
| M9 | sweep: unit 0 never swept | P1 175, P2 175, P3 321, P6 175 |
| M10 | sweep: a segment closed a unit early | P1 352, P3 58, P5 360, P6 352 |
| M23 | sweep: a segment never closed | P1 241, P3 279, P6 241 |
| M11 | struct: the walk started at the start, painted or not | P1 263, P3 207, P4 360, P5 263, P6 263 |
| M12 | struct: one pointer followed, not the chain | P1 133, P3 132, P4 174, P5 133, P6 133 |
| M22 | struct: the walk jumping to the end after one unit | P1 327, P3 133, P5 360, P6 327 |
| M14 | tree: full nodes entered | P1 252, P2 226, P3 199, P5 166, P6 252 |
| M15 | tree: a node's earlier paint counted again | P1 230, P2 197, P3 142, P5 100, P6 230 |
| M17 | tree: the middle unit dropped from the right half | P1 308, P2 336, P3 288, P5 310, P6 308 |
| M18 | solution: a jump landing a unit past the block | P1 198, P3 203, P5 203, P6 198 |
| M19 | solution: a block claimed a unit past the day's end | P1 198, P3 205, P5 203, P6 198 |

P1 and P6 kill all seventeen, P3 fifteen, P5 ten, P2 five and P4 three.
Each property moves the segments in a way that leaves every right log
alone. P3 turns the wall end for end, so an edit that treats a
segment's two ends differently shows there: all but M1 and M2, which
treat them alike. P5 doubles every unit, which sees most edits that are
out by a fixed number of units, since on the doubled wall they are out
by the same number, not by twice it. P2 moves every segment 7 units on, which sees an edit
that treats unit 0 or the tree's halves apart (M4, M9, M14, M15, M17).
P4 paints every day twice, which sees an edit that counts a unit
painted before as new (M1, M11, M12): the repeat day must log 0.

Of the twenty-three, six were not kept. Four fail as a kept one does:
the ★ arm's last unit never painted, as M2; and the sweep paying the
latest covering day, the sweep paying every covering day, and the
struct counting a unit free when it points ahead, as M1, since each
counts a unit painted before as new. Two fail in ways of their own but
were left out to keep three to each arm: the runs arm missing a
stretch that begins at the start (M7), and the tree never telling a
node what its children added (M16).

## Verification

Every arm prints the same output as `painted.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 2.3 s to 10.7 s, the sweep the
slowest, since the interpreter keeps a `SortedSet` as one sorted array,
and the differential 2.8 s.

## Benchmarks

The bench builds 4 lists of 100000 segments of 1 to 500 units on a wall
of 50000 once; then solves every list 5 times, one segment replaced by
a new one before each solve so that no solve repeats one before, with
the ★ arm in all five languages. Every implementation prints `20
solves: 999985 units in all, checksum 823235554`.

BENCHTAB
