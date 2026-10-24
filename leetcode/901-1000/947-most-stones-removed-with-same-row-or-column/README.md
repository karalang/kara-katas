# 947. Most Stones Removed with Same Row or Column

On a 2D plane, we place `n` stones at some integer coordinate points.
Each coordinate point may have at most one stone.

A stone can be removed if it shares either **the same row or the same
column** as another stone that has not been removed.

Given an array `stones` of length `n` where `stones[i] = [xi, yi]`
represents the location of the `i`-th stone, return *the largest
possible number of stones that can be removed*.

```
stones = [[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]]  ->  5
stones = [[0,0],[0,2],[1,1],[2,0],[2,2]]        ->  3
stones = [[0,0]]                                ->  0
```

**Constraints:** `1 <= stones.length <= 1000`; `0 <= xi, yi <= 10^4`;
no two stones are at the same coordinate point.

## Approaches

Stones that share a row or a column, directly or through other stones,
form a group, and a group can always be removed down to its last stone:
take its stones off a spanning tree leaf first, each still sharing a line
with the stone it hangs from. No group can lose its last stone, so the
answer is the number of stones less the number of groups. Every arm
counts the groups.

| file | mechanism |
|---|---|
| `remove_stones.kara` ★ | the rows and columns are what is joined: each stone joins its row to its column in a union-find over the 10,001 rows and 10,001 columns, a group counted for each line seen for the first time and one taken away for each join of two groups. O(n α(n)) after O(20002) set-up |
| `remove_stones_dfs.kara` | the stones as a graph, two joined when they share a row or a column, and its groups counted by a search from each stone not yet reached, every stone compared with every other, on an explicit stack. O(n^2) time, O(n) space |
| `remove_stones_lines.kara` | the stones listed by row and by column in two maps, and each group found breadth first: a stone taken off the queue hands on every stone of its row and its column, and each line's list, once handed on, is taken out of its map so that it is never walked again. O(n) time and space |
| `remove_stones_labels.kara` | every stone labelled with its own index, and in each pass every row and column taking the least label among its stones and every stone the least of its row's and its column's; when a pass changes nothing each group carries its least index, and the groups are the stones still holding their own. O(n d) for the longest path of lines `d` in a group |
| `remove_stones_sorted.kara` | the stones sorted by row, each joined in a union-find over the stones to the one before it when they share the row, then the same by column; every join that brings two groups together is one stone that can go, so the answer is the count of those joins. Each stone is kept with its index as one number, `line * 65536 + index`, so that sorting the numbers sorts the stones. O(n log n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's three examples and five
more (two stones in a row, a diagonal, a chain through rows and columns
in turn, three stones at the largest coordinates, and two groups); for
300 random sets of 1 to 40 stones at distinct points of grids of 1 to 25
by 1 to 25, the stones, how many are removed and a checksum; and five of
LeetCode's largest, 1,000 stones: at random points up to 10,000, at
random points up to 999, in a staircase that is one group 1,000 stones
long, on a diagonal where no two share a line, and in 25 rows of 40.
`remove_stones.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: from the stones still there, any stone that shares a row or a
column with another of them may be removed, and the most stones some
order of removals takes away is searched over every set of stones left,
each kept as a mask and worked out once. It checks 3,200 random sets of
stones at distinct points: 3,000 of up to 7 stones on grids up to 4 by 4,
against the statement, and 200 of up to 300 stones on grids up to 600 by
600, against the other properties; 38,982 stones, 24,988 removed.

| | property |
|---|---|
| P1 | the statement's most removals, on the small sets |
| P2 | at least the stones less the fewer of the rows and the columns used, at most one less than the stones, and 0 exactly when no two stones share a row or a column |
| P3 | the stones in a random order, each turned a quarter, `[x, y]` to `[10000 - y, x]`, give the same answer |
| P4 | the stones beside a copy of themselves moved past every row and column used give twice the answer |
| P5 | one more stone at a random free point gives 0, 1 or 2 more, and 0 exactly when it shares no row or column with another stone |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 sets of 38982 stones, 24988 removed, checksum 557278249,
95000 checks over 5 arms: 0 failures` under `karac __mir-run` (25 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a row seen for the first time not counted | P1 3000, P2 3200, P3 2014, P5 777, P6 3200 |
| M2 | ★: rows and columns numbered alike | P1 202, P2 61, P3 376, P4 2030, P5 465, P6 376 |
| M3 | ★: the columns numbered from 10000 | P3 150 |
| M4 | dfs: a column compared with a row | P1 1004, P2 616, P3 2113, P4 1641, P5 879, P6 1181 |
| M5 | dfs: only the first stone searched from | P1 954, P3 322, P5 550, P6 1121 |
| M6 | dfs: every stone a group | P1 2282, P2 2472, P5 2423, P6 2472 |
| M7 | lines: a column's first stone never listed | P1 177, P3 389, P5 1, P6 324 |
| M8 | lines: a row handed on but never searched | P1 395, P3 490, P5 368, P6 554 |
| M9 | lines: the column looked up by the row | P1 896, P2 518, P3 2087, P4 1381, P5 716, P6 1075 |
| M10 | labels: the group of stone 0 counted | P1 2308, P2 2263, P3 185, P4 3200, P5 3021, P6 2506 |
| M11 | labels: a column's last label taken | P1 1367, P2 890, P3 2105, P5 1114, P6 1547 |
| M12 | labels: the labels starting backwards | P1 288, P2 274, P3 217, P4 2940, P5 876, P6 477 |
| M13 | sorted: each stone compared with the first | P1 1073, P2 919, P3 752, P4 2215, P5 1132, P6 1262 |
| M14 | sorted: the first pair skipped | P1 1879, P2 1250, P3 634, P4 1978, P5 780, P6 1978 |
| M15 | sorted: the rows never sorted | P1 563, P2 164, P3 793, P5 490, P6 749 |

P1, P3, P5 and P6 kill fourteen each, P2 eleven and P4 seven.

M3 numbers the columns from 10,000 rather than 10,001, so column 0 and
row 10,000 are the same line. No random set uses a row that high, so
P1, P2, P4, P5 and P6 never see it; P3's quarter turn puts every stone
with `y = 0` on row 10,000, and P3 alone kills it.

M6 counts every stone as a group and so always answers 0. Turned, the
stones still give 0, and a copy beside them gives twice 0, so P3 and P4
miss it.

P2 misses M5, M7 and M8, which find too many groups. M5 searches only
from each group's first stone, marking that stone's own row and column
and no further, so every stone it starts from has a row and a column no
earlier one used; its count stays within the fewer of the rows and the
columns, and two stones on one line still give a removal. That M7 and
M8, which lose stones of a line reached from a stone already found,
stay within the same bounds on these sets was seen, not proved.

P4 misses eight. M3 never meets row 10,000 in the copy and M6 answers 0.
M1, M5, M7, M8, M11 and M15 make their mistake inside each group, so the
copy, past every line the stones use, adds the same wrong count again
and the answer still doubles. The other seven are tied to something
that is not repeated in the copy: M2's rows and columns numbered alike
meet differently once the copy moves its rows and columns by different
amounts, M4 and M9 compare a row with a column, M10 counts the group
of stone 0, M12's labels and M13's first stone are numbered across the
whole set, and M14 skips the first pair once, not once in each copy.

Thirteen other edits were tried and set aside. Eight failed exactly the
same checks as each other, in three groups, so none of them was kept:
★ stopping each find after one step, ★ joining the row itself rather
than its root, and sorted counting every join, even inside a group;
dfs sharing only rows, labels never passing the columns on, and sorted
joining only rows; and dfs looking only at later stones and labels
making a single pass. Why the first and the last group agree was not
worked out. Four were sound but beyond three an arm (★ never taking a
join away, lines listing the rows by column and keeping only each row's
last stone, and sorted never sorting the columns). One crashed: sorted
packing each row by 256 rather than 65536, with an index out of bounds.

## Verification

Every arm prints the same output as `remove_stones.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 0.2 to 2.2 s each and the
differential 25 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The ★, dfs, labels and sorted arms print the same output under the
frozen legacy interpreter, the legacy JIT and both legacy builds, with
and without auto-par. Legacy refuses the lines arm and the differential
at `get_mut` on a `Map` ("no method 'get_mut' on type 'Map'"), and the
bench program at `remove_stones(sets[(r + i) % count])`, a move out of
an index ("cannot move ... out of an index"), which v2's borrowing
parameters make a borrow. Legacy is frozen, so none of this is filed.

## Benchmarks

The bench program builds 20 sets of 1,000 stones once, LeetCode's
largest, each at distinct random points of a square grid of side 200 to
2,000, so that the groups run from a few large ones to many small ones;
in each of 1,000 rounds it runs the ★ arm on every set, each round
starting from a different one, and folds the answers into a checksum.
Every implementation prints `1000 rounds over 20 sets of 1000 stones:
16340000 removed, checksum 736489918`. Each call allocates and fills the
20,002 lines' parents, as the ★ arm does.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.30 to 0.36 s | 0.32 s |
| Rust (`rustc -O`) | 0.32 to 0.37 s | 0.33 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.32 to 0.41 s | 0.34 s |
| Go | 1.22 to 1.47 s | 1.33 s |
| Python | 7.72 s | |
| Kāra (`karac build --mir`) | 0.36 to 0.38 s | 0.37 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about 24 times C's.

v2 takes 1.08 times Rust's median time under overflow checks and 1.15
times C's. Under valgrind's cachegrind v2 runs 4.40 billion
instructions and 3.56 billion branches with 23.8 million mispredicted,
Rust with overflow checks 4.19 billion, 3.53 billion and 23.6 million,
and C 3.94 billion, 3.34 billion and 22.6 million: the three do nearly
the same work, branch for branch. That Go's time, about four times the
others', is its garbage collector reclaiming the 20,000 slices of 160 KB
the calls allocate is inferred, not profiled.
