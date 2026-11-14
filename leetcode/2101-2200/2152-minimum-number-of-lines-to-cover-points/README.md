# 2152. Minimum Number of Lines to Cover Points

You are given an array `points` where `points[i] = [xi, yi]` represents
a point on an **X-Y** plane.

**Straight lines** are going to be added to the **X-Y** plane, such
that every point is covered by at **least** one line.

Return *the **minimum** number of **straight lines** needed to cover
all the points*.

```
points = [[0,1],[2,3],[4,5],[4,3]]  ->  2
points = [[0,2],[-2,-2],[1,4]]      ->  1
```

**Constraints:** `1 <= points.length <= 10`; `points[i].length == 2`;
`-100 <= xi, yi <= 100`; all the points are **unique**.

At most 10 points, so the points covered so far are a mask, and the
fewest lines for each mask are found over every mask. The lowest point a
mask leaves uncovered must be on some line, so only the lines through it
need trying: alone, or through it and one other point, the line then
taking every point collinear with the two, tested by a cross product.
O(2^n n^2).

## Approaches

| file | mechanism |
|---|---|
| `lines.kara` ★ | forwards over every mask in order, from the lowest uncovered point, found by a `while` over the mask's bits; the fewest lines kept in a `Vec.filled` |
| `lines_memo.kara` | top down over the points still left, a mask remembered in a `Map[i64, i64]` behind a `mut ref`; the lowest point by `trailing_zeros`, the line taking the points left on it away by `^=` |
| `lines_bfs.kara` | breadth first over the covered masks, one line a step, every pair's line found once up front; a `VecDeque` of (mask, lines) under `while let`, the lowest uncovered point by `(~mask).trailing_zeros()` |
| `lines_struct.kara` | a `struct Point` that knows whether it lies `on` the line through two others (`ref self`), and a `struct Cover` holding the points and the fewest lines for each mask, which `extend`s a mask and `reach`es the masks after it (`mut ref self`) |
| `lines_set.kara` | the distinct lines first, each pair's line as a mask made by `filter` and `fold`, the copies dropped by a `Set[i64]`, every single point's own line added; then every line tried from every mask, no lowest point singled out |
| `lines_solution.kara` | LeetCode's Rust template: `vec![i32::MAX; 1 << n]`, `usize` masks, `||`, the lowest uncovered point by `(0..n).find(|&k| ..).unwrap()`, tuple-bound differences; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one point, two points, the corners of a square, and a 3 by 3 grid),
each with its lines; then the total and a checksum over 2000 random sets
of 1 to 8 points, in -2 to 2 and in -100 to 100 in turn; then the
constraints' largest, 10 points: all on one slanted line, on two
crossing lines, and at random in the whole range. `lines.py` mirrors the
★ arm and its output is byte-identical.

