# 2481. Minimum Cuts to Divide a Circle

A **valid cut** in a circle can be:

- A cut that is represented by a straight line that touches two points
  on the edge of the circle and passes through its center, or
- A cut that is represented by a straight line that touches one point
  on the edge of the circle and its center.

Given the integer `n`, return *the **minimum** number of cuts needed to
divide a circle into* `n` *equal slices*.

```
n = 4  ->  2
n = 3  ->  3
```

**Constraints:** `1 <= n <= 100`.

`n` equal slices, for `n` of 2 or more, are bounded by `n` radii,
equally spaced. A cut of the first kind draws two radii half a turn
apart, and both are among them exactly when half a turn is a whole
number of slices, that is when `n` is even; a cut of the second kind
draws one. So an even `n` takes `n / 2` cuts and an odd one `n`. One
slice is the whole circle and takes none: a single radius would leave
it whole.

## Approaches

| file | mechanism |
|---|---|
| `cuts.kara` ★ | by parity: `0` for one slice, `n / 2` for an even count, `n` for an odd one, as an `if` chain. O(1) |
| `cuts_pair.kara` | by pairing radii: each radius not yet drawn takes a cut, which runs on through the centre to draw the radius at `k + n / 2` too when `n` is even, marked in a `Vec[bool]`. O(n) |
| `cuts_angles.kara` | by angles: the radii's angles in degrees as `f64`, and a radius whose angle less 180 is among them, within `10^-9`, the far end of a cut already drawn. O(n^2) |
| `cuts_gcd.kara` | by a common divisor: each cut draws `gcd(n, 2)` radii, so `n / gcd(n, 2)` cuts, the divisor by Euclid's algorithm. O(1) |
| `cuts_iter.kara` | iterators: `filter` over the radii keeping those whose cut is not the far end of an earlier one's, and `count`. O(n) |
| `cuts_solution.kara` | LeetCode's Rust template: `i32` in and out, the three cases as a `match` with a guard on the even counts; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; then four
more, one slice, two, and the constraints' largest odd and even
counts, 99 and 100; then every count from 1 to 100, the constraints'
whole range, as a list; and 3000 random counts from 1 to 100, as a
checksum. `cuts.py` mirrors the ★ arm and its output is byte-identical,
and the mirror was checked for every count from 1 to 9 against a
brute force that tries every set of cuts, each a radius or a line
through the centre at any of `2 n` angles half a slice apart, smallest
sets first, until the radii drawn are `n` equally spaced ones, or for
one slice at most one. The two agreed on every count.

`check` first reports 1 error on the template, `struct Solution;`, and
`karac fix` carries it in one call, reporting 2 edits: `struct
Solution {}` given its braces; and the wrapper's `as i64` on the `i32`
answer goes, since an `i32` widens by itself. The `match` with its
guard, the rebinding `n` patterns and the `i32`s stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally, in whole steps of half a slice: the slices are equal exactly
when the cuts draw the `n` radii at the even steps of a circle of
`2 n`, and a line through the centre draws two radii `n` steps apart,
both of which must be among them. So every radius takes a cut, less one
for each pair the radii make, found by searching the radii for each
one's opposite; one slice takes none. No parity is read. It checks every
count from 1 to 100, then 260 random ones, all drawn before any arm
answers.

| | property |
|---|---|
| P1 | the cuts are the literal reading's |
| P2 | twice as many slices: `n` cuts |
| P3 | two slices or more: between `n / 2` and `n` cuts |
| P4 | two slices or more: four times as many slices need twice the cuts of twice as many |
| P5 | two slices or more: twice as many slices need as many cuts again for an odd count, twice as many for an even one |
| P6 | each arm agrees with at least three of the other five |

P2 holds because `2 n` radii pair off into `n` lines. P3 holds because a
cut draws at most two radii and at least one. P4 holds because `2 n`
and `4 n` are both even, so their cuts are `n` and `2 n`. P5 holds
because an odd `n` takes `n` cuts and so does `2 n`, and an even `n`
takes `n / 2`. P2, P4 and P5 ask the arms for counts up to 400, past
the constraints' 100; every arm reads any count the same way.

