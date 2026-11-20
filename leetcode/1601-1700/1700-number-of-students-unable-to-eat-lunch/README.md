# 1700. Number of Students Unable to Eat Lunch

The school cafeteria offers circular and square sandwiches at lunch
break, referred to by numbers `0` and `1` respectively. All students
stand in a queue. Each student either prefers square or circular
sandwiches.

The number of sandwiches in the cafeteria is equal to the number of
students. The sandwiches are placed in a **stack**. At each step:

- If the student at the front of the queue **prefers** the sandwich on
  the top of the stack, they will **take it** and leave the queue.
- Otherwise, they will **leave it** and go to the queue's end.

This continues until none of the queue students want to take the top
sandwich and are thus unable to eat.

You are given two integer arrays `students` and `sandwiches` where
`sandwiches[i]` is the type of the `ith` sandwich in the stack (`i = 0`
is the top of the stack) and `students[j]` is the preference of the
`jth` student in the initial queue (`j = 0` is the front of the queue).
Return *the number of students that are unable to eat.*

```
students = [1,1,0,0], sandwiches = [0,1,0,1]               ->  0
students = [1,1,1,0,0,1], sandwiches = [1,0,0,0,1,1]       ->  3
```

**Constraints:** `1 <= students.length, sandwiches.length <= 100`;
`students.length == sandwiches.length`; `sandwiches[i]` is `0` or `1`;
`students[i]` is `0` or `1`.

## Approaches

| file | mechanism |
|---|---|
| `lunch.kara` ★ | the queue turns until the student who wants the top sandwich reaches the front, so its order never matters: the wants of each kind counted, the sandwiches taken from the top while anyone wants the next one, and those left want the kind that ran out. O(n) |
| `lunch_queue.kara` | the queue played out in a `VecDeque`: the front student takes the top sandwich or goes to the back, until the whole queue has gone round with no one eating. O(n^2) at worst |
| `lunch_iter.kara` | the wants counted, then `take_while` over the sandwiches with a closure that takes one want of the sandwich's kind while there is one, and `count()` of the sandwiches eaten. O(n) |
| `lunch_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `[0; 2]` count indexed by `s as usize` and filled by `for &s in &students`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 7 lines: LeetCode's two examples, one student
without and with a match; then the answers summed and a checksum for
3000 random lunches of up to 12 students, 300 of up to 100 and 10 of up
to `10^4`, each lunch with its own chance from 0 to 10 in 10 that a
student or a sandwich is a 1. `lunch.py` mirrors the ★ arm and its
output is byte-identical.

```
0
3
1
0
3000 lunches of up to 12 students: answers sum to 4552, checksum 878655503
300 lunches of up to 100 students: answers sum to 1806, checksum 572150528
10 lunches of up to 10000 students: answers sum to 615, checksum 421514356
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally on two `Vec`s: while some student in the queue wants the
sandwich on top, the front one takes it if it is the kind they want
(`remove(0)` from both), or else goes to the end (`remove(0)` and
`push`); the students left are the answer. It checks 3000 random lunches
of 1 to 12 students and as many sandwiches. Every case is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the students in another order (rotated by one) give the same answer |
| P3 | every 0 and 1 swapped, in students and sandwiches, gives the same answer |
| P4 | a student and a sandwich of the same kind put in front give the same answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 502016880, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, the same queue on lists, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M6 and M9 never stop at a sandwich no
one wants, and fail the same checks, P1 and P5 alone: the rotated,
swapped and lengthened lunches go just as wrong. Only the queue arm sees
the order of the queue, so only its mutants fail P2.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a sandwich no one wants passed over, not the end | P1 771, P5 771 |
| M2 | ★: a sandwich taken from the other kind's wants | P1 1565, P4 980, P5 1565 |
| M3 | ★: the lunch over while one want of the kind is left | P1 3000, P4 185, P5 3000 |
| M4 | queue: given up one turn before the whole queue has gone round | P1 1693, P2 409, P5 1693 |
| M5 | queue: the turns counted on after someone eats | P1 910, P2 794, P5 910 |
| M6 | iter: a sandwich taken with no want left for it | P1 1677, P5 1677 |
| M7 | iter: the counts of the two kinds swapped | P1 2788, P4 3000, P5 2788 |
| M8 | solution: only the students who want a 0 counted | P1 852, P3 1677, P5 852 |
| M9 | solution: no stop at a sandwich no one wants | P1 1677, P5 1677 |
| M10 | solution: every student counted as wanting a 0 | P1 2349, P3 3000, P4 1488, P5 2349 |

## Benchmarks

The bench draws 50000 random lunches of 100 students, LeetCode's most,
all of them first, then answers each 80 times by the ★ arm in all five
languages. Every implementation prints `50000 lunches of 100 students, 80
rounds: answers sum to 38855040, checksum 857295799`. The C build also
runs clean under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 1.319 s |
| Kāra (`karac build`) | 1.367 s |
| Rust (`rustc -O`) | 1.373 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.384 s |
| Go | 1.388 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.411 s |
| Python | 22 s |

The sequential Kāra build is level with Rust and level with Rust with
overflow checks on, the equal-safety comparison (BENCHMARKS.md). C is
the fastest here at 1.319 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (1.266 s and 1.295 s on one
run).

## Verification

All four arms print the same output as `lunch.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★, queue and iter arms checked clean as first written; the iter
arm's closure decrements a count it captures from the function, and
`take_while` stops at the first `false`.

LeetCode's Rust template took one `karac fix` of 9 edits:
`struct Solution {}` added, `Vec<i32>` written `Vec[i32]`, and each
`for &s in &students` written `for s in ref students`. The `[0; 2]`
count, a fixed `Array` in Kāra too, and its `cnt[s as usize]` indexes
carried over as written: `usize` is for FFI (design.md §5), but an
index takes any integer, and nothing here meets an `i64`, so no
diagnostic fires.

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