No compiler gap was met. Two arms were first written with a slip that
`karac fix` mends: the breadth-first arm with Rust's `!mask` for the
complement, which Kāra spells `~`, and the struct's `Cover.new` handing
its borrowed `points` into the struct it returns, which the fix makes an
`own` parameter. `karac fix` carries the template in two rounds of 17
and 3 edits: Rust's spellings (`<..>` to `[..]`, `i32::MAX` to
`i32.MAX`, `||` to `or`, the `|&k|` and `|&v|` patterns to bare ones,
`struct Solution;` to `struct Solution {}`, the adapter's `&Vec` to `ref
Vec`, `Solution::` to `.`); then `vec![i32.MAX; 1 << n]` to
`Vec.filled(1 << n, i32.MAX)`, the adapter's `as i64` dropped, since an
`i32` widens on return, and the `ref` dropped from the adapter's
parameter, which borrows already. The `usize` masks and the `1usize <<
n` range stay.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the points are split into groups in every way there is, each
point joining a group already begun or starting one, and a split counts
when every group lies on one line, three points at a time; the fewest
groups of any split is the answer, since a line can be given the points
it covers and a group on one line is covered by it. No mask is formed.
It checks 300 random sets of 1 to 7 points in -2 to 2 or -6 to 6 in
turn; then 30 with every point but one on one line; then 30 on two
lines. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the fewest lines are the statement read literally |
| P2 | the points in reverse order: the same |
| P3 | every point moved by (7, -3): the same |
| P4 | every point turned a quarter round the origin: the same |
| P5 | every point sheared, (x, y) to (x + 2y, y): the same |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 sets: checksum 600809188, 12960 checks over
6 arms: 0 failures` under every lane in Verification; the checksum of
the literal answers was checked against a Python reading of the same
sets by the distinct lines and every mask. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, five to six to each arm, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each arm but the distinct-lines arm, which keeps two. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a point on one side taken as on the line | P1 260, P2 43, P6 260 |
| M3 | ★: the next point never paired | P1 61, P2 1, P6 61 |
| M4 | ★: the cross product's last difference taken from the second point | P1 243, P2 2, P4 1, P5 90, P6 243 |
| M8 | memo: the collinear test's last difference from the second point | P1 235, P2 34, P4 42, P5 107, P6 235 |
| M10 | memo: the answer remembered for the wrong points | P1 6, P2 4, P6 6 |
| M11 | memo: the highest point taken first | P1 321, P6 321 |
| M12 | bfs: one line too many | P1 360, P6 360 |
| M14 | bfs: the lines that miss the point taken | P1 216, P2 51, P6 216 |
| M16 | bfs: a pair's line missing its second point | P1 321, P2 12, P6 321 |
| M17 | struct: the line's test taken from its second point | P1 242, P4 1, P5 88, P6 242 |
| M19 | struct: no point alone | P1 39, P6 39 |
| M21 | struct: only the lower half of the masks extended | P1 15, P2 5, P6 15 |
| M24 | set: the first point never on a pair's line | P1 216, P2 48, P6 216 |
| M26 | set: the next point never paired | P1 61, P6 61 |
| M27 | solution: the template's lines missing the points before the second | P1 321, P2 11, P6 321 |
| M29 | solution: the template's lowest covered point taken | P1 190, P2 80, P6 190 |
| M30 | solution: the adapter halving every coordinate | P1 122, P2 66, P3 111, P5 83, P6 122 |

P1 and P6 kill all seventeen, P2 twelve, P5 four, P4 three and P3 one.
The four other properties all keep the answer as it is, and three of
them move the points in ways that keep every line a line, so a wrong
edit that reads every point alike gives the same wrong count after the
move and passes them; the edits are told apart mostly by how many sets
they get wrong and by P2. P2 lists the points from the other end, which sees an edit tied
to which point comes first or next (M1, M3, M4, M8, M10, M14, M16, M21,
M24, M27, M29, M30). P4 and P5 turn and shear the plane, which change
the coordinates a broken collinear test reads while keeping which points
are collinear (M4, M8, M17); P3 and P5 also see the adapter's
halving (M30), since moving or shearing the points changes
which of them the halving runs together.

Of the thirty-one, fourteen were not kept. Six are equivalent: the ★
arm extending masks no line reaches, which only offers counts above the
best; the memo arm drawing a line through a point already covered,
which is still a line; the breadth-first arm with no point alone, which
a line through the point and any other replaces whenever there are two
points, and its fallback answers for one; the struct taking a tie as
better and the distinct-lines arm trying a line that adds nothing, which
both leave every count as it was; and the adapter swapping x and y,
which is a reflection. Two fail by a crash: the ★ arm looking for the
lowest uncovered point from the second, which runs past the end, and the
breadth-first arm taking the lowest covered point, whose shift runs out
of range. Six fail as a kept one does: the ★ arm, the distinct-lines arm
and the template with no point alone, as M19; and the memo arm needing
a line with no points left, the struct reading the best one mask short,
and the distinct-lines arm counting each line twice, as M12.

## Verification

Every arm prints the same output as `lines.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.5 s to 2.7 s and the
differential 3.5 s.

## Benchmarks

The bench builds 4 sets of 10 points on a 7 by 7 grid once, so that
many fall on shared lines; then solves every set 2500 times, one point
moved to a free place of the grid before each so that no solve repeats
one before, with the ★ arm in all five languages. Every implementation
prints `10000 solves: 40854 lines in all, checksum 793136012`.

BENCHTAB
