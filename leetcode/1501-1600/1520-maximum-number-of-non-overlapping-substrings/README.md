# 1520. Maximum Number of Non-Overlapping Substrings

Given a string `s` of lowercase letters, find the maximum number of
non-empty substrings of `s` that meet the following conditions:

1. The substrings do not overlap: for any two substrings `s[i..j]` and
   `s[x..y]`, either `j < x` or `i > y` is true.
2. A substring that contains a certain character `c` must also contain all
   occurrences of `c`.

Find the maximum number of substrings that meet the above conditions. If
there are multiple solutions with the same number of substrings, return
the one with minimum total length. It can be shown that there exists a
unique solution of minimum total length. Return the substrings in any
order.

```
s = "adefaddaccc"  ->  ["e","f","ccc"]
s = "abbaccd"      ->  ["d","bb","cc"]
```

**Constraints:** `1 <= s.length <= 10^5`; `s` contains only lowercase
English letters.

## Approaches

| file | mechanism |
|---|---|
| `substrings.kara` ★ | each letter's span, from its first occurrence, is grown until it holds every occurrence of every letter inside it, and dropped if it would have to grow left. Walking first occurrences left to right, a span that starts after the last one taken is added, and one that starts inside it (it can only be nested in it) replaces it. O(26 n) |
| `substrings_end.kara` | the valid spans are collected first, then taken by earliest end, as in interval scheduling: sorted by end, a nested pair that ends together ordered inner first, a span taken when it starts after the last one taken ends. O(26 n) |
| `substrings_closure.kara` | each letter's span is closed over the 26 letters, not grown along the string: a span takes in the span of every letter inside it, repeated until no span changes. A span is valid when its closure still starts at its letter's first occurrence; the ★ arm's walk takes them. O(26 n) |
| `substrings_iter.kara` | the ★ arm with iterator adapters: `position` and `rposition` for each letter's ends, `filter_map` for the valid spans, `fold` for the walk that adds or replaces |
| `substrings_solution.kara` | LeetCode's Rust template (`as_bytes()`, `usize` indices, `[usize; 26]`, `*ans.last_mut().unwrap() = piece`), carried by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples, one letter
three times, a string that is its own only answer, then a checksum of the
printed answers for 3000 random strings of 1 to 12 letters over 4 and 30 of
1 to 30000 over 26. The answer is unique as a set, so it is printed sorted.
`substrings.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every substring that holds all of each of its letters is
listed, and a dynamic program over positions picks the most of them that do
not overlap, then the least total length. It checks 3000 strings of 1 to 10
letters over 3, every random choice drawn before any arm answers, and
compares answers as sorted lists.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the letters renamed (a to b, b to c, c to a) rename the answer |
| P3 | the string reversed reverses each substring of the answer |
| P4 | every substring of the answer holds all of each of its letters, and no two share a letter |
| P5 | the string followed by a copy over d, e, f answers with the string's answer and the copy's |
| P6 | each arm agrees with at least two of the other four |

The differential prints `3000 problems: checksum 370438147, 90000 checks
over 5 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Sixteen edits to the differential, two to four to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Eleven are killed, each the
same way under both backends; five survive, and all five are equivalent.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a span dropped only if it would grow left by two | P1 550, P3 714, P4 550, P6 550 |
| M3 | ★: the right edge kept at the largest end, not the replacing span's | P1 156, P3 156, P6 156 |
| M4 | end: sorted by start ascending within an end, outer first | P1 1999, P3 1060, P5 3000, P6 1999 |
| M6 | end: a span not grown by the letters inside it | P1 683, P3 778, P4 683, P6 683 |
| M8 | closure: validity not asked of the closed span | P1 865, P3 993, P4 865, P6 865 |
| M9 | closure: a span grown only to the right | P1 670, P3 756, P4 670, P6 670 |
| M12 | iter: each letter's last occurrence found by `position` | P1, P4, P6 2425 each |
| M15 | iter: a nested span pushed, not replacing | P1, P4, P6 1136 each |
| M16 | iter: a span dropped only if it would grow left by two | P1 550, P3 714, P4 550, P6 550 |
| M13 | template: each letter's first occurrence overwritten by later ones | P1, P4, P6 2425 each |
| M14 | template: a nested span pushed, not replacing | P1, P4, P6 1136 each |

The survivors: `>=` for `>` in the ★ arm's and the iterator arm's add test
(M2, M10) and in the end arm's take test (M5), since a letter's first
occurrence is never the end of a span already taken; the closure arm not
merging the inner letter sets (M7), since the letter it absorbs already
carries its own closure; and the iterator arm starting the growth at the
span's start rather than its letter's last occurrence (M11), since the
first step reaches it.

## Benchmarks

The bench builds 200000 random strings of 1 to 64 letters over 5 once and
answers each 3 times by the ★ arm, in all five languages. Each answer
copies the string's bytes and returns its substrings as fresh strings, as
the signature asks (`malloc` and `free` in C). Every implementation prints
`3 passes over 200000 strings of up to 64 letters: 739788 substrings,
checksum 431088825`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `218952d3b` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.150 s |
| Rust (`rustc -O`) | 0.161 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.169 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.194 s |
| Kāra (`karac build`) | 0.194 s |
| Go | 0.228 s |
| Python | 5.03 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.186 s and 0.191 s on one run).

Kāra is 1.15x Rust under overflow checks by median. Not traced. Each
answer makes five small allocations before its substrings (the byte copy,
the two 26-entry lists, the span list and the result), so allocation may
be much of the time, and allocators differ.

## Verification

All five arms print the same output as `substrings.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change.

## Writing it

The ★, end and closure arms were written in Kāra and `karac fix` had
nothing to change. The iterator arm took 6 edits over two rounds: three
`*` dereferences of a `filter` closure's `i64` and a pattern's `i64`
dropped, then `ref Vec[..]` parameters made bare, since a bare parameter
already borrows. The differential's literal reading took the same last
edit once.

The Rust template took 11, 7 and 1 edits over three rounds: `as_bytes()`
to `bytes()`, `Vec<..>` to `Vec[..]`, the `usize` indices and the
`0usize` literal to `i64` (with the casts that feed them, since
B-2026-11-08-49), `!` to `not`, and `i as i64` dropped. It then stopped at
`*ans.last_mut().unwrap() = piece`: the library has no `last_mut`, and
the error named the index form but offered no fix. `karac fix` now writes
`ans[ans.len() - 1] = piece` for that shape (kara `218952d3b`,
`tests/fix_last_mut_write.rs`), and the template checks and agrees.
