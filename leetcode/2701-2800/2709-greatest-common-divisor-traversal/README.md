# 2709. Greatest Common Divisor Traversal

You are given a **0-indexed** integer array `nums`, and you are allowed
to **traverse** between its indices. You can traverse between index `i`
and index `j`, `i != j`, if and only if `gcd(nums[i], nums[j]) > 1`,
where `gcd` is the **greatest common divisor**.

Your task is to determine if for **every pair** of indices `i` and `j`
in nums, where `i < j`, there exists a **sequence of traversals** that
can take us from `i` to `j`.

Return `true` *if it is possible to traverse between all such pairs of
indices, or* `false` *otherwise.*

```
nums = [2,3,6]      ->  true
nums = [3,9,5]      ->  false
nums = [4,3,12,8]   ->  true
```

**Constraints:** `1 <= nums.length <= 10^5`, `1 <= nums[i] <= 10^5`.

## Approaches

| file | mechanism |
|---|---|
| `traversal.kara` ★ | two indices are a step apart when their numbers share a prime, so every pair can be traversed exactly when the indices form one connected set. A smallest-prime-factor sieve up to the largest number splits each into its primes; each index is joined, in a union-find with path halving, to the first index seen with each of its primes. A 1 shares nothing, so it strands itself unless it is alone. O(m log log m + n log m) for the largest number m |
| `traversal_search.kara` | the graph of indices and primes, an index linked to each prime it holds, found by trial division; a breadth-first search from index 0 through primes to every index that holds them, each prime crossed once. Every pair can be traversed when the search reaches every index. O(n m^(1/2)) |
| `traversal_primes.kara` | a union-find over the primes themselves: the primes of each number, sieved by its smallest factor, joined to one another, and every pair traversable when every number's first prime ends in one set and no number is 1 among others. Union by size, with full path compression by recursion. O(m log log m + n log m) |
| `traversal_solution.kara` | a Rust solution as LeetCode's Rust users write it, a union-find `struct` with `usize` parents and a recursive `find(&mut self)`, a sieve of `vec![0usize; m + 1]`, and every index joined to the index first seen with each prime in a `HashMap<usize, usize>`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 12 lines: LeetCode's three examples; one 1,
alone and twice; two primes; `10^5` copies of the prime 99991; every
number from 2 to 100001; the even numbers to `10^5`; a prime among
numbers that join; then the traversable count and a checksum for 2000
random cases of 1 to 8 numbers up to 30, and 100 of up to `10^4`
numbers, half of them drawn from the numbers up to `10^5` whose only
prime factors are 2, 3, 5 and 7, half at random up to `10^5`.
`traversal.py` mirrors the ★ arm and its output is byte-identical.

```
true
false
true
true
false
false
true
false
true
false
2000 cases up to 30: 616 traversable, checksum 441635239
100 cases up to 100000: 56 traversable, checksum 621214273, 693 smooth numbers
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: a step from i to j wherever `gcd(nums[i], nums[j]) > 1`,
every sequence of steps closed over by Floyd and Warshall's rule, and
every pair `i < j` asked whether it can be traversed, with no primes. It
checks 1000 random cases of 1 to 8 numbers up to 30 or up to 12, then 10
of up to 1000 numbers up to 20000 or up to 2000. Every case is drawn
before any arm answers.

| | property |
|---|---|
| P1 | up to 8 numbers, the answer is the literal reading's |
| P2 | the numbers reversed: the same answer |
| P3 | one of the numbers added again: the same answer, but for a lone 1 |
| P4 | every number doubled: true; and the next prime above the largest added: false |
| P5 | each arm agrees with at least two of the other three |

The differential prints `1010 cases: checksum 59171798, 20200 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by closure gives the same checksum. On a
failure it prints the first ten and then the count by property. P4's
prime is the next one above the case's largest number, not a fixed one
above `10^5`: a sieve to 99991 in every arm made the interpreter lane
take minutes.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Two first choices were equivalent and
were replaced: the ★ arm letting a 1 among others through, which the
union count already refuses since a 1 joins nothing, and the solution's
holder of each prime replaced by the latest index, which joins the same
sets. Two more crashed with an index out of bounds and a division by
zero rather than answering wrong, and were replaced too.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only indices already joined are joined | P1 158, P3 100, P4 899, P5 158 |
| M2 | ★: the sieve stops below the square root's square | P1 15, P4 1, P5 15 |
| M3 | search: a prime crossed without its holders | P1 31, P2 44, P5 31 |
| M4 | search: the prime left over after trial division dropped | P1 106, P3 41, P4 206, P5 106 |
| M5 | primes: a number's last prime never joined | P1 75, P5 75 |
| M6 | primes: every number held to its own first prime | P1 526, P4 793, P5 535 |
| M7 | solution: a union never counted | P1 158, P3 100, P4 899, P5 158 |
| M8 | solution: two sets taken as one | P1 291, P4 258, P5 291 |
| M9 | solution: a lone number answers false | P1 111, P3 100, P4 111, P5 111 |
| M10 | ★: every prime's first holder taken as index 0 | P1 31, P2 44, P5 31 |

## Benchmarks

The bench draws 20 arrays of `10^5` numbers, LeetCode's most, all of
them first: the even arrays every number a multiple of 2, 3, 5 or 7, so
the sets join, the odd ones from 2 to `10^5` at random, so a prime above
`5 * 10^4` strands its index. It answers each 5 times by the ★ arm in
all five languages, each answer a sieve to the largest number and a
union-find over the array. Every implementation prints `20 arrays of
100000 numbers up to 100000, 5 rounds: 50 traversable, checksum
341912206`.

BENCHTAB

## Verification

All four arms print the same output as `traversal.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The three arms of our own checked clean as first written.

LeetCode's Rust template took one `karac fix` of 30 edits, most of them
`usize` becoming `i64`, since Kāra indexes with `i64`. Beyond those: the
`use std::collections::HashMap;` dropped and `struct Solution {}` added;
`&mut self` became `mut ref self`; `vec![0usize; m + 1]` became
`Vec.filled(m + 1, 0)`; `Dsu::new` became `Dsu.new`; `HashMap<usize,
usize>` became `Map[i64, i64]`; and `if let Some(&j) = seen.get(&p)`
became `if let Some(j) = seen.get(p).cloned()`.
