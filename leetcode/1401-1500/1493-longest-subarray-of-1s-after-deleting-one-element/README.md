# 1493. Longest Subarray of 1's After Deleting One Element

Given a binary array `nums`, you should delete one element from it.
Return the size of the longest non-empty subarray containing only `1`'s
in the resulting array. Return `0` if there is no such subarray.

```
[1,1,0,1]            ->  3
[0,1,1,1,0,1,1,0,1]  ->  5
[1,1,1]              ->  2
```

**Constraints:** `1 <= nums.length <= 10^5`, and `nums[i]` is either `0`
or `1`.

The arms are `fn longest_subarray(nums: Vec[i32]) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `longest_subarray.kara` ★ | a sliding window holding at most one 0; the longest window, less the one element deleted. O(n) |
| `longest_subarray_runs.kara` | the run of 1s before the last 0 and the run since; a 0 joins them, and with no 0 at all one of the 1s is the one deleted. O(n) |
| `longest_subarray_dp.kara` | the 1s running into each place from the left and from the right; deleting element i joins the run that ends before it to the one that starts after it. O(n) time and space |
| `longest_subarray_groups.kara` | `nums.split(\|x\| x == 0)` into the runs of 1s between the 0s; two runs either side of one 0 join, and a single run, with no 0 to delete, loses one. O(n) |
| `longest_subarray_solution.kara` | a Rust solution as LeetCode's Rust users write it (`let (mut left, mut zeros, mut ans) = (0, 0, 0);`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples (`3 5 2`);
six edges, one 1, one 0, all 0s, a 0 at each end, two 0s side by side,
and the longest run last (`0 0 0 2 3 6`); the constraints' most, 100000
1s, the same with one 0 in the middle, and 100000 digits nine in ten 1s
(`100000 digits: 99999 | 99999 | 156`); and 3000 random arrays of 1 to
30 digits (`3000 random arrays: checksum 795810794`).
`longest_subarray.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★ arm checks clean as first written. The runs arm was
first written `let mut best = 0;`, and its two runs likewise, for
counters that take only `i32`s and are returned; an operator or a method
does not fix a literal's type (design.md §8 Literals), so check refused
both branches of the return, naming `best`, and `karac fix` declared the
three `i32`. The dp arm's `best` took the same 1 fix. The groups arm was
first written `nums.split(|x| x == 0).map(...)`; `split` gives a `Vec`
of slices, and `karac fix` added the `.into_iter()` check asked for. The
Rust solution takes one round of 10 fixes by `karac fix`'s count, and
its diff is: `struct Solution;` to `struct Solution {}`, each `Vec<i32>`
to `Vec[i32]`, `let (mut left, mut zeros, mut ans)` to `let mut (left,
zeros, ans)` and `Solution::` to `Solution.`. Every arm's output matches
on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each element deleted in turn, and the longest run of 1s in
what is left. LeetCode's examples, the edges, and 1990 random arrays of
1 to 14 digits, a 0 from one in five to four in five. Each arm meets six
properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | no more than the 1s there are, and fewer than the elements |
| P3 | the array reversed gives the same |
| P4 | a 1 more at the front gives the same or one more |
| P5 | a 0 more at the end gives the same when there was a 0 already, and every 1 when there was none |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 cases: checksum 637596919,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, deleting each
element of a list in turn, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: two 0s kept in the window | P1 1433, P2 895, P5 338, P6 5732 |
| M2 | ★: nothing deleted from the window | P1 2000, P2 1212, P5 229, P6 8000 |
| M3 | runs: the run before a 0 never joined to the one after | P1 711, P6 711 |
| M4 | runs: with no 0, nothing deleted | P1 229, P2 229, P6 229 |
| M5 | dp: the run after a deleted element counted from the element itself | P1 932, P2 148, P3 140, P4 81, P5 73, P6 932 |
| M6 | dp: each 1 counted alone from the left | P1 509, P3 655, P5 148, P6 509 |
| M7 | groups: with no 0, nothing deleted | P1 229, P2 229, P6 229 |
| M8 | groups: the first two runs never joined | P1 533, P3 532, P5 421, P6 533 |
| M9 | solution: the window holds no 0 | P1 1551, P5 229, P6 1551 |
| M10 | solution: the answer started at 1 | P1 301, P2 301, P6 301 |

## Benchmarks

The bench keeps one array of 100000 digits, nine in ten 1s, and makes
1000 calls of the ★ arm, each first flipping one digit chosen from the
checksum so far. Every implementation prints `1000 calls over 100000
digits: checksum 902629978`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.37 s against Rust's 0.34 s (0.41 s with overflow checks
on), C's 0.35 s and Go's 0.42 s; Python takes 12.4 s.
