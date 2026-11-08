# 1528. Shuffle String

You are given a string `s` and an integer array `indices` of the same
length. The string `s` will be shuffled such that the character at the
`i`th position moves to `indices[i]` in the shuffled string. Return the
shuffled string.

```
s = "codeleet", indices = [4,5,6,7,0,2,1,3]  ->  "leetcode"
s = "abc",      indices = [0,1,2]            ->  "abc"
```

**Constraints:** `s.length == indices.length == n`; `1 <= n <= 100`; `s`
holds only lowercase English letters; `0 <= indices[i] < n`, and the
values of `indices` are unique.

## Approaches

| file | mechanism |
|---|---|
| `shuffle.kara` ★ | each letter written where its index sends it, into a byte buffer of the string's length, then `String.from_utf8`. O(n) |
| `shuffle_gather.kara` | read rather than written: the indices inverted first, so each place of the answer knows its letter, and the answer built left to right by `push`. O(n) |
| `shuffle_cycles.kara` | in place, cycle by cycle: while place `i` holds a letter that belongs elsewhere it is swapped there, its index with it, so each swap settles one letter. O(n) swaps |
| `shuffle_iter.kara` | the letters paired with their indices by `zip`, the pairs sorted, and the letters collected back into a `String`. O(n log n) |
| `shuffle_solution.kara` | LeetCode's Rust template (`vec![0u8; n]`, `for (c, &i) in s.bytes().zip(..)`, `i as usize`, `String::from_utf8`), carried by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples, `aiohn`
shuffled to `nihao`, a single letter and a reversal, then checksums of
the answers for 3000 random strings of 1 to 8 letters over 3 and 3000 of
1 to 100 over 26, each with a shuffled `0..n`. `shuffle.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for each place of the answer, every position is asked whether
its letter moves there. It checks 3000 strings of 1 to 8 letters over 3,
every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer shuffled by the inverse indices is the string again |
| P3 | shuffling by `p` and then by `q` is shuffling once by `q` after `p` |
| P4 | the answer has the string's letters, as many of each |
| P5 | the letters renamed (a to b, b to c, c to a) rename the answer |
| P6 | each arm agrees with at least two of the other four |

The differential prints `3000 problems: checksum 841999891, 90000 checks
over 5 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Eight are killed, each the
same way under both backends; two survive, and both are equivalent.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each letter read from its index, not written to it | P1 1533, P3 1804, P6 1533 |
| M2 | ★: the first letter never written | P1, P2, P4, P5, P6 3000 each, P3 1963 |
| M3 | gather: the indices copied, not inverted | P1 1533, P3 1804, P6 1533 |
| M4 | gather: the letters read in their own order | P1 2070, P6 2070 |
| M5 | cycles: one swap at each place, not until it settles | P1 550, P2 704, P3 1056, P6 550 |
| M7 | iter: the pairs left unsorted | P1 2070, P6 2070 |
| M8 | iter: the indices zipped in reverse | P1 2222, P2 1789, P3 2222, P6 2222 |
| M9 | template: the indices zipped in reverse | P1 2222, P2 1789, P3 2222, P6 2222 |

The survivors: the cycle arm stopping before the last place (M6), since
once every other letter is settled the last one is too; and the
template's buffer filled with `a` rather than 0 (M10), since every place
is written. The mutations that apply the inverse permutation or none
(M1, M3, M4, M7) pass P2, P4 and P5, which hold for any permutation; P1
and P3 catch them.

## Benchmarks

The bench builds 100000 random strings of 1 to 100 letters with shuffled
indices once and answers each 30 times by the ★ arm, in all five
languages. Each answer borrows the string and the indices and returns a
fresh string (`malloc` and `free` in C). Every implementation prints
`30 passes over 100000 strings of up to 100 letters: checksum 223123063`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `a90821c8d` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.165 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.293 s |
| Rust (`rustc -O`) | 0.304 s |
| Kāra (`karac build`) | 0.375 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.383 s |
| Go | 0.411 s |
| Python | 6.24 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.33 s and 0.37 s on one run).

Kāra is 1.31x Rust under overflow checks by median. Not traced. Each
answer allocates the buffer and checks it as UTF-8 in both languages;
Kāra also builds the bench's 100000 strings by `push`, which is part of
the time, so the gap may not be in the answer itself.

## Verification

All five arms print the same output as `shuffle.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change.

## Writing it

The ★, gather and iterator arms were written in Kāra and checked as
written. The cycle arm first took the bytes as `let mut b = s.bytes();`
and swapped them in place, as Rust does with `into_bytes()`. `bytes()` is
a read-only view, so `b.swap(i, j)` is refused, but the error says only
`Slice.swap() requires a mutable slice` and carries no fix, while an
index assignment through the same binding names `.to_vec()` (and is
reported twice). Filed as B-2026-11-08-64; the arm now writes
`s.bytes().to_vec()`, the copy the assignment message advises.

The differential's letter renaming wrote `(c as u8) + 1`, refused by
design (`char` to `u8` would truncate a non-ASCII scalar) with a help but
no machine edit, since the two remedies it names differ; it now writes
`c as u32 as u8 + 1`. The bench's `as i64` on a byte was dropped by
`karac fix`.

The Rust template took 4 edits and then 2 over two rounds: `Vec<i32>` to
`Vec[i32]`, `vec![0u8; n]` to `Vec.filled(n, 0u8)`, the `&i` pattern
dropped with `.iter()` added after `bytes()`, and `String::from_utf8` to
`String.from_utf8`. Its `i as usize` stays as written. It checks and
agrees with no hand edit.
