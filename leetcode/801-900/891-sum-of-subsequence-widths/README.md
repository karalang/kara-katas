# 891. Sum of Subsequence Widths

The width of a sequence is the difference between the maximum and
minimum elements in the sequence. Given an array of integers `nums`,
return the sum of the widths of all the non-empty subsequences of
`nums`. Since the answer may be very large, return it modulo `10^9 + 7`.

A subsequence is a sequence that can be derived from an array by
deleting some or no elements without changing the order of the
remaining elements. For example, `[3,6,2,7]` is a subsequence of the
array `[0,3,1,6,2,2,7]`.

```
nums = [2,1,3]  ->  6
nums = [2]  ->  0
```

**Constraints:** `1 <= nums.length <= 10^5` and `1 <= nums[i] <= 10^5`.

## Approaches

| file | mechanism |
|---|---|
| `sum_subseq_widths.kara` ★ | sorted, with powers of two: a width depends only on which values a subsequence holds, so sort them; the value at sorted position i is the largest of the 2^i subsequences made of it and any values before it, and the smallest of the 2^(n-1-i) made of it and any after it, so it adds itself 2^i times and takes itself away 2^(n-1-i) times. O(n log n) |
| `sum_subseq_widths_pairs.kara` | every pair of ends: sorted, the subsequences that start at i and end at j choose freely among the j - i - 1 values between, so each pair adds (a[j] - a[i]) 2^(j-i-1). O(n^2) |
| `sum_subseq_widths_counting.kara` | a count of each value instead of a sort: walking the values upwards, the c copies of a value fill sorted positions p to p + c - 1, and the ★ arm's powers for those positions sum to 2^p (2^c - 1) as the largest and 2^(n-p-c) (2^c - 1) as the smallest. O(n + largest value) |
| `sum_subseq_widths_running.kara` | a running sum of starts: sorted, the subsequences ending at j add a[j] (2^j - 1) less s, the sum of a[i] 2^(j-i-1) over the starts i < j; moving to j + 1 doubles s and adds a[j]. O(n log n) |
| `sum_subseq_widths_rank.kara` | the rank of each value, counted, with no sort: a value with b values below it, ties broken by position, and c above is the largest of 2^b subsequences and the smallest of 2^c. O(n^2) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples and four more
(three equal values; two values; six values with a repeat; and 1 to 40,
whose widths pass the modulus many times), and for 2,000 random cases of
up to 200 numbers, from 1 to 100,000 or, a third of the time, from 1 to
10 so that values repeat, the sum of the answers modulo `10^9 + 7`,
158611244, with a checksum. The O(n^2) arms keep the random cases well
below LeetCode's 10^5 numbers; the bench program takes arrays of that
size. `sum_subseq_widths.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every non-empty subsequence, chosen by the bits of a mask,
its largest value less its smallest, summed exactly and then taken
modulo `10^9 + 7`. It checks 3,200 random cases: 3,000 of up to 12
numbers from 1 to 3, 20 or 1,000 against the statement, and 200 of up to
200 numbers from 1 to 10 or 100,000 against the other properties. The
★ arm's answers sum to 235176086 modulo `10^9 + 7`.

| | property |
|---|---|
| P1 | the statement's sum, on up to 12 numbers |
| P2 | the answer is below the modulus and not negative, and the same for the numbers in any order |
| P3 | every number shifted up by the same amount keeps the answer, and every number scaled by 2 to 5 scales it |
| P4 | each number v turned into largest + 1 - v keeps the answer |
| P5 | a new largest number moved up by d adds d (2^n - 1), one d for each subsequence that holds it and some other number |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every case. It prints `3200 cases, 38962
numbers, widths sum to 235176086, 95000 checks over 5 arms: 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the values never sorted | P1 2494, P2 2719, P4 2882, P6 2694 |
| M2 | ★: the powers of two starting at 2 | P1 2722, P5 3200, P6 2922 |
| M3 | ★: the subsequences each value starts never taken away | P1 3000, P3 3200, P4 2974, P5 3200, P6 3200 |
| M4 | pairs: neighbouring values never taken as ends | P1 2722, P5 3200, P6 2922 |
| M5 | pairs: a pair weighted by the values before it, not between | P1 2425, P4 2535, P6 2625 |
| M6 | pairs: the powers of two counted up by one | P1 2233, P5 2691, P6 2431 |
| M7 | counting: each value moving the position on by one | P1 1220, P3 1307, P4 1355, P5 1505, P6 1307 |
| M8 | counting: the copies of a value counted, not their subsets | P1 1321, P3 1290, P4 1290, P5 4, P6 1407 |
| M9 | counting: the largest value never reached | P1 2722, P3 2922, P4 2426, P5 3200, P6 2922 |
| M10 | running: the sum of starts never doubled | P1 2491, P3 2691, P4 2517, P6 2691 |
| M11 | running: a value counted as a subsequence on its own | P1 3000, P3 3200, P4 2962, P5 3200, P6 3200 |
| M12 | running: the first value never taken | P1 2722, P4 2535, P5 3200, P6 2922 |
| M13 | rank: equal values each counted below the other | P1 1418, P3 1505, P4 1366, P5 4, P6 1505 |
| M14 | rank: the two powers the wrong way round | P1 2722, P5 3200, P6 2922 |
| M15 | rank: only the earlier values counted | P1 2494, P2 2726, P3 2694, P4 2900, P6 2694 |

