# 2237. Count Positions on Street With Required Brightness

You are given an integer `n`. A perfectly straight street is
represented by a number line ranging from `0` to `n - 1`. You are given
a 2D integer array `lights` representing the street lamp(s) on the
street. Each `lights[i] = [position_i, range_i]` indicates that there is
a street lamp at position `position_i` that lights up the area from
`[max(0, position_i - range_i), min(n - 1, position_i + range_i)]`
(**inclusive**).

The **brightness** of a position `p` is defined as the number of street
lamps that light up the position `p`. You are given a **0-indexed**
integer array `requirement` of size `n` where `requirement[i]` is the
minimum **brightness** of the `i`th position on the street.

Return *the number of positions* `i` *on the street between* `0` *and*
`n - 1` *that have a **brightness** of **at least*** `requirement[i]`.

```
n = 5, lights = [[0, 1], [2, 1], [3, 2]], requirement = [0, 2, 1, 4, 1]  ->  4
n = 1, lights = [[0, 1]], requirement = [2]                               ->  0
```

**Constraints:** `1 <= n <= 10^5`; `1 <= lights.length <= 10^5`;
`0 <= position_i < n`; `0 <= range_i <= 10^5`;
`requirement.length == n`; `0 <= requirement[i] <= 10^5`.

A difference array: each light adds one where its span, clamped to the
street, starts and takes it back just past where it ends; a running sum
over the street is then each position's brightness, and the positions
that meet their requirement are counted. O(n + m) for `m` lights.

## Approaches

| file | mechanism |
|---|---|
| `brightness.kara` ★ | a difference array from `Vec.filled(n + 1, 0)` and a running sum in one loop |
| `brightness_heap.kara` | a sweep: the spans as tuples, `sort`ed by where they start, and a min-first `PriorityQueue` of where the lit ones end; at each position the spans starting there join, the ended ones are `pop`ped while `peek` shows them, and the brightness is the queue's `len` |
| `brightness_fenwick.kara` | a Fenwick tree over the differences, `add` with `i += i & -i` and `prefix` with `i -= i & -i`, each position's brightness a prefix sum |
| `brightness_struct.kara` | a `struct Street` holding the difference array, with `light` (`mut ref self`), `brightness` for the running sums and `meeting` for the count |
| `brightness_iter.kara` | the spans a `map` over the lights, the differences a `fold` that takes the array `own` and marks each span, the brightness a `map` whose closure keeps a running sum, and the answer a `zip` with the requirements, `filter`ed and `count`ed |
| `brightness_solution.kara` | LeetCode's Rust template: `Vec<Vec<i32>>` in, a `vec![0i32; n + 1]` difference array indexed through `as usize` casts, `for l in &lights`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and five
more (no requirement anywhere, a range far past both ends, two lights at
one position, a light of range 0 at each end, and every position asking
for one more than it gets), each with its count; then a checksum of 3000
random streets of 1 to 30 positions and 1 to 30 lights, the ranges up to
the street's length (one street in ten up to 10^5); then the
constraints' largest, 10^5 positions and 10^5 lights with ranges and
requirements up to 10^5, and up to 100. `brightness.py` mirrors the ★
arm and its output is byte-identical.

