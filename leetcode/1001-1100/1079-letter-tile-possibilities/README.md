# 1079. Letter Tile Possibilities

You have `n` tiles, where each tile has one letter `tiles[i]` printed on
it. Return the number of possible non-empty sequences of letters you can
make using the letters printed on those tiles.

```
tiles = "AAB"     ->  8      ("A", "B", "AA", "AB", "BA", "AAB", "ABA", "BAA")
tiles = "AAABBC"  ->  188
tiles = "V"       ->  1
```

**Constraints:** `1 <= tiles.length <= 7`; `tiles` consists of uppercase
English letters.

A sequence uses each tile at most once, and two sequences that spell the
same letters are one sequence, whichever tiles of a letter they took.

The arms take the tiles as a `String` and return the count as an `i64`.

## Approaches

| file | mechanism |
|---|---|
| `tiles.kara` ★ | the tiles counted by letter into an `Array[i64, 26]`, and a depth-first walk that places one more tile of each letter left: every placement is one more sequence, and the walk below it counts the sequences that extend it. O(number of sequences) |
| `tiles_set.kara` | the sequences themselves: every ordering of every choice of tiles, built by placing unused tiles one at a time into a `Set[String]`, which keeps one copy of what equal tiles make twice. O(sum over k of n!/(n-k)!) |
| `tiles_multinomial.kara` | counted, not walked: for every way to take `k` tiles of each letter, the sequences of exactly those tiles number (k1 + k2 + ..)! / (k1! k2! ..); the answer is their sum less the empty choice. The letters' counts come from a `Map[u8, i64]`, whose order the sum does not see. O(product of (count + 1)) |
| `tiles_egf.kara` | a table over lengths, one letter at a time: `ways[n]` is how many sequences of length `n` the letters so far make, and a letter with `c` tiles puts `k` of them among the places of a sequence of length `n` in `C(n + k, k)` ways. O(26 * n^2) |
| `tiles_stack.kara` | the ★ walk without recursion: a `Vec[Array[i64, 26]]` stack of the counts still left, each copied as it is pushed; every letter a popped count still has is one more sequence. O(number of sequences) |
| `tiles_solution.kara` | LeetCode's Rust template (`struct Solution;`, a `dfs` nested in the method over `&mut [i32; 26]`, `count[(c as u8 - b'A') as usize]`, `Solution::`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: the counts for LeetCode's three
examples and seven more (`ABCDEFG` gives 13699, the most seven tiles
make); the total and a checksum over 300 random tile sets of 1 to 7 tiles
over 1 to 7 letters; and the 34 multisets of 1 to 4 tiles over `A` to `C`,
339 sequences in all. `tiles.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every string of 1 to `n` letters, each a letter printed on some
tile, counted when no letter is in it more times than the tiles carry it
(the strings are numbers in base `d` over the `d` letters, so nothing of
the arms' walks is reused). It checks 2000 problems, 600 of 1 to 6 tiles
over 1 to 3 letters and 1400 of 1 to 5 tiles over 1 to 5 letters, the
letters drawn from the whole alphabet; P4 to P6 ask the arms about up to
7 tiles. Every random choice is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every letter moved on by the same amount in the alphabet, and the tiles reversed, answer the same |
| P3 | the answer is at least `n` and the number of letters `d`, at most every ordering of every choice of `n` distinct tiles, exactly `n` when `d` is 1, and exactly the most when `d` is `n` |
| P4 | the answer is the sum, over each letter, of that letter alone and that letter before a sequence of the other tiles |
| P5 | a tile of a new letter answers the old count, plus one for each of the `len + 1` places of every sequence and of the empty one: `f(T + x) = 2 f(T) + 1 + L(T)`, `L(T)` the sequences' total length read literally |
| P6 | one more tile of a letter there is adds sequences, but fewer than a tile of a new letter: `f(T) < f(T + c) < f(T + x)` |

All 72,000 checks pass on every arm: `2000 problems: checksum 811645300,
72000 checks over 6 arms: 0 failures`. A Python reading of the same
problems with `itertools.product` gives the same checksum.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Twenty-seven are caught, each the
same way under both backends, and one more stops both with a stack
overflow (the solution arm putting a tile back twice, so the walk never
runs out). Fifteen are kept, no two failing the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last tile of a letter never placed (`> 1`) | P1 2000, P3 1856, P4 1257, P5 2000, P6 2000 |
| M2 | ★: Z never placed (`0..25`) | P1 131, P2 252, P3 106, P4 131, P5 206, P6 156 |
| M3 | ★: the empty sequence counted at every step | P1 2000, P3 1505, P4 2000, P5 2000 |
| M4 | set: only sequences of every tile kept | P1 1629, P3 1167, P4 1629, P5 2000, P6 916 |
| M5 | set: the first tile never placed | P1 2000, P2 371, P3 1308, P4 1046, P5 2000, P6 542 |
| M6 | set: a sequence never extended | P1 1629, P3 1629, P4 1629, P5 2000, P6 2000 |
| M7 | multinomial: 2! taken as 1 | P1 1084, P3 298, P4 760, P5 2000 |
| M8 | multinomial: repeated tiles not divided out | P1 1331, P3 545, P4 1331, P5 1331 |
| M9 | multinomial: the empty choice counted | P1 2000, P3 1214, P4 1455, P5 2000 |
| M10 | egf: the new tiles only at the end (no `C(n + k, k)`) | P1 1084, P3 298, P4 1084, P5 2000 |
| M11 | egf: every letter must be used (`1..=c`) | P1 1084, P3 298, P4 1084, P5 2000, P6 371 |
| M12 | egf: the longest length grown by one tile a letter | P1 562, P2 309, P3 73, P4 562, P5 904, P6 722 |
| M13 | stack: N to Z taken for A to M (`% 13`) | P1 86, P3 45, P4 86, P5 207, P6 102 |
| M14 | stack: only a placement that uses up its letter counted | P1 1331, P3 545, P4 1331, P5 1156, P6 916 |
| M15 | solution: the walk below overwrites the count (`sum =`) | P1 2000, P3 2000, P4 2000, P5 2000, P6 2000 |

P1, P3, P4 and P5 catch all fifteen, P6 ten and P2 three. P2 sees only an
edit whose answer depends on which letter or which tile comes first: Z in
M2, the first tile in M5 and the letters' order in M12. The others count
every letter and every tile alike.

Of the fifteen not kept, one is the crash above and five fail as a kept
edit: the multinomial arm's last tile never taken as M1, the egf arm's
longest sequences never extended as M15, the egf arm's empty sequence as
M9, and the solution arm's empty sequence and first tile dropped as M3
and M5. Seven fail in a way of their own but were not needed: the ★ arm's
tile never put back and the set arm's tile never freed (alike), repeated
tiles counted once in the ★ and multinomial arms and every tile of a
letter used at once in the stack arm (alike), and the stack arm's count
per tile left and its A never placed. Two are equivalent and survive: the
set arm putting each tile in front of the sequence rather than behind
(the set of reversed sequences is as large), and the solution arm
indexing its counts by `c % 26` rather than `c - 'A'` (65 to 90 mod 26 is
13 to 25 and 0 to 12, the same 26 places in another order).

## Verification

Every arm prints the same output as `tiles.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file. Under `karac __mir-run` the arms take 0.2 s to 2.2 s (the set
arm the slowest) and the differential 30.0 s.

