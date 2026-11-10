# 2060. Check if an Original String Exists Given Two Encoded Strings

An original string, consisting of lowercase English letters, can be
encoded by the following steps: arbitrarily split it into a sequence of
some number of non-empty substrings; arbitrarily choose some elements (possibly
none) of the sequence, and replace each with its length (as a numeric
string); concatenate the sequence as the encoded string. For example,
`"abcdefghijklmnop"` can be encoded as `"ab121p"`: split as `["ab", "cdefghijklmn",
"o", "p"]`, the second and third replaced by `"12"` and `"1"`. Note that
the same string can be encoded many ways.

Given two encoded strings `s1` and `s2`, consisting of lowercase English
letters and digits 1-9 (inclusive), return `true` if there exists an
original string that could be encoded as both `s1` and `s2`. Otherwise,
return `false`.

**Note:** the test cases are generated such that the number of consecutive
digits in `s1` and `s2` does not exceed 3.

```
s1 = "internationalization", s2 = "i18n"  ->  true
s1 = "l123e",                s2 = "44"    ->  true    (both 8 letters: l, 1+2+3, e against 4+4)
s1 = "a5b",                  s2 = "c5b"   ->  false
s1 = "112s",                 s2 = "g841"  ->  true
```

**Constraints:** `1 <= s1.length, s2.length <= 40`; `s1` and `s2` consist
of digits 1-9 (inclusive) and lowercase English letters only; the number
of consecutive digits in `s1` and `s2` does not exceed 3.

A run of digits stands for any of the numbers its digits make when split
(`"123"` is 123, 12 and 3, 1 and 23, or 1, 2 and 3: 123, 15, 24 or 6
letters). Reading both strings from the left, the only thing that matters
is how many letters one has run ahead of the other: a search over (place
in `s1`, place in `s2`, lead) answers it, and with runs of at most three
digits the lead stays within -999..=999. O(n1 · n2 · 2000) states. The
approaches differ in which way they walk the states and what they keep
them in.

## Approaches

| file | mechanism |
|---|---|
| `original.kara` ★ | a depth-first search over (place, place, lead) on `Vec[char]`: a digit run read as each number its prefixes make, a lead paid off one letter at a time by the string behind, two letters compared only with no lead; a `Set[(i64, i64, i64)]` passed `mut ref` keeps each state to one try |
| `original_table.kara` | the same search without recursion: a `Vec` of states as a stack, the states seen in a `Vec[bool]` of `(n1 + 1) · (n2 + 1) · 1999` indexed by a closure, the strings as `bytes()` |
| `original_tokens.kara` | each string read first into an `enum Token { Letter(char), Lengths(Vec[i64]) }`, a run with every sum its digits make split every way (`sums`, recursive over a `Slice[char]`); the search walks tokens with a `match` on `(a.get(i), b.get(j))` with guards, every state's answer, true or false, kept in a `Map` |
| `original_forward.kara` | forward, cell by cell: `leads[i][j]`, a `Vec[Vec[Set[i64]]]`, holds every lead some reading reaches with `i` and `j` characters read; every step reads more of one string, so filling in order of `i`, then `j`, finishes each cell before any step leaves it. True when the last cell holds 0 |
| `original_bits.kara` | the forward cells as bitsets: each cell's leads -999..=999 as bits of 32 `u64` words, a digit run's number one shift of a whole cell (`shift_or`, carrying across words), a letter paying off a lead a shift of one half by one |
| `original_solution.kara` | LeetCode's Rust template (`s1.as_bytes()`, a nested `fn dfs` over `&[u8]` slices and a `&mut HashSet<(usize, usize, i32)>`, `usize` places, `(c - b'0') as i32`), carried by `karac fix` in five rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's four examples and four
more (among them a pair of dense 40-character strings of digit runs), each pair
and its answer; then how many of 3000 random pairs are possible and a
checksum. Each pair encodes a string of 1 to 40 letters from 1 to 3 of
the alphabet, and the same string, another of its length, or the string
with one letter dropped or added, pieces of each replaced by their
lengths. `original.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every reading of each string, a wildcard for each letter a
number stands for, and some pair of readings the same length and equal
wherever both have a letter. It checks 600 pairs of strings of 1 to 14
letters, encoded as the harness encodes them, then 40 pairs whose numbers
run from 20 to 300 (`encode_long`), so that a lead passes 64 either way,
which a bitset arm must carry from one word to the next. All 640 are
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the two strings swapped have the same answer |
| P3 | both strings reversed, each digit run kept as written, have the same answer |
| P4 | the same new letter put in front of both strings leaves the answer |
| P5 | a letter of `s1` with no digit beside it, made `1`, never turns a yes into a no |
| P6 | each arm agrees with at least three of the other five |

P3 holds because a run stands for the same numbers read either way it is
split, and an original string read backwards is encoded by the same
pieces backwards. P5 holds because a `1` stands for any one letter,
the one it replaced among them; next to a digit it would join that run.

The differential prints `640 pairs: checksum 607303746, 23040 checks
over 6 arms: 0 failures` under every lane in Verification; 376 of its
640 pairs are possible. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Thirty-one edits to the differential, four to six to each of its arms,
each run under `karac __mir-llvm-run`, and the kept ones and the
survivor under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed, fails
the same way under both backends and not by a crash, and no two kept
ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a lead paid off by the string that is ahead | P1 175, P2 243, P3 1, P5 67, P6 175 |
| M2 | ★: states told apart without their lead | P1 37, P3 2, P6 37 |
| M3 | ★: a lead of `s2` paid off the wrong way | P1 160, P2 243, P3 1, P6 160 |
| M4 | table: `s2`'s run added to the lead | P1 249, P2 147, P3 1, P6 249 |
| M5 | table: `s1`'s last letter never paying a lead | P1 83, P2 183, P3 82, P6 83 |
| M6 | table: the search given up at the first end with a lead | P1 83, P3 32, P6 83 |
| M7 | tokens: every reading of a run one letter longer | P1 223, P5 127, P6 223 |
| M8 | tokens: a lead of one never paid by `s2` | P1 127, P2 215, P3 55, P5 77, P6 127 |
| M9 | tokens: two letters wanted different | P1 150, P4 248, P6 150 |
| M10 | forward: `s2`'s letter paying nothing | P1 178, P2 247, P3 2, P5 69, P6 178 |
| M11 | forward: `s1`'s numbers one short | P1 322, P2 242, P5 129, P6 322 |
| M12 | forward: a run read only whole | P1 104, P6 104 |
| M13 | bits: no carry between words | P1 3, P2 2, P6 3 |
| M14 | bits: a zero lead counted above zero | P1 54, P6 54 |
| M15 | bits: the search started with a lead of one | P1 457, P2 160, P3 32, P4 45, P6 457 |
| M16 | solution: a state's first try refused | P1 376, P6 376 |
| M17 | solution: the adapter comparing `s1` with itself | P1 264, P6 264 |

P1 and P6 kill all seventeen, P2 and P3 nine each, P5 five and P4 two.
The 40 pairs of long numbers are what kill M13: before they were added,
no lead in 600 pairs of short strings passed 64, no shift crossed from
one word to the next, and the bits arm with no carry survived. P2 sees, among others,
the edits that treat the two strings unevenly (M1, M3, M4, M5, M8, M10,
M11); P3 those whose answer depends on which end a string is read from,
like a state's lead forgotten (M2) or a search stopped at the first end
it meets (M6); P4 a letter compared the wrong way (M9) and a start with a
lead (M15), which a common first letter turns into a mismatch; P5 the
edits that read a number as more or fewer letters than it stands for.

Of the thirty-one, fourteen were not kept. One survives: the table arm's
index with `n2` for `n2 + 1`, which folds (place, `n2`) onto (place + 1,
0). That is the only pair it folds, and it is equivalent: a state that
has read nothing of `s2` but something of `s1` comes only from the first
state, reading `s1`'s first digit run, so it is marked before any state
that has read all of `s2`; and that one, at the same positive lead, has
`s1` still ahead with nothing left to pay it, so it fails anyway. Eleven
fail as a kept one or as each other: the ★ arm's run read only to its first digit and the
table arm's digits summed alike; the ★ arm's two letters always equal as
M14; the ★ arm's, forward arm's and Rust arm's end reached with any lead
alike; the forward and bits arms' matched letter of `s2` left unread
alike; the bits arm's numbers of `s2` added as M4; the Rust arm's last
letter never paying a lead as M5 and a lead of `s1` grown by `s2`'s
letter as M1. Two are killed with checks of their own but were left out
because their arm keeps three: the tokens arm's end reached with `s1`
ahead (P1 67, P2 96, P3 43) and a letter after each letter skipped (P1
285, P3 48, P4 115, P5 17).

## Verification

Every arm prints the same output as `original.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them.