`karac fix` carries the template in one round of 19 edits: `Vec<..>` to
`Vec[..]` throughout, `vec![0i32; n + 1]` to `Vec.filled(n + 1, 0i32)`,
`for l in &lights` to `for l in ref lights`, every `as usize` to `as
i64`, the index type of a Kāra `Vec`, the adapter's `vec![..]` to an
array literal, `struct Solution;` to `struct Solution {}`,
`Solution::meet_requirement` to `Solution.meet_requirement`, and the
adapter's `as i64` on the `i32` count dropped as a lossless cast.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each position, the lights whose position is within their
range of it counted, with no clamping and no differences, and the
positions whose count meets their requirement. It checks 300 random
streets of 1 to 12 positions and 1 to 8 lights, the ranges up to the
street's length and each requirement up to the number of lights; then
30 with ranges up to 10^5; then 30 with every light at one position.
All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement's count |
| P2 | the lights in the other order: the same answer |
| P3 | no requirement anywhere: every position; every requirement one more than the lights: none |
| P4 | one more light, of range 0 at position 0: no smaller answer |
| P5 | the street mirrored, each position `p` at `n - 1 - p` and the requirements reversed: the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 498095927, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that puts
each light's index into a set at every position it reaches and counts
the sets big enough. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under `karac __mir-llvm-run`, and the kept
ones under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: spans never starting at 0 | P1 196, P5 123, P6 196 |
| M4 | ★: each span one short on the right | P1 78, P5 109, P6 78 |
| M6 | ★: two per light | P1 162, P3 359, P6 162 |
| M8 | heap: spans joining one position late | P1 241, P5 144, P6 241 |
| M9 | heap: the spans never sorted | P1 147, P2 134, P5 114, P6 147 |
| M10 | heap: at most one ended span popped per position | P1 17, P5 26, P6 17 |
| M12 | fenwick: `add` stepping by one, not by the low bit | P1 128, P3 278, P5 123, P6 128 |
| M13 | fenwick: each prefix one position short | P1 224, P5 171, P6 224 |
| M16 | fenwick: a requirement met by one less | P1 151, P3 267, P6 151 |
| M17 | struct: the start of a span never marked | P1 343, P3 211, P4 159, P5 135, P6 343 |
| M18 | struct: the span's end taken back at the street's end | P1 121, P5 114, P6 121 |
| M20 | struct: the first position skipped | P1 276, P3 360, P5 118, P6 276 |
| M22 | iter: every span from 0 | P1 128, P5 158, P6 128 |
| M25 | iter: the requirement at least the brightness | P1 319, P3 360, P4 78, P6 319 |
| M26 | iter: the last position dropped | P1 282, P3 360, P5 118, P6 282 |
| M28 | solution: each span's end at its range, not its position plus range | P1 186, P3 23, P5 180, P6 186 |
| M31 | solution: a start marked once whatever its lights | P1 251, P2 26, P3 40, P4 185, P5 130, P6 251 |

P1 and P6 kill all seventeen, P5 fourteen, P3 nine, P4 three and P2
two. P5's mirror turns every edit that treats the street's two ends or
a span's two sides differently into a different count, which is most of
them. P3's two extremes catch the edits that count wrongly whatever the
light (the skipped and dropped positions, the reversed comparison, two
per light). P2 catches only the edits whose answer depends on the
lights' order: the heap arm unsorted (M9) and the template's start
overwritten rather than added to (M31).

Of the thirty-one, fourteen were not kept, and none crashes, survives,
or differs between the backends. One fails as a kept one does: the
struct arm's levels one position behind (M19) as the Fenwick arm's
prefix one short (M13). Eleven fail alike in groups of their own: the
★ arm's end taken back at the end and the heap arm's span still lit at
its end dropped (M2, M7); the ★ arm's and the template's strictly
brighter (M3, M29); the ★ arm's running sum restarted and the iter
arm's not kept (M5, M24); the heap arm's ends never popped and the
Fenwick and iter arms' end never taken back (M11, M14, M23); and the
Fenwick arm's span from its centre and the template's low end not
clamped (M15, M27). Two fail their own way and are left out for the
count of three: the struct arm's range halved (M21) and the template's
count of the dark positions (M30).

The heap arm's ends-never-popped edit (M11) was first written as the
`pop` deleted from inside the `while let` over `peek`, which then loops
forever on the first ended span; it was killed by hand and rewritten
to `break` out of the loop instead.

## Verification

Every arm prints the same output as `brightness.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★ and struct arms take 1.2 s, the iter,
template and Fenwick arms 2.0 s to 2.7 s, the heap arm 4.4 s, and the
differential 0.6 s.

## Benchmarks

The bench draws 10^5 lights with ranges up to 1000 over a street of
10^5 positions, and requirements up to 2000, once; then makes 100
passes, one light and one requirement drawn again before each, with the
★ arm in all five languages. Every implementation prints `100 passes
over 10^5 positions and lights: checksum 689323112`. Measured here by
hand, a pass took Kāra about twice what `rustc -O` took, and the same
as `rustc -O -C overflow-checks=on`: the loop's additions are checked
in Kāra.

BENCHTAB
