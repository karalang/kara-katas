# 1592. Rearrange Spaces Between Words

You are given a string `text` of words that are placed among some number
of spaces. Each word consists of one or more lowercase English letters
and is separated by at least one space. It's guaranteed that `text`
contains at least one word.

Rearrange the spaces so that there is an equal number of spaces between
every pair of adjacent words and that number is maximized. If you cannot
redistribute all the spaces equally, place the extra spaces at the end,
meaning the returned string should be the same length as `text`.

Return the string after rearranging the spaces.

```
text = "  this   is  a sentence "     ->  "this   is   a   sentence"
text = " practice   makes   perfect"  ->  "practice   makes   perfect "
```

**Constraints:** `1 <= text.length <= 100`; `text` consists of lowercase
English letters and `' '`; `text` contains at least one word.

## Approaches

| file | mechanism |
|---|---|
| `spaces.kara` ★ | the words by `split_whitespace` into a `Vec[Str]`, the spaces counted by a `filter`, the answer one f-string of `join` and `" ".repeat(..)`. O(n) |
| `spaces_bytes.kara` | one pass over the bytes, the words as `(start, end)` places, the answer written into a `Vec[u8]` by `extend_from_slice` and padded to the text's length. O(n) |
| `spaces_split.kara` | `split(" ")` with the empty pieces dropped, the spaces as the text's length less the letters, the answer built by `push_str`. O(n) |
| `spaces_solution.kara` | LeetCode's Rust template (`chars().filter(\|&c\| ..)`, `Vec<&str>`, `format!`, `join(&" ".repeat(gap))`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples and six more
(one word with and without spaces, gaps that divide and that do not, a
leading space, trailing spaces), then the count ending in a space and a
checksum of every answer's bytes for 3000 random texts of up to 10
characters, 300 of up to 100, and 10 of up to 100000, each a third
spaces and otherwise the letters a to c. `spaces.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every gap width from 0 up to the number of spaces, kept when
the gaps between words fit in the spaces, the widest taken and the rest
put at the end. It checks 3000 texts of 1 to 9 characters, spaces and
the letters a to c, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is as long as the text and has the text's words in order |
| P3 | every letter moved one along (a to b, b to c, c to d) moves the answer's letters the same way |
| P4 | the answer rearranged again is itself |
| P5 | the text's leading spaces moved to its end leave the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 917982047, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

One first choice was replaced: letting the template's one-word case fall
through divided by zero gaps, killed only by the panic.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the spaces left over never put at the end | P1 171, P2 171, P6 171 |
| M2 | ★: one word returned without its spaces | P1 731, P2 731, P6 731 |
| M3 | ★: the spaces divided by at least two gaps | P1 1036, P2 1036, P4 703, P6 1036 |
| M4 | bytes: the spaces never counted | P1 1445, P2 1445, P6 1445 |
| M5 | bytes: padded to one short of the text | P1 902, P2 902, P4 319, P6 902 |
| M6 | bytes: no gap before the second word | P1 1445, P2 1445, P4 409, P6 1445 |
| M7 | split: one space too few | P1 1274, P2 491, P6 1274 |
| M8 | split: never padded at the end | P1 902, P2 902, P6 902 |
| M9 | template: the rest taken over the words, not the gaps | P1 965, P2 965, P4 965, P6 965 |
| M10 | template: the gap taken over the words, not the gaps | P1 1303, P2 1303, P4 783, P6 1303 |

## Benchmarks

The bench runs the ★ arm on 200 texts of 100000 characters, all drawn
first, in all five languages. Every implementation prints `200 texts of
100000 characters: 2223996 trailing spaces, checksum 392629179`. The C
mirror finds the words as (start, end) places, the spaces counted, the
answer written into a new buffer per call.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5dc4418bbd` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O -C overflow-checks=on`) | 0.349 s |
| Rust (`rustc -O`) | 0.362 s |
| C (`clang -O3`) | 0.399 s |
| Kāra (`karac build`) | 0.420 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.421 s |
| Go | 0.554 s |
| Python | 7.1 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is below its real time (0.389 s and 0.418 s on one run).

## Verification

All four arms print the same output as `spaces.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5dc4418bbd`.

## Writing it

The ★ and split arms were written in Kāra and checked as written. The
bytes arm wrote `b[*start..*end]` over a borrowed `(i64, i64)` pattern,
and `karac fix` dropped both `*`s. The harness wrote `mix(check, *c as
i64)`, and `karac fix` dropped the cast. The differential wrote Rust's
`c as u8` on a `char`, which Kāra refuses as a narrowing; `karac fix`
wrote `c as u32 as u8`, and dropped six `.clone()`s on arguments that
only borrow.

The Rust template took one round of `karac fix`: `struct Solution;` to
`struct Solution {}`, the `|&c|` pattern to `|c|`, `Vec<&str>` to
`Vec[Str]`, `format!("{}{}", ..)` to an f-string, the two `&" ".repeat(..)`
borrows to plain arguments, and `Solution::` to `Solution.`. It then
checks and agrees with no hand edit.
