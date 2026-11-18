# 2295. Replace Elements in an Array

You are given a **0-indexed** array `nums` that consists of `n`
**distinct** positive integers. Apply `m` operations to this array,
where in the `i`th operation you replace the number `operations[i][0]`
with `operations[i][1]`.

It is guaranteed that in the `i`th operation:

- `operations[i][0]` **exists** in `nums`.
- `operations[i][1]` does **not** exist in `nums`.

Return *the array obtained after applying all the operations*.

```
nums = [1,2,4,6], operations = [[1,3],[4,7],[6,1]]   ->  [3,2,7,1]
nums = [1,2], operations = [[1,3],[2,1],[3,2]]       ->  [2,1]
```

**Constraints:** `n == nums.length`; `m == operations.length`;
`1 <= n, m <= 10^5`; all the values of `nums` are **distinct**;
`operations[i].length == 2`; `1 <= nums[i], operations[i][0],
operations[i][1] <= 10^6`; `operations[i][0]` will exist in `nums`
when applying the `i`th operation; `operations[i][1]` will not exist in
`nums` when applying the `i`th operation.

The numbers stay distinct after every operation, so each number has
one index at a time. Keep a map from number to index: an operation
looks the old number up, writes the new one at its index, and hands the
index over. O(n + m).

## Approaches

