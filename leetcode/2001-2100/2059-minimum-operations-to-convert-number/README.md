# 2059. Minimum Operations to Convert Number

You are given a 0-indexed integer array `nums` of distinct numbers, an
integer `start`, and an integer `goal`. There is an integer `x` that is
initially `start`, and you want to perform operations on `x` until it is
converted into `goal`. If `0 <= x <= 1000`, then for any index `i`, you
can set `x` to `x + nums[i]`, `x - nums[i]`, or `x ^ nums[i]` (bitwise
XOR). You may perform each operation any number of times, in any order.
Operations that set `x` to be out of the range `0 <= x <= 1000` are valid,
but no more operations can be done afterward. Return the minimum number
of operations needed to convert `x = start` into `goal`, and `-1` if it
is not possible.

```
nums = [2, 4, 12], start = 2, goal = 12   ->  2     (2 + 12 = 14, 14 - 2 = 12)
nums = [3, 5, 7],  start = 0, goal = -4   ->  2     (0 + 3 = 3, 3 - 7 = -4)
nums = [2, 8, 16], start = 0, goal = 1    ->  -1
```

**Constraints:** `1 <= nums.length <= 1000`;
`-10^9 <= nums[i], goal <= 10^9`; `0 <= start <= 1000`; `start != goal`;
the numbers in `nums` are distinct.

Only the 1001 values from 0 to 1000 can be operated on, so this is a
shortest path over 1001 nodes, each with `3 · n` edges, where an edge may
also land on `goal` outside the range. A breadth-first search finds it in
O(1001 · n). The approaches differ in which way they search and what they
keep the distances in.

## Approaches

| file | mechanism |
|---|---|
| `ops.kara` ★ | a breadth-first search from `start`: a `VecDeque` of `(value, steps)` pairs and a `Vec[bool]` of the values seen; every result tested against `goal` before the range, since the last step may leave it. O(1001 · n) |
| `ops_layers.kara` | the search a level at a time: a `Set` of the values reached in exactly `steps` operations, each level built from the last, the values already reached left out, until `goal` appears or a level is empty |
| `ops_backward.kara` | the search run backwards from `goal`: `y` came from `y - n`, `y + n` or `y ^ n`, and only a value from 0 to 1000 can have been operated on, so it walks those predecessors, of `goal` first (which may lie outside the range) and then of each value found, until it reaches `start`. A `Vec` with a read index is the queue |
| `ops_map.kara` | a `Map` from each value reached to its distance, a `VecDeque`, the three operations as a list of closures `Vec[Fn(i64, i64) -> i64]`, and each result tested by a `match` with a guard and a range pattern `0..=1000` |
| `ops_rounds.kara` | the distances to every value from 0 to 1000 relaxed in rounds, as Bellman-Ford does, until a round changes nothing; the answer is one more than the least distance of a value with an operation that gives `goal`. O(1001 · n) a round, as many rounds as the longest distance |
| `ops_solution.kara` | LeetCode's Rust template (`use std::collections::VecDeque`, `vec![false; 1001]` indexed `as usize`, `for &n in &nums`, `(0..=1000).contains(&y)`, `i32` throughout), carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples and six
more, each problem and its answer; then how many are unreachable, the sum
of the answers and a checksum for 400 random problems of 1 to 8 numbers,
most within 5, 50, 300 or 1500 of 0 and one in eight anywhere in the
constraints' range; then the same for 4 problems of 100 numbers.
`ops.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the set of values reachable in at most `k` operations, each
operation made from a value from 0 to 1000, grown one operation at a time
until an operation gives `goal` or the values in range stop growing. It
checks 150 random problems of 1 to 5 numbers, drawn as the harness draws
them, then 20 problems of one number `a` whose only way to `goal` passes
through 0 (`goal = -a`) or through 1000 (`goal = 1000 + a`), from a
`start` that is a multiple of `a`, so every value reached is one too. All
170 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is -1 or at least 1, and 1 exactly when one operation on `start` gives `goal` |
| P3 | the numbers listed backwards have the same answer |
| P4 | one more number never makes the answer larger, -1 counting as larger than any |
| P5 | from a value in range one operation from `start`, `goal` is out of reach exactly when it is from `start`, and otherwise at most one operation nearer |
| P6 | each arm agrees with at least three of the other five |

P5 holds because every operation can be undone by another from the same
number: from that value `start` is one operation away, and the reverse.

The differential prints `170 problems: checksum 198387208, 6120 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty-two edits to the differential, five to seven to each of its arms,
each run under `karac __mir-llvm-run`, and the kept ones and the
survivors under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed, fails
the same way under both backends and not by a crash, and no two kept
ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the steps not grown on a push | P1 112, P2 112, P6 112 |
| M2 | ★: subtraction left out | P1 63, P5 3, P6 63 |
| M3 | ★: the goal returned at the steps so far | P1 112, P2 3, P5 1, P6 112 |
| M4 | layers: 0 out of range | P1 10, P6 10 |
| M5 | layers: the next level never taken | P1 56, P5 8, P6 56 |
| M6 | layers: the steps counted once too often | P1 112, P6 112 |
| M7 | backward: the first step from the goal not inverted for subtraction | P1 26, P6 26 |
| M8 | backward: the start checked before it is reached | P1 106, P2 2, P6 106 |
| M9 | backward: the queue read from its second entry | P1 38, P3 19, P6 38 |
| M10 | map: the range stopping at 999 | P1 10, P5 1, P6 10 |
| M11 | map: a distance not grown | P1 99, P2 24, P3 35, P4 15, P5 1, P6 99 |
| M12 | map: the queue a stack | P1 93, P3 77, P4 42, P5 27, P6 93 |
| M13 | rounds: a single round | P1 63, P5 4, P6 63 |
| M14 | rounds: a shorter distance never taken | P1 19, P4 6, P5 2, P6 19 |
| M15 | rounds: the largest last step kept | P1 86, P4 2, P6 86 |
| M16 | solution: the adapter dropping the last number | P1 48, P3 60, P5 9, P6 48 |
| M17 | solution: the adapter's goal off by one | P1 105, P2 2, P6 105 |

