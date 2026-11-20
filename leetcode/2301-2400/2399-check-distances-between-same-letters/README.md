# 2399. Check Distances Between Same Letters

You are given a **0-indexed** string `s` consisting of only lowercase
English letters, where each letter in `s` appears **exactly twice**. You
are also given a **0-indexed** integer array `distance` of length `26`.

Each letter in the alphabet is numbered from `0` to `25` (i.e. `'a' ->
0`, `'b' -> 1`, `'c' -> 2`, ... , `'z' -> 25`).

In a **well-spaced** string, the number of letters between the two
occurrences of the `i`th letter is `distance[i]`. If the `i`th letter
does not appear in `s`, then `distance[i]` can be **ignored**.

Return `true` *if* `s` *is a **well-spaced** string, otherwise return*
`false`.

```
s = "abaccb", distance = [1,3,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]  ->  true
s = "aa",     distance = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]  ->  false
```

**Constraints:** `2 <= s.length <= 52`; `s` consists only of lowercase
English letters; each letter appears in `s` exactly twice;
`distance.length == 26`; `0 <= distance[i] <= 50`.

A letter at indexes `i < j` has `j - i - 1` letters between them, so
only the first index of each letter needs remembering.

## Approaches

| file | mechanism |
|---|---|
| `distances.kara` ★ | the first index of each letter in a `Vec` of 26; at a letter's second index the gap is checked against its entry. O(n) |
| `distances_letters.kara` | letter by letter: each of the 26 letters' first and last index found by scanning from each end, the gap checked when the letter is there. O(26 n) |
| `distances_map.kara` | a `Map[char, i64]` from each char to where it was first seen, read by `s.chars()`; the Map is only looked up, so its order never shows. O(n) |
| `distances_sort.kara` | each letter paired with its index and the pairs sorted, so a letter's two indexes sit side by side, in order. O(n log n) |
| `distances_iter.kara` | iterators: `enumerate` and `all` ask of each index that, when it is its letter's first (found by `position`), the byte `distance + 1` further on is the same letter. O(n^2) at worst, n at most 52 |
| `distances_solution.kara` | LeetCode's Rust template: a `[-1i32; 26]` of first indexes over `s.bytes().enumerate()`, each letter's slot `as usize`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; a letter
twice side by side, with 0 and with 1; every letter twice in order,
true and with `z` off by one; then 3000 random strings of 1 to 26
letters each twice, a third with true distances, a third with one
letter's off by one and a third with one letter's drawn at random, with
a checksum and the count of yes. `distances.py` mirrors the ★ arm and
its output is byte-identical, and the mirror was checked on 20000 random
strings against the statement read literally.

`distances_iter.kara` was first written with an `as` cast that changes
nothing; `karac fix` removed it, in one call of 1 edit.

`check` first reports 2 errors on the template, and `karac fix` carries
it in one call, reporting 4 edits: `struct Solution;` given its braces;
the two angle brackets of `Vec<i32>` made square; and `.iter()` put
after `s.bytes()` before `enumerate`. `[-1i32; 26]`, `as usize` and `as i32` stand as
Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every two indexes holding the same letter, the letters
strictly between them are counted one by one and compared with that
letter's distance. No first-index table. It checks 360 random strings
of 1 to 26 distinct letters, each twice, shuffled; a third with every
distance true, a third with one letter's off by one, and a third with
one letter's drawn at random. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the letters renamed one along the alphabet, and the distances with them: the same answer |
| P3 | the string reversed: the same answer |
| P4 | the distances of letters not in the string changed: the same answer |
| P5 | when the answer is yes, the first letter's distance one more: no |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a letter's name never enters its gap, P3 because
reversing the string keeps every gap, and P4 because the statement
ignores the distance of a letter that is not there.

The differential prints `360 cases: checksum 102775415, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and counts every gap. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the distance counted with one end | P1 126, P6 126 |
| M3 | ★: the first finished pair deciding yes | P1 236, P5 360, P6 236 |
| M4 | ★: every letter seen at index 0 | P1 124, P6 124 |
| M7 | letters: the first absent letter answering yes | P1 202, P2 25, P5 293, P6 202 |
| M10 | letters: z never checked | P1 12, P2 25, P5 8, P6 12 |
| M11 | letters: each letter checked against the one before's distance | P1 123, P2 1, P4 1, P5 1, P6 123 |
| M14 | map: the distances read backwards | P1 124, P2 1, P4 1, P6 124 |
| M15 | map: a gap shorter than its distance allowed | P1 109, P5 233, P6 109 |
| M16 | map: the first character skipped | P1 40, P3 49, P5 164, P6 40 |
| M17 | sort: the pairs never sorted | P1 118, P3 3, P6 118 |
| M19 | sort: a gap longer than its distance allowed | P1 127, P5 13, P6 127 |
| M20 | sort: each pair's distance by its rank | P1 120, P2 2, P6 120 |
| M23 | iter: a partner merely inside the string | P1 156, P3 20, P5 253, P6 156 |
| M24 | iter: only the first two indexes checked | P1 175, P3 73, P6 175 |
| M25 | iter: a partner past the end accepted | P1 80, P3 20, P5 44, P6 80 |
| M28 | solution: each distance read as at most 25 | P1 39, P5 1, P6 39 |
| M29 | solution: each first index one early | P1 125, P3 1, P5 15, P6 125 |

P1 and P6 kill all seventeen, P5 eleven, P3 six, P2 five and P4 two.
P4, the distances of absent letters changed, fails only the two edits
that read a letter's distance from another letter's slot (M11, M14),
once each, on a case where that slot was an absent letter's. P2, the
letters renamed, fails those and the edits that treat a letter by its
name: the first absent letter answering yes (M7), `z` never checked
(M10), and each pair's distance by its rank (M20). P3, the string
reversed, fails six (M16, M17, M23, M24, M25, M29).

Of the thirty-one, fourteen were not kept. Nine fail exactly as the ★
arm's every letter seen at index 0 (M4) does: the ★ and map arms' each
first index one late (M5, M12), the letters arm's last byte never
searched and distance counted with both ends (M8, M9), the map arm's
index never advanced (M13), the sort arm's each index halved and each
pair's first index taken for its second (M18, M21), the iter arm's each
letter checked against the next one's distance (M26), and the
template's every letter seen at index 0 (M27). The ★ arm's letter at
index 0 seen afresh and index 0 never read, and the template's letter
at index 0 seen afresh and first character skipped (M1, M6, M30, M31),
fail as the map arm's first character skipped (M16); and the iter
arm's any letter enough (M22) as the ★ arm's first finished pair
deciding yes (M3). Three edits were replaced because they too failed as
M4 does: the iter arm's partner one further and second indexes checked
instead of first, now a partner merely inside the string (M23) and only
the first two indexes checked (M24), and the template's distance
counted with both ends, now each distance read as at most 25 (M28).

## Verification

Every arm prints the same output as `distances.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.71 to 1.3 s. The differential
takes 1.5 s there and 0.66 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 1000 strings of all 26 letters, each twice, shuffled,
every other one with one letter's distance off by one, once from the
harness's generator, then makes 2000 passes, answering every string and
folding each answer plus the pass into the checksum, with the ★ arm in
all five languages. Every implementation prints `2000 passes over 1000
strings of 52 letters: checksum 293536734, 1000000 yes`. Kāra, Rust and
Python allocate the first-index table in each call; C and Go keep it in
a fixed array on the stack.

BENCHTAB
