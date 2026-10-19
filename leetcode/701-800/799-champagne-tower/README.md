# 799. Champagne Tower

Glasses stand in a pyramid: one in the first row, two in the second, and
so on up to 100 rows. Each glass holds one cup. Pour `poured` cups into
the top glass; a full glass passes whatever more it gets, half to each
of the two glasses under it. Return how full the glass at `query_glass`
in row `query_row` is, both counted from 0.

```
poured = 1,         query_row = 1,  query_glass = 1   ->  0.00000
poured = 2,         query_row = 1,  query_glass = 1   ->  0.50000
poured = 100000009, query_row = 33, query_glass = 17  ->  1.00000
```

**Constraints:** `0 <= poured <= 10^9`, `0 <= query_glass <= query_row <
100`.

## Approaches

| file | mechanism |
|---|---|
| `champagne_tower.kara` ★ | pour into the top glass and go down a row at a time, each glass with more than a cup passing half the rest to each glass under it; each row needs only the one above, and the answer is what reached the glass, capped at 1; O(r²) |
| `champagne_tower_inplace.kara` | one array for the row, moved to the next row from the right: glass `c` adds half its overflow to glass `c + 1`, which already holds what came from its right, and keeps the other half as the new glass `c`; O(r²) |
| `champagne_tower_grid.kara` | the whole triangle down to `query_row`, each glass's overflow poured into the two under it, top to bottom; O(r²) time and space |
| `champagne_tower_memo.kara` | what reaches a glass is half the overflow of the glass above it on the left plus half that of the one above on the right, asked from the queried glass up and kept in a map so no glass is worked out twice; O(r²) |
| `differential.kara` | the four arms against the definition, four properties |

All four do the same additions of the same halves, so they give the same
doubles, not merely close ones, and print alike. Every arm prints the
same 11 lines, each answer to five decimals: LeetCode's three examples;
nothing poured; one cup and the top glass; four cups and the middle and
edge of the third row; 25 cups and the edge of row 6, which none
reaches; 10^9 cups and the edge of row 99, LeetCode's deepest, which
none reaches either, as the edges pass on ever less and stop being full,
and its middle, which is full; and 300 random questions, half with up to
199 cups and half up to 10^9, with the answers added up and a checksum.
`champagne_tower.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition, in
whole numbers. Down to row 20 every amount is a whole number of 2^-20
cups, so the definition pours in those units, where halving is exact;
the answer has a power of two below and fewer than 53 bits, so it
converts to the very double the arms should reach. Its 1,600 cases ask
about a glass down to row 15 in four kinds of 400: up to 20 cups; about
as much as fills the rows above the asked one, so that its glasses are
part full; up to 1,000 cups and a glass in row 10 or below; and just
enough to fill the first `k` rows, `k (k + 1) / 2` cups, give or take
one.

| | property |
|---|---|
| P1 | the definition's amount, to the bit |
| P2 | the tower is the same in a mirror: glass `c` and glass `row - c` hold alike |
| P3 | one cup more takes nothing from any glass |
| P4 | the glasses down to a row hold no more than was poured, and all of it when nothing reaches the row below |

It prints `1600 cases (688 glasses full, 185 part full), 4 arms, 25600
checks, 0 failures` under `karac __mir-run` and `karac __mir-llvm-run`,
and the same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: all the overflow passed to the left | P1 753, P2 434 |
| M2 | ★: a full glass keeping nothing | P1 403, P4 788 |
| M3 | ★: the answer not capped at 1 | P1 670, P4 1390 |
| M4 | in-place: a glass not emptied after pouring | P1 495, P2 504, P4 876 |
| M5 | in-place: a glass holding half a cup | P1 415, P4 825 |
| M6 | in-place: the last glass of a row not poured from | P1 408, P2 570, P4 711 |
| M7 | grid: the whole overflow passed to each glass | P1 629, P4 827 |
| M8 | grid: the last row not poured into | P1 756, P4 1390 |
| M9 | grid: a glass short of full passing on what it lacks | P1 245, P3 43, P4 576 |
| M10 | memo: the glass above on the left read as the one above | P1 330, P2 383 |
| M11 | memo: a glass past the end of a row asked about | P1 333, P2 364, P4 767 |
| M12 | memo: the kept amounts looked up by row alone | P1 272, P2 259, P4 708 |

P1 kills all twelve. P4 kills the ten that lose or make champagne, and
misses the two that only send it the wrong way: all of a glass's
overflow passed to the left, and a glass reading the glass above on its
right in place of the one on its left, which P2 sees as a lopsided
tower. P2 kills six, the edits that treat the two sides unlike each
other. P3 kills only the glass short of full that passes on what it
lacks: its pours below can be less than nothing, so more champagne above
can leave less in a glass below.

## Verification

Every arm prints the same output as `champagne_tower.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`e6919e6fcc`, which is its last compiler change. The runtime archives
were built after the last runtime change, `216d20e28a`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept the ★, in-place and grid arms and the
bench program unchanged and print the same output under the legacy
interpreter (`karac run --interp`), the legacy JIT (`karac run`), `karac
build` and an auto-par build. Legacy's checker refuses the memo arm and
the differential for the `*` on the amount found in the map, which it
takes as a copied `f64`; copies without it print the same output under
all four. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 4,096 questions
are made once: up to 10^9 cups, LeetCode's most, poured into a tower and
a glass asked about in rows 50 to 99, the deepest LeetCode allows. Each
of 81,920 rounds answers the next question, adding up the answers. Every
implementation prints `81920 glasses: 50950.25387 cups in all, checksum
812476325`, the Kāra program under `karac __mir-run` included (in 224
s).

The bench measures short loops of floating-point work over rows of up to
100 glasses, with an allocation for each row. Spot timings on a shared
4-core container, eight runs of each compiled program, five of them
interleaved, and two of Python (`bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.54 to 1.68 s |
| Rust (`rustc -O`) | 1.54 to 1.64 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.53 to 1.65 s |
| Go | 1.09 to 1.31 s |
| Python | 20.57 to 20.80 s |
| Kāra (`karac build --mir`) | 1.88 to 2.12 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, which this kata measures now that legacy is frozen;
that edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 5.4 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 2.01 s,
against C's 1.59, Rust's 1.60 (1.57 under overflow checks) and Go's
1.16. Under valgrind's cachegrind v2 runs 11.3 billion instructions and
2.28 billion branches, mispredicting 82 million, against C's 5.14
billion, 0.86 billion and 29 million and Rust's 5.46 billion, 0.91
billion and 32 million. The legacy build of the same program ran 1.50 to
1.60 s, a median of 1.53 s in the interleaved runs, so v2 takes 1.31
times legacy. The comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new in v2.
