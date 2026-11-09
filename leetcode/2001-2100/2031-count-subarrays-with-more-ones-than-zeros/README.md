# 2031. Count Subarrays With More Ones Than Zeros

Given a binary array `nums`, return the number of subarrays that hold more
1s than 0s. The answer may be large, so return it modulo `10^9 + 7`.

```
nums = [0,1,1,0,1]  ->  9
nums = [0]          ->  0
nums = [1]          ->  1
```

**Constraints:** `1 <= nums.length <= 10^5`; `0 <= nums[i] <= 1`.

Count a 1 as +1 and a 0 as -1. A subarray holds more 1s than 0s exactly
when the prefix sum at its end is above the prefix sum at its start, so the
answer is the number of pairs of prefix sums `i < j` with `p[i] < p[j]`.
The prefix sums move one step at a time, so the count of earlier prefixes
below the current one moves by the count at a single sum.

## Approaches

| file | mechanism |
|---|---|
| `subarrays.kara` ★ | the prefix sums counted in an array offset by `n`; the count below the current sum gains the count at the old sum on a step up and loses the count at the new sum on a step down. O(n) |
| `subarrays_map.kara` | the same counts in a `Map[i64, i64]` keyed by the sum itself, read with `get(..).unwrap_or(0)` and bumped through `entry(..).or_insert(0)`. O(n) expected |
| `subarrays_fenwick.kara` | a Fenwick tree (a struct with `mut ref self` methods) over the shifted sums; each prefix asks how many earlier ones lie strictly below it, then adds itself. O(n log n) |
| `subarrays_merge.kara` | the rising pairs of prefix sums counted by a recursive merge sort through `mut ref` buffers: while two sorted halves merge, each sum from the right counts the left sums below it. O(n log n) |
| `subarrays_segtree.kara` | a segment tree kept bottom up in one array, summed from both ends of the range below the current sum, then updated up from its leaf. O(n log n) |
| `subarrays_solution.kara` | LeetCode's Rust template (a unit struct, `impl Solution`, a `const` inside the body, `1_000_000_007`, `vec![0i64; ..]`, `for &x in nums.iter()`, `as i32`, a `&Vec` wrapper with `|&x|`), carried by `karac fix` to a clean check |
| `differential.kara` | all six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's three
examples and five more; then the total and a checksum of the answers for
3000 arrays of 1 to 20 bits, the 1s at odds of their own, and a checksum
for 6 arrays of 100000 bits, one of them all 1s, whose 5000050000
subarrays pass the modulus. `subarrays.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every subarray tried and its 1s and 0s counted one by one. It
checks 1500 arrays of 1 to 12 bits, the 1s at odds of their own. Every
array is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the array reversed leaves the answer |
| P3 | the answer, the answer for every bit flipped, and the subarrays with as many 1s as 0s (counted literally) make up all `n (n + 1) / 2` |
| P4 | with a 1 appended, the answer grows by the suffixes holding at least as many 1s as 0s, the empty one included (counted literally) |
| P5 | the first 0 turned into a 1 raises the answer |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a subarray reversed holds the same bits. P3 because every
subarray has more 1s, more 0s or as many of each, and flipping the bits
swaps the first two. P4 because the new subarrays all end at the new 1,
and one starting after position `i` has more 1s exactly when the old part
of it has at least as many 1s as 0s. P5 because every subarray holding
that bit gains two and the bit alone now counts.

The differential prints `1500 arrays: checksum 926416892, 54000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept, three to
each of the five Kāra arms and two to the Rust arm. All thirty are killed,
each fails the same way under both backends, none by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the count at the new sum added on a step up | P1 976, P2 553, P3 1500, P4 1031, P5 843, P6 976 |
| M2 | ★: a step down takes away the count at the old sum | P1 970, P2 553, P3 1500, P4 939, P5 17, P6 970 |
| M3 | ★: a step up adds one more | P1 1167, P2 730, P3 1500, P4 1500, P6 1167 |
| M4 | map: a sum not yet seen read as 1 on a step down | P1 882, P2 607, P3 1500, P4 882, P6 882 |
| M5 | map: each prefix entered afresh rather than counted | P1 564, P2 448, P3 757, P4 679, P6 564 |
| M6 | map: the count below never lowered | P1 761, P2 722, P3 846, P4 761, P5 217, P6 761 |
| M7 | fenwick: the query includes the current sum | P1 846, P3 846, P4 891, P6 846 |
| M8 | fenwick: an add steps up one index at a time | P1 632, P2 335, P3 1104, P4 727, P5 17, P6 632 |
| M9 | fenwick: a query steps down one index at a time | P1 737, P2 331, P3 1264, P4 893, P5 5, P6 737 |
| M10 | merge: the left count taken from index 0 | P1 1379, P3 1379, P4 1500, P6 1379 |
| M11 | merge: the merged run never copied back | P1 581, P2 598, P3 726, P4 555, P6 581 |
| M12 | merge: a run of two left unsorted | P1 1091, P2 540, P3 1455, P4 1150, P5 293, P6 1091 |
| M13 | segtree: a left end taken when even | P1 801, P2 442, P3 1360, P4 1269, P5 106, P6 801 |
| M14 | segtree: the walk stops one level early | P1 801, P2 442, P3 1360, P4 1269, P5 369, P6 801 |
| M15 | segtree: a right end taken when even | P1 953, P2 532, P3 1379, P4 1011, P5 449, P6 953 |
| M16 | Rust: each prefix counted twice | P1 1061, P2 576, P3 1379, P4 1500, P6 1061 |
| M17 | Rust: the last running count added once more | P1 893, P2 576, P3 1500, P4 1500, P6 893 |

