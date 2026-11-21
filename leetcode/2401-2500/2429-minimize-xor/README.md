# 2429. Minimize XOR

Given two positive integers `num1` and `num2`, find the positive integer
`x` such that:

- `x` has the same number of set bits as `num2`, and
- the value `x XOR num1` is **minimal**.

Note that `XOR` is the bitwise XOR operation.

Return *the integer* `x`. The test cases are generated such that `x` is
**uniquely determined**.

The number of **set bits** of an integer is the number of `1`'s in its
binary representation.

```
num1 = 3, num2 = 5   ->  3
num1 = 1, num2 = 12  ->  3
```

**Constraints:** `1 <= num1, num2 <= 10^9`.

A bit where `x` and `num1` differ costs its place value, and one high
bit outweighs every bit below it. So `x` should agree with `num1` on as
many of the highest bits as it can: it takes `num1`'s set bits from the
top, one for each set bit of `num2`, and if any are left over they go in
`num1`'s clear bits from the bottom, where they cost least. The answer
is unique because XOR with `num1` is one-to-one.

## Approaches

| file | mechanism |
|---|---|
| `xor.kara` ★ | `num2.count_ones()` bits to place: `num1`'s set bits taken from bit 30 down while any are left, then the clear bits of `x` filled from bit 0 up. O(31) |
| `xor_adjust.kara` | `num1` adjusted in place: while it has too many set bits its lowest is cleared by `x & (x - 1)`, and while too few its lowest clear bit is set by `x \| (x + 1)`, each the cheapest change left. O(31) |
| `xor_feasible.kara` | bit by bit from the top, each bit of `x` matched to `num1`'s whenever the bits still to place fit in the bits below, and set the other way otherwise. O(31) |
| `xor_bits.kara` | the bits as a `Vec[bool]` of 31, lowest first, made by `map` and `collect`: `num1`'s set bits kept from the top while the count allows, the rest in the lowest clear places, and the vector read back into a number. O(31) |
| `xor_iter.kara` | iterators: `num1`'s set bits from the top by `rev`, `filter` and `take`, folded into `x`, then as many of `x`'s clear bits from the bottom as are still wanted, folded in the same way. O(31) |
| `xor_solution.kara` | LeetCode's Rust template: the count by `num2.count_ones()`, a `u32` in Rust, and two passes over the bits with `&&` and `1 << i`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples; 1 and 1;
the constraints' largest, `10^9` twice; 1 against 29 set bits, the most
a value up to `10^9` holds; `2^29` against 29 set bits; `10^9` and
`2^29 - 1` against one set bit; then 3000 random pairs from 1 to `10^9`
and 3000 from 1 to 63, each as a checksum. `xor.py` mirrors the ★ arm
and its output is byte-identical, and the mirror was checked on every
pair from 1 to 255 against every `x` below 512 with the right count.

`check` first reports 3 errors on the template, and `karac fix` carries
it in one call, reporting 3 edits: each `&&` written `and`, and `struct
Solution;` given its braces. `count_ones()` stands as Kāra, where it
returns an `i64` rather than Rust's `u32`, so `k > 0` and `k -= 1` need
nothing; so do `1 << i`, `x |= ..` and the shifts and masks.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the value of `x XOR num1` tried from 0 upward, `x` being
`num1` XOR it, until `x` has as many set bits as `num2`, counted by
halving; the first such `x` is the answer. No bit is placed by hand. It
checks 300 random pairs from 1 to 1023; then 30 with `num1` from 1 to
`10^9` and `num2` a run of low set bits whose count is within three of
`num1`'s, so the search stays short; then 30 random pairs from 1 to
`2^16`. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | `num2` replaced by the run of its count of low set bits: the same answer |
| P3 | the answer has as many set bits as `num2` |
| P4 | `num1` against itself: `num1` |
| P5 | the answer XOR `num1` is no larger than `num2` XOR `num1` |
| P6 | each arm agrees with at least three of the other five |

