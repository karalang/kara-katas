# 1829. Maximum XOR for Each Query

You are given a sorted array `nums` of `n` non-negative integers and an
integer `maximumBit`. You want to perform the following query `n` times:
find a non-negative integer `k < 2^maximumBit` such that `nums[0] XOR
nums[1] XOR ... XOR nums[nums.length-1] XOR k` is maximized, and `k` is
the answer to the `i`th query; then remove the last element from the
current array `nums`. Return an array `answer`, where `answer[i]` is the
answer to the `i`th query.

```
nums = [0,1,1,3], maximumBit = 2        ->  [0,3,2,3]
nums = [2,3,4,7], maximumBit = 3        ->  [5,2,6,5]
nums = [0,1,2,2,5,7], maximumBit = 3    ->  [4,3,6,4,6,7]
```

**Constraints:** `nums.length == n`, `1 <= n <= 10^5`, `1 <= maximumBit
<= 20`, `0 <= nums[i] < 2^maximumBit`, `nums` is sorted in ascending
order.

The arms are `fn get_maximum_xor(nums: Vec[i64], maximum_bit: i64) ->
Vec[i64]`.

## Approaches

| file | mechanism |
|---|---|
| `get_maximum_xor.kara` ★ | the XOR of the numbers left, XORed with a `k` below `2^maximumBit`, is largest when `k` flips every one of its low `maximumBit` bits, so each answer is that XOR against the mask of `maximumBit` ones; the XOR of all the numbers is taken once, and the last number is XORed out of it after each answer. O(n) |
| `get_maximum_xor_prefix.kara` | a table of prefix XORs, `prefix[i]` the XOR of the first `i` numbers, so the query after `j` removals asks for `prefix[n - j]` against the mask. O(n) |
| `get_maximum_xor_bits.kara` | `k` built a bit at a time: of the low `maximumBit` bits, `k` takes each one that the XOR of the numbers left has clear, as that bit is then set in their XOR with `k`. O(n b), b = maximumBit |
| `get_maximum_xor_fold.kara` | the answers worked from the front: one `fold` over the numbers carries the XOR so far and pushes each prefix's XOR against the mask, and the list, made in the order the prefixes grow, is reversed to the order the queries shrink them. O(n) |
| `get_maximum_xor_solution.kara` | a Rust solution as LeetCode's Rust users write it (the ★ arm's walk, the XOR of all taken by `fold` and the numbers walked by `rev`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples; four
edges, one zero on one bit, one number with every bit set, equal numbers
whose XOR comes and goes, and the most bits (`[1] [0] [7, 2, 7, 2] [1,
1048574, 1048575]`); the constraints' most, 10^5 sorted numbers below
2^20, the answers summed, with the first and the last (`the most:
69638683025 855457 1048574`); and 3000 random cases of 1 to 10 sorted
numbers below `2^b`, `b` from 1 to 5 (`3000 random cases: checksum
859085736`). `get_maximum_xor.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, prefix and bits arms and the harness check clean
as first written. The fold arm was first written `let (_, mut answer) =
nums.iter().fold(..)`; check refused `mut` inside a pattern as Rust's,
and `karac fix` wrote `let mut (_, answer) = ..`, 2 fixes by its count.
The Rust solution takes 22 fixes by `karac fix`'s count, and its diff
is: `struct Solution {}` added above the `impl`; `Vec<i32>` to
`Vec[i32]`; `let mask = (1 << maximum_bit) - 1` to `let mask: i32 = ..`,
and `fold(0, |acc, &n| acc ^ n)` to `fold(0i32, |acc, n| acc ^ n)`, as a
bare literal is an `i64` and both meet `i32`s; `let mut ans =
Vec::with_capacity(..)` to `let mut ans: Vec[i32] =
Vec.with_capacity(..)`; `for &n in nums.iter().rev()` to `for n in ..`;
`Solution::` to `Solution.` at the harness's 4 calls; and in the
harness, `|&k| k as i64` to `|k| k as i64`, and `*k as i64` folded into
the checksum to `*k`. `nums.iter().rev()` and `x ^= n` are Kāra as they
stand. The solution takes a `Vec[i32]` and an `i32`, so its harness
builds its lists as `Vec[i32]`. Every arm's output matches on the first
run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: before each removal of the last number, every `k` below
`2^maximumBit` is tried against the XOR of the numbers left, and the
first `k` giving the largest XOR is the answer. It runs 2000 random
cases of 1 to 10 sorted numbers below `2^b`, `b` from 1 to 6. Each arm
meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | one answer to a number, each below `2^maximumBit` |
| P3 | each answer XORed with the XOR of the numbers left sets every one of the `maximumBit` bits |
| P4 | one more bit allowed, each answer gains that bit |
| P5 | the largest number given twice more cancels out: the first answer is as before, and after the two removals the answers are |
| P6 | the ★ arm's answer |

It checks clean as first written. All 60,000 checks pass on every arm:
`2000 cases: checksum 122998273, 60000 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, over the same cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the mask one short, its lowest bit clear | P1 2000, P3 2000, P6 8000 |
| M2 | ★: the last number taken out before its query | P1 1948, P3 1948, P6 7792 |
| M3 | prefix: each query read one prefix short | P1 1948, P3 1948, P6 1948 |
| M4 | prefix: the prefixes taken by OR | P1 1659, P3 1659, P6 1659 |
| M5 | bits: the lowest bit never set in k | P1 1827, P3 1827, P6 1827 |
| M6 | bits: k given the bits already set | P1 2000, P3 2000, P4 2000, P6 2000 |
| M7 | fold: each prefix read without its last number | P1 1948, P3 1948, P6 1948 |
| M8 | fold: the answers sorted in place of reversed | P1 1545, P3 1545, P5 1948, P6 1545 |
| M9 | solution: the last number XORed into its own answer | P1 1948, P3 1948, P6 1948 |
| M10 | solution: the numbers summed in place of XORed | P1 1659, P2 1580, P3 1659, P4 948, P5 1948, P6 1659 |

## Benchmarks

The bench builds one sorted list of 10^5 numbers below 2^20 once and
makes 200 calls of the ★ arm with `maximumBit` 20 on its first 50000 to
99999 numbers, each run's length drawn from the checksum so far, the
answers of each call summed into the checksum. Each call copies its run,
as the arm takes its list by value. It checks clean as first written.
Every implementation prints `200 calls: checksum 977176008`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.04 s against Rust's 0.07 s (0.08 s with
overflow checks on), C's 0.03 s and Go's 0.29 s; Python takes 1.7 s.
