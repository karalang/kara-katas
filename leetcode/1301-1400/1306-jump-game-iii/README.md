# 1306. Jump Game III

Given an array of non-negative integers `arr`, you are initially
positioned at `start` index of the array. When you are at index `i`, you
can jump to `i + arr[i]` or `i - arr[i]`; check if you can reach **any**
index with value 0.

Notice that you can not jump outside of the array at any time.

```
arr = [4,2,3,0,3,1,2], start = 5  ->  true     5 -> 4 -> 1 -> 3
arr = [4,2,3,0,3,1,2], start = 0  ->  true     0 -> 4 -> 1 -> 3
arr = [3,0,2,1,2], start = 2      ->  false
```

**Constraints:** `1 <= arr.length <= 5 * 10^4`, `0 <= arr[i] <
arr.length`, `0 <= start < arr.length`.

The arms are `fn can_reach(arr: Vec[i64], start: i64) -> bool`.

## Approaches

| file | mechanism |
|---|---|
| `can_reach.kara` ★ | a breadth-first walk from the start in a `VecDeque`, each place queued once, its two jumps tried when it comes off, true at the first place holding 0. O(n) |
| `can_reach_dfs.kara` | a recursive call for each place, which gives up on a place off the array or already seen and otherwise answers whether it holds 0 or either jump from it reaches one. O(n), as deep as the longest walk |
| `can_reach_stack.kara` | the depth-first walk without recursion, the places still to try on a `Vec` used as a stack, a place marked seen when it comes off. O(n) |
| `can_reach_sweep.kara` | the set of places reached, the start alone at first, grown by sweeping the array from left to right and marking both jumps from every place already reached, again and again until a sweep marks nothing new; then any place reached that holds 0. O(n^2) |
| `can_reach_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `std::collections::VecDeque` of `usize` places, a `vec![false; n]` of visited ones checked as each comes off, `i + arr[i] as usize` and `i - arr[i] as usize` guarded against running off either end), carried to Kāra by `karac fix` |
| `can_reach_negate.kara` | a second Rust solution as LeetCode's Rust users write it (the array taken as `mut arr` and each place marked seen by negating its value, in a `fn dfs(arr: &mut Vec<i32>, i: i32) -> bool` nested in the method, `dfs(arr, i + v) \|\| dfs(arr, i - v)`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, one place
holding 0, two places with no 0, and `5 * 10^4` places, the constraints'
most, each a jump of 1 to the right but the last, a 0, reached from the
far left, the longest walk there is (`true true false true false true`);
then 3000 random arrays of 1 to 300 places, each value below the length,
with from none to three places holding 0, and a random start (`3000
random arrays: 404 reach a 0, checksum 918686194`). `can_reach.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run` and `karac
__mir-llvm-run`, the longest walk taking the two recursive arms `5 *
10^4` calls deep.

The Mend loop: the four Kāra arms checked clean as first written. The
first Rust arm takes one round of 19 fixes by `karac fix`'s count, from 7
errors: `struct Solution;` to `struct Solution {}`, `Vec<..>` to
`Vec[..]`, `vec![false; n]` to `Vec.filled(n, false)`,
`std::collections::VecDeque::new()` to `VecDeque.new()`, since
`VecDeque` needs no path, the `usize` places made `i64`, Kāra's own
(`start as usize` to `start as i64`, and `arr[i] as usize` to `arr[i]`,
which widens to `i64` with no cast), `::` to `.`, and the wrapper's
`|&x|` to `|x|`. The second takes one round of 22 fixes from 14 errors:
the parameter `mut arr: Vec<i32>` to `arr: own Vec[i32]` with `let mut
arr = arr;` as the body's first line, the nested `fn dfs` moved to the
top level and its `&mut Vec<i32>` made `mut ref Vec[i32]`, `||` to `or`,
the call's `&mut arr` to `mut arr`, and the same `struct`, `Vec`, `::`
and wrapper rewrites; its `as usize` indexes stay as written. Both
outputs match on the first run. No gap was met.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every walk of at most n - 1 jumps from the start, each to the
right or the left, none off the array, true if one stands on a 0; a
place that can be reached at all can be reached in n - 1 jumps, since a
shortest walk never stands on a place twice. 2000 arrays of 1 to 9
places in four kinds, 500 each: values from 0 to n - 1, so that 0s are
common; values from 1 to n - 1 with one 0; jumps of 1 or 2 with one 0;
and values from 1 to n - 1 with one 0, half of them a place's distance
to the far end, so that walks bounce. 1346 reach a 0. Every array, start
and extra 0 is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the array reversed, and the start with it: the same answer |
| P3 | from each place one jump from the start: a 0 reached there is reached from the start |
| P4 | one more place given a 0: no worse |
| P5 | every 0 made a jump of 1: false, when there is more than one place |
| P6 | the ★ arm's answer |

All 75,432 checks pass on every arm: `2000 arrays: checksum 900705901,
75432 checks over 6 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Fifteen edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. Three are left out: the stack arm
never trying the start itself pushes its two jumps instead, but a start
holding 0 jumps to itself, so the edit changes nothing; the stack arm
ending the walk at the first place off the array or seen fails P1, P2
and P3 exactly as often as the ★ arm trying only the jump to the right
(M1) does; and the negating arm taking a 0 for a place already seen
answers false everywhere, as the stack arm marking its start seen (M5)
does. The twelve kept, two to each arm, are each killed, fail the same
way under both backends and not by a crash, and no two fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only the jump to the right tried | P1 427, P2 531, P3 271, P6 2135 |
| M2 | ★: the last place never jumped to | P1 238, P2 379, P3 158, P6 1190 |
| M3 | depth first: both jumps needed | P1 704, P3 392, P6 704 |
| M4 | depth first: the jump to the left one place too far | P1 385, P2 565, P3 222, P6 385 |
| M5 | stack: the start marked seen before it comes off | P1 1346, P6 1346 |
| M6 | stack: the jump to the left twice as far | P1 358, P2 485, P3 233, P6 358 |
| M7 | sweeping: one sweep only | P1 177, P2 259, P3 113, P6 177 |
| M8 | sweeping: only the start's own value asked | P1 705, P3 393, P6 705 |
| M9 | solution: no jump to place 0 | P1 227, P2 379, P3 171, P6 227 |
| M10 | solution: the walk begun at place 0 | P1 291, P2 258, P6 291 |
| M11 | negating: a place marked seen with a 0 | P1 374, P5 1433, P6 374 |
| M12 | negating: only the jump to the left tried | P1 446, P2 531, P3 238, P6 446 |

