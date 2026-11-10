# 1092. Shortest Common Supersequence

Given two strings `str1` and `str2`, return the shortest string that has
both `str1` and `str2` as **subsequences**. If there are multiple valid
strings, return **any** of them.

A string `s` is a **subsequence** of string `t` if deleting some number
of characters from `t` (possibly `0`) results in the string `s`.

```
str1 = "abac", str2 = "cab"            ->  "cabac"
str1 = "aaaaaaaa", str2 = "aaaaaaaa"   ->  "aaaaaaaa"
```

**Constraints:** `1 <= str1.length, str2.length <= 1000`; `str1` and
`str2` consist of lowercase English letters.

The arms are `fn shortest_common_supersequence(a: String, b: String) ->
String`. Any shortest answer is right, and the arms break ties apart, so
the harness prints each answer's length and whether both words can be
read out of it.

## Approaches

| file | mechanism |
|---|---|
| `shortest_common_supersequence.kara` ★ | by the longest common subsequence: `lcs[i][j]` the LCS of the first i letters of `a` and the first j of `b`, a table of `Vec.filled` rows; walking back from the full table, a letter both words end with is written once, and otherwise the word whose last letter the LCS does not need gives it up; what either word has left goes in front, and the `Vec[char]` written backwards is reversed into a `String` (`iter().rev().collect()`). |a| + |b| - LCS letters, O(\|a\| \|b\|) |
| `shortest_common_supersequence_table.kara` | the supersequence's own table, forward: `scs[i][j]` the length of the shortest supersequence of what is left of the words from letters i and j on, filled from the ends (`(0..=n).rev()`), a used-up word leaving the other's rest; the answer read forward from the first letters into a `String` with `push`. O(\|a\| \|b\|) |
| `shortest_common_supersequence_memo.kara` | top down: the shortest length for the first i and j letters by recursion, memoized in a `Map[(i64, i64), i64]` passed as `mut ref`, so only the pairs the recursion reaches are computed; the answer read back from the end by asking the same function which step keeps the length, then `reverse()`. O(\|a\| \|b\|) at most, the recursion as deep as \|a\| + \|b\| |
| `shortest_common_supersequence_halves.kara` | Hirschberg's linear-space LCS, then a merge: `a` cut in half, the LCS lengths of its first half against every prefix of `b` and of its second half, reversed, against every suffix (one row each), `b` cut where their sum is largest, and the halves recursed on (slices `x[..half].to_vec()`); the words are then merged along the LCS, and what each has left is added with `out.extend(x[i..].iter())`. O(\|a\| \|b\|) time, O(\|a\| + \|b\|) space |
| `shortest_common_supersequence_steps.kara` | a table of steps: an `enum Step { Both, FromA, FromB }` per pair of suffixes, what the shortest supersequence of the rest writes first, filled from the ends with the lengths kept in two rows only; the answer read by following the steps with a `match`. O(\|a\| \|b\|) steps, O(\|b\|) lengths |
| `shortest_common_supersequence_solution.kara` | LeetCode's Rust template (`impl Solution` with no `struct Solution;`, `str1.as_bytes()`, `vec![vec![0; m + 1]; n + 1]`, `let (mut i, mut j)`, the bytes pushed into a `Vec`, reversed and read back with `String::from_utf8(res).unwrap()`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 15 lines: LeetCode's two examples and ten
more (one letter each, the same word twice, no letter shared, one word
inside the other either way round, a letter against its own run, and
four longer pairs), a sum and checksum of the lengths over 2000 random
pairs of 1 to 12 letters from a to c with a count of answers missing a
word (`lengths sum to 19485, 0 missing a word, checksum 461624550`), and
two pairs of 1000 letters, LeetCode's longest, from 26 letters (`1675`)
and from 4 (`1356`). `shortest_common_supersequence.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a writer puts down one letter at a time, and each word is
read out of what it wrote by taking its next letter whenever the writer
puts that letter down; the fewest letters after which both words have
been read whole, found level by level from no letters read over every
letter either word has. That is the answer's length, by a search that
never forms a common subsequence. It checks 2000 problems in four kinds
of 500: two words of 1 to 8 letters from a to c; of 1 to 16 from a and
b; a word of 1 to 12 letters from a to d and a word made from it (each
letter kept or not, and a letter put in after it or not), so the two
share a long common subsequence; and two words of up to five runs of
one letter. Each has a letter from a to d to put after both words.
Every random choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer's length is the statement read literally |
| P2 | both words can be read out of the answer |
| P3 | the words the other way round give an answer as long |
| P4 | renaming the letters (a to b, b to c, c to d, d to a) before the arm or after gives the same answer |
| P5 | one letter put after both words makes the answer one letter longer |
| P6 | the arm given its own answer and either word gives the answer back |

All 72,000 checks pass on every arm: `2000 problems: checksum 74665246,
72000 checks over 6 arms: 0 failures`. A Python reading of the same
problems, by the longest common subsequence, gives the same checksum.

P4 and P6 ask for an exact answer even though any shortest one is
right. P4 holds because the arms only ever compare two letters for
equality, so renaming them changes no choice; P6 holds because a word
that can be read out of `s` adds nothing to it, and the only string of
\|s\| letters with `s` in it is `s`.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. Three survive, as they must: the ★, table and Hirschberg
arms breaking their ties the other way, which gives another shortest
answer. The other 27 are all caught. Fifteen are kept, no two failing
the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: what `b` has left dropped | P1 1047, P2 1047, P3 1447, P6 1456 |
| M2 | ★: a shared letter left in `b` too | P1 1836, P5 2000, P6 2000 |
| M3 | ★: the smaller LCS kept | P1 552, P3 867, P6 1070 |
| M4 | table: the longer rest kept | P1 547, P3 894, P5 750, P6 1087 |
| M5 | table: the rest of the longer word dropped | P1 1570, P2 1570, P3 759, P5 1193, P6 677 |
| M6 | memo: what `a` has left counted twice | P1 135, P3 215 |
| M7 | memo: the longer step taken | P1 1408, P3 725, P6 1795 |
| M8 | memo: the answer not reversed | P2 1808, P6 1892 |
| M9 | Hirschberg: a row taking the left of the row above | P1 217, P3 333, P5 203, P6 418 |
| M10 | Hirschberg: what `b` has left dropped | P1 1199, P2 1199, P3 1486, P5 911, P6 1644 |
| M11 | Hirschberg: a shared letter never written | P1 1836, P2 1836, P5 2000, P6 2000 |
| M12 | steps: the last row counted from the wrong end | P1 970, P3 1276, P5 1351, P6 1777 |
| M13 | steps: the row below never moved up | P1 508, P3 716, P5 270, P6 920 |
| M14 | solution: the answer not reversed | P2 1821, P6 1906 |
| M15 | solution: the last column never filled | P1 241, P3 514, P5 241, P6 1188 |

P6 catches fourteen of the fifteen, P1 thirteen, P3 eleven, P5 nine, P2
six and P4 none. P1 counts letters, so it misses the two answers left
backwards (M8, M14), which are as long as the right ones; P2 sees those
and the answers that lose letters, and no answer that is merely too
long. P4 sees nothing here because no edit names a letter: a renaming
can only catch an arm that treats some letter apart. M6 is the hardest
to see: counting what `a` has left twice only matters where the memo
arm weighs a step that uses `a` up against one that does not, and is
wrong in 135 of the 2000 problems.

Five edits first written turned out to change nothing, and were
replaced: the ★ arm counting a shared letter as 2 in the LCS (every
entry of the table doubles, so every choice stands), the memo arm's
used-up word counted as `i.max(j)` or as `i + j + 1` (the first is the
same number when one of them is 0; the second adds one to every
length), the steps arm counting a shared letter as nothing (the length
of the rest then compares as the LCS does), and the steps arm counting
a used-up `b` one short (no difference in the differential, nor in
every pair of words of up to five letters from two).

Of the twelve caught but not kept, five fail exactly as a kept edit:
the steps arm leaving a shared letter in `b` and the Hirschberg arm
never letting a lone letter into the LCS as M2, the memo arm keeping
the longer rest as M3, the memo arm dropping `b`'s first letters once
`a` is used up as M1, and the solution arm following the smaller LCS as
M7. Seven fail in ways of their own but were not needed: the ★ arm
stopping its walk a letter of `a` early, the table arm leaving all of
`b` to a used-up `a` and counting a shared letter twice, the steps arm
counting a letter of `b` twice and taking `a`'s letter one too readily,
and the solution arm not counting a shared letter and dropping `a`'s
first letters once `b` is used up.

## Verification

Every arm prints the same output as `shortest_common_supersequence.py`
under `karac __mir-run` (the v2 MIR interpreter), `karac
__mir-llvm-run`, and `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer) with no error. `karac run` and a `karac build` binary
print the same output for every arm and the differential. `karac check
--output=json` reports nothing on any file, and `karac fix` has nothing
to apply. Under `karac __mir-run` the differential takes 15 s.

