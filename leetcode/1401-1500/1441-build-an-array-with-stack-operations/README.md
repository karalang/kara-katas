# 1441. Build an Array With Stack Operations

You are given an integer array `target` and an integer `n`. You have an
empty stack with the two following operations: `"Push"` pushes an
integer to the top of the stack, and `"Pop"` removes the integer on the
top of the stack. You also have a stream of the integers in the range
`[1, n]`. Use the two stack operations to make the numbers in the stack
(from the bottom to the top) equal to `target`. If the stream of the
integers is not empty, pick the next integer from the stream and push it
to the top of the stack. If the stack is not empty, pop the integer at
the top of the stack. If, at any moment, the elements in the stack (from
the bottom to the top) are equal to `target`, do not read new integers
from the stream and do not do more operations on the stack. Return the
stack operations needed to build `target` following the mentioned rules.

```
target = [1,3], n = 3       ->  ["Push","Push","Pop","Push"]
target = [1,2,3], n = 3     ->  ["Push","Push","Push"]
target = [1,2], n = 4       ->  ["Push","Push"]
```

**Constraints:** `1 <= target.length <= 100`, `1 <= n <= 100`, `1 <=
target[i] <= n`, `target` is strictly increasing.

Each arm is `fn build_array(target: Vec[i32], n: i32) -> Vec[String]`.

## Approaches

| file | mechanism |
|---|---|
| `build_array.kara` ★ | the stream read from 1, each number pushed, and popped again unless it is the next number of the target, until the target is built. O(n) |
| `build_array_gaps.kara` | each number of the target pushed, after a push and a pop for every number the stream gives between it and the one before. O(n) |
| `build_array_stack.kara` | the stack itself as a `Vec[i32]`: each number of the stream pushed, popped when it is not the target's number at its place, until `stack == target`. O(n · m) for m numbers in the target |
| `build_array_set.kara` | the target's numbers in a `Set[i32]`, and every number up to `target.last()` pushed, and popped again when the set does not hold it. O(n) |
| `build_array_solution.kara` | a Rust solution as LeetCode's Rust users write it (`let mut cur = 1`, `for &t in target.iter()`, a `while cur < t` pushing `"Push"` and `"Pop"`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and four
more, each case's operations joined by commas (`Push,Push,Pop,Push
Push,Push,Push Push,Push Push,Pop,Push,Pop,Push Push
Push,Pop,Push,Push,Pop,Push Push,Push,Pop,Push,Pop,Push,Push`); the
constraints' most, every number of 1 to 100, only 100, and every even
number, each with n = 100, by how many operations they take (`n = 100:
100 199 150`); and 2000 random cases of n from 1 to 100, each number
kept in the target with a drawn chance (`2000 random cases: 141532
operations, checksum 801605034`). `build_array.py` mirrors the ★ arm,
and its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★, gaps, stack and set arms check clean as first
written. The Rust solution takes one round of 12 fixes by `karac fix`'s
count: `struct Solution;` to `struct Solution {}`, `Vec<..>` to
`Vec[..]`, `Vec::new` to `Vec.new`, the `&t` pattern to `t`, and
`Solution::` to `Solution.`. Every arm's output matches on the first
run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the operations done in turn on an empty stack, a push taking
the stream's next number while there is one and a pop only while the
stack holds a number, no operation once the stack is the target, and the
stack the target at the end. LeetCode's examples, five edge cases (one
number in a stream of one, only the stream's last number, every number,
a stream far longer than the target, and every other number), the
constraints' most three ways (every number of 1 to 100, only 100, and
every even number), and 1992 random cases drawn as the harness draws
them.

| | property |
|---|---|
| P1 | the statement read literally: the operations build the target by the rules |
| P2 | a longer stream, n = 100, gives the same operations |
| P3 | as many pushes as the target's last number, and a pop for each number below it the target leaves out |
| P4 | the target less its last number gives the operations up to the push before |
| P5 | every number one more, and the stream one longer, gives a push and a pop first and then the same operations, while n is below 100 |
| P6 | the ★ arm's answer |

All 59,065 checks pass on every arm: `2003 cases: checksum 112016705,
59065 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by the gaps
between the target's numbers, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: no pop for a number the target leaves out | P1 1871, P3 1871, P5 1978, P6 7484 |
| M2 | ★: the stream's last number never read | P1 988, P2 977, P3 988, P4 638, P6 3952 |
| M3 | gaps: a push and a pop more before each number | P1 2003, P3 2003, P6 2003 |
| M4 | gaps: each gap counted from one past the number before | P1 1708, P3 1708, P6 1708 |
| M5 | stack: each number pushed one more than the stream gives | P1 2003, P2 1024, P3 2003, P4 988, P5 1024, P6 2003 |
| M6 | stack: the stream read from 2 | P1 2003, P2 1024, P3 2003, P4 988, P5 1024, P6 2003 |
| M7 | set: the target's last number never pushed | P1 2003, P3 2003, P6 2003 |
| M8 | set: the target's numbers popped and the rest kept | P1 2003, P3 1937, P5 1978, P6 2003 |
| M9 | solution: a push and a pop for the number itself too | P1 2003, P3 2003, P6 2003 |
| M10 | solution: the stream not moved on past a number the target keeps | P1 1823, P3 1823, P6 1823 |

## Benchmarks

The bench draws 1000 targets from 1 to 100, each number kept with a
drawn chance, and builds each 200 times with n = 100, folding the
operations to a checksum. Each implementation makes a fresh string for
every operation, as the ★ arm's `to_string` does, except Go's, whose
strings are immutable, so each operation appends the literal's header
and copies no bytes. Every implementation prints `2 * 10^5 targets:
checksum 752413441`.

BENCHTAB

Kāra is ahead of the rest here, measured by hand at 0.35 to 0.48 s
against Rust's 1.00 to 1.03 s (1.01 to 1.02 s with overflow checks on),
C's 1.03 to 1.12 s and Go's 2.17 to 2.26 s; Python takes 4.9 s.
