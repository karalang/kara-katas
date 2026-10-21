# 832. Flipping an Image

Given an `n x n` binary image, flip it horizontally, then invert it, and
return the result. To flip an image horizontally is to reverse each of
its rows: `[1,1,0]` flipped is `[0,1,1]`. To invert it is to replace
each `0` by `1` and each `1` by `0`: `[0,1,1]` inverted is `[1,0,0]`.

```
image = [[1,1,0],[1,0,1],[0,0,0]]                    ->  [[1,0,0],[0,1,0],[1,1,1]]
image = [[1,1,0,0],[1,0,0,1],[0,1,1,1],[1,0,1,0]]    ->  [[1,1,0,0],[0,1,1,0],[0,0,0,1],[1,0,1,0]]
```

**Constraints:** `1 <= n <= 20`, and every cell is `0` or `1`.

## Approaches

Each row is reversed and every cell inverted; the arms differ in whether
they change the image in place and in how they reverse a row.

| file | mechanism |
|---|---|
| `flip_and_invert_image.kara` ★ | two pointers in place: the cells at `i` and `n - 1 - i` swap places and are each inverted as the walk closes in from both ends, and the middle cell of an odd row is only inverted. The image is taken owned. O(n^2) |
| `flip_and_invert_image_fresh.kara` | a new image, cell by cell: column `c` of a row is `1 -` the cell at `n - 1 - c` of the same input row, which is only read. O(n^2) |
| `flip_and_invert_image_reverse.kara` | the library's `reverse` on each row of the owned image, then every cell inverted with `^= 1` through `iter_mut`. O(n^2) |
| `flip_and_invert_image_iter.kara` | a `map` over the rows, each row's cells `rev`ersed, `map`ped to `1 - x` and `collect`ed, the rows `collect`ed in turn. O(n^2) |
| `differential.kara` | the four arms against the statement read in its two steps, four properties |

Every arm prints the same 11 lines: LeetCode's two examples; five more
(the 1 by 1 images `[[0]]` and `[[1]]`, a 2 by 2 that the answer leaves
as it is, a 2 by 2 of ones, and a 3 by 3 checkerboard); three images of
LeetCode's greatest size, 20 by 20, at random with half ones, all ones
and all zeros, each with its count of ones and a checksum; and 300
random images up to 20 by 20 with their rows counted and a checksum.
`flip_and_invert_image.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally, in its two steps: each row reversed into a new image, then
each cell of that image inverted into another. Its 1,600 cases come in
four kinds of 400: images of 1 by 1 to 4 by 4, where the two pointers
meet or cross after a step or two; images up to 20 by 20; images up to
12 by 12 whose every row reads the same both ways, so that the flip
changes nothing; and images up to 12 by 12 almost all zeros or almost
all ones. The share of ones is drawn afresh for each image.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the answer flipped and inverted again gives back the image |
| P3 | the image with its rows in the opposite order gives the answer with its rows in the opposite order |
| P4 | each row of the answer holds only zeros and ones, and as many ones as its row of the image holds zeros |

It prints `1600 cases, 25600 checks over 4 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the middle cell of an odd row not inverted | P1 813, P4 813 |
| M2 | ★: the left cell not inverted | P1 1427, P2 1427, P4 1418 |
| M3 | ★: the walk stopping one pair early | P1 775, P4 775 |
| M4 | fresh: the last row left out | P1 1600, P2 1600, P3 1178, P4 1600 |
| M5 | fresh: the cells not inverted | P1 1600, P4 1590 |
| M6 | fresh: the rows taken from the bottom up | P1 1142, P4 1098 |
| M7 | reverse: the row not reversed | P1 807 |
| M8 | reverse: the first row not reversed | P1 446, P3 603 |
| M9 | reverse: every cell set to 1 | P1 1400, P2 1385, P4 1400 |
| M10 | iter: the row not reversed | P1 807 |
| M11 | iter: the rows reversed too | P1 1142, P4 1098 |
| M12 | iter: each cell less 1, not taken from 1 | P1 1385, P2 1600, P4 1385 |

P1 kills all twelve. P2 sees only M2, M4, M9 and M12. Every other edit
undoes itself when the arm is applied twice: a flip without the
inversion (M5), the inversion without the flip (M7, M10), the rows
turned round (M6, M11), and a middle cell, an inner pair or a first row
handled wrongly the same way both times (M1, M3, M8). P3 sees only M4
and M8, the edits that treat one row unlike the others: every arm
handles each row on its own, and every other edit does the same to every
row. P4, which counts, is blind to the edits that only move cells within
a row (M7, M8, M10). M6 and M11 are the same mistake in two arms and
fail the same cases, as are M7 and M10. M12 matches the answer only on
an image of all ones, where `x - 1` and `1 - x` are both 0.

