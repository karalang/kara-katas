# 2114. Maximum Number of Words Found in Sentences

A sentence is a list of words that are separated by a single space with
no leading or trailing spaces.

You are given an array of strings `sentences`, where each `sentences[i]`
represents a single sentence.

Return the maximum number of words that appear in a single sentence.

```
sentences = ["alice and bob love leetcode","i think so too","this is great thanks very much"]  ->  6
sentences = ["please wait","continue to fight","continue to win"]                              ->  3
```

**Constraints:** `1 <= sentences.length <= 100`; `1 <=
sentences[i].length <= 100`; `sentences[i]` consists only of lowercase
English letters and `' '` only; `sentences[i]` does not have leading or
trailing spaces; all the words in `sentences[i]` are separated by a
single space.

With single spaces between words and none at either end, a sentence has
exactly one word more than it has spaces, so the answer is the most
spaces in any sentence, plus one.

## Approaches

| file | mechanism |
|---|---|
| `words.kara` ★ | each sentence's spaces counted with `bytes().iter().filter(\|b\| b == b' ').count()`, plus one, the largest kept with `max`. O(total length) |
| `words_split.kara` | `split(" ").count()` per sentence through `map`, then `max() ?? 0` |
| `words_starts.kara` | word starts: a letter that is first or follows a space, counted by indexing each sentence's bytes, so the count does not lean on the single-space rule |
| `words_fold.kara` | one `fold` over the sentences carrying the best count, each sentence's `split_whitespace().count()` |
| `words_struct.kara` | a `struct Tally` fed the characters one at a time, its `see` method (`mut ref self`) counting spaces and its `finish` method closing a sentence and keeping the most words |
| `words_solution.kara` | LeetCode's Rust template (`Vec<String>` to `i32`): `split(' ').count() as i32` per sentence through `map`, then `max().unwrap()`, carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and three
more (one word alone, one-letter words, the longest sentence last), each
with its answer; then the total for 3000 random lists of 1 to 10
sentences of 1 to 12 words of 1 to 6 letters, and a checksum of the
answers; then the constraints' largest, 100 sentences of 100
characters: 50 one-letter words each, and one 100-letter word each.
`words.py` mirrors the ★ arm and its output is byte-identical.

The ★ arm was first written `s.bytes().filter(..)`; `karac fix` added
the `.iter()`, since in Kāra `bytes()` gives a `Slice` rather than an
iterator, and turned the harness's `'a' as u8` into `b'a'`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each sentence cut into its words, a word ending at each space
and at the end of the sentence, the words kept in a list, and the
longest list's length taken. It checks 300 random lists of 1 to 5
sentences of 1 to 6 words of 1 to 3 letters (from `a` to `c`); then 30
of up to 30 sentences of up to 50 words of 1 to 4 letters; then 30 in
which one sentence of up to 50 one-letter words sits among up to four
short ones. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is at least 1 and at most half of the longest sentence's length plus one, rounded down |
| P3 | every letter made `z`: the same answer |
| P4 | the sentences joined with spaces and appended: the answer is the sum of each sentence's alone |
| P5 | the sentences reversed: the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 lists: checksum 308568828, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
lists with `split(" ")`. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept, three
to each Kāra arm and two to the Rust-template arm. Each kept one is
killed, fails the same way under both backends and not by a crash, and
no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: spaces counted without the one more | P1 360, P2 6, P4 295, P6 360 |
| M3 | ★: the last sentence's count kept | P1 190, P5 250, P6 190 |
| M5 | ★: the first sentence skipped | P1 137, P2 65, P4 360, P5 139, P6 137 |
| M8 | split: the first sentence only | P1 184, P4 295, P5 250, P6 184 |
| M9 | split: split at each letter `a` | P1 280, P2 9, P3 353, P4 295, P6 280 |
| M10 | split: the last sentence dropped | P1 126, P4 327, P5 139, P6 126 |
| M12 | starts: every letter a start | P1 337, P2 337, P6 337 |
| M14 | starts: the last byte never looked at | P1 121, P2 1, P4 187, P6 121 |
| M15 | starts: the count carried across sentences | P1 242, P2 50, P4 354, P5 170, P6 242 |
| M17 | fold: the counts summed | P1 295, P2 258, P4 360, P6 295 |
| M19 | fold: two-letter words counted twice | P1 308, P2 62, P6 308 |
| M20 | fold: words past 20 not counted | P1 47, P4 60, P6 47 |
| M21 | struct: the count not reset | P1 273, P2 221, P4 354, P6 273 |
| M23 | struct: every character a word | P1 360, P2 360, P6 360 |
| M25 | struct: the last sentence never finished | P1 56, P2 38, P4 194, P5 24, P6 56 |
| M27 | solution: the smallest taken | P1 281, P4 295, P6 281 |
| M29 | solution: the count halved | P1 338, P4 278, P6 338 |

P1 and P6 kill all seventeen, P4 thirteen, P2 eleven, P5 six and P3
one. P4 compares a whole list with its sentences one at a time, so it
sees an edit that miscounts a single sentence or keeps the wrong one.
It misses four: the ★ arm's last count kept (M3), since the joined
sentence is appended last and is the longest, and the edits whose count
of a sentence adds up over its words or letters (M12, M19, M23), which
the joined sentence adds up the same way. P5 sees the edits that depend
on which sentence comes first or last (M3, M5, M8, M10, M15, M25). P2
sees the counts that can fall to zero or pass one word per two
characters: one word fewer on a one-word sentence (M1), letters or
words counted twice (M12, M19, M23), counts carried or summed across
sentences (M15, M17, M21), a sentence skipped or cut short (M5, M14,
M25), and the split at the letter `a` (M9). P3 sees only that split
(M9), the one edit that reads a letter.

Of the thirty, thirteen were not kept. One survives and is equivalent:
the fold arm's fold started at 1 rather than 0, which no answer is below.
Six fail as M1 does (P1 360, P2 6, P4 295, P6 360), one fewer word than
there is: the split arm's pieces counted one short, the starts arm's
start counted only after a space and its word ends counted at spaces
only, the struct arm's spaces counted without the one more and its last
word unseen, and the Rust arm's spaces counted. The ★ arm's smallest
count kept and the split arm's smallest taken fail as M27, the fold
arm's newest count kept and the Rust arm's last sentence only as M3.
The ★ arm's letters counted is killed with checks of its own (P1 360, P2
360, P4 295, P6 360) but was left out because its arm keeps its share,
and the Rust arm's first sentence skipped was not kept for how it ends:
`max().unwrap()` panics on a list of one.

## Verification

Every arm prints the same output as `words.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.0 s to 1.5 s, and the
differential 2.8 s; compiled it takes 0.5 s.

`karac fix` carries the template in two rounds of 4 and 2 edits: Rust's
spellings (`Vec<String>` to `Vec[String]`, `struct Solution;` to
`struct Solution {}`, `Solution::` to `.`); then the `char` pattern `'
'` in `split` to the string `" "`, and the adapter's `as i64` dropped,
since the `i32` result widens without one.

## Benchmarks

The bench builds 200 lists of 100 sentences of 1 to 25 words of 1 to 6
letters once; it then solves each list 10 times, appending the word `a`
to one of its sentences before each solve so no solve repeats the one
before, with the ★ arm in all five languages: each sentence's spaces
counted over its bytes. Every implementation prints `2000 solves: 50324
words, checksum 665501699`.

BENCHTAB
