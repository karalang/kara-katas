# 2113. Elements in Array After Removing and Replacing Elements

You are given a 0-indexed integer array `nums`. Initially on minute 0,
the array is unchanged. Every minute, the leftmost element in `nums` is
removed until no elements remain. Then, every minute, one element is
appended to the end of `nums`, in the order they were removed in, until
the original array is restored. This process repeats indefinitely.

For example, the array `[0,1,2]` would change as follows: `[0,1,2] ->
[1,2] -> [2] -> [] -> [0] -> [0,1] -> [0,1,2] -> [1,2] -> [2] -> [] ->
[0] -> [0,1] -> [0,1,2] -> ...`

You are also given a 2D integer array `queries` of size `n` where
`queries[j] = [time_j, index_j]`. The answer to the `j`th query is:

- `nums[index_j]` if `index_j < nums.length` at minute `time_j`
- `-1` if `index_j >= nums.length` at minute `time_j`

Return an integer array `ans` of size `n` where `ans[j]` is the answer
to the `j`th query.

```
nums = [0,1,2], queries = [[0,2],[2,0],[3,2],[5,0]]  ->  [2,2,-1,0]
nums = [2],     queries = [[0,0],[1,0],[2,0],[3,0]]  ->  [2,-1,2,-1]
```

**Constraints:** `1 <= nums.length <= 100`; `0 <= nums[i] <= 100`;
`1 <= queries.length <= 10^5`; `queries[j].length == 2`; `0 <= time_j
<= 10^5`; `0 <= index_j < nums.length`.

The process repeats every `2n` minutes, so a query needs only its
minute `t` modulo `2n`. For `t < n` the first `t` values are gone and
place `i` holds `nums[t + i]` while `i < n - t`; for `t >= n` the first
`t - n` values are back and place `i` holds `nums[i]` while `i < t - n`.
Each query is then one comparison and one read.

## Approaches

