# 2267. Check if There Is a Valid Parentheses String Path

A parentheses string is a **non-empty** string consisting only of `'('`
and `')'`. It is **valid** if **any** of the following conditions is
**true**:

- It is `()`.
- It can be written as `AB` (`A` concatenated with `B`), where `A` and
  `B` are valid parentheses strings.
- It can be written as `(A)`, where `A` is a valid parentheses string.

You are given an `m x n` matrix of parentheses `grid`. A **valid
parentheses string path** in the grid is a path satisfying **all** of
the following conditions:

- The path starts from the upper left cell `(0, 0)`.
- The path ends at the bottom-right cell `(m - 1, n - 1)`.
- The path only ever moves **down** or **right**.
- The resulting parentheses string formed by the path is **valid**.

Return `true` *if there exists a **valid parentheses string path** in
the grid.* Otherwise, return `false`.

```
grid = [["(","(","("],[")","(",")"],["(","(",")"],["(","(",")"]]  ->  true
grid = [[")",")"],["(","("]]                                      ->  false
```

**Constraints:** `m == grid.length`; `n == grid[i].length`;
`1 <= m, n <= 100`; `grid[i][j]` is either `'('` or `')'`.

A string is valid when its balance, the number of brackets open, never
falls below 0 and ends at 0. So each cell needs only the set of
balances that some path to it can end with: the cell above's and the
cell to the left's, moved by its own bracket. A balance is at most
about half the path, which gives O(m n (m + n)).

## Approaches

