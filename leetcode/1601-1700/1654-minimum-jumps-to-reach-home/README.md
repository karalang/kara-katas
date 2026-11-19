# 1654. Minimum Jumps to Reach Home

A certain bug's home is on the x-axis at position `x`. Help them get
there from position `0`.

The bug jumps according to the following rules:

- It can jump exactly `a` positions **forward** (to the right).
- It can jump exactly `b` positions **backward** (to the left).
- It cannot jump backward twice in a row.
- It cannot jump to any `forbidden` positions.

The bug may jump forward **beyond** its home, but it **cannot jump** to
positions numbered with **negative** integers.

Given an array of integers `forbidden`, where `forbidden[i]` means that
the bug cannot jump to the position `forbidden[i]`, and integers `a`,
`b`, and `x`, return *the minimum number of jumps needed for the bug to
reach its home*. If there is no possible sequence of jumps that lands
the bug on position `x`, return `-1`.

```
forbidden = [14,4,18,1,15],       a = 3,  b = 15, x = 9   ->  3
forbidden = [8,3,16,6,12,20],     a = 15, b = 13, x = 11  ->  -1
forbidden = [1,6,2,14,5,17,4],    a = 16, b = 9,  x = 7   ->  2
```

**Constraints:** `1 <= forbidden.length <= 1000`;
`1 <= a, b, forbidden[i] <= 2000`; `0 <= x <= 2000`; all the elements
in `forbidden` are distinct; position `x` is not forbidden.

## Approaches

| file | mechanism |
|---|---|
| `minimum_jumps.kara` ★ | a breadth-first search over (position, whether the last jump was backward), with a `VecDeque`; positions never pass the largest of x and the forbidden positions plus a + b, past which no shortest path needs to go. O(limit) |
| `minimum_jumps_levels.kara` | the same search one level of jumps at a time, the states in a `Set` of pairs and the blocked positions in a `Set`. O(limit) |
| `minimum_jumps_relax.kara` | the states as a graph of one-jump edges and Bellman-Ford relaxation until nothing improves: no queue at all. O(limit^2) at worst |
| `minimum_jumps_solution.kara` | LeetCode's Rust template: a `VecDeque` of (position, backward, steps), a `HashSet` of visited states, positions capped at 6000. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's three examples, home at 0
(0), home one jump away (1), and a home reached only by jumping past it
and back (2); then the jumps summed, how many problems cannot be solved
and a checksum for 3000 random problems with a, b, x and the forbidden
positions up to 12, 300 up to 200 and 20 up to 2000. Most random
problems cannot be solved: x must be a combination of a and b that the
no-two-backward rule allows. `minimum_jumps.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every sequence of jumps that never lands on a forbidden
position or below 0 and never jumps backward twice in a row, searched
breadth first over positions up to ten times the sum of every number in
the problem, a cap no shortest path comes near. It checks 3000 random
problems with a and b from 1 to 12, x from 0 to 12 and up to 6
forbidden positions from 1 to 12. Every problem is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the forbidden positions in reverse order give the same answer |
| P3 | one more forbidden position never makes home nearer |
| P4 | a, b, x and every forbidden position doubled give the same answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 81385548, 60000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: two backward jumps in a row allowed | P1 401, P5 401 |
| M2 | ★: a backward jump recorded as forward | P1 401, P5 401 |
| M3 | ★: the cap at the largest of x and the forbidden positions, without a + b | P1 380, P3 29, P5 380 |
| M4 | levels: the forbidden positions ignored | P1 712, P5 712 |
| M5 | levels: each level counted as two jumps | P1 982, P5 982 |
| M6 | relax: two backward jumps in a row allowed | P1 401, P5 401 |
| M7 | relax: home reached backward never counted | P1 352, P5 352 |
| M8 | relax: forward jumps onto forbidden positions allowed | P1 545, P5 545 |
| M9 | template: the backward jump `a` long | P1 527, P5 527 |
| M10 | template: one jump too many reported | P1 1207, P5 1207 |

## Benchmarks

The bench draws 5000 random problems with a, b and x up to 2000 and up
to 1000 forbidden positions, LeetCode's largest, all of them first, then
answers each by the ★ arm in all five languages. Most cannot be solved,
so most searches visit every state below the cap. Every implementation
prints `5000 problems up to 2000: jumps sum to 647895, 4369 unreachable,
checksum 520322885`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ee08f070a` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.040 s |
| Kāra (`karac build`) | 0.041 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.041 s |
| Rust (`rustc -O`) | 0.041 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.042 s |
| Go | 0.127 s |
| Python | 4.5 s |

The sequential Kāra build is level with Rust and level with Rust with
overflow checks on, the equal-safety comparison (BENCHMARKS.md). C is
the fastest here at 0.040 s.

The ★ arm first kept its seen marks as `Vec.filled(limit + 1, [false,
false])`, as Rust's `vec![[false, false]; n]` reads, and the Kāra build
took 0.550 s, thirteen times Rust's. In Kāra a list literal is a `Vec`
by default (design.md § List literals), so each of the 4000 or so marks
was a heap `Vec[bool]` of its own, cloned in by `Vec.filled` for every
problem; the fixed pair is `[false; 2]`, an `Array[bool, 2]` held
inline, which is also what the Rust and C mirrors hold. Nothing in
`karac check` points this out; that is B-2026-11-19-102.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.032 s and
0.036 s on one run).

## Verification

All four arms print the same output as `minimum_jumps.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `ee08f070a`.

## Writing it

The ★ and relaxation arms negated with Rust's `!`, which `karac fix`
turned into `not`, and lost the `as i64` on `blocked[f as i64]`. The
levels arm also took `*forbidden.iter().max().unwrap_or(&0)`, whose `&`
the fix dropped, and wrote `vec![..]`, which became list literals.

The levels arm's `[(0, false)]`, rebuilt each round as `[(p + a,
false)]`, met an `i32` position and was refused with no fix: the literal
did not reach the refusal through the rebuilt list. Since kara
`bd214fffc0` it does, and `karac fix` writes `[(0i32, false)]`.

LeetCode's Rust template takes one `karac fix` of 24 edits: the `use
std::collections::{HashSet, VecDeque};` line dropped, `struct Solution;`
to `struct Solution {}`, `Vec<i32>` to `Vec[i32]`, `HashSet<..>` and
`HashSet::new()` to `Set[..]` and `Set.new()`, `VecDeque::new()` to
`VecDeque.new()`, `forbidden.into_iter()` on the borrowed parameter to
`forbidden.clone().into_iter()`, `&next` and `&prev` to `next` and
`prev`, `&&` to `and` and `!` to `not`. Since kara `bd214fffc0` the same
pass also writes the queue's first entry `(0i32, false, 0)`, the literal
followed from the `while let Some(..) = queue.pop_front()` that reads it
to the `i32` it meets.