The kata found one diagnostics gap, fixed in kara `10ef8e8c7a` with
`tests/kata_1079_char_cast_fix.rs`:

- **`c as u8` on a `char` got a help but no fix.** The Rust arm keeps
  LeetCode's `count[(c as u8 - b'A') as usize] += 1` over
  `tiles.chars()`. Kāra refuses the cast, since a scalar value does not
  fit in 8 bits, and its help names `c as u32 as u8`, which is what Rust
  means by `c as u8`; but the error had no edit, so `karac fix` stopped
  there. It now inserts the ` as u32` after the operand, unless the
  operand is itself a cast. Kara B-2026-11-09-18.

Every file went through `karac fix`. In the set arm it put the `.iter()`
before `.collect()` on `tiles.bytes()`. The Rust arm reaches a clean
check in three rounds and gives the text the arm holds: the
syntax (`struct Solution {}`, `&mut [i32; 26]` to `mut ref Array[i32,
26]`, `dfs(mut count)`, `Solution.`); then the nested `fn dfs` moved out
of the method; then `sum`'s type written as `i32`, the recursive call's
`mut`, the lossless `as i64` dropped and the ` as u32`. In the differential
it wrote `fresh.to_string()` for a `char` handed to `contains` and
dropped a redundant `as u8`.

## Benchmarks

The bench builds 200 sets of 7 tiles once, each over 1 to 7 letters
drawn from the alphabet, and counts every set with the ★ arm in each of
200 rounds, in an order that changes with the round, folding every count
into a checksum. Every implementation prints `200 rounds of 200 sets of
7 tiles: 44937000 sequences, checksum 600593841`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `c9e5bdc8b7`
on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.770 to 0.861 s | 0.810 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.773 to 0.863 s | 0.813 s |
| C (`clang -O3`) | 0.781 to 0.905 s | 0.826 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.788 to 0.991 s | 0.851 s |
| Go | 1.016 to 1.211 s | 1.054 s |
| Rust (`rustc -O`) | 1.023 to 1.160 s | 1.096 s |
| Python | 35.4 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.80 s) is its real time.

The work is 45 million steps of one recursive walk, each a loop over 26
counts, with no allocation after the sets are built. Kāra, C and Rust
with overflow checks are level, within 5% of one another; plain `rustc
-O` takes 29% longer than its overflow-checked build of the same source,
which these runs did not explain. Python runs the same walk at 44x Kāra.
