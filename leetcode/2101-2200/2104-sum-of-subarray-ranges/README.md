# 2104. Sum of Subarray Ranges

You are given an integer array `nums`. The range of a subarray of `nums`
is the difference between the largest and smallest element in the
subarray.

Return the sum of all subarray ranges of `nums`.

A subarray is a contiguous non-empty sequence of elements within an
array.

```
nums = [1,2,3]          ->  4
nums = [1,3,3]          ->  4
nums = [4,-2,-3,4,1]    ->  59
```

**Constraints:** `1 <= nums.length <= 1000`; `-10^9 <= nums[i] <= 10^9`.

**Follow-up:** Could you find a solution with `O(n)` time complexity?

The sum of the ranges is the sum of every subarray's largest less the
sum of every subarray's smallest, and each of those is a sum over the
numbers: a number is the largest of as many subarrays as it can reach
left and right before a larger one, which a monotonic stack finds for
every number in one pass. Equal numbers need a tie-break, so that a
subarray with two equal largest counts it once: the stack stops at an
equal number on one side and passes it on the other. At the constraints'
largest the answer is near 10^15, past `i32` but well within `i64`.

## Approaches

| file | mechanism |
|---|---|
| `ranges.kara` ★ | two monotonic stacks of places, a falling one for the largest and a rising one for the smallest; each number's share is added or taken away as it is popped, `nums[top] * (top - left) * (i - top)`, with a final pass at `i == n` to empty the stack. O(n) |
| `ranges_brute.kara` | every subarray in turn: for each start, the running smallest and largest carried right with `min` and `max`, each end adding their difference. O(n^2) |
| `ranges_scan.kara` | iterators only: for each start, `scan` over `nums[i..]` with the (smallest, largest) pair as its state, yielding each range, summed with `sum`, the starts summed again. O(n^2) |
| `ranges_bounds.kara` | the four boundaries first: a `nearest` function, given the order to walk in and the comparison as an `Fn(i64, i64) -> bool`, finds each place's nearest greater and nearest smaller on each side; one pass then adds each number's share as largest and takes away its share as smallest. O(n) |
| `ranges_struct.kara` | a `struct Sweep` holding a stack of `struct Run`s (a number and how many places it stands for) and the total of the extremes of the subarrays ending at the current place; pushing a number pops the runs it beats and takes over their places. One sweep for the largest, one for the smallest. O(n) |
| `ranges_solution.kara` | LeetCode's Rust template (`nums: Vec<i32>` to `i64`, two stacks of `usize` popped with `while let Some(&top) = stack.last()`, `map_or(-1, \|&l\| l as i64)` for the left boundary, every product cast to `i64`), carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples and four
more (one number; all equal; the two extremes; a valley of repeats),
each array with its answer; then the total of the answers, each taken
modulo 10^9 + 7, for 3000 random arrays of 1 to 60 numbers (from -20 to
20, so that ties are common, or from -10^9 to 10^9) and a checksum of
them; then the constraints' largest, 1000 numbers: rising evenly from
-10^9, alternating between the two extremes, and random over the whole
range. `ranges.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every subarray's largest less its smallest, each found by a
scan of the subarray, summed. It checks 300 random arrays of 1 to 12
numbers from -5 to 5, so that ties are everywhere; then 20 of 1 to 30
numbers up to 5 * 10^8 either side of zero; then 20 of 1 to 30 numbers
in runs of 1 to 6 that rise, fall or stay level. All 340 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is at least the whole array's range, and at most that range times the number of subarrays |
| P3 | the numbers listed in reverse: the same answer |
| P4 | every number negated: the same answer |
| P5 | every number doubled: the answer doubled |
| P6 | each arm agrees with at least three of the other five |

The wide arrays stay within 5 * 10^8 so that doubled they keep to the
constraints. The differential prints `340 arrays: checksum 175950118,
12240 checks over 6 arms: 0 failures` under every lane in Verification;
the checksum of the literal answers was checked against a Python reading
of the same arrays with `max` and `min` of every slice. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, four to six to each arm, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a largest's subarrays one start too many | P1 333, P2 51, P3 298, P4 336, P6 333 |
| M2 | ★: no number left of a largest meaning place 0 | P1 276, P2 17, P3 281, P4 290, P6 276 |
| M3 | ★: a smallest counted once per start | P1 298, P2 27, P3 301, P4 313, P6 298 |
| M5 | brute: the largest the latest number | P1 299, P2 35, P3 306, P4 312, P6 299 |
| M6 | brute: every start's smallest from zero | P1 307, P2 28, P4 324, P6 307 |
| M7 | brute: the last end never reached | P1 315, P2 36, P3 286, P6 315 |
| M8 | scan: the largest started at zero | P1 303, P2 23, P4 324, P6 303 |
| M9 | scan: the largest not carried | P1 251, P4 266, P6 251 |
| M10 | scan: the first start skipped | P1 315, P2 37, P3 286, P6 315 |
| M11 | bounds: an equal largest on the left not stopping | P1 184, P2 19, P4 207, P6 184 |
| M13 | bounds: a smallest's subarrays one end too few | P1 331, P2 56, P3 301, P4 333, P6 331 |
| M14 | bounds: one place popped at most | P1 279, P2 4, P3 120, P6 279 |
| M15 | struct: the smallest sweep keeping the largest | P1 315, P2 315, P6 315 |
| M16 | struct: a popped run's places not taken off | P1 267, P2 28, P3 275, P6 267 |
| M17 | struct: a popped run counted as one place | P1 280, P2 10, P3 278, P6 280 |
| M21 | solution: the adapter halving every number | P1 312, P2 29, P5 299, P6 312 |
| M22 | solution: the smallest's share halved | P1 333, P2 53, P4 332, P5 239, P6 333 |

P1 and P6 kill all seventeen, P2 sixteen, P3 ten, P4 ten and P5 two.
P2 misses only M9, whose largest is the larger of the start and the
current number, so its ranges stay within the bounds. P3 sees the edits
that treat the two ends of the array differently: a boundary off by one
on one side (M1, M13), a missing left neighbour read as place 0 (M2), a
start or an end skipped (M7, M10), a share counted from one side only
(M3), the largest taken as the latest number reading left to right
(M5), and the stacks that lose places (M14, M16, M17). P4
sees the edits that treat the largest and the smallest differently,
which negating swaps: M1, M2, M3, M13 and M22 change one side's share
only, M5, M6, M8 and M9 one side's running bound, and M11 one side's
tie-break, which double-counts equal largest but not equal smallest. P5
sees the two edits that do not scale with the numbers: the adapter's
halving, which rounds toward zero (M21), and the smallest's share
halved after the product (M22), which rounds too.

Of the thirty, thirteen were not kept, and none survives. Four fail as
M15, the 315 arrays whose range is not zero, all from an answer that
can only fall to zero or below: the Rust arm's largest's pop test turned
round (M19), the brute arm's smallest tracking the largest (M25), the
scan arm's largest carried as a smallest (M29), and the struct arm's
pushed number standing for no place (M30). Two fail the same way as
each other and were left out together: the struct arm keeping only the
last end's ranges (M18) and the scan arm keeping only each start's
largest range (M23), P1 292, P3 286, P6 292. Seven are killed with checks
of their own but were left out because their arm keeps its share: the ★
arm's smallest left on the stack (M4) and one place popped at most
(M27); the bounds arm's missing smaller on the right read as the last
place (M12) and its right boundaries searched left to right (M26); the
struct arm's pushed run of one place (M24); and the Rust arm's missing
left neighbour of a smallest (M20) and its largest's stack never emptied
(M28).

A first version of M29, the scan arm's state set to `(bounds.0.min(x),
x)`, did not compile: `x` is a `ref i64` from `iter()`, so the pair is
`(i64, ref i64)`, not the state's `(i64, i64)`. Rust refuses the same,
but Kāra's refusal read "expected 'Option[((i64, i64), OutV)]'", naming
`scan`'s own type parameter, which means nothing at the call. See
Verification.

## Verification

Every arm prints the same output as `ranges.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the O(n) arms take 1.2 s to 2.2 s, the brute arm
3.0 s, the scan arm 15.7 s, and the differential 1.4 s (timed while
other work shared the machine). The scan arm walks the same O(n^2)
subarrays as the brute arm; the interpreter's closure call per step is
the difference. Under `karac __mir-llvm-run`, compilation included,
they take 0.5 s and 0.3 s.

