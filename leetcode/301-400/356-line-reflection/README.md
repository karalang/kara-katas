# 356. Line Reflection

Given `n` points on a 2D plane, decide whether there is a line parallel to
the y-axis that reflects the given points symmetrically: reflecting every
point over the line gives the same set of points. Points may repeat.

```
points = [[1,1],[-1,1]]   ->  true   (the line x = 0)
points = [[1,1],[-1,-1]]  ->  false
```

**Constraints:** `1 <= n <= 10^4`; `-10^8 <= points[i][j] <= 10^8`.

## Approaches

Every arm uses the same first step: if a line `x = c` works, it maps the
leftmost points onto the rightmost ones, so `2c = min x + max x`. Working in
doubled coordinates keeps it integral: the image of `(x, y)` is
`(min + max - x, y)`.

| file | mechanism | cost |
|---|---|---|
| `line_reflection.kara` ★ | put every point in a `Set`, then look up each point's image | `O(n)` expected |
| `line_reflection_rows.kara` | group xs into rows by y in a `Map`; sort and deduplicate each row and check that its i-th smallest and i-th largest x sum to `min + max` | `O(n log n)` |
| `line_reflection_mirror.kara` | sort and deduplicate the points and their images, then compare the two lists | `O(n log n)` |
| `line_reflection_pairs.kara` | for each point, scan the whole list for its image | `O(n^2)` |
| `differential.kara` | the four arms against an oracle that tries every candidate line, 24,000 checks, five properties | — |

Every arm prints the same 13 lines: both LeetCode examples, ten edge cases
(no points, one point, a point on the line, duplicates on one side, a
half-integer line, matching xs with the wrong ys, a column of points on the
line, one stray point, negative coordinates, coordinates of `10^8`), and a
checksum over 2,000 random sets. `line_reflection.py` mirrors the ★ arm and
its output is byte-identical.

Duplicates are the trap for the sorting arms: `[(1, 1), (1, 1), (3, 1)]`
reflects about `x = 2` because it is the set that reflects, but without the
deduplication the row `[1, 1, 3]` pairs `1` with itself and fails.

## Differential

`differential.kara` holds copies of the four arms and an oracle that never
uses the `min + max` step: it tries every candidate line `x = c / 2` for
doubled `c` between the extremes and asks whether that line maps every point
onto a point. 3,000 random sets of 0 to 10 points with x in `-4..=4` and y in
`0..=2`, so collisions, duplicates and points on the line are all common;
half of them are built symmetric about a random line.

| | property |
|---|---|
| P1 | every arm returns the oracle's answer |
| P2 | shifting every x by the same amount does not change the answer |
| P3 | negating every x does not change the answer |
| P4 | duplicating every point does not change the answer |
| P5 | a set built symmetric about a line reflects |

It prints `3000 cases, 24000 checks, 1869 reflect, 0 failures` under
`karac run --interp`, LLJIT, and both builds.

## Mutation testing

Eleven edits to the copies inside `differential.kara`, each built and run.
All eleven are killed.

| # | mutation | how |
|---|---|---|
| M1 | set: the line is off by half a unit | P1 and P2, 3186 failures |
| M2 | set: the image lookup ignores y | P1 and P2, 2628 failures |
| M3 | rows: no deduplication | P1 and P3, 2 failures |
| M4 | rows: every x is paired with the row's largest | P1 and P3, 2842 failures |
| M5 | mirror: no deduplication | P1 and P4, 2 failures |
| M6 | mirror: the images drop their y | P1 and P4, 2774 failures |
| M7 | pairs: `lo` tracks the maximum | P1, 1421 failures |
| M8 | pairs: compares x only | P1, 323 failures |
| M9 | set: an empty set does not reflect | P1 and P2, 552 failures |
| M10 | oracle: ignores y | P1 to P4, 2261 failures |
| M11 | set: the line taken from the first point alone | P1 and P2, 2710 failures |

M3 and M5 are killed by two cases each. The symmetric half of the random
sets pushes every point together with its image, so duplicates arrive in
pairs and a row without deduplication still reads as a palindrome; only a
random set with an odd duplicate on a symmetric row catches it, which is why
every arm's own edge cases include `duplicates on one side`.

## Verification

All four arms and the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build`, and the four arms match
`line_reflection.py` byte for byte. Under valgrind at `KARAC_OPT_LEVEL=0`
every arm ends with `in use at exit: 0 bytes in 0 blocks` and
`ERROR SUMMARY: 0 errors`. The bench program prints
`266 of 400 sets reflect, checksum 982136625` under LLJIT, the interpreter
and both builds, as do its C, Rust, Go and Python mirrors.

## Benchmarks

Not measured yet. The bench programs in `bench/` and their C, Rust, Go and
Python mirrors are written and agree on the printed checksum, but the timings
still have to be taken on a quiet machine. This section will carry the table
when they are.

## Compiler findings

- **B-2026-10-06-124 (fixed in kara, typecheck): an unsolved collection type was
  not pinned by the declared slot it flowed into.** The first draft's
  `fn show(label: String, points: ref Vec[(i64, i64)])` refused
  `show("no points", Vec.new())` with "expected 'ref Vec[(i64, i64)]', found
  'Vec[?T0]'", and so did `let e = Vec.new();` handed to any parameter,
  struct field, return or annotated `let` before a `push` pinned it. Fixed in kara `783f87213`.
- **B-2026-10-06-125 (open, codegen):** `Vec.with_capacity(n)` as a call argument
  does not build: codegen asks for a `let` annotation even where the
  parameter names the type.
