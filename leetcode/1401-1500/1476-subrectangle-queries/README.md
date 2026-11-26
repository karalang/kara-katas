# 1476. Subrectangle Queries

Implement the class `SubrectangleQueries` which receives a `rows x cols`
rectangle as a matrix of integers in the constructor and supports two
methods:

1. `updateSubrectangle(int row1, int col1, int row2, int col2, int
newValue)` updates all values with `newValue` in the subrectangle whose
upper left coordinate is `(row1,col1)` and bottom right coordinate is
`(row2,col2)`. 2. `getValue(int row, int col)` returns the current value
of the coordinate `(row,col)` from the rectangle.

```
["SubrectangleQueries","getValue","updateSubrectangle","getValue","getValue","updateSubrectangle","getValue","getValue"]
[[[[1,2,1],[4,3,4],[3,2,1],[1,1,1]]],[0,2],[0,0,3,2,5],[0,2],[3,1],[3,0,3,2,10],[3,1],[0,2]]
  ->  [null,1,null,5,5,null,10,5]
["SubrectangleQueries","getValue","updateSubrectangle","getValue","getValue","updateSubrectangle","getValue"]
[[[[1,1,1],[2,2,2],[3,3,3]]],[0,0],[0,0,2,2,100],[0,0],[2,2],[1,1,2,2,20],[2,2]]
  ->  [null,1,null,100,100,null,20]
```

**Constraints:** there will be at most `500` operations considering both
methods; `1 <= rows, cols <= 100`, `rows == rectangle.length`, `cols ==
rectangle[i].length`, `0 <= row1 <= row2 < rows`, `0 <= col1 <= col2 <
cols`, `1 <= newValue, rectangle[i][j] <= 10^9`, `0 <= row < rows` and
`0 <= col < cols`.

The arms are `struct SubrectangleQueries` with `fn new(rectangle: own
Vec[Vec[i32]])`, `fn update_subrectangle(mut ref self, row1: i32, col1:
i32, row2: i32, col2: i32, new_value: i32)` and `fn get_value(self, row:
i32, col: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `subrectangle_queries.kara` ★ | the grid kept as given, each update writing its value into every cell of the subrectangle, `self.rect[r][c] = new_value`. O(area) an update, O(1) a read |
| `subrectangle_queries_log.kara` | the grid never written: each update pushed to a log, and a read walking the log from the newest back, the first update whose subrectangle holds the cell giving its value, else the grid's own. O(1) an update, O(updates) a read |
| `subrectangle_queries_fill.kara` | each row of the subrectangle written as a span, `self.rect[r][col1..=col2].fill(new_value)`, a mutating method on a range view of a list inside a field. O(area) an update |
| `subrectangle_queries_flat.kara` | the grid laid out row after row in one flat `Vec[i32]`, made by `flat_map`, the cell at row `r` and column `c` at `r * cols + c`. O(area) an update |
| `subrectangle_queries_solution.kara` | a Rust solution as LeetCode's Rust users write it (`&mut self`, `Vec<Vec<i32>>`, `row1 as usize..=row2 as usize`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 5 lines: LeetCode's two examples; the edges,
one cell updated twice, from 7 to 10^9 to 1, one row and one column with
cells inside them updated; the constraints' most, a 100 by 100 grid and
500 calls, an update and a read in turn (`100 by 100, 500 calls: values
sum 104455261814`); and 2000 random grids of 1 to 10 rows and columns, 1
to 60 calls, an update one time in three, values from 1 to top, top from
1 to 10^9, each value read folded into a checksum (`2000 random grids:
40115 reads, checksum 704168694`). `subrectangle_queries.py` mirrors the
★ arm, and its output is byte-identical. Every arm gives the same output
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★, log, fill and flat arms check clean as first
written. The Rust solution takes one round of 9 fixes by `karac fix`'s
count, and its diff is: each `Vec<Vec<i32>>` to `Vec[Vec[i32]]`, the
constructor's parameter to `own`, since it is kept in the struct, `&mut
self` to `mut ref self` and `&self` to `self`. Rust's `as usize` casts
stay. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the grid as a `Map[(i32, i32), i32]` from each cell to its
value, an update setting every cell it names and a read looking its cell
up. LeetCode's examples, the edges, the constraints' most, and 1994
random grids, half of 1 to 4 rows and columns, 1 to 10 calls and values
from 1 to 5, so a value written is often one already there, and half of
1 to 10 rows and columns, 1 to 60 calls and values from 1 to top, top
from 1 to 10^9. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | each read is the cell's first value or the value of an earlier update over the cell |
| P3 | the grid turned on its side, rows for columns, and every call with it, reads the same |
| P4 | 7 more on every value, the grid's and each update's, reads 7 more |
| P5 | the grid read whole after the first half of the calls, made anew and given the rest, reads as the whole run does |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 cases: checksum 536377587,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, keeping each
cell in a dict, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: an update's last row left as it was | P1 1187, P3 998, P6 4748 |
| M2 | ★: an update's first column left as it was | P1 1177, P3 1006, P6 4708 |
| M3 | log: the oldest update over a cell wins | P1 891, P5 756, P6 891 |
| M4 | log: an update's last column not counted as inside it | P1 1191, P3 998, P6 1191 |
| M5 | fill: each row's span stops short of its last column | P1 1191, P3 998, P6 1191 |
| M6 | fill: an update's first row left as it was | P1 1190, P3 1006, P6 1190 |
| M7 | flat: each row placed one column short of its start | P1 1048, P2 864, P3 1226, P6 1048 |
| M8 | flat: a read takes the first cell of its row | P1 1444, P2 1421, P3 1717, P6 1444 |
| M9 | solution: an update writes 1 less than its value | P1 1367, P2 1294, P6 1367 |
| M10 | solution: an update's last column left as it was | P1 1191, P3 998, P6 1191 |

## Benchmarks

The bench makes one 100 by 100 grid once; then makes 5000 passes of 250
updates with the ★ arm, each followed by a read, the subrectangles and
cells drawn from a seeded stream and each new value taken from the
checksum so far. The 1,250,000 updates write 828,509,932 cells, 663 an
update. The C mirror holds the grid as 100 `malloc`ed rows, Kāra and
Rust as a `Vec` of `Vec`s, and Go as a slice of slices. Every
implementation prints `5000 passes of 250 updates on 100 by 100:
checksum 841499486`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.60 s against Rust's 0.79 s (0.78 s with
overflow checks on), C's 0.21 s and Go's 1.3 s; Python takes 16.9 s.
