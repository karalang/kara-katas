# 905. Sort Array By Parity

Given an integer array `nums`, move all the even integers at the
beginning of the array followed by all the odd integers.

Return **any array** that satisfies this condition.

```
nums = [3,1,2,4]  ->  [2,4,3,1]    ([4,2,3,1], [2,4,1,3] and [4,2,1,3] would also be accepted)
nums = [0]        ->  [0]
```

**Constraints:** `1 <= nums.length <= 5000` and `0 <= nums[i] <= 5000`.

## Approaches

| file | mechanism |
|---|---|
| `sort_array_by_parity.kara` ★ | two pointers from both ends: the left one walks past even numbers, the right one past odd ones, and when both stop they swap. In place, O(n) |
| `sort_array_by_parity_stable.kara` | two passes into a new array, the even numbers and then the odd ones, each in the order given. Stable, O(n) time and space |
| `sort_array_by_parity_lomuto.kara` | one pointer for the place the next even number goes: every even number met is swapped there and the place moves on. In place, O(n) |
| `sort_array_by_parity_sort.kara` | a sort keyed on each number's remainder mod 2. O(n log n) |
| `sort_array_by_parity_recursive.kara` | divide and conquer: each half sorted by parity, then the evens of both halves before the odds of both. O(n log n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Since any order within each side is accepted, the arms give different
answers, and the harness prints what they must share. Every arm prints
the same 12 lines: for LeetCode's two examples and seven more (`[1]`,
`[2,4,6]`, `[1,3,5]`, `[1,2]`, `[2,1]`, `[1,2,3,4,5,6,7,8]` and
`[5000,4999,0,1,2,3,3,2]`), the answer's even and odd numbers each
sorted, and whether the answer fits (the numbers of `nums`, every even
one first); for 300 random cases of up to 5,000 numbers, from no even
number to all, how many fit, the evens in front in all, and a checksum
of the numbers on each side that does not depend on their order; and
two of LeetCode's largest, 5,000 numbers half of them even, and 4,999
odd numbers followed by 5000. `sort_array_by_parity.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every pair of places in the answer checked for an odd number
before an even one, and every number counted in the answer and in
`nums`. It checks 3,200 random cases: 3,000 of up to 12 numbers against
the statement and 200 of up to 500 against the other properties, with
numbers up to 3, 10 or 5,000 and from no even number to all; 69,206
numbers in all.

| | property |
|---|---|
| P1 | the statement allows the answer, on the small cases |
| P2 | n numbers, the first of them as many as `nums` has even ones and all even, the rest odd |
| P3 | the answer sorted is `nums` sorted |
| P4 | the reversed `nums` gives as many evens in front and the same numbers on each side |
| P5 | every number one more, which swaps even and odd, gives as many numbers in front as this answer has behind, its odd numbers one more in front and its even ones one more behind |
| P6 | each arm agrees with at least two of the other four on how many evens lead and which numbers are on each side |

P2 to P6 are checked on every case. It prints `3200 cases, 69206
numbers, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
and `karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan`
with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the left pointer stopping at even numbers | P1 1679, P2 1873, P4 1405, P5 2099, P6 1873 |
| M2 | ★: the pointers stopping one apart | P1 438, P2 466, P4 716, P5 837, P6 466 |
| M3 | ★: the first number never looked at | P1 934, P2 1033, P4 1019, P5 2099, P6 1033 |
| M4 | stable: the even numbers copied twice, the odd ones never | P1 3000, P2 3200, P3 3200, P5 3200, P6 3200 |
| M5 | stable: only multiples of 4 taken as even | P1 2011, P2 2206, P3 2206, P5 3003, P6 2206 |
| M6 | stable: a 0 left at the front | P1 3000, P2 3200, P3 3200, P5 3200, P6 3200 |
| M7 | lomuto: nothing moved | P1 1679, P2 1873, P4 1405, P5 2099, P6 1873 |
| M8 | lomuto: the first number never looked at | P1 540, P2 630, P4 653, P5 1239, P6 630 |
| M9 | lomuto: an even number already in place passed over | P1 540, P2 630, P4 653, P5 1239, P6 630 |
| M10 | sort: odd numbers first | P1 1905, P2 2099, P5 2099, P6 2099 |
| M11 | sort: keyed on the remainder mod 3 | P1 1739, P2 1933, P4 1064, P5 2074, P6 1933 |
| M12 | sort: keyed on the number itself | P1 1569, P2 1761, P5 2099, P6 1761 |
| M13 | recursive: two numbers taken as one | P1 2770, P2 2969, P3 2969, P4 2760, P5 2969, P6 2969 |
| M14 | recursive: the right half's first odd number lost | P1 2239, P2 2436, P3 2436, P4 1757, P5 2969, P6 2436 |
| M15 | recursive: every single number taken as the first | P1 2718, P2 2099, P3 2917, P4 2512, P6 2917 |

