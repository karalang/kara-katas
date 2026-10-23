# 873. Length of Longest Fibonacci Subsequence

A sequence `x1, x2, ..., xn` is Fibonacci-like if `n >= 3` and `xi +
xi+1 == xi+2` for all `i + 2 <= n`. Given a strictly increasing array
`arr` of positive integers forming a sequence, return the length of the
longest Fibonacci-like subsequence of `arr`. If one does not exist,
return `0`. A subsequence is derived from another sequence by deleting
any number of elements (including none) without changing the order of
the remaining elements.

```
arr = [1,2,3,4,5,6,7,8]         ->  5    ([1,2,3,5,8])
arr = [1,3,7,11,12,14,18]       ->  3    ([1,11,12], [3,11,14] or [7,11,18])
```

**Constraints:** `3 <= arr.length <= 1000`, `1 <= arr[i] < arr[i + 1] <=
10^9`.

## Approaches

| file | mechanism |
|---|---|
| `len_longest_fib_subseq.kara` ★ | the longest run ending in each pair, through a value index: a run is fixed by its last two values, since the one before them is their difference. So `longest[j][k]`, the longest run ending `arr[j], arr[k]`, is one more than `longest[i][j]` when `arr[k] - arr[j]` is some `arr[i]` below `arr[j]`, and 2 otherwise; a `Map` from value to index finds `i`. O(n^2) time and space |
| `len_longest_fib_subseq_pointers.kara` | the same table, with the pairs before each value found by two pointers: for each `arr[k]`, the pairs `arr[i] + arr[j] == arr[k]` are found by closing in from both ends of `arr[0..k]`, which is increasing. O(n^2), no hashing |
| `len_longest_fib_subseq_greedy.kara` | every pair extended as far as it goes: the first two values fix the whole run, so each pair is followed forward while the sum of its last two values is in a `Set` of the array's values. The values at least double every two steps, so a run below 10^9 has at most about 45 values. O(n^2 log M) for values up to M |
| `len_longest_fib_subseq_search.kara` | the ★ table, with `arr[k] - arr[j]` found by a binary search of `arr[0..j]` instead of in a `Map`. O(n^2 log n) |
| `len_longest_fib_subseq_memo.kara` | the longest run starting at each pair, by memoized recursion: read forward, a run starting `arr[i], arr[j]` is 2 long when `arr[i] + arr[j]` is not in the array and one longer than the run starting `arr[j], arr[k]` when it is `arr[k]`. A `Map` keyed by the pair keeps each answer. O(n^2) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's two examples and nine
more (the shortest array, with a run and without; two arrays whose
longest run skips values, 4, 14, 18, 32, 50 and 5, 16, 21, 37; LeetCode's
extremes, 1 and 10^9, with a run and without; an array that is one run
end to end; the 43 Fibonacci
numbers from 1, 2 up to 10^9; and 1 to 1000, LeetCode's largest length,
whose answer is the 15 Fibonacci numbers up to 987); the lengths of
3,000 random arrays of 3 to 12 values with gaps up to 4, 10,574 in all
with 193 arrays having no run; and 4 arrays of 1000 values, two dense and
two up to 10^9 with a run of 10 and of 30 planted, with a checksum.
`len_longest_fib_subseq.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every subsequence, built one value at a time from left to
right and given up as soon as a value is not the sum of the two before
it, the longest that reaches 3 values. It checks 1,700 arrays: 1,500 of
3 to 12 values with gaps up to 5 against the statement, and 200 of 20 to
79 values, dense or up to 10^9 with a run of 2 to 21 values planted,
against the other properties. The ★ arm's lengths sum to 7,226.

| | property |
|---|---|
| P1 | the statement's answer (up to 12 values) |
| P2 | the answer is 0, or a length from 3 to the array's length |
| P3 | every value multiplied by the same factor, 2 to 4, gives the same answer |
| P4 | dropping one value never gives a longer run |
| P5 | a value above all the others never shortens the longest run, and the sum of the last two values added makes it at least 3 |
| P6 | at least two of the other arms give the same answer |

It prints `1700 arrays, lengths sum to 7226, 49250 checks over 5 arms: 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a pair allowed to follow itself (`before <= arr[j]`) | P1 670, P2 162, P6 707 |
| M2 | ★: a run extended by two | P1 1464, P2 196, P6 1663 |
| M3 | ★: a pair counted as one value | P1 1464, P2 814, P5 413, P6 1663 |
| M4 | pointers: a value taken twice as its own pair | P1 212, P6 214 |
| M5 | pointers: the third value never a sum | P1 477, P6 603 |
| M6 | pointers: the right pointer moved when the sum is too small | P1 488, P4 30, P5 110, P6 648 |
| M7 | greedy: a lone pair counted | P1 36, P2 37, P6 37 |
| M8 | greedy: adjacent values never a starting pair | P1 625, P5 408, P6 756 |
| M9 | greedy: the last two values both set to the sum | P1 565, P6 736 |
| M10 | search: the search lands past an equal value | P1 1464, P5 1700, P6 1663 |
| M11 | search: the value before searched for up to `k` | P1 944, P2 162, P6 1013 |
| M12 | search: the value just before `arr[j]` never found | P1 817, P5 408, P6 966 |
| M13 | memo: a pair with no next value counted as one | P1 1464, P5 413, P6 1663 |
| M14 | memo: a run continued from its first and third values | P1 753, P6 936 |
| M15 | memo: the next value looked up as twice the first | P1 934, P2 43, P5 279, P6 1112 |

