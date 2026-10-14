# 583. Delete Operation for Two Strings

Given two strings `word1` and `word2`, return the minimum number of
steps required to make `word1` and `word2` the same. In one step, you
can delete exactly one character in either string.

```
word1 = "sea", word2 = "eat"            ->  2   ("sea" to "ea", "eat" to "ea")
word1 = "leetcode", word2 = "etco"      ->  4
```

**Constraints:** `1 <= word1.length, word2.length <= 500`; `word1` and
`word2` consist of only lowercase English letters.

## Approaches

Every arm is `fn min_distance(word1: String, word2: String) -> i64`.

| file | mechanism |
|---|---|
| `min_distance.kara` ★ | the longest common subsequence, in a table over every pair of prefixes of the two words collected into `Vec[char]`; the letters it keeps are the ones not deleted, so the answer is m + n - 2 * lcs; O(m * n) |
| `min_distance_direct.kara` | the deletions counted directly: an empty prefix costs the other's length, equal last letters cost nothing more, and otherwise the cheaper of the two last letters is deleted; O(m * n) |
| `min_distance_rows.kara` | the ★ arm's table kept one row at a time, over `bytes()`; O(m * n) time, O(n) space |
| `min_distance_memo.kara` | the deletions for the letters from i on and from j on, by recursion, each pair worked out once and kept in a `Map[(i64, i64), i64]`; O(m * n) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 14 lines: nine pairs at the edges (the two
examples, the same word twice, no letter in common, one letter alike and
not, one word a subsequence of the other, a word and its reverse, and
repeated letters), a count and checksum over 300 random pairs of 1 to
12 letters from the first 2 to 4 of the alphabet, and the problem's
largest, two words of 500: random over all 26 letters and over two, the
same word twice, and 500 of `a` against 500 of `b`. `min_distance.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: what is left of word1 after its deletions
is one of its subsequences, each tried in turn by a bitmask, and it must
be a subsequence of word2 as well; the fewest deletions keep the longest
such string. Each arm is held to the properties below on 1,000 random
pairs of 1 to 8 letters from the first 2 or 3 of the alphabet.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | at least the difference in length, at most m + n, and m + n less the answer is even |
| P3 | swapping the two words changes nothing |
| P4 | reversing both words changes nothing |
| P5 | the same letter put on the end of both changes nothing |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac
__mir-llvm-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the letter of word2 never skipped | P1 455, P3 645, P4 442 |
| M2 | ★: a matched letter of word2 matched again | P1 460, P2 210, P3 724, P5 181 |
| M3 | direct: an empty word1 costs nothing | P1 677, P2 537, P3 819, P4 431 |
| M4 | direct: a deletion counted twice | P1 838, P2 524, P4 656 |
| M5 | rows: the letter of word2 never skipped | P1 455, P3 645, P4 442 |
| M6 | rows: a matched letter of word1 matched again | P1 513, P2 249, P3 724, P5 207 |
| M7 | memo: word2's rest not deleted | P1 679, P2 545, P3 826, P4 431, P5 356 |
| M8 | memo: the dearer deletion taken | P1 714, P4 559, P5 709 |
| E1 | ★: the max taken the other way round | 0 |
| E2 | direct: equal letters may be deleted too | 0 |
| E3 | rows: each row started as a copy of the one before | 0 |
| E4 | memo: the memo never consulted | 0 |

M1 and M5 are the same edit to the same table, the ★ arm's in full and
the rows arm's one row at a time, and fail on the same cases. Neither
fails P2 or P5: the table can only lose matches, so the answer stays in
bounds and of the right parity, and a letter put on the end of both
words is matched on the diagonal, adding one to the table whatever came
before. M2 and M6 are mirror images, one letter of one word matched with
several of the other, so their answers can fall below the bounds;
reversing both words reverses those matches too, so P4 sees neither.
M4 and M8 treat the two words alike, so P3 does not see them, and
M8 stays within P2 because every path its recursion follows is still a
real sequence of deletions, only not the shortest. E2 is safe because
keeping two equal last letters is never worse than deleting one,
E3 because every cell of a row but the first is written before it is
read and the first is 0 in every row, and E4 because no pair (-1, -1) is
ever stored, so the memo is never hit and the arm only works harder.

## Verification

The four arms print the same output as `min_distance.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and run
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes on every arm, the differential and the bench program.

The frozen legacy backends split. `karac run --interp` prints the same
output for the ★, direct and rows arms, and refuses the memo arm and the
differential at type checking: they read `*known` out of the map and
`*c` out of `iter()`, and legacy gives each as a value where v2 gives a
reference ("unary '*' requires 'ref T' ... found 'i64'"). `karac run`
and `karac build` refuse all four arms and the differential: the memo
arm and the differential on that same `*`, the ★ and direct arms in
codegen on `lcs[i - 1][j].max(...)` and `cost[i - 1][j].min(...)`
("chained indexed receivers ... are deferred to v1.x"), and the rows arm
in codegen on the harness's `word1.to_string()` on a `Str` parameter
("no handler for method 'to_string'"). Legacy is frozen, so this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 40 pairs of words once, each
word 500 letters (the problem's most) from the first 2 to 26 of the
alphabet; then 30 times over every pair is answered. Every
implementation prints `40 pairs of 500 letters, 30 rounds:
602220 deletions, checksum 213239199`, the Kāra program under `karac
__mir-run` included (258 s).

Each call collects both words into arrays of characters and allocates
the table one row at a time, as the Kāra arm does: a `Vec<char>` and a
`Vec<Vec<i64>>` in Rust, a `[]rune` and a slice of slices in Go, and
lists in Python. C copies each word into a fresh array of code points
and `calloc`s each row of the table. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.17 to 1.40 s |
| Rust (`rustc -O`) | 1.41 to 1.61 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.38 to 1.59 s |
| Go | 1.55 to 1.85 s |
| Python | 50.1 to 50.2 s |
| Kāra (`karac build --mir`) | 0.78 to 1.03 s |

The legacy `karac build` refuses this program on the same chained index.
So `bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`f6052c659c`, and the compiled rows were timed again back to back,
interleaved, with the same result. Under `karac __mir-llvm-run` the
program prints the same line in 4.8 s, compile included; that JITs the
MIR's IR without optimization passes, so it is not a benchmark.

The Kāra row is the fastest, about two thirds of C's time and three
fifths of Rust's. Where that lead comes from is not measured; the loop's
two tests, equal letters and the larger neighbour, are on random
letters, so how each compiler turns them into branches or selects is the
first place to look.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
