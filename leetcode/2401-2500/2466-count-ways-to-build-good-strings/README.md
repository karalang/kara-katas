# 2466. Count Ways To Build Good Strings

Given the integers `zero`, `one`, `low`, and `high`, we can construct a
string by starting with an empty string, and then at each step perform
either of the following:

- Append the character `'0'` `zero` times.
- Append the character `'1'` `one` times.

This can be performed any number of times.

A **good** string is a string constructed by the above process having a
**length** between `low` and `high` (**inclusive**).

Return *the number of **different** good strings that can be
constructed satisfying these properties*. Since the answer can be
large, return it **modulo** `10^9 + 7`.

```
low = 3, high = 3, zero = 1, one = 1  ->  8
low = 2, high = 3, zero = 1, one = 2  ->  5
```

**Constraints:** `1 <= low <= high <= 10^5`; `1 <= zero, one <= low`.

The two blocks are different characters, so a string's blocks can be
read back from it, and counting the strings is counting the sequences of
blocks: the strings of length `len` are those of length `len - zero`
with a block of zeros after them and those of length `len - one` with a
block of ones.

## Approaches

| file | mechanism |
|---|---|
| `good.kara` ★ | bottom-up counts: `ways[len] = ways[len - zero] + ways[len - one]` from `ways[0] = 1`, and the counts from `low` to `high` summed. O(high) |
| `good_memo.kara` | top-down: the number of good strings that extend a prefix of length `len`, one if `len` itself is in range plus those after a block of each kind, each length answered once and kept in a memo. O(high), recursing up to `high` deep |
| `good_blocks.kara` | counting by blocks: `a` zero blocks and `b` one blocks order in `C(a + b, a)` ways; for each `a` the `b` that put the length in range form a run, which the hockey-stick identity sums as `C(a + hi + 1, a + 1) - C(a + lo, a + 1)`, from factorials and their inverses mod p. O(high + high / zero) |
| `good_push.kara` | pushed forward: each length's count added to the two lengths a block longer, held in a ring of `max(zero, one) + 1` slots, each cleared once read. O(high) time, O(zero + one) space |
| `good_iter.kara` | iterators: the counts filled by `for_each`, each the `fold` of the counts one block back that `filter_map` finds over the two block sizes; the counts from `low` on `skip`ped to and summed by `fold`. O(high) |
| `good_solution.kara` | LeetCode's Rust template: the same bottom-up counts in a `vec![0i64; high + 1]`, the bounds cast `as usize`, and the answer returned `as i32`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples; then five
more, one block of each and length one, blocks of two that never reach
an odd length, equal blocks over a range, the largest equal blocks the
constraints allow, and blocks of 3 and 7; then four at the
constraints' largest, every length up to `10^5` with blocks of one,
`10^5` alone, blocks of 1 and `10^5`, and blocks of 3 and 7 from 50000
to `10^5`; and 3000 random cases with `high` up to 300 and each block
no longer than `low`, as a checksum. The memo arm recurses `10^5` deep
on the first of the four, and every lane holds it. `good.py` mirrors
the ★ arm and its output is byte-identical, and the mirror was checked
on all 4200 cases with `high` up to 14 against every string built
explicitly.

`check` first reports 1 error on the template, `struct Solution` not
declared, and `karac fix` carries it in one call, reporting 8 edits:
`struct Solution {}` added; the four `as usize` casts written `as i64`,
since Kāra indexes by `i64`; `vec![0i64; high + 1]` written
`Vec.filled(high + 1, 0)`; and the `i64` suffixes of `0i64` dropped
twice. The inner `const MOD`, `1..=high`, `+=` and `%=` on an element,
and `ans as i32` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: starting from the empty string, every string built by
appending a block of zeros or a block of ones is kept as text in a
`Set` while it is no longer than `high`, and the good ones are counted
by their length. No count stands in for a string. It checks 300 random
cases with `high` up to 12 and blocks no longer than `low`; then 60 with
`high` up to 24 and every block 3 or longer. All 360 are drawn before
any arm answers, each with a random length at which P3 splits it.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the two block sizes swapped: the same answer |
| P3 | the range split at a random length: the two answers sum to it |
| P4 | every bound and block doubled: the same answer |
| P5 | the answer is above 0 exactly when some length in range is a sum of blocks, and below `10^9 + 7` |
| P6 | each arm agrees with at least three of the other five |

