# 2868. The Wording Game

Alice and Bob each have a **lexicographically sorted** array of
strings named `a` and `b` respectively.

They are playing a wording game with the following rules:

- On each turn, the current player should play a word from their list
  such that the new word is **closely greater** than the last played
  word; then it's the other player's turn.
- If a player can't play a word on their turn, they lose.

Alice starts the game by playing her **lexicographically smallest**
word.

Given `a` and `b`, return `true` *if Alice can win knowing that both
players play their best, and* `false` *otherwise.*

A word `w` is **closely greater** than a word `z` if the following
conditions are met:

- `w` is **lexicographically greater** than `z`.
- If `w1` is the first letter of `w` and `z1` is the first letter of
  `z`, `w1` should either be **equal** to `z1` or be the **letter after**
  `z1` in the alphabet.
- For example, the word `"care"` is closely greater than `"book"` and
  `"car"`, but is not closely greater than `"ant"` or `"cook"`.

```
a = ["avokado","dabar"],           b = ["brazil"]                     ->  false
a = ["ananas","atlas","banana"],   b = ["albatros","cikla","nogomet"] ->  true
a = ["hrvatska","zastava"],        b = ["bijeli","galeb"]             ->  true
```

**Constraints:** `1 <= a.length, b.length <= 10^5`; `a[i]` and `b[i]`
consist only of lowercase English letters; `a` and `b` are
lexicographically sorted; all the words in `a` and `b` combined are
distinct; the sum of the lengths of all the words in `a` and `b`
combined does not exceed `10^6`.

## Approaches

| file | mechanism |
|---|---|
| `wording.kara` ★ | a player does best to play the largest word they hold of the letter in play when it beats the last word, which leaves the other the least room under that letter, and else the largest of the next letter, which also beats it; a table of each player's largest word per letter makes every turn one look-up, and the game is played out |
| `wording_search.kara` | the smallest word that will do, by binary search: the first word a player holds past the last one, by `partition_point`, is playable exactly when it starts with the letter in play or the next, since every later word starts no earlier; playing the smallest also wins whenever a win is there |
| `wording_scan.kara` | two pointers, one per hand, that only move forward: on a turn the player's pointer passes every word that cannot be played until one can, which is played; a hand walked to its end loses. No word passed could be played later, as every later word beats it |
| `wording_dp.kara` | the game solved backwards with no strategy assumed: every word is a position, the player to move being the one who does not hold it; worked from the largest word down, the player to move wins when they hold a larger word of the same letter or the next that leaves the other a lost position, and a flag per player and letter says whether any such word has been seen |
| `wording_solution.kara` | a Rust solution as LeetCode's Rust users write it: two indices, the hand and its index picked each turn as `(&b, &mut j)` or `(&a, &mut i)`, first letters compared by `as_bytes()[0]`, and the first playable word taken, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

The ★ arm and the search arm play different strategies, the largest
word that will do and the smallest; both win exactly when a win is
there, which the differential checks against the whole game searched
and the backward solution, which assumes neither.

Every arm prints the same 4 lines: LeetCode's three examples; a game
played through all 26 letters, Alice holding a, c, ..., y and Bob b,
d, ..., z; then 3000 small deals of 2 to 8 words of 1 to 3 letters from
a to d, and 30 of 10^4 to 10^5 words of up to 8 letters, every other one
from a to e only, as the count of Alice's wins and a checksum of the
answers. `wording.py` mirrors the ★ arm and its output is
byte-identical.

```
false true true
false
3000 small deals: Alice wins 1817, checksum 825732003
30 large deals: Alice wins 17, checksum 44983684
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: the whole game searched, every playable word tried on
every turn, a player winning when some word leaves the other with no
win. It draws 2000 random deals of 2 to 8 words of 1 to 3 letters from
a to d, then 50 of up to 3000 words of up to 6 letters, every other one
from a to e only, all before any arm answers; the literal reading is
asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 8 words, the answer is the literal reading's |
| P2 | Bob given `"a"`, smaller than Alice's first word, which he can never play: the same answer |
| P3 | every letter moved one on, when no word holds a z: the same answer |
| P4 | Alice given only her first word: she wins exactly when Bob has no reply to it |
| P5 | when Bob has no reply to Alice's first word, Alice wins |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 deals, Alice wins 1266: checksum
566716342, 61500 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python reading of the same deals gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the smallest word of a letter kept, not the largest | P1 115, P2 28, P4 44, P6 139 |
| M2 | ★: the next letter tried first | P1 21, P6 21 |
| M3 | search: Alice's first word read from Bob's hand | P1 468, P2 378, P4 655, P5 131, P6 468 |
| M4 | search: a word two letters on allowed | P1 349, P4 291, P5 196, P6 349 |
| M5 | scan: Bob's pointer started past his first word | P1 378, P2 250, P4 538, P6 378 |
| M6 | scan: a same-letter word allowed without beating the last | P1 349, P2 125, P4 218, P5 155, P6 374 |
| M7 | dp: the next letter's words not looked at | P1 612, P4 709, P6 637 |
| M8 | dp: a winning position marked good | P1 764, P4 1263, P6 784 |
| M9 | solution: a word two letters on taken for the next letter | P1 683, P4 754, P5 224, P6 694 |
| M10 | solution: a hand walked out read as a win | P1 2000, P4 2050, P5 787, P6 2050 |

## Benchmarks

The bench draws 20 deals of 10^5 words, LeetCode's most, of 1 to 8
letters, every other one from a to e only, all of them first, then
plays each 20 times by the ★ arm in all five languages. Building the
two tables walks every word, and the game itself takes a few turns per
letter, so the bench measures the walk. Every implementation prints `20
deals of 100000 words, 20 rounds: Alice wins 200, checksum 41902703`.

BENCHTAB

## Verification

All five arms print the same output as `wording.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★ arm, as first written, indexed its table with `(w.bytes()[0] -
b'a') as i64`, and `karac check` warned that the cast was lossless, a
`u8` widening to `i64` on its own; `karac fix` took it off. The other
three arms checked clean, `let hands = [a, b]` included: an array of
two borrowed parameters is an array of borrows.

The differential's literal reading, as first written, handed `[a,
b].to_vec()` straight to its search, and `karac check` reported E0200
at each, the parameters being borrows where the call wanted the vectors
owned; it takes the two hands apart instead. Its letter shift, first
`(c as u8) + 1` over the characters, got E_CHAR_AS_NARROW_INT, a `char`
not fitting `u8`, and walks the bytes instead.

LeetCode's Rust template took 23 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; `Vec<..>`
became `Vec[..]`; `let (mut i, mut j)` became `let mut (i, j)`; `(&b,
&mut j)` became `(ref b, mut ref j)`, both arms of the `if`, and `&words[*k]`
`ref words[*k]`; `as_bytes()` became `bytes()`; `&&`, `||` and `!` became
`and`, `or` and `not`, and `Solution::` took `.`. `*k += 1` through the
picked `mut ref`, `*x > w` and `x.clone()` were accepted as written.
