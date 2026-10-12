# 421. Maximum XOR of Two Numbers in an Array

Given an integer array `nums`, return the maximum result of
`nums[i] XOR nums[j]`, where `0 <= i <= j < n`.

```
nums = [3,10,5,25,2,8]                          -> 28   (5 XOR 25)
nums = [14,70,53,83,49,91,36,80,92,51,66,70]    -> 127
```

**Constraints:** `1 <= nums.length <= 2 * 10^5`;
`0 <= nums[i] <= 2^31 - 1`.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `maximum_xor.kara` ★ | prefix bits: settle the answer from the top bit down. With the high bits fixed, the next bit can be 1 when some number's prefix `p` (its bits down to this one) has a partner `p ^ candidate` among the prefixes, since `a ^ b = c` exactly when `a ^ c = b`; a `Set` of the prefixes answers that | O(31 n) | O(n) |
| `maximum_xor_trie.kara` | binary trie in two child tables: before inserting a number, walk the trie taking the opposite bit wherever that branch exists, which finds its best partner among the numbers before it | O(31 n) | O(31 n) |
| `maximum_xor_pairs.kara` | every pair | O(n^2) | O(1) |
| `maximum_xor_split.kara` | sort and split: sorted, the numbers that share their high bits sit in one range with the 0s at the next bit before the 1s. The best pair takes one number from each side of the first split; to pair two groups, split both at the next bit and prefer crossing pairs, falling back to matching pairs only when no crossing pair exists | O(n log n + 31 n) | O(n) |
| `differential.kara` | the four arms on 2,000 random arrays, five properties, one of them a brute force that never uses `^` | — | — |

Every arm prints the same 11 lines: the two LeetCode examples, eight
edge cases (one number, three equal, 0 with 2^31 - 1, powers of two,
2^30 with 2^30 - 1, eight numbers sharing their top bits, two
neighbours, numbers at the top of the range), and for 2,000 random
arrays of 1 to 50 numbers below a random power of two from 2 to 2^31,
the total of the answers and a checksum. `maximum_xor.py` mirrors the ★
arm and its output is byte-identical.

The ★ arm walks its `Set` (`for p in prefixes`), whose order is the
per-process hash order. It stops at the first prefix with a partner,
and whether one exists does not depend on the order, so the output is
the same on every run.

## Differential

`differential.kara` holds copies of the four arms. Each of 2,000 random
cases is an array of 1 to 40 numbers below a random power of two from 2
to 2^30, so that doubling stays within 31 bits:

| | property |
|---|---|
| P1 | the answer is the largest XOR found by a brute force that builds each pair's XOR from the two numbers' base-2 digits, without `^` |
| P2 | XOR-ing every number with one constant, or reversing the array, gives the same answer |
| P3 | adding a 0 gives the larger of the answer and the largest number; adding a copy of a number changes nothing |
| P4 | doubling every number doubles the answer; setting bit 30 in every number changes nothing |
| P5 | the numbers 0 to 2^w - 1 give 2^w - 1, and a number with its 31-bit complement gives 2^31 - 1 |

It prints `2000 cases, 4 arms, 40000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | prefix: each prefix keeps only the current bit | P1 1884, P3 1935, P5 2000 |
| M2 | prefix: the search starts at bit 29 | P4 65, P5 2000 |
| M3 | trie: the walk prefers the same bit | P1 1945, P2 1368, P3 1519, P4 1945, P5 2000 |
| M4 | trie: the second number is not compared | P1 104, P2 85, P3 128, P5 2000 |
| M5 | pairs: neighbours are skipped | P1 289, P3 188, P5 2000 |
| M6 | pairs: OR instead of XOR | P1 1444, P2 990, P3 51, P4 1945 |
| M7 | split: the 1-with-0 crossing pair is skipped | P1 1686, P2 912, P4 905, P5 2000 |
| M8 | split: no fallback to matching pairs | P1 1461, P3 1498, P4 1943 |

Only P4 and P5 see M2: the random arrays stay below 2^30, so bit 30
matters only once the numbers are doubled or in P5's complement pair.
P4 cannot see M4 or M5, because doubling or setting a shared bit keeps
the same pairs in the same places, so the mutant is wrong the same way
on both arrays. P5 cannot see M6 or M8: OR and XOR agree on the
largest pair of 0 to 2^w - 1 and on a number with its complement, and
neither of those arrays needs a matching pair.

## Verification

All four arms print the same output as `maximum_xor.py` on every
backend: `karac __mir-run` (the v2 MIR interpreter),
`karac __mir-llvm-run`, `karac run --interp`, LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`. `karac check` passes on every file.
The differential prints `40000 checks, 0 failures` on all six.

## Benchmarks

The bench program uses the ★ arm on 20,000 random numbers below 2^31.
Each of 100 rounds replaces one number with a new random one and
recounts, so no compiler can hoist the count out of the loop; it folds
the answers into a total and a checksum. Every implementation prints
`100 rounds on 20000 numbers: total 214748363500, checksum 147213845`;
a 3-round cut of the Kāra program under `karac __mir-run` prints the
same as the C program cut the same way. With 20,000 numbers the answer
is near 2^31 every round, which does not shorten the work: every bit
still builds a set of every prefix. Spot timings on a shared 4-core
container, three runs each (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.35 to 0.50 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.92 to 2.26 s |
| Rust (`rustc -O`) | 1.99 to 2.10 s |
| Kāra (legacy `karac build`) | 3.18 to 3.45 s |
| Go | 3.87 to 4.03 s |
| Python | 8.05 to 8.15 s |

The set is most of the cost, and the mirrors do not use the same one.
Kāra's `Set` and Rust's `HashSet` both hash with SipHash-1-3; Go's map
uses its own hash; the C mirror's set is open addressing with a
multiplicative hash and no keyed hashing, which is why it is several
times faster than the others. Python hashes a small integer to itself,
which keeps it within a few times of Go here. The Kāra program also prints the same
line under `karac __mir-llvm-run` in 69 s, compile included; that JITs
the MIR's IR without optimization passes, so it is not a benchmark. The
`karac build` time is the frozen legacy backend.

## Compiler findings

No new findings.
