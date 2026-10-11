# 368. Largest Divisible Subset

Given a set of distinct positive integers `nums`, return the largest subset
in which every pair `(a, b)` satisfies `a % b == 0` or `b % a == 0`. If there
are several, return any of them.

```
nums = [1, 2, 3]      -> [1, 2]   ([1, 3] is also accepted)
nums = [1, 2, 4, 8]   -> [1, 2, 4, 8]
```

**Constraints:** `1 <= nums.length <= 1000`; `1 <= nums[i] <= 2 * 10^9`; the
numbers are distinct.

## Approaches

In ascending order, a divisible subset is a chain in which each number
divides the next, and since divisibility is transitive that is all it needs.
LeetCode accepts any largest subset; here every arm returns the same one,
the lexicographically first in ascending order, so their outputs can be
compared byte for byte.

| file | mechanism | time |
|---|---|---|
| `largest_subset.kara` ★ | sort; `size[i]`, the longest chain starting at `a[i]`, is filled from the right as one more than the best chain starting at a later multiple; the first best multiple and the first best start give the lexicographically first answer | O(n²) |
| `largest_subset_memo.kara` | the same recurrence top down: a recursive `chain_from` with a `Map` from each number to its chain length and the multiple that continues it | O(n²) |
| `largest_subset_chains.kara` | the textbook direction, best chain *ending* at each number, keeping each chain itself and comparing chains by length and then lexicographically | O(n² · chain length) |
| `differential.kara` | the three arms against a brute-force oracle over every subset, 29,328 checks, five properties | — |

Every arm prints the same 11 lines: the two LeetCode examples, eight edge
cases (one number, primes only, unsorted input, two chains of equal length,
a longer chain that starts at a larger number, no 1 but shared factors,
values near `2 * 10^9`, and 1 to 1000), and the total size and a checksum
of the answers for 300 random sets of up to 40 numbers up to 500.
`largest_subset.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the three arms. The oracle sorts the
numbers and tries every subset as a bitmask, keeping the divisible ones and
comparing candidates with its own order (more numbers, then the first
difference), not the chains arm's `better`, so that a fault in one cannot
hide in both. The test draws 2,000 random sets of 1 to 10 distinct
numbers, half from `1..=30`, where most pairs share a factor and ties are
common, and half from `1..=200`.

| | property |
|---|---|
| P1 | each arm gives the oracle's subset |
| P2 | the answer is drawn from the input, ascending, and each number divides the next |
| P3 | reversing the input changes nothing |
| P4 | multiplying every number by 2 or 3 multiplies the answer by the same |
| P5 | adding a 1 that is not there puts it in front of the same answer |

It prints `2000 cases, 29328 checks, 0 failures` under `karac run --interp`,
LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac build`. It does not run
under `karac __mir-run` yet, because its copy of the ★ arm uses
`(0..n).rev()`: see Compiler findings.

## Mutation testing

Eight edits to the copies inside `differential.kara`, each run as a
`karac build` binary, since the MIR interpreter cannot run the file yet.
All eight are killed.

| # | mutation | how |
|---|---|---|
| M1 | dp: a tie moves to the later multiple | P1 and P5, 1396 failures |
| M2 | dp: a tie moves to the later start | P1 and P5, 2046 failures |
| M3 | dp: an extra `or a[i] % a[k] == 0`, which takes the size test with it, so any multiple overwrites the best | P1 and P5, 2140 failures |
| M4 | memo: `rest > len` instead of `rest + 1 > len`, so a multiple whose own chain is one number long is never taken | P1 and P5, 2783 failures |
| M5 | memo: skips the next number when looking for multiples | P1 and P5, 2044 failures |
| M6 | chains: `better` prefers the lexicographically later chain | P1, 1299 failures |
| M7 | chains: compares prefixes by length only | P1, 1 failure |
| M8 | oracle: compares candidates by size only | P1, 207 failures |

M7 is caught by a single case. A first longest prefix that is not the
lexicographically first one needs a chain that starts higher but ends lower,
like `[3, 6]` against `[2, 10]` under 30, and those are rare among ten
numbers.

## Verification

All three arms print the same output as `largest_subset.py` under
`karac run --interp`, LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac
build`. Under `karac __mir-run` the memo and chains arms match too; the ★
arm stops with `an iterator value is not lowered yet`.

## Benchmarks

The bench program answers 200 random sets of 1,000 distinct numbers up to
100,000, the problem's largest size, with the ★ arm. The Kāra build and the
C, Rust, Go and Python mirrors all print `568 numbers in the answers,
checksum 722629395`. Timings are not taken yet; they need a quiet machine.

## Compiler findings

- **`(0..n).rev()` is not lowered by the MIR builder.** `karac __mir-run`
  stops at the ★ arm's `for i in (0..n).rev()` with `error[mir]: build:
  an iterator value is not lowered yet`, at kara `a1bc8de9e6`. Every other
  backend runs it. This is the corpus's existing `mir-gap:an iterator value`
  bucket (32 programs, among them kata 337's iterative arm and the
  `iter_rev_range` fixtures), so it is a known gap rather than a new one.
