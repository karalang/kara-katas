# 2222. Number of Ways to Select Buildings

You are given a **0-indexed** binary string `s` which represents the
types of buildings along a street where:

- `s[i] = '0'` denotes that the `ith` building is an office and
- `s[i] = '1'` denotes that the `ith` building is a restaurant.

As a city official, you would like to **select** 3 buildings for random
inspection. However, to ensure variety, **no two consecutive** buildings
out of the **selected** buildings can be of the same type.

- For example, given `s = "001101"`, we cannot select the `1st`, `3rd`,
  and `5th` buildings as that would form `"011"` which is **not**
  allowed due to having two consecutive buildings of the same type.

Return *the **number of valid ways** to select 3 buildings.*

```
s = "001101"  ->  6
s = "11100"   ->  0
```

**Constraints:** `3 <= s.length <= 10^5`; `s[i]` is either `'0'` or
`'1'`.

The selections are the subsequences `"010"` and `"101"`. One pass keeps
how many 0s and 1s are behind, and how many pairs `"01"` and `"10"`: a 0
extends every 1 behind into a `"10"` and closes every `"01"` into a
`"010"`, and a 1 the other way round. O(n). The count reaches about
n^3 / 24, past `i32` at 10^5 buildings.

## Approaches

| file | mechanism |
|---|---|
| `buildings.kara` ★ | one pass keeping the 0s and 1s behind and the pairs `"01"` and `"10"`, each building closing the pairs that end in the other type |
| `buildings_middle.kara` | by the middle building: each adds (other type before) * (other type after), the counts after the totals less those before |
| `buildings_table.kara` | `ending[k][d]`, the alternating subsequences of length k ending in type d, a building extending those of length k - 1 that end in the other type; the answer the two of length 3 |
| `buildings_struct.kara` | a `struct Surveyor` holding a `struct Tally` of buildings seen and pairs for each type and the selections closed, with `see` (`mut ref self`) and `ways` (`ref self`) |
| `buildings_iter.kara` | a `fold` over the characters carrying a five-field tuple, each step a `match` on the character returning the next tuple |
| `buildings_solution.kara` | LeetCode's Rust template: a `String` in, `i64` out, the street read through `as_bytes()` and compared with `b'0'`, the totals by `filter(\|&&b\| ...).count() as i64`, the running counts a tuple of `0i64`s, each building scored as the middle; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(too short, `"010"`, `"101"`, and all alike), each with its answer; then
a checksum of 3000 random streets of 1 to 40 buildings, each a 1 with
chance 1, 5 and 9 in 10 in turn; then the constraints' largest, 10^5
random buildings and 10^5 alternating, whose count of 41666666650000 is
past `i32`. `buildings.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one round of 13 edits: `as_bytes()`
to `bytes()`, the `|&&b|` and `for &b` patterns to `|b|` and `for b`, the
`as i64` casts dropped where the value is already `i64`, `let (mut c0,
mut c1) = (0i64, 0i64)` to `let mut (c0, c1) = (0, 0)`, `0i64` to `0`,
`struct Solution;` to `struct Solution {}` and `Solution::` to
`Solution.`. The byte literal `b'0'` is Kāra's too.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every three buildings i < j < k tried, and kept when no two
adjacent in the selection are of the same type; no running counts. It
checks 300 random streets of 1 to 20 buildings, each a 1 with chance 1,
5 and 9 in 10 in turn; then 30 of one type; then 30 alternating. All 360
are drawn before any arm answers.

| | property |
|---|---|
| P1 | the ways are the statement read literally |
| P2 | they are at least 0 and at most C(zeros, 2) * ones + C(ones, 2) * zeros |
| P3 | the street reversed: the same ways |
| P4 | every building's type swapped: the same ways |
| P5 | the street cut in two at a random point: at least the two halves' ways together |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 917389207, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading over
`itertools.combinations` of three buildings. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to each
of the others, each run under `karac __mir-llvm-run` and `karac
__mir-run`. Seventeen are kept, three to each Kāra arm and two to the
Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: a 0 never counted as seen | P1 181, P4 195, P6 181 |
| M5 | ★: a 1 closing at most one selection | P1 167, P3 104, P4 181, P6 167 |
| M6 | ★: each 1 behind a 0 counted twice into its pairs | P1 182, P2 9, P4 195, P6 182 |
| M7 | middle: a 0 scored by the 0s before it, itself included | P1 202, P2 21, P3 202, P4 233, P6 202 |
| M8 | middle: a 1's two sides added, not multiplied | P1 228, P2 16, P4 195, P6 228 |
| M11 | middle: a 0 scored by the other 0s around it | P1 253, P2 93, P4 310, P6 253 |
| M13 | table: a building extending runs of its own type | P1 320, P2 182, P6 320 |
| M14 | table: the pairs counted, not the triples | P1 227, P2 8, P6 227 |
| M15 | table: the selections ending in 0 counted twice, those in 1 not | P1 195, P2 11, P4 195, P6 195 |
| M18 | struct: a 0 closing the pairs that end in 0 | P1 170, P3 169, P4 220, P6 170 |
| M20 | struct: the selections reset at every seventh 1 | P1 90, P3 81, P4 145, P5 18, P6 90 |
| M21 | struct: each 0 adding one pair too many | P1 226, P2 8, P3 202, P4 202, P6 226 |
| M24 | iter: a 1 pairing with the 1s behind it | P1 192, P3 171, P4 222, P6 192 |
| M25 | iter: a 1 extending the 0s behind into `"10"` pairs too | P1 183, P3 171, P4 200, P6 183 |
| M26 | iter: a 1 adding the square of the pairs it closes | P1 167, P2 119, P3 124, P4 183, P6 167 |
| M28 | solution: the 1s after a 0 counted from the whole street | P1 223, P2 94, P3 202, P4 234, P6 223 |
| M29 | solution: a 0 scored by the 0s around it, itself among those after | P1 261, P2 114, P4 323, P6 261 |

P1 and P6 kill all seventeen, P4 fifteen, P2 eleven, P3 nine and P5
one. P4 swaps the types, so it kills every edit that treats 0s and 1s
unlike; it misses only the table arm's two that spoil both types alike
(M13, M14). P5 is weak: cutting the street only loses the selections
that cross the cut, so an arm that undercounts or overcounts the same
way in every street keeps the halves below the whole, and only the
struct arm's reset at every seventh 1 (M20), which loses more the
longer the street, breaks it.

Of the thirty-one, fourteen were not kept. Three survive and are
equivalent: the ★ arm's `"10"` pairs grown before the `"010"`s are
closed (M1), the table arm's lengths updated upward (M12), and the
struct arm's 0 counted as seen before its pairs grow (M19); in each the
two updates read and write different counts, so their order cannot
matter. None crashes, and none differs between the backends. Seven fail
as a kept one does: the ★ and iter arms' 0 closing `"10"` pairs (M2,
M23) as the struct arm's (M18); the ★ and struct arms' 1 pairing with
the 1s behind (M3, M17) as the iter arm's (M24); the middle and iter
arms' 1 never scored or the 0s never counted (M10, M22) as the ★ arm's
0 never counted (M4); and the table arm's single 1 counted twice (M16)
as the ★ arm's pairs counted twice (M6). Four fail their own way and are
left out for the count of three (two for the template): the middle
arm's total of 1s one short (M9), and the template's 1s never counted
as seen, its 0s counted as `b'1'`, and a 1 scored with one 0 too few
after it (M27, M30, M31).

## Verification

Every arm prints the same output as `buildings.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.5 s to 1.0 s, and the
differential 0.5 s.

## Benchmarks

The bench draws 30 streets of 10^5 buildings once, each a 1 with chance
one half, then punches each street 10 times, one building drawn again
each time, and answers it after each punch with the ★ arm in all five
languages. Every implementation prints `30 streets of 10^5, 10 punches:
checksum 430313226`.

BENCHTAB
