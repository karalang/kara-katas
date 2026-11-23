# 2525. Categorize Box According to Criteria

Given four integers `length`, `width`, `height`, and `mass`, representing
the dimensions and mass of a box, respectively, return *a string
representing the **category** of the box*.

- The box is `"Bulky"` if:
  - **Any** of the dimensions of the box is greater or equal to `10^4`.
  - Or, the **volume** of the box is greater or equal to `10^9`.
- If the mass of the box is greater or equal to `100`, it is `"Heavy"`.
- If the box is both `"Bulky"` and `"Heavy"`, then its category is
  `"Both"`.
- If the box is neither `"Bulky"` nor `"Heavy"`, then its category is
  `"Neither"`.
- If the box is `"Bulky"` but not `"Heavy"`, then its category is
  `"Bulky"`.
- If the box is `"Heavy"` but not `"Bulky"`, then its category is
  `"Heavy"`.

**Note** that the volume of the box is the product of its length, width
and height.

```
length = 1000, width = 35, height = 700, mass = 300  ->  "Heavy"
length = 200, width = 50, height = 800, mass = 50    ->  "Neither"
```

**Constraints:** `1 <= length, width, height <= 10^5`;
`1 <= mass <= 10^3`.

The volume reaches `10^15` at most, well inside an `i64` and far past an
`i32`. The category is two independent tests, so the approaches differ
in how they form the bulky one and how they turn the pair into a name.

## Approaches

| file | mechanism |
|---|---|
| `box.kara` ★ | two flags, `bulky` and `heavy`, then a `match` on the pair. O(1) |
| `box_table.kara` | the two tests read as the bits of an index, bulky the high one, into a `Vec[Str]` of the four names in order; the side test on the largest side |
| `box_nested.kara` | nested tests with early returns, the volume never formed past `10^9`: below `10^4` a side, `height` is compared with `10^9 / (length * width)` rounded up |
| `box_rec.kara` | a recursion over an `Array[i64, 3]` of the sides carrying the volume so far, bulky at the first side of at least `10^4` or at the end on a volume of at least `10^9`; at most 4 deep |
| `box_iter.kara` | iterators: bulky when `any` side reaches `10^4` or the sides' `product` reaches `10^9`; the name `filter`ed from a table of the four by its two tests |
| `box_solution.kara` | LeetCode's Rust template: `i32` in, `String` out, the volume formed as an `i64` from the sides cast up; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples and eight
more at the edges, among them a side of exactly `10^4`, a volume of
exactly `10^9`, a mass of exactly 100 and the largest box; then `10^5`
random boxes with sides from 1 to `10^5` and `10^5` with sides from 1 to
2000, masses from 1 to 1000, as how many took each name. `box.py`
mirrors the ★ arm and its output is byte-identical, and the mirror was
checked on a grid of 288 boxes at and around each threshold against the
statement's two tests, and the two agreed on every box.

