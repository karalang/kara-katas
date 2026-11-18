# 2286. Booking Concert Tickets in Groups

A concert hall has `n` rows numbered from `0` to `n - 1`, each with `m`
seats, numbered from `0` to `m - 1`. You need to design a ticketing
system that can allocate seats in the following cases:

- If a group of `k` spectators can sit **together** in a row.
- If **every** member of a group of `k` spectators can get a seat. They
  may or **may not** sit together.

Note that the spectators are very picky. Hence:

- They will book seats **only** if each member of their group can get
  a seat with row number **less than or equal** to `maxRow`. `maxRow`
  can **vary** from group to group.
- In case there are multiple rows to choose from, the row with the
  **smallest** number is chosen. If there are multiple seats to choose
  in the same row, the seat with the **smallest** number is chosen.

Implement the `BookMyShow` class:

- `BookMyShow(int n, int m)` Initializes the object with `n` as number
  of rows and `m` as number of seats per row.
- `int[] gather(int k, int maxRow)` Returns an array of length `2`
  denoting the row and seat number (respectively) of the **first seat**
  being allocated to the `k` members of the group, who must sit
  **together**. In other words, it returns the smallest possible `r`
  and `c` such that all `[c, c + k - 1]` seats are valid and empty in
  row `r`, and `r <= maxRow`. Returns `[]` in case it is **not
  possible** to allocate seats to the group.
- `boolean scatter(int k, int maxRow)` Returns `true` if all `k`
  members of the group can be allocated seats in rows `0` to `maxRow`,
  who may or **may not** sit together. If the seats can be allocated,
  it allocates `k` members to the first available seats with the
  smallest row and seat number; otherwise returns `false`.

```
BookMyShow(2, 5); gather(4, 0); gather(2, 0); scatter(5, 1); scatter(5, 1)
  ->  [0, 0], [], true, false
```

**Constraints:** `1 <= n <= 5 * 10^4`; `1 <= m, k <= 10^9`;
`0 <= maxRow <= n - 1`; at most `5 * 10^4` calls in total to `gather`
and `scatter`.

Every booking takes the smallest free seats it can, so each row's free
seats are always one run at its end, and a row is described by its
count of free seats alone. A segment tree over the rows keeps each
range's largest count and its total: `gather` walks down to the
leftmost row with `k` free in O(log n) and answers if that row is at
most `maxRow`; `scatter` sums the free seats through `maxRow`, and if
there are enough, fills rows from the first one not full, each full row
paid for once.

## Approaches

| file | mechanism |
|---|---|
| `booking.kara` ★ | `struct BookMyShow` of two `Vec[i64]` trees over a power-of-two width, the largest free count and the free total; `leftmost(k)` walks down, `free_through(row)` is the bottom-up range sum |
| `booking_naive.kara` | the seats taken in each row; `gather` walks rows from 0, `scatter` sums and then fills through `max_row`. O(n) per call |
| `booking_blocks.kara` | the rows in blocks of about sqrt(n), each block keeping its largest free count and its free total; whole blocks skipped or summed. O(sqrt n) per call |
| `booking_fenwick.kara` | a Fenwick tree of free seats for `scatter`'s sum, and the first row not full kept, from which `scatter` fills and `gather` walks. O(n) per `gather` |
| `booking_iter.kara` | the free seats per row; `gather` by `take` and `position`, `scatter` by `take` and `sum` and then an `iter_mut` loop |
| `booking_solution.kara` | LeetCode's Rust template: `struct BookMyShow` with `new(n: i32, m: i32) -> Self`, `gather(&mut self, k: i32, max_row: i32) -> Vec<i32>`, `scatter(..) -> bool`, a recursive segment tree over `usize` nodes; carried by `karac fix`, and driven through a `Show` adapter that takes the harness's `i64`s |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's example, a show of 3
rows of 4 seats that fills a row exactly, refuses a gather in a full
row, gathers past it and scatters every seat left; then 400 random
shows of 1 to 20 rows of 1 to 20 seats and 1 to 60 calls of up to
twice a row, with a checksum of the answers and the seats booked; then
one show of 2000 rows of 10^9 seats and 5000 calls of 1 to about 2^30
seats. `booking.py` mirrors the ★ arm and its output is byte-identical.

The iterator arm was first written with `take_while(|f| need > 0)` on
the `iter_mut` that fills the rows, while the loop body writes `need`.
`karac check` refuses it (E0516: `need` is written while the closure
still borrows it), as Rust does; the loop breaks on `need == 0`
instead.

`karac fix` carries the template in one round, reporting 44 edits:
every `usize` in the struct and the signatures to `i64`, with `n as
usize` to `n as i64` and the `max_row as usize` arguments dropped to
`max_row`, `Vec<i64>` and `Vec<i32>` to brackets, `vec![0; 4 * n]` to
`Vec.filled(4 * n, 0)`, `vec![i as i32, used as i32]` to the list
literal and `vec![]` to `Vec.new()`, `&mut self` and `&self` to `mut
ref self` and `self`, `Option<usize>` to `Option[i64]`, `||` to `or`,
and `m: m as i64` to `m: m`. `fn new(..) -> Self` and the struct
shorthand `BookMyShow { n, .. }` stay as written.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a grid of seats, each taken or not. A `gather` looks row by
row from row 0 for `k` free seats side by side, at the smallest seat
they can start from; a `scatter` counts the free seats through
`maxRow` and takes the smallest seat of the smallest row, one at a
time. No counts. It checks 300 random shows of 1 to 20 rows of 1 to 20
seats; then 30 shows of one row; then 30 of 1 to 50 rows of 10^9
seats, too many to lay out, judged by P2 to P6 only. Each show takes 1
to 60 calls of up to twice a row (at most 2^30 - 1). All 360 shows and
their calls are drawn before any arm answers.

