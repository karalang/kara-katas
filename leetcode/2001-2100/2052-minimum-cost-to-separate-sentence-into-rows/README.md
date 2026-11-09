# 2052. Minimum Cost to Separate Sentence Into Rows

You are given a string `sentence` of words separated by single spaces, and
an integer `k`. Separate `sentence` into rows, each row holding whole words
in their order, separated by single spaces, and no row more than `k`
characters long. A row of length `n` costs `(k - n)^2`, and the total cost
is the sum of the costs of every row except the last. Return the minimum
possible total cost.

```
sentence = "i love leetcode", k = 12                ->  36
sentence = "apples and bananas taste great", k = 7  ->  21
sentence = "a", k = 5                               ->  0
```

**Constraints:** `1 <= sentence.length <= 5000`; `1 <= k <= 5000`; the
length of each word is at most `k`; `sentence` holds only lowercase
letters and spaces, with no leading or trailing space and single spaces
between words.

The last row is free, so a layout's cost is decided by where its rows
break before the last one. Taking the rows from the front, each first row
is a run of words that fits, and the rest is the same problem again: a
table over the word where the rest starts, each entry the least over the
first rows that fit, each a step of at most `k / 2` words.

## Approaches

| file | mechanism |
|---|---|
| `separate.kara` ★ | dynamic programming from the end over the word lengths from `split(" ")`: `best[i]` is zero when the words from `i` on fit in one row, else the least over each first row that fits of `(k - width)^2 + best[j]`, the row grown word by word until it is too wide |
| `separate_memo.kara` | a memoized recursion over where the rest starts, its widths from prefix sums of the word lengths, each rest kept in a `Vec[Option[i64]]` |
| `separate_forward.kara` | dynamic programming from the front: `paid[j]` is the least cost of the first `j` words in rows all paid for, each row grown backwards from its end; the answer is the least `paid[s]` over each start `s` of a free last row that fits |
| `separate_dijkstra.kara` | a shortest path over the places between words, a row from one to another an edge costing `(k - width)^2`, or nothing when it ends the sentence; a `PriorityQueue` of (cost so far, place), cheapest first |
| `separate_text.kara` | the table from the end, measured in the text: each word's start found from the spaces in `chars().enumerate()`, a row as wide as the text from its first word's start to the space before the next row; each entry a `filter` and `map` over the row ends that fit, folded with `min` |
| `separate_solution.kara` | LeetCode's Rust template (`sentence.split(' ')` into word lengths `as i32`, a `vec![i32::MAX; n + 1]` table filled from the end, an inner `for` that `break`s once a row is too wide), carried by `karac fix` in two rounds to a clean check |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four more,
each sentence, `k` and its answer; then the sum and a checksum of the
answers for 2000 random sentences of 1 to 30 words up to 8 letters, `k`
at least the longest word; then for three sentences of about 5000
characters, the constraints' limit: short words in rows of 200, words up
to 14 letters in rows of 15, and 2500 one-letter words in rows of 2.
`separate.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to break the words into rows tried, as each subset of
the gaps between words, those with a row wider than `k` dropped, and each
costed by its rows but the last. It checks 500 random sentences of 1 to 12
words, drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is at least 0 and at most the cost of filling each row as full as it goes |
| P3 | the sentence with every letter changed, the word lengths kept, has the same answer |
| P4 | a word of `k` letters put first, a full row that costs nothing, leaves the answer the same |
| P5 | a word of `k` letters put last makes every other row paid for: the answer is the least cost with every row paid, read literally |
| P6 | each arm agrees with at least three of the other five |

The differential prints `500 sentences: checksum 793683377, 18000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-five edits to the differential, five to seven to each of its arms,
each run under `karac __mir-run` and `karac __mir-llvm-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last row paid for | P1 427, P2 424, P6 427 |
| M2 | ★: the spaces not counted | P1 340, P2 167, P4 500, P5 492, P6 340 |
| M3 | ★: the first word's row only one word | P1 363, P2 363, P4 363, P5 330, P6 363 |
| M4 | memo: widths counted without the last word's letters | P1 389, P2 389, P4 500, P5 500, P6 389 |
| M5 | memo: each first row only one or two words | P1 192, P2 192, P5 224, P6 192 |
| M6 | memo: a rest kept for every first word, the first one's | P1 214, P2 181, P5 394, P6 214 |
| M7 | forward: the free last row only the last word | P1 245, P2 245, P6 245 |
| M8 | forward: a row's cost its width, not its gap | P1 368, P2 361, P4 500, P5 481, P6 368 |
| M9 | forward: the first word left out of the free row | P1 111, P2 111, P4 111, P6 111 |
| M10 | Dijkstra: the dearest place taken first (`max_first`) | P1 305, P2 305, P5 272, P6 305 |
| M11 | Dijkstra: a row's gap counted with one letter less | P1 364, P2 81, P4 500, P5 486, P6 364 |
| M12 | Dijkstra: edges only to the next word | P1 412, P2 412, P5 412, P6 412 |
| M13 | text: the gap cubed | P1 200, P2 198, P5 403, P6 200 |
| M14 | text: the free last row taken from the start always | P1 313, P5 466, P6 313 |
| M15 | text: the dearest row taken (`max`) | P1 340, P2 340, P5 412, P6 340 |
| M16 | solution: the spaces not counted | P1 308, P2 47, P4 338, P5 479, P6 308 |
| M17 | solution: the adapter widening `k` by one | P1 384, P2 216, P4 500, P5 496, P6 384 |

P1 and P6 kill all seventeen, P2 sixteen, P5 fourteen and P4 eight. P3
kills none: no arm reads the letters, only where the spaces are. It
stands for a text arm that would, and is cheap. P2 compares with the
greedy layout, which is always possible, so an answer above it is too
dear: it misses only M14, which makes every sentence free, and that is
below. P4 puts a word as long as a row first: an arm that mismeasures a
row (M2, M4, M8, M11, M16, M17) gets that row wrong, and M3 and M9, which
treat the first word apart, now treat the long word apart instead. P5's
last long word makes every row of the sentence paid for; the edits that
get only the free row wrong (M1, M7, M9) pass it, since there the free row
is the long word alone, and the others fail it.

Of the thirty-five, eighteen were not kept. Five crash: when no row
fits, which the free last row never taken (memo), the spaces counted
twice (memo), the space before each word counted in its row, the next
word's start taken at the space, and the whole sentence free only if
exactly `k` wide (text) all reach, the least over no rows is `i64.MAX`,
and adding a cost to it overflows. One is equivalent: the shortest path
answering when the end is first reached rather than first taken, since the
place that reaches it first is the cheapest one that can reach it at all,
and the last row costs nothing.

The other twelve fail as a kept one does or as each other. The last row
paid for (forward, Dijkstra, Rust) fails as M1, and the memo arm's cost
cubed as M13. A row allowed one letter wider than `k` (★) and a row that
does not fit costed (Rust) fail the same way, as do the gap not squared
(★, Rust), and the last row taken as wide as possible (★) and the first
path found to a place kept (Dijkstra). The forward arm's last paid row
taken alone and a row grown backwards one letter too wide fail on checks
of their own.

## Verification

Every arm prints the same output as `separate.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error. `karac
run` and a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 0.7 s (★) to 4.7 s (text), and the
differential 9.3 s; on kara 3dcd076373.

