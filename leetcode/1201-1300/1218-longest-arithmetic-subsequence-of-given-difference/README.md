# 1218. Longest Arithmetic Subsequence of Given Difference

Given an integer array `arr` and an integer `difference`, return the
length of the longest subsequence in `arr` which is an arithmetic
sequence such that the difference between adjacent elements in the
subsequence equals `difference`.

A subsequence is a sequence that can be derived from `arr` by deleting
some or no elements without changing the order of the remaining
elements.

```
arr = [1,2,3,4], difference = 1                ->  4
arr = [1,3,5,7], difference = 1                ->  1
arr = [1,5,7,8,5,3,4,2,1], difference = -2     ->  4    [7,5,3,1]
```

**Constraints:** `1 <= arr.length <= 10^5`; `-10^4 <= arr[i], difference
<= 10^4`.

The arms are `fn longest_subsequence(arr: Vec[i64], difference: i64) ->
i64`. The two Rust arms keep the method LeetCode gives Rust users, on
`i32`, inside `impl Solution`, and a one-line `longest_subsequence`
narrows the values and calls it.

## Approaches

| file | mechanism |
|---|---|
| `longest_arithmetic_subsequence_of_given_difference.kara` ★ | a `Map` from each value to the longest such subsequence seen so far that ends with it; a value extends the one ending at itself minus the difference, or starts its own. O(n) expected |
| `longest_arithmetic_subsequence_of_given_difference_slots.kara` | the values lie in -10^4 to 10^4, so the same lengths sit in an array of 20001 slots, the value plus 10^4 its index; a predecessor outside that range ends nothing. O(n + 20001) |
| `longest_arithmetic_subsequence_of_given_difference_jumps.kara` | from the right: each element's next in a subsequence is the first later element holding its value plus the difference, found by a binary search in that value's list of places (a `Map` of `Vec`s filled through `entry`), and the longest subsequence starting at an element is one more than the one starting at its next. O(n log n) |
| `longest_arithmetic_subsequence_of_given_difference_ordered.kara` | the ★ arm's recurrence over a `SortedMap`, read with a `match` on `get`, and the answer taken at the end as the map's greatest length, by `values().max()`. O(n log n) |
| `longest_arithmetic_subsequence_of_given_difference_hash.kara` | a Rust solution as LeetCode's Rust users write it (a `HashMap<i32, i32>` read by `*dp.get(&(x - difference)).unwrap_or(&0) + 1` and written by `insert`, over `for &x in &arr`), carried to Kāra by `karac fix` |
| `longest_arithmetic_subsequence_of_given_difference_offset.kara` | another Rust solution (a `vec![0i32; 40001]` indexed by the value plus a `const OFFSET: i32 = 20000` declared in the function, the predecessor read only when `(-OFFSET..=OFFSET).contains(&prev)`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six more properties |

Every arm prints the same 12 lines: LeetCode's three examples; one value
(`1`); three equal values with a difference of 0 (`3`); `-10^4`, 0 and
10^4 with the difference 10^4 and the same reversed with -10^4 (`3` each);
`[4, 1, 3, 2]` with -1 (`3`); 1000 random small cases, 1 to 12 values
near 0 with a difference from -2 to 2 (`1000 small cases: lengths total
1924, checksum 327325791`); and three lines at the constraints' top,
10^5 values: random ones from -10^4 to 10^4 with the differences 3, -7
and 0 (`17` each), -10^4 to 10^4 over and over with 1 (`20001`) and -1
(`5`), and -10^4 and 10^4 in turn with 10^4 (`1`) and 0 (`50000`).
`longest_arithmetic_subsequence_of_given_difference.py` mirrors the ★
arm, and its output is byte-identical. Every arm gives the same output
under `karac run` and `karac build`, and under the AddressSanitizer
build.

The Mend loop: the ★, slots, jumps and ordered arms check clean as
written. The hash arm takes one round of 16 fixes (among them the `use`
line dropped, `HashMap<i32, i32>` to `Map[i32, i32]`, `for &x in &arr`
to `for x in ref arr`, `let mut ans = 0` to `let mut ans: i32 = 0`, and
`dp.get(&(x - difference)).unwrap_or(&0)` to `dp.get(x -
difference).unwrap_or(0)`, the leading `*` kept, since `get` gives a
reference), and the offset arm one round of 6 (among them `vec![0i32;
40001]` to `Vec.filled(40001, 0i32)`, `let mut res = 1` to `let mut res:
i32 = 1`, and `contains(&prev)` to `contains(prev)`). Both outputs match.

## Gaps

None found.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every subsequence, as a mask of the places it keeps, checked
for steps of exactly the difference, and the longest that passes. 2000
random cases: 1 to 12 values from -s to s, s from 1 to 6, with a
difference from -3 to 3; in 1208 of them the answer is more than 1.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | every value three more gives the same |
| P3 | the array reversed, with the difference negated, gives the same |
| P4 | every value negated, with the difference negated, gives the same |
| P5 | a value put at the end lengthens the answer by at most one, and never shortens it |
| P6 | between 1 and the array's length |
| P7 | the ★ arm's answer |

All 84,000 checks pass on every arm: `2000 cases: checksum 725008453,
84000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. A Python reading of
the same cases, every subsequence by `itertools.combinations`, gives the
same checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the predecessor looked for at the value plus the difference | P1 631, P7 3155 |
| S2 | ★: a value that starts a subsequence never recorded | P1 1208, P7 6040 |
| L1 | slots: the new value not counted in the length | P1 2000, P6 2000, P7 2000 |
| L2 | slots: the last value's length taken for the answer | P1 605, P3 672, P5 458, P7 605 |
| J1 | jumps: the next place may be the element itself | P1 199, P6 18, P7 199 |
| J2 | jumps: worked from the left | P1 382, P7 382 |
| O1 | ordered: the least length read off the map | P1 1199, P5 5, P7 1199 |
| O2 | ordered: a new subsequence begun at length 0 | P1 2000, P6 792, P7 2000 |
| H1 | hash: a value's first length kept | P1 177, P3 91, P7 177 |
| H2 | hash: a missing predecessor counted as one | P1 2000, P6 176, P7 2000 |
| F1 | offset: the value's own slot read for its predecessor's | P1 1007, P7 1007 |
| F2 | offset: the length stored in the predecessor's slot | P1 1007, P7 1007 |

A mutation of the ★ arm fails P7 on all six arms, the ★ arm against the
other five. P2 and P4 catch none: every arm reads the values only
through their differences, so a mutation's answer moves with the right
one when every value is shifted, or negated along with the difference.
P3, the array reversed, catches the two that depend on which occurrence
of a value comes last: L2 takes the last value's length for the answer,
and H1 keeps a value's first length rather than its latest. P5 catches
L2 too, whose answer shrinks when the value put at the end starts
nothing, and O1. P6, between 1 and the array's length, catches the
three that are wrong on every array (L1 and O2, the new value not
counted, and H2, a missing predecessor counted as one) where their
answer leaves that range, and J1, whose subsequence can count one
element twice.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (a `Map` from each value to the longest subsequence ending with it)
on 16 arrays of 10^5 values from -10^4 to 10^4, the constraints' most,
drawn once, each asked with the differences -3 to 3; every answer folded
into a checksum. Every program prints `16 arrays of 10^5 values,
differences -3 to 3: checksum 759498631`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.427 to 0.541 s | 0.459 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.424 to 0.520 s | 0.460 s |
| Rust (`rustc -O`) | 0.419 to 0.522 s | 0.449 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.430 to 0.499 s | 0.465 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.437 to 0.468 s | 0.451 s |
| C (`clang -O3`) | 0.094 to 0.117 s | 0.098 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.096 to 0.137 s | 0.102 s |
| Go | 0.445 to 0.579 s | 0.484 s |
| Python | 2.051 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (0.465 s
against 0.460 s), and the two ranges overlap. Kāra takes about 4.7x C's
time (0.460 s against 0.098 s); Kāra is about 5% ahead of Go (0.460 s
against 0.484 s). Python takes about 4x Kāra's time. No profile was
taken.