| | property |
|---|---|
| P1 | every answer is the literal reading's (20 seats or fewer) |
| P2 | a gather's `[r, c]` has `r <= maxRow` and `c + k <= m`, and the seats booked never pass `n * m` |
| P3 | a gather's seat `c` is the count already booked in row `r` by the arm's own answers: each gather where it said, each scatter from the smallest row with a seat free |
| P4 | the same calls on a show with one more row: the same answers |
| P5 | after the calls, scatters of every seat left, at most 10^9 each, all book, and then a gather of 1 finds none |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 990339614, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python grid. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the walk down preferring the right | P1 274, P3 225, P4 324, P6 304 |
| M3 | ★: each seat one later | P1 304, P2 159, P3 334, P6 334 |
| M6 | ★: an exact fit refused | P1 76, P5 316, P6 76 |
| M7 | naive: row 0 never gathered into | P1 174, P6 186 |
| M10 | naive: the seat read after booking | P1 304, P2 298, P3 334, P6 334 |
| M11 | naive: a scatter filled from the last row | P1 247, P3 266, P6 277 |
| M12 | blocks: a block's largest run from its first row | P1 220, P4 43, P6 248 |
| M13 | blocks: the block holding max_row skipped | P1 99, P4 19, P6 106 |
| M16 | blocks: a gather's seat moved by the row's place in its block | P1 220, P2 137, P3 248, P4 39, P6 248 |
| M18 | fenwick: the first free row never gathered into | P1 285, P6 314 |
| M19 | fenwick: the update walking one at a time | P1 209, P5 236, P6 236 |
| M21 | fenwick: a scatter's take not capped by the row | P1 241, P2 86, P3 270, P5 222, P6 270 |
| M24 | iter: the seat from the free count | P1 275, P3 305, P6 305 |
| M25 | iter: a scatter filled from the last row | P1 253, P3 273, P4 241, P6 283 |
| M26 | iter: a gather of k fits k - 1 | P1 224, P2 224, P3 2, P5 292, P6 224 |
| M29 | solution: a gather books one more | P1 212, P3 179, P5 311, P6 239 |
| M31 | solution: the search trying the right half first | P1 268, P3 231, P6 298 |

P1 and P6 kill all seventeen, P3 eleven, and P2, P4 and P5 five each.
P3, the arm's own answers replayed as a ledger, catches every edit that
puts a group at the wrong seat or fills rows in the wrong order. P4, one
more row, fails where an arm's layout depends on `n`: the blocks arm's
widths, and a tree walked from the wrong side. P5 fails where an arm
loses count of its free seats, so the scatters of every seat left are
refused or a seat is left over. No property but P1 and P6 sees the
naive arm's row 0 never gathered into or the Fenwick arm's first free
row skipped: both answer `[]` or a later row where the literal hall has
room, and every answer they do give is consistent.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Nine fail as a kept one does or as another
not-kept one does: a gather past `max_row` in the ★ and iter arms and
`max_row` ignored in the template's search (M2, M22, M27); the free
seats or the sum one row short in the ★, naive, Fenwick and iter arms
(M4, M9, M17, M23); a gather that needs more than `k` in the naive and
Fenwick arms (M8, M20). Five fail in ways of their own and are left
out because their arm keeps enough: the ★ arm's gather in `max_row`
refused (M5), the blocks arm's partial block one row short and block
with an exact fit skipped (M14, M15), and the template's seat from the
free seats through its row and one seat fewer in every row (M28, M30).

Four edits of the first draft were replaced. The ★ arm's parent's
largest run never refreshed sends `scatter`'s walk down to a full row,
which gives nothing, so it never ends; the template's parent's total
from its left child does the same; both are now M5 and M28. The blocks
arm's block total one less per take and empty block skipped from
mid-block walk `scatter` off the end of the rows (an index out of
bounds), and its block's largest run never refreshed changes nothing,
since a block with no room is then only scanned for nothing; they are
now M15, M16 and M12.

## Verification

Every arm prints the same output as `booking.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, blocks, Fenwick and template arms take
0.3 to 0.6 s, the naive arm 1.8 s and the iterator arm 3 s, both
walking the rows from 0 on every call of the 2000-row show; the
differential takes 1.8 s.

## Benchmarks

The bench draws 50000 calls once, each a gather or a scatter of 1 to
10^9 seats through a random row, then plays all of them on 40 fresh
shows of 50000 rows of 10^9 seats, with the ★ arm in all five
languages. Every implementation prints `40 shows of 50000 calls:
checksum 642897183`. C's `gather` answers through two out-parameters
and a `bool` rather than a returned array; the others return a
two-element list, or an empty one.

BENCHTAB