P1 kills all fifteen, and P6 does too, on arrays too long for the
literal reading. P3 kills none: every mutation here is wrong at every
scale, so an arm compared with itself on scaled values agrees with
itself. Two mutants tried first were equivalent and were replaced with
M12 and M14: the binary search's upper bound one lower (the final
comparison still checks the last place), and pairs ending at the last
value never started (such a pair has nothing after it, so it can only be
a run of 2).

## Verification

Every arm prints the same output as `len_longest_fib_subseq.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are at kara
`e903d5b111`. Under `karac __mir-run` the arms take 3 to 18 s (the memo
arm, whose `Map` is keyed by pairs, the slowest) and the differential
16 s; the 1,000-value arrays were cut from 8 to 4 to keep the memo arm
there.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends refuse all five arms, the differential and
the bench program at a `*` on a `for` element, saying the value is not a
reference, where v2 yields a reference. Legacy is frozen, so this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 100 arrays of
1000 values, LeetCode's largest, from the same generators, half dense
(each value at most 2 to 6 above the one before) and half up to 10^9
with a run of 11 to 39 values planted, built once and then each solved, summing the lengths and a
checksum. The value index is a `Map` in Kāra, a `HashMap` in Rust (both
SipHash-1-3), a `map` in Go, a `dict` in Python, and in C, which has no
hash map, an open-addressing table with a multiplicative hash. Every
implementation prints `100 arrays of 1000 values: lengths sum to 1591,
checksum 84612133`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.38 to 0.48 s | 0.43 s |
| Rust (`rustc -O`) | 1.14 to 1.22 s | 1.19 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.15 to 1.31 s | 1.24 s |
| Go | 1.25 to 1.34 s | 1.29 s |
| Python | 6.8 s | |
| Kāra (`karac build --mir`) | 1.07 to 1.19 s | 1.10 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 872's does. Legacy refuses the bench program
(above), so it has no lane here.

v2 takes 0.89 times Rust's median time under overflow checks and 2.6
times C's. Under valgrind's cachegrind C runs 0.97 billion instructions,
Rust with overflow checks 3.45 billion and v2 4.95 billion. Under
callgrind 70% of v2's are in the map's runtime calls, 2.16 billion in
`karac_hash_word` and 1.33 billion in `karac_mir_map_find_hv`, where Rust
inlines its hashing and lookup into `main`. v2 still finishes first of
the two, so the instruction count is not what sets the time; each array's
table of a million entries, 8 MB, is past the caches in every language,
which most likely makes its reads and writes the larger cost (inferred
from the timings, not traced). C's cheaper hash is the plainest reason
for its lead. The comparison with C and Rust waits until after M4.
