# 1752. Check if Array Is Sorted and Rotated

Given an array `nums`, return `true` *if the array was originally sorted
in non-decreasing order, then rotated **some** number of positions
(including zero)*. Otherwise, return `false`.

There may be **duplicates** in the original array.

**Note:** An array `A` rotated by `x` positions results in an array `B`
of the same length such that `B[i] == A[(i+x) % A.length]` for every
valid index `i`.

```
nums = [3, 4, 5, 1, 2]    ->  true     [1, 2, 3, 4, 5] rotated by 2
nums = [2, 1, 3, 4]       ->  false
nums = [1, 2, 3]          ->  true     rotated by 0
```

**Constraints:** `1 <= nums.length <= 100`; `1 <= nums[i] <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `rotated.kara` ★ | a sorted array rotated by any amount falls at most once walking around it in a circle, last value back to first included, and any other array falls at least twice; the neighbours come from `windows(2)` and the wrap is compared on its own. O(n) |
| `rotated_try.kara` | every start tried: the array read from it around the circle is checked for being non-decreasing with nested `any` and `all`. O(n^2) |
| `rotated_sort.kara` | the array is a rotation of its sorted copy exactly when the sorted copy appears in the array written twice over; every offset is compared as a slice. O(n^2) |
| `rotated_solution.kara` | a Rust solution as LeetCode's Rust users write it, the drops around the circle counted with `nums[(i + 1) % n]`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's three examples, then one
value, all equal values, a rotation with equal values across the cut,
and two drops; then how many arrays answer true and a checksum for 3000
random arrays of up to 6 values from 1 to 3 and 3000 of up to 100 from
1 to 100, LeetCode's limits. Half of each batch is sorted and rotated,
and every other one of those then has one value changed. `rotated.py`
mirrors the ★ arm and its output is byte-identical.

```
true
false
true
true
true
true
false
3000 arrays of up to 6 values from 1 to 3: 2442 sorted and rotated, checksum 221338880
3000 arrays of up to 100 values from 1 to 100: 860 sorted and rotated, checksum 247826205
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the array sorted, and every rotation `x` of it compared with
the array index by index. It checks 3000 random arrays of 1 to 7 values
from 1 to 4, half of them sorted and rotated. Every case is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the array rotated by one gives the same answer |
| P3 | the array reversed and negated gives the same answer |
| P4 | the array sorted answers true |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 38530981, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading, every rotation of the sorted list compared, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. A first M7, the sorted copy compared
on all but its last value, is equivalent, since a rotation with the
same values that matches on all but one place matches on that one too,
and was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: two equal neighbours counted as a drop | P1 1181, P2 270, P4 1931, P5 1181 |
| M2 | ★: the wrap from last to first not compared | P1 183, P2 303, P5 183 |
| M3 | ★: an equal last and first counted as a drop | P1 542, P2 793, P5 542 |
| M4 | try: the last pair of each reading not compared | P1 123, P5 123 |
| M5 | try: equal neighbours taken as out of order | P1 1432, P4 2043, P5 1432 |
| M6 | try: only the start at 0 tried | P1 1278, P2 984, P5 1278 |
| M7 | sort: the offset 0 not tried | P1 917, P2 984, P4 2852, P5 917 |
| M8 | sort: the sorted copy's repeats replaced by zeros | P1 1432, P4 2043, P5 1432 |
| M9 | solution: the wrap from last to first not counted | P1 183, P2 303, P5 183 |
| M10 | solution: two drops allowed | P1 437, P5 437 |

## Benchmarks

The bench draws 100000 random arrays of 100 values from 1 to 100,
LeetCode's limits, half of them sorted and rotated, all of them first,
then answers each 5 times by the ★ arm in all five languages. Kāra's
`windows(2)` builds a `Vec` of slices for each answer, where Rust's is
a lazy iterator and C and Go index the neighbours directly. Every
implementation prints `100000 arrays of 100 values, 5 rounds: 263835
sorted and rotated, checksum 756887813`. The C build also runs clean
under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `21cdf88b69` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.132 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.140 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.264 s |
| Kāra (`karac build`) | 0.279 s |
| C (`clang -O3`) | 0.311 s |
| Go | 0.330 s |
| Python | 4.4 s |

The sequential Kāra build takes 2.00x Rust's time and 1.89x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md).
The whole gap is the `Vec` that `windows(2)` builds for each answer: the
same bench with the count written over indices,
`(1..nums.len()).filter(|i| nums[i - 1] > nums[i])`, runs in 0.12 s,
Rust's time (B-2026-11-20-109).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.230 s and
0.243 s on one run).

## Verification

All four arms print the same output as `rotated.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★ arm was first written `nums.windows(2).filter(..)`, as Rust's
lazy `windows` reads, and took one `karac fix`: Kāra's `windows` returns
a `Vec[Slice[i32]]`, so the fix added `.into_iter()` before `filter`.
The try and sort arms checked clean as written.

LeetCode's Rust template took one `karac fix` of 6 edits: `struct
Solution {}` added, `Vec<i32>` written `Vec[i32]`, and `Solution::check`
written `Solution.check`. The `(i + 1) % n` loop and the `cnt` counter
carried over as written.

The differential and the bench checked clean as generated.
