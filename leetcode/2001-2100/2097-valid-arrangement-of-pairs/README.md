# 2097. Valid Arrangement of Pairs

You are given a 0-indexed 2D integer array `pairs` where `pairs[i] =
[start_i, end_i]`. An arrangement of `pairs` is valid if for every index
`i` where `1 <= i < pairs.length`, we have `end_{i-1} == start_i`.

Return any valid arrangement of `pairs`.

Note: the inputs will be generated such that there exists a valid
arrangement of `pairs`.

```
pairs = [[5,1],[4,5],[11,9],[9,4]]  ->  [[11,9],[9,4],[4,5],[5,1]]
pairs = [[1,3],[3,2],[2,1]]         ->  [[1,3],[3,2],[2,1]]
pairs = [[1,2],[1,3],[2,1]]         ->  [[1,2],[2,1],[1,3]]
```

**Constraints:** `1 <= pairs.length <= 10^5`; `pairs[i].length == 2`;
`0 <= start_i, end_i <= 10^9`; `start_i != end_i`; no two pairs are
exactly the same; there exists a valid arrangement of `pairs`.

Each pair is an edge from its start to its end, and a valid arrangement
is a walk that takes every edge once: an Euler path. It must start at the
value with one more pair out than in, when there is one; otherwise every
value is balanced, the walk is closed, and any value with a pair out will
do. Every arm here starts a closed walk at the first pair's start, so they
all start and end at the same values. Hierholzer's walk finds the path:
follow any unused pair out of the value on top of a stack, and when the
top has none left it is finished and goes on the path, which comes out
backwards. The arms differ in how they hold the pairs and walk them.

## Approaches

| file | mechanism |
|---|---|
| `arrangement.kara` ★ | each value's ends in a `Map[i64, Vec[i64]]` and its out-minus-in count in a `Map[i64, i64]`; Hierholzer's walk on an explicit `Vec` stack, `match next[top].pop()` taking a pair or finishing the value; the path reversed and paired up with a range `map`. O(n) |
| `arrangement_rec.kara` | the walk written recursively, `while let Some(v) = next[at].pop()` calling itself on each end through `mut ref` parameters; the start found with `find` over the out counts against a second `Map` of in counts, `unwrap_or` the first pair's start; the path paired up with `windows(2)` |
| `arrangement_ids.kara` | the values sorted, deduplicated and renamed by a `binary_search` closure, so every table is a `Vec`; each value keeps a count of the pairs it has used instead of popping them, read through `while let Some(top) = stack.last()`. O(n log n) |
| `arrangement_edges.kara` | the walk over pair numbers rather than values: each value lists the pairs leaving it, the stack holds pair numbers, and a finished pair goes on the answer as it was given; out and in counts kept together as a `Map[i64, (i64, i64)]` updated through `.0` and `.1` |
| `arrangement_struct.kara` | a `struct Itinerary` owning each value's routes as a `VecDeque[i64]` taken from the front, its surplus `Map` and the first start, with methods for the start, the next route and the path |
| `arrangement_solution.kara` | LeetCode's Rust template (`pairs: Vec<Vec<i32>>`, `HashMap<i32, Vec<i32>>` routes filled through `entry(..).or_default()`, a degree map read with `for (&k, &v) in &deg`, `while let Some(&u) = stack.last()` over `graph.get_mut(&u)`, the answer from `windows(2)` as `vec![w[0], w[1]]`), carried by `karac fix` in four rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and three
more, each with the one arrangement it has; then how many of 2000 random
walks of 1 to 40 pairs over 2 to 12 values (every third one closed)
come back as valid arrangements, their pairs, and a checksum of where
each starts and ends; then the constraints' largest, 100000 pairs in an
open walk and in a closed one over 1000 values, and a chain of 100000
different values given back to front. The walks keep to the
constraints: no pair from a value to itself and none twice.
`arrangement.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the answer uses each given pair once, and each pair's end is
the next one's start. For the checksum it also counts every arrangement
of each walk, by trying each unused pair after each. It checks 300
random walks of 1 to 7 pairs over 2 to 5 values, every third one
closed; then 20 chains of 6 to 8 different values; then 20 closed walks
of 7 or 8 pairs over 4 values. Each walk's pairs are shuffled, and all
340 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is an arrangement, the statement read literally |
| P2 | the pairs each turned round: the answer is an arrangement of them, and when the walk is open it starts where the first answer ended |
| P3 | the values renamed, `v` to `10^9 - v`: the answer is the first one renamed |
| P4 | the pairs after the first shuffled: the answer starts and ends where the first one did |
| P5 | the answer starts at the value with one more pair out than in, or at the first pair's start when none has, and ends at the value with one more in than out, or where it started |
| P6 | each arm agrees with at least three of the other five on where the answer starts and ends |

The arms may give different arrangements of the same walk, which is
why P6 compares only the ends, which the statement fixes for an open
walk and the arms' shared rule fixes for a closed one. The differential
prints `340 walks: checksum 208223052, 12240 checks over 6 arms: 0
failures` under every lane in Verification; the checksum of the
arrangement counts was checked against a Python reading of the same
walks. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-six edits to the differential, five to each arm and then six
more aimed at arms whose failures crowded one another, each run under
`karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept, three
to each Kāra arm and two to the Rust-template arm. Each kept one is
killed, fails the same way under both backends and not by a crash, and
no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the start never the value with more out | P1 76, P2 84, P4 76, P5 76, P6 76 |
| M2 | ★: a finished value put on the path twice | P1 340, P2 340, P4 340, P5 340 |
| M3 | ★: the stack's bottom taken for its top | P1 340, P2 340, P4 340, P5 340, P6 139 |
| M4 | rec: a value put on the path before its pairs | P1 199, P2 208, P4 211, P5 199, P6 157 |
| M5 | rec: the start the value with one more in | P1 97, P2 100, P4 97, P5 97, P6 97 |
| M6 | rec: a closed walk from the middle pair's start | P4 75, P5 180, P6 180 |
| M7 | ids: each pair written turned round | P1 249, P2 249, P4 249, P5 340, P6 340 |
| M8 | ids: the path read forwards | P1 229, P2 229, P4 229, P5 320, P6 320 |
| M9 | ids: a value's last pair never taken | P1 340, P2 340, P4 340, P5 340, P6 271 |
| M10 | edges: the walk back resumed at the pair's end | P1 40, P2 57, P4 62, P5 40, P6 8 |
| M11 | edges: the walk staying at the pair's start | P1 320, P2 320, P4 320, P5 320, P6 288 |
| M12 | edges: each pair counted twice into its end's ins | P1 36, P2 40, P4 36, P5 36, P6 36 |
| M13 | struct: a value with pairs left dropped from the stack | P1 340, P2 340, P4 340, P5 340, P6 340 |
| M14 | struct: the start only a value that is a multiple of three | P1 52, P2 52, P3 50, P4 52, P5 52, P6 52 |
| M15 | struct: a closed walk from the last pair's start | P4 69, P5 186, P6 186 |
| M16 | solution: the adapter's pairs turned round | P1 183, P2 183, P4 183, P5 340, P6 340 |
| M17 | solution: the start the value with one more in | P1 139, P2 139, P4 139, P5 139, P6 139 |

