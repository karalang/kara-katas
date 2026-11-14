# 1156. Swap For Longest Repeated Character Substring

You are given a string `text`. You can swap two of the characters in the
`text`.

Return the length of the longest substring with repeated characters.

```
text = "ababa"     ->  3
text = "aaabaaa"   ->  6
text = "aaaaa"     ->  5
```

**Constraints:** `1 <= text.length <= 2 * 10^4`; `text` consists of
lowercase English characters only.

The arms are `fn max_rep_opt1(text: Str) -> i64`.

## Approaches

One swap can do two things for a run of one letter: bring in one more of
the letter from elsewhere to extend it, or replace a single other letter
between two runs of the letter and join them. Either way the letter must
come from somewhere, so no run can be longer than the text's count of
that letter.

| file | mechanism |
|---|---|
| `max_rep_opt1.kara` ★ | the text as runs of `(letter, length)`: each run grown by one, and each pair of runs of one letter split by a single other letter joined through it, both capped by the letter's count. O(n) |
| `max_rep_opt1_window.kara` | for each letter, a sliding window over `text.chars()` holding at most one other letter, which one swap could replace; the window's length capped by the letter's count. O(26 n) |
| `max_rep_opt1_sides.kara` | the run lengths ending at and starting at each place: replacing the letter at a place joins the runs on its two sides when they match, and the run through a place grows by one, each capped by the count. O(n) |
| `max_rep_opt1_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `text.as_bytes()`, a `[i32; 26]` count indexed by `usize`, the runs walked by `while` with a second look past one letter, and `std::cmp::{max, min}`), carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 18 lines: LeetCode's examples (`ababa` 3,
`aaabaaa` 6, `aaabbaaa` 4, `aaaaa` 5, `abcdef` 1); `a` and `ab` (1
each); three short texts where the count caps the answer (`aba` 2,
`aab` 2, `baaab` 3); a join the count caps (`aaabaaab` 6: joining makes
7, but there are six `a`s); `abaaac` 4; and `bbababaaaa` 6. Then 2000 random texts of 1 to 40 letters over the
first 1 to 4 letters, with a total and a checksum (`2000 random texts:
total 17833, checksum 778468252`), and four texts of 20,000 letters, the
most the constraints allow: random over 2 letters (19) and over 26 (5),
all one letter (20000), and one letter split once by another with a
third at the end (19998: the join would make 19999, but there are only
19998 `a`s). `max_rep_opt1.py` mirrors the ★ arm and its output is
byte-identical; a Python search over every swap agrees on 3000 more
random texts of up to 14 letters.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the longest run after each swap of two places, or after none.
It checks 4000 texts in four kinds of 1000: 1 to 10 letters over the
first 1 to 4; 10 to 60 letters over the first 2 to 5; runs of `a` of 1
to 8 letters split by single other letters, with 0 to 2 `c`s and 0 to 2
more `a`s at the end; and two runs of `a` of 1 to 10 letters split by
one `b`, with the same tail, so that the `a`s elsewhere cap the join or
do not. The literal search runs on all but the second kind. Every random
choice the properties make is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one (the first, third and fourth kinds) |
| P2 | the text reversed gives the same answer |
| P3 | the letters renamed by a random permutation of all 26 give the same answer |
| P4 | the answer is no shorter than the longest run and no longer than the most of any one letter |
| P5 | a letter the text does not hold, added at the end, changes nothing |
| P6 | for the text with two random places swapped, each text's longest run is within the other's answer |

All 92,000 checks pass on every arm: `4000 texts: checksum 796293969,
92000 checks over 4 arms: 0 failures`. A Python reading of the same
texts, with the same swap search, gives the same line.

## Mutation testing

Twenty-two edits to the differential, five or six to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run` with
`KARAC_HASH_SEED=1`, each failing the same way under both. Eighteen are
caught; four are equivalent. In the sides arm, the backward run lengths
never computed at the first place, a run never grown from the place
before it, and the best starting from 0 rather than 1 all change
nothing: the run through each place already grows by one, at every
place of the run, and every text has a run of 1. In the solution arm, a
run never grown by itself changes nothing either, since the join it
tries next grows the run by one when nothing follows the letter after
it. Seventeen are kept, no two failing the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a run grown by one without a letter to spare | P1 706, P4 712 |
| M2 | ★: runs joined across two letters | P1 67 |
| M3 | ★: a join never grows by the swapped-in letter | P1 1177, P6 94 |
| M4 | ★: runs of different letters joined | P1 1820, P2 114, P5 147, P6 264 |
| M5 | ★: a run never grown | P1 159, P6 42 |
| M6 | ★: the last join never tried | P1 537, P2 1118, P5 563, P6 56 |
| M7 | window: two other letters allowed | P1 861 |
| M8 | window: no cap by the letter's count | P1 1185, P4 1196, P5 454 |
| M9 | window: `z` never tried | P3 153 |
| M10 | window: the wrong letter leaves the count | index out of bounds |
| M11 | window: one short | P1 1815, P4 454, P5 454, P6 617 |
| M12 | sides: runs never grow left to right | P1 1553, P2 1580, P6 168 |
| M13 | sides: joined only when the middle matches the left | P1 1803, P2 368, P6 259 |
| M14 | sides: a join not capped | P1 944, P4 951 |
| M15 | solution: the join looks two places on | P1 117 |
| M16 | solution: `max` for `min` on the join | P1 2490, P4 1650 |
| M17 | solution: a run skipped after each | P1 124, P2 1059, P6 48 |

