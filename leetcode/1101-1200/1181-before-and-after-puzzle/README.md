# 1181. Before and After Puzzle

Given a list of `phrases`, generate a list of Before and After puzzles.

A phrase is a string of lowercase English letters and spaces only, with no
space at the start or end and no two spaces in a row. A Before and After
puzzle is a phrase made by merging two phrases where the last word of the
first is the first word of the second, that word written once.

Return the puzzles that can be formed by every two phrases `phrases[i]` and
`phrases[j]` where `i != j`, in both orders, as a list of distinct strings
sorted lexicographically.

```
["writing code", "code rocks"]  ->  ["writing code rocks"]
["mission statement", "a quick bite to eat", "a chip off the old block",
 "chocolate bar", "mission impossible", "a man on a mission", "block party",
 "eat my words", "bar of soap"]
    ->  ["a chip off the old block party", "a man on a mission impossible",
         "a man on a mission statement", "a quick bite to eat my words",
         "chocolate bar of soap"]
["a", "b", "a"]                 ->  ["a"]
```

**Constraints:** `1 <= phrases.length <= 100`,
`1 <= phrases[i].length <= 100`.

The arms are `fn before_and_after_puzzles(phrases: Vec[String]) ->
Vec[String]`. The two Rust arms keep the method LeetCode gives Rust users,
over `Vec<String>`, inside `impl Solution`, and a one-line
`before_and_after_puzzles` calls it.

## Approaches

A puzzle is a pair of phrases that meet at a word, so the work is finding
the pairs without trying all of them: group the phrases by first word, and
each phrase's last word names the group it can be followed by. Two
different pairs can make the same puzzle (`["a", "b", "a"]` makes `"a"`
twice), so repeats are dropped.