| file | mechanism |
|---|---|
| `replace.kara` ★ | a `Map[i64, i64]` from each number to its index; an operation `remove`s the old number's entry, writes the new number there and inserts its entry |
| `replace_naive.kara` | for each operation, a scan from the front for the old number, replaced where found. O(n * m) |
| `replace_table.kara` | the index of each number in a `Vec.filled(top + 1, -1)` indexed by the number, `top` the largest number that ever appears; an operation moves one entry. O(top + n + m) |
| `replace_struct.kara` | `struct Slots` keeps the array and a `SortedMap` from number to index, and `replace` keeps the two in step. O((n + m) log n) |
| `replace_iter.kara` | the operations `fold`ed backwards into a map from each number to what it finally becomes, `x` becoming whatever `y` becomes later or `y` itself; then the numbers `map`ped through it. O(n + m) |
| `replace_solution.kara` | LeetCode's Rust template: `mut nums: Vec<i32>`, `Vec<Vec<i32>>` operations and `Vec<i32>` out; a `HashMap<i32, usize>` from number to index; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; no
operations; a number replaced and replaced back; a chain that moves one
slot through five values to 10^6; then 2000 random arrays of 1 to 50
distinct numbers from 1 to 200, each with 0 to 60 operations to a
number not then present, with a checksum and the sum of every answer.
`replace.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one call, reporting 19 edits: the
`use std::collections::HashMap;` dropped, since `Map` is in the
prelude; `struct Solution;` to `struct Solution {}`; the parameter `mut
nums: Vec<i32>` to `nums: own Vec[i32]` with `let mut nums = nums;` at
the top of the body; the brackets of every `Vec<..>` and of the
`HashMap<i32, usize>`, then `HashMap` to `Map` and `usize` to `i64`;
`HashMap::new()` to `Map.new()`; and the `&` of `for (i, &x)` and of
`pos.remove(&op[0])` dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each slot's number is carried through the operations one by
one, and becomes the second number of every operation whose first
number it then is. No index and no map. It checks 300 random arrays of
1 to 30 distinct numbers from 1 to 100, each with 0 to 40 operations at
random slots; then 30 where every operation replaces the number the one
before it wrote, so that one slot runs through a chain; then 30 where
each operation is undone by the next. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | as many numbers as given, all distinct |
| P3 | the operations split in two, and the second part applied by the arm to what the literal reading gives for the first: the same answer |
| P4 | the operations followed by their inverses, last first: the numbers as given |
| P5 | every number and operation 1000 higher: every number 1000 higher |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 81780194, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that does
the same walk. On a failure it prints the first ten and then the count
by property.

P3 as first drafted applied the second part to what the arm itself gave
for the first. An arm with a wrong first half then handed itself an
array missing a number the second half replaces, which the three map
arms answer with an `unwrap` of `None` and the table arm with an index
of `-1`: a mutation that should fail the checks crashed instead. P3 now
starts the second part from the literal reading's array, which always
holds the numbers the operations name.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the old number written back | P1 347, P2 50, P3 233, P4 347, P6 347 |
| M3 | ★: the replacement one slot on | P1 334, P2 71, P3 277, P4 334, P6 334 |
| M4 | ★: the new number indexed at the mirrored slot | P1 297, P2 43, P3 265, P4 331, P6 297 |
| M7 | naive: the match from the second slot | P1 220, P2 14, P3 153, P6 220 |
| M8 | naive: the last slot never scanned | P1 212, P2 18, P3 157, P6 212 |
| M9 | naive: the slot after the match replaced | P1 334, P2 138, P3 313, P4 334, P6 334 |
| M12 | table: the first slot read as the second | P1 208, P2 15, P3 143, P4 131, P6 208 |
| M14 | table: the answer sorted | P1 342, P4 340, P6 342 |
| M15 | table: the larger of the two written | P1 296, P2 68, P3 182, P4 298, P6 296 |
| M19 | struct: the first slot's index the last's | P1 209, P2 13, P3 144, P4 130, P6 209 |
| M20 | struct: the values from a sorted copy | P1 273, P2 67, P3 273, P4 273, P6 273 |
| M21 | struct: the smaller of the two written | P1 305, P2 60, P3 187, P4 298, P6 305 |
| M22 | iter: the operations walked forwards | P1 301, P2 88, P3 298, P4 347, P6 301 |
| M24 | iter: a number the first in its chain | P1 137, P2 132, P3 133, P4 187, P6 137 |
| M26 | iter: a number never changed left as nothing | P1 278, P2 250, P3 233, P4 278, P5 278, P6 278 |
| M29 | solution: the new number indexed at slot 0 | P1 298, P2 50, P3 294, P4 327, P6 298 |
| M31 | solution: the last operation skipped | P1 347, P4 347, P6 347 |

P1 and P6 kill all seventeen, P2, P3 and P4 fifteen each, and P5 one.
P2 misses the two edits that keep every number distinct: the table
arm's answer sorted and the template's last operation skipped. P3
misses the same two, since a sorted answer is the same sorted from
either start and a skipped last operation is skipped from either start.
P4 misses the naive arm's match from the second slot and last slot never
scanned, which leave an operation on a number they cannot find undone
and so undo it too. P5, every number 1000 higher, kills only the iter
arm's number never changed left as nothing, which writes 0 where it
should keep the number: no arm reads a number's size, so a shift by
1000 changes nothing else. It is kept because it fails for that edit
alone.

Of the thirty-one, fourteen were not kept. Eight crash the same way
under both backends: the ★ arm's new number never indexed, operations
from the second, and from and to swapped in the index (M1, M5, M6) and
the template's new number never indexed (M27) on an `unwrap` of `None`;
the table arm's new entry never set and last slot never indexed (M13,
M16) on an index of `-1`; and the struct arm's index keyed by the old
number again (M18) on a missing key. The naive arm's last operation
dropped (M10) fails as the template's last operation skipped (M31); the
naive arm's match by the new number (M11) as the struct arm's values
never written (M17); the template's operation's numbers swapped (M28)
as the ★ arm's old number written back (M2), and its index from 1 (M30)
as the ★ arm's replacement one slot on (M3). The iter arm's only the
next operation followed and numbers mapped by the start of their chain
(M23, M25) fail in ways of their own, past the three kept for that arm.

Eight edits as first drafted were equivalent, each passing all 12960
checks, and were replaced before the run above: the old number left in
the index, in the ★ arm and the template, and the old entry left in the
table, since the numbers are distinct and a stale entry is never asked
for again; the first slot never indexed with a miss read as slot 0, the
table sized by the numbers alone, and the old entry cleared to 0, each
of which lands on the right slot anyway; every match replaced, since
there is only one; and an operation done twice that only rewrote a
value with itself. Two replacements for the table arm, the new number
indexed at the mirrored slot and every slot indexed one on, failed as
the ★ arm's M4 and M3 and were replaced by M12 and M14.

## Verification

Every arm prints the same output as `replace.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.4 to 0.8 s. The differential
takes 1.2 s.

## Benchmarks

The bench builds 10 arrays of 10^5 distinct numbers from 1 to 10^6, each
with 10^5 operations to a number not then present, once, then makes 3
passes over all of them with the ★ arm in all five languages. Every
implementation prints `3 passes over 10 arrays of 10^5 with 10^5
operations: checksum 531098898`. C keeps the index in an open-addressed
table with linear probing and backward-shift deletion, Rust in a
`HashMap`, Go in a `map` and Python in a `dict`.

BENCHTAB
