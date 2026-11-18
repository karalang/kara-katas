# 2275. Largest Combination With Bitwise AND Greater Than Zero

The **bitwise AND** of an array `nums` is the bitwise AND of all
integers in `nums`.

- For example, for `nums = [1, 5, 3]`, the bitwise AND is equal to `1 &
  5 & 3 = 1`.
- Also, for `nums = [7]`, the bitwise AND is `7`.

You are given an array of positive integers `candidates`. Compute the
**bitwise AND** for all possible **combinations** of elements in the
`candidates` array.

Return *the size of the **largest** combination of* `candidates` *with a
bitwise AND **greater** than* `0`.

```
candidates = [16,17,71,62,12,24,14]  ->  4
candidates = [8,8]                   ->  2
```

**Constraints:** `1 <= candidates.length <= 10^5`; `1 <= candidates[i]
<= 10^7`.

An AND is above zero exactly when some bit is set in every value it
takes, so the largest combination is the most values that share one
bit. Every value is below 2^24, so 24 counts settle it. O(24 n).

## Approaches

| file | mechanism |
|---|---|
| `combo.kara` ★ | for each of the 24 bits, the values with `(x >> bit) & 1 == 1` counted; the most kept |
| `combo_tally.kara` | each value shifted down a bit at a time, its low bit added into an `Array[i64, 24]` of counts |
| `combo_lowbit.kara` | the set bits only: each value's lowest by `trailing_zeros`, cleared by `x & (x - 1)`, one step per bit it has |
| `combo_struct.kara` | `struct BitTally` of the 24 counts; `add` (`mut ref self`) takes a value's bits by `x & (1 << bit)` and `largest` reads the most common |
| `combo_iter.kara` | one chain: `(0..24).map` of a `filter` and `count` over the values, then `max` |
| `combo_solution.kara` | LeetCode's Rust template: `Vec<i32>` in, `i32` out; for each bit, `filter(\|&&x\| (x >> b) & 1 == 1).count() as i32`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and five
more (one value, 1; four bits apart, 1; one value thrice, 3; the
largest value, 1; three values sharing bits only in pairs, 2), each with
its size; then 2000 random lists of 1 to 40 values up to 15, 1000 or
10^7, with a checksum; then three of the constraints' largest, 10^5
values: random up to 10^7 (50248), every value from 1 to 10^5 (50000),
and the powers of two below 2^24 in turn (4167). `combo.py` mirrors the
★ arm and its output is byte-identical.

`karac fix` carries the template in one round, reporting 12 edits:
`Vec<i32>` to `Vec[i32]`, the pattern `|&&x|` to `|x|`, `let mut ans:
i32 = 0`, which the `i32` return names, `struct Solution;` to `struct
Solution {}`, and in the adapter `&Vec<i64>` to a bare `Vec[i64]`,
`|&x|` to `|x|`, `Solution::` to `Solution.` and the `as i64` dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every combination, as a mask over the values' places, its
AND taken, and the largest whose AND is above zero. No bits counted. It
checks 300 random lists of 1 to 10 values up to 3, 15, 255 or 10^6;
then 30 of one value repeated; then 30 of distinct powers of two. All
360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the size is the literal reading's |
| P2 | the list reversed: the same size |
| P3 | every value doubled, its bits one place up: the same size |
| P4 | at least 1 and at most the number of values, and all of them when the AND of the whole list is above zero |
| P5 | the list twice over: twice the size |
| P6 | each arm agrees with at least three of the other five |

The differential's values stay below 2^20, so doubling them keeps every
bit below 2^24, where the arms look.

The differential prints `360 cases: checksum 615904773, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that ANDs
every `itertools.combinations` of the values by `reduce`. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: each value counted twice | P1 360, P4 330, P6 360 |
| M5 | ★: the highest bit present kept | P1 181, P4 60, P6 181 |
| M6 | ★: bit 0 never counted | P1 43, P3 43, P4 15, P6 43 |
| M8 | tally: the bit never moved | P1 344, P4 314, P6 344 |
| M9 | tally: two bits shifted at a time | P1 103, P3 188, P4 42, P6 103 |
| M10 | tally: the least kept | P1 360, P4 360, P6 360 |
| M12 | lowbit: bits counted in pairs | P1 322, P3 234, P4 273, P6 322 |
| M13 | lowbit: only the lowest bit counted | P1 168, P4 54, P6 168 |
| M16 | lowbit: each run of bits cleared from its top | P1 251, P4 181, P6 251 |
| M18 | struct: presence for count | P1 286, P4 102, P5 360, P6 286 |
| M19 | struct: the test inverted | P1 211, P6 211 |
| M20 | struct: the first value never added | P1 250, P2 92, P4 149, P5 250, P6 250 |
| M22 | iter: only the low 8 bits | P1 31, P3 8, P4 12, P6 31 |
| M23 | iter: a value of 1 never counted | P1 36, P3 36, P4 13, P6 36 |
| M25 | iter: the shift the wrong way | P1 233, P3 295, P4 115, P6 233 |
| M30 | solution: two bits tested at once | P1 198, P6 198 |
| M31 | solution: the count rounded down to even | P1 217, P4 116, P5 217, P6 217 |

P1 and P6 kill all seventeen, P4 fifteen, P3 six, P5 three, and P2 one.
P4 misses only the two edits that count values a combination cannot
hold together yet stay within the list's length: the bit test inverted
and two bits tested at once. P3 catches every edit that treats bits by
their place, low bits dropped, bit 0 skipped, bits paired or shifted
the wrong way, since doubling moves each bit up one. P5 sees only a
count that does not double with the list: presence, a value left out,
and rounding. Every arm reads the values as a multiset, so reversing
the list moves only the edit that skips the first value.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Thirteen fail as a kept one does: the ★ arm's low
8 bits (M1) as the iter arm's (M22); the ★ arm's count never reset (M2)
as the tally arm's bit never moved (M8); the ★, tally and template
arms' values without the bit counted (M3, M7, M29) as the struct arm's
test inverted (M19); the tally arm's bit 0 dropped and the struct
arm's bit 0 never tested (M11, M17) as the ★ arm's bit 0 never counted
(M6); the lowbit arm's last bit 0 never counted (M14) as the iter arm's
value of 1 (M23); the lowbit arm's presence for count (M15) as the
struct arm's (M18); the struct arm's bit 0's count only (M21) as the
iter arm's shift the wrong way (M25); the iter arm's least kept and the
template's last bit kept (M24, M28) as the tally arm's least kept
(M10); and the iter arm's first value skipped (M26) as the struct
arm's first value never added (M20). One fails in a way of its own and
is left out because its arm keeps enough: the template's low 16 bits
(M27), wrong in only 6 cases, those where a bit at 2^16 or above is
shared by more values than any lower one.

One edit of the first draft was replaced because it failed as another
did: the iter arm's values without the bit counted, as the struct
arm's M19. It is now M23.

## Verification

Every arm prints the same output as `combo.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the differential takes 1.1 s, the ★ arm 1.4 s,
the lowbit arm 1.7 s, the struct and tally arms 2.4 s and 2.5 s, the
iter arm 4.9 s, and the template 5.3 s.

## Benchmarks

The bench answers 100 lists of the constraints' largest, 10^5 values
from 1 to 10^7, with the ★ arm in all five languages. Every
implementation prints `100 lists of 10^5: checksum 470713377`. Each
builds its list a value at a time from the same generator, two draws to
a value.

BENCHTAB
