# 839. Similar String Groups

Two strings `X` and `Y` are similar if swapping two letters of `X`, at
two different positions, makes it equal to `Y`, and also if they are
equal. `"tars"` and `"rats"` are similar (swap positions 0 and 2), and
so are `"rats"` and `"arts"`, but `"star"` is similar to none of the
three. Similar strings join into groups: a word is in a group if it is
similar to at least one other word of the group, so `{"tars", "rats",
"arts"}` and `{"star"}` are two groups even though `"tars"` and `"arts"`
are not similar. Given a list `strs` in which every string is an anagram
of every other, return the number of groups.

```
strs = ["tars","rats","arts","star"]  ->  2
strs = ["omv","ovm"]                  ->  1
```

**Constraints:** `1 <= strs.length <= 300`, `1 <= strs[i].length <=
300`, every word holds only lowercase letters, and all the words are the
same length and anagrams of each other.

## Approaches

Every arm compares words letter by letter; they differ in how they
decide a pair is similar and how they find the groups.

| file | mechanism |
|---|---|
| `similar_string_groups.kara` ★ | union-find: every pair compared once, stopping at a third difference, and a pair that differs in no position or in two joins its groups, in a forest with path halving. As anagrams, two words cannot differ in one position, and two differences always hold each other's letters. O(n^2 m) |
| `similar_string_groups_dfs.kara` | depth-first search: the words are a graph with an edge between similar ones, and a recursive search from each word not yet seen marks its group. Similar here means no difference, or exactly two holding each other's letters, checked without leaning on the anagrams. O(n^2 m) |
| `similar_string_groups_labels.kara` | labels to a fixed point: each word lists the words similar to it and starts labelled with its own index, and pass after pass takes the smallest label among them, until a pass changes nothing; the groups are the words still labelled with their own index. O(n^2 m), then O(n^2) a pass |
| `similar_string_groups_swaps.kara` | every swap looked up, or every pair compared: when there are more words than the square of their length, each word's swaps are made and looked up in a `Map` from word to index, joining the earlier words equal to it or to a swap; otherwise every pair is compared in full. Union-find with recursive path compression. O(n m^3) or O(n^2 m) |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 18 lines: LeetCode's two examples; eleven more
(one word, two equal words, a pair of letters swapped, three equal words
of one letter, two words apart in four positions and then the same two
joined by a word between them, every arrangement of `abc`, the three
rotations of `abc`, none a swap of another, the arrangements of `aab`,
five words in two groups, and two pairs of equal words); three lists of
LeetCode's most and longest words, 300 of 300 letters, each word an
earlier one with one swap or, once in 4, 2 or 1 words, with more, shown
by their number of groups; 300 words of 8 letters, more than the square
of their length; and 300 random lists of up to 20 words of up to 10
letters with their total groups and a checksum.
`similar_string_groups.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: two words are similar when they are equal or when one of the
swaps of the first, at every pair of positions, gives the second, and
the groups come from the closure of that relation, each counted at its
first word. Its 1,600 cases come in four kinds of 400, each list a
family of words in which each is an earlier one with a few swaps: up to
8 words of up to 5 letters; families that seldom jump, so that the
groups are large; families where every word jumps, so that they are
small; and more words than the square of their length, up to 3 letters,
where the swaps arm looks its swaps up. The letters come from the first
1 to 6 of the alphabet, so that repeated letters and equal words are
common.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the words in the opposite order give the same answer |
| P3 | every word given twice gives the same answer |
| P4 | every word read backwards gives the same answer |
| P5 | the same letter put before every word gives the same answer |

It prints `1600 cases, 32000 checks over 4 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: two words similar at three differences | P1 80 |
| M2 | ★: a pair already in one group counted again | P1 1313, P3 1481 |
| M3 | ★: the first letter not compared | P1 524, P4 186, P5 524 |
| M4 | dfs: the search going on only to later words | P1 92, P2 177 |
| M5 | dfs: the swapped letters looked for in the same word | P1 736 |
| M6 | dfs: a third difference ignored | P1 59, P4 20 |
| M7 | labels: one pass only | P1 92, P2 177 |
| M8 | labels: the comparison stopping at the second difference | P1 101 |
| M9 | labels: only the earlier similar words listed | P1 92, P2 177 |
| M10 | swaps: a word not joined with an equal earlier word | P1 625, P2 128, P3 967, P5 336 |
| M11 | swaps: the last position never swapped | P1 237, P3 126, P4 4, P5 174 |
| M12 | swaps: a pair compared at three differences similar | P1 80, P3 2 |