P2 holds because only `num2`'s count of set bits matters. P4 holds
because `num1` itself has the count and XORs to 0, and P5 because `num2`
is one of the values with the count, so the least XOR is no larger than
its.

The differential prints `360 cases: checksum 350828650, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and runs the same search. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: bits 29 and 30 never matched | P1 11, P4 11, P6 11 |
| M2 | ★: the last bit kept for the bottom | P1 187, P4 165, P5 1, P6 187 |
| M3 | ★: bit 0 never filled | P1 84, P5 1, P6 84 |
| M7 | adjust: a bit shifted off the bottom instead | P1 159, P5 94, P6 159 |
| M9 | adjust: one bit cleared at most | P1 87, P3 87, P6 87 |
| M11 | adjust: one bit short | P1 142, P3 142, P6 142 |
| M13 | feasible: every set bit matched | P1 159, P3 159, P6 159 |
| M14 | feasible: num2's bits matched | P1 359, P2 329, P6 359 |
| M15 | feasible: each bit spent twice | P1 359, P3 359, P4 355, P5 11, P6 359 |
| M19 | bits: the bits read one place up | P1 354, P2 172, P3 188, P4 360, P5 177, P6 354 |
| M20 | bits: the fill from the top | P1 142, P5 142, P6 142 |
| M21 | bits: num1 returned | P1 301, P3 301, P6 301 |
| M23 | iter: num1's set bits from the bottom | P1 159, P5 65, P6 159 |
| M24 | iter: the fill without the top bits | P1 360, P3 360, P4 360, P5 171, P6 360 |
| M26 | iter: the lowest clear bit skipped | P1 142, P5 1, P6 142 |
| M28 | solution: bits 0 and 1 never filled | P1 118, P5 4, P6 118 |
| M31 | solution: the two swapped | P1 360, P2 316, P3 301, P5 106, P6 360 |


P1 and P6 kill all seventeen, P5 eleven, P3 eight, P4 five and P2
three.

Fourteen are not kept. Seven fail exactly as a kept one: the ★ arm's
`num1`'s own count (M5) as the bits arm's `num1` returned (M21); the
adjust arm's `num2` adjusted (M10) as the feasible arm's `num2`'s bits
matched (M14), both answering `num2` itself; the feasible arm's clear bit set one late and the template's set
bit filled again (M16, M30) as the adjust arm's one bit short (M11); the
bits arm's every set bit kept and the template's every set bit of
`num1` kept (M18, M27) as the feasible arm's every set bit matched
(M13); and the iter arm's one top bit left to the fill (M22) as the ★
arm's last bit kept for the bottom (M2). Six fail apart from every kept
one and were left out because those arms keep their share already: the
★ arm's fill one bit high and count never spent at the top (M4, M6),
the feasible arm's clear bit set one early (M12), the bits arm's bits
read back reversed (M17), the iter arm's whole count filled again
(M25), and the template's one bit too many (M29).

One survives, and is equivalent: the adjust arm's one added instead of
a bit set (M8). Adding 1 sets the lowest clear bit and clears the run
of set bits below it, so the count of set bits rises by at most one at
each step, and the loop stops at the least value above `num1` with the
wanted count, which is `num1` with its lowest clear bits set, the
answer.

## Verification

Every arm prints the same output as `xor.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.2 to 0.8 s, and the
differential 0.5 s; under `karac __mir-llvm-asan` the differential
takes 0.5 s and under `karac run` 0.4 s.

## Benchmarks

The bench builds `10^5` pairs from 1 to `10^9` once from its own
generator, then makes 10 passes, pass `p` XORing every `num2` with
`p + 1` so its count of set bits changes, answering every pair and
folding the answer plus the pass into the checksum. The bench uses the
★ arm, `num1`'s high set bits then the lowest clear ones, in all five
languages. Every implementation prints `10 passes over 10^5 pairs:
checksum 669567329`. The count of set bits is the language's own:
`count_ones()` in Kāra and Rust, `__builtin_popcountll` in C,
`bits.OnesCount64` in Go, and `bin(n).count("1")` in Python.

BENCHTAB
