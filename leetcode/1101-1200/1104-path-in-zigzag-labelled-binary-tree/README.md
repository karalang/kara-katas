# 1104. Path In Zigzag Labelled Binary Tree

In an infinite binary tree where every node has two children, the nodes
are labelled in row order. In the odd numbered rows (the first, third,
fifth, ...) the labelling is left to right, while in the even numbered
rows (the second, fourth, sixth, ...) it is right to left.

Given the `label` of a node in this tree, return the labels in the path
from the root of the tree to the node with that `label`.

```
label = 14  ->  [1,3,4,14]
label = 26  ->  [1,2,6,10,26]
```

**Constraints:** `1 <= label <= 10^6`.

The arms are `fn path_in_zig_zag_tree(label: i64) -> Vec[i64]`. Row
`d` holds the labels `2^(d - 1)` to `2^d - 1` whichever way it runs, so
10^6 is in row 20 and every path has at most 20 labels.

## Approaches

| file | mechanism |
|---|---|
| `path_in_zig_zag_tree.kara` ★ | walking up from the label: a node's parent in the plain order is half its place, so the parent is half the label's mirror in its row, `start + end - label`; the path pushed from the label up, then `reverse`d. O(log label) |
| `path_in_zig_zag_tree_plain.kara` | through the plain tree, numbered left to right in every row: the row from `leading_zeros`, the label's plain place its mirror on the even rows, the plain path that place shifted right row by row, each mirrored back on the even rows, by a closure in a `map` over `1..=depth` |
| `path_in_zig_zag_tree_rec.kara` | recursion: the path to a label is the path to its parent and then the label, the row found by a second recursion halving the label down to 1 |
| `path_in_zig_zag_tree_bits.kara` | through the binary digits: in the plain tree a node's ancestors are the prefixes of its digits, so the plain place is written with `f"{plain:b}"`, each prefix read back with `i64.from_str_radix` over a slice of the string, and the even rows mirrored |
| `path_in_zig_zag_tree_iter.kara` | iterator chains: `successors` from the label to the root, each parent the label with every bit below its highest flipped by `^` and then halved by `>>`, collected and reversed |
| `path_in_zig_zag_tree_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `label: i32`, `vec![0; level as usize]` filled from the end), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 14 lines: the paths for LeetCode's two
examples and ten more (the root, both of row 2, a row's first and last
labels on rows 3 to 5, 100 and 10^6), then over every label of the
first fourteen rows, 1 to 16383, the sum of the labels on their paths
(`path labels total 268304384, checksum 646547199`), and over 2000
random labels up to 10^6 how many nodes their paths hold (`37961 nodes
on their paths, checksum 94298905`). `path_in_zig_zag_tree.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the rows laid out down to the label's, each in the order its
labels sit, left to right on the odd rows and right to left on the
even, the label's place in its row found by `position`, and its parent
at half that place in the row above, up to the root. It checks 2000
problems in four kinds of 500: a label below 2^11 at random; the first
or last label of a row of 1 to 11; a label below 32; and the two labels
in the middle of a row of 2 to 11. Every random choice is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the path is the literal one |
| P2 | by a second reading, from the top down: one label in each row from the first to the label's, starting at 1 and ending at the label, each one of the two children of the one before, at places `2p` and `2p + 1` below place `p` |
| P3 | the path to a node on the path is the path cut there |
| P4 | the label's sibling, `label ^ 1`, has the same path but the last |
| P5 | the label's mirror in its row has every label of the path mirrored in its own row |
| P6 | the label's two children, the labels in the row below whose place halves to the label's, each have the label's path and then themselves |

All 72,000 checks pass on every arm: `2000 problems: checksum
606521215, 72000 checks over 6 arms: 0 failures`. A Python reading of
the same problems, laying out the rows, gives the same checksum.

P1 lays out the rows and P2 judges the path by another reading; P3 to
P6 compare the arm only with itself.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All thirty are caught. Fifteen are kept, no two failing the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a row's first label counted in the row above | P1 314, P2 314, P3 330, P4 465, P5 632, P6 697 |
| M2 | ★: the plain tree's parent | P1 1799, P2 1799, P6 1935 |
| M3 | ★: the path left from the label up | P1 1935, P2 1935, P3 1935, P4 1935, P6 2000 |
| M4 | plain: the label mirrored on the odd rows | P1 1935, P2 1935, P3 1578, P4 1935, P6 2000 |
| M5 | plain: the even rows never mirrored back | P1 1935, P2 1935, P3 911, P4 815, P6 1185 |
| M6 | plain: the mirror one too far | P1 1869, P2 1869, P3 266, P4 815, P5 1935, P6 2000 |
| M7 | rec: the root's row counted as 0 | stops: stack overflow |
| M8 | rec: the root left out | P1 2000, P2 2000, P3 65, P4 1935 |
| M9 | rec: each row counted twice | stops: shift amount out of range |
| M10 | bits: the decimal digits counted | stops: index out of bounds |
| M11 | bits: the mirror one too far | P1 1869, P2 1869, P3 270, P4 745, P5 1935, P6 2000 |
| M12 | bits: the label's own digits read | P1 815, P2 815, P3 911, P4 815, P6 2000 |
| M13 | iter: stopped at the second row | P1 1935, P2 1935, P4 1935, P6 65 |
| M14 | solution: a row's first label counted in the row above | P1 379, P2 379, P3 703, P4 465, P5 632, P6 697 |
| M15 | solution: the parent rounded up | P1 1797, P2 1797, P3 286, P4 1935, P5 1935, P6 2000 |

