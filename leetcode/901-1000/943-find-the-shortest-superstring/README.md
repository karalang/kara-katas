# 943. Find the Shortest Superstring

Given an array of strings `words`, return the smallest string that
contains each string in `words` as a substring. If there are multiple
valid strings of the smallest length, return **any of them**.

You may assume that no string in `words` is a substring of another
string in `words`.

```
words = ["alex","loves","leetcode"]                  ->  "alexlovesleetcode"
words = ["catg","ctaagt","gcta","ttca","atgcatc"]    ->  "gctaagttcatgcatc"
```

**Constraints:** `1 <= words.length <= 12`; `1 <= words[i].length <=
20`; `words[i]` consists of lowercase English letters; all the strings
of `words` are unique.

## Approaches

No word lies inside another, so a shortest superstring writes the words
one after another in some order, each overlapping the one before as far
as it can. Every arm first measures, for each pair of words, how far the
end of one overlaps the start of the other, and then looks for the best
order.

| file | mechanism |
|---|---|
| `shortest_superstring.kara` ★ | for every set of words and the word it ends with, the most letters an order of that set can save, built from the set without its last word, with the word before kept; the best order read back through the words before. O(2^n n^2) |
| `shortest_superstring_memo.kara` | the shortest string that starts with a given word and holds a given set, worked out recursively: that word cut where it overlaps the next, followed by the shortest string that starts with the next word and holds the rest, the next word tried every way; each set and first word's string kept in a table so it is worked out once. O(2^n n^2) steps, each joining strings |
| `shortest_superstring_paths.kara` | shortest paths over states, a set of words written and the word written last, writing one more word costing its letters less its overlap with the last; the first state holding every word to come off a `PriorityQueue`, lowest cost first, is the answer (Dijkstra), read back through the state each was reached from. O(2^n n^2 log) |
| `shortest_superstring_forward.kara` | for every set and last word the least length of a string writing them, each set's lengths pushed forward to the sets one word larger; no word before is kept, and the order is read back by finding at each step a word whose length plus the cost of the step gives exactly the length reached. O(2^n n^2) |
| `shortest_superstring_search.kara` | every order tried depth first, cut wherever the set written so far and its last word have been reached before at no greater length, and wherever the length so far is already no shorter than the best whole string found. Exponential in the worst case |
| `differential.kara` | the five arms against the statement read literally, six properties |

