# 1658. Minimum Operations to Reduce X to Zero

You are given an integer array `nums` and an integer `x`. In one
operation, you can either remove the leftmost or the rightmost element
from the array `nums` and subtract its value from `x`. Note that this
**modifies** the array for future operations.

Return *the **minimum number** of operations to reduce* `x` *to
**exactly*** `0` *if it is possible, otherwise, return* `-1`.

```
nums = [1,1,4,2,3],     x = 5   ->  2
nums = [5,6,7,8,9],     x = 4   ->  -1
nums = [3,2,20,1,1,3],  x = 10  ->  5
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^4`;
`1 <= x <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `operations.kara` ★ | removing from both ends leaves a contiguous middle summing to the total less x, so the fewest operations keep the longest such middle; the numbers are positive, so a sliding window finds it. O(n) |
| `operations_map.kara` | every suffix sum up to x in a `Map` from sum to length, then each prefix up to x looks up the suffix that makes up the rest, the two never overlapping. O(n) |
| `operations_pointers.kara` | the longest prefix not over x, then suffix numbers added one at a time and prefix numbers dropped until the sum is back at or under x, each exact hit counted. O(n) |
| `operations_solution.kara` | LeetCode's Rust template: the ★ arm's sliding window on `i32`s. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's three examples, x the
whole array (3), x one end (1), and x more than the whole array (-1);
then the operations summed, how many problems cannot be solved and a
checksum for 3000 random arrays of up to 10 numbers to 5, 1000 of up to
1000 numbers to `10^4` and 20 of up to `10^5` numbers to `10^4`, half of
the x's a prefix plus a suffix of the array. `operations.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every way of removing some numbers from the left end and some
from the right, together never more than the array holds, and the
fewest whose removed numbers sum to x. It checks 3000 random arrays of 1
to 8 numbers from 1 to 5, each with an x from 1 to 40. Every problem is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the array reversed gives the same answer |
| P3 | every number and x doubled give the same answer |
| P4 | x put at the front of the array takes one operation |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 948372860, 60000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends; two of them stop the program with an
index out of bounds, the window's left end run off the array. Three
first tries survived and were replaced, each equivalent: the map arm
storing suffix sums past x, which no lookup of `x - prefix` reaches; the
map arm allowing a prefix and suffix to share one number, which needs a
sum past the whole array and so lands on the -1 it already reports; and
the two-pointer arm's `left > right` stop, which the sum check already
makes.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: at most one number dropped per step | P1 32, P2 62, P5 32 |
| M2 | ★: the middle one shorter than it is | P1 722, P4 3000, P5 722 |
| M3 | ★: no early -1 when x passes the total | index out of bounds |
| M4 | map: each suffix one longer than it is | P1 418, P2 376, P5 418 |
| M5 | map: the "suffix" sums taken from the left | P1 490, P2 724, P5 490 |
| M6 | map: no empty suffix | P1 138, P2 279, P4 2928, P5 138 |
| M7 | pointers: the first prefix number never dropped | P1 115, P2 226, P5 115 |
| M8 | pointers: a whole-prefix answer never counted | P1 138, P2 279, P4 2928, P5 138 |
| M9 | template: one operation too few reported | P1 722, P4 3000, P5 722 |
| M10 | template: the window's left end moved two at a time | index out of bounds |

## Benchmarks

The bench draws 1000 random arrays of `10^5` numbers from 1 to `10^4`,
LeetCode's largest, each x a random prefix of up to 999 numbers plus a
random suffix of up to 999, all of them first, then answers each by the
★ arm in all five languages. Every implementation prints `1000 arrays of
100000 numbers: operations sum to 974771, checksum 90028795`. The C
build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ee08f070a` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.557 s |
| Kāra (`karac build`) | 0.582 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.591 s |
| Rust (`rustc -O`) | 0.594 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.619 s |
| Go | 1.080 s |
| Python | 36 s |

The sequential Kāra build is level with Rust and level with Rust with
overflow checks on, the equal-safety comparison (BENCHMARKS.md). C is
the fastest here at 0.557 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.412 s and
0.648 s on one run).

## Verification

All four arms print the same output as `operations.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `336218278`.

## Writing it

The ★, map and two-pointer arms checked clean as first written.

LeetCode's Rust template takes one `karac fix` of 5 edits:
`struct Solution;` to `struct Solution {}`, `Vec<i32>` to `Vec[i32]`,
the turbofish dropped from `nums.iter().sum::<i32>()`, its `let target:
i32` already naming the type, and `0usize` to `0`. The arm then checks
and agrees with no hand edit.
