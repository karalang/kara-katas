# 2293. Min Max Game

You are given a **0-indexed** integer array `nums` whose length is a
power of `2`.

Apply the following algorithm on `nums`:

1. Let `n` be the length of `nums`. If `n == 1`, **end** the process.
   Otherwise, **create** a new **0-indexed** integer array `newNums` of
   length `n / 2`.
2. For every **even** index `i` where `0 <= i < n / 2`, **assign** the
   value of `newNums[i]` as `min(nums[2 * i], nums[2 * i + 1])`.
3. For every **odd** index `i` where `0 <= i < n / 2`, **assign** the
   value of `newNums[i]` as `max(nums[2 * i], nums[2 * i + 1])`.
4. **Replace** the array `nums` with `newNums`.
5. **Repeat** the entire process starting from step 1.

Return *the last number that remains in* `nums` *after applying the
algorithm*.

```
nums = [1,3,5,2,4,8,2,2]   ->  1
nums = [3]                 ->  3
```

**Constraints:** `1 <= nums.length <= 1024`; `1 <= nums[i] <= 10^9`;
`nums.length` is a power of `2`.

Play it. Each round writes only the first half of the array and reads
pair `i` before slot `i` is overwritten, since `2i >= i`, so the rounds
can run in place. O(n) in all, n/2 + n/4 + ...

## Approaches

| file | mechanism |
|---|---|
| `game.kara` ★ | the rounds in place on a clone, the length halved each round, slot `i` the `min` or `max` of `a[2i]` and `a[2i + 1]` by the parity of `i` |
| `game_naive.kara` | the statement's steps as written: a fresh `newNums` of `Vec.filled(n / 2, 0)` each round, then `nums = new_nums` |
| `game_tree.kara` | the rounds as a tournament tree: a block ends as the minimum or maximum of its two halves, the left half by a minimum and the right half by a maximum, and the root by a minimum; recursion over the halves |
| `game_struct.kara` | `enum Pick { Min, Max }` chosen by `Pick.at(i)`, and `struct Round` that makes the next round until it is `done` |
| `game_iter.kara` | each round `chunks(2)`, `into_iter`, `enumerate`, a `map` to the pair's `min` or `max` by the index, and `collect` |
| `game_solution.kara` | LeetCode's Rust template: `mut nums: Vec<i32>` in, `i32` out; the rounds in place with `std::cmp::min` and `std::cmp::max`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; two
numbers; a rising and a falling run of eight; four equal numbers; the
largest number the constraints allow beside the smallest; then 3000
random arrays of 1 to 1024 numbers, a power of two, from 1 to 10^9,
with a checksum and the sum of the answers. `game.py` mirrors the ★ arm
and its output is byte-identical.

`karac fix` carries the template in one call, reporting 8 edits:
`struct Solution;` to `struct Solution {}`; the parameter `mut nums:
Vec<i32>` to `nums: own Vec[i32]` with `let mut nums = nums;` at the
top of the body, and the brackets of the `Vec<i32>`; `std::cmp::min`
and `std::cmp::max` to plain `min` and `max`; and in the adapter the
`as i64` on the template's `i32` answer dropped. In the iterator arm,
written first as Rust would, `round.chunks(2).enumerate()`, `chunks`
is a method of `Vec` that returns a `Vec[Slice[i64]]`, not an iterator
(collections.md), and `karac fix` adds the `.into_iter()`: 1 edit. It
placed it on the `.chunks(2)` line of the chain; the arm keeps it on a
line of its own.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every round kept as a list of its own; to make the next,
first each even index `i` is filled with `min(nums[2 * i], nums[2 * i +
1])`, by `step_by(2)` from 0, then each odd one with the `max`, by
`step_by(2)` from 1, until a round of one number. It checks 300 random
arrays of 1 to 256 numbers, a power of two, from 1 to 10^9; then 30 of
numbers from 1 to 3, so that most pairs tie; then 30 of those sorted,
rising or falling. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer is one of the numbers, and no larger than either of the first two |
| P3 | the right half all made the largest number: the answer of the left half alone |
| P4 | each pair's two numbers swapped: the same answer |
| P5 | the left half all made the smallest number: that number |
| P6 | each arm agrees with at least three of the other five |

P2, P3 and P5 follow from the tree: the root is the minimum of the left
half's answer and the right half's, and the left half's answer is in
turn at most the minimum of its own first pair. A right half of the
largest number can only lose that minimum, and a left half of the
smallest can only win it.

