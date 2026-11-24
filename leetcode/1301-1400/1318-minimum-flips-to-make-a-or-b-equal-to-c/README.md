# 1318. Minimum Flips to Make a OR b Equal to c

Given 3 positives numbers `a`, `b` and `c`. Return the minimum flips
required in some bits of `a` and `b` to make ( `a` OR `b` == `c` ).
(bitwise OR operation).

Flip operation consists of change **any** single bit 1 to 0 or change the
bit 0 to 1 in their binary representation.

```
a = 2, b = 6, c = 5  ->  3
a = 4, b = 2, c = 7  ->  1
a = 1, b = 2, c = 3  ->  0
```

**Constraints:** `1 <= a <= 10^9`, `1 <= b <= 10^9`, `1 <= c <= 10^9`.

The arms are `fn min_flips(a: i64, b: i64, c: i64) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `min_flips.kara` ★ | each of the 30 bits a number up to `10^9` can have looked at alone; where c wants a 1 it costs one flip if a and b are both 0, and where c wants a 0 it costs one flip for each of a and b that has a 1. O(bits) |
| `min_flips_count.kara` | the bits where a \| b is wrong are `(a \| b) ^ c`, one flip each, except where c wants a 0 and both a and b have a 1, which costs a second, so those bits, `a & b & wrong`, are counted again. Two `count_ones`. O(1) |
| `min_flips_text.kara` | the three numbers written in binary, 30 digits each with leading 0s, by `f"{a:030b}"`, and the digits read side by side, each place costing as the ★ arm's bit does. O(bits) |
| `min_flips_peel.kara` | recursive: the lowest bit of each number costed by `% 2` and the rest asked of a call on all three halved, until nothing is left. O(bits), as deep as the highest bit |
| `min_flips_solution.kara` | a Rust solution as LeetCode's Rust users write it (`((a \| b) ^ c).count_ones() + (a & b & ((a \| b) ^ c)).count_ones()`, returned `as i32`), carried to Kāra by `karac fix` |
| `min_flips_masks.kara` | a second Rust solution as LeetCode's Rust users write it (`for i in 0..32` with `let mask = 1 << i;`, each bit tested by `a & mask != 0`, and a `match (bit_a, bit_b, bit_c)` on the three), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples; `10^9` and
`10^9 - 1` with c 1, nearly every bit to clear; 1 and 1 with c `10^9`,
every bit of `10^9` to set and both 1s to clear; and all three `10^9`, the constraints' most
(`3 1 0 33 15 0`); then 100000 random triples from 1 to `10^9`, every
other one from 1 to 15 (`100000 random triples: flips total 1060706,
checksum 732272944`). `min_flips.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`.

The Mend loop: the ★, text and peel arms checked clean as first written.
The count arm's `(..).count_ones() + (..).count_ones()` was written
`as i64`, Rust's habit for a count that is a `u32` there; in Kāra a bit
count is already an `i64`, the redundant cast is flagged, and `karac fix`
dropped it (1 fix). Each Rust arm takes one round of 3 fixes by `karac
fix`'s count, from 2 errors: `struct Solution;` to `struct Solution {}`,
`::` to `.`, and the wrapper's `as i64` dropped as a widening. The first
keeps its `as i32`, which narrows the `i64` count to the `i32` LeetCode
returns. Both outputs match on the first run. No gap was met.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every pair a2, b2 with a2 OR b2 equal to c tried, up to the
next power of 2 above all three numbers, since no higher bit can be
wanted, and the least number of bits they differ from a and b in taken.
2000 triples in four kinds, 500 each: numbers 1 to 7; 1 to 31; a and b
equal, with c from 1 to 31; and c a OR b with one or two of its bits
changed, kept at 1 or more. Every triple, shift and bit is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | a and b swapped: the same answer |
| P3 | all three shifted left by 1 to 20 places: the same answer |
| P4 | a bit above all their bits put on all three, which costs nothing: the same answer |
| P5 | one bit of c changed: an answer at most 2 away |
| P6 | the ★ arm's answer |

All 72,000 checks pass on every arm: `2000 triples: checksum 204530180,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Fourteen edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. Two are left out, both on the
first Rust arm: counting a & b & c again in place of the bits both have
where c wants a 0 fails exactly the checks the count arm's `a ^ b ^ c`
fails, since each is wrong just when the bits where all three have a 1
and the bits where only c has a 0 differ in number; and leaving `& b` out
of the second count fails exactly the checks the second Rust arm's M11
fails, since both get wrong only a bit that a alone has where c wants a
0. The twelve kept, two to each arm, are each killed, fail the same way
under both backends and not by a crash, and no two fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the lowest bit never looked at | P1 844, P3 844, P6 4220 |
| M2 | ★: two 1s where c wants a 0 costing one flip | P1 982, P6 4910 |
| M3 | count: the wrong bits taken as a ^ b ^ c | P1 1412, P4 2000, P6 1412 |
| M4 | count: every bit both have counted again | P1 1257, P4 2000, P6 1257 |
| M5 | text: a wanted 1 costing a flip whenever b has a 0 | P1 788, P2 939, P6 788 |
| M6 | text: b's digits read in place of c's | P1 1619, P2 1033, P6 1619 |
| M7 | peel: stopping when a and b run out, whatever c has left | P1 322, P4 322, P6 322 |
| M8 | peel: c shifted two places at each step | P1 1680, P3 1625, P4 1898, P6 1680 |
| M9 | solution: the wrong bits taken as a ^ c | P1 920, P2 1112, P6 920 |
| M10 | solution: the first count taken over a AND b | P1 1097, P6 1097 |
| M11 | masks: a 1 in a alone where c wants a 0 costing nothing | P1 517, P2 763, P6 517 |
| M12 | masks: the mask moved on one bit every two steps | P1 1850, P3 694, P5 501, P6 1850 |

P1 and P6 kill all twelve, P2 and P4 four each, P3 three and P5 one.
Swapping a and b (P2) catches the four edits that treat the two
differently (M5, M6, M9, M11). Shifting all three left (P3) catches the
three whose answer depends on where the bits sit: the lowest bit skipped
(M1), c peeled twice as fast as a and b (M8), and the mask that falls
behind the bit it should test (M12). A bit on all three above the rest
(P4) is one where c wants a 1 and both have it, which costs nothing, so
it catches the edits that charge for such a bit (M3, M4), the peel that
now finds a and b as long as c (M7), and the misaligned peel (M8). One
bit of c changed (P5) moves the right answer by at most 2 and bounds
little: it sees only M12, whose answer can jump further. The edits that
get a cost wrong for both numbers alike and wherever the bit is (M2,
M10) show only against the statement and the ★ arm.

## Benchmarks

The bench builds 1000 triples of numbers from 1 to `10^9`, the
constraints' range, once from its own generator; then makes 3000 passes,
each setting one number of every triple from the checksum so far, so no
answer carries over, and folding every answer plus the pass into the
checksum. Every implementation prints `3000 passes over 1000 triples:
checksum 5765279`.

BENCHTAB
