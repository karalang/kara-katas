# 1486. XOR Operation in an Array

You are given an integer `n` and an integer `start`. Define an array
`nums` where `nums[i] = start + 2 * i` (0-indexed) and `n ==
nums.length`. Return the bitwise XOR of all elements of `nums`.

```
n = 5,  start = 0  ->  8     0 ^ 2 ^ 4 ^ 6 ^ 8
n = 4,  start = 3  ->  8     3 ^ 5 ^ 7 ^ 9
n = 1,  start = 7  ->  7
n = 10, start = 5  ->  2
```

**Constraints:** `1 <= n <= 1000`, `0 <= start <= 1000`.

The arms are `fn xor_operation(n: i32, start: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `xor_operation.kara` ★ | each number made in turn, `start + 2 * i`, and folded into the XOR as it comes. O(n) |
| `xor_operation_reduce.kara` | the numbers as an iterator chain, `map` making each one and `reduce` XOR-ing them together. O(n) |
| `xor_operation_closed.kara` | O(1): every number shares `start`'s low bit, which survives when `n` is odd; the rest, halved, are the consecutive `s, s + 1, .., s + n - 1` with `s = start / 2`, whose XOR is that of `0..=s + n - 1` against that of `0..=s - 1`, each read from `x % 4` |
| `xor_operation_bits.kara` | bit by bit: a bit of the XOR is set when an odd count of the numbers have it, so each of the 12 bits a number up to 2998 can have is counted over the numbers. O(12 n) |
| `xor_operation_solution.kara` | a Rust solution as LeetCode's Rust users write it (`(0..n).fold(0, \|acc, i\| acc ^ (start + 2 * i))`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's four examples (`8 8 7 2`);
six edges, one number from the least and the most start, the most
numbers from the least and the most start, an odd start with an even
count and an even start with an odd one (`0 1000 0 0 22 4`); every `n`
from 1 to 1000 from start 999, and every start from 0 to 1000 with `n`
1000, each folded into a checksum (`every n: checksum 855406546 | every
start: checksum 549878748`); and 3000 random pairs (`3000 random pairs:
checksum 349198830`). `xor_operation.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the reduce, closed-form and bits arms check clean as
first written. The ★ arm was first written `let mut x = 0;`, and `x ^=
start + 2 * i` keeps it an `i64`, since an operator beside an `i32` does
not fix a literal (design.md §8 Literals), so its return as an `i32` was
refused; `karac fix` declared it `x: i32`. The bits arm's same `let mut
x = 0;` checks clean, since `x |= 1 << bit`, with `bit` from `0..12`,
has only literals on both sides for the return to fix. The Rust solution
takes one round of 2 fixes by `karac fix`'s count: `struct Solution;` to
`struct Solution {}` and `Solution::xor_operation` to
`Solution.xor_operation`. Its `fold(0, ..)` stays, its seed fixed by the
return. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the array built, then its XOR. LeetCode's examples, the
edges, and 1990 random pairs, half of `n` from 1 to 20 and start from 0
to 30, half of `n` from 1 to 1000 and start from 0 to 1000. Each arm
meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | one number more XORs in `start + 2n` |
| P3 | the same count from `start + 2` differs by `start` and `start + 2n` |
| P4 | one number is itself, and two are their XOR |
| P5 | the low bit is `start`'s, kept when `n` is odd |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 cases: checksum 533628554,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, building the
array and reducing it, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the numbers step by 1, not 2 | P1 1728, P2 2000, P3 1812, P4 2000, P5 1024, P6 6912 |
| M2 | ★: the first number, start itself, left out | P1 1961, P3 2000, P4 1961, P5 997, P6 7844 |
| M3 | reduce: OR in place of XOR | P1 1892, P2 1943, P3 1919, P4 1808, P5 524, P6 1892 |
| M4 | reduce: every number 2 higher | P1 2000, P2 2000, P3 1331, P4 2000, P6 2000 |
| M5 | closed: the XOR of 0..=x taken as x when x % 4 is 2 | P1 733, P2 999, P3 1017, P4 1500, P6 733 |
| M6 | closed: start's low bit kept whatever n is | P1 524, P2 997, P4 997, P5 524, P6 524 |
| M7 | bits: a bit set when an even count have it | P1 2000, P4 2000, P5 2000, P6 2000 |
| M8 | bits: only the low 10 bits counted | P1 341, P2 750, P3 750, P6 341 |
| M9 | solution: each number's low bit flipped | P1 1009, P2 2000, P4 2000, P5 1009, P6 1009 |
| M10 | solution: the fold starts from 1 | P1 2000, P4 2000, P5 2000, P6 2000 |

## Benchmarks

The bench makes 2000000 calls to the ★ arm, each `n` from 1 to 1000 and
start from 0 to 1000 chosen from the checksum so far, so no call can be
answered before the one before it. Every implementation prints `2000000
calls: checksum 937604841`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.15 s against Rust's 0.15 s (0.15 s with overflow checks
on), C's 0.15 s and Go's 0.53 s; Python takes 61.7 s.