The scan arm was first written as Rust writes `scan`: `|bounds, x| {
*bounds = (bounds.0.min(x), bounds.1.max(x)); Some(bounds.1 - bounds.0)
}`. Kāra's `scan` closure takes the state by value and returns it with
the item, `Some((next_state, item))`, and `karac` already explained and
rewrote Rust's form, but only when the body used the state through `*`
alone; Rust reads a lent pair's fields without one, so `bounds.0` read
as some other use of the state, and the call drew a "drop the `*`" error
and a mismatch naming `scan`'s own `OutV`. A field read of the state now
counts as a read, and `karac fix` rewrites the closure to `let bounds =
(bounds.0.min(x), bounds.1.max(x)); Some((bounds, bounds.1 -
bounds.0))`; its lines are indented where the closure sits since kara
B-2026-11-10-32, which fixed the same layout from another kata first
(the rewrite had laid a multi-line closure out from the first column).
Fixed in kara SCANSHA, test `tests/kata_2104_rust_scan_field_reads.rs`. The
arm is written in Kāra's form.

A type mismatch whose expected type holds a parameter of the library
signature it came from, one nothing at the call has bound, now writes
it `_`: the M29 refusal reads "expected 'Option[((i64, i64), _)]'".
Fixed in kara PARAMSHA, test `tests/kata_2104_foreign_param_display.rs`.

`karac fix` carries the template in three rounds of 19, 5 and 7 edits:
Rust's spellings (`Vec<..>` to brackets, `::` to `.`, `&&` to `and`,
`Some(&top)` in a `while let` to `Some(top)` over `.cloned()`, the `&l`
closure pattern dropped, `struct Solution;` to `struct Solution {}`, the
adapter's `&Vec` to `ref` and its `&x` pattern dropped); then the
`usize` stack to `i64`, as Kāra writes indices, and the casts of `i32`
to `i64` dropped as widening; then the casts the `i64` stack made
redundant, `l as i64`, `i as i64` and `top as i64`, and the adapter's
`ref` parameter to a bare one. The template's products keep the
template's order, an `i32` number times `i64` place counts, which Kāra
widens before it multiplies.

## Benchmarks

The bench builds 1000 arrays of 1000 numbers from -10^9 to 10^9 once,
then sums every array's subarray ranges ten times over, with the ★ arm
in all five languages: two monotonic stacks (a `Vec` in Kāra and Rust, a
fixed array in C, a slice in Go, a list in Python). Every
implementation prints `10000 arrays: total 621357366, checksum 6664411`.

BENCHTAB