Under `karac __mir-run` the arms take 1.2 s (★) to 5.5 s (forward),
except the table and bits arms at 107 s and 105 s, which set up a table
of `(n1 + 1) · (n2 + 1)` cells of 1999 flags or 32 words for every pair,
and the differential 40 s (timed while other work shared the machine).

The tokens arm met one compiler gap. `sums` was written first with
`digits.slice(k + 1, digits.len())` on its `Slice[char]`. The library has
no `slice` method on a sequence (a run is the range index `v[a..b]`), and
the checker said so and offered the edit to `[a..b]`, but only when both
bounds were a literal or a name: a computed bound got the hint and no
edit. `karac fix` now writes any bound but a range back as it reads,
`digits[k + 1..digits.len()]`, which the arm now holds. Fixed in kara
0556eab231, test `tests/kata_1078_slice_hint.rs`.

The table arm was written with `as_bytes()` and `!`, which `karac fix`
turned into `bytes()` and `not`, then a cast the next round found lossless.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in five rounds of 22, 2, 2, 13 and 2 edits to a clean check: first
Rust's spellings (the `HashSet` import deleted, `struct Solution;` to
`struct Solution {}`, `&[u8]` to `Slice[u8]`, `&mut` to `mut ref`,
`<..>` to brackets, `&&` and `!` to `and` and `not`, `HashSet::new` to
`.new`), then the nested `fn dfs` hoisted out of the method (it captures
nothing), then `HashSet` to `Set`, then the `usize` places to `i64` with
the casts and `mut` markers that follow, and last two casts it found
lossless. The fixed arm reads as the template does.

## Benchmarks

The bench answers 2000 pairs of dense strings with the ★ arm in all five
languages: runs of 1 to 3 digits, each followed by `u` or `v`, up to 40
characters, so nearly every place is a digit and the search meets the
most leads the constraints allow. C keeps the states in an
open-addressing table doubled when half full; Rust a `HashSet`; Go a
`map`. Every implementation prints `2000 pairs: 116 possible, checksum
823479292`.

BENCHTAB
