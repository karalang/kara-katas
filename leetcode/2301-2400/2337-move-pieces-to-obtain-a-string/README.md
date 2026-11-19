# 2337. Move Pieces to Obtain a String

You are given two strings `start` and `target`, both of length `n`.
Each string consists **only** of the characters `'L'`, `'R'`, and `'_'`
where:

- The characters `'L'` and `'R'` represent pieces, where a piece `'L'`
  can move to the **left** only if there is a **blank** space directly
  to its left, and a piece `'R'` can move to the **right** only if there
  is a **blank** space directly to its right.
- The character `'_'` represents a blank space that can be occupied by
  **any** of the `'L'` or `'R'` pieces.

Return `true` *if it is possible to obtain the string* `target` *by
moving the pieces of the string* `start` ***any** number of times*.
Otherwise, return `false`.

```
start = "_L__R__R_", target = "L______RR"   ->  true
start = "R_L_", target = "__LR"             ->  false
start = "_R", target = "R_"                 ->  false
```

**Constraints:** `n == start.length == target.length`;
`1 <= n <= 10^5`; `start` and `target` consist of the characters `'L'`,
`'R'`, and `'_'`.

A move takes a piece into a blank beside it, so pieces never pass each
other: the start's pieces, blanks skipped, must be the target's, letter
for letter in the same order. Matched in that order, each `L` can only
have gone left and each `R` right, so each `L` must stand no later in
the target than in the start, and each `R` no earlier. Those conditions
are also enough: moving the `L`s into place from the first and then the
`R`s from the last never meets a piece in the way.

## Approaches

| file | mechanism |
|---|---|
| `pieces.kara` ★ | two indices walk the two strings' `bytes()` together, each skipping blanks, and each pair of pieces is held to the same letter, an `L` no later in the target and an `R` no earlier. O(n) |
| `pieces_lists.kara` | each string's pieces listed as (letter, place) pairs, the lists held to the same length and compared pair by pair. O(n) |
| `pieces_counts.kara` | counts over prefixes: the pieces compared with blanks `replace`d away, then every prefix of the target held to at least as many `L`s as the start's, and every prefix of the start to at least as many `R`s as the target's. O(n) |
| `pieces_moves.kara` | the moves made: each piece matched to the target's piece of the same rank, the `L`s walked left one blank at a time from the first, the `R`s right from the last, and the result compared with the target. O(n^2) at worst |
| `pieces_iter.kara` | iterators: each string's pieces with their places from `enumerate` and `filter`, the lengths compared, and the pairs from `zip` held by `all` to the rules. O(n) |
| `pieces_solution.kara` | LeetCode's Rust template: the strings read through `as_bytes()`, a tuple of `mut` indices, `\|\|` and `&&` conditions and byte literals; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples; only
blanks; an `L` and an `R` that would have to pass each other; an `L`
asked to move right; 2000 places moved 100000 times by allowed moves,
then with one blank turned into a piece; then 2000 random cases of 1 to
10 places, the target half the time the start moved 0 to 20 times and
otherwise drawn on its own, with a checksum and how many are reachable.
`pieces.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one call, reporting 14 edits.
`check` first reports 11 errors and offers 12 edits for them: the tuple
pattern `(mut i, mut j)` to `mut (i, j)`, three edits, since `mut` goes
before a whole pattern; the two `||` to `or` and the five `&&` to
`and`; `struct Solution;` to `struct Solution {}`; and `Solution::` to
`Solution.` in the harness's wrapper. The other two follow from those:
the two `as_bytes()` to `bytes()`. The byte literals `b'_'`, `b'L'`
and `b'R'` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every string the start can become, found by trying each
allowed move, an `L` one place left into a blank or an `R` one place
right into one, from every string found until no new one appears, kept
in a `Set[String]`; the answer is whether the target is among them. No
matching of pieces. It checks 300 random cases of 1 to 8 places, the
target half the time the start moved 0 to 20 times by allowed moves;
then 30 of up to 40 places, three in four blank; then 30 of up to 2000
places, the target the start moved up to 100000 times. All 360 are
drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 8 places, the answer is the literal reading's |
| P2 | the start to itself: true; and true only for the same pieces in the same order |
| P3 | both strings reversed with `L` and `R` swapped: the same answer |
| P4 | where true, the target moved on by allowed moves: still true |
| P5 | true both ways only for equal strings |
| P6 | each arm agrees with at least three of the other five |

P3 holds because reversing a string turns every `L` move into an `R`
move and back. P4 is the moves' composition, and P5 holds because a
move only ever takes an `L` left or an `R` right, so two strings each
reachable from the other can differ in no piece's place.

The differential prints `360 cases: checksum 274437596, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
builds the same cases and the same set of reachable strings. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: an `R` allowed to move left | P1 1, P3 3, P5 54, P6 2 |
| M3 | ★: the letters never compared | P1 18, P2 18, P4 2, P5 14, P6 18 |
| M5 | ★: an `L` held to its place | P1 49, P3 92, P4 9, P6 79 |
| M7 | lists: a blank given no place | P1 2, P5 134, P6 3 |
| M8 | lists: an `L` held to moving right | P1 50, P3 94, P4 9, P6 80 |
| M11 | lists: the first pair skipped | P1 14, P2 12, P3 6, P5 56, P6 14 |
| M12 | counts: the pieces never compared | P1 50, P2 52, P3 97, P6 52 |
| M15 | counts: an `L` counted in the start as an `R` | P1 87, P2 225, P3 117, P5 4, P6 127 |
| M16 | counts: the first place never counted | P1 46, P3 60, P4 17, P6 58 |
| M17 | moves: the `L`s walked from the last | P1 8, P3 24, P4 5, P6 38 |
| M18 | moves: the `R`s walked from the first | P1 7, P3 24, P4 7, P6 44 |
| M19 | moves: an `R` stopping one short | P1 49, P3 92, P4 15, P6 91 |
| M22 | iter: the lengths never compared | P1 35, P2 39, P3 23, P5 28, P6 39 |
| M23 | iter: an `L` allowed anywhere | P1 1, P3 3, P5 41, P6 1 |
| M24 | iter: an `R` held to moving left | P1 50, P3 94, P4 15, P6 92 |
| M27 | solution: the walk stopped when either string runs out | P1 2, P2 2, P3 6, P6 2 |
| M29 | solution: the start's blanks never skipped | P1 148, P2 315, P6 190 |

