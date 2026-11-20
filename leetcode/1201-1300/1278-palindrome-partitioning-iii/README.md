# 1278. Palindrome Partitioning III

You are given a string `s` containing lowercase letters and an integer
`k`. You need to:

- First, change some characters of `s` to other lowercase English
  letters.
- Then divide `s` into `k` non-empty disjoint substrings such that each
  substring is a palindrome.

Return the minimal number of characters that you need to change to divide
the string.

```
s = "abc", k = 2       ->  1
s = "aabbc", k = 3     ->  0
s = "leetcode", k = 8  ->  0
```

**Constraints:** `1 <= k <= s.length <= 100`; `s` only contains
lowercase English letters.

The arms are `fn palindrome_partition(s: Str, k: i64) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `palindrome_partition.kara` ★ | by dynamic programming over two tables: the changes that make each substring a palindrome, one per mismatched pair, built from the inside out; then the fewest changes for the first `j` letters in `p` pieces, the last piece tried at every start. O(k n^2) |
| `palindrome_partition_memo.kara` | by memoised recursion: the fewest changes from a start in a number of pieces is the best over the first piece's end, its changes counted by two pointers, each answer kept in a `Map[(i64, i64), i64]` |
| `palindrome_partition_centres.kara` | by centres: every substring's changes found by growing it outward from each of its 2n - 1 centres, a mismatched pair adding one as it grows; then one row of answers per piece count, each entry a `map` and `min` over the last piece's start |
| `palindrome_partition_bytes.kara` | over bytes: the string read as `bytes()`, the answers for (pieces, length) in one flat `Vec`, filled forward from each reached prefix by every next piece, whose changes are counted where they are needed |
| `palindrome_partition_solution.kara` | a Rust solution as LeetCode's Rust users write it (`s.as_bytes()`, `vec![vec![..]; ..]` tables of `i32`, `usize` loops, `i32::MAX / 2` as unreached), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples (`1 0 0`);
2000 random strings of 1 to 30 letters from the first 2 to 4, each cut
into 1 to all of its letters (`2000 random strings: 1301 changes,
checksum 888016806`); and the constraints' top, 100 letters all `a` in
one piece, `ab` 50 times in one and in two, and 100 letters from all 26
in 1, 7 and 100 pieces (`0 50 0 48 37 0`). `palindrome_partition.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac run` and `karac build`, and under the
AddressSanitizer build.

The Mend loop: the ★, memo and centres arms checked clean as first
written. The bytes arm was written with Rust's `s.as_bytes()`; E0236 said
a string's bytes are `.bytes()`, and `karac fix` made that edit. The
solution arm takes one round of 12 fixes by `karac fix`'s count:
`s.as_bytes()` to `s.bytes()`, `vec![vec![0; n]; n]` to
`Vec.filled(n, Vec.filled(n, 0i32))`, `usize` to `i64`, `i32::MAX` to
`i32.MAX`, `&str` to `Str`, `struct Solution;` to `struct Solution {}`,
`::` to `.`, and the wrapper's `as i64` on the `i32` answer dropped as a
widening Kāra does by itself. Rust's `1..=n` ranges stay. No gap was met.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way of cutting the string into `k` non-empty pieces,
each gap between letters cut or not; a piece made a palindrome by
changing one letter of each pair that differs from its mirror, counted by
comparing the piece with its reverse; and the fewest changes over all the
cuttings. 2000 random strings of 1 to 9 letters from the first 2 or 3.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | at least 0 and at most half the longest piece, `(n - k + 1) / 2` |
| P3 | the string reversed, the same answer |
| P4 | the letters renamed, the same answer |
| P5 | one more letter and one more piece, never more changes |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 strings: checksum 680185418,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the same
checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the inner pair of a four-letter substring not counted | P1 129, P6 516 |
| S2 | ★: the last piece never starting right after one letter per earlier piece | P1 2000, P2 2000, P5 2000, P6 8000 |
| M1 | memo: the first piece never leaving exactly one letter per later piece | P1 657, P2 401, P3 346, P5 966, P6 657 |
| M2 | memo: an answer kept under (parts, start) | P1 2, P3 4, P5 2, P6 2 |
| C1 | centres: the odd-length substrings' changes never found | P1 243, P6 243 |
| C2 | centres: a prefix as long as its piece count left unreached | P1 474, P2 401, P3 127, P5 637, P6 474 |
| B1 | bytes: a piece's middle pair skipped | P1 311, P6 311 |
| B2 | bytes: the last letter never starting a piece | P1 893, P2 637, P3 346, P5 329, P6 893 |
| O1 | solution: neighbouring letters never compared | P1 311, P6 311 |
| O2 | solution: no prefix cut into as many pieces as it has letters | P1 893, P2 637, P3 346, P6 893 |

All ten are caught, every one by P1, the statement read literally. The
four that count too few changes (S1, C1, B1, O1) are seen by P1 alone: an
answer too low still lies in P2's bounds, a reversed or renamed string
is miscounted the same way, and P5 only asks for no more. The five that
leave some cutting unreached (S2, M1, C2, B2, O2) answer more than half
the longest piece, which P2 sees, and P3, the string reversed, sees all
of them but S2, which misses every cutting alike. P4, the letters renamed, catches none: no
edit looks at which letters they are. M2, the memo's key swapped, is
caught on 2 strings only, where a swapped key meets another state's.
The first versions of S1 (`len > 3`, which changes only three-letter
substrings, whose inner pair is one letter) and C2 (a write to the row's
unused first entry) were equivalent and were replaced by these.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (the changes for every substring, then the fewest for each prefix in
each number of pieces) on 200 random strings of 100 letters from 2 to
26, each cut into 1 to 100 pieces, drawn once; 20 rounds, every answer
folded into a checksum. Every program prints `20 rounds of 200 strings
of 100 letters: checksum 936885027`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 1.821 to 1.976 s | 1.871 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.827 to 1.948 s | 1.895 s |
| Rust (`rustc -O`) | 1.725 to 1.829 s | 1.780 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.827 to 1.995 s | 1.911 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 1.813 to 1.989 s | 1.876 s |
| C (`clang -O3`) | 1.134 to 1.267 s | 1.188 s |
| C (`clang -O3 -march=x86-64-v3`) | 1.245 to 1.320 s | 1.295 s |
| Go | 2.130 to 2.324 s | 2.209 s |
| Python | 49.09 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (1.911 s
against 1.895 s), and the two ranges overlap. Kāra takes about 1.6x C's
time (1.895 s against 1.188 s); Kāra is about 14% ahead of Go (1.895 s
against 2.209 s). Python takes about 26x Kāra's time. No profile was
taken.
