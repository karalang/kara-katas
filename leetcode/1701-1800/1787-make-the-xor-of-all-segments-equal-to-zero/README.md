# 1787. Make the XOR of All Segments Equal to Zero

You are given an array `nums` and an integer `k`. The XOR of a segment
`[left, right]`, where `left <= right`, is the XOR of all the elements
with indices from `left` to `right` inclusive. Return the minimum number
of elements to change in the array such that the XOR of every segment of
size `k` is equal to zero.

```
nums = [1, 2, 0, 3, 0],           k = 1  ->  3
nums = [3, 4, 5, 2, 1, 7, 3, 4, 7], k = 3  ->  3
nums = [1, 2, 4, 1, 2, 5, 1, 2, 6], k = 3  ->  3
```

**Constraints:** `1 <= k <= nums.length <= 2000` and `0 <= nums[i] <
2^10`.

The arms are `fn min_changes(nums: Vec[i32], k: i32) -> i32`.

## Approaches

Every segment of size `k` has XOR 0 exactly when `nums[i] == nums[i +
k]` for every `i` and the first `k` numbers XOR to 0. So the positions
fall into `k` groups by `i % k`, each group must end up holding one
value, and the `k` values must XOR to 0.

| file | mechanism |
|---|---|
| `min_changes.kara` ★ | a DP over the groups, keeping for each XOR `x` of the values chosen so far the fewest changes, in a list of 1024: a group takes one of its own values `v` at its size less `v`'s count, reaching `x` from `x ^ v`, or any value at all at its whole size, which reaches every `x` from the best so far. Each group's counts in a `Map`. O(k * 1024 * distinct) |
| `min_changes_array.kara` | the same DP, each group's counts in a list of 1024 and its distinct values in the order they first appear, the group walked with `(g..n).step_by(k)` |
| `min_changes_onefree.kara` | two cases. If some group is changed whole, it can take whatever value cancels the rest, so the others keep their commonest value and the group given up is the one whose commonest counts least. Otherwise every group keeps a value it already holds, and a DP over a `Map` of only the XORs those values reach keeps the most numbers kept. The better of the two |
| `min_changes_memo.kara` | the DP read top down: a recursion over the fewest changes that make groups `g` to `k - 1` XOR to `x`, memoized in `k` rows of 1024, each row's least value kept once the row is filled |
| `min_changes_solution.kara` | a Rust solution as LeetCode's Rust users write it (`std::collections::HashMap::new()` with `*cnt.entry(..).or_insert(0) += 1`, `vec![..; MX]`, `i32::MAX / 2`, `for (&v, &c) in cnt.iter()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples (`3 3 3`);
seven edges, one number 0 and one not, `k` the whole length with the XOR
0 already and not, a repeating pattern that already works, and four 7s
with `k` of 2 and 3 (`0 1 0 1 0 0 1`); the constraints' most, 2000
random numbers below 1024 with `k` of 1, 7, 1000 and 2000 (`the most:
2000 1979 999 1`); and 1500 random cases of 1 to 24 numbers below 2 to
32, `k` from 1 to the length, a quarter of them built from a pattern of
`k` numbers with a few changed (`1500 random cases: checksum
750022230`). `min_changes.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the onefree arm and the harness check clean as first
written. The ★ and array arms counted each group's size from `let mut
size = 0;`, which keeps the literal's default `i64`, and check refuses
each sum with it where it meets the `i32` list, in the new row's fill
and in what is stored into it: "`size` is an 'i64' because its literal
kept the default, since an operator or a method does not fix a literal's
type; declare it `size: i32`". `karac fix` writes that, 1 fix in each,
and the same for the memo arm's `let mut low = 1000000;`. The Rust
solution takes a first round of 17 fixes by `karac fix`'s count: `struct
Solution;` to `struct Solution {}`, `Vec<i32>` to `Vec[i32]`, each
`usize` to `i64`, `vec![..; MX]` to `Vec.filled(MX, ..)`, `i32::MAX` to
`i32.MAX`, `std::collections::HashMap::new()` to `Map.new()`, the `&`
dropped from `for (&v, &c)`, and `Solution::` to `Solution.`. One error
is left with no machine fix: `f = g`, where `g = Vec.filled(MX, t2min +
size)` is a `Vec[i64]` from the same bare `size`, is refused "expected
'Vec[i32]', found 'Vec[i64]'", with only the general advice to annotate
a binding or suffix a literal. That is B-2026-11-26-86. Written `let mut
g: Vec[i32] = ...` by hand as the advice says, check traces the fill to
`size`, and a second round of `karac fix` writes `size: i32` and
`or_insert(0i32)`, 2 fixes. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every array of numbers below 8 tried a position at a time,
each window of `k` checked as soon as it is complete, and the fewest
positions that differ from `nums` kept, while there are at most 8
numbers, all below 8, and `k` is at most 4. A changed number needs no
bit that no number has, since clearing that bit in every changed number
keeps every window's XOR 0. LeetCode's examples, the seven edges, 500
random numbers below 1024 with `k` of 1, 7, 250 and 500, and 1986 random
cases, half small enough for the literal reading and half of 1 to 24
numbers below 2 to 32, half of them built from a pattern of `k` numbers
with a few changed. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally, on the small cases |
| P2 | 0 exactly when every window already XORs to 0, and never more than the changes that keep each group's commonest value but give up the group whose commonest counts least |
| P3 | the numbers reversed give the same answer |
| P4 | each group's numbers shuffled among its own positions give the same answer |
| P5 | groups 0 and 1 XORed by one mask give the same answer, since every window holds one number of each; with `k` of 1, the answer is the count of numbers that are not 0 |
| P6 | the ★ arm's answer |

The differential checks clean as first written. All 55,565 checks pass
on every arm: `2000 cases: checksum 355910770, 55565 checks over 5 arms:
0 failures`, under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. Python, running the ★ arm's mirror over the same
cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a group changed whole reaching every XOR only from 0 | P1 87, P2 250, P3 131, P5 16, P6 1000 |
| M2 | ★: a kept value joined by OR in place of XOR | P1 356, P2 517, P3 209, P5 112, P6 3392 |
| M3 | array: each group taken a step of k + 1 apart | P1 554, P2 320, P3 293, P4 347, P5 536, P6 1197 |
| M4 | array: a group changed whole charged one change more | P1 582, P2 1167, P5 328, P6 1167 |
| M5 | onefree: the group given up the one whose commonest counts most | P1 343, P2 839, P6 839 |
| M6 | onefree: the group given up costing no changes | P1 674, P2 648, P5 400, P6 1307 |
| M7 | memo: any XOR at all accepted past the last group | P1 674, P2 648, P5 400, P6 1307 |
| M8 | memo: a kept value charged as a change | P1 874, P2 1524, P5 228, P6 1672 |
| M9 | solution: each group taken a step of 1 apart | P1 564, P2 1282, P3 714, P4 292, P5 641, P6 1316 |
| M10 | solution: a kept value reaching x from v alone | P1 378, P2 539, P3 422, P5 355, P6 859 |

## Benchmarks

The bench builds 100 lists of 600 random numbers below 1024 once and
makes 300 calls of the ★ arm, each list and `k` from 1 to 600 drawn from
the checksum so far. It checks clean as first written. Every
implementation prints `300 calls over 100 lists: checksum 371001104`.
The C mirror counts each group in a small open-addressing hash table, as
the other languages' maps do.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.52 s against Rust's 0.43 s (0.47 s with overflow checks
on), C's 0.21 s and Go's 6.1 s; Python takes 20.1 s.