The arms may give different strings of the same length, so every arm
prints the same 13 lines of lengths and verdicts rather than its
strings, each string checked to hold every word: LeetCode's two
examples and six more (one word, three words that chain, the same three
in another order, three that overlap nothing, three over `a` and `b`,
and three windows of `abcabc`); for 300 random sets of up to 8 words of 1
to 6 letters from the first 2 to 4 of the alphabet, with any word equal
to or inside another dropped, the words, the letters and a checksum of
the lengths; and four of LeetCode's largest, 12 words of 20 letters:
random letters from `a` and `b`, twelve windows of one string of 31
letters in a mixed order, twelve words that overlap nothing, and random
letters from all 26. `shortest_superstring.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the strings of `a` and `b` of each length in turn, from the
longest word up, until one holds every word. It checks 3,200 random
sets with any word equal to or inside another dropped: 3,000 of up to 4
words of 1 to 3 letters of `a` and `b`, against the statement, and 200
of up to 9 words of up to 20 letters from the first 2 to 25 of the
alphabet, against the other properties; 5,595 words of 20,022 letters.

| | property |
|---|---|
| P1 | holding every word, at the statement's length, on the small sets |
| P2 | holding every word |
| P3 | every letter in some word of the set, and no longer than all of them written one after another |
| P4 | each word reversed gives a string holding them, of the same length |
| P5 | the words in a random order, with their letters renamed by a random shuffle of the alphabet, give the same length; and one more word of 1 to 4 `z`'s, which no word uses, gives that much more |
| P6 | each arm agrees with at least two of the other four on the length |

It prints `3200 sets of 5595 words of 20022 letters, checksum 755900764,
95000 checks over 5 arms: 0 failures` under `karac __mir-run` (25 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an overlap of one letter never found | P1 687, P6 799 |
| M2 | ★: each overlap read the wrong way round | P1 607, P4 71, P5 51, P6 728 |
| M3 | ★: overlaps measured from the start of the first word | P1 594, P2 715, P3 523, P4 713, P5 726 |
| M4 | memo: the longest string kept | P1 183, P4 24, P5 577, P6 302 |
| M5 | memo: only the first two words tried first | P1 22, P4 83, P5 55, P6 41 |
| M6 | memo: the table keyed by the set alone | P1 323, P2 122, P3 109, P4 700, P5 465, P6 387 |
| M7 | paths: every start costing nothing | P1 43, P4 139, P5 68, P6 75 |
| M8 | paths: each state kept as first reached | P1 7, P4 22, P5 10, P6 17 |
| M9 | paths: the costliest state first | P1 407, P4 614, P5 404, P6 511 |
| M10 | forward: every first word costing nothing | P1 43, P4 139, P5 68, P6 74 |
| M11 | forward: each length kept as first reached | P1 56, P4 130, P5 125, P6 141 |
| M12 | forward: the last word never the end | P1 265, P4 485, P5 389, P6 269 |
| M13 | search: a state cut whenever seen | P1 47, P4 126, P5 397, P6 130 |
| M14 | search: each step counted with no overlap | P1 322, P4 672, P5 409, P6 423 |
| M15 | search: only orders from the first word | P1 257, P4 584, P5 330, P6 303 |

P1 kills all fifteen, P4, P5 and P6 fourteen each, and P2 and P3 two.

P2 and P3 kill only M3 and M6. Every other mistake still writes the
words in some order, each joined at its true overlap with the one
before, so the string holds every word with no letter outside one; it
is only longer than it need be. M3 measures how far the start of one
word overlaps the end of the next, which is the true overlap of the
pair the other way round, and joins the words at it, cutting letters
that belong to them; M6 hands back, for a set, a string that may start
with a different word from the one asked for, and joins it as though it
did.

P6 misses M3. Its overlaps are those of each pair the other way round,
so the order it finds saves as much as the best order written backwards,
and its string has the right length even though it does not hold the
words.

P4 and P5 miss M1, which never finds an overlap of a single letter. That
mistake is the same with every word reversed, the words reordered and
renamed, or a word of `z`'s added, which overlaps nothing, so the arm
agrees with itself; P1 and P6 compare it with something else.

M7 and M10 make the same mistake in two arms, every first word costing
nothing, and fail every check the same number of times but one: P6's
count differs by one. Why was not worked out.

Thirteen other edits were tried and set aside. Four failed exactly the
same checks as each other, in two pairs, so none of them was kept: ★
choosing the order ending where least is saved and forward choosing the
one ending at the longest; and ★ and forward joining each word at the
other pair's overlap. Six were sound but beyond three an arm (★ taking
the word before from outside the set, memo cutting each word at the
wrong overlap and never taking the last word next, paths overlapping
each step the wrong way round and reaching each state from where it was
first reached, and search overlapping each step the wrong way round).
Two crashed: forward pushing lengths only to later words, whose
unreached end states stay at -1, look least, and leave its walk back
with no word before, so the walk runs past the last word and overflows
a shift; and search taking an order one word short, with an index out
of bounds. One was equivalent: forward counting each first word one
letter short, which shortens every length alike.

## Verification

Every arm prints the same output as `shortest_superstring.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 0.6 to 3.1 s each and the
differential 25 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

Legacy refuses all five arms where the harness's `verdict` passes its
`ref` parameter on to the arm ("expected 'Vec[String]', found 'ref
Vec[String]'"), and the bench program at
`shortest_superstring(sets[(r + i) % count])`, a move out of an index
("cannot move ... out of an index"); v2's borrowing parameters make both
a borrow. It refuses the differential at the first `*` on an element of
a `Vec`'s `.iter()` ("unary '*' requires 'ref T', ..."), legacy's older
rule, under which the element is a copy. Legacy is frozen, so none of
this is filed.

## Benchmarks

The bench program builds 40 sets of 12 words of 20 letters once,
LeetCode's largest, each word of random letters from the first 2 to 4
of the alphabet and no two alike; in each of 10 rounds it runs the ★ arm
on every set, each round starting from a different one, and folds the
letters of every answer into a checksum. Every implementation prints
`10 rounds over 40 sets of 12 words of 20 letters: lengths adding to
85250, checksum 424678368`, so every one writes the same strings. Kāra
compares each overlap through two `substring` copies, as the ★ arm does;
C compares in place with `memcmp`, and Rust, Go and Python by slices.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.50 to 0.59 s | 0.53 s |
| Rust (`rustc -O`) | 0.61 to 0.69 s | 0.63 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.67 to 0.76 s | 0.70 s |
| Go | 0.83 to 1.00 s | 0.86 s |
| Python | 13.4 s | |
| Kāra (`karac build --mir`) | 0.66 to 0.92 s | 0.70 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about 25 times C's.

v2 takes 1.00 times Rust's median time under overflow checks and 1.32
times C's. Under valgrind's cachegrind v2 runs 3.08 billion
instructions and 1.03 billion branches with 89 million mispredicted,
Rust with overflow checks 2.56 billion, 1.06 billion and 87 million,
and C 1.03 billion, 0.54 billion and 46 million. v2 and Rust mispredict
about as often; that nearly all of it is the inner loop over the word
before, that C's half as many
branches and mispredictions come from turning the keep-the-larger test
into a conditional move, and that v2's 8.9 million indirect branches,
against 1.0 million in Rust, are the `substring` copies its overlaps
allocate, are inferred, not profiled.
