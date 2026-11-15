# 2170. Minimum Operations to Make the Array Alternating

You are given a **0-indexed** array `nums` consisting of `n` positive
integers.

The array `nums` is called **alternating** if:

- `nums[i - 2] == nums[i]`, where `2 <= i <= n - 1`.
- `nums[i - 1] != nums[i]`, where `1 <= i <= n - 1`.

In one **operation**, you can choose an index `i` and **change**
`nums[i]` into **any** positive integer.

Return *the **minimum number of operations** required to make the array
alternating*.

```
nums = [3, 1, 3, 2, 4, 3]  ->  3
nums = [1, 2, 2, 2, 2]     ->  2
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^5`.

An alternating array holds one number on every even place and another
on every odd place, so each side keeps its most frequent number and
changes the rest. When both sides favour the same number, one of them
settles for its second, so each side's two most frequent counts are
enough. O(n).

## Approaches

| file | mechanism |
|---|---|
| `alternating.kara` ★ | each side counted in a `Map` (`entry`, `or_insert`), its two best counts and their numbers kept in one walk of the map; the second taken on a clash |
| `alternating_sorted.kara` | each side's numbers sorted so that equal ones sit together, the runs measured and the two longest kept, a pad of count 0 added; every pair of runs with different numbers tried |
| `alternating_array.kara` | the counts in two `Vec.filled(100001, 0)`s indexed by the number itself, and one walk from 1 to 10^5 for each side's two best |
| `alternating_struct.kara` | a `struct Favourites` that keeps the two best `(number, count)` pairs it is `offer`ed (`mut ref self`), made for a side `of` a `SortedMap` of its counts, and asked what it can keep `beside` the other side's (`ref self`) |
| `alternating_iter.kara` | each side `skip`ped and `step_by(2)`, `fold`ed into a `Map`, sorted by `sort_by_key` on the count falling, `take(2)` and a pad `chain`ed on; the best pair of different numbers by `flat_map`, `filter` and `max` |
| `alternating_solution.kara` | LeetCode's Rust template: two `HashMap<i32, i32>`s by `entry().or_insert`, each collected into a `Vec<(i32, i32)>` and `sort_unstable_by` the count falling, `(0, 0)` pushed for a short side, `std::cmp::max`; carried by `karac fix` in four rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and five
more (one number, two the same, two different, a list already
alternating, and both sides favouring the same number with a close
second), each with its count; then the total and a checksum over 2000
random lists of 1 to 20 numbers from 1 to 2, 1 to 4 or 1 to 10^5 in
turn; then the constraints' largest, 10^5 numbers from 1 to 3, from 1 to
10^5, and one number throughout. `alternating.py` mirrors the ★ arm and
its output is byte-identical.

The ★ arm walks its `Map` in hash order, which differs from run to run,
but its answer does not: when two numbers tie, whichever is taken first
leaves the same count to keep.

The iterator arm's `fold(Map.new(), ..)` over `skip(..).step_by(2)` into
an annotated `Map[i64, i64]` was at first refused with a type mismatch
between two function types that differed only in an open variable: the
map's hidden hasher. That is ledger row B-2026-11-14-66, fixed in karac
b2eff8ea4d.

