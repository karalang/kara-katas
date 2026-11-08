# 1061. Lexicographically Smallest Equivalent String

Given two strings `s1` and `s2` of the same length and a string
`baseStr`, `s1[i]` and `s2[i]` are equivalent for every `i`. The relation
is reflexive, symmetric and transitive, so `a == b` and `b == c` make
`a == c`. Return the lexicographically smallest string equivalent to
`baseStr`: each of its letters replaced by the smallest letter equivalent
to it.

```
s1 = "parker",   s2 = "morris",   baseStr = "parser"      ->  "makkek"
s1 = "hello",    s2 = "world",    baseStr = "hold"        ->  "hdld"
s1 = "leetcode", s2 = "programs", baseStr = "sourcecode"  ->  "aauaaaaada"
```

**Constraints:** `1 <= s1.length, s2.length, baseStr.length <= 1000`;
`s1.length == s2.length`; every string is lowercase English letters.

The pairs split the 26 letters into classes, and every letter of
`baseStr` is answered by the smallest letter of its class. A letter no
pair names is its own class.

## Approaches

| file | mechanism |
|---|---|
| `lexi.kara` ★ | a union-find over the 26 letters whose root is always the smallest letter of its class: a union hangs the larger root under the smaller, and a find compresses the path it walks. O((n + m) α(26)) |
| `lexi_recursive.kara` | the same union-find with a recursive find that points each letter it passes at the root on the way back. O((n + m) α(26)) |
| `lexi_graph.kara` | the pairs as edges on the letters, and a depth-first walk from each letter not yet reached, in order, so the walk's first letter is its class's smallest. O(26 + n + m) |
| `lexi_closure.kara` | the transitive closure on a 26 by 26 table (Warshall), each letter's smallest equivalent read off its row with `find`. O(n + m + 26^3) |
| `lexi_map.kara` | a union-find over the letters themselves in a `Map[char, char]` that holds only the letters some pair names, walked with `chars()`. O((n + m) α(26)) |
| `lexi_solution.kara` | LeetCode's Rust template (`struct Solution;`, a nested `fn find(parent: &mut Vec<usize>, x: usize)`, `as_bytes()`, `as usize`, `Solution::`), carried to Kāra by `karac fix`. O((n + m) α(26)) |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 15 lines: the answers for LeetCode's three
examples and seven more; the letters moved and a checksum of the answers
for 3000 problems of 1 to 8 pairs over 6 letters and for 3000 of 1 to 4
pairs over all 26; the same for 100 bases of 1000 letters and for 1000
pairs with a base of 1000; and a chain of 25 pairs that joins `z` to `a`
one letter at a time. `lexi.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each letter of the base grows a `SortedSet` from itself, a pair
with one letter in it and one out adding the other, until a pass over the
pairs adds nothing, and the smallest letter in the set answers it. It
checks 2000 problems: 1000 of 1 to 8 pairs over 6 letters with a base of 1
to 10 over 8 (two letters no pair names), and 1000 of 1 to 30 pairs over
26 with a base of 1 to 40. Every random choice of a problem is drawn
before any arm answers, so a wrong arm cannot change the problems the
others see.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is as long as the base, and no letter of it lies above the base's letter in the same place |
| P3 | the answer, taken as the base, is answered by itself |
| P4 | the pairs swapped (`s1` for `s2`), or both strings reversed, leave the answer |
| P5 | the base cut in two is answered by the two answers joined, and a pair of a base letter and its answer added to the pairs leaves the answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `2000 problems: checksum 518929279, 96000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Fifteen are kept, two or three to
each arm. All thirty are killed, each fails the same way under both
backends, none by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the larger root wins a union | P1 1823, P2 1684, P6 1823 |
| M2 | ★: find climbs one step | P1 1021, P3 944, P4 1210, P6 1021 |
| M3 | ★: the pairs misaligned by one | P1 1399, P4 2750, P5 1171, P6 1399 |
| M4 | recursive: find climbs two steps | P1 221, P3 197, P4 372, P5 98, P6 221 |
| M5 | recursive: each letter paired with itself | P1 1699, P6 1699 |
| M6 | graph: the edges one way only | P1 1383, P4 1657, P6 1383 |
| M7 | graph: a letter mapped to the one it was reached from | P1 1208, P2 949, P3 1208, P4 372, P6 1208 |
| M8 | graph: only the first letter of a class walked | P1 1208, P6 1208 |
| M9 | closure: only through `a` to `m` | P1 732, P3 310, P6 732 |
| M10 | closure: only letters below the middle one added | P1 654, P3 423, P5 64, P6 654 |
| M11 | map: the second string read backward | P1 1129, P5 1542, P6 1129 |
| M12 | map: the path pointed at the letter asked | P1 1433, P2 308, P3 955, P4 991, P5 927, P6 1433 |
| M13 | solution: the larger root wins a union | P1 1779, P2 1401, P4 2353, P6 1779 |
| M14 | solution: the last pair left out | P1 721, P4 993, P5 721, P6 721 |
| M15 | solution: find stopped at a parent one letter below | P1 421, P3 392, P4 658, P5 30, P6 421 |

