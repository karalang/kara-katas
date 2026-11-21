# 2425. Bitwise XOR of All Pairings

You are given two **0-indexed** arrays, `nums1` and `nums2`, consisting
of non-negative integers. There exists another array, `nums3`, which
contains the bitwise XOR of **all pairings** of integers between `nums1`
and `nums2` (every integer in `nums1` is paired with every integer in
`nums2` **exactly once**).

Return *the **bitwise XOR** of all integers in `nums3`*.

```
nums1 = [2,1,3], nums2 = [10,2,5,0]  ->  13
nums1 = [1,2], nums2 = [3,4]          ->  0
```

**Constraints:** `1 <= nums1.length, nums2.length <= 10^5`;
`0 <= nums1[i], nums2[j] <= 10^9`.

XOR is associative and commutative, and a value XORed with itself
cancels. Each value of `nums1` enters `nums3` once for every value of
`nums2`, so it survives exactly when `nums2` has odd length, and the
same holds the other way round. The answer is the XOR of `nums1` when
`nums2.length` is odd, XORed with the XOR of `nums2` when
`nums1.length` is odd, in one pass over each.

## Approaches

| file | mechanism |
|---|---|
| `xor.kara` ★ | the XOR of `nums1` taken when `nums2` has odd length, and that of `nums2` XORed in when `nums1` has odd length. O(n + m) |
| `xor_naive.kara` | the statement read directly: every pairing XORed, one value of `nums1` with one of `nums2`, and all of them folded into the answer. O(n m) |
| `xor_bits.kara` | bit by bit: for each of the 30 bits, the pairings that hold it are those where exactly one value does, `ones1 (m - ones2) + (n - ones1) ones2` of them, and the bit is set when that count is odd. O(30 (n + m)) |
| `xor_map.kara` | a `Map[i64, i64]` of how many times each value enters the XOR of every pairing, a value of `nums1` `m` times and one of `nums2` `n` times; the values entered an odd number of times are XORed. O(n + m) |
| `xor_iter.kara` | iterators: each list's XOR by `fold`, the two paired with the other list's length in an array, kept by `filter` when that length is odd, and folded once more. O(n + m) |
| `xor_solution.kara` | LeetCode's Rust template: each list's XOR by `iter().fold(0, \|acc, &x\| acc ^ x)`, XORed into `ans` when the other's length is odd by `len() & 1 == 1`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples; one value
each; both lengths even; `nums2` odd; `nums1` odd; one value repeated
throughout; then the constraints' largest, `10^5` values against 3 and
3 against `10^5`, and 3000 against 3001, all up to `10^9`, each pair
answered both ways round; and 3000 random pairs of lists of 1 to 12
values, up to 1 to 16 or up to `10^9`, as a checksum and the total.
`xor.py` mirrors the ★ arm and its output is byte-identical, and the
mirror was checked on 20000 random pairs of lists of up to 9 values
against the XOR of every pairing.

`check` first reports 5 errors on the template, and `karac fix` carries
it in one call, reporting 11 edits: the brackets of each `Vec<i32>`; the
`&` of each pattern `|acc, &x|` dropped; `struct Solution;` given its
braces; then, once the template parses, `ans` declared `ans: i32`, since
its literal `0` kept the default `i64` and `ans ^= ..` does not fix it
(`E0200`), with each fold's seed written `0i32` to match; and the
wrapper's `as i64` on the method's `i32` answer dropped, since it widens
without one. `.len() & 1 == 1`, `fold` and the closures stand as Kāra.
The values fit an `i32`, as LeetCode's signature has them; the other
arms take `i64`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: `nums3` built with the XOR of every pairing, then every value
of it XORed together. No parity is used. It checks 300 random pairs of
lists of 1 to 10 values, up to 1 to 16 or up to `10^9`; then 30 of up
to 200 values up to `10^9`; then 30 pairs of lists of up to 20 copies
of one value each. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the two lists swapped: the same answer |
| P3 | each list reversed: the same answer |
| P4 | a value of `nums1` added twice more: the same answer |
| P5 | every value of both lists XORed with one mask: the same answer |
| P6 | each arm agrees with at least three of the other five |