The differential prints `360 cases: checksum 522237873, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and searches a set of the radii. On a failure it prints
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
| M1 | ★: one slice one cut | P1 2, P6 2 |
| M4 | ★: two slices no cut | P1 2, P2 2, P3 2, P5 2, P6 2 |
| M5 | ★: only a multiple of four paired | P1 82, P2 183, P4 181, P5 263, P6 82 |
| M7 | pair: the radius past the opposite drawn | P1 177, P2 360, P4 358, P5 358, P6 177 |
| M10 | pair: radius 0 never cut | P1 181, P5 181, P6 181 |
| M11 | pair: every cut counted twice | P1 358, P2 360, P3 181, P6 358 |
| M12 | angles: a quarter turn taken for a half | P1 177, P2 360, P3 95, P4 181, P5 263, P6 177 |
| M13 | angles: a tolerance wider than a slice | P1 19, P2 36, P3 19, P4 167, P5 36, P6 19 |
| M15 | angles: angles a slice too narrow | P1 358, P2 360, P5 181, P6 358 |
| M17 | gcd: the divisor of four | P1 95, P2 177, P3 95, P4 181, P5 82, P6 95 |
| M18 | gcd: the remainder taken the wrong way round | P1 181, P3 181, P5 181, P6 181 |
| M20 | gcd: two slices taken as one | P1 4, P2 2, P3 2, P5 2, P6 4 |
| M22 | iter: both tests needed | P1 358, P2 360, P3 358, P5 181, P6 358 |
| M24 | iter: radius 0 left out | P1 358, P2 360, P3 177, P4 358, P5 177, P6 358 |
| M26 | iter: odd read as one more than a multiple of three | P1 176, P2 106, P3 118, P4 227, P5 227, P6 176 |
| M28 | solution: an even count not halved | P1 177, P2 360, P5 181, P6 177 |
| M30 | solution: two slices taken as odd | P1 2, P2 2, P5 2, P6 2 |

P1 and P6 kill all seventeen, P5 fifteen, P2 fourteen, P3 ten, and P4
seven.

Fourteen are not kept, and every one fails exactly as a kept one: the
answer is one number from a few cases, so most wrong edits are wrong
on the same counts. Six are wrong on every odd count of 3 or more and
right on the rest, each with an answer outside P3's bounds: the ★
arm's odd count halved, the angles arm's only the far ends cut, the gcd
arm's radius too many and the template's odd count halved and a cut
over (M6, M14, M21, M29, M31) as the gcd arm's remainder taken the
wrong way round (M18); the ★ arm's odd count a cut short (M3) is wrong
on the same counts but within the bounds, `n - 1`, as the pair arm's
radius 0 never cut (M10) is. Two give `n`
for every even count: the pair arm's drawn radius cut again and the gcd
arm's divisor always 1 (M9, M19) as the template's even count not
halved (M28). The ★ arm's cut too many for an even count and the iter
arm's half turn itself kept (M2, M23), each `n / 2 + 1` for an even
count, fail as the pair arm's radius past the opposite drawn (M7); the pair arm's opposite
drawn for odd counts (M8) fails as the angles arm's angles a slice too
narrow (M15); the angles arm's first radius never cut (M16) as the
iter arm's radius 0 left out (M24); and the iter arm's and the
template's one slice one cut (M25, M27) as the ★ arm's (M1). No edit
crashes, and every edit is killed by some check.

The one-slice edits are killed only by P1 and P6, on the two cases with
`n` of 1, and those of two slices by a handful: the cases hold every
count once and 260 more at random, so each small count is met two to
four times.

## Verification

Every arm prints the same output as `cuts.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.2 s, the angles arm 8.9 s, and the differential 19.9 s; under `karac __mir-llvm-asan` the arms take 0.3 to 0.4 s, the angles arm 1.5 s, and the differential 2.7 s, and under `karac run` the differential takes 0.5 s.

## Benchmarks

The bench makes 500000 passes over every count from 1 to 100, each
pass starting at a count chosen by the checksum so far, so no pass
repeats the last, folding each answer plus the pass into the checksum.
The bench uses the ★ arm in all five languages. The work per answer is
a comparison and a division or two, so the bench measures the call and
the checksum's arithmetic as much as the answer. Every implementation
prints `500000 passes over every count from 1 to 100: checksum
584720353`.

BENCHTAB
