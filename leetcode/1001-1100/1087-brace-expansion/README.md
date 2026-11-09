# 1087. Brace Expansion

You are given a string `s` representing a list of words. Each letter in
the word has one or more options.

- If there is one option, the letter is represented as is.
- If there is more than one option, then curly braces delimit the
  options. For example, `"{a,b,c}"` represents options `["a", "b", "c"]`.

For example, if `s = "a{b,c}"`, the first character is always `'a'`, but
the second character can be `'b'` or `'c'`. The original list is
`["ab", "ac"]`.

Return all words that can be formed in this manner, sorted in
lexicographical order.

```
s = "{a,b}c{d,e}f"  ->  ["acdf","acef","bcdf","bcef"]
s = "abcd"          ->  ["abcd"]
```

**Constraints:** `1 <= s.length <= 50`; `s` consists of curly brackets
`'{}'`, commas `','`, and lowercase English letters; `s` is guaranteed
to be a valid input; there are no nested curly brackets; all characters
inside a pair of consecutive opening and ending curly brackets are
different.

The arms take the pattern as a `Str` and return the words as a
`Vec[String]`.

## Approaches

| file | mechanism |
|---|---|
| `brace_expansion.kara` ★ | the pattern read once, `match` on each `char`, into its groups, each a sorted `Vec[char]` (an `Option[Vec[char]]` holds the open group, and a letter alone is a group of one); the words built by a depth-first walk over one `mut ref String`, pushing and popping a letter, that takes each group's letters in order, so they come out sorted. O(total length of the words) |
| `brace_expansion_bfs.kara` | breadth first: the words start as one empty word, and each group, cut out as `String`s with `find("}")` and `split(",")` and sorted, makes a new list of every word followed by every letter (`f"{w}{l}"`). O(total length of the words) |
| `brace_expansion_text.kara` | recursion on the text: with no `{` left the text is its only word; otherwise the part before the first `{`, each letter of its group, and each word of the rest after the `}`; the words sorted at the end. O(w log w) for w words |
| `brace_expansion_odometer.kara` | an odometer: the groups read as sorted byte lists, one wheel each, and the k-th word, for k from 0 to the product of their sizes, read off the wheels in mixed radix with the last turning fastest, so the words come out sorted (`Vec.filled`, `String.from_utf8`). O(total length of the words) |
| `brace_expansion_set.kara` | the words gathered in a `SortedSet[String]`: each group, its letters in the order written, extends every word so far into a new set, and the set is walked once at the end. O(w log w) for w words |
| `brace_expansion_solution.kara` | LeetCode's Rust template (`struct Solution;`, `s.chars().collect()` into a `Vec<char>`, a `Vec<Vec<char>>` of groups, `vec![chars[i]]`, an associated `fn dfs(groups: &Vec<Vec<char>>, i: usize, cur: &mut String, res: &mut Vec<String>)`, `for &c in &groups[i]`, `Self::dfs(&groups, 0, &mut cur, &mut res)`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples and eight
more; the words and a checksum over 300 random patterns of up to 50
characters (`300 random patterns: 5445 words, checksum 943556290`); and
seven groups of three, the most words a pattern of 50 characters can
hold (`2187 words, first adgjmps, last cfiloru, checksum 178540527`).
`brace_expansion.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every word the pattern can form, built in the order the
letters are written, and then the words put in order by taking out the
least of those left, again and again. It checks 2000 problems: 1000
patterns of up to 14 characters over the first 1 to 3 letters, so that
groups of one and letters repeated across groups are common, and 1000 of
up to 24 characters over the first 1 to 6; each comes with a second pattern of up to 10
characters for P6. Every random choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every group's letters written in reverse answer the same |
| P3 | each letter alone written as a group of one, `{x}`, and each group of one unwrapped, answer the same |
| P4 | every letter moved by a random map into a to z that keeps the order of the six letters a pattern can use moves the answer's letters the same way |
| P5 | there are as many words as the product of the group sizes, each as long as there are groups, and each word is less than the next |
| P6 | the pattern p followed by q answers each word of p's followed by each word of q's, in that order |

All 72,000 checks pass on every arm: `2000 problems: checksum 379468437,
72000 checks over 6 arms: 0 failures`. A Python reading of the same
problems, with `itertools.product` over the sorted groups, gives the same
checksum.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Twenty-nine are caught,
each the same way under both backends, and the thirtieth runs out of
time under both (the breadth-first arm closing every group at the first
`}`, which never moves past the second group). Fifteen are kept, no two
failing the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a group left as written | P1 805, P2 1042, P5 805 |
| M2 | ★: each word given twice | P1 2000, P5 2000, P6 2000 |
| M3 | ★: a letter alone dropped | P1 1653, P3 1720, P5 1653 |
| M4 | bfs: each letter put in front | P1 1157, P5 450, P6 1492 |
| M5 | bfs: the closing brace read as a letter | P1 1679, P3 1861, P5 1679 |
| M6 | bfs: the new letter turning slowest | P1 450, P5 450, P6 618 |
| M7 | text: the part before a group dropped | P1 987, P3 1139, P5 987, P6 835 |
| M8 | text: the group's letter put after the rest | P1 928, P3 950, P6 1234 |
| M9 | text: the rest not expanded | P1 1030, P2 590, P3 1490, P5 1030, P6 1365 |
| M10 | odometer: a wheel carrying one late | P1 796, P5 796, P6 814 |
| M11 | odometer: an `a` in a group dropped | P1 1454, P3 844, P4 488, P5 1454 |
| M12 | set: a letter alone added to the last group | P1 869, P3 1034, P5 869, P6 705 |
| M13 | set: each letter put in front | P1 1121, P6 1488 |
| M14 | set: the words walked backwards | P1 1042, P5 1042 |
| M15 | solution: a group's first letter only | P1 1042, P2 1042, P5 1042 |

P1 catches all fifteen, P5 thirteen, P6 nine, P3 seven, P2 three and P4
one. P5 misses M8 and M13 because both still give the right number of
distinct words of the right length, and both arms sort their words at
the end. P2 sees only the edits whose answer depends on the order a
group's letters are written in: M1 and M15 read a group as written, and
M9 leaves the rest of the pattern as text. P4 sees only M11, the one edit
that treats a letter by what it is rather than where it falls in the
order; every other edit moves with the relabelling. P6 sees the edits
that break how a word is put together from its parts, and P3 those that
treat a letter alone differently from a group.

Of the fifteen not kept, one runs out of time (above), four fail in ways
of their own but were not needed, and ten fail exactly as a kept edit.
A group left as written in the breadth-first, text (the words left
unsorted), odometer and solution arms fails as M1; the ★ arm's last
group never reached and the solution arm keeping every partial word as
M2; the solution arm reading `}` as a letter as M5; the odometer's first
wheel turning fastest, and its sizes added rather than multiplied, as
M6; and the set arm reading a comma as a letter as M14. The four not
needed are the ★ arm taking its letter back before going on, the text
arm dropping the text after the last group, a group in the set arm
keeping the last one's letters, and the solution arm never taking a
letter back.

## Verification

Every arm prints the same output as `brace_expansion.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file. Under `karac __mir-run` the differential takes 6 s.

