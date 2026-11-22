# 2708. Maximum Strength of a Group

You are given a 0-indexed integer array `nums` representing the score of
students in an exam. The teacher would like to form one **non-empty**
group of students with maximal **strength**, where the strength of a
group of students of indices `i0, i1, i2, ... , ik` is defined as
`nums[i0] * nums[i1] * nums[i2] * ... * nums[ik]`.

Return *the maximum strength of a group the teacher can create.*

```
nums = [3,-1,-5,2,5,-9]  ->  1350
nums = [-4,-5,-4]        ->  20
```

**Constraints:** `1 <= nums.length <= 13`, `-9 <= nums[i] <= 9`.

## Approaches

| file | mechanism |
|---|---|
| `strength.kara` ★ | every number but the zeros multiplies the strength up in size, so all of them are taken; if that leaves an odd count of negatives, the one nearest zero is left behind, which costs the least. A lone number is its own answer, and a group that ends up empty, only zeros and one negative, takes a zero instead. O(n) |
| `strength_extremes.kara` | the largest and the smallest strength of any non-empty group among the numbers seen so far: a new number either starts a group alone or multiplies one of the two extremes, since a negative turns the smallest into the largest. O(n) |
| `strength_sorted.kara` | sorted, the negatives come first, most negative first, and pair up two by two into positive products while two remain; every positive is taken. A group of no pair and no positive answers the largest number, a zero or the lone negative. O(n log n) |
| `strength_subsets.kara` | every non-empty group as a mask over the numbers, each one's strength a `fold` over the indices the mask holds, the largest kept by `max`. O(2^n n); LeetCode's 13 numbers make 8191 groups |
| `strength_solution.kara` | a Rust solution as LeetCode's Rust users write it, `i32` numbers widened by `as i64`, the two extremes as a tuple and `.max()` / `.min()` chains on the three candidates, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples; one
negative alone; zero alone; a negative and a zero; one negative and two
zeros; 13 nines, LeetCode's largest group, and 13 minus nines; zeros
around one negative; then the strengths summed and a checksum for 1000
random groups of 1 to 13 from -9 to 9, and 5000 of 1 to 4 from -3 to 1,
where zeros and lone negatives are common. `strength.py` mirrors the ★
arm and its output is byte-identical.

```
1350
20
-9
0
0
0
2541865828329
282429536481
0
1000 groups: strengths sum to 100216146084, checksum 403379706
5000 groups of 1 to 4 from -3 to 1: strengths sum to 11392, checksum 102720232
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every group, built by deciding for each number in turn to
take it or not, its strength the product of what it took, the largest
over the groups that took something. It checks 800 random groups of 1 to
6 numbers from -3 to 1, where zeros and lone negatives are common; 300
of 1 to 10 from -9 to 9; and 100 of 13, LeetCode's most. Every case is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the numbers reversed: the same answer |
| P3 | a 1 added: the answer, or 1 if that is larger |
| P4 | a 0 added: the answer, or 0 if that is larger |
| P5 | the answer is at least every number and the product of all |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1200 cases: checksum 379455393, 36000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases over every group gives the same checksum. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the negative farthest from zero left out | P1 464, P3 362, P5 179, P6 464 |
| M2 | ★: an emptied group answers its product | P1 48, P4 130, P6 48 |
| M3 | extremes: the new number never alone | P1 87, P2 144, P3 257, P5 79, P6 87 |
| M4 | extremes: the smallest never tracked | P1 384, P2 237, P5 132, P6 384 |
| M5 | sorted: negatives paired from the third | P1 772, P5 249, P6 772 |
| M6 | sorted: a group of no pairs and no positives answers the smallest | P1 42, P4 144, P5 42, P6 42 |
| M7 | subsets: the empty group counted | P1 178, P6 178 |
| M8 | subsets: the last number never in a group | P1 739, P2 576, P3 482, P4 482, P5 246, P6 739 |
| M9 | solution: a negative never turns the smallest into the largest | P1 649, P2 413, P5 170, P6 649 |
| M10 | solution: the first number skipped | P1 599, P2 602, P3 130, P4 102, P5 283, P6 599 |

## Benchmarks

The bench draws `10^6` groups of 1 to 13 numbers from -9 to 9, all of
them first, then answers each 10 times by the ★ arm in all five
languages. Every implementation prints `1000000 groups of 1 to 13, 10
rounds: strengths mod 1000 sum to 3252769670, checksum 67179440`.

BENCHTAB

## Verification

All five arms print the same output as `strength.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

The subsets arm takes about 15 s under `karac __mir-run`, the
interpreter, which is why its harness's first random set is 1000 groups
rather than more.

## Writing it

The four arms of our own checked clean as first written.

LeetCode's Rust template took one `karac fix` of 6 edits: `struct
Solution {}` added, `Vec<i32>` respelled `Vec[i32]`, and `let (mut hi,
mut lo) = ..`, Rust's spelling, became `let mut (hi, lo) = ..`, Kāra's,
which makes every binding of the pattern mutable. The `as i64` widenings
carried over as written.
