# 2103. Rings and Rods

There are `n` rings and each ring is either red, green, or blue. The
rings are distributed across ten rods labeled from `0` to `9`.

You are given a string `rings` of length `2n` that describes the `n`
rings that are placed onto the rods. Every two characters in `rings`
form a color-position pair that is used to describe each ring, where:

- The first character of the `i`th pair denotes the `i`th ring's color
  (`'R'`, `'G'`, `'B'`).
- The second character of the `i`th pair denotes the rod that the `i`th
  ring is placed on (`'0'` to `'9'`).

For example, `"R3G2B1"` describes `n == 3` rings: a red ring placed onto
the rod labeled 3, a green ring placed onto the rod labeled 2, and a blue
ring placed onto the rod labeled 1.

Return the number of rods that have all three colors of rings on them.

```
rings = "B0B6G0R6R0R6G9"   ->  1
rings = "B0R0G0R9R0B0G0"   ->  1
rings = "G4"               ->  0
```

**Constraints:** `rings.length == 2 * n`; `1 <= n <= 100`; `rings[i]`
where `i` is even is `'R'`, `'G'`, or `'B'`; `rings[i]` where `i` is odd
is a digit from `'0'` to `'9'`.

A rod's state is which of the three colors it has seen, so three bits
per rod, and the answer is how many of the ten rods have all three set.
How many rings of a color a rod holds, and in what order they came, do
not matter.

## Approaches

| file | mechanism |
|---|---|
| `rings.kara` ★ | an array of ten masks, red 1, green 2 and blue 4, filled by a `while` loop over the string's `bytes()` two at a time with a `match` on the color; the masks equal to 7 counted with `filter` and `count`. O(n) |
| `rings_sets.kara` | a `Vec[Set[char]]` of each rod's colors, fed by `zip` of the string's `chars()` at the even positions (`step_by(2)`) and the odd ones (`skip(1).step_by(2)`), the rod from `to_digit(10)`; the sets of size 3 counted |
| `rings_search.kara` | no state at all: for each rod `d`, whether each of `R`, `G` and `B` appears as some two-byte chunk of color then `d`, asked with `chunks(2)`, `all` and `any`. O(30 n) |
| `rings_struct.kara` | a `struct Rod` of three `bool` flags with a `put` method taking the color's letter (`mut ref self`) and a `full` method; the ten rods a `Vec[Rod]` |
| `rings_counts.kara` | a ten-by-three `Vec[Vec[i64]]` of counts, built by `fold` over the pairs, each color's column found with `position` in `"RGB"`; the rows with no zero counted |
| `rings_solution.kara` | LeetCode's Rust template (`rings: String`, a `[0u8; 10]` of masks from `as_bytes().chunks(2)`, the full ones counted with `filter(\|&&m\| m == 7)`), carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples and four
more (every rod holding all three; one color many times on one rod; two
colors only on two rods; and the longest a string may be, 100 rings that
never put a second color on a rod), each string with its answer; then
the total of the answers for 3000 random strings of 1 to 100 rings, on
rods 0 to 9 or on rods 0 to 2 so that rods fill up, and a checksum of
them. `rings.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a rod holds all three colors when the string contains `R`,
`G` and `B` each followed by that rod's digit. It checks 300 random
strings of 1 to 100 rings on rods 0 to 9; then 20 on rods 0 to 2 only,
so that rods fill up; then 20 that put all three colors on every one of
a random set of rods, in shuffled order, with up to three stray rings
between. All 340 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is 0 to 10, no more than a third of the rings, and no more than the rods that have any ring |
| P3 | the rings listed in reverse: the same answer |
| P4 | every rod's digit `d` made `9 - d`: the same answer |
| P5 | one more random ring added at the end: an answer no smaller, and at most one larger |
| P6 | each arm agrees with at least three of the other five |

The reversed and mirrored strings stay within the constraints; the one
with a ring added may be 101 rings long, one past them, which no arm
depends on. The differential prints `340 strings: checksum 180626989,
12240 checks over 6 arms: 0 failures` under every lane in Verification;
the checksum of the literal answers was checked against a Python reading
of the same strings that tests membership in the list of pairs. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, four to seven to each arm, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: green taken for blue | P1 295, P6 295 |
| M4 | ★: the first ring skipped | P1 44, P3 54, P6 44 |
| M5 | ★: every other ring skipped | P1 279, P3 89, P6 279 |
| M6 | sets: a rod with two colors counted | P1 270, P2 2, P6 270 |
| M7 | sets: each color put on the next ring's rod | P1 219, P3 202, P6 219 |
| M8 | sets: each rod given the next ring's color | P1 200, P3 202, P6 200 |
| M9 | search: any one color enough | P1 299, P2 93, P6 299 |
| M10 | search: a color anywhere or the rod anywhere | P1 324, P2 139, P5 3, P6 324 |
| M11 | search: rod 9 never asked about | P1 149, P4 132, P6 149 |
| M15 | struct: a rod full without blue | P1 182, P6 182 |
| M17 | struct: rod 9 merged into rod 0 | P1 118, P6 118 |
| M18 | struct: a second red ring taking red off | P1 230, P5 40, P6 230 |
| M19 | counts: an even count read as none | P1 272, P5 30, P6 272 |
| M20 | counts: two of each color wanted | P1 278, P6 278 |
| M23 | counts: rods 5 to 9 merged into 0 to 4 | P1 248, P6 248 |
| M25 | solution: red and blue enough | P1 180, P6 180 |
| M27 | solution: the adapter adding a red ring on rod 0 | P1 32, P4 62, P6 32 |

P1 and P6 kill all seventeen, P3 four, P2 three, P5 three and P4 two.
P3 sees the edits that read the string out of step: a ring skipped at
the start (M4) or every other one (M5), and a color paired with the
next ring's rod (M7, M8). P2 sees the edits that count a rod with
fewer than three colors, so that a rod with one or two rings can count
(M6, M9, M10). P4 sees the edits that treat one rod differently from
its mirror: rod 9 never asked about (M11) and the adapter's added ring
always on rod 0 (M27). P5 sees the edits under which a ring can take a
color off a rod (M18, M19), and the search for any color or any rod
(M10), under which one ring can fill several rods.

Of the thirty, thirteen were not kept, and none survives. Seven leave
no rod ever full and fail the same 295 strings, those whose answer is
not 0: green taken for blue in the ★, struct and counts arms
(M1, M14, M22), red worth green's bit in the Rust arm (M24), the ★ arm
keeping only a rod's last color (M3) or reading the color from the
rod's digit (M29), and the search arm comparing the digit with the
color (M30); M1 is kept for them. Four more fail as a kept one: the ★
arm's two colors counted as M6; the struct arm's last ring dropped and
the counts arm's first ring skipped as M4; the search arm's blue never
asked for as M15; and the Rust arm's second ring of a color taking it
off (`^=`) as M19. Two are killed with checks of their own but were
left out because their arm keeps its share: the search arm asking each
rod about the next (P1 169, P4 132), and the Rust arm's ten full rods
read as none (P1 16), which only the 16 strings filling every rod see.

## Verification

Every arm prints the same output as `rings.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.8 s to 2.2 s, and the
differential 3.2 s (timed while other work shared the machine).