| file | mechanism |
|---|---|
| `elements.kara` ★ | each query's minute modulo `2n`, then an `if` per phase pushing `nums[t + index]`, `nums[index]` or -1, in a `for` over the query pairs. O(q) |
| `elements_table.kara` | the period's `2n` arrays built once as slice copies (`nums[t..].to_vec()` while removing, `nums[..t - n].to_vec()` while restoring), each query a `get(index).cloned() ?? -1` on its minute's. O(n^2 + q) |
| `elements_deque.kara` | the process itself, once round its period: the queries' indices sorted by minute modulo `2n` with `sort_by_key`, and a `VecDeque` popping its front each minute, then pushing the values back, answering each query when its minute comes. O(n + q log q) |
| `elements_phase.kara` | an `enum Phase { Removing(gone), Restoring(back) }` built by `Phase.at(time, n)`, its `read` method a `match` with guards giving an `Option`, turned into -1 with `??` |
| `elements_iter.kara` | iterators: the array at a minute is `nums.iter().skip(t)` or `nums.iter().take(t - n)`, and the answer its `nth(index) ?? -1` |
| `elements_solution.kara` | LeetCode's Rust template (`Vec<i32>, Vec<Vec<i32>>` to `Vec<i32>`): `queries.iter().map(..).collect()`, each minute taken modulo `2n` after `as usize`, carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples and two
more (two values over two periods and a minute, and the last place
of four asked across a removal and a restoring, once at minute 10^5),
each with its answers; then the sum of the values found, the number of
-1s and a checksum, over 2000 random arrays of 1 to 10 values from 0 to
100 asked 1 to 20 queries at minutes 0 to 60; then the constraints'
largest, 100 values asked 10^5 queries, minute `j` at place `j * 37 mod
100`. `elements.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each query the process run minute by minute from minute
0, the first value removed with `remove(0)` until none is left and then
the original values pushed back one a minute, and the place read at the
query's minute. It checks 300 random arrays of 1 to 6 values from 0 to
100, each asked 1 to 12 queries at minutes 0 to 40; then 30 of up to 30
values asked 1 to 40 queries at minutes up to 200; then 30 of up to 100
values asked at the minutes next to the period's turns (`2mn` and `2mn
+ n` for `m` from 0 to 2, one either side and on it). All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | there is an answer per query, and each is -1 or one of the values |
| P3 | every minute moved on by one period, `2n`: the same answers |
| P4 | every value raised by 5: every answer but a -1 raised by 5 |
| P5 | the queries reversed: the answers reversed |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 arrays: checksum 590449692, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
queries by slicing. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Thirty-four edits to the differential, five to seven to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the period taken as `n` | P1 315, P6 315 |
| M2 | ★: a removed array read from the front | P1 215, P6 215 |
| M4 | ★: one value too many while restoring | P1 194, P6 194 |
| M6 | table: the restored array one short | P1 129, P6 129 |
| M8 | table: a missing place read as 0 | P1 335, P2 308, P4 335, P6 335 |
| M10 | table: the minute not wrapped past one period | P1 320, P3 151, P6 320 |
| M11 | deque: the deque never restored | P1 206, P6 206 |
| M12 | deque: the queries unsorted | P1 285, P5 264, P6 285 |
| M14 | deque: restored values pushed at the front | P1 150, P6 150 |
| M16 | phase: removing and restoring swapped | P1 268, P6 268 |
| M20 | phase: the period three halves | P1 322, P3 342, P6 322 |
| M31 | phase: places from 50 on read as missing | P1 15, P6 15 |
| M22 | iter: the restored array the whole array | P1 312, P6 312 |
| M24 | iter: a place one further | P1 313, P6 313 |
| M33 | iter: minutes past 100 read as minute 100 | P1 52, P3 47, P6 52 |
| M28 | solution: the queries' fields swapped | P1 321, P3 111, P6 321 |
| M29 | solution: the values offset by one | P1 330, P2 329, P6 330 |

P1 and P6 kill all seventeen, P3 four, P2 two, P4 one and P5 one. Most
edits misplace a value or a phase boundary, which reads another of the
values or a -1 where the other belongs: P2, P4 and P5 hold for those,
and only P1 and P6 see them. P3 sees the edits that read a minute other
than modulo `2n`: the table's unwrapped minute (M10), a period of `3n`
(M20), minutes capped at 100 (M33), and the Rust adapter's swapped
fields (M28), whose minute is a place. P2 sees answers that are not
values of the array: 0 for a missing place (M8), where no value is 0,
and every value one up (M29); P4 sees
only the 0, which stays 0 when the values are raised. P5 sees only the deque
arm's unsorted queries (M12), the one arm whose answers depend on their
order. M31 shows only on the last 30 arrays, the ones with more than 50
values.

Of the thirty-four, seventeen were not kept. Two survive and are
equivalent: the ★ arm's `index <= n - t and t + index < n` is
`index < n - t`, and the table arm's array at minute `n` built as
`nums[n..]` is the empty one it was. Eleven fail as a kept one does:
the ★ arm's restoring phase never empty and the phase arm's restored
place one past as M4 (P1 194, P6 194); the table arm's removed array
from its back, the deque arm's removal from the back and the phase and
Rust arms' removed values read from the front as M2 (P1 215, P6 215);
the phase arm's every phase read as removing and the Rust arm's period
`n` as M1; the iterator arm's one value too few taken as M6; its
minute not wrapped as M10; and its skip and take swapped as M16. Four
more are killed with checks of their own but were left out because
their arm keeps its share: the deque arm's one minute behind (P1 323,
P6 323), the Rust arm's missing place read as 0 (P1 312, P2 287, P4
312, P6 312), and the phase and iterator arms' missing place read as a
value, which fail alike (P1 335, P6 335).

## Verification

Every arm prints the same output as `elements.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.8 s to 2.6 s, and the
differential 1.0 s; compiled it takes 0.6 s.

`karac fix` carries the template in three rounds of 17, 3 and 1 edits:
Rust's spellings (`Vec<..>` to brackets in both signatures and the
adapter, `struct Solution;` to `struct Solution {}`, the `&` dropped from
the three closures' patterns, `Solution::` to `.`); then both `as usize` casts to
`as i64` and `vec![..]` to an array literal; then the minute's `as i64`
dropped, since `q[0] % (2 * n)` widens the `i32` without it. The place
keeps its `as i64`, which types its binding.

The differential met one compiler gap, fixed in karac with a test named
for this kata (karac FROMITERSHA,
`tests/kata_2113_collect_compared_from_iter.rs`): P4 was first written
`answer(arm, raised, queries) == x.iter().map(..).collect()`. `==` takes
its own right-hand type, so nothing fixes what `collect` builds, and the
refusal advised a `let` with a type annotation and offered no edit.
When the other side's type is known, `karac fix` now names the
collection at the call, `Vec[i64].from_iter(x.iter().map(..))`, as the
turbofished form's fix already wrote it.

## Benchmarks

The bench builds 20 arrays of 100 values from 0 to 100 and 10^5 queries
at minutes 0 to 10^5 once; then 50 solves each answer every query
against one of the arrays, moving one query's minute on by one before
each solve so no solve repeats the one before, with the ★ arm in all
five languages: each minute modulo the period. The sink is the sum of
the answers, -1s included. Every implementation prints `50 solves:
125487755 summed, checksum 583735963`.

BENCHTAB