The arms found no compiler gap; the bench found the performance one
below. Every file went through `karac fix`, which changed nothing
outside the Rust arm. The Rust arm reaches a clean check in three rounds
and gives the text the arm holds: first the syntax (`struct Solution
{}`, `<>` to `[]`, `::` to `.`, `Self::` to `Solution.`, `&str` to
`Str`, `&Vec` to `ref Vec`, `&mut T` to `mut ref T`, `for &c in
&groups[i]` to `for c in ref groups[i]`, and the first call's `&groups,
0, &mut cur, &mut res` to `groups, 0, mut cur, mut res`); then
`vec![chars[i]]` to `[chars[i]]`, `usize` to `i64`, and `mut` at the
recursive call's `cur` and `res`; then the `ref` dropped from `groups`,
as a parameter borrows unless it says otherwise.

## Benchmarks

The bench builds 2000 random patterns of up to 50 characters once,
pattern t over the first t % 6 + 1 letters. Each of 400 rounds expands
every pattern with the ★ arm, in an order that changes with the round,
folding each answer's length and the last letter of its middle word into
a checksum. Every implementation prints `400 rounds over 2000 patterns:
20187600 words, checksum 95123740`.

Each mirror keeps the ★ arm's steps in its own language's way: Rust over
`Vec<Vec<char>>` and a `String` it pushes and pops; Go over byte slices,
each group sorted with `sort.Slice`, each word copied out with
`string(word)`; C over fixed groups of up to 26 letters sorted by
insertion, each word copied into its own `malloc`; Python over lists and
`"".join`. Every mirror allocates each word afresh, as the Kāra arm's
`word.clone()` does.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `521196fb53`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.618 to 0.803 s | 0.657 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.639 to 0.727 s | 0.668 s |
| Rust (`rustc -O`) | 0.868 to 1.044 s | 0.946 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.875 to 1.060 s | 0.966 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.886 to 1.059 s | 0.970 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.162 to 1.385 s | 1.221 s |
| Kāra (`karac build`) | 1.132 to 1.370 s | 1.233 s |
| Go | 1.397 to 1.678 s | 1.555 s |
| Python | 7.65 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (1.22 s) is its real time.

The work is 20 million short words, each cloned into its own allocation,
pushed and later freed. Kāra is 26% behind Rust with overflow checks at
the same ISA, 29% behind plain `rustc -O`, and 21% ahead of Go; C takes
54% of Kāra's time; Python takes 6.3x. Kāra and Rust make the same
allocations (27.55 million blocks, 1.668 GB, under valgrind), so the gap
is not extra work. Under callgrind Kāra runs 1.31x Rust's instructions:
the walk itself about 26% more, and most of the rest in glibc's slow
path, where 14.8 million of Kāra's mallocs land against 2.7 million of
Rust's, and in `malloc_consolidate`, which Rust never reaches. Which of
Kāra's allocator calls empties the fast bins is not measured; kara
B-2026-11-09-43 records the profile.
