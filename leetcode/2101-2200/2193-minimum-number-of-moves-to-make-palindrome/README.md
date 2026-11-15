# 2193. Minimum Number of Moves to Make Palindrome

You are given a string `s` consisting only of lowercase English letters.

In one **move**, you can select any two **adjacent** characters of `s`
and swap them.

Return *the **minimum number of moves** needed to make* `s` *a
palindrome*.

**Note** that the input will be generated such that `s` can always be
converted to a palindrome.

```
s = "aabb"    ->  2      ("abba" or "baab")
s = "letelt"  ->  2      ("lettel" in two moves)
```

**Constraints:** `1 <= s.length <= 2000`; `s` consists only of lowercase
English letters; `s` can be converted to a palindrome using a finite
number of moves.

Greedy from the outside in: the leftmost letter keeps its place and its
nearest twin from the right end is swapped out to the end; a letter with
no twin left is the middle one, and moving it one step inward and trying
again costs no more than any other order. The same count is the number
of inversions between each letter's place and the place it takes in the
palindrome, each letter's k-th from the left paired with its k-th from
the right. O(n^2) by swaps, O(n log n) by counting inversions.

## Approaches

| file | mechanism |
|---|---|
| `moves.kara` ★ | the letters as a `Vec[u8]`, matched from the outside in; the leftmost letter's nearest twin from the right end swapped out to the end one step at a time, a letter with no twin swapped one step inward instead; O(n^2) |
| `moves_remove.kara` | the letters as a `Vec[char]` that shrinks: the first letter's last twin, found by `rposition`, costs its distance from the end and both leave by `remove`; a first letter with no twin is the middle one, costs half of what is left, and leaves alone; O(n^2) |
| `moves_struct.kara` | each letter given the place it takes in the palindrome (a letter's k-th from the left paired with its k-th from the right, the pairs laid outward in the order their left ends come, a lone letter in the middle), and the moves counted as the inversions of those places by a `struct Fenwick` that `add`s a place (`mut ref self`) and counts the places `below` one (`ref self`); O(n log n) |
| `moves_merge.kara` | the same places, found by a search from the right that skips the letters already paired, and the inversions counted by a merge sort that recurses on two halves (`own Vec[i64]`, returning the sorted half and its count); O(n log n) |
| `moves_iter.kara` | the same places worked out with iterators: a `scan` for each letter's rank among its kind, a `fold` for how many of each there are, `position` for the twin of the matching rank from the right; the inversions as `(0..n).map(..).sum()` over a `filter(..).count()`; O(n^2) |
| `moves_solution.kara` | LeetCode's Rust template: `s: String`, `-> i32`, `s.into_bytes()`, `let (mut l, mut r)`, `&&`, `struct Solution;`, `Solution::`, and the twin moved out by `s[k..=r].rotate_left(1)`; carried by `karac fix` in two rounds, the rotation written as the refusal says, and one more round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and six more
(one letter, a palindrome already, the middle letter at the front, a
palindrome twice over, a pair crossed, and pairs in the wrong halves),
each with its moves; then the moves' total and a checksum over 3000
random shuffled palindromes of 1 to 40 letters, of 2, 5 and 26 letters
in turn; then the constraints' longest, 2000 letters: of 26, of 2, and a
half followed by itself. `moves.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in two rounds of 6 and 3 edits: Rust's
spellings (`let (mut l, mut r)` to `let mut (l, r)`, `&&` to `and`,
`struct Solution;` to `struct Solution {}`, `Solution::` to `.`); then
`s.into_bytes()` to `s.bytes().to_vec()`, the counter typed `i32`, and
the adapter's widening `as i64` dropped. That leaves `s[k..=r]
.rotate_left(1)` refused: rotation is a `Vec` method in the library, and
the refusal says to `remove` the element and `insert` it at its new
place, which the arm does (`let c = s.remove(k); s.insert(r, c);`).
Rust's slices have `rotate_left`; kara B-2026-11-15-35 asks for it on a
`mut Slice`. A last round of 1 edit drops the adapter's `.clone()`,
which the call only borrows.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the fewest swaps of two adjacent letters that reach a
palindrome, found by a breadth-first search over the words one swap at
a time, with no greedy rule. It checks 300 random shuffled palindromes
of 1 to 8 letters, of 2, 3 and 4 letters in turn; then 30 palindromes as
they are; then 30 of 7 or 8 letters of 2. All 360 are drawn before any
arm answers.

| | property |
|---|---|
| P1 | the moves are the statement read literally |
| P2 | no moves exactly when the word is a palindrome already |
| P3 | the word reversed: the same moves |
| P4 | every letter c renamed to 'a' + 'z' - c: the same moves |
| P5 | one adjacent swap made first: the moves within one of these |
| P6 | each arm agrees with at least three of the other five |

P3 holds since a sequence of swaps reversed in place reaches the
reversed palindrome. P4 holds since a renaming keeps which letters are
alike. P5 holds since the swap made first can be undone by one more.

The differential prints `360 words: checksum 525551682, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python breadth-first search
over the same words. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept, three
to each Kāra arm and two to the Rust-template arm. Each kept one is
killed, fails the same way under both backends and not by a crash, and
no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the lone letter never moved | P1 43, P2 24, P3 76, P6 43 |
| M2 | ★: the twin searched from the left | P1 202, P2 68, P3 15, P6 202 |
| M3 | ★: the twin's moves never counted | P1 166, P2 147, P3 76, P6 166 |
| M8 | remove: the distance to the end one short | P1 317, P2 194, P6 317 |
| M9 | remove: the lone letter's half rounded up | P1 174, P2 85, P6 174 |
| M10 | remove: only the twin removed | P1 114, P2 38, P3 92, P5 6, P6 114 |
| M13 | struct: the lone letter at the front | P1 80, P2 37, P3 76, P6 80 |
| M14 | struct: the twin the nearest, not the last | P1 179, P2 53, P3 97, P5 4, P6 179 |
| M15 | struct: the tree's last slot never added | P1 169, P2 85, P3 48, P5 1, P6 169 |
| M18 | merge: the halves' own inversions dropped | P1 144, P2 81, P3 118, P5 15, P6 144 |
| M19 | merge: the twin searched among the used | P1 53, P2 5, P3 72, P5 5, P6 53 |
| M20 | merge: the pairs laid inward from the middle | P1 201, P2 65, P6 201 |
| M22 | iter: the twin of the same rank | P1 190, P2 190, P6 190 |
| M23 | iter: the inversions the other way | P1 317, P2 127, P6 317 |
| M25 | iter: only the pairs next to each other | P1 120, P3 41, P6 120 |
| M29 | solution: the lone letter swapped twice | P1 43, P3 76, P5 14, P6 43 |
| M30 | solution: the twin searched past the left | P1 6, P3 13, P6 6 |

P1 and P6 kill all seventeen, P2 fourteen, P3 twelve, P5 six and P4
none. No edit reads which letter is which, only whether two are alike,
so the renaming P4 makes sees nothing; it guards the arms that index by
a letter's byte (`at[b[i] - 97]`, `seen[c - 97]`). P3 reverses the word,
and misses the five edits whose wrong count is the same both ways: the
distance to the end one short (M8) and the lone letter's half rounded up
(M9), the pairs laid inward (M20), the twin of the same rank (M22) and
the inversions counted the other way (M23). P2 misses the three that
still answer 0 on a palindrome and more than 0 on every other word: only
the pairs next to each other (M25), the lone letter swapped twice (M29),
and the twin searched past the left (M30). P5, a swap made first, kills
the six edits whose count can jump by two or more for one swap.

Of the thirty, thirteen were not kept. Three are equivalent: the struct
arm's place below itself counted (M12) and the merge arm's tie counted
as an inversion (M16), since no two letters take the same place, and
the iter arm's rank read after the count goes up, less one (M21), the
same number. One crashes: the iter arm's first letter never counted
(M24), whose twin search then finds `None`. Three never finish: the ★
arm's and the template's right end held still (M4, M26) and the
template's twin left in place (M27), each of which runs past the
timeout, so none is a verdict. Six fail as a kept one does: the ★ arm's
lone letter counted twice (M5) as M29; the remove arm's twin found from
the front (M6) as M2 and its lone letter free (M7) as M1; the struct
arm's places counted below (M11) and the merge arm's inversion counted
once (M17) as M23; and the template's moves one short (M28) as M8.


## Verification

Every arm prints the same output as `moves.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the template, ★, remove, struct and merge arms
take 0.4 s to 0.9 s, and the iter arm 10 s: its twin search and its
inversion count are both quadratic closures, about 6 million calls on
the three 2000-letter words. The differential takes 1.1 s.

## Benchmarks

The bench builds 20 shuffled palindromes of 2000 letters of 26 once,
then solves 3000 times over them in turn, with the ★ arm in all five
languages, each over a copy of the word's letters. With 26 letters a
twin is seldom far from the right end, so a solve costs about 2000 x 26
steps rather than 2000^2. Every implementation prints `3000 solves:
checksum 145960885`.

BENCHTAB
