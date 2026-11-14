# 2121. Intervals Between Identical Elements

You are given a 0-indexed array of `n` integers `arr`.

The interval between two elements in `arr` is defined as the absolute
difference between their indices. More formally, the interval between
`arr[i]` and `arr[j]` is `|i - j|`.

Return an array `intervals` of length `n` where `intervals[i]` is the
sum of intervals between `arr[i]` and each element in `arr` with the
same value as `arr[i]`.

```
arr = [2, 1, 3, 1, 2, 3, 3]  ->  [4, 2, 7, 2, 4, 4, 5]
arr = [10, 5, 10, 10]        ->  [5, 0, 3, 4]
```

**Constraints:** `n == arr.length`; `1 <= n <= 10^5`; `1 <= arr[i] <=
10^5`.

Summing over every pair is O(n^2), too slow when all `10^5` values are
equal. Within one value's indices `p[0] < p[1] < ...`, the distances
from `p[k]` are `k * p[k]` less the sum of the indices before it, plus
the sum of those after it less `(c - k - 1) * p[k]`, so one running sum
over each value's list answers every index. The same sums can be kept
per value while scanning left to right and then right to left, or the
answer stepped from one index to the next: a gap of `g` takes the `k`
copies behind `g` farther and the `c - k` ahead `g` nearer.

## Approaches

| file | mechanism |
|---|---|
| `intervals.kara` ★ | each value's indices gathered in a `Map` through `entry().or_insert(..)`, then one running sum per list. O(n) |
| `intervals_passes.kara` | a `Map` of `(count, sum)` per value, left to right for the copies before each index and right to left for those after; `get(..).unwrap_or((0, 0))` and `m[k] = v`. O(n) |
| `intervals_sorted.kara` | the indices sorted by `(arr[i], i)` with `sort_by_key`, each run of one value answered from its sum through a slice; no `Map`. O(n log n) |
| `intervals_struct.kara` | a `struct Group { positions }` per value whose `spread_into` (`mut ref` to the answer) answers the first index by summing and every next one by the step `(2k - c) * gap` |
| `intervals_iter.kara` | a `SortedMap` of each value's indices over `enumerate()`, prefix sums from `scan`, the answers paired with their ranks by `enumerate` |
| `intervals_solution.kara` | LeetCode's Rust template: a `HashMap<i32, Vec<usize>>` through `entry().or_insert_with(Vec::new)` and `usize` indices cast to `i64`, carried by `karac fix` in four rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one element, every value different, every value the same, two values
alternating), each with its answer; then the sum and a checksum of the
answers over 2000 random arrays of 1 to 40 values from 1 to 1, 3, 10 or
100000 in turn; then the constraints' largest, 100000 equal values and
100000 values in a cycle of seven. `intervals.py` mirrors the ★ arm and
its output is byte-identical.