A first M8, the reverse arm's first cell left uninverted by
`row.iter_mut().skip(1)`, did not build on v2 until kara `b1a1307f12`
(Compiler findings), so the table uses another edit for it. It now
builds and is killed, P1 1600, P2 1427 and P4 1600.

## Verification

Every arm prints the same output as `flip_and_invert_image.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The release build
that runs `check`, `__mir-run` and the mutation runs is at kara
`4ef4491a35`; the debug build that runs `__mir-llvm-run`,
`__mir-llvm-asan` and `build --mir` is at `90714715b1`, 20 commits
earlier. One of those, `840bd80797`, changes the runtime for
`Pool.close`, which no program here calls; the runtime archives were
built before it and match the debug build. Under `karac __mir-run` each
arm takes about 0.3 s, the iterator arm 0.5 s, and the differential 6 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`) prints the same
output for all four arms and the differential, and the legacy JIT
(`karac run`), `karac build` and an auto-par build for the ★,
fresh-image and iterator arms. Its compiled backends refuse the reverse
arm and the differential that copies it: they lower `for .. in
v.iter_mut()` only over elements that are scalars, and the arm's outer
loop walks rows that are `Vec`s. They also refuse the bench program,
whose `mem.take` needs `Vec.default()`. Legacy is frozen, so this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
images once, the g-th of side `17 + g % 4` up to LeetCode's 20, with
each cell a one with chance 1 in 2. Each of 4,000,000 rounds takes the
next image out with `mem.take`, flips and inverts it in place, puts it
back, and reads one of its rows. Every implementation prints `4000000
rounds of 64 images: 37061138 ones, checksum 112602206`, the Kāra
program under `karac __mir-run` included, in 585 s with the
interpreter's step limit raised by `KARAC_MIR_MAX_STEPS`.

Spot timings on a shared 4-core container, eight runs of each compiled
program and 13 of v2's, five of them interleaved, and three of Python
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.85 to 1.03 s |
| Rust (`rustc -O`) | 1.23 to 1.53 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.28 to 1.67 s |
| Go | 1.40 to 1.65 s |
| Python | 60.5 to 62.0 s |
| Kāra (`karac build --mir`) | 1.33 to 1.82 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 1.66 s, against Rust's
1.39 (1.59 under overflow checks), C's 0.93 and Go's 1.56: 1.04 times
Rust's time under overflow checks, and 1.8 times C's. Under valgrind's
cachegrind C runs 8.6 billion instructions and 0.9 billion branches,
Rust 16.5 and 2.9 billion and v2 17.9 and 4.7 billion; most likely the
gap to C is the bounds check on each of the four cell accesses a step
that C does not make (not traced). Built for `x86-64-v3`, the target
`karac build` uses, C takes 0.87 to 0.99 s and Rust with overflow checks
1.39 to 1.52 s, against v2's 1.33 to 1.62 s in the same five interleaved
runs. Python takes 61 s, about 65 times C's time. The comparison with C
and Rust waits until after M4.

## Compiler findings

B-2026-10-21-50: the iterator arm's natural form, the chain returned as
the function's tail expression, passed `karac check` and was not lowered
by v2's MIR builder: the inner `collect()`, whose only type target is
the function's return type, stopped it with `an expression whose type
does not lower (Type(UnknownParam("C")))`. It was a remainder of
B-2026-10-14-6. It is fixed in kara `d6d05f6a7a`, and the arm returns
the chain itself again (rechecked at kara `13fdc32828`); until then it
bound the chain to an annotated `let` and returned that.

B-2026-10-21-51: `iter_mut()` on a `Vec` took no adaptor on v2. `for x
in row.iter_mut().skip(1)`, the first edit tried for M8, passed `karac
check` and failed to build with `an iterator value is not lowered yet`,
as did `take`, `rev`, `step_by` and an `iter_mut()` iterator bound to a
name; only `for x in v.iter_mut()` and `for (i, x) in
v.iter_mut().enumerate()` worked. No arm needs an adaptor there. It is
fixed in kara `b1a1307f12`: rechecked at kara `4a744e1ec3`, that M8 and
`skip`, `take`, `rev().step_by(2)` and a bound iterator under `while
let` all run right on both v2 backends.
