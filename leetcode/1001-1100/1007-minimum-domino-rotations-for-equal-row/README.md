# 1007. Minimum Domino Rotations For Equal Row

In a row of dominoes, `tops[i]` and `bottoms[i]` represent the top and
bottom halves of the `i`th domino. (A domino is a tile with two numbers
from 1 to 6, one on each half of the tile.)

We may rotate the `i`th domino, so that `tops[i]` and `bottoms[i]`
swap values.

Return the minimum number of rotations so that all the values in `tops`
are the same, or all the values in `bottoms` are the same.

If it cannot be done, return `-1`.

```
tops = [2,1,2,4,2,2], bottoms = [5,2,6,2,3,2]   ->  2
tops = [3,5,1,2,3],   bottoms = [3,6,3,3,4]     ->  -1
```

**Constraints:** `2 <= tops.length <= 2 * 10^4`;
`bottoms.length == tops.length`; `1 <= tops[i], bottoms[i] <= 6`.

## Approaches

A row of equal values needs a face that every domino shows on one
half. Turning a domino moves the face from one row to the other, so for
a face that qualifies, filling the top costs the dominoes without it on
top and filling the bottom those without it below. The arms differ in
how they find the faces that qualify and how they count.

| file | mechanism |
|---|---|
| `min_rotations.kara` ★ | two candidates: a qualifying face must be on the first domino, so try its top and its bottom, each in one walk that counts both rows' turns and gives up at the first domino without the face. O(n) |
| `min_rotations_count.kara` | counting faces: for each face, the dominoes showing it on top, below, and on both; it qualifies when top plus bottom less both is all n. O(n) |
| `min_rotations_faces.kara` | every face: twelve tries, each of the six faces for each of the two rows, each a walk that stops at the first domino without the face. O(n) |
| `min_rotations_mask.kara` | a set of faces: six bits, each domino keeping only the bits of its two faces; the faces left qualify, and each is counted. O(n) |
| `min_rotations_halves.kara` | divide and conquer: a table of twelve costs, one per face and row, for each half of the dominoes, added entry by entry; a single domino costs 0 where the face is in place, 1 where it is on the other half, and none elsewhere. O(n), log n calls deep |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 17 lines. The first ten are LeetCode's two
examples and eight more: two doubles of 1; two dominoes that need one
turn; two that share no face; one domino of four turned; a row where
face 6 needs one turn; a row where only 6 qualifies through the
bottoms; `[2,3,2,3]` over `[3,2,3,2]`, where 2 and 3 both qualify at
two turns; and `[4,4,1,4]` over `[1,1,4,1]`, where 4 and 1 both
qualify at one. Then three rows of LeetCode's longest, 20,000
dominoes: all 6 over 6; 3 on alternate halves; and 5 everywhere but
the last domino, which cannot be done. Then totals over random rows,
each with faces from 1 to a random top, and with a random chance in 8
that a domino shows a chosen face on a random half (every domino, in
half the rows): 3,000 rows of up to 8 dominoes, 1,000 of up to 100,
100 of up to 2,000 and 3 of up to 20,000. `min_rotations.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every set of dominoes to turn, kept when it leaves the
top row or the bottom row all one value, and the size of the smallest.
It checks 3,200 random rows drawn as above: 3,000 of 2 to 8 dominoes
against the statement, and 200 of up to 300 against the other
properties.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 rows |
| P2 | swapping the two rows gives the same answer |
| P3 | the dominoes in reverse order give the same answer |
| P4 | -1, or at most half the dominoes |
| P5 | renaming every face `v` to `7 - v` gives the same answer |
| P6 | each arm agrees with at least two of the other four |

P4 holds because, for a face that qualifies, the turns that fill the
top and those that fill the bottom are the dominoes without it on one
half each, at most n together.

It prints `3200 rows of 45912 dominoes: 2478 possible, checksum
553869021, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (5.2 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-five edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only the first top tried | P1 620, P2 1284, P3 833, P6 654 |
| M2 | ★: a double counted as a turn below | P1 512, P2 1102, P6 564 |
| M3 | ★: every domino must show the face twice | P1 1803, P6 1907 |
| M4 | count: doubles counted twice | P1 2012, P6 2146 |
| M5 | count: "on both" read backwards | P1 1998, P2 670, P6 2131 |
| M6 | count: face 6 never tried | P1 44, P5 1075, P6 47 |
| M7 | faces: a turn counted twice | P1 1241, P4 713, P6 1343 |
| M8 | faces: face 1 never tried | P1 974, P5 1075, P6 1028 |
| M9 | faces: the other half read backwards | P1 1822, P4 1602, P6 1979 |
| M10 | mask: only the top face kept | P1 1499, P2 524, P6 1602 |
| M11 | mask: faces joined, not intersected | P1 656, P4 146, P6 722 |
| M12 | mask: both rows' turns added | P1 1803, P4 1446, P6 1907 |
| M13 | halves: costs merged by the larger | P1 484, P6 584 |
| M14 | halves: one half able is enough | P1 1259, P3 259, P4 1, P6 1343 |
| M15 | halves: the most turns kept | P1 1383, P4 687, P6 1477 |

P1 and P6 kill all fifteen, P4 six, P2 four, and P3 and P5 two each.
The checks draw no random number that depends on an answer, so every
mutant sees the same rows and their counts can be compared. P5 sees
exactly the edits that skip a face, since renaming moves the faces
the edit skips (M6 and M8 fail it on the same 1,075 checks, as 6 and 1
trade places). P2 sees the edits that treat the two rows unevenly: the
★ arm trying only the first top, or charging a double to the bottom,
the count arm's "on both", and the mask keeping only the top face. P3
sees only the two that depend on where a domino is: the ★ arm's first
domino picks its candidates, and a halves table that accepts one able
half depends on how the row splits. Most edits are caught only by the
statement and by agreement, because a wrong answer here is usually
still a small number of turns, or -1, which P4 allows.

Ten other edits were tried and set aside. Two change no answer: the ★
arm keeping the first candidate when both work, and the halves arm
splitting one domino off at a time. The first is a fact about the
problem: two different faces both qualify only when every domino shows
both, and then the turns to fill a row with one face are those that
fill the other row with the other, so the two candidates cost the same.
Five failed exactly the same checks as a kept one: the ★ arm taking the
more turns, the count arm taking the more turns and the faces arm
keeping the most, as M15; the mask leaving out face 6, as M6; and the
halves arm charging one turn for a domino without the face, as M11.
Three were killed but beyond three an arm and failed the same checks as
each other: the count arm, the faces arm and the mask each filling only
the top row.

## Verification

Every arm prints the same output as `min_rotations.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer)
with no error; the differential prints its line under all three.
`karac check` passes all five arms, the differential and the bench
program. `karac run` and a `karac build` binary print the same output
for every arm and the differential. The release build is at kara
`8b6e8a9088`, with the runtime archives rebuilt there. Under `karac
__mir-run` the arms take 0.8 s (★) to 3.9 s (halves).

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. The program draws 20
rows of 20,000 dominoes, LeetCode's longest, once, with faces from 1 to
6; in row `t` every domino shows face `t % 6 + 1` on a random half,
except in the odd rows, where one domino in 2,000 is left as drawn, so
those rows can rarely be done and their walks stop early. In each of
400 rounds it runs the arm on every row, each round starting from a
different one, and folds every answer into a checksum. Every
implementation prints `400 rounds over 20 rows of 20000 dominoes:
answers sum to 33020800, checksum 63470463`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `8b6e8a9088`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.401 to 0.477 s | 0.415 s |
| Rust (`rustc -O`) | 0.451 to 0.492 s | 0.466 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.597 to 0.652 s | 0.611 s |
| Go | 0.476 to 0.510 s | 0.490 s |
| Python | 10.6 s | |
| Kāra (`karac build`) | 0.629 to 0.652 s | 0.636 s |

`bench.sh` builds the Kāra program with `karac build`, which is the v2
compiled backend since M3. Python's run is about 17 times Kāra's.

v2 took 1.04 times Rust's median time under overflow checks and 1.53
times C's. Under valgrind's cachegrind v2 ran 1,223 million
instructions with 67.0 million branches mispredicted, Rust with
overflow checks 1,120 million and 46.9 million, Rust without them
1,079 million and 46.9 million, and C 833 million and 46.9 million.
The other three mispredict the same 46.9 million, on the faces drawn
at random; v2 mispredicts 20 million more, and we did not look into
which branch.
