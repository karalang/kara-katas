# 898. Bitwise ORs of Subarrays

Given an integer array `arr`, return the number of distinct bitwise ORs
of all the non-empty subarrays of `arr`.

The bitwise OR of a subarray is the bitwise OR of each integer in the
subarray. The bitwise OR of a subarray of one integer is that integer.

A subarray is a contiguous non-empty sequence of elements within an
array.

```
arr = [0]      ->  1
arr = [1,1,2]  ->  3
arr = [1,2,4]  ->  6
```

**Constraints:** `1 <= arr.length <= 5 * 10^4`, `0 <= arr[i] <= 10^9`.

## Approaches

Extending a subarray to the left only ever adds bits, so the subarrays
ending at one place have at most 31 different ORs, one more for each bit
added, and all the ORs number at most 31 times the length. The arms
differ in how they reach each place's ORs and in how they count the
different ones.

| file | mechanism |
|---|---|
| `subarray_bitwise_ors.kara` ★ | the ORs ending at each place: those ending at `i - 1` with `arr[i]` put in, and `arr[i]` alone, kept in a `Set` from place to place and gathered into another. O(n * 31) |
| `subarray_bitwise_ors_back.kara` | each number folded back: in a copy of the array, the OR of every subarray from an earlier place to the current one, `arr[i]` OR-ed in from `i - 1` backwards until a running value already holds all its bits, which all before it then do. O(n * 31) |
| `subarray_bitwise_ors_sorted.kara` | lists in place of sets, and one sort: the ORs ending at a place rise from the shortest subarray to the longest, so a list of them stays in order and repeats sit side by side; every list is appended to one, which is sorted and its different values counted. O(n * 31 * log) |
| `subarray_bitwise_ors_table.kara` | the ★ arm with a hash table of its own: the same short lists, every value gathered into an open-addressing table written in the kata, with a multiplicative hash, linear probing and doubling at half full. O(n * 31) |
| `subarray_bitwise_ors_bits.kara` | where each bit was last seen: the OR of `arr[j..=i]` changes only as `j` passes the last place at or before `i` where one of the 30 bits was set, so those places, sorted, are walked from the nearest back. O(n * 30 * log 30) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples and five
more (three zeros, four sevens, the first eight powers of two, a mixed
five, and LeetCode's largest values); for 300 random cases of up to
1,000 numbers, a third of them up to 8, below 2^1 to 2^30, half of them
sparse (a random number AND-ed with another), the ORs in all, 233,818,
with a checksum; and two of LeetCode's largest, 50,000 numbers up to
10^9 and 50,000 sparse numbers below 2^12. `subarray_bitwise_ors.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the OR of every subarray `arr[i..=j]`, element by element,
for every `i <= j`, the different ones counted in a `Set`. It checks
3,200 random cases: 3,000 of up to 12 numbers below 2^1 to 2^6 against
the statement, and 200 of up to 400 numbers below 2^1 to 2^30 against
the other properties, half of them sparse. The ★ arm finds 109,289 ORs
in all.

| | property |
|---|---|
| P1 | the statement's count, on the small cases |
| P2 | at least the number of different numbers, each a subarray of one, and at most one for each subarray, 31 for each place, and 2 to the width of the OR of everything |
| P3 | the same count for the array read backwards |
| P4 | the same count with the bits of every number reversed within that width, and with a bit no number has set in every number |
| P5 | a random number added at the end adds at most 31 ORs, those ending there, and takes none away |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every case. It prints `3200 cases, 109289 ORs
in all, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
and `karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan`
with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `arr[i]` never put into the longer ORs | P1 1554, P6 1729 |
| M2 | ★: the ORs ending here never carried on | P1 1554, P6 1729 |
| M3 | ★: only the ORs ending at the last place counted | P1 2219, P2 2088, P3 1694, P5 934, P6 2415 |
| M4 | back: a number alone not counted | P1 3000, P2 2527, P3 1361, P6 3200 |
| M5 | back: the fold never reaching the first place | P1 622, P3 774, P6 739 |
| M6 | back: the number put in with XOR | P1 1212, P2 70, P3 1287, P4 2236, P5 86, P6 1376 |
| M7 | sorted: the long list never sorted | P1 2313, P2 1323, P3 2305, P6 2511 |
| M8 | sorted: values one apart counted once | P1 2121, P2 1596, P4 1348, P5 198, P6 2311 |
| M9 | sorted: 0 kept in place of the number alone | P1 1129, P2 223, P3 1249, P4 1817, P6 1256 |
| M10 | table: a value already in never found | P1 2503, P2 1470, P3 2272, P4 69, P6 2701 |
| M11 | table: the count kept through a doubling | P2 25, P5 2, P6 158 |
| M12 | table: 0 dropped when the table doubles | P3 17, P4 17, P6 17 |
| M13 | bits: each bit seen one place early | P1 524, P3 644, P4 23, P6 657 |
| M14 | bits: the places never sorted | P1 532, P3 762, P4 839, P6 697 |
| M15 | bits: only pairs with `arr[i]` counted | P1 524, P3 699, P6 683 |

P6 kills all fifteen, and P1 all but the two table mutants (M11, M12),
whose faults wait for the table's first doubling, at 33 values, which
none of the small cases, 12 numbers of at most 6 bits, reaches. M1 and M2
fail the same cases: both count only the numbers themselves, which keeps
every property but P1 and P6, since that count is also unchanged by
reversing the array or renaming its bits and grows by at most one when
a number is added. P3 kills the mutants that treat the two ends
differently, such as the fold that stops short of the first place (M5),
and it and P4 are what catch M12, since reversing the array or renaming
the bits changes whether 0 is already in the table when it first
doubles. P4 kills the mutant that merges values one apart (M8), as
renaming the bits moves which values are one apart.

No mutant had to be replaced.

## Verification

Every arm prints the same output as `subarray_bitwise_ors.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 1.5 to 12.2 s
each (the table arm, whose hash table is interpreted step by step, is
the slow one) and the differential 26 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The back and bits arms print the same output under every frozen legacy
lane, the interpreter, the JIT and `karac build --legacy` with and
without auto-par. Every legacy lane refuses the ★, sorted and table
arms, the differential and the bench program: `*x` on an element of
`.iter()` is rejected, because legacy's iterator gives the value
itself. Legacy is frozen, so this is not filed.

## Benchmarks

The bench program uses the table arm, so that no language's library set
or sort is what gets measured: 12 arrays of 50,000 numbers, LeetCode's
largest, each a random number below 2^30 AND-ed with a second, so that
about a quarter of the bits are set and more ORs end at each place
than for dense numbers. The hash table, its hash and its probing are the
same code in all five languages. Kāra, Rust, Go and Python build a new
short list at every place, as the arm does; C keeps two fixed arrays of
32 and swaps them. Every implementation prints `12 arrays of 50000
numbers: 3360578 ORs in all, checksum 963950627`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.42 to 0.51 s | 0.45 s |
| Rust (`rustc -O`) | 0.51 to 0.58 s | 0.54 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.51 to 0.59 s | 0.53 s |
| Go | 0.56 to 0.65 s | 0.59 s |
| Python | 20.3 s | |
| Kāra (`karac build --mir`) | 0.42 to 0.54 s | 0.44 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 897's does. Legacy refuses the bench program
(above), so it has no row.

v2 takes 0.82 times Rust's median time under overflow checks and 0.96
times C's. Under valgrind's cachegrind C runs 1.76 billion instructions
and mispredicts 16.3 million branches, Rust with overflow checks 2.63
billion and 23.1 million, and v2 2.87 billion and 19.0 million. v2 runs
the most instructions of the three and still beats Rust; it mispredicts
4 million fewer branches, which may be the difference, though that was
not measured beyond these counts. The comparison with C and Rust waits
until after M4.
