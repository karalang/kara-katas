# 2532. Time to Cross a Bridge

There are `k` workers who want to move `n` boxes from the right (old)
warehouse to the left (new) warehouse. You are given the two integers
`n` and `k`, and a 2D integer array `time` of size `k x 4` where
`time[i] = [right_i, pick_i, left_i, put_i]`.

The warehouses are separated by a river and connected by a bridge.
Initially, all `k` workers are waiting on the left side of the bridge.
To move the boxes, the `i`th worker can do the following:

- Cross the bridge to the right side in `right_i` minutes.
- Pick a box from the right warehouse in `pick_i` minutes.
- Cross the bridge to the left side in `left_i` minutes.
- Put the box into the left warehouse in `put_i` minutes.

The `i`th worker is **less efficient** than the `j`th worker if either
`left_i + right_i > left_j + right_j`, or `left_i + right_i == left_j +
right_j` and `i > j`.

The following rules regulate the movement of the workers through the
bridge:

- Only one worker can use the bridge at a time.
- When the bridge is unused, prioritize the **least efficient** worker
  (who has picked up the box) on the right side to cross. If not, prioritize
  the **least efficient** worker on the left side to cross.
- If enough workers have already been dispatched from the left side to
  pick up all the remaining boxes, **no more** workers will be sent from
  the left side.

Return the **elapsed minutes** at which the last box reaches the **left
side of the bridge**.

```
n = 1, k = 3, time = [[1,1,2,1],[1,1,3,1],[1,1,4,1]]  ->  6
n = 3, k = 2, time = [[1,9,1,8],[10,10,10,10]]        ->  50
```

**Constraints:** `1 <= n, k <= 10^4`; `time.length == k`;
`time[i].length == 4`; `1 <= left_i, pick_i, right_i, put_i <= 1000`.

The arms read "enough workers have already been dispatched" as the
accepted solutions do: a box is spoken for when a worker sets off for
it, so a worker leaves the left side only while fewer have set off
than there are boxes.

## Approaches

| file | mechanism |
|---|---|
| `bridge.kara` ★ | an event simulation on four `PriorityQueue`s: each side's waiting workers as `(right + left, i)`, largest first, and the workers picking or putting as `(done, i)`, soonest first. The bridge goes to a worker waiting on the right, else to one on the left while boxes are left to send for, else the clock jumps to the next worker to finish. O(n log k) |
| `bridge_scan.kara` | no queues: each worker's place (an `enum`) and the minute it is free, and every choice a scan over all `k` workers. O(n k) |
| `bridge_sorted.kara` | the ★ arm's four queues as `SortedSet`s of tuples: the least efficient is `pop_last`, the soonest done `pop_first`, put back when it is not done yet. O(n log k) |
| `bridge_rec.kara` | recursion: the ★ arm's queues, with each move of the simulation (a crossing or a jump of the clock) one call, and the release of the finished workers a recursion of its own; at most about 4n deep |
| `bridge_iter.kara` | iterators: the scan arm's places and free minutes, the least efficient waiting worker a `max_by_key` on `(right + left, i)`, the next jump of the clock a `min` over the working, and the places renewed by a `zip` and `map` each move. O(n k) |
| `bridge_solution.kara` | LeetCode's Rust template: two `i32`s and a `Vec<Vec<i32>>` in, `i32` out; the ★ arm's queues as `BinaryHeap`s with `use` lines inside the function, the working ones soonest first through `Reverse`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and six
more, among them a single worker carrying 1000 boxes and four workers
with equal times; then 2000 random cases of 1 to 10 boxes, 1 to 5
workers and times to 10, and 40 of 1 to 1000 boxes, 1 to 100 workers
and times to 1000, as a total and a checksum. `bridge.py` mirrors the ★
arm and its output is byte-identical, and the mirror was checked on
3000 random cases of 1 to 8 boxes, 1 to 4 workers and times to 3, 6 or
12 against a minute-by-minute reading of the statement, and the two
agreed on every case.

## Check and fix