P1, P3, P4 and P6 kill all seventeen, P2 fifteen and P5 nine. P2 reverses
the array, so it misses exactly the edits whose wrong answer is itself
symmetric: the query including the current sum (M7) and the left count
taken from index 0 (M10). M7 counts the subarrays with at least as many 1s
as 0s, which reversing leaves alone. P5 turns the first 0 into a 1 and asks
only for a rise, so it sees the edits that can lower an answer as a bit is
raised: a step that reads the count at the wrong sum (M1, M2), the count
below never lowered (M6), the Fenwick and segment trees walked wrongly (M8,
M9, M13 to M15), and a run of two left unsorted (M12).

The other thirteen fail as a kept one does, or with counts of their own.
The Rust arm's count at the new sum fails as M1, the map arm's step down
before moving as M2, and the Rust arm's running count never lowered as M6.
Four edits fail with exactly M7's counts: a 0 leaving the sum where it was
(★), an equal left sum counted as below and a 1 worth 2 in the sums
(merge), and the range below including the current leaf (segment tree). The
second and fourth count `>=` as M7 does; the other two reach the same
counts on these 1500 arrays by another road. The empty prefix never counted
fails alike in the ★, map, Fenwick and Rust arms; a 0 moving the Fenwick
sum up and the segment tree's leaf never updated fail with counts of their
own. Three drafts changed no answer and were replaced: a sum not yet seen
read as 1 on a step up (the current sum is always seen), a Fenwick add
stopping one node short (the highest sum is added last and never asked
about), and the segment tree's root never updated (no query reads the
root).

## Verification

Every arm prints the same output as `subarrays.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them. Under `karac __mir-run` the arms take 1.0 s to 7.6 s, most of it
the six arrays of 100000 bits, and the differential 1.7 s.

The five arms were written in Kāra and checked clean but one: the Fenwick
arm first wrote its `add` as `fn add(mut self, at: i64)`, Rust's spelling
of a receiver that writes. The check refused it with the Kāra spelling and
a machine fix to `mut ref self`, which `karac fix` applied.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` alone, in three rounds (9, 2 and 1 edits). The
first carries the unit struct, `Vec<..>` twice, the `&` in `for &x in` and
in `|&x|`, the `&Vec` parameter and the `::` path. The second drops the
`i64` suffix of `0i64` and the wrapper's `ref`; the deprecated `vec![0;
..]` around the suffix overlaps it, so its fix waits for the third round,
which writes `Vec.filled(2 * n + 1, 0)`. The `const MOD` inside the
function body and the `1_000_000_007` literal are accepted as written (a
block may declare a constant, design.md § Constants).

## Benchmarks

The bench builds 20 arrays of 100000 bits once in all five languages,
array `a` with odds `a % 9 + 1` in 10 of a 1, then runs 100 rounds, each
flipping one bit of each array before the ★ arm answers it: 2000 calls,
each a pass over 100000 bits with an array of 200001 counts. Every
implementation prints `2000 calls: sum 636553529, checksum 556219170`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 1.116 to 1.335 s | 1.175 s |
| Rust (`rustc -O`) | 1.152 to 1.318 s | 1.220 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.206 to 1.390 s | 1.256 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.191 to 1.399 s | 1.263 s |
| Kāra (`karac build`) | 1.231 to 1.361 s | 1.298 s |
| Go | 1.415 to 1.527 s | 1.478 s |
| Python | 25.1 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (1.251 s) is not above its real time (1.298 s).

The sequential Kāra program is 0.99x Rust under overflow checks and 1.07x
C.