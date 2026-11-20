# 2341. Maximum Number of Pairs in Array

You are given a **0-indexed** integer array `nums`. In one operation,
you may do the following:

- Choose **two** integers in `nums` that are **equal**.
- Remove both integers from `nums`, forming a **pair**.

The operation is done on `nums` as many times as possible.

Return *a **0-indexed** integer array* `answer` *of size* `2` *where*
`answer[0]` *is the number of pairs that are formed and* `answer[1]`
*is the number of leftover integers in* `nums` *after doing the
operation as many times as possible*.

```
nums = [1,3,2,1,3,2,2]   ->  [3,1]
nums = [1,1]             ->  [1,0]
nums = [0]               ->  [0,1]
```

**Constraints:** `1 <= nums.length <= 100`; `0 <= nums[i] <= 100`.

Removing a pair of one value changes no other value's count, so the
order of the operations does not matter: each value gives half its
count in pairs and its count's parity left over.

## Approaches

| file | mechanism |
|---|---|
| `pairs.kara` ★ | a table of 101 counts; the pairs every count's half and the leftovers its parity. O(n) |
| `pairs_sorted.kara` | sorted, equal values side by side: a walk takes two at a time where the next is the same and one alone where it is not. O(n log n) |
| `pairs_set.kara` | a `Set` of the values waiting for a partner: each value completes the pair waiting for it or waits; what still waits is left over. O(n) |
| `pairs_map.kara` | the operation done: a `Map` of counts, and each value's pairs removed one at a time while two remain. O(n) |
| `pairs_iter.kara` | iterators: each value from 0 to 100 counted by `filter` and `count`, and the pairs and leftovers by one `fold` over the counts. O(101 n) |
| `pairs_solution.kara` | LeetCode's Rust template: an array of 101 counts filled through a `&x` pattern, the pairs from `map(\|&c\| c / 2).sum()`, and the leftovers what the pairs do not take; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples; 100 of one
value; 99 of it; every value from 0 to 99 once; both ends of the range
in pairs beside a value alone; then 2000 random cases of 1 to 100
values below a spread of 1 to 101, with a checksum and the pairs and
leftovers in all. `pairs.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one call, reporting 14 edits.
`check` first reports ten errors and offers 13 edits for them: the six
brackets of the three `Vec<..>`; the four `&` of the patterns `&x`,
`|&c|` and `|&x|` dropped; `&nums` to `ref nums`; `struct Solution;` to
`struct Solution {}`; and `Solution::` to `Solution.` in the harness's
wrapper. The other one follows from those: `vec![pairs, left]` to the
list `[pairs, left]`. The array `[0; 101]` and its index `x as usize`
stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the first two equal values found and removed, again and
again while any two are equal, the removals counted and what remains
left over. No counts and no parity. It checks 300 random cases of 1 to
20 values below a spread of 1 to 10; then 30 of up to 100 values from 0
to 100; then 30 of up to 100 values below a spread of 1 to 3. All 360
are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 20 values, the answer is the literal reading's |
| P2 | twice the pairs and the leftovers make all the values, and no more are left over than there are distinct values |
| P3 | the values reversed: the same answer |
| P4 | two more of the first value: one pair more and the same left over |
| P5 | one more of the first value: one more left over, or one pair more and one fewer left over |
| P6 | each arm agrees with at least three of the other five |

The differential's case-building was first written with
`nums.iter().collect[SortedSet[i64]]().len()` for the distinct values;
`karac check` refuses the bracketed type after `collect` as a call-site
type argument, and it names the set in a `let` instead. `karac fix`
then dropped five `.clone()`s of vectors passed to parameters that only
borrow them.

The differential prints `360 cases: checksum 309560333, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and removes the same pairs. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an odd count rounded up to a pair | P1 264, P2 313, P5 360, P6 313 |
| M2 | ★: every value seen left over once | P1 218, P2 267, P5 360, P6 267 |
| M3 | ★: each value counted once | P1 258, P2 316, P4 360, P5 360, P6 316 |
| M7 | sorted: the sort left out | P1 191, P2 229, P6 240 |
| M9 | sorted: the last value never reached | P1 181, P2 220, P5 143, P6 220 |
| M10 | sorted: any value paired with the next | P1 193, P6 233 |
| M13 | set: each pair counted twice | P1 258, P2 316, P4 360, P5 204, P6 316 |
| M14 | set: a value waiting under the next value | P1 264, P2 298, P3 206, P4 325, P5 197, P6 322 |
| M15 | set: every value waiting dropped at a pair | P1 209, P2 259, P3 199, P4 207, P5 83, P6 259 |
| M17 | map: the first of each value counted twice | P1 300, P2 360, P6 360 |
| M18 | map: pairs taken only while four remain | P1 258, P2 316, P4 94, P6 316 |
| M21 | map: the first value never counted | P1 300, P2 360, P3 100, P6 360 |
| M23 | iter: every value up to v counted for v | P1 300, P2 360, P4 360, P5 360, P6 360 |
| M24 | iter: the pairs and leftovers swapped in the fold | P1 272, P2 332, P4 360, P5 360, P6 332 |
| M26 | iter: 0 never counted | P1 229, P2 270, P4 101, P5 101, P6 270 |
| M28 | solution: the pairs of 0 never summed | P1 176, P2 150, P4 101, P6 208 |
| M31 | solution: each value counted twice | P1 300, P2 360, P4 360, P6 360 |

P1 and P6 kill all seventeen, P2 sixteen, P4 and P5 ten each, and P3
three. P2 misses only the sorted arm's any value paired with the next,
which still takes the values two at a time and leaves at most one. P3,
the values reversed, fails only where an edit depends on their order: a
value waiting under the next value, every waiting value dropped at a
pair, and the first value never counted. P4, two more of the first
value, and P5, one more, fail where an edit miscounts a value's own
count as it grows; P4 misses those whose error does not move with two
more of one value, such as an odd count rounded up or every value seen
left over once, and P5 those that keep a single value's parity right,
such as pairs taken only while four remain.

Of the thirty-one, fourteen were not kept. 100 never counted fails
alike in the ★ (M4) and iter (M22) arms, and neither is kept. The pairs
and leftovers swapped in the ★ arm (M5) and the template (M30) fail as
the iter arm's swap in the fold (M24); each pair counted as its two
values in the ★ arm (M6), the set arm's leftovers taken as all the
values less the pairs (M16) and the template's (M27) as the set arm's
each pair counted twice (M13); a pair stepping one place in the sorted
arm (M8), a partner left waiting in the set arm (M12) and a pair taking
one value in the map arm (M19) as the ★ arm's each value counted once
(M3); a value alone counted twice in the sorted arm (M11) and a
leftover counted twice in the map arm (M20) as the ★ arm's odd count
rounded up (M1); the iter arm's fold starting from one pair (M25) as
the map arm's first of each value counted twice (M17); and the
template's leftovers counted from the table (M29) as the iter arm's
every value up to `v` counted for `v` (M23).

## Verification

Every arm prints the same output as `pairs.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.25 to 0.6 s but the iter arm,
which counts each of the 101 values by a walk over the array, 5.7 s.
The differential takes 3.7 s there and 0.55 s under `karac
__mir-llvm-run`.

## Benchmarks

The bench builds 10 arrays of `10^5` values from 0 to 100 once, from a
scramble that never repeats, then makes 50 passes, pass `p` folding
each answer plus `p` into the checksum, with the ★ arm in all five
languages. Every implementation prints `50 passes over 10 arrays of
10^5 values: checksum 695574603`. Each allocates its 101 counts afresh
for every call, as 64-bit integers.

BENCHTAB