P1 kills all twelve. M1, M5 and M8 only P1 sees, and M6 and M12 nearly
so: an arm that takes the wrong pairs for similar does so in whatever
order and however often the words come. M4, M7 and M9 fail the same 269
checks: each follows the similar words only from earlier to later, so
each splits a group whose words are joined only through a later one, and
P2, the words reversed, turns that round. P3 sees the edits that count
an equal word wrongly: M2 counts every copy as a new join, and M10 never
joins a copy in the swaps arm. P4, the words backwards, sees the edits
tied to one end of the word (M3, M6, M11), and P5 sees M3, whose first
letter is now the same in every word, and M10 and M11, because a word
one letter longer can move the swaps arm from looking its swaps up to
comparing pairs. M6 is the weakest kill, 79 checks: it needs two words
whose first two differences hold each other's letters and that differ
again later. A first P5 renamed every letter, `a` to `z` and so on, and
killed none of the twelve: every arm and every edit looks at letters
only to see whether two are equal, and a renaming keeps those answers.

## Verification

Every arm prints the same output as `similar_string_groups.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `4a744e1ec3`, and the runtime archives are
current with them. Under `karac __mir-run` the ★, search and labels arms
take 1.8 to 4.1 s, the swaps arm 15 s (it compares every letter of every
pair of the long words), and the differential 9.3 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends do not run this kata. `karac run --interp`,
`karac run` and `karac build` all refuse every arm, the differential and
the bench program as moving a `Vec` out of an index (`words[i]` passed
to a parameter), which v2's borrowing parameters do not do. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 16
cases once, each LeetCode's most and longest words, 300 of 300 letters:
the first word of case `g` is random, and each later one is an earlier
word with one swap, or with three once in `1 + g % 4` words. Each of 500
rounds counts the groups of the next case. Every implementation prints
`500 rounds of 16 cases: 77190 groups, checksum 691103922`, the Kāra
program under `karac __mir-run` included, in 250 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.01 to 1.06 s |
| Rust (`rustc -O`) | 1.20 to 1.30 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.19 to 1.28 s |
| Go | 1.68 to 1.84 s |
| Python | 33.7 to 34.3 s |
| Kāra (`karac build --mir`) | 1.25 to 1.31 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 1.26 s, against Rust's
1.24 (1.24 under overflow checks), C's 1.04 and Go's 1.77: 1.02 times
Rust's time under overflow checks, 1.2 times C's, and 0.71 times Go's.
Under valgrind's cachegrind C runs 3.7 billion instructions and 1.16
billion branches, Rust 7.0 and 2.48 billion and v2 7.9 and 2.68 billion;
the three mispredict about alike, 90, 98 and 100 million branches. Most
likely the gap to C is the bounds check on each letter compared, which
Rust pays as well (not traced). Built for `x86-64-v3`, the target `karac
build` uses, C takes 0.98 to 1.06 s and Rust with overflow checks 1.21
to 1.25 s, against v2's 1.22 to 1.30 s in the same five interleaved
runs. Python takes 34 s, about 33 times C's time. The comparison with C
and Rust waits until after M4.

## Compiler findings

None on v2: every arm, the differential and the bench program pass
`karac check` and run on both v2 backends as written.
