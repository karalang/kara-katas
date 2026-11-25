# 1380. Lucky Numbers in a Matrix

Given an `m x n` matrix of distinct numbers, return all lucky numbers in
the matrix in any order.

A lucky number is an element of the matrix such that it is the minimum
element in its row and maximum in its column.

```
matrix = [[3,7,8],[9,11,13],[15,16,17]]           ->  [15]
matrix = [[1,10,4,2],[9,3,8,7],[15,16,17,12]]     ->  [12]
matrix = [[7,8],[1,2]]                            ->  [7]
```

**Constraints:** `m == mat.length`, `n == mat[i].length`, `1 <= n, m <=
50`, `1 <= matrix[i][j] <= 10^5`, and all elements in the matrix are
distinct.

Each arm is `fn lucky_numbers(matrix: Vec[Vec[i32]]) -> Vec[i32]`.

## Approaches

| file | mechanism |
|---|---|
| `lucky_numbers.kara` ★ | each row's least value and each column's greatest found in one pass, then every cell that is both. O(mn) |
| `lucky_numbers_maxmin.kara` | the greatest of the rows' least values against the least of the columns' greatest: the first is never more than the second, and with the values all different they meet exactly at the one lucky number there can be. O(mn) |
| `lucky_numbers_brute.kara` | every cell tried in turn: lucky when nothing in its row is less and nothing in its column greater. O(mn(m + n)) |
| `lucky_numbers_sets.kara` | the rows' least values gathered in a `Set`, then each column's greatest looked up in it. O(mn) |
| `lucky_numbers_solution.kara` | a Rust solution as LeetCode's Rust users write it (`*r.iter().min().unwrap()` for each row's least, `matrix.iter().map(\|r\| r[j]).max().unwrap()` for each column's greatest, `let mut ans = vec![];`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, and 50 by
50, the constraints' most, with the values rising along each row and
down each column, so the bottom left corner is lucky, and with each row
the one above shifted one place left, so no cell is (`[15] [12] [7]
[2451] []`); and 2000 random matrices of 1 to 50 rows and columns
holding different values up to 10^5, half placed at random and half with
a lucky number planted at a random cell, the least values given to the
rest of its column and the greatest to the rest of its row (`2000 random
matrices: 1055 lucky numbers, checksum 91237484`). `lucky_numbers.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. The `Set` arm only looks values up, never walks
the set, so its order cannot reach the output.

The Mend loop: the four Kāra arms check clean as first written. The Rust
solution takes one round of 18 fixes by `karac fix`'s count, from 9
errors: `struct Solution;` to `struct Solution {}`, each `Vec<..>` to
`Vec[..]`, `vec![]` to `Vec.new()`, `&&` to `and`, and `Solution::` to
`Solution.`. The `*` of `*r.iter().min().unwrap()` stays: `min()` gives
a view of the row's element, and `*` reads it. Its output matches on the
first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for each cell, its row and its column sorted, the cell lucky
when it is the first of its row and the last of its column. Each arm's
answer is sorted before it is compared, since any order is an answer.
LeetCode's three examples and 2000 matrices of 1 to 6 rows and columns
holding different values from 1 to 60, half at random and half with a
lucky number planted as above, each with an order for its rows and one
for its columns. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | turned over and negated, a row's least becoming a column's greatest: the lucky numbers negated |
| P3 | the rows and the columns shuffled: the same |
| P4 | at most one, the values being different |
| P5 | a row of values greater than all added: its least alone |
| P6 | the ★ arm's answer |

All 60,090 checks pass on every arm: `2003 cases: checksum 601732668,
60090 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, reading each row
and column the same way, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each row's greatest kept, not its least | P1 1467, P2 1467, P5 2003, P6 5868 |
| M2 | ★: every row's least answered, its column not asked | P1 1688, P2 1671, P4 1688, P5 2003, P6 6752 |
| M3 | maxmin: an answer whenever the greatest row least is at most the least column greatest | P1 536, P2 536, P6 536 |
| M4 | maxmin: the rows' greatest values taken, not their least | P1 1135, P2 1152, P5 1671, P6 1135 |
| M5 | brute: nothing in the row may be equal, the cell itself included | P1 1467, P2 1467, P5 2003, P6 1467 |
| M6 | brute: the greatest of its row asked, not of its column | P1 1410, P2 1410, P4 275, P5 2003, P6 1410 |
| M7 | sets: the columns' greatest that are not a row's least | P1 2003, P2 2003, P4 1396, P5 2003, P6 2003 |
| M8 | sets: the columns' least looked up, not their greatest | P1 1688, P2 1671, P4 540, P5 2003, P6 1688 |
| M9 | solution: least in its row or greatest in its column | P1 1946, P2 1946, P4 1946, P5 2003, P6 1946 |
| M10 | solution: the last column never looked at | P1 670, P2 669, P3 442, P5 332, P6 670 |

P1, P2 and P6 kill all ten, P5 nine, P4 five and P3 one. Turning the
matrix over and negating it (P2) swaps the roles of rows and columns,
and every edit here treats the two differently. A row of values greater
than all (P5) makes its least the one lucky number, and catches every
edit but the one that answers whenever the greatest row least is at most
the least column greatest (M3): the added row makes the two equal, which
the edit and the true arm both answer. At most one (P4) catches the
edits that can answer several: every row's least (M2), the cells least
and greatest in their own row, which every cell of a one-column matrix
is (M6), the columns' greatest that are no row's least (M7), the
columns' least that are (M8), and either one (M9). Shuffling (P3)
catches only the edit that looks at a place rather than a value, the
last column left out (M10). The two edits that lose every answer or make
the wrong cells lucky in the same cases, the rows' greatest (M1) and a
cell never equal to itself (M5), fail as many checks but in different
arms.

## Benchmarks

The bench builds 20 matrices of 50 by 50, the constraints' most, once:
the values 1 to 2500 rising along each row and down each column, then
300 random swaps of two cells. Then 20,000 rounds, each swapping two
cells of one matrix, all drawn from the checksum so far, and finding
that matrix's lucky numbers with the ★ arm. Every implementation prints
`20000 rounds over 20 matrices of 50 by 50: checksum 232616725`. The
work is one pass over the 2500 cells for the rows' least and the
columns' greatest and one to collect, a round. The Rust function takes
`&[Vec<i32>]`, as the Kāra one borrows its `Vec`; C keeps fixed 50 by 50
arrays.

BENCHTAB
