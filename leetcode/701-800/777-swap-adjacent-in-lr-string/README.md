# 777. Swap Adjacent in LR String

In a string of the letters `L`, `R` and `X`, a move replaces one
occurrence of `"XL"` with `"LX"`, or one occurrence of `"RX"` with
`"XR"`. Given `start` and `end`, return whether some sequence of moves
turns `start` into `end`.

```
start = "RXXLRXRXL", end = "XRLXXRRLX"  ->  true
start = "X", end = "L"                  ->  false
```

**Constraints:** both strings have 1 to 10,000 letters, the same number,
and every letter is `L`, `R` or `X`.

## Approaches

A move takes an L one place left through an X, or an R one place right,
and no letter ever passes another. So `end` can be reached exactly when
the two strings hold the same letters in the same order once the X's are
left out, each L at the same place in `end` or further left, and each R
at the same place or further right. The arms test that in four ways.

| file | mechanism |
|---|---|
| `swap_adjacent_in_lr_string.kara` ★ | two pointers: walk both strings skipping X's, and compare each pair of letters, their kinds and their places; O(n), O(1) space |
| `swap_adjacent_in_lr_string_prefix.kara` | the strings with the X's taken out compared, then every prefix of `end` must hold at least as many L's as the same prefix of `start` and at most as many R's; O(n) |
| `swap_adjacent_in_lr_string_balance.kara` | one pass with two balances: an R of `start` is owed to `end` until `end`'s R arrives, an L of `end` is owed to `start` until `start`'s arrives, and nothing may cross an owed letter; O(n), O(1) space |
| `swap_adjacent_in_lr_string_positions.kara` | each string's letters listed with their places, then the two lists compared item by item; O(n) time and space |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 13 lines: LeetCode's two examples and eight
other short pairs, among them an L moved left past several X's, an L
moved right, an R and an L that would have to pass each other, and each
legal one-place move; a string of 10,000 letters, LeetCode's limit,
against itself after 400,000 random legal moves, and against itself with
an L moved a place right; then 300 random pairs of 1 to 40 letters, half
of them an end reached by legal moves and half random, with how many are
reachable and a checksum. `swap_adjacent_in_lr_string.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every string reachable from `start`, found breadth first by making each
move wherever it fits, and `end` among them. Its 1,500 random pairs are
1,300 of 1 to 8 letters and 200 of 9 to 200. A quarter of the ends are
reached by legal moves, a quarter are such an end with any two
neighbours then swapped, a quarter are `start`'s letters shuffled and a
quarter are random. The definition answers the small pairs; on the large
ones the ★ arm's answer stands in for it, and P2 to P4 still apply.

| | property |
|---|---|
| P1 | the answer is the definition's (small pairs) |
| P2 | both strings turned end for end, with every L made an R and every R an L, give the same answer |
| P3 | `end` to `start`, with L and R swapped, gives the same answer: a move undone is the other letter's move |
| P4 | moves compose: `start` after more legal moves reaches `end` only if `start` does, and if `start` reaches `end` it reaches `end` after more moves |

It prints `1500 pairs (853 reachable), 4 arms, 23200 checks, 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an L allowed only rightwards | P1 214, P2 374, P3 374, P4 111 |
| M2 | ★: letters left over in one string ignored | P1 118, P2 41 |
| M3 | ★: the paired letters' kinds not compared | P1 111, P3 50, P4 22 |
| M4 | prefix: the letters' order not compared | P1 154, P2 171 |
| M5 | prefix: L's counted the wrong way | P1 214, P2 374, P3 374, P4 111 |
| M6 | prefix: the R counts not checked | P1 45, P2 105, P3 105 |
| M7 | balance: an R in `start` may cross an owed L | P1 6, P2 12, P3 16, P4 3 |
| M8 | balance: an R in `end` that nothing owes accepted | P1 44, P2 108, P3 108, P4 1 |
| M9 | balance: R's still owed at the end ignored | P1 18, P2 49, P3 39 |
| M10 | positions: the letters' kinds not compared | P1 111, P3 50, P4 22 |
| M11 | positions: an R that stays put refused | P1 294, P2 278, P3 278 |
| M12 | positions: an L allowed one place right | P1 32, P2 64, P3 64 |

