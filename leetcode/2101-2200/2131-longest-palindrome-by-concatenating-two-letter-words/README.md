# 2131. Longest Palindrome by Concatenating Two Letter Words

You are given an array of strings `words`. Each element of `words`
consists of two lowercase English letters.

Create the longest possible palindrome by selecting some elements from
`words` and concatenating them in any order. Each element can be
selected at most once.

Return the length of the longest palindrome that you can create. If it
is impossible to create any palindrome, return `0`.

A palindrome is a string that reads the same forward and backward.

```
words = ["lc","cl","gg"]                 ->  6
words = ["ab","ty","yt","lc","cl","ab"]  ->  8
words = ["cc","ll","xx"]                 ->  2
```

**Constraints:** `1 <= words.length <= 10^5`; `words[i].length == 2`;
`words[i]` consists of lowercase English letters.

A palindrome of two-letter words mirrors itself word by word: the word
at each place from the start is the reverse of the word at the same
place from the end. So a word and its reverse sit as a mirrored pair,
four letters, as often as the rarer of the two allows; a doubled word
such as `"gg"` is its own reverse and pairs with another copy; and one
doubled word left over can sit alone in the middle, two letters more.
O(n).

## Approaches

| file | mechanism |
|---|---|
| `palindrome.kara` ★ | the words counted in a 26 by 26 `Vec[i64]` by their two letters, then each letter pair `x <= y` read once |
| `palindrome_map.kara` | a `Map[String, i64]` of counts through `entry().or_insert(0)`; each word met with its reverse, a `String` of its chars reversed, counted from the smaller of the two |
| `palindrome_greedy.kara` | one pass: a word whose reverse is waiting takes it, four letters; otherwise it waits itself; at the end a waiting doubled word is the middle |
| `palindrome_sorted.kara` | the words sorted so equal words stand in runs; a run's reverse found by `binary_search`, which gives some place in it, walked back to its start with `let mut Some(at) = .. else` |
| `palindrome_struct.kara` | a `struct Shelf { counts: Array[i64, 676] }` with `put` (`mut ref self`), `pairs` and `centre` (`ref self`) |
| `palindrome_solution.kara` | LeetCode's Rust template: a `HashMap<String, i32>` of counts, `for (w, &c) in count.iter()` and `if let Some(&rc) = count.get(&r)`, carried by `karac fix` in four rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more (one doubled word, two, a word with two of its reverse, a word with
no partner), each with its answer; then the letters and a checksum over
2000 random lists of 1 to 12 words over the first 2, 3 or 5 letters in
turn; then the constraints' largest, 100000 of `"aa"`, 100000 of `"ab"`
and `"ba"` in turn, and 100000 random words. `palindrome.py` mirrors the
★ arm and its output is byte-identical.