The ★ arm as first written joined its two release loops' tests to the
`while let`, as Rust 2024's let-chains do: `while let Some((done, i)) =
putting.peek() and done <= now`. The release `karac` of the day read the
pattern as matched against the whole `.. and ..` condition and reported
`undefined name 'done'` twice, with no word about the shape. Kara main
had just fixed that (B-2026-11-21-71, found by kata 1353): `check` now
gives the `while let` form the `if let` form's let-chain diagnostic, and
a machine fix that tests the condition first in the body and breaks,
which is what the chain means: `while let Some((done, i)) =
putting.peek() { if not (done <= now) { break; } .. }`. With it,
`check` reports 5 errors on the arm, the two chains and three `!`, and
`karac fix` carries it in one call, reporting 7 edits; the guard it
writes on the `while let` line is set on lines of its own here.

The iter arm as first written chained an `if let` that has an `else`:
`} else if let Some(i) = worst(..) and boxes > 0 {`. `check` refused
it with the let-chain diagnostic and no fix, since nesting under an
`else` changes the meaning; the arm was rewritten as `worst(..).filter(|_|
boxes > 0)`. `check` reported nothing on the other three Kāra arms as
first written.

The template wrote `use std::collections::BinaryHeap;` and `use
std::cmp::Reverse;` inside the function, as LeetCode's Rust solutions
often do. `check` read the `use` as a name, reported `undefined name
'use'` with an `expected ;` error, and its machine fix inserted the
`;`, so the fixed file held `use; BinaryHeap;` and no fix pass recovered
it. B-2026-11-23-70 tells a block-level `use` or `import` for what it is,
Rust's block-level import where Kāra's imports are file-level
(design.md §4), and its fix moves the line to the top of the file,
where the file-level `use` rewrites take it on the next pass. With it,
`check` first reports 21 errors on the template: the unit struct, the
`Vec<..>` and two `BinaryHeap<..>` spellings, the two block-level `use`
lines, five `::` paths, two `||`, one `&&` and three `!`, and the four
`&` patterns. `karac fix` carries it in one call, reporting 53
edits, among them `PriorityQueue.max_first()` for `BinaryHeap.new()`,
a smallest-first `PriorityQueue.new()` with the `Reverse` taken off its
pushes and patterns, `.cloned()` for the `&` patterns, and the
wrapper's `as i64` dropped as lossless; a second and third call find
nothing.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the clock moved one minute at a time, each worker's step
ended when its minute comes, and the bridge given out by the
statement's rules whenever it is free. It checks 300 random cases of 1
to 8 boxes, 1 to 4 workers and times to 3, 6 or 12, all drawn before
any arm answers; in 222 of them no two workers are equally efficient.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | at least `n` of the quickest crossings each way |
| P3 | the first worker alone: `n` round trips less the last put |
| P4 | one box: the least efficient worker's trip there and back |
| P5 | with no two workers equally efficient, the workers listed backwards: the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `300 cases, 222 with no two workers equally
efficient: checksum 369264339, 10800 checks over 6 arms: 0 failures`
under every lane in Verification; the checksum of the literal answers
was checked against the Python minute-by-minute reading. On a failure
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
| M1 | ★: the right side most efficient first | P1 27, P6 27 |
| M2 | ★: the first queue keyed by the pick | P1 123, P4 95, P5 40, P6 123 |
| M4 | ★: the clock a minute past a pick | P1 227, P3 300, P4 300, P6 227 |
| M7 | scan: ties to the lower index | P1 45, P4 24, P6 45 |
| M8 | scan: the efficiency the crossing over alone | P1 116, P4 74, P5 47, P6 116 |
| M10 | scan: the put timed as a pick | P1 126, P3 215, P6 126 |
| M12 | sorted: the most efficient sent from the left | P1 216, P4 215, P6 216 |
| M14 | sorted: a worker back on the left keyed by its put | P1 39, P5 10, P6 39 |
| M16 | sorted: the right side keyed by the crossing back alone | P1 9, P5 3, P6 9 |
| M17 | rec: one worker released a move | P1 20, P5 14, P6 20 |
| M18 | rec: done while a worker still picks | P1 300, P2 46, P3 300, P4 300, P6 300 |
| M20 | rec: the first queue keyed by the difference | P1 153, P4 135, P5 24, P6 153 |
| M22 | iter: the most efficient first | P1 215, P4 215, P6 215 |
| M24 | iter: no time to put | P1 150, P3 265, P6 150 |
| M26 | iter: the crossing over timed as the crossing back | P1 259, P2 16, P3 237, P4 232, P6 259 |
| M29 | solution: a worker back on the left keyed by the crossing over | P1 69, P5 22, P6 69 |
| M31 | solution: one box fewer | P1 299, P2 54, P3 300, P4 300, P6 299 |

P1 and P6 kill all seventeen, P4 ten, P5 seven, P3 six, and P2 three.

Three of the first thirty-one edits never finished and were replaced:
the ★ arm's and the template's worker sent with no box left keep a
worker always on the road, so the loop that waits for the last one
never ends, and the ★ arm's put released only after its minute leaves
the clock waiting on a worker it will not release. They became the ★
arm's left side most efficient first, its clock a minute past a pick,
and the template's worker back on the left keyed by the crossing over
(M3, M4, M29). The first versions of P3 and P4, every time doubled and
one more box never earlier, killed none of the edits: an edit that
changes a time or an order changes it the same way at twice the scale
and with one more box. They were replaced by the first worker alone,
whose answer is a formula, and one box, which the least efficient
worker carries alone.

Fourteen are not kept, and none survives. Four fail exactly as a kept
one: the ★ arm's left side most efficient first (M3) as the sorted
arm's most efficient sent from the left (M12), the sorted arm's most
efficient sent from the right (M13) as the ★ arm's right side (M1), the
iter arm's ties to the lower index (M23) as the scan arm's (M7), and
the template's no time to put (M28) as the iter arm's (M24); the ★
arm's and the template's crossing back timed as the crossing over (M6,
M30) also fail alike. The other eight fail in ways of their own, in
arms that already hold their kept edits: the ★ arm's pick timed as a
put (M5); the scan arm's box count never lowered and the iter arm's
worker sent with no box left (M9, M25), which differ by one case on P1;
the scan arm's one box fewer carried (M11); the sorted arm's no time to
pick (M15); the rec arm's put counted before the arrival and its pick
counted twice (M19, M21); and the template's efficiency the crossing
over alone (M27).

## Verification

Every arm prints the same output as `bridge.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.9 to 13.2 s and the differential 2.1 s; under `karac __mir-llvm-asan` the arms take 0.7 to 3.1 s and the differential 0.9 s; and under `karac run` the differential takes 1.1 s.

## Benchmarks

The bench builds 200 random cases once from its own generator, each of
1 to 1000 boxes, 1 to 100 workers and times to 1000, then makes 100
passes. Each pass asks every case, starting at an offset the checksum
so far picks, and folds each answer plus the pass into the checksum.
The bench reads each case as `let (n, k, time) = ref cases[..]`:
written without the `ref`, `check` refused moving the `Vec` out of the
list and offered the `ref` as the fix. The bench uses the ★ arm in all
five languages: C with a hand-written binary heap, Rust's `BinaryHeap`
with `Reverse`, Go's `container/heap`, and Python's `heapq`. Every
implementation prints `100 passes over 200 cases: checksum 373698878`.

BENCHTAB
