# 2317. Maximum XOR After Operations

You are given a **0-indexed** integer array `nums`. In one operation,
select **any** non-negative integer `x` and an index `i`, then
**update** `nums[i]` to be equal to `nums[i] AND (nums[i] XOR x)`.

Note that `AND` is the bitwise AND operation and `XOR` is the bitwise
XOR operation.

Return *the **maximum** possible bitwise XOR of all elements of* `nums`
*after applying the operation **any number** of times*.

```
nums = [3,2,4,6]    ->  7
nums = [1,2,3,9,2]  ->  11
```

**Constraints:** `1 <= nums.length <= 10^5`; `0 <= nums[i] <= 10^8`.

`nums[i] AND (nums[i] XOR x)` is `nums[i]` with the bits of `x` that it
holds cleared, so an operation can clear any of a number's bits and
can set none. A bit no number holds can never reach the XOR, and a bit
some number holds can: clear it from every holder but one. So the most
is the OR of all the numbers, and every bit is settled on its own.
O(n).

## Approaches

| file | mechanism |
|---|---|
| `xor.kara` ★ | one walk ORing every number into `all` |
| `xor_naive.kara` | each of the 27 bits a number up to `10^8` can hold, the whole array scanned for a holder. O(27 n) |
| `xor_ops.kara` | the operations done: for each bit held an even number of times, the last holder given `nums[i] & (nums[i] ^ x)` with `x` that bit, then the numbers XORed |
| `xor_count.kara` | a `[0; 27]` table of how many numbers hold each bit, filled by shifting each number down, and the bits counted at all |
| `xor_iter.kara` | `nums.iter().fold(0, \|all, x\| all \| x)` |
| `xor_solution.kara` | LeetCode's Rust template: `i32` numbers and `into_iter().fold(0, \|a, b\| a \| b)`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; a single
zero; a single number; two equal numbers, whose XOR is 0 untouched; the
largest number beside a power of two it holds and one it does not;
`10^5` numbers up to `10^8`, each under a random mask; then 1000 random
arrays of 1 to 30 numbers below `2^1` to `2^27`, with a checksum and
the bits set in all. `xor.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one call, reporting 9 edits.
`check` first reports five errors and offers 7 edits for them:
`struct Solution;` to `struct Solution {}`; the four brackets of the
two `Vec<i32>`; the `&` of the closure's pattern `|&x|` dropped; and
`Solution::maximum_xor` to `Solution.maximum_xor` in the harness's
wrapper. The other two follow from those: `nums` marked `own`, since
`into_iter()` consumes it and a bare parameter only borrows; and the
wrapper's `as i64` on the `i32` answer dropped, as it widens on its own.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each number in turn is given `nums[i] & (nums[i] ^ x)` for
every `x` below the next power of two past the largest number, `x = 0`
leaving it as it is, and a table of the XORs reachable so far is
carried from number to number; the largest XOR in the table is the
answer. No OR and no bits taken apart. It checks 300 random arrays of 1
to 6 numbers below `2^1` to `2^4`; then 30 of one number below 64
repeated, whose XOR untouched is 0 or the number; then 30 of 1 to 6
numbers below 64. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer is at least every number and the XOR of them all, both reachable with no operation or with all but one number cleared |
| P3 | the numbers reversed: the same answer |
| P4 | every number twice: the same answer |
| P5 | `2^26` added to the numbers, a bit none of them holds: `2^26` more |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 45345864, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
builds the same cases and carries the set of reachable XORs through
each number's submasks. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: the OR begun at 1 | P1 66, P6 66 |
| M4 | ★: the first number left out | P1 118, P2 102, P3 107, P4 118, P6 118 |
| M6 | ★: each number's lowest bit dropped | P1 339, P2 294, P5 360, P6 339 |
| M7 | naive: the bits up to `2^25` only | P5 360 |
| M8 | naive: the bits no number holds | P1 360, P5 360, P6 360 |
| M10 | naive: each bit's place added, not its value | P1 339, P2 339, P5 360, P6 339 |
| M13 | ops: the holder left with that bit alone | P1 196, P2 183, P3 125, P4 276, P6 196 |
| M14 | ops: bit 0 never looked at | P1 98, P2 69, P4 196, P6 98 |
| M15 | ops: the last number alone kept | P1 245, P2 245, P3 165, P4 203, P5 203, P6 245 |
| M17 | count: every place below the top counted | P1 80, P5 360, P6 80 |
| M18 | count: the number shifted two places a step | P1 264, P2 264, P5 360, P6 264 |
| M20 | count: each bit set one place up | P1 339, P5 360, P6 339 |
| M22 | iter: the numbers summed | P1 242, P4 339, P6 242 |
| M23 | iter: the first number alone | P1 184, P2 163, P3 218, P5 360, P6 184 |
| M24 | iter: the last number left out | P1 119, P2 100, P3 107, P4 119, P5 360, P6 119 |
| M27 | solution: the numbers XORed | P1 196, P2 175, P4 279, P6 196 |
| M31 | solution: the largest number | P1 101, P2 33, P5 339, P6 101 |

P1 and P6 kill sixteen, P2 and P5 eleven each, P4 seven and P3 five.
The naive arm's bits up to `2^25` (M7) is killed by P5 alone: no case
holds a number past 63 until P5 adds `2^26`, the one bit the edit never
looks at. P5 fails wherever a number's high bit is lost or moved: the
lowest bit dropped, the places shifted, the first or the last number
alone or left out. P4, every number twice, fails where the duplicates
count, as in a XOR or a sum, and where a number is left out or kept
alone; P3, the numbers reversed, only where the first or the last
number is special. P2 fails for an answer below some number or below
the plain XOR.

Of the thirty-one, fourteen were not kept. The numbers XORed in the ★
arm (M1), a bit held an odd number of times in the naive (M9) and count
(M19) arms, and the iter arm's XOR (M26) fail as the template's (M27);
the ★ arm's AND (M2), the ops arm's bit cleared when held an odd
number of times (M12), the count arm's top bit never counted (M21), the
iter arm's numbers halved (M25) and the template's AND (M29) fail as
the naive arm's place added (M10), every one of them low on nearly
every case and missing `2^26`; the ★ arm's
largest number (M5) fails as the template's (M31); the naive arm's bits
some number lacks (M11) as its bits no number holds (M8); the
template's OR begun at 1 (M28) and lowest bit always set (M30) as the ★
arm's OR begun at 1 (M3). The ops arm's lower bits cleared, not the bit
(M16), fails apart from every kept one, and was left out to keep three
to an arm.

M30 replaces the template's first number left out,
`nums.into_iter().skip(1).fold(0, |a, b| a | b)`, which `karac check`
refuses: after `skip`, and after `take`, `filter` or `map` as well, the
`0` that starts the fold is typed `i64` and the `i32` the method returns
reads as a narrowing, while the same fold straight on `into_iter()`, or
on a `let` holding the adapter, types as `i32`. That gap is B-2026-11-18-90 in
kara's ledger.

## Verification

Every arm prints the same output as `xor.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★ and iter arms take 0.3 s, the template
0.6 s, the ops and naive arms, which walk the array once for each of
27 bits, 0.8 and 1.0 s, and the count arm, shifting every number down
bit by bit, 1.3 s, most of it the `10^5` numbers. The differential takes
0.4 s there and under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 20 arrays of `10^5` numbers once, array `a` holding
random numbers up to `10^8` under a mask of `a + 4` random bits, then
makes 100 passes, pass `p` taking array `(a + p) % 20` at step `a`,
with the ★ arm in all five languages. Every implementation prints `100
passes over 20 arrays of 10^5 numbers: checksum 601437598`. Each ORs
64-bit integers in one loop, which C, Rust and Kāra's LLVM build may
vectorize; the 2 million random numbers drawn first are a large share
of the run.

BENCHTAB
