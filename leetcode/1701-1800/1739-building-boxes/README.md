# 1739. Building Boxes

You have a cubic storeroom where the width, length, and height of the
room are all equal to `n` units. You are asked to place `n` boxes in this
room where each box is a cube of unit side length. There are however some
rules to placing the boxes:

- You can place the boxes anywhere on the floor.
- If box `x` is placed on top of the box `y`, then each side of the four
  vertical sides of the box `y` **must** either be adjacent to another
  box or to a wall.

Given an integer `n`, return *the **minimum** possible number of boxes
touching the floor.*

```
n = 3   ->  3
n = 4   ->  3
n = 10  ->  6
```

**Constraints:** `1 <= n <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `boxes.kara` ★ | boxes piled in a corner as a staircase hold the most for their floor: a staircase on the triangle of side s holds the triangles 1, 3, 6, ... up to it, s (s + 1) (s + 2) / 6 boxes. Whole layers are added while they fit; then each floor box laid along the staircase's edge lets a column one taller than the last stand on it, so the j-th holds j more, and they are added until the n boxes fit. O(n^(1/2)) |
| `boxes_search.kara` | the largest staircase that fits by a binary search on its side, then the fewest extra floor boxes j with j (j + 1) / 2 at least the boxes left by a second; both searches share one function that takes the test as a closure. O(log n) |
| `boxes_floor.kara` | a binary search on the floor itself: a floor of f boxes holds the most as the triangle of the largest side s with s (s + 1) / 2 at most f, found from an `f64` square root, plus its f - s (s + 1) / 2 boxes along the edge, and the answer is the smallest f that holds n. O(log n) |
| `boxes_solution.kara` | a Rust solution as LeetCode's Rust users write it, `sum += k * (k + 1) / 2` while it fits, `k -= 1`, then `ans += 1; sum += i; i += 1` while `sum < n`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 11 lines: LeetCode's three examples, then 1
and 2 boxes, a full staircase of 4 layers (20 boxes) and one box more,
and `10^9`, LeetCode's largest; then the answers for every count from 1
to 2000 summed, and the answers summed and a checksum for 3000 random
counts up to 1000 and 3000 up to `10^9`. `boxes.py` mirrors the ★ arm
and its output is byte-identical.

```
3
3
6
1
2
10
11
1650467
every count from 1 to 2000: floors sum to 304108
3000 counts up to 1000: floors sum to 284746, checksum 237575868
3000 counts up to 1000000000: floors sum to 2764284474, checksum 19520311
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: in a room n boxes wide, floor boxes are laid in the corner one
diagonal after another, and after each one every box the rule allows is
stacked, a box going on top of another only when each of the lower box's
four sides touches a box or a wall, until n boxes stand; the answer is
the floor boxes laid by then. It checks 1000 random counts from 1 to 120,
each with a random split m. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | one box more needs the same floor or one floor box more |
| P3 | n boxes need no more floor than m boxes and n - m boxes apart |
| P4 | a full staircase of s layers needs s (s + 1) / 2 floor boxes |
| P5 | each arm agrees with at least two of the other three |

P3 holds because the two piles can stand in two corners of the room. The
literal reading takes the corner staircase's floor order as given, which
is the problem's insight, but it stacks every box by the rule itself
rather than counting by formula. The differential prints `1000 problems:
checksum 37148871, 20000 checks over 4 arms: 0 failures` under every lane
in Verification, and a Python reading, the smallest floor whose best
pile holds n found by counting up, gives the same checksum. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Two first choices were equivalent and
were replaced: the ★ arm's layer test `<=` made `<`, and the search
arm's staircase test `>` made `>=`. Each only moves an exact staircase
from the layers to the edge, where its last layer's s (s + 1) / 2 boxes
take exactly s extra floor boxes, the same count.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: floor boxes added while two or more boxes are missing, not one | P1 300, P3 7, P5 300 |
| M2 | ★: each extra floor box holds one box more than it does | P1 693, P5 693 |
| M3 | ★: the staircase's floor the triangle of side s - 1 | P1 1000, P2 68, P3 56, P4 1000, P5 1000 |
| M4 | search: the staircase counted as (s + 1) (s + 2) (s + 2) / 6 | P1 107, P5 107 |
| M5 | search: extra floor boxes until they hold more than what is left | P1 307, P4 1000, P5 307 |
| M6 | search: the staircase's boxes taken as twice what they are | P1 927, P2 56, P3 132, P5 927 |
| M7 | floor: the edge's j boxes holding j (j - 1) / 2, not j (j + 1) / 2 | P1 686, P2 65, P3 16, P5 686 |
| M8 | floor: the smallest floor holding more than n, not at least n | P1 294, P4 975, P5 294 |
| M9 | solution: the last layer that did not fit kept, `k -= 1` dropped | P1 1000, P4 1000, P5 1000 |
| M10 | solution: the first extra floor box holding none | P1 927, P2 141, P3 10, P5 927 |

## Benchmarks

The bench draws 20000 random counts up to `10^9`, LeetCode's largest,
all of them first, then answers each 15 times by the ★ arm in all five
languages; each answer walks about 1800 layers and up to as many edge
boxes, its loops' trip counts set by the count. Every implementation
prints `20000 counts up to 1000000000, 15 rounds: floors sum to
278846682150, checksum 443337599`. The C build also runs clean under
gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ad6400d909` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.258 s |
| Rust (`rustc -O`) | 0.264 s |
| Go | 0.276 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.406 s |
| Kāra (`karac build`) | 0.431 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.677 s |
| Python | 55 s |

The sequential Kāra build takes 1.54x Rust's time and 0.60x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md).
The loops' sums are overflow-checked in Kāra; with Rust's checks on,
Kāra is 40% faster, so the gap to plain Rust is the cost of the checks
rather than a missed optimization. C is the fastest here at 0.258 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.400 s and 0.402 s on one
run).

## Verification

All four arms print the same output as `boxes.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `ad6400d909`.

## Writing it

The ★ arm checked clean as first written. The search and floor arms
each took one `karac fix`: `let (mut low, mut high) = ..`, Rust's
spelling, became `let mut (low, high) = ..`, Kāra's, which makes every
binding of the pattern mutable.

LeetCode's Rust template took one `karac fix` of 4 edits: `struct
Solution {}` added, and the `0i64` and `1i64` suffixes on `sum`, `k` and
`i` dropped, since an integer literal is `i64` by default. `n as i64`,
`k -= 1` and `ans as i32` carried over as written.

The differential took one `karac fix`: the literal reading's `let (mut
floor, mut diagonal, mut along)` became `let mut (floor, diagonal,
along)`, and an `as i64` on the `i32` answer was dropped, since it widens
by itself.