Of the twelve that run to the end, P1 and P2 catch all twelve, P4 and
P6 eleven, P3 ten and P5 five. 65 of the problems ask for the root,
whose path no edit but M8 gets wrong, so 1935 is every other problem.
P5 sees the five edits that put a row's ends in the wrong place (M1,
M6, M11, M14, M15); an edit that mirrors in the right row, or never
mirrors, gets a label and its mirror wrong the same way. P3 to P6,
which compare the arm only with itself, catch all twelve. M2, the plain
tree's parent, is caught only by P6: a path of plain parents agrees
with itself when cut, from the sibling and from the mirror, but P6
finds the children by the zigzag rule, and from them the plain parent
does not lead back to the label. The three that stop each stop their own way: M7's row one
short makes a parent larger than its child, and the recursion never
reaches the root; M9 shifts by twice the row; and M10, counting the
decimal digits for the binary ones, slices the string past its end.

One edit first written changed nothing: the iterator arm never flipping
the lowest bit, which the halving drops anyway. It was replaced by the
bit below the highest never flipped, which fails as M2.

The fifteen not kept all fail exactly as a kept edit: the plain tree's
parent (M2) is also the recursive and iterator arms' and the iterator
arm's unflipped bit; the path left from the label up (M3) is also the
iterator arm's; the root left out (M8) is also the ★, bits and solution
arms'; each row's end one too far in the ★ and solution arms fails as
M15; the label's own digits halved in the plain arm as M12; the odd
rows mirrored back in the bits arm as M4; the plain arm leaving out the
label's row and the iterator arm flipping the highest bit stop as M10,
the recursive arm's mirror one too far as M7, and the solution arm's
rows filled from the top as M9.

## Verification

Every arm prints the same output as `path_in_zig_zag_tree.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The kata found no compiler gap. The ★ arm was written as Kāra, and the
other five as Rust writes them; `karac fix` carried every Rust spelling
to a clean check:

- The plain arm in two rounds: `Vec<i64>` to `Vec[i64]`, the `as i64`
  on `leading_zeros()` dropped, the closure's `-> i64` and the `1i64`
  suffixes dropped, and `collect::<Vec<i64>>()` to `collect()`, the
  return type giving the target.
- The recursive arm in two: `Vec<i64>` and `vec![1]` to `[1]`.
- The bits arm in two: `format!("{:b}", label)` to `f"{label:b}"`, the
  closure's `d: usize` to `d: i64` and `3i64` to `3`, `Vec::new()` to
  `Vec.new()`, and `i64::from_str_radix(&digits[..d], 2)` to
  `i64.from_str_radix(digits[..d], 2)`.
- The iterator arm in one: `std::iter::successors` to `successors` and
  the closure's `|&x|` to `|x|`.
- The Rust solution in five: `struct Solution {}` declared, `vec![0;
  level as usize]` to `Vec.filled(level, 0i32)`, the `as usize` on the
  loop's range dropped, `i32` written on `lo` and `hi`, `Solution::` to
  `Solution.`, and `|&x|` to `|x|`.

## Benchmarks

The bench finds the path of every label from 1 to 10^6, LeetCode's
most, in a different order each of 8 rounds, with the ★ arm: 8 million
calls, each building and reversing a path of up to 20 labels. Every
implementation prints `8 rounds over the labels 1 to 10^6: 151611560
nodes on their paths, checksum 196585409`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `33ef2a7ad2`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.345 to 0.520 s | 0.386 s |
| C (`clang -O3`) | 0.380 to 0.520 s | 0.407 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.722 to 0.940 s | 0.755 s |
| Kāra (`karac build`) | 0.720 to 0.842 s | 0.762 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.874 to 1.180 s | 0.929 s |
| Rust (`rustc -O`) | 0.914 to 1.023 s | 0.955 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.886 to 1.077 s | 0.969 s |
| Go | 2.455 to 2.872 s | 2.637 s |
| Python | 32.3 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. C takes about half Kāra's time: it sizes each path to its depth
before filling it, where Kāra, Rust and Go grow a vector one push at a
time. Kāra takes about 0.8x Rust's time and Go about 3.5x Kāra's. Python
takes about 43x Kāra's time.