| file | mechanism |
|---|---|
| `before_and_after_puzzles.kara` ★ | the phrases' indices grouped by first word (`split_once`) in a `Map`; each phrase's last word (`rsplit_once`) looks up the phrases that start with it, every other one is joined on, and the puzzles go into a `SortedSet`, which drops repeats and keeps them in order. O(n + puzzles * log) |
| `before_and_after_puzzles_pairs.kara` | every ordered pair tried: each phrase split into its words once with `split_whitespace`, a pair joined when the first's last word is the second's first, the words joined, then `sort` and `dedup`. O(n^2 * length) |
| `before_and_after_puzzles_cuts.kara` | every ordered pair tried on text: the last word cut at the last space with `rfind`, the other phrase's first word at its first space with `find`; a match joins the first phrase to the rest of the second, into a `Set`, sorted at the end. O(n^2 * length) |
| `before_and_after_puzzles_search.kara` | the phrases' indices sorted by first word; each last word finds the start of its run of matches with `partition_point`, the run is walked, and the puzzles are sorted and their repeats dropped. O(n log n + puzzles * log) |
| `before_and_after_puzzles_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `HashMap<&str, Vec<usize>>` from each first word to the phrases it starts, `split(' ').next()` and `.last()` for the words, the other phrase's tail taken as `&phrases[j][last.len()..]`, the puzzles in a `BTreeSet`), carried to Kāra by `karac fix` |
| `before_and_after_puzzles_chain.kara` | another Rust solution, one iterator chain (every ordered pair `(i, j)` from `flat_map`, kept when `i != j` and the words meet, joined with `format!`, gathered by `collect::<BTreeSet<_>>()`), carried to Kāra by `karac fix`. O(n^2) pairs |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples; a phrase
that starts and ends with the same word, alone (`small 1: 0 []`) and given
twice (`small 2: 1 [go fig go fig go]`), since a phrase is never joined to
itself but its copy is; two equal one-word phrases beside a third
(`small 3: 2 [eel / eel cat]`) and a ring of three (`small 4: 3 [a be cat
/ be cat a / cat a be]`); 300 random problems of 1 to 12 phrases of 1 to 4
words over the first 1 to 5 of eight (`300 random problems: 2707 puzzles,
checksum 932570332`); and 100 phrases of 1 to 25 words over all eight, the
constraints' most phrases, each at most 99 letters (`100 phrases: 1180
puzzles, checksum 235821891`). `before_and_after_puzzles.py` mirrors the ★
arm and its output is byte-identical; with `lit` it joins every ordered
pair of different phrases split into words, as the statement reads, and
its output is the same. Every arm gives the same output under `karac run`
and `karac build`.

The Mend loop: the pairs, cuts and search arms take no fixes. The ★ arm,
as first written, was refused with no fix and no hint (gap 1 below); with
the fix it takes one round of 3: `.as_str()` on the two bare `p` arms, and
`"".to_string()` to `""`, since a literal is already a `String`. The Rust
arms take one round each: `use std::collections::..` dropped; `struct
Solution;` to `struct Solution {}`; `Vec<String>` to `Vec[String]`;
`::` paths to `.`; `format!` to an f-string; `split(' ')` to
`split(" ")`; a `&` pattern dropped. The solution arm also takes
`HashMap<&str, Vec<usize>>` to `Map[Str, Vec[i64]]` and `BTreeSet` to
`SortedSet`; the chain arm `move` and `&&` to `and`, and its
`collect::<BTreeSet<_>>()` to `SortedSet.from_iter(..)`, which was
misplaced before the fix (gap 2 below). Both arms' outputs match on the
first run.

## Gaps

1. **A bare `ref String` arm had no fix.** The ★ arm takes the first word
   with `match p.split_once(" ") { Some((w, _)) => w, None => p }` over a
   `ref String` `p` from `phrases.iter()`. A `ref String` is a `Str` only
   as a call argument (design.md §8), so the arms disagree, and the
   refusal ("match arms have incompatible types: 'Str' and 'ref String'")
   had no fix and no hint: the `.as_str()` edit covered only an arm that
   reads `ref x`. Now a bare place (a name, a field, an index, a call)
   beside a `Str` arm takes `.as_str()`, and `if let` / `else`, which had
   neither the fix nor the hint, gets both. Beside string literals alone,
   which are `String`s by default, the arm keeps its advice to `.clone()`:
   a check sweep over kara-katas found an app where `.as_str()` would have
   been the wrong fix. kara B-2026-11-17-69.
2. **`karac fix` opened `from_iter(` inside a receiver's parentheses.** The
   chain arm's `(0..n).flat_map(..).filter(..).map(..)
   .collect::<BTreeSet<_>>().into_iter().collect()` is fixed to
   `SortedSet.from_iter(it)`, but a parenthesized expression keeps the
   span of what is inside it, so the edit wrote
   `(SortedSet.from_iter(0..n).flat_map(..))`, refused as "no method
   'flat_map' on type 'SortedSet'". Now the edit starts before each `(`
   that closes inside the receiver, while one around the whole receiver
   still holds the call (`(i64.parse(s.trim()))`); the `parse::<T>()` fix,
   which took the same span, is mended too. kara B-2026-11-17-70.

The differential took 7 fixes as first written, an annotated closure's
`-> String` and six `.clone()`s of arguments the callee only borrows, and
one refusal with no fix: the words of a phrase renamed with
`words(p).iter().map(|w| vocabulary[..]).collect()` borrow the temporary
`words(p)`, since the closure takes the item as a reference and returns a
`Str`, and a call's result borrows what such a closure could hand back
(core-semantics.md §5.4); the words are bound first. It takes none now.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every ordered pair of different phrases, each split into its
words, joined when the last word of one is the first of the other, the
puzzles gathered into a `Set` and sorted. 400 random problems of 1 to 10
phrases of 1 to 4 words over the first 1 to 4 of eight; the first five
have one phrase and the first ten use only the first word.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the phrases in another order give the same puzzles |
| P3 | the puzzles come sorted, each once |
| P4 | the words renamed by a random permutation of the eight rename the puzzles |
| P5 | every phrase given twice adds the phrases whose last word is their first, each joined to itself, and nothing else |
| P6 | the ★ arm's answer |

All 14,400 checks pass on every arm: `400 problems: checksum 110167700,
14400 checks over 6 arms: 0 failures`, in 8.7 s under `karac __mir-run`,
and the same under `karac __mir-llvm-run` and `karac build`.

## Mutation testing

Eighteen edits to the differential, three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All eighteen are caught.

| # | mutation | failures by property |
|---|---|---|
| A1 | ★: a phrase joined to itself too | P1 328, P6 1640 |
| A2 | ★: the space after the shared word lost | P1 332, P4 322, P5 314, P6 1660 |
| A3 | ★: the last word read as all after the first | P1 281, P5 260, P6 1405 |
| W1 | pairs: a puzzle made twice kept twice | P1 253, P3 253, P5 379, P6 253 |
| W2 | pairs: the shared word written twice | P1 344, P5 364, P6 344 |
| W3 | pairs: two phrases joined on their first words | P1 232, P5 258, P6 232 |
| C1 | cuts: the last word cut with the space before it | P1 319, P5 314, P6 319 |
| C2 | cuts: a phrase joined to itself too | P1 328, P6 328 |
| C3 | cuts: a one-word phrase's first word read as empty | P1 173, P5 264, P6 173 |
| S1 | search: the search starts past the matching phrases | P1 344, P5 364, P6 344 |
| S2 | search: every other matching phrase skipped | P1 202, P2 182, P5 211, P6 202 |
| S3 | search: the phrases searched unsorted | P1 193, P2 187, P4 150, P5 191, P6 193 |
| X1 | solution: the first word taken for the last | P1 232, P5 258, P6 232 |
| X2 | solution: only a later phrase joined on | P1 206, P2 207, P5 206, P6 206 |
| X3 | solution: only the last phrase kept for each first word | P1 280, P2 213, P5 270, P6 280 |
| R1 | chain: a phrase joined to itself and only to later ones | P1 344, P2 207, P5 206, P6 344 |
| R2 | chain: last words matched with last words | P1 239, P5 249, P6 239 |
| R3 | chain: a one-word phrase appended whole | P1 236, P4 219, P5 264, P6 236 |

A mutation of the ★ arm fails P6 on every arm, since P6 compares each arm
with the ★ arm. 344 of the 400 problems make at least one puzzle, and W2
and S1 fail P1 on exactly those, as every puzzle W2 makes is wrong and S1
makes none. W3 and X1 fail the same checks: both join two phrases on their
first words. A phrase joined to itself (A1, C2) fails only P1 and P6, since
P5 adds those joins on purpose. P2 catches the mutations that depend on
which of two phrases comes first (S2, S3, X2, X3, R1); P3 only W1, which
keeps a repeat; P4 only those that write a word not in the list (A2, R3)
or depend on which word sorts first (S3). Two more edits look like faults
and pass all 14,400 checks under both backends, since they are equivalent:
the pairs arm splitting on `" "` rather than `split_whitespace` (a phrase
has single spaces and none at its ends), and the chain arm walking the
second phrase backwards (a `SortedSet` keeps its own order).

## Benchmarks

`bench/` times the ★ arm against the same algorithm in C, Rust, Go and
Python: 100 problems of 100 phrases, the constraints' most, each phrase 1
to 25 words over the first 2 to 8 of the list, built once, then 5 rounds
over all of them, each puzzle's length and the count folded into a
checksum. Every program prints `5 rounds of 100 problems: checksum
633275861`. Rust keeps the puzzles in a `BTreeSet` as Kāra does; C (no
ordered set) collects them in an array and sorts it with `qsort`, dropping
repeats; Go and Python gather them in a hash set and sort it.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac `cf35bf7d49`
on LLVM 22. A plain `karac build` now targets x86-64-v2 (kara
40435b5a79); C and overflow-checked Rust are shown at their own defaults
and at x86-64-v3, which differ here by under 3%:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.581 to 0.690 s | 0.602 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.592 to 0.682 s | 0.607 s |
| Rust (`rustc -O`) | 0.457 to 0.533 s | 0.474 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.448 to 0.511 s | 0.458 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.446 to 0.485 s | 0.466 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.272 to 0.286 s | 0.281 s |
| C (`clang -O3`) | 0.264 to 0.308 s | 0.281 s |
| Go | 0.458 to 0.541 s | 0.502 s |
| Python | 0.757 to 0.760 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; user time is within 1% of wall time for both Kāra
rows, so both ran on one core. Kāra takes about 1.3x the time of
overflow-checked Rust, the equal-safety comparison, 2.2x C's and 1.21x
Go's; Python takes about 1.25x Kāra's. The work is building strings and
ordering them: about 2,300 distinct puzzles a problem, 78 letters long on
average and at most 184, inserted into an ordered set and compared byte by
byte. Overflow checks cost nothing measurable here (Rust's checked build
is as fast as its plain one), and Python's string operations, written in
C, keep it close. C sorts an array once rather than keeping a tree, which
may be most of its lead; where Kāra's time over Rust's goes was not
profiled.