`karac fix` carries the template in four rounds of 27, 4, 3 and 1
edits: Rust's spellings (the `use` dropped, `Vec<..>` and `HashMap<..>`
to `[..]`, `HashMap::new()` to `HashMap.new()`, the `&x` pattern and the
`&` on `cmp`'s arguments dropped, `std::cmp::max` to `max`, `struct
Solution;` to `struct Solution {}`, `Solution::` to `.`, the adapter's
`&Vec<i64>` to `ref Vec[i64]`, among them); then `HashMap` to `Map`,
once the `use` that named it is gone; then `sort_unstable_by` to
`sort_by` and the adapter's widening `as i64` dropped; then the
adapter's `ref` dropped, since a parameter borrows already.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every pair of different numbers for the even and the odd
places, each one of the list's or one not in it, and the places that
differ from their side's number counted; the least. No counting of
favourites. It checks 300 random lists of 1 to 12 numbers from 1 to 2, 1
to 4 or 1 to 1000 in turn; then 30 alternating lists with a few places
changed; then 30 whose two sides favour the same number. All 360 are
drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | every number 7 more: the same count |
| P3 | the list reversed: the same count |
| P4 | every number x made 1001 - x: the same count |
| P5 | the first number dropped: the count no more, and at most 1 less |
| P6 | each arm agrees with at least three of the other five |

P2 and P4 hold since each renames the numbers one to one, and the count
reads only which places hold equal numbers. P3 holds since a reversed
list's sides are the sides reversed, swapped when the length is even.
P5 holds since dropping the first number swaps the sides: each choice of
two numbers for the list is a choice for the rest with the numbers
swapped, and changes the same places but perhaps the first.

The differential prints `360 lists: checksum 538995470, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
lists. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Twenty-eight edits to the differential, five to each Kāra arm and three
to the template, each run under `karac __mir-llvm-run` and `karac
__mir-run`. Seventeen are kept, three to each Kāra arm and two to the
Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: the odd places read from 0 | P1 148, P3 24, P5 23, P6 148 |
| M4 | ★: every place counted on both sides | P1 188, P6 188 |
| M5 | ★: a clash told by the counts, not the numbers | P1 77, P5 58, P6 77 |
| M6 | sorted: only the longest run kept | P1 86, P4 57, P5 30, P6 86 |
| M8 | sorted: the side never sorted | P1 97, P3 10, P5 1, P6 97 |
| M10 | sorted: a run started at 0 | P1 360, P6 360 |
| M13 | array: a new best not passing the old one down | P1 5, P3 2, P4 15, P5 5, P6 5 |
| M14 | array: the odd side's second its first | P1 23, P3 6, P4 35, P5 10, P6 23 |
| M15 | array: a clash settled the lesser way | P1 64, P4 52, P5 18, P6 64 |
| M16 | struct: the second offered only a lower count | P1 66, P4 101, P5 18, P6 66 |
| M19 | struct: a count started at 1 | P1 360, P5 23, P6 360 |
| M20 | struct: a clash settled by its own first only | P1 32, P3 28, P4 25, P5 45, P6 32 |
| M21 | iter: the pairs sorted fewest first | P1 45, P5 10, P6 45 |
| M22 | iter: the pad counted one | P1 49, P6 49 |
| M24 | iter: each count 1 | P1 199, P6 199 |
| M26 | solution: the evens sorted by number | P1 28, P3 24, P4 49, P5 19, P6 28 |
| M27 | solution: the odd places counted as even | P1 258, P6 258 |

P1 and P6 kill all seventeen, P5 twelve, P4 seven, P3 six and P2 none.
P5 drops the first number, and sees an edit whose count moves by more
than the one place that leaves: a clash told wrong (M5, M15, M20), the
best runs or counts lost (M6, M8, M13, M14, M16, M21), a count off by
one at every number (M19), and the ★ arm's odd side read from 0 (M3);
it misses the edits that count a place on the wrong side or a pad as
one, whose error is the same with the first number or without it. P4
turns the numbers end to end, so a tie is broken the other way, and
sees an edit that holds a tie as a clash or keeps the wrong one of two
equal counts: the longest run alone (M6), the passing down and the
second (M13, M14, M16), a clash settled one way (M15, M20), and the
template's evens sorted by number (M26). P3 reverses the list and sees
an edit that reads one end unlike the other: the odd side read from 0
(M3), a side unsorted (M8), the best kept by its place in the walk (M13,
M14, M20), and the sort by number (M26). P2 adds 7 to every number,
which no edit here tells from the numbers it had.

Of the twenty-eight, eleven were not kept. Two fail differently under
each backend, since the ★ arm walks its `Map` in hash order: the first
replaced without passing it down (M1), and a clash kept by the evens'
first only (M2). One is equivalent: the sorted arm's pad never paired
with a pad (M7), since a pad with a pad keeps 0 and is never the best.
Six fail as a kept one does: the sorted arm's runs sorted shortest
first, as M21; the array arm's odd places counted as even, as M27; the
struct arm's every place counted on both sides, as M4, and its clash
told by the counts, as M5; the iter arm's best one only, as M6; and the
template's clash kept by the evens' first only, as M20. Two were left
out to keep three to an arm: the array arm's numbers read only up to
999 (M12), which fails only P4, since a 1000 is all but absent from the
lists until P4 makes every 1 one; and the iter arm's clash allowed
(M25).

## Verification

Every arm prints the same output as `alternating.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.1 s to 3.5 s, but for the array
arm, 98 s, past the corpus's 60 s cap: it walks every number from 1 to
10^5 for each of its 2005 lists, 2 x 10^8 steps of a plain loop, which
is the arm's O(n + 10^5) and not an adapter's cost. The differential,
which holds the same arm, takes 84 s.

## Benchmarks

The bench builds one row of 400000 numbers from 1 to 1000 once; then
solves 100 windows of 100000 numbers, each at a random start, so that no
solve repeats one before, with the ★ arm in all five languages: each
counts the sides of its window in a hash map (an open-addressing table
in C). C works over a pointer and a length, the others over a slice, and
Python over the row and the window's bounds. Every implementation
prints `100 solves: checksum 160494362`.

BENCHTAB