P2 holds because swapping the characters' block sizes maps each string
to one of the same length. P3 holds because each good string has one
length, on one side of the split; the second half starts above `low`,
so it keeps the constraints. P4 holds because a string of doubled
blocks is a string of the original blocks with each character written
twice, and its length is twice the original's. P5 holds because a
length that is `a * zero + b * one` has at least the string of `a` zero
blocks then `b` one blocks.

The differential prints `360 cases: checksum 78476424, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and keeps every string in a set. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no empty string to build on | P1 335, P5 335, P6 335 |
| M5 | ★: one block of ones alone never counted | P1 325, P2 192, P5 9, P6 325 |
| M6 | ★: only the last length kept | P1 303, P3 181, P5 57, P6 303 |
| M7 | memo: the length high cut off | P1 278, P3 181, P5 32, P6 278 |
| M8 | memo: the length low itself not good | P1 279, P3 181, P5 39, P6 279 |
| M9 | memo: each length remembered one more | P1 319, P2 125, P3 212, P5 12, P6 319 |
| M12 | blocks: each factorial one factor along | P1 335, P2 225, P3 221, P4 335, P6 335 |
| M13 | blocks: the least count of ones rounded down | P1 205, P2 190, P3 157, P5 25, P6 205 |
| M14 | blocks: the most ones left out of the sum | P1 335, P2 156, P3 172, P5 106, P6 335 |
| M17 | push: each slot never cleared | P1 335, P4 225, P5 17, P6 335 |
| M18 | push: the ring sized by the smaller block | P1 146, P4 238, P5 10, P6 146 |
| M20 | push: the ones push overwriting | P1 226, P2 219, P5 3, P6 226 |
| M22 | iter: the counts summed from one before low | P1 277, P3 181, P4 277, P5 19, P6 277 |
| M24 | iter: length one never filled | P1 160, P4 160, P5 65, P6 160 |
| M26 | iter: each count one more | P1 360, P4 330, P5 25, P6 360 |
| M27 | solution: each answer read one length back | P1 300, P4 277, P5 28, P6 300 |
| M31 | solution: one block of zeros alone never counted | P1 326, P2 192, P5 10, P6 326 |

P1 and P6 kill all seventeen, P5 sixteen, P3 eight, and P2 and P4
seven each. The only kept one P5 misses is the blocks arm's factorial
one factor along (M12): its answers are wrong but never 0 where a
length is reachable.

Fourteen are not kept. Seven fail exactly as a kept one: the ★ arm's
length `low` not counted (M2) as the memo arm's (M8); the ★, push and
template arms' length `high` never reached (M4, M19, M29) as the memo
arm's cut off (M7); the memo arm's start from length one and the
template's empty string at length one (M11, M30) as the template's
answer read one length back (M27), each counting the lengths from
`low - 1` to `high - 1`; and the iter arm's block as long as the length
skipped (M23) as the ★ arm's no empty string (M1), each answering 0
everywhere. Five fail apart from every kept one: the memo arm's ones
block a zeros block and the iter arm's both blocks the zeros (M10,
M25), alike, each building every string from two blocks of zeros; the blocks
arm's zeros alone never reaching `high` (M15) and choosing every block
taken as none (M16); and the push arm's zero block one longer (M21).
Two end in an index below 0, the ★ arm's and the template's zero block
read one block back (M3, M28): a length past `zero` but short of `one`
reads the count `one` back. Every edit is killed by some check.

## Verification

Every arm prints the same output as `good.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.1 to 3.1 s, the iter arm 7.0 s, and the differential 1.7 s; under `karac __mir-llvm-asan` the arms take 0.5 to 2.4 s and the differential 1.0 s, and under `karac run` the differential takes 0.7 s.

## Benchmarks

The bench builds 20 cases once from its own generator, `high` from
50000 to `10^5`, `low` from 1 to `high` and blocks of 1 to 20 no longer
than `low`, then makes 28 passes; each sets every case's zero block from
the checksum so far, so no answer carries over, then answers it,
folding the answer plus the pass into the checksum. The bench uses the
★ arm, a fresh vector of counts per answer, in all five languages.
Every implementation prints `28 passes over 20 cases up to 10^5:
checksum 23283353`.

BENCHTAB
