# 1799. Maximize Score After N Operations

You are given `nums`, an array of `2 * n` positive integers, and must
perform `n` operations on it. In the `i`th operation (1-indexed) you
choose two elements `x` and `y`, receive a score of `i * gcd(x, y)`, and
remove `x` and `y` from `nums`. Return the largest total score you can
receive after the `n` operations.

```
nums = [1,2]            ->  1
nums = [3,4,6,8]        ->  11
nums = [1,2,3,4,5,6]    ->  14
```

**Constraints:** `1 <= n <= 7`, `nums.length == 2 * n`, and `1 <=
nums[i] <= 10^6`.

The arms are `fn max_score(nums: Vec[i32]) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `max_score.kara` ★ | dynamic programming over the set of numbers already taken, a bitmask: a set of `2k` numbers has had `k` operations, so the next pair taken from outside it scores `k + 1` times its gcd, and each set pushes its best forward to every set one pair larger. O(4^n n^2) at worst |
| `max_score_memo.kara` | recursion with a memo: the best score from the set of numbers still free, every free pair tried as the next operation, each answer kept in a `Map` by its set, which fixes how many operations are behind it. O(4^n n^2) at worst |
| `max_score_match.kara` | every way to pair the numbers tried, and for each the gcds sorted, since the largest gcd is best taken last, at the largest multiplier. (2n - 1)!! pairings, 135135 at n = 7 |
| `max_score_pull.kara` | the same sets taken, each pulling its best from the sets one pair smaller, over a table of every pair's gcd worked out once. O(4^n n^2) at worst |
| `max_score_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `fn gcd` nested in the method, `vec![0; 1 << n]`, `(mask as u32).count_ones()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples (`1 11
14`); four edges, one pair alike, one pair coprime, six ones, and `[6,
10, 15, 30]`, whose pairs share more across than within (`5 1 6 32`);
the constraints' most, 14 numbers of `10^6` and 14 at random (`the most:
28000000 290`); and 1000 random cases of 1 to 5 pairs of numbers of 1 to
60 (`1000 random cases: checksum 766257392`). `max_score.py` mirrors the
★ arm, and its output is byte-identical. Every arm gives the same output
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the pull arm and the harness check clean as first
written. The ★ arm was first written with `let op = taken / 2 + 1;`,
`taken` being `mask.count_ones()`, which is an `i64` as every count in
Kāra is, and check refused `best[next].max(best[mask] + op * gcd(..))`,
"`max` expects an argument of type `i32`, got `i64`", with no fix:
nothing narrows by itself, so the cast is written by hand, `(taken / 2 +
1) as i32`, as the pull arm already had it. The memo and match arms
start a score as `let mut most = 0;` and `let mut score = 0;`, which
check refuses as `i64` where an `i32` is returned, and the memo arm
cleared its bits with Rust's `!(1 << i)`, where Kāra writes `~`; `karac
fix` annotated the two and wrote `~(1 << i)` twice, 3 fixes in the memo
arm and 1 in the match arm. The Rust solution takes one round of 10
fixes by `karac fix`'s count, and its diff is: `struct Solution;` to
`struct Solution {}`, the nested `fn gcd` moved above the `impl`,
`Vec<i32>` to `Vec[i32]` in both signatures, `vec![0; 1 << n]` to
`Vec.filled(1 << n, 0i32)`, and `Solution::` to `Solution.`. Its `1usize
<< n` and `(mask as u32).count_ones() as i32` stay.

The memo arm was first written pairing only the lowest free number at
each step. That fixes the order of the operations along with the
pairing, and the mirror caught it on the random 14 numbers, 251 against
290. It now tries every free pair, and every arm's output matches.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the `op`-th operation tries every pair of the numbers left,
scores `op` times its gcd, and plays the rest out the same way, every
order of every pairing, while there are at most 4 pairs. LeetCode's
examples, the four edges, 14 numbers of up to `10^6` and 14 of up to 60,
and 1991 random cases of 1 to 4 pairs of numbers of 1 to 60. Each arm
meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally, while there are at most 4 pairs |
| P2 | the numbers in reverse order give the same answer |
| P3 | every number doubled doubles the answer |
| P4 | a pair of ones more raises the answer by at least 1, while there are fewer than 7 pairs |
| P5 | the first number moved to the end gives the same answer |
| P6 | the ★ arm's answer |

The differential's literal reading was first written with `let mut best
= 0;`, and `karac fix` annotated it `best: i32`, 1 fix. All 59,980
checks pass on every arm: `2000 cases: checksum 696463927, 59980 checks
over 5 arms: 0 failures`, under `karac __mir-run`, `karac run`, `karac
build` and `karac __mir-llvm-run`. Python, running the ★ arm's mirror
over the same cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the first operation scored 0 times its gcd | P1 1998, P6 8000 |
| M2 | ★: a number never paired with the one right after it | P1 1257, P5 354, P6 5032 |
| M3 | memo: a remembered score read back one too high | P1 940, P2 235, P3 942, P5 163, P6 942 |
| M4 | memo: every operation scored at the first one's multiplier | P1 1487, P6 1489 |
| M5 | match: the gcds never sorted | P1 1011, P2 1164, P5 1090, P6 1013 |
| M6 | match: the largest gcd given the smallest multiplier | P1 1417, P6 1419 |
| M7 | pull: each operation scored one multiplier too high | P1 1998, P6 2000 |
| M8 | pull: a set pulled from the set missing only one of the pair | P1 1487, P6 1489 |
| M9 | solution: the sets of an even count skipped | P1 1998, P4 1998, P6 2000 |
| M10 | solution: each operation scored one multiplier too high | P1 1998, P6 2000 |

## Benchmarks

The bench builds 100 random lists of 14 numbers of up to `10^6` once,
and makes 100 calls of the ★ arm, each list drawn from the checksum so
far; each call fills a table of 16384 sets. It checks clean as first
written. Every implementation prints `100 calls over 100 lists of 14
numbers: checksum 82487315`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.63 s against Rust's 0.64 s (0.67 s with
overflow checks on), C's 0.62 s and Go's 0.67 s; Python takes 6.4 s.
