# 756. Pyramid Transition Matrix

A pyramid is stacked from blocks, each a letter from A to F. Each row
has one block fewer than the row below it, and each block sits on two
neighbours. A triangle of a pair of neighbours and the block on them is
allowed only if its three letters, left, right and top, are one of the
strings in `allowed`. Given the bottom row, return whether the pyramid
can be built all the way to a single block with every triangle allowed.

```
bottom = "BCD", allowed = ["BCC", "CDE", "CEA", "FFF"]  ->  true
bottom = "AAAA", allowed = ["AAB", "AAC", "BCD", "BBE", "DEF"]
                                                        ->  false
```

**Constraints:** 2 to 6 blocks in the bottom row; up to 216 allowed
triples, all different; letters A to F.

## Approaches

A row of width w has at most 6^(w - 1) rows that could stand on it, so
the arms search, and differ in how they search and what they remember.

| file | mechanism |
|---|---|
| `pyramid_transition.kara` ★ | the triples as a bitmask of tops per pair; depth first, building the row above a block at a time, and a `Set` of rows, as numbers, already shown to lead nowhere |
| `pyramid_transition_strings.kara` | rows as strings, a `Map` from each pair to the letters that may sit on it, and a `Map` remembering every row asked about with its answer |
| `pyramid_transition_levels.kara` | breadth first: the `Set` of every row that can stand at each level, from the bottom up, each triple checked against a `Set` of the allowed ones |
| `pyramid_transition_table.kara` | from the top down: a `Vec[bool]` per width marking the rows that can be finished, each marked from the rows that can be finished one level up |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 8 lines: the two LeetCode examples; a pair
with its triple, a pair with only its mirror's triple, and a pair with
none; six Fs with the triple FFF, and A to F with only FFF; and
300 random pyramids two to six blocks wide with up to 59 random triples,
with how many can be built and a checksum. The random triples may
repeat, which LeetCode rules out; every arm treats a repeat as one
triple. `pyramid_transition.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which at each level tries every row of the next width against every row
that can stand at this one and keeps those that stand on one.
2,000 random pyramids are checked, two to five blocks wide over two to
six letters, with up to twice as many triples as there are pairs of
letters, so that about a third can be built.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the same answer with the letters renamed by a random permutation and the triples shuffled |
| P3 | the same answer in a mirror: the bottom reversed and each triple's pair swapped |
| P4 | one more random triple never makes a buildable pyramid unbuildable, and the answer with it is the definition's |

It prints `2000 pyramids (636 buildable), 4 arms, 32000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a row's number with no leading 1 | P1 1, P2 1, P3 1 |
| M2 | ★: the highest block a pair allows never tried | P1 507, P2 17, P4 549 |
| M3 | ★: a triple's pair read the wrong way round | P1 346, P4 373 |
| M4 | strings: a row of two taken as the top | P1 229, P4 212 |
| M5 | strings: the middle letter of a triple taken as its top | P1 71, P4 78 |
| M6 | strings: the first letter tried taken as success | P1 464, P3 512, P4 487 |
| M7 | levels: an empty level not taken as failure | P1 1364, P4 1298 |
| M8 | levels: the letter F never tried | P1 23, P2 128, P4 21 |
| M9 | levels: stopped at width two | P1 229, P4 212 |
| M10 | table: a row's digits read in reverse | P1 50, P4 47 |
| M11 | table: the pair below read the wrong way round | P1 346, P4 373 |
| M12 | table: the letter F never put first | P1 28, P2 140, P3 44, P4 28 |
| E1 | ★: dead rows never remembered | 0 |
| E2 | strings: every row remembered as a failure | 0 |
| E3 | table: the rows that can be finished taken in reverse | 0 |

P1 kills all twelve. P2 sees the edits that treat one letter or one
position in the number unlike the others, which renaming moves:
M1, M2, M8 and M12. P3 sees M1, M6 and M12, but neither edit that reads
every pair the wrong way round, M3 and M11: such an arm answers for the
mirrored pyramid, and the mirror of the mirror is the original, so both
sides of P3 agree. P4 sees every edit but M1, since its second half
compares with the definition. M1 drops the leading 1 from a row's
number, so a row that starts with A shares its number with the same row
one block narrower, without the A; that matters only when one is
remembered as dead and the other asked about later, which happens once
among the 2,000. E1 never writes the memo, which saves time and changes
no answer; E2 remembers every row as a failure, but a row is remembered
only on the way back from it, and a success goes straight back to the
top with no row asked about again; E3 marks the rows in the other order,
and marking is the same in any order.

## Verification

Every arm prints the same output as `pyramid_transition.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`a62eacd307`, whose last compiler change is `7d736aae75`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept the level and table arms: each prints
the same output under `karac run`, `karac build` and an auto-par build,
and the level arm under the legacy interpreter too, where the table arm
did not finish within 60 s. They refuse the ★ arm, the differential and
the bench at a `*` over a vector's `iter()`, which legacy gives by value
where v2 gives references, and the string arm and the differential at
`Map.get_mut`, which legacy lacks. Legacy is frozen, so this is noted,
not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages, on
200,000 random pyramids six blocks wide, the widest LeetCode allows,
each with 40 to 119 random triples, counting the ones that can be built
and a checksum. The search for one such pyramid is short, so the bench
also measures making the strings and the memo. Every implementation
prints `200000 pyramids of width 6: 101341 can be built, checksum
625281034`, the Kāra program under `karac __mir-run` included (in
141 s). The C program's memo is an open-addressing hash set made per
call; Rust uses `HashSet`, Go a map and Python a set.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.18 to 0.21 s |
| Rust (`rustc -O`) | 0.71 to 0.78 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.74 to 0.82 s |
| Go | 1.11 to 1.21 s |
| Python | 19.0 to 19.7 s |
| Kāra (`karac build --mir`) | 1.73 to 1.81 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 7.0 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 1.79 s,
against C's 0.19, Rust's 0.73 (0.75 under overflow checks) and Go's
1.18. Under valgrind's cachegrind v2 runs 22.3 billion instructions
against Rust's 10.2 billion and C's 1.6 billion; C makes no string per
triple and its memo hashes with one multiply, where Rust's `HashSet` and
Kāra's `Set` both hash with SipHash. The legacy backends refuse the
program; a copy for legacy alone, with `*x` written `x` in `row_code`,
ran 1.15 to 1.24 s, a median of 1.22 s in the interleaved runs, so
v2 takes about 1.5 times legacy's time, inside M2's limit of twice
legacy. The legacy copy is a measurement only and is not in the kata,
and new katas' benches are outside M2's frozen set in any case. The
comparison with C and Rust waits until after M4.

## Compiler findings

B-2026-10-18-53 (kara ledger, open, filed from this kata): `opt ?? ""`
with `opt` an `Option[ref String]`, here `tops.get(pair) ?? ""` in the
string arm, passes `karac check`, which suggests `""` as the empty
default, but crashes on every v2 surface when `opt` is `None`: `deref of
non-reference Box` under `karac __mir-run`, a segfault under `karac
build --mir`. The string arm spells it `tops.get(pair).unwrap_or("")`,
which is right on every surface and just as natural.
