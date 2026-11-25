# 1356. Sort Integers by The Number of 1 Bits

You are given an integer array `arr`. Sort the integers in the array in
ascending order by the number of 1's in their binary representation,
and in case of two or more integers have the same number of 1's you
have to sort them in ascending order.

Return the array after sorting it.

```
arr = [0,1,2,3,4,5,6,7,8]                    ->  [0,1,2,4,8,3,5,6,7]
arr = [1024,512,256,128,64,32,16,8,4,2,1]    ->  [1,2,4,8,16,32,64,128,256,512,1024]
```

**Constraints:** `1 <= arr.length <= 500`, `0 <= arr[i] <= 10^4`.

Each arm is `fn sort_by_bits(arr: Vec[i32]) -> Vec[i32]`.

## Approaches

| file | mechanism |
|---|---|
| `sort_by_bits.kara` ★ | one sort keyed by the pair (the number of 1 bits, the value), which orders by bits first and breaks ties by value. O(n log n) |
| `sort_by_bits_insertion.kara` | each value's 1 bits counted by clearing the lowest one at a time (Kernighan's loop), then an insertion sort that moves a value left past every value that should come after it. O(n^2) |
| `sort_by_bits_buckets.kara` | how often each value from 0 to 10^4 occurs, counted once; then for each number of 1 bits from 0 to 14, every value with that many in increasing order, as often as it occurs. A counting sort, O(n + 15 V) for values up to V |
| `sort_by_bits_packed.kara` | each value packed with its number of 1 bits into one integer, the bits above 2^14 and the value below, so a plain sort of the packed integers orders by bits and then by value; the value is the remainder. O(n log n) |
| `sort_by_bits_solution.kara` | a Rust solution as LeetCode's Rust users write it (`arr.sort_by(\|a, b\| a.count_ones().cmp(&b.count_ones()).then(a.cmp(b)))` on a `mut arr: Vec<i32>`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 5 lines: LeetCode's two examples; one value,
the largest, equal values, and the 14 powers of two up to 10^4, largest
first; 500 values, the constraints' most, from 0 to 10^4 (`500 values:
first 1024, middle 9493, last 8191`); and 2000 random arrays of 1 to
500 values, from 0 to 15, 0 to 1000 or 0 to 10^4, each answer folded
into a checksum (`2000 random arrays: checksum 439386680`).
`sort_by_bits.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run`
and `karac __mir-llvm-run`.

The Mend loop: the ★, insertion, buckets and packed arms check clean.
The Rust solution takes one round of 8 fixes by `karac fix`'s count:
`struct Solution;` becomes `struct Solution {}`, `mut arr: Vec<i32>`
becomes `arr: own Vec[i32]` and a `let mut arr = arr;`, each `Vec<i32>`
`Vec[i32]`, and `cmp(&b.count_ones())` drops its `&`, an argument being
borrowed with no sigil; `.cmp(..).then(..)` stands as Rust wrote it.
Every arm matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: again and again, of the integers left, the one with the
fewest 1's, the smallest of those, taken out and put next, each
integer's 1's counted by reading its 14 places one by one. 2000 arrays
of 1 to 12 integers in four kinds, 500 each: from 0 to 15; from 0 to
100; from 0 to 10^4; and powers of two and their neighbours, 2^k - 1,
2^k and 2^k + 1 up to 10^4. Every array is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the same integers, each as often as in `arr` |
| P3 | the integers in the opposite order: the same answer |
| P4 | in order: each integer's 1's no fewer than the one before's, and its value no smaller where they tie |
| P5 | `arr` twice over: each integer of the answer twice, in place |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 arrays: checksum 923493424,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python's `sorted`, keyed by
`bin(x).count("1")` and the value, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: ties put largest first | P1 1570, P4 1570, P6 6280 |
| M2 | ★: the value compared before the bits | P1 1429, P4 1429, P6 5716 |
| M3 | insertion: the first place never reached | P1 1459, P3 1791, P4 1459, P5 1459, P6 1459 |
| M4 | insertion: a tie moved first whatever its value | P1 1315, P3 1554, P4 1315, P5 1570, P6 1315 |
| M5 | buckets: a repeated value written once | P1 640, P2 640, P5 2000, P6 640 |
| M6 | buckets: 0 never written | P1 283, P2 283, P6 283 |
| M7 | packed: a value from 2^13 up loses its top bit | P1 469, P2 469, P4 404, P6 469 |
| M8 | packed: never sorted | P1 1718, P3 1839, P4 1718, P5 1843, P6 1718 |
| M9 | solution: the most 1 bits first | P1 1792, P4 1792, P6 1792 |
| M10 | solution: ties left in their order | P1 1318, P3 1554, P4 1318, P5 1570, P6 1318 |

P1 and P6 kill all ten, P4 eight, P5 five, P3 four and P2 three. The
same integers (P2) catch the three edits that lose or change a value: a
repeated value written once (M5), 0 never written (M6) and a top bit
lost in the packing (M7); the first two still come out in order, so P4
misses them. The opposite order (P3) catches the edits whose answer
depends on where the integers start: the insertion arm's two slips (M3,
M4), the packed keys never sorted (M8) and ties left as they came
(M10). `arr` twice over (P5) catches those four as well, and the
repeated value written once, which it makes of every value.

## Benchmarks

The bench builds 20 arrays of 500 values from 0 to 10^4, the
constraints' most, once; then makes 2 * 10^4 rounds, each setting one
place of one array to a value, all drawn from the checksum so far, so no
answer carries over, sorting it with the ★ arm's keyed sort, and
folding three values of the answer into the checksum. Every
implementation prints `20000 rounds over 20 arrays of 500 values:
checksum 225775334`. C sorts with `qsort` and a comparison function
over `__builtin_popcount`, Go with `sort.Slice` over
`bits.OnesCount32`, Rust and Python with a key of the pair.

BENCHTAB
