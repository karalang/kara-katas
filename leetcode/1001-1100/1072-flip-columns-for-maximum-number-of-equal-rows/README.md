# 1072. Flip Columns For Maximum Number of Equal Rows

You are given an `m x n` binary matrix `matrix`. You can choose any number
of columns in the matrix and flip every cell in that column (change the
value of the cell from 0 to 1 or vice versa). Return the maximum number of
rows that have all values equal after some number of flips.

```
[[0,1],[1,1]]              ->  1
[[0,1],[1,0]]              ->  2
[[0,0,0],[0,0,1],[1,1,0]]  ->  2
```

**Constraints:** `1 <= m, n <= 300`; every cell is 0 or 1.

A set of flips makes a row all zeros exactly when it flips the columns
where the row has a 1, and all ones when it flips the columns where it has
a 0. So two rows can end up equal together exactly when they are the same
or each other's complement, and the answer is the size of the largest such
group. Read with its first cell as 0 (each cell XORed with the first), a
row and its complement read the same.

The arms take the matrix as `Vec[Vec[i64]]` and return the answer as an
`i64`.

## Approaches

| file | mechanism |
|---|---|
| `equal_rows.kara` ★ | each row read as a `String` of `'0'`s and `'1'`s, a `'1'` where the cell differs from the first, counted in a `Map[String, i64]`; the largest count. O(m * n) |
| `equal_rows_brute.kara` | every row against every other, cell by cell: the rows equal to it or to its complement, the comparison stopping at the first cell that rules out both. O(m^2 * n) |
| `equal_rows_sorted.kara` | the rows XORed with their first cell (`Vec[Vec[i64]]`), sorted, and the longest run of equal neighbours. O(m * n * log m) |
| `equal_rows_bits.kara` | each row packed 64 cells to a word (`Vec[u64]`, `|= 1u64 << (j % 64)`) where the cell differs from the first, counted in a `Map[Vec[u64], i64]`; `counts.values().max()`. O(m * n) |
| `equal_rows_trie.kara` | a binary trie over the rows XORed with their first cell (`Vec[Array[i64, 2]]` of children), each row ending at a node that counts it. O(m * n) |
| `equal_rows_solution.kara` | LeetCode's Rust template (`use std::collections::HashMap`, `struct Solution;`, `HashMap<Vec<i32>, i32>`, `\|&x\| x ^ row[0]`, `*count.entry(key).or_insert(0) += 1`, `*count.values().max().unwrap()`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 15 lines: the answers for LeetCode's three
examples and six more; the sum and a checksum of the answers for 3000
random matrices up to 8 by 6 and for 40 up to 300 by 300, each row one of
one to three patterns, its complement, or one time in four a row of its
own; and the answers for 300 by 300 of zeros and of stripes, for the
numbers 0 to 299 in 9 bits, and for one row of zeros. `equal_rows.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every set of columns, as the bits of a mask, flipped, and the
rows that then hold one value in every cell counted; the most over all
sets. It checks 2000 problems, 1000 up to 6 rows by 4 columns and 1000 up
to 12 by 8, each row one of one to three patterns, its complement, or one
time in four a row of its own. Every random choice is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the rows reversed give the same answer |
| P3 | the columns reversed give the same answer |
| P4 | the first column flipped, and the first row complemented, give the same answer |
| P5 | the matrix stacked on itself answers twice as many, and each row written twice side by side answers the same |
| P6 | each arm agrees with at least three of the other five |

The differential prints `2000 problems: checksum 248228774, 96000 checks
over 6 arms: 0 failures` under every lane in Verification; a Python
reading of the same 2000 problems gives the same checksum. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Fifteen are kept, two or three to
each arm; every kept edit fails the same way under both backends, none
by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: rows not read with their first cell as 0 | P1 1214, P4 1005, P6 1214 |
| M2 | ★: the key keeps only the cells that differ | P1 367, P3 294, P6 367 |
| M3 | brute: `flipped` never cleared, so every row is a complement | P1 1126, P6 1126 |
| M4 | brute: the first column never compared | P1 445, P3 377, P5 445, P6 445 |
| M5 | brute: the first row never counted | P1 1418, P2 417, P5 1418, P6 1418 |
| M6 | sorted: the rows reversed, not sorted | P1 682, P5 1033, P6 682 |
| M7 | sorted: a run counted to two at most | P1 1176, P5 1584, P6 1176 |
| M8 | sorted: a run starts at nothing | P1 2000, P5 2000, P6 2000 |
| M9 | bits: every differing cell sets the same bit | P1 798, P4 406, P6 798 |
| M10 | bits: the number of patterns, not the most rows | P1 1516, P5 2000, P6 1516 |
| M11 | trie: a node counts one row | P1 1584, P5 2000, P6 1584 |
| M12 | trie: the last row's count, not the most | P1 319, P2 474, P6 319 |
| M13 | solution: the fewest rows, not the most (`min`) | P1 925, P6 925 |
| M14 | solution: rows OR-ed with their first cell, not XORed | P1 1195, P3 653, P4 2240, P6 1195 |
| M15 | solution: each row counted twice | P1 2000, P6 2000 |

P1 and P6 kill all fifteen, P5 seven, P4 and P3 three each, P2 two. P5's
stacking doubles every count, so an edit that adds a fixed amount or caps
a count shows there and one that scales every count (M15) does not. P2
sees only an edit that treats the rows unequally: M5 skips the first and
M12 keeps the last. P4 sees the edits that stop treating a row and its
complement as one (M1, M9, M14).

Of the fifteen not kept, two crash: the bits arm's words counted as
`row.len() / 64`, so a row under 64 cells has none and the first write is
out of range, and the trie's walk sent back to the root at every cell,
which indexes a child that was never made. One survives: the trie's new
child pointed at the last node made rather than at the one about to be
pushed. On rows of one length it still seems to send different rows to
different nodes; a Python search over 200000 random matrices found no
matrix where it answers differently, so it is kept out as equivalent
(inferred, not proved). The other twelve fail as a kept edit: the rows
not read with their first cell as 0 in the brute (complements uncounted),
sorted, bits, trie and solution arms as M1; a new pattern counted twice
in the ★ and solution arms as M8; the last row's count in the ★ and brute
arms as M12; the count never grown in the ★ arm as M7; neighbours compared
by their first cell as M3; and the bits arm's count never grown as M11.

## Verification

Every arm prints the same output as `equal_rows.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file. Under `karac __mir-run` the arms take 1.4 s to 4.3 s, the brute
arm 26 s and the differential 11 s.

