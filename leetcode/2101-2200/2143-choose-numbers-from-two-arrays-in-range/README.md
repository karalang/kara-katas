# 2143. Choose Numbers From Two Arrays in Range

You are given two **0-indexed** integer arrays `nums1` and `nums2` of
length `n`.

A range `[l, r]` (**inclusive**) where `0 <= l <= r < n` is
**balanced** if:

- For every `i` in the range `[l, r]`, you pick either `nums1[i]` or
  `nums2[i]`.
- The sum of the numbers you pick from `nums1` equals to the sum of the
  numbers you pick from `nums2` (the sum is considered to be `0` if you
  pick no numbers from an array).

Two **balanced** ranges from `[l1, r1]` and `[l2, r2]` are considered
to be **different** if at least one of the following is true:

- `l1 != l2`
- `r1 != r2`
- `nums1[i]` is picked in the first range, and `nums2[i]` is picked in
  the second range or **vice versa** for at least one `i`.

Return *the number of **different** ranges that are balanced.* Since the
answer may be very large, return it **modulo** `10^9 + 7`*.*

```
nums1 = [1,2,5], nums2 = [2,6,3]    ->  3
nums1 = [0,1], nums2 = [1,0]        ->  4
```

**Constraints:** `n == nums1.length == nums2.length`; `1 <= n <= 100`;
`0 <= nums1[i], nums2[i] <= 100`.

Picking `nums1[i]` adds it to a running difference and picking
`nums2[i]` takes it away, so a range balances where the difference is
back at zero. For each right end the ranges ending there are counted by
their difference: those ending one place before moved on by either
pick, and a new range started at zero. O(n (sum1 + sum2)).

## Approaches

| file | mechanism |
|---|---|
| `choose.kara` ★ | the counts by difference in a `Vec` offset by nums2's sum, each step pushed into a fresh one |
| `choose_map.kara` | the same counts in a `Map[i64, i64]` holding only the differences some range reaches, so no offset; each step's map built by `entry().or_insert(0)` |
| `choose_weights.kara` | no negative difference: a range balances when the places picked from nums1 weigh, at `nums1[i] + nums2[i]` each, nums2's sum over the range, so a range starts at nums2's sum before it, and each step is a 0/1 knapsack's, in place from the top down |
| `choose_struct.kara` | a `struct Tally` of the counts, `open`ed at zero and `step`ped by a pair (`mut ref self`), asked how many are `balanced` (`ref self`) |
| `choose_fold.kara` | one `fold` over the `zip`ped pairs carrying the counts and the total, its closure taking tuple patterns; each count pulled from the two differences it comes from, `collect`ed by `map` |
| `choose_solution.kara` | LeetCode's Rust template: a `vec!` offset by nums2's sum, `as usize` indices, a `const MOD` written `1_000_000_007`, and `continue`; carried by `karac fix` in four rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four
more (one pair of 0s, one pair that cannot balance, two equal pairs,
and four), each with its count; then the total and a checksum over 2000
random pairs of arrays of 1 to 12 values, of 0 to 9, 0 to 2 or 0 to 100
in turn; then the constraints' largest, 100 values in each array: every
one 0, every one 100, and at random. `choose.py` mirrors the ★ arm and
its output is byte-identical; it was checked against a brute force over
500 random small pairs.