`check` reported one error on each of three Kāra arms as first written.
The table arm bound its names as `let names = ["Neither", .., "Both"]`
and returned `names[bulky * 2 + heavy]` from a `-> Str` function. With
nothing at the `let` asking for views, the literals took `String`, and
`check` first offered a machine fix to `.as_str()` that only led to a
second error, a view of a local that cannot outlive the function
(B-2026-11-23-68). It now says the literals took `String` because nothing at
the `let` asked for views, and asks for `names: Vec[Str]`, which `karac
fix` writes. The iter arm wrote the table in place, `[("Both", true,
true), ..].iter()..`, and returned the name the chain found; `check`
gives the same reason and asks for the list to be bound with its
element type first, with no machine fix, as no binding exists to type.
It was bound by hand as `let table: Vec[(Str, bool, bool)] = [..]`.
The rec arm typed its sides `[i64; 3]`, Rust's array type, and `karac
fix` rewrote it as `Array[i64, 3]`.

`check` first reports 5 errors on the template: the unit struct
`struct Solution;`, the three `||`, and the path call
`Solution::categorize_box`. `karac fix` carries it in one call,
reporting 6 edits: `struct Solution {}`, three `or`, `Solution.`, and
the `as i64` on `height` dropped, since an `i32` widens to `i64` without
a cast. The digit separators in `10_000` and `1_000_000_000` are
accepted as written.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a loop over the three sides for one of at least `10^4`, the
volume formed and compared with `10^9`, the mass compared with 100, and
then the statement's four sentences in its own order. It checks 200
random boxes with sides from 1 to `10^5`; 100 near a threshold with a
mass from 98 to 101, half with one side of 9999 or `10^4` and two of 1
to 100, half with three sides of 999 to 1001, the volume about `10^9`;
and 100 with sides from 1 to 1000 and a mass from 1 to 200. Masses are
otherwise from 1 to 1000. All 400 are drawn before any arm answers, and
85 of them are neither.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is one of the four names, and names heavy exactly when the mass is at least 100 |
| P3 | the sides rotated (`width`, `height`, `length`): the same answer |
| P4 | the mass raised to 1000: the answer names heavy, its bulky half kept |
| P5 | the length raised to `10^5`: the answer names bulky, its heavy half kept |
| P6 | each arm agrees with at least three of the other five |

The differential prints `400 boxes, 85 neither: checksum 750617536, 14400
checks over 6 arms: 0 failures` under every lane in Verification; the
checksum of the literal answers was checked against a Python reading
that builds the same boxes and applies the statement's two tests. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a side past 10^4 needed | P1 9, P3 16, P6 9 |
| M4 | ★: heavy from a mass of 99 | P1 23, P2 23, P6 23 |
| M5 | ★: Bulky and Heavy swapped | P1 114, P2 114, P4 199, P5 199, P6 114 |
| M9 | table: the bits added, not placed | P1 237, P2 237, P4 237, P5 199, P6 237 |
| M10 | table: the height left out of the side | P1 6, P3 15, P6 6 |
| M11 | table: the volume test dropped | P1 15, P6 15 |
| M12 | nested: the ceiling taken as a floor | P1 10, P6 10 |
| M14 | nested: a long side read as heavy | P1 29, P2 29, P5 92, P6 29 |
| M15 | nested: a big volume read as bulky alone | P1 8, P2 8, P4 15, P5 8, P6 8 |
| M17 | rec: the walk stopped a side early | P1 22, P3 17, P6 22 |
| M20 | rec: the volume compared with 10^8 | P1 83, P6 83 |
| M21 | rec: heavy tested before bulky | P1 114, P2 78, P4 199, P5 199, P6 114 |
| M22 | iter: all sides needed long | P1 22, P5 25, P6 22 |
| M24 | iter: the first name whose bulky half matches | P1 121, P2 121, P6 121 |
| M26 | iter: the last two sides only | P1 25, P3 18, P5 188, P6 25 |
| M28 | solution: heavy from a mass of 101 | P1 25, P2 25, P6 25 |
| M31 | solution: mass read as the height | P1 117, P2 117, P3 54, P4 46, P6 117 |

P1 and P6 kill all seventeen, P2 nine, P5 seven, and P3 and P4 five
each.

One of the first thirty-one edits survived, to the ★ arm, and was
replaced twice. Its volume past `10^9` needed, and then its volume
compared with `10^9 - 1`, differ from the arm only on a volume of
exactly `10^9` or `10^9 - 1`, and none of the 400 boxes has one: the
cubes near the threshold have sides of 999 to 1001, and only `1000^3`
reaches `10^9` exactly, which the draw never made. The harness's fixed
box `1000 1000 1000 100` holds that edge, so the first edit changes the
kata's own output. The ★ arm's edit became Both read as Neither (M2).

Fourteen are not kept, and none survives. Eight fail exactly as a kept
one. The ★ arm's height not tested alone (M3) fails as the table arm's
height left out of the side (M10); the ★ arm's volume of length and
width alone, the rec arm's volume begun at 0, the iter arm's sum for
the product and the template's volume without the height (M6, M18,
M23, M27) as the table arm's volume test dropped (M11), each never
bulky by volume alone; the table arm's names in another order and the
iter arm's halves crossed (M7, M25) as the ★ arm's Bulky and Heavy
swapped (M5); and the table arm's smallest side tested (M8) as the iter
arm's all sides needed long (M22). The other six fail in ways of their
own, in arms that already hold their kept edits: the ★ arm's Both read
as Neither (M2), the nested arm's height past its share needed and
width not tested alone (M13, M16), the rec arm's side past `10^4`
needed (M19), and the template's length not tested alone and Both read
as Bulky (M29, M30).

## Verification

Every arm prints the same output as `box.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.4 to 5.2 s and the differential 0.4 s; under `karac __mir-llvm-asan` the arms take 0.5 to 1.2 s and the differential 0.5 s; and under `karac run` the differential takes 0.5 s.

## Benchmarks

The bench builds `10^5` random boxes once from its own generator, half
with sides from 1 to `10^5` and half from 1 to 2000, masses from 1 to
1000, then makes 220 passes. Each pass names every box, starting at an
offset the checksum so far picks, and folds the name's place among the
four plus the pass into the checksum. The bench uses the ★ arm in all
five languages. Every implementation prints `220 passes over 100000
boxes: checksum 281780205`.

BENCHTAB