`karac fix` carries the template in two rounds of 4 and 3 edits: Rust's
spellings (the `&&m` closure pattern dropped, `struct Solution;` to
`struct Solution {}`, the adapter's `&str` to `Str` and `Solution::` to
`.`); then `as_bytes()` to `bytes()`, the adapter's `as i64` dropped as
a cast `i32` widens without, and `bit` given `: u8`.

That last edit is the one this kata turned up. Rust infers `bit`'s
type from the `|=` into a `u8` array. Kāra typed a `let` bound to a
`match` of bare literals at the default `i64` at once, before any later
use could fix it, and the refusal of the narrowing `|=` named no reason
and offered no edit. Since kara B-2026-11-10-49 a join of literals is
a literal that stays open until a use fixes it (design.md §8). An
operator's operand does not fix it, so the `|=` still keeps `bit` an
`i64`, and the refusal now says why and offers `bit: u8`, the edit
above; the §8 ruling of 2026-11-10 says a compound assignment into a
target of a fixed type will fix it, at which point the template needs
one edit less. Test `tests/kata_2103_literal_match_binding_fix.rs`
(kara 81aca4606b) runs the Mend loop on the kata's pattern either way.

## Benchmarks

The bench builds 4096 strings of 100 rings once, half on rods 0 to 9 and
half on rods 0 to 2, then counts 300000 of them, string `k * 7919 mod
4096` at step `k`, with the ★ arm in all five languages: an array of ten
masks filled from the bytes two at a time and the masks equal to 7
counted. Every implementation prints `300000 counts: 1805629 rods with
all three, checksum 160413903`.

BENCHTAB