No compiler gap was met. `karac fix` carries the template in four
rounds of 18, 6, 2 and 4 edits: Rust's spellings (`Vec<..>` to
`Vec[..]`, `struct Solution;` to `struct Solution {}`, the adapter's
`&Vec` to `ref Vec`, the `|&v|` patterns to `|v|`, `Solution::` to
`.`); then the `0i64` suffixes dropped, the `ref` dropped from the
adapter's parameters, which borrow already, and the adapter's `as i64`,
since an `i32` widens on return; then each `vec![0; w]` to
`Vec.filled(w, 0)`; then each `as usize` to `as i64`, since Kāra's
indices are `i64`. The `const MOD`, its `1_000_000_007`, the
`continue` and the `ans as i32` that narrows are kept.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every range is tried, and every way to pick from nums1 or
nums2 at each place in it, and a pick counts when the two sums are
equal; no difference is counted and nothing is carried from one range
to the next. It checks 300 random pairs of arrays of 1 to 8 values of 0
to 9, 0 to 2 or 0 to 4 in turn; then 30 with the two arrays equal; then
30 of 1 to 6 values of 0 to 100. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | the two arrays swapped: the same count |
| P3 | both arrays reversed: the same count |
| P4 | every value doubled: the same count |
| P5 | the arrays laid twice end to end, with a pair between of twice their whole sum and one more, too large for any range across it to balance: twice the count |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 pairs: checksum 813065225, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal counts was checked against a Python reading of the same
pairs by the same search. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Thirty-seven edits to the differential, four to eight to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no new range started | P1 282, P6 282 |
| M3 | ★: the counts never carried | P1 247, P3 184, P5 223, P6 247 |
| M4 | ★: the balance read before the step | P1 241, P3 207, P5 259, P6 241 |
| M7 | map: the new range started at nums1's value | P1 259, P2 229, P3 228, P5 360, P6 259 |
| M9 | map: the balance read at difference one | P1 273, P2 235, P4 249, P5 15, P6 273 |
| M37 | map: nums2's pick taken the other way round | P1 193, P2 210, P3 190, P6 193 |
| M11 | weights: the knapsack from the bottom up | P1 222, P2 211, P5 298, P6 222 |
| M12 | weights: the weight nums1's value alone | P1 280, P2 234, P5 360, P6 280 |
| M13 | weights: the balance read at nums2's sum before r | P1 324, P2 185, P3 217, P5 360, P6 324 |
| M18 | struct: the balance asked before the step | P1 259, P3 207, P5 259, P6 259 |
| M19 | struct: the step adding to the old counts | P1 360, P5 360, P6 360 |
| M32 | struct: a range opened only where none stands | P1 184, P3 134, P6 184 |
| M22 | fold: nums2's value pulled from below | P1 243, P6 243 |
| M24 | fold: the pull from nums1 one short | P1 15, P2 17, P3 15, P5 15, P6 15 |
| M25 | fold: the zip over nums1 twice | P1 245, P2 233, P5 7, P6 245 |
| M27 | solution: the adapter dropping the first pair | P1 257, P3 207, P5 257, P6 257 |
| M33 | solution: the template's nums1 pick counted twice | P1 272, P2 229, P6 272 |

P1 and P6 kill all seventeen, P5 twelve, P2 and P3 nine each, and P4
one. P5 lays the arrays twice with a pair between that no range across
it can balance, so the right count doubles; it sees an edit that lets a
count run on past where it should stop or start too late (M3, M4, M18,
M19, M27), that misplaces where a range starts or where the balance is
read (M7, M9, M13), or that misweighs a pick (M11, M12, M24, M25). P2
swaps the arrays, which turns every difference round; it sees an edit
that treats the two arrays unlike (M7, M9, M37, M11, M12, M13, M24, M25,
M33). P3 reverses both arrays, which every right count ignores; it sees
an edit that ties the count to the direction of the walk: a count read
before its step (M4, M18) or never carried (M3), a range opened only
when none stands (M32), the adapter's lost first pair (M27), and some
of the asymmetric ones (M7, M13, M24, M37). P4 doubles every value,
which makes every difference even; it sees only the map arm's balance
read at difference one (M9), which doubling empties.

Of the thirty-seven, twenty were not kept. Five fail by a crash, an
index out of bounds: the ★ arm adding nums2's pick, and its zero offset
at nums1's sum; the struct's step with its pair swapped; and the
template's skip turned and its offset at nums1's sum. One fails
differently from run to run: the map arm's down count overwritten,
which leaves whichever difference the `Map` happens to visit last, and
its walk order is the per-process hash order, so it is no defect of
either backend. Eleven fail as a kept one does: no new range started in
the map, the struct opened never or twice, a single way never stepped
by the struct, the fold's range opened after the pull, and the
template's start inside the step and its single ways skipped, as M1;
the map's old counts kept, as M19; the fold's balance not carried and
the template's, as M4; and the struct's nums1 pick counted twice, as
M33. Three are killed with checks of their own but were left out
because their arms keep their share: the weights arm starting every
range at 0 (P1 236, P2 199, P3 238, P5 257, P6 236) and leaving its
lowest value out of the knapsack (P1 250, P2 80, P3 195, P5 250, P6
250), and the map arm never carrying a balanced range on (P1 184, P6
184).

## Verification

Every arm prints the same output as `choose.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.3 s to 9.9 s and the
differential 6.1 s.

## Benchmarks

The bench builds 4 pairs of arrays of 100 values of 0 to 100 once; then
solves every pair 50 times, one pair of values redrawn before each solve
so that no solve repeats one before, with the ★ arm in all five
languages. Every implementation prints `200 solves: 97385163272 ranges
in all, checksum 290450838`.

BENCHTAB