P2 and P3 hold because `nums3` holds the same values whichever list
comes first and in whatever order. P4 holds because the two copies
leave the length's parity alone and enter `nums3` the same number of
times, so they cancel. P5 holds because `(x ^ k) ^ (y ^ k)` is `x ^ y`,
so `nums3` itself does not change.

The differential prints `360 cases: checksum 178913243, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and XORs every pairing. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: a value of nums2 ORed in | P1 165, P2 199, P5 137, P6 165 |
| M5 | ★: each value of nums1 with its low bit flipped | P1 90, P6 90 |
| M6 | ★: the answer started at 1 | P1 360, P6 360 |
| M8 | naive: only the first value of each pairing | P1 167, P2 236, P5 90, P6 167 |
| M9 | naive: the first of nums2 never paired | P1 326, P2 320, P3 140, P6 326 |
| M10 | naive: the pairings added | P1 354, P4 356, P6 354 |
| M12 | bits: only 16 bits | P1 130, P6 130 |
| M15 | bits: pairs where both hold the bit counted | P1 270, P5 227, P6 270 |
| M16 | bits: the bit set one high | P1 236, P6 236 |
| M19 | map: an even count taken | P1 341, P5 169, P6 341 |
| M20 | map: the values ORed | P1 206, P5 161, P6 206 |
| M21 | map: a repeated value of nums2 counted once | P1 82, P2 106, P5 63, P6 82 |
| M23 | iter: an even length taken | P1 331, P5 179, P6 331 |
| M24 | iter: nums1 folded by OR | P1 137, P2 236, P5 118, P6 137 |
| M25 | iter: the two kept added | P1 71, P5 90, P6 71 |
| M29 | solution: the second fold seeded with 1 | P1 187, P2 179, P6 187 |
| M31 | solution: the last of nums1 left out | P1 165, P2 257, P3 136, P4 105, P5 172, P6 165 |


P1 and P6 kill all seventeen, P5 ten, P2 seven, and P3 and P4 two
each.

Fourteen are not kept. Three fail exactly as a kept one: the naive
arm's each pairing ORed (M7) as the bits arm's pairs where both hold
the bit counted (M15), since a bit is then set where either value holds
it; the naive arm's pairings cut to 16 bits (M11) as the bits arm's
only 16 bits (M12); and the bits arm's even count taken (M14) as the ★
arm's answer started at 1 (M6), both failing every case. Eleven fail
apart from every kept one and were left out because those arms keep
their share already: the ★ arm's first list's own length read, first
value of `nums1` left out and `nums2` kept when `nums1` is even (M1,
M3, M4); the bits arm's pairs with the bit only in `nums2` left out
(M13); the map arm's each value of `nums1` counted once and `nums2`
counted by its own length (M17, M18), the second failing exactly as the
iter arm's `nums2` kept by its own length (M22); the iter arm's first
of `nums2` left out (M26); and the template's bit 1 of the length read,
second XOR assigned and `nums2` kept only when both are odd (M27, M28,
M30).

## Verification

Every arm prints the same output as `xor.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.4 to 2.5 s, but for the bits
arm, which takes 5.6 s there and 0.3 s under `karac run`: it walks each
list once for each of the 30 bits, through a `filter` closure. The
differential takes 2.1 s under `karac __mir-run`, 0.9 s under `karac
__mir-llvm-asan` and 0.5 s under `karac run`.

## Benchmarks

The bench builds 10 pairs of lists once from its own generator, pair `i`
of `10^5 - i` and `10^5 - i / 2 - 1` values up to `10^9`, so every mix
of odd and even lengths comes up, both even leaving nothing to do. It
then makes 500 passes; each changes one value of every first list, so
no answer can be carried from one pass to the next, and answers every
pair, folding the answer plus the pass into the checksum. The bench
uses the ★ arm, the XOR of a list taken when the other's length is
odd, in all five languages. Every implementation prints `500 passes
over 10 pairs of 10^5 values: checksum 354461683`. The lists are
growable arrays of 64-bit integers in every language, and a flat
`malloc`'d array in C.

BENCHTAB