No compiler gap was met. Two arms went through `karac fix` as they were
written: the ★ arm's `count[(b[0] - 97) as i64 * 26 + (b[1] - 97) as
i64]`, whose second cast the `+` makes itself (the first is kept, since
`(b[0] - 97) * 26` would be a `u8`), and the sorted arm's Rust `match
sorted.binary_search(word) { Ok(i) => .., Err(_) => .. }`, which the
diagnostic rewrote through `partition_point`; the arm was then written
with Kāra's own `binary_search`, an `Option`, and `karac fix` moved the
`mut` of `let Some(mut at)` before the pattern.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every sequence of distinct words is tried, built one word at
a time by a search over which are used, and the longest whose letters
read the same backwards is kept; no pairing is assumed. It checks 300
random lists of 1 to 7 words over the first 2, 3 or 5 letters in turn;
then 30 of 1 to 7 doubled words over 3 letters; then 30 of 1 to 7 words
each a word or its reverse over 4 letters. All 360 are drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the words in reverse order: the same answer |
| P3 | every word reversed: the same answer |
| P4 | a new word and its reverse added: four more |
| P5 | every letter moved on by one in the alphabet: the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 lists: checksum 389795418, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
lists by the same search. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Twenty-five edits to the differential, three to five to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every doubled word counted in full | P1 213, P6 213 |
| M2 | ★: any doubled word enough for the middle | P1 33, P6 33 |
| M4 | ★: the commoner of a word and its reverse | P1 278, P6 278 |
| M5 | map: each pair counted from both words | P1 107, P4 360, P6 107 |
| M6 | map: an even count of a doubled word for the middle | P1 203, P6 203 |
| M7 | map: a missing reverse taken as plentiful | P1 175, P3 213, P6 175 |
| M8 | greedy: a word waiting for itself | P1 139, P4 360, P6 139 |
| M9 | greedy: a waiting reverse never used up | P1 67, P2 31, P6 67 |
| M21 | greedy: a mirrored pair two letters | P1 166, P4 360, P6 166 |
| M11 | sorted: a run never walked back to its start | P1 106, P3 47, P6 106 |
| M12 | sorted: only the last doubled run for the middle | P1 18, P6 18 |
| M13 | sorted: every word of a run counted again | P1 110, P3 47, P6 110 |
| M14 | struct: a doubled word's count taken as its pairs | P1 246, P6 246 |
| M15 | struct: an even count for the middle | P1 147, P6 147 |
| M16 | struct: the doubled words never asked | P1 88, P6 88 |
| M18 | solution: the adapter dropping the first word | P1 128, P2 146, P4 307, P6 128 |
| M25 | solution: every word taken as its own reverse | P1 215, P4 360, P6 215 |

P1 and P6 kill all seventeen, P4 five, P3 three, P2 two, and P5 none.
Most edits miscount one kind of word, doubled or mirrored, and so fail
P1 alone: whatever the order of the words, their reversal or their
letters, the same kind of word is miscounted the same way. P4 adds a
mirrored pair, which sees the edits that count a mirrored pair wrongly
(M5, M8, M21, M25) or drop a word (M18). P3 reverses every word, which
sees an edit that treats a word unlike its reverse: a reverse looked up
as plentiful when absent (M7), a run's start misread in the sorted
order the reversal changes (M11, M13). P2 reverses the order, which
only the edits that read the words in order see: the greedy pass (M9)
and the adapter's first word (M18). P5 renames every letter, and no
arm reads a letter's value beyond telling the letters apart, so no edit
here is seen by it; it stays as a check that none does.

Of the twenty-five, eight were not kept. One is equivalent: the
template counting each mirrored pair from the larger of the two words
rather than the smaller. None survives, and none fails by a crash. Six
fail as a kept one does: the ★ arm pairing a doubled word with itself
again as M14; the greedy arm's middle only for two waiting, a middle
for every odd doubled word in the map arm and the template's middle of
one letter as M1; the template's pair of doubled words two letters as
M16; and its mirrored pair two letters as M5. One is killed with checks
of its own but was left out because its arm keeps its share: the greedy
arm taking down the word's own count (P1 15, P2 31, P6 15).

## Verification

Every arm prints the same output as `palindrome.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.85 s to 1.6 s and the differential 5.3
s, nearly all of it the literal search over every sequence of up to 7
words.

`karac fix` carries the template in four rounds of 16, 2, 2 and 1
edits: Rust's spellings (the `use` dropped, `<..>` to `[..]`, `for w in
&words` to `for w in ref words`, the `&c` pattern to `c`, `Some(&rc) =
count.get(&r)` to `Some(rc) = count.get(r).cloned()`, `struct
Solution;` to `struct Solution {}`, the adapter's `&Vec` to `ref Vec`,
`::` to `.`); then `HashMap` to `Map`; then `ans` annotated `i32` and
the adapter's `as i64` dropped; then the `ref` dropped from the
adapter's parameter, which borrows already. The adapter's
`words.clone()` stays: it is the copy that kata 2125 found no lint
names (karac B-2026-11-14-3).

## Benchmarks

The bench builds 20 lists of 100000 words over the first 8 letters once,
then solves every list 10 times, one word replaced by a random one before
each solve so that no solve repeats one before, with the ★ arm in all
five languages. Every implementation prints `200 solves: 39608026
letters in all, checksum 249895675`.

BENCHTAB
