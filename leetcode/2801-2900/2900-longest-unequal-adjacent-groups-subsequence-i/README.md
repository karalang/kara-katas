# 2900. Longest Unequal Adjacent Groups Subsequence I

You are given a string array `words` and a **binary** array `groups`,
both of length `n`, where `words[i]` is associated with `groups[i]`.

Your task is to select the **longest alternating** subsequence from
`words`. A subsequence of `words` is alternating if for any two
consecutive strings in the sequence, their corresponding elements in
the binary array `groups` differ. Essentially, you are to choose
strings such that adjacent elements have non-matching corresponding
bits in the `groups` array.

Formally, you need to find the longest subsequence of an array of
indices `[0, 1, ..., n - 1]` denoted as `[i0, i1, ..., ik-1]`, such
that `groups[ij] != groups[ij+1]` for each `0 <= j < k - 1` and then
find the words corresponding to these indices.

Return *the selected subsequence. If there are multiple answers, return
**any** of them.*

```
words = ["e", "a", "b"],      groups = [0, 0, 1]     ->  ["e", "b"]
words = ["a", "b", "c", "d"], groups = [1, 0, 1, 1]  ->  ["a", "b", "c"]
```

**Constraints:** `1 <= n == words.length == groups.length <= 100`;
`1 <= words[i].length <= 10`; `groups[i]` is either `0` or `1`; `words`
consists of **distinct** strings; `words[i]` consists of lowercase
English letters.

## Approaches

| file | mechanism |
|---|---|
| `words.kara` ★ | a run of one group can give the subsequence at most one word, and one word from every run alternates, so the longest takes one word per run. The first of each run is taken: the very first word, and each word whose group differs from the word before it |
| `words_filter.kara` | the ★ arm's first of each run as one iterator chain: the indices filtered and mapped to their words |
| `words_runs.kara` | the words and groups walked together with `zip`, the group of the last word taken kept as an `Option[i64]`, and a word taken whenever its group is not that one |
| `words_dp.kara` | as a longest-path problem, with no insight about runs: the longest subsequence starting at each word, one more than the best over the later words of the other group, then the earliest word that starts a longest one and each next the earliest of the other group that still reaches the length |
| `words_solution.kara` | a Rust solution as LeetCode's Rust users write it: `vec![words[0].clone()]`, then each later word whose group differs from the one before, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

The statement accepts any longest subsequence. Every arm here returns
the same one, the earliest indices, so that their outputs compare
exactly; the differential checks what the statement asks of any answer
as well. Taking one word per run was checked first against every
subsequence of 3000 random cases of up to 10 words in Python, before
any arm was written.

Every arm prints the same 4 lines: LeetCode's two examples; 100 words,
LeetCode's most, in one group, in groups taking turns, and in runs of
three, as the three lengths and two of the words chosen; then 3000
random cases of 1 to 8 words with random groups, and 1000 of 100 words
in runs of a group up to 5 long, as a count of the words chosen and a
checksum over them. Each word is a random letter and then its index in
base 26, so the words are distinct. `words.py` mirrors the ★ arm and
its output is byte-identical.

```
e b | a b c
1 100 34: ia pvd
3000 small cases: 8217 words chosen, checksum 71186411
1000 cases of 100: 33593 words chosen, checksum 603472237
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every nonempty set of indices tried as a bit mask,
kept when no two neighbours in it share a group, and the longest kept,
the earliest indices among equals. It draws 2000 random cases of 1 to 8
words with random groups, then 50 of up to 3000 words, past LeetCode's
100, in runs of a group up to 5 long, all before any arm answers; the
literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 8 words, the answer is the literal reading's |
| P2 | the answer is a subsequence of the words, no two neighbours in it of one group |
| P3 | one word for each run of a group |
| P4 | the groups flipped: the same answer |
| P5 | a word added at the end in the last word's group: the same answer; in the other group: that word added to it |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, 27874 words chosen: checksum
104565009, 61500 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python search over the same cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, three to the longest-path arm, two each
to the ★ arm, the filter and the `zip` walk, and one to the solution,
each run under `karac __mir-run` and `karac __mir-llvm-run`. All ten
are killed, each the same way under both backends. A first draft of M2
crashed with an index out of bounds before any property was asked, and
was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each group compared with the first word's | P1 1237, P2 1059, P3 1048, P5 916, P6 1287 |
| M2 | ★: the last word always taken | P1 886, P2 921, P3 921, P5 2050, P6 921 |
| M3 | filter: the words that keep their group taken | P1 1732, P2 1343, P3 1492, P5 2050, P6 1782 |
| M4 | filter: the first word never offered | P1 2000, P3 2050, P6 2050 |
| M5 | runs: the last group never moved on | P1 1484, P2 1534, P3 1534, P5 2050, P6 1534 |
| M6 | runs: a word taken when its group repeats | P1 1732, P2 1529, P3 1422, P5 1134, P6 1782 |
| M7 | dp: the last later word's length taken, not the best | P1 581, P3 631, P5 1049, P6 631 |
| M8 | dp: the next word never a neighbour | P1 846, P3 895, P5 1347, P6 895 |
| M9 | dp: every length one short | P1 1478, P3 1528, P5 2050, P6 1528 |
| M10 | solution: the second word never offered | P1 860, P2 616, P3 869, P5 268, P6 869 |

## Benchmarks

The bench draws 10000 cases of 100 words, LeetCode's most, in runs of a
group up to 5 long, all first, then answers each 20 times by the ★ arm
in all five languages, every chosen word copied into the answer: a
`clone` in Kāra and Rust, a fresh allocation in C, a copy through a
byte slice in Go, whose strings would otherwise be shared, and the
shared string itself in Python, which has no cheap way to copy one.
Every implementation prints `10000 cases of 100, 20 rounds: 6746440
words chosen, checksum 936628226`.

BENCHTAB

## Verification

All five arms print the same output as `words.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as written. The harness did not at
first. It printed the examples with `f"{one.join(\" \")}"`, quotes
escaped inside the interpolation as the string around it would need;
the check refuses that, says string literals inside an interpolation
take plain quotes, and the fix writes `{one.join(" ")}`. Then the check
warned that the harness's `words.clone()`, passed to a function whose
parameter only borrows, copies for nothing, and the clones went. The
bench's `bytes()[0] as i64` drew the lossless-cast warning, and the cast
went.

LeetCode's Rust template took one `karac fix` run, the wrapper
included, and the diff shows these: `struct Solution {}` came for the
`impl`; `Vec<..>` became `Vec[..]`; `vec![words[0].clone()]` became the
list literal `[words[0].clone()]`, the `Vec` the binding goes on to
`push` to; `|&g|` lost its `&`, and `Solution::` took `.`.