| file | mechanism |
|---|---|
| `path.kara` ★ | a table `reach[i][j][b]` over the cells and balances, each cell taking `b - step` from above and from the left; the answer `reach[m - 1][n - 1][0]`, after the parity and both ends are checked |
| `path_bits.kara` | the balances as bits: a `u128` per cell, the masks above and to the left ORed, then shifted left for `(` and right for `)`, the right shift dropping a path that would go below 0; one row of masks kept; O(m n) |
| `path_dfs.kara` | a depth-first search right and down with a `Set[(i64, i64, i64)]` of states seen, giving up when the balance is below 0 or more than the cells left could close |
| `path_struct.kara` | `struct Sweep` of the lowest and highest balance per column; between them every balance of the same parity is reachable, so `next_row` (`mut ref self`) carries two numbers per cell, a dead cell holding `low = i64.MAX` and `high = -1`; O(m n) |
| `path_iter.kara` | a `fold` over the rows carrying the row above's `Set[i64]`s, each row a `scan` along its cells whose state is the set to the left, Kāra's `Some((next_state, item))` |
| `path_solution.kara` | LeetCode's Rust template: `Vec<Vec<char>>` in, `bool` out; `vec![vec![vec![false; max + 1]; n]; m]`, the previous balance `k as i32 - d` and `as usize` into the table; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and five
more (one cell, false; `()` in a row, true; `(` over `)`, true; a path
of odd length, false; `)` at the start, false), each with its answer;
then 2000 random grids of 1 to 8 rows and columns, `(` 50 or 60 times
in 100, with how many have a path (179) and a checksum; then three of
the constraints' largest, 100 by 99: random at 55 in 100 (false), a
checkerboard (true), and `(` above the anti-diagonal with `)` below
(true). `path.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one round, reporting 17 edits:
`Vec<Vec<char>>` to `Vec[Vec[char]]`, the `||` and `&&` to `or` and
`and`, the nested `vec![..; ..]` to `Vec.filled`, `prev as usize > max`
to `prev > max`, `prev as usize` to `prev as i64`, and `struct
Solution;` to `struct Solution {}`.

The bits arm fills its rows with `Vec.filled(n, 0)` into a `Vec[u128]`.
Under the compiled backend the literal reached the fill as an 8-byte
`i64` constant while the fill copied 16 bytes from it, so the high half
of every element after the first was whatever lay past the constant:
`karac __mir-llvm-run` answered the random 100 by 99 grid `true`, and
`karac __mir-llvm-asan` reported a stack-buffer-overflow, a read of 16
bytes from an 8-byte const. The interpreter was right. The fill is now
fitted to the element type in kara (B-2026-11-18-81), and the arm is as
it was first written.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every path from the top left to the bottom right, built move
by move, its string checked for a balance that never falls below 0 and
ends at 0. No table of balances. It checks 300 random grids of 1 to 6
rows and columns, `(` 50 or 60 times in 100; then 30 with every row the
same; then 30 planted with a valid path along the top row and down the
last column. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the grid transposed: the same answer |
| P3 | turned half round, every bracket swapped: the same answer |
| P4 | true only for an odd number of rows plus columns, `(` at the top left and `)` at the bottom right |
| P5 | a row of `(` put on top and a row of `)` below: still true when it was true |
| P6 | each arm agrees with at least three of the other five |

P3 holds because a path read backwards with every bracket swapped is
valid exactly when the path is. P5 holds because the new top row opens
`n` brackets that the new bottom row closes, and a valid path through
the old grid stays valid between them.

The differential prints `360 cases (64 with a path): checksum
285497008, 12960 checks over 6 arms: 0 failures` under every lane in
Verification; the checksum of the literal answers was checked against a
Python reading that tries every order of the `m - 1` downward and `n -
1` rightward moves with `itertools.combinations`. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the left cell read at the new balance | P1 36, P2 64, P6 36 |
| M2 | ★: only the cell above | P1 58, P2 15, P6 58 |
| M6 | ★: the left cell from the row above | P1 50, P2 32, P6 50 |
| M8 | bits: the shifts swapped | P1 88, P4 24, P5 24, P6 88 |
| M9 | bits: the answer at bit 1 | P1 122, P3 67, P4 58, P6 122 |
| M11 | bits: a close keeping the mask | P1 85, P3 58, P4 21, P5 21, P6 85 |
| M12 | dfs: the search from one open | P1 119, P3 67, P4 55, P6 119 |
| M15 | dfs: the state seen by the cell only | P1 3, P2 5, P3 2, P5 4, P6 3 |
| M16 | dfs: the cut one too tight | P1 64, P6 64 |
| M17 | struct: the low never raised from 0 | P1 19, P4 19, P6 19 |
| M20 | struct: the answer by the high | P1 37, P3 22, P5 6, P6 37 |
| M21 | struct: an open bracket raising the high by two | P1 1, P3 2, P6 1 |
| M22 | iter: the set above ignored | P1 55, P2 15, P5 9, P6 55 |
| M23 | iter: negative balances kept | P1 68, P4 67, P6 68 |
| M25 | iter: the answer any balance | P1 132, P3 186, P4 128, P6 132 |
| M27 | solution: the start not checked | P1 27, P3 61, P4 27, P5 5, P6 27 |
| M29 | solution: the cell above only off the first column | P1 10, P2 30, P3 19, P6 10 |

P1 and P6 kill all seventeen, P3 nine, P4 eight, P2 six, and P5 six.
P2 catches the edits that favour one direction: a neighbour missed,
read from the wrong place, or only off the first column. P3 catches the
edits that are wrong about where a balance starts or ends, which the
half turn swaps: the answer at the wrong bit, any balance accepted, the
start not checked. P4 catches the answers true where no path can be:
negative balances kept, a close that keeps the mask, a low that never
leaves 0. Every answer false for a grid with a path, the cut too tight,
fails P1 alone, as P5 only asks that a true answer stay true.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Thirteen fail as a kept one does: the bits arm's
left mask never joined, the dfs arm's only moves down, the struct arm's
left cell never read and its high from the minimum, and the iter arm's
scan state never moved (M7, M14, M18, M19, M24) as the ★ arm's only
the cell above (M2); the ★ arm's start at balance 0, its step the wrong
way and its answer at balance 1, the bits arm's row above never moved
on, the iter arm's step always up, and the template's step from `d`
and first cell open twice (M3, M4, M5, M10, M26, M30, M31) as the dfs
arm's cut one too tight (M16), every one of them false for every grid
with a path; and the dfs arm's cell seen at balance 0 never searched
again (M13) as its state seen by the cell only (M15). One fails in a
way of its own and is left out because its arm keeps enough: the
template's table read at `k` for the left cell (M28), which fails as
the ★ arm's M1 does.

Six edits of the first draft were replaced. Three were equivalent: the
★ arm's parity check dropped, since an odd path never ends at balance
0 anyway; the dfs arm's cut for too many open removed, which the end's
`open == 0` still decides; and the struct arm's dead cell kept, which a
later `min` and `max` absorb. Two crashed with an index out of bounds:
the ★ arm's balances capped two lower, and the template's `max` one
less. One anchor matched twice in the dfs arm. They are now M1, M12,
M13, M21, M27 and M29.

## Verification

Every arm prints the same output as `path.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the bits arm takes 0.3 s, the dfs and struct
arms 0.4 s, the differential 0.7 s, the ★ arm 1.5 s, the template 1.6
s, and the iter arm 2.0 s, which builds a new `Set` for every cell.

## Benchmarks

The bench answers 20 grids of the constraints' largest, 100 by 99, `(`
at 50 to 69 in 100 with the top left `(` and the bottom right `)`, with
the ★ arm in all five languages. Every implementation prints `20 grids
of 100 by 99: 18 with a path, checksum 597956381`. Each builds its grid
a cell at a time from the same generator and allocates the table per
call.

BENCHTAB