P1 and P6 kill all seventeen, P5 nine, P2 five, P3 four and P4 four.
The 20 edge problems are what kill M4 and M10: before they were added,
150 random problems never needed a path through 0 or 1000, and the edits
that put 0 (M4) or 1000 (M10, and the ★ arm's like it) out of range
survived. P2 sees an answer of 0, from a distance never grown (M1, M11),
or a 1 that is not one operation (M3, M8, M17). P3 and P4 change the
order the search meets values in, so they catch the edits whose answer
depends on that order: a stack for the queue (M12), a distance that
grows only on odd values (M11), a queue that skips its first entry (M9),
and a relaxation that keeps the first distance found (M14). P5 checks
the answer against the answer one operation away, so it catches edits
that lose operations or levels (M2, M5, M13).

Of the thirty-two, fifteen were not kept. Three are equivalent: the ★
arm and the Rust arm with `start` never marked seen, and the layers arm
with `start` never counted reached, each let `start` be queued again two
operations on, where it can find nothing shorter. Nine fail as a kept
one or as each other: the ★ arm's 1000 out of range as M10; the layers
arm's xor as or and the map arm's xor closure an or alike; the map arm's
second closure an addition as M2, its goal one operation early as M3
and its start at a distance of one as M6; the Rust arm's `d` not grown
and the backward arm's distance not grown as M1, and the Rust arm's goal
one step short as M6. Three are killed with checks of their own but were
left out because their arm keeps three: the backward arm's range limit
kept on the goal (P1 and P6, 19 each), and the rounds arm's xor left out
on the last step (9 each) and value 1000 never relaxed (1 each).
One more edit to the backward arm, a value seen again whenever its
distance is not 1, queued values without end and ran out of memory; it
was replaced by M9.

## Verification

Every arm prints the same output as `ops.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them.
Under `karac __mir-run` the arms take 1.9 s (★) to 3.1 s (layers), except
the rounds arm at 82 s, which relaxes every value in every round, and the
differential 143 s (timed while other work shared the machine).

The map arm met two compiler gaps.

- Pushed one at a time, `ops.push(|x, n| x + n)` into a `Vec[Fn(i64, i64)
  -> i64]` was refused "type '?T0' does not implement trait Add": the
  closure was typed alone, its parameters unknown, though the element type
  names them. A closure passed for a function parameter already took its
  parameter types from the parameter; one pushed now takes them from the
  element. Fixed in kara `093c72b97d`, test `tests/kata_2059_push_closure.rs`.
  The arm keeps the list literal, which typed its closures from the
  annotation all along.
- The same message comes from any unannotated closure parameter used with
  an operator before a later use fixes its type: `let f = |x, n| x + n;
  f(1, 2)` is refused at the `+`, though design.md §8 lets the call fix
  `x` and `n`. Written first as `[|x, n| x + n, ...].to_vec()`, the arm
  got that message twice before the real refusal, that `to_vec` clones
  each element and a function value is move-only. Open as B-2026-11-10-8.

The other four Kāra arms checked as written.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in two rounds of 10 and 1 edits to a clean check: the
`std::collections` import deleted (`VecDeque` is in the prelude), `struct
Solution;` to `struct Solution {}`, `Vec<..>` to brackets, `VecDeque::new`
to `VecDeque.new`, the `&` of `for &n` dropped and the one of `&nums` made
`ref`, the `&` of `contains(&y)` dropped, `&&` and `!` to `and` and `not`,
and then `vec![false; 1001]` to `Vec.filled(1001, false)`. The fixed arm
reads as the template does.

## Benchmarks

The bench answers 16000 problems of 1 to 16 numbers, drawn as the
harness draws them, with the ★ arm in all five languages: a breadth-first
search over at most 1001 values each. C's queue is two fixed arrays of
1001; Rust's a `VecDeque`; Go's a slice read from a moving head. Every
implementation prints `16000 problems: 2540 unreachable, sum 340580,
checksum 218685012`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `093c72b97d`, on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.218 to 0.228 s | 0.223 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.281 to 0.315 s | 0.285 s |
| Rust (`rustc -O`) | 0.276 to 0.331 s | 0.289 s |
| Kāra (`karac build`) | 0.281 to 0.329 s | 0.291 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.284 to 0.306 s | 0.299 s |
| Go | 0.467 to 0.507 s | 0.484 s |
| Python | 14.9 s |  |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.290 s) is not above its real time (0.291 s).

The sequential Kāra program is 0.95x Rust under overflow checks and 1.28x
C. C's queue is a fixed array, where Kāra's and Rust's are a `VecDeque`
grown afresh for each problem and Go's a slice grown by `append`; Go
takes about twice as long as C.
