# 2014. Longest Subsequence Repeated k Times

You are given a string `s` of length `n` and an integer `k`. Find the
longest subsequence repeated `k` times in `s`: a subsequence `seq` such
that `seq * k`, `seq` written `k` times one after another, is a subsequence
of `s`. If there are several, return the lexicographically largest; if
there is none, return the empty string.

```
s = "letsleetcode", k = 2  ->  "let"
s = "bb", k = 2            ->  "b"
s = "ab", k = 2            ->  ""
```

**Constraints:** `2 <= k <= 2000`; `2 <= n < 8k`; `s` is lowercase
English letters.

`n < 8k` keeps the answer to at most 7 letters, and only a letter seen at
least `k` times can be in it. Every prefix of a valid answer, and every
string left by deleting one of its letters, is valid too.

## Approaches

| file | mechanism |
|---|---|
| `longest.kara` ★ | a breadth-first search from the empty string over the letters seen `k` times, each candidate grown by one letter and kept while it still repeats `k` times; each level comes out sorted, so the last candidate found is the answer. O(n * 8^7) at worst |
| `longest_dfs.kara` | each letter usable `count / k` times; the lengths tried from the longest the pool allows down, the candidates grown from `z` down and cut at the first prefix that no longer repeats; the first to reach the length wins |
| `longest_table.kara` | the ★ arm's search over letter indices, a candidate checked by jumping through a table of where each letter next occurs: `k * len` jumps however long `s` is. O(26 n) for the table |
| `longest_levels.kara` | the valid candidates of each length in a `SortedSet`; `t + c` checked only when `t` without its first letter, then `c`, is already in the level; the answer is the largest of the last level |
| `longest_perms.kara` | every arrangement of every part of the pool of usable letters (at most 7) listed once in a `Set`, each checked, the best taken by `max_by_key` on (length, string). No pruning |
| `longest_solution.kara` | LeetCode's Rust template (a unit struct, `impl Solution`, `as_bytes()`, `b'a'`, `[0; 26]` counts, a `VecDeque<Vec<u8>>`, `Self::check`, `&[u8]` slices, `String::from_utf8`, a `&str` wrapper), carried by `karac fix` to a clean check |
| `differential.kara` | all six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's three
examples and five more; then the total length and a checksum of the
answers for 2000 strings of 2 to 31 letters with `k` from 2 to 6, and for 6
strings of 2000 letters with `k` from 251 to 400. A string is a pattern
written out again and again, some of its letters dropped, stray letters
between. `longest.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every subsequence of `s`, by bitmask, kept when written `k` times
it is a subsequence of `s`, the longest and then the largest of those kept.
It checks 800 problems of 2 to 11 letters from up to 5. Every random choice
of a problem (the string, `k`, a shift, a letter to append) is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer written `k` times is a subsequence of `s` |
| P3 | every letter moved the same number of places up the alphabet moves the answer's letters alike |
| P4 | `k` raised by one never gives a longer answer, nor a larger one of the same length |
| P5 | one more letter appended to `s` never gives a shorter answer, nor a smaller one of the same length |
| P6 | each arm agrees with at least three of the other five |

The differential prints `800 problems: checksum 87039368, 28800 checks over
6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Fifteen are kept, two or
three to each arm. All thirty are killed, each fails the same way under
both backends, none by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a letter seen exactly `k` times left out | P1 157, P6 157 |
| M2 | ★: `k - 1` copies enough | P1 411, P2 411, P6 411 |
| M3 | dfs: a letter never put back in the pool | P1 74, P4 36, P5 30, P6 74 |
| M4 | dfs: the last letter never checked | P1 74, P2 74, P6 74 |
| M5 | table: the next index one past the letter | P1 564, P6 564 |
| M6 | table: the letter `a` never used | P1 332, P3 314, P6 332 |
| M7 | levels: the smallest of the last level taken | P1 64, P4 7, P5 22, P6 64 |
| M8 | levels: the tail's letter put first | P1 14, P6 14 |
| M9 | levels: the smallest letter never appended | P1 288, P6 288 |
| M10 | arrangements: the pool divided by `k + 1` | P1 376, P6 376 |
| M11 | arrangements: the largest taken, whatever its length | P1 47, P4 1, P5 3, P6 47 |
| M12 | arrangements: no single letter listed | P1 282, P6 282 |
| M13 | Rust: a later letter matching | P1 103, P2 103, P6 103 |
| M14 | Rust: only candidates under 3 letters grown | P1 53, P6 53 |
| M15 | Rust: each letter counted once | P1 592, P6 592 |