The struct arm first bound the group's indices as `let p =
self.positions;`, a move out of the borrowed receiver. That met a
compiler gap, fixed in karac with a test named for this kata (karac
fa7746a0b2, `tests/kata_2121_let_ref_only_read.rs`). The refusal's one
machine fix was `.clone()`, a copy of the whole list on every call,
though core-semantics.md §4.6 names `let p = ref self.positions;` as
the other fix and nothing after the `let` needed a value of its own. An
immutable `let` of a place whose binding is afterwards only read (a
method receiver, an index or field base, an operand, an interpolation,
a bare `for`'s collection) now gets the `ref` borrow as its fix, and
`karac fix` carries the arm in one round.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each index, every index holding the same value, and the
distances summed. It checks 300 random arrays of 1 to 30 values from 1
to 1, 3, 10 or 1000 in turn; then 30 of up to 200 values from 1 to 5;
then 30 of up to 12 equal values. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | the array reversed: the answers reversed |
| P3 | the first value replaced by one not in the array: its answer 0, every other copy of the old value that far nearer, the rest the same |
| P4 | a value not in the array appended: the same answers and a 0 |
| P5 | one answer per index, never negative, 0 exactly where the value is alone, and their sum even, since each pair is counted from both ends |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 arrays: checksum 414848764, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
arrays. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-four edits to the differential, five to seven to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: the running sum never grows | P1 264, P2 267, P6 264 |
| M4 | ★: the first index never gathered | P1 251, P2 250, P3 251, P5 251, P6 251 |
| M5 | ★: only the copies to the left | P1 276, P2 276, P5 276, P6 276 |
| M7 | passes: the earlier indices' sum left out | P1 264, P2 267, P5 97, P6 264 |
| M8 | passes: the second pass forwards | P1 276, P3 251, P5 276, P6 276 |
| M9 | passes: the counts kept for the second pass | P1 276, P2 276, P3 251, P5 276, P6 276 |
| M13 | sorted: one copy too many to the right | P1 349, P2 349, P4 360, P5 264, P6 349 |
| M14 | sorted: the run's first index left out of its sum | P1 247, P2 242, P3 251, P4 360, P5 205, P6 247 |
| M15 | sorted: a run's next index skipped | P1 159, P2 146, P3 260, P4 276, P5 159, P6 159 |
| M17 | struct: the first gap left out | P1 276, P2 147, P3 132, P5 182, P6 276 |
| M21 | struct: the step taken backwards | P1 251, P2 147, P3 214, P5 6, P6 251 |
| M22 | struct: a pair left unanswered | P1 94, P3 56, P5 94, P6 94 |
| M23 | iter: the prefix sums exclusive | P1 349, P2 349, P4 360, P5 212, P6 349 |
| M27 | iter: the indices counted from the end | P1 170, P3 250, P4 276, P5 83, P6 170 |
| M33 | iter: the prefix sums seeded with 1 | P1 360, P3 360, P4 360, P5 268, P6 360 |
| M30 | solution: the values folded modulo 1000 | P3 1, P4 1 |
| M31 | solution: the copies to the right uncorrected | P1 264, P2 173, P5 97, P6 264 |

P1 and P6 kill sixteen, P5 fifteen, P2 twelve, P3 eleven and P4 seven.
P5 sees an answer that is negative, odd in sum or nonzero for a lone
value. P2 sees the edits that treat the copies before an index unlike
those after it; it misses the ones that are wrong the same way from
both ends (M8, M22, M27, M33). P4 sees an error that grows with the
array's length, which a 0 appended at the end moves: a copy too many
(M13), a sum short by an index (M14, M23, M33), a skipped index (M15),
and indices counted from the end (M27). P3 sees the edits that answer
a value's first copy wrongly or forget it. M30 is the one kept edit P1
misses: the random values reach 1000 but not 0, so folding them modulo
1000 merges nothing until P3 and P4 bring in a 0 beside a 1000.

Of the thirty-four, seventeen were not kept. Two are equivalent: the ★
arm skipping a value seen once, whose answer is the 0 already there,
and the sorted arm keyed on the value alone, since `sort_by_key` is
stable and keeps each run's indices in order. Eight fail as a kept one
does: one copy too many to the right in the ★ and iter arms, and the
iter arm's index counted before itself, as M13; the iter arm's total
short by the first index as M14; the passes arm's first-pass sum never
growing as M7; its second pass overwriting the first and the Rust arm's
first copy skipped as M9; the sorted arm's runs descending as M8. Seven
are killed with checks of their own but were left out because their
arms keep their share: an index counted among those after it in the ★
and Rust arms (P1 349, P2 349, P4 360, P5 256), the struct arm's step
weighed one more (P1 276, P2 276, P3 251, P5 136), taken from the first
index (P1 251, P2 251, P3 214, P5 169) or its first index never
answered (P1 276, P2 276, P3 214, P5 276), the Rust arm's running sum
adding the rank (P1 171, P2 174, P3 214), and the iter arm's copies to
the left each one nearer (P1 276, P2 276, P3 251, P5 149).

## Verification

Every arm prints the same output as `intervals.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.7 s to 1.2 s, most of it the
two arrays of 100000 values, and the differential 3.3 s; compiled it
takes 0.4 s.

`karac fix` carries the template in four rounds of 20, 2, 4 and 3
edits: Rust's spellings (`Vec<..>` and `HashMap<..>` to `[..]`, the
`use` line dropped, the `&v`, `&i` and `|&x|` patterns to plain ones,
`Vec::new` and `HashMap::new` to `.new`, `struct Solution;` to `struct
Solution {}` and `::` to `.`); then `HashMap` to `Map`; then
`Vec[usize]` to `Vec[i64]` with the `as i64` on the length and the rank
dropped and the `0i64` suffix with them; then `vec![0; n]` to
`Vec.filled(n, 0)` and the last two casts dropped. The casts leave `let
k = k;`, `let x = i;` and `map(|x| x)` behind, which nothing flags.

## Benchmarks

The bench builds 40 arrays of 50000 values once, from 1 to 10, 100,
1000 or 10000 in turn, then solves every array 20 times, one value
raised by one before each solve so that no solve repeats one before,
with the ★ arm in all five languages; the C mirror's map is an open
addressing table of growable lists. Every implementation prints `800
solves: distances sum to 925816799380256, checksum 877035943`.

BENCHTAB