Every file went through `karac fix`. The Rust arm reaches a clean check
in two rounds: the syntax (the `use` line deleted, `struct Solution {}`,
`Vec[..]` and `HashMap[..]` for `Vec<..>` and `HashMap<..>`, `HashMap.new`
and `Solution.` for the `::` paths, the `&` dropped from `|&x|`), then
`HashMap` to `Map`. A third round dropped the `as i64` from the harness's
bridge, since an `i32` widens to `i64` without one. In the arms written
in Kāra it turned `||` and `&&` into `or` and `and`, and split `counts[key]
= counts.get(key).unwrap_or(0) + 1` into a `let` and the assignment, since
a map assignment moves its key before the value runs. The kata found one
compiler gap, fixed in kara `274ec2990d` with `tests/kata_1072_check_gaps.rs`:

- **Rust's array type inside a generic argument.** The trie arm was first
  written `let mut next: Vec[[i64; 2]] = [[-1, -1]];`. On its own `[T; N]`
  is reported as Rust's array type with a fix to `Array[T, N]`, but in a
  generic argument list a `[` was taken for a shape literal
  (`Tensor[f64, [3, 4]]`), whose parser stopped at the `;` with "Expected
  `]`, found `;`", and `karac fix` inserted a second `;`
  (`Vec[[i64; 2;]]`). A bracket that holds a `;` at its own depth is now
  read as a type there, so the fix to `Vec[Array[i64, 2]]` applies in one
  round. Kara B-2026-11-08-54.

## Benchmarks

The bench builds 200 matrices once, in all five languages, the way the
arms' random sets do: up to 300 by 300, each row one of up to three
patterns, its complement, or one time in four a row of its own. It
answers every matrix 30 times with the ★ arm's count of patterns in a
hash map. Every implementation prints `6000 calls: answers sum 447390,
checksum 251407173`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with kara `f723e9c165`
on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.388 to 0.455 s | 0.405 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.436 to 0.521 s | 0.458 s |
| Rust (`rustc -O`) | 0.449 to 0.535 s | 0.491 s |
| Kāra (`karac build`) | 0.479 to 0.536 s | 0.503 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.479 to 0.588 s | 0.504 s |
| Go | 0.630 to 0.702 s | 0.663 s |
| Python | 7.2 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.476 s) is below its real time.

Kāra runs level with both Rust builds, within 10% of their medians. The
two programs do the same work: each row's key is a `String` grown one
character at a time, hashed with SipHash-1-3, and looked up and stored in
the map. Under callgrind Kāra runs 4.29 billion instructions and Rust
4.46 billion; in Kāra 19% are the hash (`karac_hash_bytes`) and in Rust
about a quarter are the allocator (`malloc`, `realloc` and `free`). C runs 1.46 billion:
its key is allocated once at the row's length and hashed with FNV-1a, one
multiply a byte, and its table is a flat array of slots. FNV's chain of
dependent multiplies keeps C's lead to 1.25x in time, against 2.9x in
instructions. Go's map hashes the key with its own AES-based hash; its
1.3x is not broken down here.