P4 and P5 kill all seventeen, P6 sixteen, P1 and P2 fifteen each, and
P3 one. P1 misses the edits that only move a closed walk's start (M6,
M15): the answer is still an arrangement, so only P5, P4 (the first
pair is kept, the last is not) and P6 see it. P6 misses M2, the one edit
whose wrong answers still start and end where the others' do. P3 sees
only M14, the one edit that looks at a value's size: renaming `v` to
`10^9 - v` changes which values are multiples of three. Every other edit
is blind to the values, so P3, which asks exactly that, holds for them.

Of the thirty-six, nineteen were not kept, and none survives. Three
fail differently under the two backends, and not by a compiler bug: an
end counted as one more out (★, struct and Rust arms) gives several
values a surplus of one, and which of them the walk starts from follows
the `Map`'s walk order, which is per process. Nine fail as a kept one:
each pair counted into its start (rec, ids and edges arms) as M1; the
start the value with more in (ids, edges and struct arms) as M17; the
edges arm's arrangement read backwards as M8; the Rust arm's adapter's
answers turned round as M7; the Rust arm's closed walk from the last
pair's start as M15. Six fail the same way as others and were left out
together: the path read forwards (★, rec, struct and Rust arms), and a
closed walk from the first pair's end (rec and struct arms). One is
killed with checks of its own but was left out because its arm keeps
its share: the struct arm's path cut at eight values (P1 24, P2 24, P4
24, P5 24, P6 23).

## Verification

Every arm prints the same output as `arrangement.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 6.5 s to 10.0 s, and the
differential 1.2 s (timed while other work shared the machine).

The kata met two gaps, both fixed.

- The ids arm's `binary_search` closure made the MIR interpreter slow:
  its `binary_search` read every element of the `Vec` and ranked them
  all on each call, so each search was linear, and the arm's chain of
  100000 pairs (200001 searches over 100001 values) ran past 15 minutes
  under `karac __mir-run`, against 0.6 s compiled. It now reads only the
  probed elements, in std's probe order as the compiled runtime does, so
  among equal elements both answer the same index. Fixed in kara
  BSEARCHSHA, test `tests/kata_2097_interp_binary_search.rs`.
- The ids arm was first written `while let Some(top) = stack.last()`,
  pushing onto `stack` in the body. `last` returns `Option[ref T]`, so
  `top` borrows `stack` for the whole body and the push is refused, as
  Rust refuses it. The message names the repair, a copy of the value,
  but `karac fix` applied it only to a `let` initializer, not to a
  `while let` or `if let` scrutinee. It now writes `.cloned()` there
  when the element is `Copy` or `shared`. Fixed in kara WHILESHA, test
  `tests/kata_2097_while_let_last_copy_fix.rs`. The Rust template's
  `while let Some(&u) = stack.last()` goes the same way.

With those, `karac fix` carries the template in four rounds of 33, 4, 5
and 1 edits: Rust's spellings (`Vec<Vec<i32>>` and `HashMap<..>` to
brackets, `&pairs` to `ref pairs`, the patterns' `&` dropped, `::` to
`.`, `struct Solution;` to `struct Solution {}`, the `use` line dropped)
and `stack.last()` given its `.cloned()`; then `HashMap` to `Map`; then
`or_default()` to `or_insert(Vec.new())`, `vec![..]` to brackets and
`windows(2)` given its `.iter()`; then the adapter's `ref` parameter to
a bare one, which borrows already. The rec and struct arms'
`windows(2).map(..)` met the same `.iter()` fix-it.

## Benchmarks

The bench arranges 100 random walks of 100000 pairs over 1000 values,
the constraints' largest, every other one closed, with the ★ arm in all
five languages: a hash map from each value to its ends and one to its
balance, and Hierholzer's walk on an explicit stack. The maps are Kāra's
`Map` and Rust's `HashMap` (both SipHash), Go's `map`, Python's `dict`,
and in C one open-addressing table that numbers the values, with an
array of ends and a balance per number. Building the walks takes a set
of the pairs already used (`Set`, `HashSet`, `map[pair]bool`, `set`, an
open-addressing table in C). Every implementation prints `100 rounds:
10000003 pairs, checksum 98686391`.

BENCHTAB
