# 2109. Adding Spaces to a String

You are given a 0-indexed string `s` and a 0-indexed integer array
`spaces` that describes the indices in the original string where spaces
will be added. Each space should be inserted before the character at
the given index.

For example, given `s = "EnjoyYourCoffee"` and `spaces = [5, 9]`, we
place spaces before `'Y'` and `'C'`, which are at indices 5 and 9
respectively. Thus, we obtain `"Enjoy Your Coffee"`.

Return the modified string after the spaces have been added.

```
s = "LeetcodeHelpsMeLearn", spaces = [8,13,15]   ->  "Leetcode Helps Me Learn"
s = "icodeinpython", spaces = [1,5,7,9]          ->  "i code in py thon"
s = "spacing", spaces = [0,1,2,3,4,5,6]          ->  " s p a c i n g"
```

**Constraints:** `1 <= s.length <= 3 * 10^5`; `s` consists only of
lowercase and uppercase English letters; `1 <= spaces.length <= 3 *
10^5`; `0 <= spaces[i] <= s.length - 1`; all the values of `spaces` are
strictly increasing.

The places are sorted, so one walk over the letters with a second index
into `spaces` meets each space just before its letter. Inserting into
the string one space at a time instead moves the rest of it each time,
O(n * k), which at the constraints' largest is 9 * 10^10 moves.

## Approaches