The differential prints `360 cases: checksum 229200793, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading by list
comprehension. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: min and max swapped | P1 319, P2 308, P3 245, P5 245, P6 319 |
| M4 | ★: one round short | P1 48, P2 19, P3 40, P4 37, P6 48 |
| M6 | ★: a round's last slot left as it was | P1 29, P3 22, P6 29 |
| M7 | naive: the odd slots the minimum too | P1 218, P6 218 |
| M8 | naive: an odd slot copying the slot before | P1 91, P6 91 |
| M9 | naive: the right of each pair skipped | P1 201, P2 156, P4 295, P6 201 |
| M12 | tree: the root a maximum | P1 316, P2 266, P3 248, P5 296, P6 316 |
| M15 | tree: the left half a maximum | P1 270, P2 260, P3 254, P6 270 |
| M16 | tree: the right half from its middle | P1 108, P4 136, P6 108 |
| M17 | struct: the pick by half the index | P1 160, P6 160 |
| M18 | struct: a max for a min | P1 320, P2 309, P3 137, P5 301, P6 320 |
| M20 | struct: the pairs shifted | P1 241, P2 41, P4 280, P6 241 |
| M24 | iter: chunks of four | P1 105, P6 105 |
| M25 | iter: the pair's right twice | P1 149, P4 187, P6 149 |
| M26 | iter: every fourth slot a maximum | P1 47, P6 47 |
| M28 | solution: slot 0 the maximum | P1 320, P2 309, P3 203, P5 296, P6 320 |
| M29 | solution: the even slot from the odd pair | P1 264, P2 113, P3 277, P4 231, P5 233, P6 264 |

P1 and P6 kill all seventeen, P2 nine, P3 eight, P4 six and P5 five.
P4, the pairs swapped, catches the edits that read one number of a
pair and not the other. P2, P3 and P5 catch the edits that change what
the first pair or the root does. Five edits, which change only which
slots take a minimum and which a maximum further in, are caught by P1
and P6 alone: every answer they give is still one of the numbers, and
still the first pair's minimum or smaller where the root and the left
edge are untouched.

The first draft's P2 was only that the answer is one of the numbers,
its P3 every number plus 1000, the answer plus 1000, and its P5 the
array written twice, no larger answer. Every edit an arm can take
picks numbers by comparing them, so the first two killed none of the
thirty-one and the third one; they were replaced by the three above.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. They fail as a kept one does: the minimum always
taken in the ★, tree, iter and template arms (M2, M13, M22, M27) as the
naive arm's odd slots the minimum too (M7); the ★ arm's pair's left
only (M3) as the naive arm's right of each pair skipped (M9); the ★
arm's pairs overlapping and the template's one round only (M5, M31) as
the naive arm's odd slot copying the slot before (M8); the naive arm's
parity reversed, the tree arm's rule turned round and the iter arm's
index from one (M10, M14, M23) as the ★ arm's min and max swapped (M1);
the naive arm's odd slots their pair's right (M11) as the iter arm's
pair's right twice (M25); the struct arm's round done at two (M19) as
the ★ arm's one round short (M4); the struct arm's pair dropped from
each round (M21) as the ★ arm's last slot left as it was (M6); and the
template's parity of `n` (M30) as the tree arm's root a maximum (M12).

Seven edits of the first draft were replaced. Four passed every check,
because each reads the last round, whose length is 1: the naive arm's
answer the last number, the struct arm's answer the largest left, the
iter arm's answer the round's last, and the tree arm's halves split
unevenly, which split every power of two evenly all the same. Three
failed exactly as another arm's edit did: the ★ arm's parity by the
pair's first index, the naive arm's rounds stopped at two and the
struct arm's pick by the pair's index. They are now M6, M8, M11, M15,
M17, M21 and M26.

## Verification

Every arm prints the same output as `game.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 1 to 1.7 s, except the
iterator arm, which builds a `Vec` of slices and then a new `Vec` for
every round: 3.9 s. The differential takes 1.7 s.

## Benchmarks

The bench builds 200 arrays of 1024 numbers from 1 to 10^9 once, then
makes 50 passes over all of them summing the answers, with the ★ arm
in all five languages; each call plays on a copy of its array. Every
implementation prints `50 passes over 200 arrays of 1024: checksum
295758045`. C and Go pick the pair's minimum or maximum with one
comparison against the parity, where the others call `min` or `max`.

BENCHTAB
