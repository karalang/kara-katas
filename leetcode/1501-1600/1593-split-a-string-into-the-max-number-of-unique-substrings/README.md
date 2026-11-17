# 1593. Split a String Into the Max Number of Unique Substrings

Given a string `s`, return the maximum number of unique substrings that
the given string can be split into.

You can split string `s` into any list of non-empty substrings, where
the concatenation of the substrings forms the original string. However,
you must split the substrings such that all of them are unique.

A substring is a contiguous sequence of characters within a string.

```
s = "ababccc"  ->  5
s = "aba"      ->  2
s = "aa"       ->  1
```

**Constraints:** `1 <= s.length <= 16`; `s` contains only lower case
English letters.

## Approaches

| file | mechanism |
|---|---|
| `unique_split.kara` ★ | backtracking: from each place every next piece not yet used is put in a `Set[String]` and the rest split the same way; a branch stops when even one piece per letter left cannot beat the best. O(2^n n) |
| `unique_split_masks.kara` | each of the `n - 1` places between letters cut or not: every mask tried, its pieces as `Str` slices sorted and checked for a repeat with `windows(2)`. O(2^n n log n) |
| `unique_split_plain.kara` | backtracking with no set and no bound: the pieces on a `Vec[String]`, a new piece checked against them by `contains`, the best returned up the recursion. O(2^n n^2) |
| `unique_split_solution.kara` | LeetCode's Rust template (a nested `fn dfs` over `&str`, `&mut HashSet<String>` and `&mut i32`, with the same bound), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples and five
more (one letter, sixteen different letters, sixteen `a`s, `abab`, and a
mixed fifteen), then the total and a checksum for 3000 random strings of
up to 8 letters from two, 300 of up to 12 from three, and 30 of 16 from
two. `unique_split.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every split of the string listed in full, each split's pieces
compared pair by pair, the most pieces among the splits with no two the
same. It checks 3000 strings of 1 to 6 letters from a to c, every random
choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the string reversed leaves the answer |
| P3 | the letters renamed (a, b, c made c, a, b) leave the answer |
| P4 | a letter not in the string added at the end adds one |
| P5 | the string written twice gives at least the answer |
| P6 | each arm agrees with at least two of the other three |

P5 holds because the same split with the second copy as one more piece
has no repeat, unless the split was the whole string alone. The
differential prints `3000 problems: checksum 513503244, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

One first choice was replaced: writing the ★ arm's bound as
`< best + 1` is the same test on integers.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the best replaced by the last count reached, not raised to it | P1 2327, P4 3000, P6 2327 |
| M2 | ★: a piece never taken out of the set on the way back | P1 2508, P2 291, P4 3000, P6 2508 |
| M3 | ★: the bound counts one piece per two letters left | P1 601, P2 219, P4 519, P6 601 |
| M4 | masks: the last piece never added | P1 1456, P2 586, P4 1544, P6 1456 |
| M5 | masks: a cut where the mask has none, never at the first place | P1 765, P2 416, P4 492, P6 765 |
| M6 | plain: a piece never popped on the way back | P1 2508, P2 291, P4 3000, P6 2508 |
| M7 | plain: no piece longer than three letters | P5 41 |
| M8 | template: a piece never taken out of the set on the way back | P1 2508, P2 291, P4 3000, P6 2508 |
| M9 | template: the bound one too tight | P1 582, P2 192, P4 515, P6 582 |
| M10 | masks: equal pieces of more than one letter let through | P1 34, P6 34 |

M7 is killed only by P5: in the strings the differential draws, of at
most six letters, a best split never needs a piece of four letters, but
the string written twice sometimes does.

## Benchmarks

The bench runs the ★ arm on 20000 strings of 16 letters from a to c, all
drawn first, in all five languages. Every implementation prints `20000
strings of 16 letters: total 178142, checksum 836300635`. C has no set;
the C mirror keeps the pieces used in an open-addressing table of owned
copies, hashed by FNV-1a, with linear probing and backward-shift
removal, and copies each piece into a malloc as Kāra's `to_string` does.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5dc4418bbd` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 3.599 s |
| Go | 6.947 s |
| Rust (`rustc -O -C overflow-checks=on`) | 8.920 s |
| Rust (`rustc -O`) | 9.096 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 10.880 s |
| Kāra (`karac build`) | 10.959 s |
| Python | 23.8 s |

C leads by far. Its mirror keeps the pieces in its own open-addressing
table hashed by FNV-1a, where Kāra's `Set` and Rust's `HashSet` hash
with SipHash, and the work is mostly the set's lookups, inserts and
removals of the pieces as they are tried; the gap was not profiled
further.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is below its real time (11.063 s and 11.162 s on one run).

## Verification

All four arms print the same output as `unique_split.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5dc4418bbd`.

## Writing it

The ★, masks and plain arms were written in Kāra and checked as
written. The ★ arm first returned the `i64` count; it was changed by
hand to LeetCode's `i32`, so that every arm shares the harness.

The Rust template took one round of `karac fix`, of 24 edits: the
nested `fn dfs` hoisted to the top level, `use std::collections::HashSet`
dropped, `struct Solution;` to `struct Solution {}`, `&str` to `Str`,
`usize` to `i64`, `&mut HashSet<String>` and `&mut i32` to `mut ref`
parameters, `*best as usize` to `*best`, `&s[..]` to `s[..]`, `!` to
`not`, the calls' `&mut` to `mut`, `HashSet::new()` to `Set.new()`,
`let mut best = 0` typed `i32`, and `Solution::` to `Solution.`. It then
checks and agrees with no hand edit.
