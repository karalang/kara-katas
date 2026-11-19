# 1649. Create Sorted Array through Instructions

Given an integer array `instructions`, you are asked to create a sorted
array from the elements in `instructions`. You start with an empty
container `nums`. For each element from **left to right** in
`instructions`, insert it into `nums`. The **cost** of each insertion is
the **minimum** of the following:

- The number of elements currently in `nums` that are **strictly less
  than** `instructions[i]`.
- The number of elements currently in `nums` that are **strictly greater
  than** `instructions[i]`.

For example, if inserting element `3` into `nums = [1,2,3,5]`, the
**cost** of insertion is `min(2, 1)` (elements `1` and `2` are less than
`3`, element `5` is greater than `3`) and `nums` will become
`[1,2,3,3,5]`.

Return *the **total cost** to insert all elements from `instructions`
into* `nums`. Since the answer may be large, return it **modulo**
`10^9 + 7`.

```
instructions = [1,5,6,2]              ->  1
instructions = [1,2,3,6,5,4]          ->  3
instructions = [1,3,3,3,2,4,2,1,2]    ->  4
```

**Constraints:** `1 <= instructions.length <= 10^5`;
`1 <= instructions[i] <= 10^5`.

## Approaches

| file | mechanism |
|---|---|
| `sorted.kara` ★ | a Fenwick tree over the values, as large as the largest: the prefix sum below a value is how many are strictly less, and what is left after the prefix through it is how many are greater. Each insertion costs the smaller, summed modulo `10^9 + 7`. O(n log m) for m the largest value |
| `sorted_insert.kara` | `nums` kept sorted, as the statement builds it: two `partition_point` searches find where the values less than the new one end and where those greater begin, and the value goes in between. O(n^2) moves in the worst case, each one block copy |
| `sorted_segment.kara` | a bottom-up segment tree of counts over the values, its leaves rounded up to a power of two: a count over a range climbs from both ends, and an insertion adds one from its leaf to the root. O(n log m) |
| `sorted_solution.kara` | LeetCode's Rust template as its Rust users write it (a Fenwick tree over LeetCode's whole value range, `const N: usize = 100_001`, `update` and `query` as nested functions), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's three examples, then one
instruction, a list rising, and one falling (all 0); then the costs
summed and a checksum for 3000 random lists of up to 8 instructions up to
5, 300 of up to 1000 up to 1000, and 3 of up to 20000 up to `10^5`.
`sorted.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: for each instruction, the values before it that are strictly
less and strictly greater are counted one by one, and the smaller is
added. It checks 3000 random lists of 1 to 10 instructions, every other
list from 1 to 3, so values repeat often, and the rest from 1 to 20.
Every list is drawn before any arm answers.

| | property |
|---|---|
| P1 | the cost is the statement read literally |
| P2 | every value v turned to top + 1 - v, which swaps less and greater, gives the same cost |
| P3 | one more instruction above every other costs nothing more |
| P4 | every value raised by 50 gives the same cost |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 614302855, 60000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. The segment arm's M8 leaves the tree
one leaf short when the largest value is a power of two, and the
insertion indexes past its end.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the values less counted through the value itself | P1 1323, P2 1425, P5 1323 |
| M2 | ★: an insertion steps up by one, not by its lowest bit | P1 2170, P2 2265, P3 1528, P4 1070, P5 2170 |
| M3 | ★: a prefix sum skips one step down | P1 2124, P2 2258, P3 2684, P4 1084, P5 2124 |
| M4 | insert: the values less taken through the value itself | P1 1323, P2 1425, P5 1323 |
| M5 | insert: the value pushed on the end, not put in order | P1 1106, P2 1422, P5 1106 |
| M6 | segment: the right end climbs on an even index | P1 1170, P2 929, P3 224, P4 774, P5 1170 |
| M7 | segment: the values greater counted from the value itself | P1 1291, P2 1425, P5 1291 |
| M8 | segment: the leaves stop one short of a power of two | `index out of bounds` |
| M9 | template: the values greater counted below the value | P1 1291, P2 1425, P5 1291 |
| M10 | template: an insertion adds two | P1 2531, P2 2473, P3 3000, P5 2531 |

## Benchmarks

The bench draws 60 random lists of `10^5` instructions from 1 to `10^5`,
LeetCode's largest, all of them first, then costs each by the ★ arm in
all five languages, each tree allocated per call. Every implementation
prints `60 lists of 100000 instructions: costs sum to 14980499427,
checksum 921702898`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

TIMINGS

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. PARNOTE

## Verification

All four arms print the same output as `sorted.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `SHA`.

## Writing it

The ★, insert and segment arms checked clean as first written.

LeetCode's Rust template first stopped at its `const N: usize =
100_001;`: a one-letter name is Type class by design.md's naming table,
and a `const` item's name must be Const class, so the check refused it
with no fix. The review thread ruled that a name after `const` is a
constant's whatever its length, and kara CONSTSHA amended CN-7 and
accepts it. The template then takes one `karac fix` of 30 edits: `struct
Solution;` to `struct Solution {}`; the nested `update` and `query`, and
the `const N` they read, hoisted to module scope; `usize` to `i64`
throughout; `&mut Vec<i32>` to `mut ref Vec[i32]` and `&Vec<i32>` to a
plain (borrowed) `Vec[i32]`, with `&bit` and `&mut bit` at the calls to
`bit` and `mut bit`; the `mut i: usize` parameters to `i: i64` with `let
mut i = i;` first in each body; `vec![0; N + 1]` to `Vec.filled(N + 1,
0)`; `for (i, &x)` to `for (i, x)`; the `lossless_cast` lint dropping
`as i64` on `less.min(greater)`; and `let mut s = 0` in `query`, which
the check found an `i64` returned as an `i32`, to `let mut s: i32 = 0`.
The arm then checks and agrees with no hand edit.