P1 and P6 kill all fifteen, P4 nine, P3 and P5 seven each, and P2 four.
P2 sees an arm that answers a letter above the base's (M1, M7, M12,
M13); the others answer a letter at or below it, which only the literal
reading and the vote catch. P3 sees an answer that is not a root of its
own class: a find that stops short (M2, M4, M15), a class split (M9, M10)
or a letter mapped to one that is not its root (M7, M12). P5 catches every
edit that reads the pairs by position (M3, M11, M14).

Of the fifteen not kept, the recursive and graph arms' larger-root edits
and the closure arm's largest-letter edit fail exactly as M1, as their
arms do the same thing the same wrong way. The ★ arm reading a base
letter off its parent and the map arm doing the same fail alike, as do the
recursive arm always hanging the second root and the map arm dropping a
union whose smaller root comes second. The other eight each fail in a way
of their own.

## Verification

Every arm prints the same output as `lexi.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
file. Under `karac __mir-run` the arms take 1.1 s (★) to 4.5 s (closure)
and the differential 20.8 s.

The ★ arm was written as Kāra would first write it, `for (a, b) in
s1.bytes().zip(s2.bytes())` and `find(mut parent, (a - b'a') as i64)`,
and `karac fix` gave it the form here. Neither had a fix
before this kata: the `.iter()` went on the receiver of `zip` but not on
its argument, a `Slice` with no `into_iter` to suggest, and the
`lossless_cast` lint had no fix for a parenthesized operand. The four
other Kāra arms were written in Kāra and checked clean, the differential
after `karac fix` renamed `SortedSet.first()` to `min()`.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` alone, in five rounds: the syntax (eight fixes),
the nested `fn` moved to the top level, then `as_bytes`, the missing
`.iter()`, the `usize` types and the `mut` markers, then each `as usize`
argument cast to `i64`, and last those casts dropped. The nested `fn`, the
`as usize` argument and the `SortedSet` rename had no fix before this kata
(kara `9bdb6b0bc4` and `39dbc078da`, `tests/kata_1061_check_gaps.rs`).

## Benchmarks

The bench builds 100 pairs of strings of 1000 letters, over 2 to 26 of
them, and 100 bases of 20000 letters once in all five languages, then
answers every pair with every base: ten thousand calls, each 1000 unions
and 20000 finds, the answer summed letter by letter. Every implementation
prints `10000 calls: letters sum 20999874160, checksum 759475784`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `39dbc078da` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.802 to 0.888 s | 0.844 s |
| Rust (`rustc -O`) | 1.003 to 1.169 s | 1.058 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.062 to 1.159 s | 1.103 s |
| Kāra (`karac build`) | 1.131 to 1.238 s | 1.179 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.141 to 1.275 s | 1.209 s |
| Go | 1.497 to 1.621 s | 1.576 s |
| Python | 28.6 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (1.166 s) is below its real time.

Kāra is 1.10x Rust under overflow checks. Rust and Kāra build each answer
by pushing to a `String` that grows, and keep `parent` on the stack
(Rust's `[i64; 26]`) or in a fresh `Vec` (Kāra's `(0..26).collect()`);
C writes each answer into one buffer allocated once, which is likely most
of its lead over Rust (inferred from the shapes, not measured).

### Fixed-size tables are arrays (2026-11-08)

Until 2026-11-08 the 26-slot union-find parent was `(0..26).collect()`,
a heap vector per call where the Rust mirror uses `[i64; 26]`; the arms,
the differential and the bench now fill a `[0; 26]` array and `find`
borrows it as `mut ref Array[i64, 26]` (an `Array` has no
`FromIterator`: its length is part of its type). `karac fix` also took
the allow-level lints the files had picked up since (list literals for
`vec![..]`, redundant `ref` on borrowed parameters, lossless casts).
Every arm's output and the bench's sink line are byte-identical before
and after, under `__mir-run`, `__mir-llvm-run` and `build`; five
interleaved runs of the bench binary on the 4-core container took 1.15
to 1.27 s before and 0.97 to 1.02 s after. Any M5 row above predates the
change.
