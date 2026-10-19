# 801. Minimum Swaps To Make Sequences Increasing

Given two integer arrays `nums1` and `nums2` of the same length, an
operation swaps `nums1[i]` with `nums2[i]` for one place `i`. Return the
fewest operations that make both arrays strictly increasing. The test
cases are made so that it can always be done.

```
nums1 = [1, 3, 5, 4], nums2 = [1, 2, 3, 7]        ->  1
nums1 = [0, 3, 5, 8, 9], nums2 = [2, 1, 4, 6, 9]  ->  1
```

**Constraints:** `2 <= nums1.length <= 10^5`, `nums2.length ==
nums1.length`, `0 <= nums1[i], nums2[i] <= 2 · 10^5`.

## Approaches

| file | mechanism |
|---|---|
| `min_swap.kara` ★ | left to right, keep the fewest swaps with place `i` left alone and with it swapped; place `i` follows place `i - 1` in the same state when each array goes up there, and in the other state when each goes up across. O(n), O(1) space |
| `min_swap_table.kara` | the same recurrence with a row `Array[i64, 2]` of the table kept for every place |
| `min_swap_memo.kara` | asked from the left: the fewest swaps for places `i` onwards given whether place `i - 1` was swapped, each answer worked out once and kept |
| `min_swap_pieces.kara` | where both "same" and "cross" work between two places, the choice at the second is free of the first, so those places cut the array into pieces; inside a piece one choice fixes the rest, and the piece's two ways swap complementary places, so each piece adds the smaller count |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 7 lines: LeetCode's two examples; `[1, 2], [3,
4]`, which needs nothing; `[3, 2], [1, 4]`, which needs its first place
swapped; `[0, 4, 4, 5, 9], [0, 1, 6, 8, 10]`, where `nums1` has a place
equal to the one before; `[0, 11, 2, 13, 4, 15], [10, 1, 12, 3, 14, 5]`,
where every other place is swapped and three swaps undo it; and 300
random pairs of up to 41 places, two increasing arrays with some places
swapped, with the total of their answers and a checksum. `min_swap.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
try every set of places to swap, and keep the smallest whose result has
both arrays strictly increasing. Its 1,600 cases have 2 to 12 places and
come in four kinds of 400: two increasing arrays climbing by 1 a place,
so that many places can go only one way; climbing by 1 or 2; by 1 to 4;
and climbing by 1 to 4 with the two arrays often holding the same number
at a place. Each place is then swapped at random.

| | property |
|---|---|
| P1 | the definition's count |
| P2 | the same count with the two arrays given the other way round |
| P3 | the same count with both arrays read backwards and every number negated |
| P4 | at most half the places, and the same count with a number above all the others put at the end of both |

It prints `1600 cases (2007 swaps), 4 arms, 25600 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: swapping the first place costing nothing | P1 283, P3 373 |
| M2 | ★: "same" checking nums1 alone | P1 450, P2 632 |
| M3 | ★: a cross into keep costed from keep | P1 906 |
| M4 | table: equal numbers taken as going up | P1 464 |
| M5 | table: the answer from the last place left alone only | P1 179, P3 270, P4 179 |
| M6 | table: a swap stored as costing nothing | P1 906 |
| M7 | memo: the earlier place's state passed on, not this one's | P1 495, P4 159 |
| M8 | memo: kept answers looked up without the state | P1 195, P3 350, P4 118 |
| M9 | memo: one array going up taken as enough | P1 906 |
| M10 | pieces: a free place not cutting the piece | P1 976, P4 835 |
| M11 | pieces: the last piece's smaller way not taken | P1 158, P3 268, P4 158 |
| M12 | pieces: flipping where only "same" works | P1 778 |

P1 kills all twelve. P2 sees only the "same" test that looks at `nums1`
alone, the one edit that treats the two arrays unlike each other. P3 and
P4 between them see six: the three that treat an end of the array unlike
the middle (M1, M5, M11), whose counts change when the arrays are read
backwards or lengthened; the memo arm's two state mix-ups (M7, M8); and
the free place that does not cut a piece (M10), whose counts can pass
half the places. The other five give a wrong count that keeps every
property, and are seen by P1 alone.

## Verification

Every arm prints the same output as `min_swap.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`b95ac9a0c5`, whose last compiler change is `e6d52d2c4b`. The runtime
archives were built after the last runtime change, `216d20e28a`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`) prints the same
output for all four arms and the differential unchanged, and the legacy
JIT (`karac run`), `karac build` and an auto-par build print it for the
★, memo and pieces arms. Legacy codegen refuses the table arm's
`best[n - 1][0].min(best[n - 1][1])` as a chained indexed receiver, and
still refuses it with the row bound first; a copy with the two numbers
bound as `i64` first prints the same output under all four. Legacy also
refuses the differential, where a bare parameter is owned rather than
borrowed and so the arrays are moved and used again; a copy with the
table fix and the arrays passed as `ref Vec[i64]` prints its line under
all four. The bench program is refused the same way at `min_swap(a, b)`,
with `a` and `b` bound by `ref`; a copy with `ref Vec[i64]` parameters
builds and prints the same line, and the bench timing below is of it.
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 16 pairs of
arrays of 100,000 places, LeetCode's longest, are made once: two
increasing arrays climbing by 1 or 2 a place, with each place swapped at
random. Each of 2,000 rounds finds the fewest swaps for the next pair.
Every implementation prints `2000 rounds of 100000 places: 98507375
swaps in all, checksum 494931962`, the Kāra program under `karac
__mir-run` included (in 227 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.29 to 1.40 s |
| Rust (`rustc -O`) | 1.28 to 1.47 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.55 to 1.79 s |
| Go | 1.37 to 1.68 s |
| Python | 51.71 to 52.88 s |
| Kāra (`karac build --mir`) | 1.44 to 1.72 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 5.2 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 1.57 s,
against C's 1.34, Rust's 1.37 (1.67 under overflow checks) and Go's
1.48. Under valgrind's cachegrind v2 runs 7.39 billion instructions and
1.94 billion branches, against Rust's 6.01 billion and 1.26 billion and
C's 4.79 billion and 752 million. The legacy build of the copy ran 1.53
to 1.69 s, a median of 1.58 s in the interleaved runs, with 6.81 billion
instructions and 1.71 billion branches, so v2 and legacy are level. All
four mispredict 117 to 155 million branches: the swaps are random, so
whether each array goes up across a place is a coin toss, and no build
seems to turn that test into a branchless select; that is inferred from
the counts, not read from the assembly. The comparison with C and Rust
waits until after M4.

## Compiler findings

- **B-2026-10-19-32** (v2 typecheck, open): on a `Vec[Array[i64, 2]]`,
  `best.push([0, 1])` is refused because the list literal is typed as a
  `Vec[i64]`, although the same literal passed to a free function whose
  parameter is `Array[i64, 2]` is accepted. `min_swap_table.kara` binds
  each row with its type written out before pushing it; push the
  literal once the row is fixed.