P1 and P6 kill all fifteen. 2,722 of the 3,000 small cases have a
non-zero answer, and a mutant that scales or negates every answer (M2,
M14) or drops a whole class of subsequences (M4, M9, M12) fails exactly
those. P2 kills only the two mutants that make the answer depend on the
order of the numbers (M1, which never sorts, and M15, which ranks a
value only against the ones before it). M7, M8 and M13 go wrong only
when values repeat, which is why they fail fewer cases.

One mutant was replaced because it never changed an answer. The first
M3 returned the ★ arm's running total without the final step that makes
a negative remainder positive; in 3,200 cases, and in 2,000 random
cases of up to 200 numbers simulated in Python with Kāra's truncating
remainder, the total never ended negative. The last term added is the
largest value times 2^(n-1) - 1, modulo `10^9 + 7`, which almost always
outweighs a running total below the modulus (inferred, not proved). The
arms keep the step, as the remainder can still be negative in principle.

## Verification

Every arm prints the same output as `sum_subseq_widths.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 0.6 to 8.4 s
each (the two O(n^2) arms and the counting arm, which sizes its table
to the largest value, are the slow ones) and the differential 27 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy interpreter, JIT and `karac build --legacy`, with and
without auto-par, print the same output for the ★, pairs, running and
rank arms. Every legacy lane refuses the counting arm, the differential
and the bench program: `*x` on an element of `nums.iter()` is rejected
because legacy's iterator gives the value itself, not a reference.
Legacy is frozen, so this is not filed.

## Benchmarks

The bench program uses the counting arm, the same algorithm in all five
languages, where a sort would have measured each language's own
library sort (C's `qsort`, with a comparison function called through a
pointer, took 3.0 s on this workload against Rust's `sort` at 1.0 s). It
takes 400 random arrays of 100,000 numbers from 1 to 100,000,
LeetCode's largest, and every implementation prints `400 arrays of
100000 numbers: widths sum to 655369596, checksum 921255727`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.39 to 0.43 s | 0.41 s |
| Rust (`rustc -O`) | 0.62 to 0.74 s | 0.65 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.62 to 0.76 s | 0.68 s |
| Go | 0.84 to 1.02 s | 0.89 s |
| Python | 17.7 s | |
| Kāra (`karac build --mir`) | 0.42 to 0.51 s | 0.45 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 890's does. Legacy refuses the bench program
(above), so it has no row.

v2 takes 0.67 times Rust's median time under overflow checks and 1.10
times C's. Under valgrind's cachegrind C runs 1.98 billion
instructions, Rust with overflow checks 2.63 billion and v2 2.41
billion. Rust's lag is in the kernel, not in its code: one run spends
0.44 s in user time, as C does, and 0.24 s in system time, where under
`strace` it makes 1,599 `brk` calls against C's 5 and v2's 6, the heap
growing and shrinking around each array's buffers. The comparison with
C and Rust waits until after M4.
