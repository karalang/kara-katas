# 1267. Count Servers that Communicate

You are given a map of a server center, represented as an `m * n` integer
matrix `grid`, where 1 means that on that cell there is a server and 0
means that it is no server. Two servers are said to communicate if they
are on the same row or on the same column.

Return the number of servers that communicate with any other server.

```
grid = [[1,0],[0,1]]                                ->  0
grid = [[1,0],[1,1]]                                ->  3
grid = [[1,1,0,0],[0,0,1,0],[0,0,1,0],[0,0,0,1]]    ->  4
```

**Constraints:** `m == grid.length`; `n == grid[i].length`; `1 <= m <=
250`; `1 <= n <= 250`; `grid[i][j] == 0 or 1`.

The arms are `fn count_servers(grid: Vec[Vec[i64]]) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `count_servers.kara` ★ | by counting: the servers in each row and each column counted, then a server communicates when its row or its column holds another. O(mn) |
| `count_servers_scan.kara` | by scanning: for each server, its row and its column searched by `any` for another. O(mn(m + n)) |
| `count_servers_union.kara` | by union-find: rows and columns are the members, each server joins its row to its column, and the servers of every set holding more than one are counted. O(mn α) |
| `count_servers_lists.kara` | by rows: the column counts folded once, then each row's servers listed; a row of two or more counts them all, and a row of one counts it when its column holds another |
| `count_servers_solution.kara` | a Rust solution as LeetCode's Rust users write it (`Vec<Vec<i32>>`, `vec![0; m]`, `iter().enumerate()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples (`0 3 4`);
2000 random grids of 1 to 12 by 1 to 12, a cell a server one time in 2 to
9 (`2000 random grids: 18105 servers communicate, checksum 592257026`);
and the constraints' top, 250 by 250 full, its diagonal, and a server one
time in 30 (`62500 0 2100`). `count_servers.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, scan and union arms checked clean as first written.
The lists arm's fold closure was first written `|mut acc, row|`, Rust's
spelling; `karac fix` rewrote it to a plain `acc` and a `let mut acc =
acc;`. The solution arm takes one round of fixes, 15 by `karac fix`'s
count: `Vec<..>` to brackets, `vec![0; m]` to `Vec.filled(m, 0)`, the
pattern `&cell` to `cell`, `&&` and `||` to `and` and `or`, `struct
Solution;` to `struct Solution {}`, `::` to `.`, the closure's `|&x|` to
`|x|`, and the wrapper's `as i64`, a lossless widening, removed. No gap
was met.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every server listed, and a server counted when some other
server shares its row or its column. 2000 random grids of 1 to 7 by 1 to
7, a cell a server one time in 2 to 6.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the grid transposed gives the same count |
| P3 | the grid turned half a circle gives the same count |
| P4 | an empty row and an empty column added give the same count |
| P5 | a server added never lowers the count |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 grids: checksum 469722111,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the same
checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a server counted when its row and its column both hold another | P1 1271, P6 5084 |
| S2 | ★: each server counted in column `r % n`, not its own | P1 552, P2 682, P3 336, P4 218, P6 2208 |
| C1 | scan: the row search finds the server itself | P1 777, P6 777 |
| C2 | scan: the column search reads column `r % n` | P1 435, P2 529, P3 326, P4 286, P6 435 |
| U1 | union: a server joins its row to row `c`, not to column `c` | P1 258, P3 197, P6 258 |
| U2 | union: a set of one server counted | P1 777, P6 777 |
| R1 | lists: a row's lone server never counted | P1 869, P2 1057, P6 869 |
| R2 | lists: a row of two or more counts one fewer | P1 1086, P2 885, P6 1086 |
| O1 | solution: each server counted twice in its row | P1 777, P6 777 |
| O2 | solution: a column of one counts as shared | P1 777, P6 777 |

All ten are caught, every one by P1, the statement read literally. Four
edits (C1, U2, O1, O2) count every server, and fail on the same 777 grids:
those that hold a server alone in its row and its column. S2 and C2, which
read a column by the row's index, fail every symmetry property. P2, the
transpose, also catches the lists arm's two, which treat a row apart from
a column, and P3, the half turn, also catches U1, which files columns
among the rows. P5, monotonicity, catches none: every edit here counts no
fewer servers when one is added, as the statement does.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (the servers in each row and each column counted, then each server
that shares its row or column with another counted) on 100 random
100-by-100 grids built once, a cell a server one time in 2 to 9, 300
rounds; every answer folded into a checksum. Every program prints `300
rounds of 100 grids of 100 by 100: checksum 553332275`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 2.296 to 2.429 s | 2.360 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 2.309 to 2.487 s | 2.372 s |
| Rust (`rustc -O`) | 2.340 to 2.446 s | 2.372 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.293 to 2.401 s | 2.352 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 2.291 to 2.420 s | 2.334 s |
| C (`clang -O3`) | 1.859 to 1.942 s | 1.903 s |
| C (`clang -O3 -march=x86-64-v3`) | 1.826 to 1.906 s | 1.857 s |
| Go | 2.387 to 2.509 s | 2.446 s |
| Python | 30.21 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (2.352 s
against 2.372 s), and the two ranges overlap. C is about 20% ahead of
Kāra (1.903 s against 2.372 s); Go runs level with Kāra (2.446 s against
2.372 s). Python takes about 13x Kāra's time. No profile was taken.
