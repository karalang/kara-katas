# 1643. Kth Smallest Instructions

Bob is standing at cell `(0, 0)`, and he wants to reach `destination`:
`(row, column)`. He can only travel **right** and **down**. You are going
to help Bob by providing **instructions** for him to reach `destination`.

The **instructions** are represented as a string, where each character is
either:

- `'H'`, meaning move horizontally (go **right**), or
- `'V'`, meaning move vertically (go **down**).

Multiple **instructions** will lead Bob to `destination`. For example, if
`destination` is `(2, 3)`, both `"HHHVV"` and `"HVHVH"` are valid
**instructions**.

However, Bob is very picky. Bob has a lucky number `k`, and he wants the
`k`th **lexicographically smallest instructions** that will lead him to
`destination`. `k` is **1-indexed**.

*Given an integer array `destination` and an integer `k`, return the `k`th
**lexicographically smallest instructions** that will take Bob to
`destination`.*

```
destination = [2,3], k = 1  ->  "HHHVV"
destination = [2,3], k = 2  ->  "HHVHV"
destination = [2,3], k = 3  ->  "HHVVH"
```

**Constraints:** `destination.length == 2`; `1 <= row, column <= 15`;
`1 <= k <= nCr(row + column, row)`.

## Approaches

| file | mechanism |
|---|---|
| `kth.kara` ★ | `'H'` sorts first, so the paths that start with it come first, `C(h - 1 + v, v)` of them for `h` moves right and `v` down left. If k is among them the next move is `'H'`; otherwise `'V'`, and k skips past them. The binomials come from Pascal's triangle. O((r + c)^2) |
| `kth_grid.kara` | a table of the paths from every cell to the destination, filled back from it; the walk from `(0, 0)` reads the paths that go right first off the cell to the right. O(r c) |
| `kth_recursive.kara` | recursive: `'H'` and the k-th path of the rest, or `'V'` and the rest past them, and all of the other move once one runs out (`"V".repeat(v)`); the binomial by the multiplicative formula. O((r + c)^2) |
| `kth_solution.kara` | LeetCode's Rust template: a 31 by 31 Pascal's triangle of `i32` and a loop while both moves remain, the leftover pushed with `repeat`. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's three examples, the last
path of the smallest grid (`VH`), the last of the largest, `k =
155117520` on `[15, 15]`, and the first of a single row down; then the
moves right before the first move down summed, and a checksum over every
letter, for 3000 random destinations up to 3 by 3, 3000 up to 15 by 15,
and 100000 up to 15 by 15, each with a k drawn from all of its paths.
`kth.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every string of `row + column` moves is a bit mask read from
the top bit down, `'H'` a 0 and `'V'` a 1, so the masks count up in
lexicographic order, and the k-th mask with `row` ones is the answer. It
checks 3000 random destinations of 1 to 5 rows and columns: every fourth
k the first path, every fourth the last, the rest random. Every case is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer moves right `column` times and down `row` times |
| P3 | the path for k + 1, when there is one, sorts after the path for k |
| P4 | `'H'` and `'V'` swapped, the answer is the (total + 1 - k)-th path to `[column, row]` |
| P5 | each arm agrees with at least two of the other three |

P4 holds because swapping the letters turns the paths to `[row, column]`
into the paths to `[column, row]` and reverses their order.

The differential prints `3000 problems: checksum 946904506, 60000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. The ★ arm's three walk off the edge of
Pascal's triangle once a wrong count spends a move that is not there, and
stop with `index out of bounds` on both backends before any property is
checked. No mutant breaks P2: every arm's loop makes exactly
`row + column` moves, and the wrong ones only reorder them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: k equal to the paths starting with `'H'` taken as past them | index out of bounds |
| M2 | ★: k not reduced after a `'V'` | index out of bounds |
| M3 | ★: the count of paths starting with `'H'` read as `C(h + v - 1, h)` | index out of bounds |
| M4 | grid: a cell's paths summed from below and diagonally below | P1 635, P3 486, P4 897, P5 635 |
| M5 | grid: a `'V'` skips the paths from the cell below, not the cell to the right | P1 1107, P3 685, P4 1571, P5 1107 |
| M6 | recursive: the binomial one row too far down the triangle | P1 2062, P3 1489, P4 3000, P5 2062 |
| M7 | recursive: k not reduced after a `'V'` | P1 929, P3 929, P4 1145, P5 929 |
| M8 | template: the loop stops with one `'V'` left | P1 1511, P3 928, P4 3000, P5 1511 |
| M9 | template: the triangle's diagonal left 0 | P1 2083, P3 953, P4 3000, P5 2083 |
| M10 | template: a `'V'` skips one path too few | P1 929, P3 571, P4 1145, P5 929 |

## Benchmarks

The bench draws 1000000 random destinations of 1 to 15 rows and columns,
each with a k drawn from all of its paths, all of them first, then walks
each by the ★ arm in all five languages, the triangle and the path
allocated per call in each. Every implementation prints `1000000
destinations of up to 15 by 15: first moves down sum to 1267419, checksum
218548706`. The C build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

TIMINGS

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. PARNOTE

## Verification

All four arms print the same output as `kth.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `SHA`.

## Writing it

The ★ and grid arms first declared their pairs Rust's way, `let (mut v,
mut h) = ..`, and `karac fix` moved the `mut` before the pattern. The
recursive arm passed `destination[1] as i64` to an `i64` parameter, and
the `lossless_cast` lint dropped all three casts. `path.find("V")` and
`"V".repeat(v)` were written as in Rust and needed nothing.

LeetCode's Rust template takes one `karac fix` of 14 edits: `struct
Solution;` to `struct Solution {}`, `Vec<i32>` to `Vec[i32]`, the `mut`
pair, both `as usize` to `as i64`, `vec![vec![0i32; 31]; 31]` to
`Vec.filled(31, Vec.filled(31, 0i32))`, `String::new` to `String.new`,
`&&` to `and`, and the `&` dropped from both `push_str(&"H".repeat(h))`.
The arm then checks and agrees with no hand edit.
