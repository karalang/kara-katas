# 2741. Special Permutations

You are given a **0-indexed** integer array `nums` containing `n`
**distinct** positive integers. A permutation of `nums` is called special
if:

- For all indexes `0 <= i < n - 1`, either `nums[i] % nums[i+1] == 0` or
  `nums[i+1] % nums[i] == 0`.

Return *the total number of special permutations.* As the answer could
be large, return it **modulo** `10^9 + 7`.

```
nums = [2, 3, 6]  ->  2
nums = [1, 4, 3]  ->  2
```

**Constraints:** `2 <= nums.length <= 14`, `1 <= nums[i] <= 10^9`.

## Approaches

Two numbers are partners when one divides the other; a special order is
a path through every number along partners, so every arm counts such
paths.

| file | mechanism |
|---|---|
| `special.kara` ★ | `ways[mask][last]`, the special orders of the numbers in `mask` that end with `last`, each carried forward to every partner of `last` outside the mask; the answer sums the full mask's row. O(2^n n^2) |
| `special_memo.kara` | top down: a `struct Counter` holding the numbers and a memo, and a `mut ref self` method counting the ways the numbers not yet placed can follow a given last one. O(2^n n^2) |
| `special_masks.kara` | each number's partners as a bit mask, built by `filter` and `fold`; the table pulled rather than pushed, the orders ending at `last` taken from the mask without it, its partners there walked bit by bit with `trailing_zeros`. O(2^n n^2) |
| `special_sieve.kara` | inclusion and exclusion, with no table over masks: for each subset S, the walks of n numbers along partners that stay inside S, added or taken away by the parity of what S leaves out, so that only the walks through every number survive. O(2^n n^3) |
| `special_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `fn dfs` nested in the method and a `const MOD` in its body, a `vec![vec![-1i64; n]; 1 << n]` memo passed `&mut`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; two numbers,
one dividing the other; two that do not; 14 powers of two, where every
order is special, so the answer is 14! mod `10^9 + 7`; 2000 random arrays
of 2 to 8 distinct numbers, by turns of the form `2^a 3^b` and up to 30;
and 10 of 14 numbers of the form `2^a 3^b`, LeetCode's longest, each
batch with the sum of its answers and a checksum. `special.py` mirrors
the ★ arm and its output is byte-identical.

```
2
2
2
0
178290591
2000 small arrays: counts sum to 519264, checksum 716127514
10 arrays of 14 numbers: counts sum to 2009043142, checksum 312196387
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every order of the numbers, in turn by the next-permutation
step over their places, counted when each neighbouring pair has one
dividing the other; no table over masks. It draws 1000 random arrays of
2 to 7 distinct numbers, by turns of the form `2^a 3^b` and up to 30,
then 100 of 8 to 10, all before any arm answers; the literal reading is
asked only of the first 1000.

| | property |
|---|---|
| P1 | up to 7 numbers, the answer is the literal reading's |
| P2 | the numbers reversed: the same answer |
| P3 | every number times 7: the same answer |
| P4 | up to 7 numbers, the answer is even: each special order read backwards is another |
| P5 | the numbers replaced by `2^k`, k their rank, so that every order is special: n! mod `10^9 + 7` |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1100 cases: checksum 682268862, 33000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by `itertools.permutations` gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M2 and M3 fail the same checks, both letting a
number follow only one it divides. M2, M3, M5, M8 and M9 fail P5 in
every case: when every order is special, each of them loses some.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the full mask never reached by the last step | P1 402, P2 281, P4 160, P5 1100, P6 449 |
| M2 | ★: only the next number dividing the last | P1 438, P4 139, P5 1100, P6 487 |
| M3 | memo: only partners the last one divides | P1 438, P4 139, P5 1100, P6 487 |
| M4 | memo: the memo keyed by the used numbers alone | P1 206, P2 254, P4 98, P6 255 |
| M5 | masks: a single number counted as no order | P1 438, P5 1100, P6 487 |
| M6 | masks: only the lowest partner counted | P1 299, P2 239, P4 175, P5 923, P6 348 |
| M7 | sieve: every subset added, none taken away | P1 675, P5 923, P6 773 |
| M8 | sieve: walks one step short | P1 438, P5 1100, P6 487 |
| M9 | solution: the last number never placed after another | P1 438, P2 281, P4 150, P5 1100, P6 487 |
| M10 | solution: an order taken as done one number short | P1 494, P6 547 |

## Benchmarks

The bench draws 30 arrays of 14 distinct numbers of the form `2^a 3^b`,
LeetCode's longest, all of them first, then answers each 5 times by the
★ arm in all five languages, each call with a fresh table of `2^14` by
14. Every implementation prints `30 arrays of 14 numbers, 5 rounds:
counts sum to 41360139195, checksum 928608133`.

BENCHTAB

## Verification

All five arms print the same output as `special.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 26 edits, the wrapper
included: the nested `fn dfs` and the `const MOD` in the method's body
moved to the top level, since Kāra has no nested items and the function
captures nothing; `struct Solution {}` added; `Vec<..>` became
`Vec[..]`, `&Vec<i32>` became `ref Vec[i32]` and `&mut Vec<..>` became
`mut ref Vec[..]`; `usize` became `i64`; `vec![vec![-1i64; n]; 1 << n]`
became `Vec.filled(1 << n, Vec.filled(n, -1))`; `&&` and `||` became
`and` and `or`; the `&nums` argument dropped its `&` and `&mut memo`
became `mut memo`; and in the wrapper the `&x` pattern dropped its `&`,
`Solution::` became `Solution.` and the `as i64` dropped.