P1 and P6 kill all fifteen, P2, P4 and P5 three each, and P3 one. Most
edits make an arm miss a valid answer, and what it returns then is shorter
or smaller but still valid, which only the literal reading and the vote
see. P2 checks the answer itself, so it sees the three edits that accept
one that does not repeat `k` times: `k - 1` copies (M2), the last letter
unchecked (M4), and a later letter taken as a match (M13). P4 and P5 see
the edits whose choice among the valid answers is not by rank, so that
fewer or more valid answers can move it the wrong way: a pool that loses
letters as the search goes (M3), the smallest of the longest (M7), and the
largest whatever its length (M11). P3 moves every letter up the alphabet,
so it sees only the edit that treats a letter by its name rather than its
place in the order, `a` never used (M6). M8 is the faintest, 14 problems
in 800: the rotated tail is not a subsequence of the candidate, so it can
prune a valid candidate, but only when the rotation is missing from a
level that the true tail is in.

The other fifteen fail as a kept one does, or with counts of their own. A
letter seen exactly `k` times left out fails alike in the ★, levels and
Rust arms (M1); `k - 1` copies alike in the ★, table and levels arms (M2).
The smallest of the longest fails alike five ways: the ★ arm keeping only a
longer candidate, the ★ arm trying its letters from `z` down, the dfs arm
trying them from `a` up, the arrangements arm's `min_by_key`, and M7. The
pool divided by `k + 1` fails alike in the dfs arm and M10; the dfs arm's
length capped at 3 as M14; and an answer that is always empty alike three
ways: the arrangements arm using a letter only while two remain, the table
built from the second letter on, and M15. Keeping only the first candidate
fails alike in the table and Rust arms, and a candidate never grown in the
★ arm with counts of its own. One draft was replaced: the table arm reusing
a letter's index (`at = next[at][c]`) makes every candidate repeat, so the
search never ends and the interpreter stops at its step limit.

## Verification

Every arm prints the same output as `longest.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error. `karac
run` and a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 1.2 s (table) to 8.1 s
(arrangements) and the differential 11 s.

The five arms were written in Kāra. Three drew one fix each from `karac
fix`: the depth-first arm's `return Some(prefix)` of a borrowed parameter
became `Some(prefix.clone())`, the levels arm's `level.last()` on a
`SortedSet` became `level.max()`, and the arrangements arm's `let pool = ..`
passed as `mut pool` became `let mut pool`.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` alone, in two rounds (29 and 1 edits). The first
carries the `use`, the struct, the `Vec<..>` and `VecDeque<..>` types, the
`::` paths, the `&` patterns and borrows, `&[u8]` as `Slice[u8]`, `let (mut
i, mut cnt)` and `&str`; the second turns `as_bytes()` into `bytes()`.
`if Self::check(s, &nxt, k)` was a parse error with no fix, "Expected `{`,
found `::`", which took the rest of the `impl` with it; since kara
d9a6a4fd5a the fix writes the type's name, `Solution.check`.

## Benchmarks

The bench builds 200 strings of 2000 letters once in all five languages,
each a pattern of up to 7 letters from 2 to 9 written out with a few
letters dropped and a few strays, each with its own `k` from 251 to 300,
and runs the ★ arm on each for 5 rounds: 1000 calls. Every implementation
prints `1000 calls: total length 4355, checksum 500376093`. Every language
builds each candidate as its own heap string, as the Kāra program does.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 0.630 to 0.703 s | 0.642 s |
| Go | 0.690 to 0.749 s | 0.712 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.729 to 0.796 s | 0.752 s |
| C (`clang -O3`) | 0.726 to 0.764 s | 0.757 s |
| Kāra (`karac build`) | 0.758 to 0.796 s | 0.773 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.782 to 0.853 s | 0.806 s |
| Python | 8.5 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.760 s) is not above its real time (0.773 s).

The sequential Kāra program is 1.07x Rust under overflow checks and 1.06x
C.