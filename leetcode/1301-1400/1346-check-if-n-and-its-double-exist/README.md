# 1346. Check If N and Its Double Exist

Given an array `arr` of integers, check if there exist two indices `i`
and `j` such that `i != j`, `0 <= i, j < arr.length`, and `arr[i] == 2 *
arr[j]`.

```
arr = [10,2,5,3]   ->  true    (10 is twice 5)
arr = [3,1,7,11]   ->  false
```

**Constraints:** `2 <= arr.length <= 500`, `-1000 <= arr[i] <= 1000`.

The arms are `fn check_if_exist(arr: Vec[i32]) -> bool`.

## Approaches

| file | mechanism |
|---|---|
| `check_if_exist.kara` ★ | a `Set` of the values seen so far; each new value x pairs with one of them if 2x is in the set, or if x is even and x / 2 is. Testing before inserting keeps a lone 0 from pairing with itself. O(n) |
| `check_if_exist_counts.kara` | the values lie from -1000 to 1000, so each is counted in an array shifted by 1000; then every x from -500 to 500 with a count asks for a count at 2x, and 0 for a count of two. O(n + range) |
| `check_if_exist_sorted.kara` | a sorted copy, and for each place the last place holding twice its value, found by `partition_point`; a hit at another place is a pair, and a hit at the place itself (only 0 is its own double) asks whether a neighbour is 0 too. O(n log n) |
| `check_if_exist_pairs.kara` | the statement tried directly: every ordered pair of different places. O(n^2) |
| `check_if_exist_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `HashSet<i32>`, `for &x in &arr`, the test `seen.contains(&(x * 2)) \|\| (x % 2 == 0 && seen.contains(&(x / 2)))` before `seen.insert(x)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples; one zero and
two zeros; -2 and -4; 7 and 14 with 498 odd numbers between them; 500 odd
numbers, the constraints' longest, none the double of another; and the
first 499 of them with 994, twice the largest, put last (`true false
false true true true false true`); and 2000 random arrays of 2 to 500
values, most of them short, from -10 to 10, from -1000 to 1000, or odd
(`2000 random arrays: 522 with a double, checksum 519239936`).
`check_if_exist.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run` and
`karac __mir-llvm-run`.

The Mend loop: three Kāra arms check clean. The sorted arm was written
first with Rust's `match s.binary_search(2 * s[i]) { Ok(j) => .., Err(_)
=> {} }`; Kāra's `binary_search` returns an `Option[i64]`
(docs/library/collections.md), `karac check` says so (E0200) with the
fix, and `karac fix` applies it: a `partition_point(|y| y <= 2 * s[i])`
that lands one past the last equal value, tested at `j - 1`, inside the
block the match stood in. The Rust solution takes one round of 19 fixes
by `karac fix`'s count: `struct Solution;` to `struct Solution {}`, the
`use std::collections::HashSet;` line deleted and `HashSet::new()` to
`Set.new()`, `for &x in &arr` to `for x in ref arr`, `&&` and `||` to
`and` and `or`, each `contains(&(..))` to `contains(..)`, `Vec<..>` to
`Vec[..]`, and `Solution::` to `Solution.`. Both match on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for each index j, the indices holding `2 * arr[j]` are
counted, j itself taken off when it is one of them, and any count left
is a pair. 2000 arrays of 2 to 10 values in four kinds, 500 each: from
-3 to 3; from -20 to 20; odd, from -99 to 99, where no value is
another's double; and powers of two up to 256 with either sign. Every
value lies within -500 to 500, so doubling keeps it within the
constraints, and every array is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the array read backwards: the same answer |
| P3 | every value negated: a = 2b exactly when -a = 2(-b), so the same answer |
| P4 | every value doubled: the same answer |
| P5 | twice the first value put at the end: a pair |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 arrays: checksum 437076309,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, trying every ordered pair,
gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the half tested for an odd value too | P1 151, P2 198, P4 151, P6 604 |
| M2 | ★: each value added before it is tested | P1 121, P6 484 |
| M3 | counts: only the values from 0 up scanned | P1 264, P3 540, P5 745, P6 264 |
| M4 | counts: a value counted once however often it appears | P1 50, P5 46, P6 50 |
| M5 | sorted: the partition taken below twice the value, not at it | P1 802, P5 2000, P6 802 |
| M6 | sorted: only the smallest value tried | P1 767, P3 53, P5 1932, P6 767 |
| M7 | pairs: only doubles after the value tried | P1 202, P2 431, P5 1321, P6 202 |
| M8 | pairs: the last place never taken as the double | P1 63, P2 129, P5 1137, P6 63 |
| M9 | solution: only the half tested | P1 229, P2 431, P6 229 |
| M10 | solution: the double and the half swapped | P1 219, P2 320, P4 219, P6 219 |

P1 and P6 kill all ten, P5 six, P2 five, P3 two and P4 two. M2, a lone
zero pairing with itself, is caught only by the statement and by the
four other arms disagreeing with the edited ★ (P6, four times P1's
count): backwards, negated or doubled, a lone zero is still lone, so the
edit errs the same way, and P5 asks only for a pair. Doubling every
value (P4) catches M1 and M10, whose false pairs come from an odd
value's rounded-down half, which vanishes once every value is even.
Negating every value (P3) catches the counts arm scanning only from 0 up
(M3) and the sorted arm trying only its smallest value (M6), which
becomes the largest. Reading backwards (P2) catches the edits whose
verdict depends on which of two values comes first (M1, M7, M8, M9,
M10). Twice the first value put last (P5) catches the six edits that can
miss a pair the statement plainly holds (M3 to M8); when the first value
is 0 that is a second zero, which counting each value once (M4) misses.

## Benchmarks

The bench builds 2000 arrays of 500 values, the constraints' longest,
odd and at random from -999 to 999, so none starts with a pair, once;
then makes 100 passes, each setting one place of every array from the
checksum so far to a value from -1000 to 1000 drawn from it too, so no
answer carries over, answering every array with the ★ arm's set and
folding the answer plus the pass into the checksum. C marks the values
seen in a stamp array over 4001 values, Rust uses a `HashSet`, Go a map.
Every implementation prints `100 passes over 2000 arrays of 500:
checksum 950061969`.

BENCHTAB