Of the seventeen caught edits that do not stop the program, P1 catches
sixteen, P6 nine, P2 and P4 five, P5 four and P3 one. The edits that
join across too much (M2, M7, M15) are seen only by P1: a join through
two letters or two places on is consistent with itself under reversal,
renaming and every bound. A first run of the mutations found them on
the short random kind alone, and M9 on nothing, since the texts never
held a `z` and P3's renaming kept it fixed; the literal search was
then run on the two structured kinds as well, and the renaming was
widened to all 26 letters, which is what catches M9. The solution arm's
join one short fails exactly as M3, and is not kept.

## Benchmarks

`bench/` times the ★ arm against the same runs in C, Rust, Go and
Python. 64 texts of 20000 letters, the most the constraints allow, are
built once in four kinds: random over 2 letters, over 3, over 26, and
runs of `a` of 1 to 40 letters split by single other letters. Each of
100 passes answers all 64 in turn. Every program prints `100 passes over
64 texts of 20000 letters: checksum 19254313`. Each builds a fresh list
of runs per call, as the ★ arm does.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `cd48de9052`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.664 to 0.783 s | 0.682 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.664 to 0.730 s | 0.693 s |
| Rust (`rustc -O`) | 0.697 to 0.837 s | 0.730 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.747 to 0.851 s | 0.773 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.757 to 0.832 s | 0.778 s |
| Kāra (`karac build`) | 0.821 to 0.897 s | 0.845 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.820 to 1.027 s | 0.855 s |
| Go | 3.349 to 3.890 s | 3.424 s |
| Python | 30.0 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; a plain `karac build` gives the same binary, byte
for byte, so the two Kāra rows are one program timed twice. Kāra takes
about 1.1x overflow-checked Rust's time, the equal-safety comparison;
Rust without the checks takes about 0.85x Kāra's time, C about 0.8x,
and Python about 35x. Go takes about 4x: its time goes to memory, not
the loop. One run spent 2.8 s of user and 3.0 s of system time; with
`GOGC=off` the user time fell to 1.1 s and the system time stayed at
2.7 s, the page faults of the fresh memory `append` takes as the list of
runs grows on every call, where the C, Rust and Kāra allocators reuse
the block the last call freed.
