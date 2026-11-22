# 2707. Extra Characters in a String

You are given a **0-indexed** string `s` and a dictionary of words
`dictionary`. You have to break `s` into one or more
**non-overlapping** substrings such that each substring is present in
`dictionary`. There may be some **extra characters** in `s` which are
not present in any of the substrings.

Return *the **minimum** number of extra characters left over if you
break up* `s` *optimally.*

```
s = "leetscode",     dictionary = ["leet","code","leetcode"]  ->  1
s = "sayhelloworld", dictionary = ["hello","world"]           ->  3
```

**Constraints:** `1 <= s.length <= 50`, `1 <= dictionary.length <= 50`,
`1 <= dictionary[i].length <= 50`; `dictionary[i]` and `s` consist of
only lowercase English letters; `dictionary` contains distinct words.

## Approaches

| file | mechanism |
|---|---|
| `extra.kara` ★ | from the end of the string back, the fewest extra characters in each suffix: its first character left over, one more than the suffix after it, or any dictionary word that starts it skipped whole, as few as the suffix after the word. The dictionary is a `Set[String]` asked about every slice, the slice borrowed from the string. O(n^3) with the hashing |
| `extra_trie.kara` | the words in a trie of 26-way nodes, `Vec[Array[i64, 26]]`, each marking whether a word ends there; from each start the walk down the trie follows the string's bytes and finds every word that starts there in one pass. O(n^2 + total word length) |
| `extra_memo.kara` | a recursion from the front: the fewest from position i on is one more than from i + 1, or, for each word the rest `starts_with`, the fewest from just past it, each position's answer remembered in a `Vec[Option[i64]]` passed down by `mut ref`. O(n * words * word length) |
| `extra_forward.kara` | the fewest extra characters in each prefix, front to back: its last character left over, or a word it `ends_with` taken whole from where it starts. O(n * words * word length) |
| `extra_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `HashSet<&str>` of the words, `vec![0; n + 1]`, `&s[i..j]` slices and a `usize` index walking back with `.rev()`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples; a letter the
dictionary lacks; 50 a's as one word, and as words of two and three; 25
"ab"s against "ba"; the alphabet twice over, cut to 50, against every
other letter; then the extra characters summed and a checksum for 1000
random cases of 1 to 50 letters from a, b and c against up to 50 words
of 1 to 5 of them, and 1000 of any letters against 50 words of 1 to 3.
`extra.py` mirrors the ★ arm and its output is byte-identical.

```
1
3
1
0
0
2
25
1000 cases of 3 letters: extra characters sum to 3685, checksum 293241443
1000 cases of 26 letters: extra characters sum to 12628, checksum 615626330
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every choice of which characters are covered, as a mask,
stands when each run of covered characters breaks into dictionary words,
and the answer is the fewest characters any standing choice leaves over,
with no dynamic programming. It checks 600 random cases of 1 to 10
letters from a and b, or a to c, against up to 8 words of up to 4
letters; 100 of up to 50 letters from a to c against up to 50 words of
up to 5; and 100 of up to 50 letters from a to y against 50 words of up
to 3. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 10 letters, the answer is the literal reading's |
| P2 | up to five dictionary words joined: the answer is 0 |
| P3 | one word more in the dictionary: the answer is no larger |
| P4 | the string cut in two: the answer is at most the two halves' answers added |
| P5 | a z added, a letter no word holds: the answer is one more |
| P6 | each arm agrees with at least three of the other four |

The differential prints `800 cases: checksum 146413855, 24000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same 600 small cases by masks gives the same checksum. On
a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. P3 kills none of them: no edit here makes an
arm's answer grow with the dictionary. One first choice was replaced:
the memo arm ignoring its remembered answers is still right, only
exponential, and timed out rather than failed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a word may end the slice one short | P1 310, P2 800, P5 432, P6 432 |
| M2 | ★: a left-over character costs nothing | P1 435, P5 800, P6 573 |
| M3 | trie: a word's end never marked | P1 464, P2 800, P6 660 |
| M4 | trie: a word found skips one character too few | P1 448, P2 800, P6 644 |
| M5 | memo: a word that ends the rest taken as if it started it | P1 285, P2 120, P4 74, P5 441, P6 419 |
| M6 | memo: a word taken costs one | P1 464, P2 800, P6 660 |
| M7 | forward: a prefix's word taken from the start | P1 246, P6 377 |
| M8 | forward: words of one letter never taken | P1 309, P2 317, P6 485 |
| M9 | solution: the dp's last cell 1 | P1 600, P2 800, P6 800 |
| M10 | solution: a slice's word skipped one too far | P1 310, P2 800, P5 432, P6 432 |

## Benchmarks

The bench draws `10^4` strings of 50 letters from a, b and c, each
against up to 50 distinct words of 1 to 5 of them, all of them first,
then answers each 5 times by the ★ arm in all five languages; each
answer hashes all 1275 slices of its string. The dictionary is each
language's own hash set: Kāra's `Set[String]`, Rust's `HashSet<String>`,
Go's `map[string]struct{}`, Python's `set`, and in C a 128-slot open
addressing table on FNV-1a. Every implementation prints `10000 strings
of 50 letters against up to 50 words, 5 rounds: extra characters sum to
2745, checksum 704739591`.

BENCHTAB

## Verification

All five arms print the same output as `extra.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★, memo and forward arms checked clean as first written; the ★ arm
asks the `Set[String]` about `s[i..j]` directly, a borrowed slice, with
no `to_string()`. The trie arm took one `karac fix` of 4 edits: the
node type `[i64; 26]`, Rust's spelling, became `Array[i64, 26]`, and
casts that the `i64` indices no longer needed were dropped.

LeetCode's Rust template took one `karac fix` of 12 edits: the `use
std::collections::HashSet;` became `struct Solution {}`, `HashSet<&str>`
became `Set[Str]`, `vec![0; n + 1]` became `Vec.filled(n + 1, 0i32)`,
and `set.contains(&s[i..j])` dropped its `&`, since a parameter borrows
by itself. The wrapper's `as i64` on the `i32` answer was dropped, since
it widens by itself.