| file | mechanism |
|---|---|
| `spaces.kara` ★ | one walk over `chars().enumerate()` with an index into `spaces`, the space pushed first when it is due, into a `String.with_capacity(n + k)`. O(n + k) |
| `spaces_slices.kara` | the pieces between spaces sliced out with `s[last..p]` and the rest with `s[last..]`, put back together with `join(" ")` |
| `spaces_bytes.kara` | the `bytes()` copied into a `Vec[u8]` with `b' '` pushed before each byte whose place is due, in a `while`, then `String.from_utf8(..).unwrap()` |
| `spaces_set.kara` | a `Set[i64]` of the places and one chain: `chars().enumerate().flat_map(..)`, each letter giving `[' ', c]` or `[c]` as an iterator, collected into the `String` |
| `spaces_iterator.kara` | a `struct Spaced` that implements `Iterator` with `Item = char`, its `next` (`mut ref self`) giving a due space or the next letter, `collect`ed |
| `spaces_solution.kara` | LeetCode's Rust template (`Vec<i32>`, `String::with_capacity`, `push_str(&s[last..sp])` over `for &sp in spaces.iter()`, `sp as usize`), carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and three
more (one space at the start, one before the last letter, one letter
with its space), each with its answer; then the length of the answers
for 3000 random strings of 1 to 30 letters of either case, with a space
before each letter with odds of one in three and at least one, and a
checksum of them; then the constraints' largest, 3 * 10^5 letters, with
a space before every letter and before every thousandth.
`spaces.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each letter in turn, a space before it when its place is
among `spaces`, found by a search of all of them. It checks 300 random
strings of 1 to 12 letters with a space before each with odds of one in
three; then 30 of up to 300 letters with odds of one in two; then 30 of
up to 50 letters with a space before every letter, or before the first
only. Each has at least one space, and all 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is `n + k` long, holds `k` spaces, and is `s` once they are taken out |
| P3 | every letter's case swapped: the answer's case swapped |
| P4 | the last space left out: the answer with that space taken out |
| P5 | a `Z` appended to `s`: the answer with a `Z` appended |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 strings: checksum 189668004, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
strings. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-five edits to the differential, five to seven to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: every other space dropped | P1 232, P2 232, P4 194, P6 232 |
| M27 | ★: each letter upper-cased | P1 330, P2 330, P3 360, P6 330 |
| M31 | ★: a space due at the first letter dropped | P1 184, P2 184, P4 31, P6 184 |
| M6 | slices: the pieces joined with nothing | P1 360, P2 360, P4 80, P6 360 |
| M8 | slices: the last piece dropped | P1 360, P2 360, P4 232, P5 360, P6 360 |
| M10 | slices: an empty piece dropped | P1 184, P2 184, P4 119, P6 184 |
| M11 | bytes: an underscore for a space | P1 360, P2 360, P6 360 |
| M13 | bytes: the last letter dropped | P1 360, P2 360, P5 355, P6 360 |
| M32 | bytes: a space before the last letter dropped | P1 143, P2 143, P4 98, P5 143, P6 143 |
| M15 | set: each space one letter early | P1 360, P2 184, P4 232, P6 360 |
| M17 | set: letters without a space doubled | P1 322, P2 322, P4 232, P5 360, P6 322 |
| M29 | set: a space before every letter not due | P1 360, P2 305, P4 232, P5 360, P6 360 |
| M19 | iterator: every other letter skipped | P1 340, P2 340, P4 30, P5 181, P6 340 |
| M22 | iterator: each space one letter early | P1 360, P2 184, P4 144, P6 360 |
| M35 | iterator: spaces past the hundredth letter dropped | P1 25, P2 25, P4 1, P6 25 |
| M24 | solution: each space one letter late | P1 360, P4 232, P6 360 |
| M26 | solution: each piece from the start | P1 295, P2 295, P4 232, P6 295 |

P1 and P6 kill all seventeen, P2 sixteen, P4 fourteen, P5 six and P3
one. P2 misses only the Rust arm's spaces one letter late (M24), which
keeps every letter and every space and only moves them. P4 misses the
edits that spoil every letter or every space alike, with or without the
last space (M11, M13, M27). P5 sees the edits that mishandle the end of
the string, which a `Z` moves: the last piece or letter dropped (M8,
M13), a space before the last letter dropped (M32), and the edits whose
damage grows with each letter (M17, M19, M29). P3 sees only the ★ arm's
letters upper-cased (M27): no other edit reads a letter's case, which
the arms copy and never inspect.

Of the thirty-five, eighteen were not kept. Every one is killed and
none survives. Ten fail as every answer wrong, P1 360, P2 360, P4 232,
P6 360: the ★ arm's two spaces at once; the slices arm's letter after
each space dropped, its first space dropped and its pieces joined with
two spaces; the bytes arm's spaced letter doubled and its first space
never made; the set arm's first space dropped; the iterator's first
space never given and its last space never given; and the Rust arm's
two spaces for one. Six fail as a kept one: the ★ arm's spaces one
letter early as M22 and after their letters as M24; the set arm's
spaces after their letters as M24; the iterator's dash for a space as
M11 and its last letter never given as M13; and the Rust arm's rest
after the last space dropped as M8. Two are killed with checks of their
own but were left out because their arm keeps its share: the ★ arm's
first letter dropped (P1 360, P2 360, P5 143, P6 360) and its letters
past the fiftieth dropped (P1 26, P2 26, P5 26, P6 26).

## Verification

Every arm prints the same output as `spaces.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 2.8 s to 5.2 s, but the set arm
12.2 s: a two-element `Vec` built and turned into an iterator for each
of the 3 * 10^5 letters. The differential takes 2.3 s there and 0.5 s
compiled.

`karac fix` carries the template in three rounds of 12, 1 and 1 edits:
Rust's spellings (`Vec<..>` to brackets, `String::` and `Solution::` to
`.`, the `&sp` pattern and the `&` before each `s[..]` dropped, `struct
Solution;` to `struct Solution {}`, the adapter's `&Vec` to `ref` and
its `|&p|` to `|p|`); then `sp as usize` to `sp as i64`, since `last`
starts as the literal `0`, an `i64`, and meets the `usize` in
`last..sp` and `last = sp`; then the adapter's `ref` parameter to a bare one.

The set arm's `flat_map` closure was written returning `[' ', c].to_vec()`
or `[c].to_vec()`, which Rust's `flat_map` takes as an `IntoIterator`;
Kāra's takes an `Iterator`, and `karac fix` appended `.into_iter()` to
the closure's `if`, which is how the arm reads.

## Benchmarks

The bench builds 20 strings of 3 * 10^5 letters once, each letter with
a space due before it with odds of one in three; it then spaces each 5
times, with the ★ arm in all five languages: one walk with an index
into the spaces. Every implementation prints `100 strings: 40003965
characters, checksum 645706955`.

BENCHTAB
