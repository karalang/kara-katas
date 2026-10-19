# 771. Jewels and Stones

Given a string `jewels` of the kinds of stone that are jewels and a
string `stones` of the stones you have, each a letter, count the stones
that are jewels. Letters are case-sensitive, so `a` and `A` are
different kinds.

```
jewels = "aA", stones = "aAAbbbb"   ->  3
jewels = "z",  stones = "ZZ"        ->  0
```

**Constraints:** both strings have from 1 to 50 letters, English letters
only, and the letters of `jewels` are all different.

## Approaches

All four arms mark the jewels' letters and then count the stones that
are marked; they differ in how they mark.

| file | mechanism |
|---|---|
| `jewels_and_stones.kara` ★ | a `Set[char]` of the jewels, then a lookup for each stone |
| `jewels_and_stones_table.kara` | a table of 128 flags indexed by the letter's byte |
| `jewels_and_stones_mask.kara` | a mask of 52 bits in an `i64`, one for each letter, a to z and then A to Z; each stone adds its bit shifted down to bit 0 |
| `jewels_and_stones_scan.kara` | for each stone, `any` over the jewels' letters, O(j times s), which LeetCode's 50 letters allow |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 8 lines: LeetCode's two examples; empty stones
and empty jewels; a letter in both cases; all 52 letters as jewels; a
repeated jewel; then 300 random pairs of up to 50 letters each, drawn
from a random number of the 52, with the total count and a checksum.
Empty strings and repeated jewels, which also turn up in many of the
random pairs, are outside LeetCode's constraints; every arm handles them
as the definition does. `jewels_and_stones.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
the number of places in the stones whose letter equals some jewel's,
found by comparing every pair. Its 2,000 random pairs are drawn as in
the harness, with a third string of stones for P3; the jewels may repeat
a letter, as there, which P4 relies on.

| | property |
|---|---|
| P1 | the count is the definition's |
| P2 | every letter's case swapped, in both strings, changes nothing |
| P3 | more stones joined on add their own count |
| P4 | the jewels followed by themselves reversed, and the stones reversed, change nothing |

It prints `2000 pairs (29328 jewels), 4 arms, 32000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error; the total is the ★ arm's.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each kind of jewel counted once | P1 1528, P3 1641 |
| M2 | ★: the first jewel left out | P1 414, P4 414 |
| M3 | ★: the stones that are not jewels counted | P1 1906 |
| M4 | table: a jewel marked in lower case | P1 1661, P2 1683 |
| M5 | table: a stone looked up in lower case | P1 1233, P2 1516 |
| M6 | table: a repeated jewel unmarks itself | P1 1418, P4 1794 |
| M7 | mask: upper and lower case sharing a bit | P1 1393 |
| M8 | mask: a repeated jewel clears its bit | P1 1418, P4 1794 |
| M9 | mask: two bits read for each stone | P1 1772, P2 17 |
| M10 | scan: a stone counted if any jewel differs | P1 1549 |
| M11 | scan: the first stone left out | P1 1187, P3 1128, P4 569 |
| M12 | scan: a stone counted only if every jewel matches | P1 1846 |

P1 kills all twelve; the others show what kind of mistake each is.
P2, which swaps every letter's case, sees M4 and M5, which fold one side
to lower case only. M7 gives a letter's two cases one bit, which
swapping case cannot see, and M9's second bit belongs to the next letter
in the order a to z, A to Z, a relation swapping case keeps except after
z, so P2 caught it 17 times. P3 sees the edits that count a stone by its
place rather than its letter: M1 counts each kind of jewel once and
M11 skips the first stone, so joined stones count differently from their
parts. P4 sees M6 and M8, where a repeated jewel undoes itself and a
doubled list undoes every jewel, so the two fail on the same pairs;
M2, whose skipped first jewel is the doubled list's last; and M11 again,
whose skipped stone is the last one once the stones are reversed.
M3, M10 and M12 count the wrong stones in a way all three other
properties keep. No first choice survived.

## Verification

Every arm prints the same output as `jewels_and_stones.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`4f079681eb`, whose last compiler change is `ecb1a0322e`. The runtime
archives were built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept all four arms and, through a copy, the
bench. Each arm prints the same output under the legacy JIT (`karac
run`), `karac build` and an auto-par build, each build with a warning
that a borrowed `jewels` is used after a move, since legacy predates
borrowed parameters. The legacy interpreter prints a different random
line, 4161 jewels and checksum 276664549: in `random_letters(mut seed,
next_random(mut seed) % 51, kinds)` it passes the first argument as
`seed` was before the second advanced it, which a small program shows,
where `take(mut seed, bump(mut seed))` sees 0 under the legacy
interpreter and 1 everywhere else. Both legacy backends refuse the
differential at `is_ascii_lowercase`, which they have no handler for.
Legacy refuses the bench at `num_jewels_in_stones(jewels[k],
stones[k])`, as a move out of an index; its timing below is of a copy
whose parameters are `ref String`. Legacy is frozen, so all this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 256 random pairs
of 50 jewels and 50 stones, LeetCode's limit, drawn from all 52 letters,
are built once; each of 1,000,000 rounds counts the next pair and folds
the count into a checksum. Every implementation prints `1000000 rounds
of 50 jewels and 50 stones: 31054702 jewels in all, checksum
597854238`, the Kāra program under `karac __mir-run` included (in
155 s). Kāra's `Set` and Rust's `HashSet` both hash with SipHash-1-3; Go
uses its own map hash, Python its own hash of a string, and C a small
open-addressing table with FNV-1a.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.29 to 0.40 s |
| Rust (`rustc -O`) | 2.13 to 2.27 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.22 to 2.41 s |
| Go | 3.13 to 3.64 s |
| Python | 3.98 to 4.46 s |
| Kāra (`karac build --mir`) | 3.32 to 4.28 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
29.8 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 3.87 s,
against C's 0.31, Rust's 2.22 (2.29 under overflow checks) and Go's
3.44, and Python, at 3.98 to 4.46 s, takes about as long as v2. Under
valgrind's cachegrind v2 runs 32.9 billion instructions, Rust
17.8 billion and C 1.6 billion. Each round builds a hash set of
50 letters and looks up 50 more, so the time is hashing: Kāra's `Set`
and Rust's `HashSet` run SipHash-1-3 on every letter, C's FNV-1a is four
multiplies, and Python's one-letter strings are shared objects whose
hashes are computed once and kept. The legacy build of the copy ran
3.31 to 3.67 s in seven runs, a median of 3.48 s in the interleaved
ones, so v2 takes 1.1 times legacy, inside M2's limit of twice legacy;
new katas' benches are outside M2's frozen set in any case. The
comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new.