P1 and P6 kill all seventeen, P3 fourteen, P4 eight, and P2 and P5
seven each. P3, the strings mirrored, fails wherever an edit treats `L`
and `R` unalike, and misses only the three that touch neither: the
letters never compared, a blank given no place, and the start's blanks
never skipped. P2 fails where an edit lets through pieces that differ in
letter or number, or refuses the start against itself: the letters,
the lengths or the pieces never compared, the first pair skipped, an
`L` counted as an `R`, the walk stopped early, the blanks never
skipped. P5, true both ways only for equal strings, fails where an
edit lets a piece go back the way it came: an `R` moved left, an `L`
anywhere, the letters or lengths never compared, the first pair
skipped. P4, the target moved on by allowed moves, fails where an edit
holds a piece to too narrow a rule, so that a further allowed move
turns a true into a false: an `L` held to its place or to moving right,
an `R` held to moving left or stopping one short, the moves made in
the wrong order, the first place never counted.

Of the thirty-one, fourteen were not kept. One is equivalent and killed
by nothing: the moves arm's `L` walked left over an `R` (M21). Where it
meets one, the unmutated `L` stops short of its place and never moves
again, so the answer is false; the mutated one writes over the `R` and
leaves a piece fewer than the target has, so the answer is false too. An `L`
allowed to move right fails alike in the ★ (M1), iter (M23) and
template (M28) arms; one string running out taken as a match in the ★
(M4), iter (M22) and template (M30); and the target's blanks never
skipped in the ★ arm (M6) as the iter arm's kept as pieces (M26) and
the template's start's blanks never skipped (M29). The letters never
compared in the lists (M9) and iter (M25) arms fail as the ★ arm's
(M3); the `R`s never checked in the lists (M10) and counts (M14) arms
as the ★ arm's `R` allowed to move left (M2); the counts arm's `L`
counts read the wrong way (M13) as the lists arm's `L` held to moving
right (M8); the moves arm's `L` stopping one short (M20) as the ★ arm's
`L` held to its place (M5); and the template's `R` held to the `L`'s
rule (M31) as the iter arm's `R` held to moving left (M24).

## Verification

Every arm prints the same output as `pieces.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.3 to 0.4 s. The differential
takes 3.3 s there, most of it the literal reading's set of every string
reachable, and 0.6 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 pairs of `10^5` places once: the start from a
scramble that never repeats, an `L` in 4 and an `R` in 4; the target
the start after 3 rounds of every `L` moved one left into a blank,
first to last, and every `R` one right, last to first; and in every
other pair the target's first piece turned to the other letter. It
then makes 10 passes, pass `p` folding each answer plus `p` into the
checksum, with the ★ arm in all five languages. Every implementation
prints `10 passes over 10 pairs of 10^5 places: checksum 629870366`.
Each walks the strings as bytes, or in Python as one-character
strings; nothing is allocated in the walk.

BENCHTAB