P1 and P6 kill all twelve, P3 nine, P2 eight and P5 one; P4 kills none.
Reversing the array (P2) turns every jump round, so it fails the edits
that favour one direction or one end: a jump one way only (M1, M12) or
altered to the left (M4, M6), the last place or place 0 left out (M2,
M9), a single left-to-right sweep, which follows jumps to the right
further than jumps to the left (M7), and the walk begun at place 0, which
the reversal moves to the far end (M10). It passes the edits that treat
both directions alike (M3, M5, M8, M11). A place one jump from the start
(P3) reaches no more than the start does, so P3 fails the edits that
lose places on the way; the walk begun at place 0 (M10), the start never
tried (M5) and the false 0s (M11) give the same answer from every start
and pass it. Only marking a place seen with a 0 (M11) answers true where
there is no 0 at all (P5). Every edit, right or wrong, still answers
true when a walk it takes stands on a 0, and one more 0 takes none of
those walks away, so P4 sees none of them.

## Benchmarks

The bench builds 10 arrays of `5 * 10^4` places, the constraints' most,
with jumps from 1 to 10 and one 0, once from its own generator; then
makes 300 passes, each setting one place of every array to a value from
0 to 10 and choosing the start, both from the checksum so far, so no
answer carries over, answering it with the ★ arm and folding the answer
and the pass into the checksum. Each call takes a fresh seen array and
queue: `VecDeque` in Kāra and Rust and `collections.deque` in Python; Go
reads a slice from a moving head, and C an array of n, since each place
is queued once. Every implementation prints `300 passes over 10 arrays
of 5 * 10^4: checksum 18123547`.

BENCHTAB
