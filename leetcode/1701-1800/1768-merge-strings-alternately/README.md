# 1768. Merge Strings Alternately

You are given two strings `word1` and `word2`. Merge the strings by
adding letters in alternating order, starting with `word1`. If a string
is longer than the other, append the additional letters onto the end of
the merged string. Return the merged string.

```
word1 = "abc",  word2 = "pqr"   ->  "apbqcr"
word1 = "ab",   word2 = "pqrs"  ->  "apbqrs"
word1 = "abcd", word2 = "pq"    ->  "apbqcd"
```

**Constraints:** `1 <= word1.length, word2.length <= 100`, and both
consist of lowercase English letters.

The arms are `fn merge_alternately(word1: String, word2: String) ->
String`.

## Approaches

| file | mechanism |
|---|---|
| `merge_alternately.kara` ★ | the two words' letters as `Vec[char]`, one index walking both up to the longer length, a letter from each word that still has one. O(n + m) |
| `merge_alternately_zip.kara` | the letters paired with `zip` while both words have one, then the longer word's rest appended whole with `push_str` of a slice. O(n + m) |
| `merge_alternately_iterators.kara` | two `chars` iterators taken in turn: each round asks both for their next letter and stops when both are spent. O(n + m) |
| `merge_alternately_bytes.kara` | the words' bytes, every letter ASCII, pushed into a `Vec[u8]` with the full capacity from the start, then read back with `String.from_utf8`. O(n + m) |
| `merge_alternately_solution.kara` | a Rust solution as LeetCode's Rust users write it (`String::with_capacity`, a `match` on `(a.next(), b.next())`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples (`apbqcr
apbqrs apbqcd`); four edges, one letter each, the first word of one
letter, the second of one, and the same letters in both (`ab abcd aebcd
zzzz`); the constraints' most, two words of 100 letters and 100 beside
1, as lengths and digests (`the most: 200 470841750, 101 535698896`);
and 3000 random pairs of words of 1 to 20 letters (`3000 random pairs:
checksum 104090714`). `merge_alternately.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, zip and iterators arms check clean as first
written. The bytes arm was first written with Rust's `word1.as_bytes()`,
and `karac fix` took the two calls to `.bytes()`, Kāra's `Slice[u8]`, in
2 fixes. The Rust solution takes one round of 6 fixes by `karac fix`'s
count, and its diff is: `struct Solution;` to `struct Solution {}`,
`String::with_capacity` to `String.with_capacity`, `let (mut a, mut b) =
..` to `let mut (a, b) = ..` and `Solution::` to `Solution.`. Every
arm's output matches on the first run.

The harness's digest was first written `s.bytes().fold(..)`, and check
refused it: `bytes()` is a `Slice[u8]`, so `fold` needs `.iter()`, which
`karac fix` inserted, dropping the `b as i64` cast as lossless in the
same run. Beside that error check printed a second one, "cannot cast
'?T11' to 'i64'", a cascade naming an internal type variable
(B-2026-11-26-81). The differential's P4 was first written `arm(..) +
arm(..).as_str()`, as Rust joins a `String` and a `&str`; Kāra's `+`
wants a `String` on the right, and `karac fix` made it
`arm(..).as_str().to_string()`, a view copied back into a `String`. The
`.as_str()` was dropped by hand instead, and the round trip is
B-2026-11-26-82.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: letters added in alternating order, starting with `word1`,
and once a word runs out the other's letters added in turn. LeetCode's
examples, the edges, and 1992 random pairs of words of 1 to 12 letters
from the first 2 to 26 of the alphabet. Each arm meets six properties on
each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | every letter once, and `word1`'s first in each pair the two words share |
| P3 | the words swapped give each shared pair swapped and the rest unchanged |
| P4 | both words cut at one place inside the shorter one merge as the two halves' merges joined |
| P5 | each letter moved one on in the alphabet, `z` to `a`, gives the answer moved the same way |
| P6 | the ★ arm's answer |

P4 runs where the shorter word has at least 2 letters. All 58,310 checks
pass on every arm: `2000 cases: checksum 266641276, 58310 checks over 5
arms: 0 failures`, under `karac __mir-run`, `karac run`, `karac build`
and `karac __mir-llvm-run`. Python, reading the statement the same way,
gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the walk stops at the shorter word | P1 1824, P2 1824, P6 7296 |
| M2 | ★: word2's last letter never taken | P1 2000, P2 2000, P3 1963, P4 1662, P6 8000 |
| M3 | zip: word2's rest taken where word1's goes | P1 1824, P2 1824, P3 1824, P6 1824 |
| M4 | zip: each pair added word2's letter first | P1 1954, P2 1954, P6 1954 |
| M5 | iterators: the loop stops when either word is spent | P1 1824, P2 1824, P6 1824 |
| M6 | iterators: word2 read only while word1 has letters | P1 889, P2 889, P3 1824, P6 889 |
| M7 | bytes: the loop runs only while both words have letters | P1 1824, P2 1824, P6 1824 |
| M8 | bytes: the index steps by two | P1 1987, P2 1987, P3 1619, P4 992, P6 1987 |
| M9 | solution: word1's rest dropped | P1 935, P2 935, P3 1824, P6 935 |
| M10 | solution: word2's rest added twice | P1 889, P2 889, P3 1824, P6 889 |

## Benchmarks

The bench builds 1000 words of 1 to 100 letters once and makes 2000000
calls of the ★ arm, each on a pair chosen from the checksum so far.
Every implementation prints `2000000 calls over 1000 words: checksum
822125501`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.76 s against Rust's 1.6 s (1.8 s with
overflow checks on), C's 0.35 s and Go's 6.3 s; Python takes 14.8 s.