The kata found two gaps, both fixed in the compiler:

- The Hirschberg arm adds what each word has left with
  `out.extend(x[i..].iter())`, `out` a `String` and `x` a `Vec[char]`.
  `karac check` refused it as ambiguous and named the two `Extend`
  impls to choose between with UFCS: a `String` extends by `char`s and
  by `String`s, and an iterator lending `ref char` matched neither
  exactly. A `Vec`'s `extend` reads a lent `Copy` item out; a
  `String`'s now does the same for a lent `char`, and lent `String`s
  still need `.cloned()` (kara B-2026-11-10-20, pinned by
  `tests/kata_1092_string_extend_lent_chars.rs`).
- LeetCode's Rust template here is `impl Solution { ... }` with no
  `struct Solution;`, which the site supplies. `karac check` said only
  "undefined type 'Solution'" and `karac fix` had nothing to apply. An
  inherent impl of a type nothing declares, whose functions take no
  `self`, uses the type only as a namespace, so the fix now declares
  it, `struct Solution {}`, above the impl (kara B-2026-11-10-21,
  pinned by `tests/kata_1092_impl_solution_template.rs`).

With that, the Rust arm reaches a clean check in four rounds of `karac
fix`, and gives the text the arm holds. The first round is the syntax:
`Vec::new` and `String::from_utf8` to `.`, `let (mut i, mut j)` to `let
mut (i, j)`, and `||` to `or`. The second declares `struct Solution
{}`. The third turns `as_bytes()` into `bytes()`, a `Slice[u8]`, and
the inner `vec![0; m + 1]` into `Vec.filled(m + 1, 0)`, and the fourth
the outer `vec![..; n + 1]`.

