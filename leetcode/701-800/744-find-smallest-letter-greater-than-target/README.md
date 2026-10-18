# 744. Find Smallest Letter Greater Than Target

Given `letters`, a list of lowercase letters sorted in non-decreasing
order, and a lowercase letter `target`, return the smallest letter in
`letters` that is greater than `target`. If there is none, return the
first letter of `letters`.

```
letters = [c, f, j], target = a     ->  c
letters = [c, f, j], target = c     ->  f
letters = [x, x, y, y], target = z  ->  x
```

**Constraints:** 2 to 10,000 letters, all lowercase, sorted in
non-decreasing order, at least two of them different; `target` is a
lowercase letter.

## Approaches

The letters greater than the target form a suffix of the sorted list, so
the answer is the start of that suffix, or the first letter when it is
empty. The arms take the letters as a `Vec[char]`.

| file | mechanism |
|---|---|
| `next_greatest_letter.kara` ★ | binary search for the first index whose letter is greater than the target, wrapping to the first letter when there is none; O(log n) |
| `next_greatest_letter_scan.kara` | walk from the left and return the first letter greater than the target, or the first letter; O(n) |
| `next_greatest_letter_table.kara` | mark which of the 26 letters occur, then try the letters after the target in turn, past `z` from `a` again, so the wrap needs no special case; O(n + 26) |
| `next_greatest_letter_least.kara` | one pass that does not trust the order: keep the least letter greater than the target and the least letter of all, and return the first if there is one; O(n) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 11 lines: the three LeetCode examples; the
first example's list with two targets between its letters and one on its
last letter; a target past both letters of a two-letter list; a target
just below `z`; runs of equal letters; every target from `a` to `z` on a
random sorted list of 10,000 letters, as the 26 answers; and 300 random
lists of 2 to 12 letters, with how many answers wrap round and a
checksum. `next_greatest_letter.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which asks for each letter after the target in turn, up to `z`, whether
the list holds it, and otherwise returns the first letter. 3,000 random
lists are checked, each of 2 to 8 sorted letters starting anywhere from
`a` to `s` and stepping up one letter about half the time, at least two
of them different, with any target; in 1,700 of them the answer wraps
round.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | every letter and the target moved up by the same number of places, as many as keeps them at `z` or below, move the answer up with them |
| P3 | every letter written twice gives the same answer |
| P4 | the target itself added to the list where it sorts gives the same answer |

It prints `3000 lists (1700 wrapping round), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a letter equal to the target counted as greater | P1 375, P4 2625 |
| M2 | ★: the wrap going to the last letter, not the first | P1 1700, P4 1589 |
| M3 | ★: the search never looking at the last letter | P1 1700, P4 1589 |
| M4 | scan: a letter equal to the target counted as greater | P1 375, P4 2625 |
| M5 | scan: the wrap going to the second letter | P1 981, P3 981 |
| M6 | scan: the last letter returned once one greater is seen | P1 1157 |
| M7 | table: the target itself tried first | P1 375, P4 2625 |
| M8 | table: the wrap taken past 'y', not past 'z' | P1 3, P2 10 |
| M9 | table: the target taken as the letter after it | P1 376 |
| M10 | least: the wrap going to the largest letter | P1 1700, P4 1589 |
| M11 | least: the largest greater letter kept, not the smallest | P1 1157 |
| M12 | least: a letter equal to the target counted as greater | P1 375, P4 2625 |
| E1 | ★: the midpoint as (lo + hi) / 2 | 0 |
| E2 | table: the fallback after the loop returning 'a' | 0 |
| E3 | least: the starting best the second letter | 0 |

P1 kills all twelve. M1, M4, M7 and M12 are one mistake in four arms, a
letter equal to the target counted as greater (in the table arm by
trying the target itself first), and fail exactly the same checks;
P4 sees them on most lists, since the target added to the list is then
an answer whenever it was not one already. M2, M3 and M10 send the wrap
to the last letter rather than the first and also fail the same checks:
M3 does so because a search that never looks at the last letter ends on
it when every other letter is at or below the target, and returns it
unchecked. P4 sees those three because in a list that wraps the added
target becomes the last letter. M5 wraps to the second letter, and
P3 sees it because written twice the second letter is a copy of the
first. M6 and M11 return the largest letter greater than the target,
which none of P2 to P4 moves. M8 goes wrong only at the end of the
alphabet, when the answer is `z` or the target is `z` and the list holds
`a`, which few random lists call for: P1 sees 3 lists and P2, which can
move lists up to `z`, 10. M9 answers for the letter after the target,
which the properties keep consistent. E1 computes the midpoint as `(lo +
hi) / 2`, the same for lists this short; E2 changes the table's fallback
after its loop, which is never reached, since the 26 tries include every
letter, the target's own; E3 starts the best at the second letter, which
is never read before a greater letter replaces it.

## Verification

Every arm prints the same output as `next_greatest_letter.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`1d96cab833`, whose last compiler change is `afe886a96d`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept the ★ arm and the bench program: the ★
arm prints the same output under the legacy interpreter, `karac run`,
`karac build` and an auto-par build. They refuse the other three arms
and the differential at type checking, at a `*` over a vector's `iter()`
(`*c` over the letters), since legacy gives those by value where
v2 gives references. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. In each of
60 rounds it makes a sorted list of 10,000 letters, starting at one of
`a` to `f` and stepping up one letter about one time in 500, and asks
for 100,000 random targets, 6 million queries in all, adding up the
answers' character codes. The letters are a growable array of
characters, as the ★ arm's are: `char` in Rust and Kāra, `rune` in Go,
one-character strings in Python, and plain bytes in C. Every
implementation prints `60 rounds of 100000 queries on 10000 letters:
answers sum to 643916634`, the Kāra program under `karac __mir-run`
included (in 28 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.27 to 0.32 s |
| Rust (`rustc -O`) | 0.19 to 0.22 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.22 to 0.35 s |
| Go | 0.22 to 0.30 s |
| Python | 7.4 to 8.0 s |
| Kāra (`karac build --mir`) | 0.34 to 0.37 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
2.1 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes a fifth
longer than C (0.35 s against 0.29), 1.75 times as long as Rust
(0.20) and a quarter longer than Rust under overflow checks (0.28), and
it is behind Go (0.25). Under valgrind's cachegrind it runs 1.5 billion
instructions against C's 1.2 and Rust's 1.1, and 0.35 billion branches
against 0.17 and 0.26, but mispredicts only 7 million of them against
C's 35 and Rust's 38: the binary search's comparison is a branch in C
and Rust, a coin toss for a random target, and v2's few mispredictions
suggest it takes each step without one (inferred, not read from its
code). Why v2 is still the slower was not traced. The legacy build of
the same program ran 0.30 to 0.35 s in the interleaved runs, a median of
0.31 s, so v2 takes 1.1 times as long as legacy, inside M2's limit of
twice legacy; new katas' benches are outside M2's frozen set in any
case. The comparison with C and Rust waits until after M4.

## Compiler findings

None new.