P1, P2 and P6 kill all fifteen; P5 kills fourteen, P4 ten and P3 six.
P3 sees only the six mutants that change which numbers are in the
answer. P4 sees only an answer that depends on the order the numbers
come in: M4, M5, M6, M10 and M12 give the same evens in front and the
same numbers on each side whatever the order. M15 answers n copies of
the first number, and adding one to every number before or after that
gives the same, so P5 holds for it. M1 and M7 fail exactly the same
cases: M1 swaps only even numbers with even ones, so every place keeps
the parity it was given, which is what moving nothing gives. M8 and M9
are the same edit in effect: when the first number is even, each starts
swapping later even numbers into place 0, and when it is odd, both work.

No mutant was replaced. The first run found two faults in the
differential instead. P5 read the answer place by place up to n, so
the four mutants whose answers had another length (M4, M5, M13 and
M14) stopped it with an index out of bounds; P5 now takes the answer's
numbers as they are. And P4 to P6 compared only which numbers were on
each side, so the nine mutants that get the order wrong but keep the
numbers were seen by P1 and P2 alone; those three properties now
compare how many evens lead as well.

## Verification

Every arm prints the same output as `sort_array_by_parity.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 2.2 to 8.1 s
each (the recursive arm the longest, 8.1 s, the others 4 s or less) and
the differential 7.6 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

Every frozen legacy lane refuses every arm and the differential: `*x`
on an element of `.iter()` is rejected, because legacy's iterator gives
the value itself. In the arms this is the harness's `show`, which sorts
each side of the answer; the stable arm also does it in the arm itself.
The bench program has no such loop, and a legacy build of it prints the
same line as the other five. Legacy is frozen, so none of this is filed.

## Benchmarks

The bench program uses the ★ arm on 1,000,000 numbers below 5001, built
once. Each round sorts a copy by parity, counts the evens in front,
folds that count and one number of the answer into a checksum and
changes one number; 100 rounds. Every implementation copies the numbers
each round, as the Kāra program's `clone` does. Every implementation
prints `100 rounds over 1000000 numbers: 49944613 evens in front,
checksum 397656000`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.63 to 0.76 s | 0.71 s |
| Rust (`rustc -O`) | 0.62 to 0.77 s | 0.66 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.67 to 0.77 s | 0.74 s |
| Go | 1.06 to 1.17 s | 1.13 s |
| Python | 13.7 s | |
| Kāra (`karac build --mir`) | 0.65 to 0.77 s | 0.70 s |
| Kāra (legacy `karac build`) | 0.59 to 0.71 s | 0.64 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does.

v2 takes 0.94 times Rust's median time under overflow checks, 0.98
times C's and 1.10 times legacy's; the runs overlap so much that the
order among C, both Rusts and the two Kāra builds is not settled by
eight of them. Every program spends its time on one branch: whether the
number at a pointer is even is a coin toss here, and under valgrind's
cachegrind each mispredicts about 50 million times, 13% to 20% of its
branches. C runs 1.03 billion instructions and 0.25 billion
branches, Rust with overflow checks 1.31 billion and 0.39 billion, v2
1.25 billion and 0.39 billion, and legacy 0.99 billion and 0.26
billion. The comparison with C and Rust waits until after M4.
