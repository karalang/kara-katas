# 1846. Maximum Element After Decreasing and Rearranging

You are given an array of positive integers `arr`. Perform some
operations (possibly none) on `arr` so that it satisfies these
conditions: the value of the first element in `arr` must be `1`; the
absolute difference between any 2 adjacent elements must be less than or
equal to `1`, that is, `abs(arr[i] - arr[i - 1]) <= 1` for each `i`
where `1 <= i < arr.length`. There are 2 types of operations that you
can perform any number of times: decrease the value of any element of
`arr` to a smaller positive integer; rearrange the elements of `arr` to
be in any order. Return the maximum possible value of an element in
`arr` after performing the operations to satisfy the conditions.

```
arr = [2,2,1,2,1]     ->  2
arr = [100,1,1000]    ->  3
arr = [1,2,3,4,5]     ->  5
```

**Constraints:** `1 <= arr.length <= 10^5`, `1 <= arr[i] <= 10^9`.

The arms are `fn maximum_element_after_decrementing_and_rearranging(arr:
own Vec[i64]) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `maximum_element.kara` ★ | the numbers sorted, and each in turn made the most it may be, one more than the one before it unless it is less already. Sorted, no number is held down by a smaller one after it, so the last is the most the largest can be. O(n log n) |
| `maximum_element_count.kara` | by counting: no number can end above `n`, the count of them, so each is counted at the least of it and `n`; walking the values from 1 up, the top climbs by the numbers at a value but never past the value itself. O(n) |
| `maximum_element_heap.kara` | the ★ arm's walk with the numbers in a `PriorityQueue`, which pops the smallest first, so they come out in order without a sort. O(n log n) |
| `maximum_element_search.kara` | a binary search on the answer: a top of `h` can be reached when, sorted, the last `h` numbers can stand for 1 to `h`, the `j`-th of them at least `j`; a top that can be reached means every lower one can too. O(n log n) |
| `maximum_element_solution.kara` | a Rust solution as LeetCode's Rust users write it (the ★ arm, with `sort_unstable` on a `mut arr` parameter), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples; six edges,
a lone 1 and a lone 10^9, every number the same, the numbers in falling
order, a gap the rest climb over, and one number held down by the 1s it
must follow (`1 1 5 5 4 2`); the constraints' most, 10^5 numbers all
10^9, and 10^5 drawn from 1 to 10^9 and from 1 to 50000 (`the most:
100000 100000 50000`); and 3000 random lists of 1 to 20 numbers from 1
to 25 (`3000 random lists: checksum 563015910`). `maximum_element.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`.

The Mend loop: every arm and the harness check clean as first written.
The arms take their list as `own Vec[i64]`, as LeetCode hands it over,
and the ★ arm sorts it in place after `let mut arr = arr;`. The Rust
solution takes 22 fixes by `karac fix`'s count, and its diff is: `struct
Solution {}` added above the `impl`; Rust's `mut arr: Vec<i32>` to `arr:
own Vec[i32]`, with `let mut arr = arr;` at the body's start, which is
how Kāra writes an owned parameter the body changes; `sort_unstable()`
to `sort()`; `let mut prev = 0` to `let mut prev: i32 = 0`; `for &x in
arr.iter()` to `for x in ..`, a Kāra pattern matching through the
reference; `Solution::` to `Solution.` at the harness's 13 calls; and
the harness's `as i64` on the result taken off. `(prev + 1).min(x)` is
Kāra as it stands. The solution takes a `Vec[i32]`, so its harness
builds its lists as `Vec[i32]`. Every arm's output matches on the first
run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every order of the numbers, and in each the values every
place can take on some list the rules allow, found forward from a 1 at
the first place, each place within 1 of a value the place before it can
take, and back from the last place, each within 1 of a value the place
after it can take, every value from 1 to the number at its place, so a
number is only ever decreased; a value found both ways is on some list,
and the largest of them over every order is the answer. It runs 2000
random lists of 1 to 6 numbers from 1 to 8. Each arm meets six
properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | from 1 to the least of the count and the largest number |
| P3 | the numbers in reverse order give the same answer |
| P4 | a 10^9 more gives at least as much, and at most one more |
| P5 | every number doubled never gives less |
| P6 | the ★ arm's answer |

It checks clean as first written. All 60,000 checks pass on every arm:
`2000 cases: checksum 683274701, 60000 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, over the same cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: each number allowed two more than the one before it | P1 1824, P2 1727, P4 2000, P6 7296 |
| M2 | ★: the numbers walked unsorted | P1 924, P3 954, P6 3696 |
| M3 | count: each number counted at the least of it and `n - 1` | P1 1742, P2 341, P6 1742 |
| M4 | count: the top allowed one past each value | P1 258, P2 49, P6 258 |
| M5 | heap: the numbers popped largest first | P1 1193, P6 1193 |
| M6 | heap: the smallest number thrown away | P1 1742, P2 341, P6 1742 |
| M7 | search: each place allowed a number one too small | P1 258, P2 49, P6 258 |
| M8 | search: no top of `n` tried | P1 1401, P6 1401 |
| M9 | solution: the walk started from 1 | P1 1099, P2 1099, P6 1099 |
| M10 | solution: the numbers walked largest first | P1 1193, P6 1193 |

## Benchmarks

The bench builds one list of 10^5 numbers from 1 to 60000 once and makes
200 calls of the ★ arm on its first 50000 to 99999 numbers, each run's
length drawn from the checksum so far. Each call is handed its own copy
of its run, which the arm sorts. It checks clean as first written. Every
implementation prints `200 calls: checksum 719739745`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.26 s against Rust's 0.34 s (0.33 s with
overflow checks on), C's 1.9 s and Go's 1.4 s; Python takes 3.5 s.