P1 kills all twelve. P3 turns every test an arm makes of an L into the
same test of an R, so it sees the mutants that treat the two letters
differently, which is all but M2 and M4: those two are as blind to an
L's direction as to an R's, and P3 maps each to itself. P2 sees them,
since turning the strings end for end moves the letters M2 leaves over
to the front, where the walk meets them, and turns the prefix counts M4
relies on into suffix counts, which disagree with them when the letters
are out of order. M7 is the weakest kill: its wrong answers need an L
owed to `start` with an R of `start` inside that gap, which the
differential rarely met until the shuffled ends were added for it. The
count of reachable pairs differs under M1 to M3 because the large pairs
take their expected answer from the ★ arm.

## Verification

Every arm prints the same output as `swap_adjacent_in_lr_string.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and under `karac __mir-llvm-asan` (AddressSanitizer)
with no error; the differential prints its line under all three. `karac
check` passes all four arms, the differential and the bench program. The
debug build that runs `__mir-llvm-run`, `__mir-llvm-asan` and `build
--mir` and the release build that runs `check` and `__mir-run` are both
at kara `4f079681eb`, whose last compiler change is `ecb1a0322e`. The
runtime archives were built after the last runtime change,
`176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept all four arms. Under the legacy JIT
(`karac run`), `karac build` and an auto-par build every arm prints the
same output, each build with a warning that a borrowed `start` is used
after a move, since legacy predates borrowed parameters. The legacy
interpreter (`karac run --interp`) prints `300 random pairs: 151
reachable, checksum 78842522` as the last line, a different set of
pairs: in `random_text(mut seed, n, 1 + next_random(mut seed) % 3)` it
passes the first argument as `seed` was before the third advanced it,
the behaviour katas 771 and 775 note. With the third arguments of that
call and of `moved` computed into names first, it prints the same
output. For the same reason it prints the differential's line with 865
reachable pairs and 0 failures. The legacy `karac build` refuses the
differential at `text.chars().rev()`, a chain its codegen does not
support, and the bench at `can_transform(starts[g], ends[g])`, as a move
out of an index; the bench timing below is of a copy whose parameters
are `ref String`. Legacy is frozen, so all this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 pairs of
10,000 letters, LeetCode's limit, are built once: each `start` is random
with half its letters X's; half the ends are the start after 100,000
random legal moves, a quarter the start with its last `"XR"` turned into
`"RX"`, an R moved left, and a quarter the same at a random `"XR"`. Each
of 20,000 rounds answers the next pair. Every implementation prints
`20000 rounds of 10000 letters: 10000 reachable, checksum 961765103`,
the Kāra program under `karac __mir-run` included (in 289 s).

The checks are a branch on each letter, X or not, and on random letters
those branches cannot be predicted: under valgrind's cachegrind each of
C, Rust and v2 mispredicts 137 million branches, about one for every
three letters read, and that sets the time far more than the
instructions do. Spot timings on a shared 4-core container, eight runs
of each compiled program, five of them interleaved, and three of Python
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.49 to 1.71 s |
| Rust (`rustc -O`) | 1.50 to 1.70 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.53 to 1.69 s |
| Go | 1.78 to 2.08 s |
| Python | 25.5 to 27.4 s |
| Kāra (`karac build --mir`) | 1.52 to 1.66 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 5.4 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 1.60 s,
against C's 1.51, Rust's 1.56 (1.66 under overflow checks) and Go's
1.93. Cachegrind counts 4.67 billion instructions for v2, 4.32 billion
for Rust and 3.45 billion for C, and 1.75 billion branches for v2
against C's 1.05 billion, but the extra branches are predicted. The
legacy build of the copy ran 1.52 to 1.75 s, a median of 1.59 s, so v2
takes 1.01 times legacy. The comparison with C and Rust waits until
after M4.

## Compiler findings

Nothing new.
