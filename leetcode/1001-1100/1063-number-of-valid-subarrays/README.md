# 1063. Number of Valid Subarrays

Given an integer array `nums`, return the number of non-empty contiguous
subarrays whose leftmost element is not larger than any other element in
the subarray.

```
nums = [1, 4, 2, 5, 3]  ->  11   ([1], [4], [2], [5], [3], [1,4], [2,5],
                                  [1,4,2], [2,5,3], [1,4,2,5], [1,4,2,5,3])
nums = [3, 2, 1]        ->  3    ([3], [2], [1])
nums = [2, 2, 2]        ->  6
```

**Constraints:** `1 <= nums.length <= 5 * 10^4`; `0 <= nums[i] <= 10^5`.

A subarray is valid when its first number is its smallest, so the valid
subarrays starting at `i` are the ones that end before the first later
number below `nums[i]`. The answer is the sum, over the starts, of the
distance to that next smaller number.

## Approaches

| file | mechanism |
|---|---|
| `num_valid.kara` ★ | left to right, a stack of the numbers no later number has gone below yet: each arriving number pops the ones above it and then ends one valid subarray for every start still on the stack (`stack.last().is_some_and(..)`). O(n) |
| `num_valid_brute.kara` | every start, extended one number at a time until a number falls below the first. O(n^2) |
| `num_valid_next.kara` | the next smaller number of each start, from a stack of indices walked right to left (`while let Some(top) = stack.last()`). O(n) |
| `num_valid_jump.kara` | the next smaller number by jumping: from the right, follow the chain of next-smaller links while the number there is not below, skipping every run already known not to be. O(n) amortized |
| `num_valid_tree.kara` | a segment tree of minimums (`struct MinTree`), descended for each start to the first later number below it. O(n log n) |
| `num_valid_solution.kara` | LeetCode's Rust template (`struct Solution;`, `Vec<i32>`, `for &x`, `while let Some(&top)`, `Solution::`), carried to Kāra by `karac fix`. O(n) |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 17 lines: the answers for LeetCode's three
examples and seven more; the sum and a checksum of the answers for 3000
arrays of 1 to 12 numbers below 1 to 4, and for 300 arrays of 50 to 300
numbers; and the answers for 2000 numbers rising (2001000), falling
(2000), equal (2001000), random, and in a zigzag (1002000). `num_valid.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every pair of a start and an end at or after it, counted when
no number between them, both included, is below the number at the start.
It checks 2000 arrays: 1000 of 1 to 12 numbers below 1 to 4, and 1000 of
1 to 30 below 2 to 30. Every random choice of a problem is drawn before
any arm answers, so a wrong arm cannot change the problems the others see.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer lies between the length and the length times the length plus one over two |
| P3 | the numbers renamed by a random strictly increasing map leave the answer |
| P4 | a number below every one appended at the end raises the answer by one, and a number at most every one put in front raises it by the length plus one |
| P5 | the array cut in two answers at least the halves' sum, and the array with every number raised above its largest, followed by the array itself, answers twice the array |
| P6 | each arm agrees with at least three of the other five |

The differential prints `2000 problems: checksum 474861630, 96000 checks
over 6 arms: 0 failures` under every lane in Verification; a Python
reading of the same 2000 arrays gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Fifteen are kept, two or three to
each arm. All thirty are killed, each fails the same way under both
backends, none by a crash, and no two kept ones fail the same checks. A
first segment-tree edit, pruning a node only when it ends before the
start rather than at it, survived: a node that ends at the start holds
the start itself and earlier numbers, its left child is still pruned,
and the search walks the right edge down to the start, which is never
below itself. It was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an equal number popped | P1 1612, P4 676, P6 1612 |
| M2 | ★: at most one number popped | P1 1251, P4 1829, P5 1829, P6 1251 |
| M3 | ★: a number one above never popped | P1 1307, P3 1151, P4 661, P5 624, P6 1307 |
| M4 | brute: the one-number subarray left out | P1 2000, P2 517, P4 4000, P6 2000 |
| M5 | brute: the first start dropped | P1 2000, P2 293, P4 2000, P5 2000, P6 2000 |
| M6 | brute: only non-decreasing runs | P1 1309, P4 1533, P6 1309 |
| M7 | next: no smaller number taken as the last | P1 2000, P2 290, P4 3756, P5 2000, P6 2000 |
| M8 | next: the bottom of the stack read | P1 973, P4 1533, P5 1533, P6 973 |
| M9 | next: walked left to right | P1 1549, P2 466, P4 3745, P5 2388, P6 1549 |
| M10 | jump: each jump one past the link | P1 1214, P4 1705, P5 1705, P6 1214 |
| M11 | jump: the last start dropped | P1 2000, P2 171, P5 2000, P6 2000 |
| M12 | tree: the root never filled | P1 1533, P4 2000, P5 2000, P6 1533 |
| M13 | tree: a node's minimum read off its left child | P1 1450, P4 3475, P5 2043, P6 1450 |
| M14 | solution: every number popped | P1 1829, P4 2000, P6 1829 |
| M15 | solution: the numbers halved crossing to `i32` | P1 1114, P3 1065, P4 698, P5 860, P6 1114 |

P1 and P6 kill all fifteen, P4 fourteen, P5 eleven, P2 five and P3 two.
P2 sees a count below the length, which every edit that loses a start or
a one-number subarray makes (M4, M5, M7, M9, M11). P3 sees an edit that
treats two numbers one apart differently from two far apart (M3, M15):
the increasing map moves them apart. P4's number below every one ends
every run but its own, so it sees every edit that lets a run go on past
a smaller number or stop short of the end, and its number in front sees
the edits that drop a start. M11 is the one P4 misses: a dropped last
start loses one subarray from the array and its extension alike.

Of the fifteen not kept, the equal-number edit fails as M1 in the next,
jump, tree and solution arms too, as does the solution arm not pushing a
number equal to the top. Counting before the push fails as M4, the jump
links all set to the end as M2, a number one below allowed in the brute
arm as M3, the ★ stack cleared for one number above as M6, the brute arm
and tree never reaching the last number as M7, and the next arm popping
every index and the tree returning the leaf after the one found as M12.
The jump arm never jumping past the last number and the solution arm
comparing with the bottom of the stack each fail in a way of their own.

## Verification

Every arm prints the same output as `num_valid.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file. Under `karac __mir-run` the arms take 0.5 s (next, jump) to 5.0 s (brute)
and the differential 5.9 s.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` in two rounds: the syntax (`struct Solution
{}`, `Vec[i32]`, `Vec.new()`, the `&x` and `&top` patterns dropped,
`Solution.`), then the bridge's `as i64` the widening return no longer
needs. One error has no fix, the one kata 1062 met: Rust infers `let mut
ans = 0` as `i32` from the `ans += stack.len() as i32` and the return,
and Kāra types the literal `i64`, so returning it as `i32` narrows.
Kara B-2026-11-07-57 made an assignment fix a literal, but by its ruling
a compound assignment's operand does not, so this error stays; what is
missing is its fix, the annotation (kara B-2026-11-08-20, open). Until
then the arm writes `let mut ans: i32 = 0`.

## Benchmarks

The bench builds 20 arrays of 100000 numbers, below 2 to 685902, once in
all five languages, then answers each on 50 of its suffixes (from 0, 100,
..., 4900) with the ★ arm's left-to-right stack: 1000 calls, about 97
million numbers pushed. Rust uses a `Vec<i64>` and `is_some_and`, Go a
slice, Python a list, and C a growable array of its own. Every
implementation prints `1000 calls: answers sum 122618131893, checksum
56294210`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `8cdef3b93a` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.721 to 0.918 s | 0.795 s |
| Rust (`rustc -O`) | 0.623 to 0.860 s | 0.798 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.729 to 0.878 s | 0.834 s |
| Kāra (`karac build`) | 0.833 to 0.901 s | 0.860 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.840 to 0.995 s | 0.926 s |
| Go | 0.928 to 1.093 s | 1.016 s |
| Python | 13.4 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.851 s) is below its real time, and the two lanes' ranges
overlap.

Kāra takes 1.11x the time of Rust under overflow checks, and C is no
faster than Rust. All four compiled programs run the same short loop,
whose pop test on random numbers is a branch the processor cannot
predict, so the mispredictions rather than the code around them are
likely most of the time (inferred from the shape, not measured).