The text arm was first written with Rust's `sentence.match_indices(" ")`
for the spaces, and refused: Kāra's strings have no `match_indices` (nor
`char_indices`), and the error, "no method 'match_indices' on type
'String'", names nothing to write instead. That is kara B-2026-11-09-51.
The arm takes the positions from `chars().enumerate()` instead, which
counts characters, the same as bytes for the sentence's lowercase letters.

The other four Kāra arms met no compiler gap and checked as written.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in two rounds of 4 and 3 edits to a clean check: `struct Solution;` to
`struct Solution {}`, `Vec<i32>` to `Vec[i32]`, `split(' ')` to `split(" ")`,
`vec![i32::MAX; n + 1]` to `Vec.filled(n + 1, i32.MAX)`, and `let mut len
= -1` to `let mut len: i32 = -1`, since the literal no longer took its type
from the `i32` lengths added to it. The adapter hands the harness's `i64`
`k` to it `as i32` and widens the `i32` cost back.

## Benchmarks

The bench answers 600 sentences of about 5000 characters, the
constraints' limit, of words up to 10 letters, with rows from 20 to 4000
wide, with the ★ arm in all five languages. Building the sentences is part
of the work timed, a character pushed at a time in every language. The C
mirror reads the word lengths off the text at each space instead of
splitting it. Every implementation prints `600
sentences: sum 71608, checksum 633704365`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `3dcd076373` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.101 to 0.141 s | 0.103 s |
| Rust (`rustc -O`) | 0.119 to 0.149 s | 0.121 s |
| Go | 0.178 to 0.185 s | 0.179 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.231 to 0.286 s | 0.252 s |
| Kāra (`karac build`) | 0.267 to 0.295 s | 0.273 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.270 to 0.343 s | 0.278 s |
| Python | 19.3 s |  |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.270 s) is not above its real time (0.273 s).

The sequential Kāra program is 1.10x Rust under overflow checks and 2.69x
C. The inner loop is checked arithmetic, a sum and a square per word, so
overflow checks cost Rust twice its unchecked time here, and Kāra checks
by default.

A first version of the Kāra bench built each sentence with
`push_str(letters.substring(at, at + 1))`, a new `String` per letter, while
the mirrors push a character; that alone took 71 ms of its run against
Rust's 12 ms. It now pushes a `char` as they do.
