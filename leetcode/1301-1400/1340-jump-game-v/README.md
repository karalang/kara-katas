# 1340. Jump Game V

Given an array of integers `arr` and an integer `d`. In one step you can
jump from index `i` to index:

- `i + x` where `i + x < arr.length` and `0 < x <= d`;
- `i - x` where `i - x >= 0` and `0 < x <= d`.

In addition, you can only jump from index `i` to index `j` if `arr[i] >
arr[j]` and `arr[i] > arr[k]` for all indices `k` between `i` and `j`.
You can choose any index of the array and start jumping. Return the
maximum number of indices you can visit. Notice that you can not jump
outside of the array at any time.

```
arr = [6,4,14,6,8,13,9,7,10,6,12], d = 2  ->  4
arr = [3,3,3,3,3], d = 3                  ->  1
arr = [7,6,5,4,3,2,1], d = 1              ->  7
```

**Constraints:** `1 <= arr.length <= 1000`, `1 <= arr[i] <= 10^5`, `1 <=
d <= arr.length`.

The arms are `fn max_jumps(arr: Vec[i32], d: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `max_jumps.kara` ★ | a jump always lands lower, so the most indices visited from i is 1 + the most from any index it reaches; memoized depth-first search, each direction walked outward up to d steps and stopped at the first value not lower, which blocks everything past it. O(n * d), as deep as the longest descent |
| `max_jumps_sorted.kara` | no recursion: the indices taken lowest first by `sort_by_key`, so every landing place is answered before the index that jumps to it. O(n log n + n * d) |
| `max_jumps_stack.kara` | O(n): if i can jump to j, so can every index on the way that stands above j, so the only jumps that matter land from an index's nearest higher neighbour on either side. A stack of falling values finds them: a higher value pops the run of equal values on top, and each popped index is reached from the newcomer and from the new top, each within d; a value above all past the end empties the stack |
| `max_jumps_solution.kara` | a Rust solution as LeetCode's Rust users write it (a memoized `fn dfs(i: usize, arr: &Vec<i32>, d: usize, memo: &mut Vec<i32>)` nested in the method, each side scanned by a `for` over `(i + 1)..=(i + d).min(n - 1)` and over `(i.saturating_sub(d)..i).rev()` with a `break`, the answer from `(0..n).map(..).max().unwrap()`), carried to Kāra by `karac fix` |
| `max_jumps_byheight.kara` | a second Rust solution as LeetCode's Rust users write it (`idx.sort_by_key(\|&i\| arr[i])`, a `dp` of ones, each side scanned by a `while` on `usize` indices guarded by `j + 1 < n` and `j > 0`, the answer `*dp.iter().max().unwrap()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, one value,
1000 values rising, the constraints' longest, with d = 1000, and 1000
values at random up to 10^5 with d = 1000 and with d = 10 (`4 1 7 1 1000
20 10`); and 1000 random arrays of 1 to 200 values, most of them short,
from 1 to 5 or to 10^5, with d from 1 to the length (`1000 random
arrays: checksum 826885699`). `max_jumps.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the three Kāra arms check clean. The first Rust solution
takes one round of 24 fixes by `karac fix`'s count, from 11 errors: the
nested `fn dfs` hoisted to the top level, `struct Solution;` to `struct
Solution {}`, each `Vec<..>` to `Vec[..]`, `&Vec<i32>` to `ref
Vec[i32]` and `&mut Vec<i32>` to `mut ref Vec[i32]`, `&arr` and `&mut
memo` at the calls to `arr` and `mut memo`, `usize` to `i64`, `vec![0;
n]` to `Vec.filled(n, 0)`, `let mut best = 1` given its `i32`, and
`Solution::` to `Solution.`. Moving `usize` to `i64` would let
`i.saturating_sub(d)` go below zero, so the fix writes
`i.saturating_sub(d).max(0)`, which keeps the floor `usize` had. The
second takes one round of 18 fixes from 11 errors: the same kinds, with
each `&&` to `and`, `|&i|` and `for &i` to `|i|` and `for i`, and `vec![1;
n]` to `Vec.filled(n, 1i32)`. Both match on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every sequence of jumps tried from every index, with nothing
remembered, each jump checked against the whole statement, including
every value between. 2000 arrays of 1 to 8 values in four kinds, 500
each: from 1 to 3, where many values tie; from 1 to 100; the numbers 1
to n shuffled; and a zigzag, the even places from 50 to 100 and the odd
ones from 1 to 49. d is drawn from 1 to the length, and every array
before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the array read backwards: the same answer |
| P3 | every value x made 3x - 1, which keeps their order: the same answer |
| P4 | one step farther allowed: no fewer indices |
| P5 | a value above all put in front, any distance allowed: one more than the array's own answer at any distance |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 arrays: checksum 289866889,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, answering the indices lowest
first and checking every jump against the whole statement, gives the
same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the walk carried on past a value as high | P1 717, P6 2868 |
| M2 | ★: a jump of exactly d not allowed | P1 681, P6 2724 |
| M3 | sorted: the indices taken highest first | P1 1115, P5 1719, P6 1115 |
| M4 | sorted: only jumps to the right | P1 841, P2 989, P6 841 |
| M5 | stack: the jump from the left neighbour taken at any distance | P1 167, P2 249, P6 167 |
| M6 | stack: one index popped where a run of equal values stands | P1 341, P2 206, P6 341 |
| M7 | solution: the farthest index on the left never tried | P1 453, P2 916, P5 486, P6 453 |
| M8 | solution: the right side scanned past a value as high | P1 438, P2 502, P6 438 |
| M9 | byheight: the right side one step farther than d | P1 140, P2 198, P6 140 |
| M10 | byheight: an equal value let through on the left | P1 357, P2 206, P6 357 |

P1 and P6 kill all ten, P2 seven, P5 two, and P3 and P4 none. Reading
the array backwards (P2) swaps the two sides, so it catches every edit
made to one side only (M4, M5, M7, M8, M9, M10) and the stack's single
pop (M6), which treats the left of a run of equal values differently
from its right. The value put in front (P5) can jump everywhere, so its
answer rests on every other index's being right first: it catches the
highest-first order (M3), which answers the new index before any other,
and the farthest left index skipped (M7): at any distance that is
always index 0, which in front of the new value is the new value itself,
never a landing, so the lifted answer comes out right and the array's own
does not. Every arm compares values only by their
order, so stretching them (P3) catches nothing, and every edit here
still lets a larger d reach at least as far, so P4 catches nothing
either. The two ★ edits are symmetric and keep the order, so only the
statement and the ★ comparison catch them. M9 is the weakest: one step farther
matters only when the index d + 1 away on the right is lower than
everything before it, 140 of the 2000 arrays.

## Benchmarks

The bench builds 20 arrays of 1000 values, the constraints' longest,
once: half at random from 1 to 10^5 with d = 1000, where most walks stop
soon, and half rising, each value 100 more than the last give or take
99, with d = 300, where every walk to the left runs its d steps. It then
makes 20 passes, each setting one value of every array from the checksum
so far, so no answer carries over, answering every array with the ★
arm's memoized search and folding the answer plus the pass into the
checksum. Every implementation prints `20 passes over 20 arrays of 1000:
checksum 262567457`.

BENCHTAB