## Benchmarks

The bench builds 50 random pairs of words of 1000 letters each,
LeetCode's longest, from 2 to 26 letters, once. Each of 4 rounds
answers every pair with the ★ arm, folding each answer's length and two
of its letters into a checksum. Every implementation prints `4 rounds
over 50 pairs of 1000 letters: lengths sum to 309936, checksum
49420282`. Each mirror fills the same table of 1001 rows of 1001
`i64`s per call and walks it back: Rust `Vec<Vec<i64>>` of `char`s, Go
`[][]int64` of runes, Python lists, and C a `calloc`'d row per row of
the bytes.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `e609854dde`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.538 to 0.619 s | 0.573 s |
| Kāra (`karac build`) | 0.543 to 0.648 s | 0.573 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.801 to 0.897 s | 0.850 s |
| C (`clang -O3`) | 0.826 to 1.003 s | 0.875 s |
| Rust (`rustc -O`) | 0.990 to 1.099 s | 1.051 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.002 to 1.120 s | 1.052 s |
| Go | 1.023 to 1.093 s | 1.067 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 1.129 to 1.277 s | 1.195 s |
| Python | 27.1 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte.

The work is 200 tables of a million `i64`s, each filled with a
comparison and a `max` per cell and walked back once. The order of the
rows above is not the order of the arithmetic: it is the allocator's.
Each call's table is 8 MB of rows that are freed when the call returns,
and glibc's `free` gives that memory back to the kernel, so the next
call's `calloc` or `vec!` faults it in again: C takes 386,000 page
faults and 0.46 s in the kernel, Rust 388,000 and 0.51 s, Go 34,000 and
0.32 s. Kāra's runtime allocator keeps the freed rows for the next call
and takes 2,000 faults and 0.004 s. In user time alone C is ahead (0.41
s against Kāra's 0.51 s, with no bounds or overflow checks), and Rust
with overflow checks takes 0.65 s. Python takes 47x Kāra's time.
