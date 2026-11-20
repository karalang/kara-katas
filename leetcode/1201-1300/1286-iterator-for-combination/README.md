# 1286. Iterator for Combination

Design the `CombinationIterator` class:

- `CombinationIterator(characters, combinationLength)` takes a string of
  sorted distinct lowercase letters and a length.
- `next()` returns the next combination of that length, in lexicographic
  order.
- `hasNext()` returns whether there is a next combination.

```
iterator = CombinationIterator("abc", 2)
next() -> "ab", hasNext() -> true, next() -> "ac", hasNext() -> true,
next() -> "bc", hasNext() -> false
```

**Constraints:** `1 <= combinationLength <= characters.length <= 15`;
`characters` is sorted and its letters are distinct; at most `10^4`
calls; every call to `next` is valid.

Each arm is a `struct CombinationIterator` with `new(characters,
combination_length)`, `next(mut ref self) -> String` and `has_next(self)
-> bool`, and a `make` that builds one for the harness.

## Approaches

| file | mechanism |
|---|---|
| `combination_iterator.kara` ★ | by bit masks: bit n - 1 - i stands for letter i, so the masks with k bits, from the largest down, are the combinations in lexicographic order; `next` steps the mask down to the next one whose `count_ones` is k |
| `combination_iterator_listed.kara` | by listing them first: a backtracking search writes every combination into a `Vec[String]`, and the iterator walks an index along it |
| `combination_iterator_indices.kara` | by an index array: the combination is k increasing positions, and the next one raises the rightmost position with room and sets each later one to follow on, as Python's `itertools.combinations` does; a `done` flag answers `has_next` |
| `combination_iterator_successor.kara` | by successor on the text: the iterator holds the next combination as an `Option[String]`, and finds the one after it by `find`ing, from the right, the first letter that can move one place along `characters`, then copying the tail from a slice of `characters` |
| `combination_iterator_solution.kara` | a Rust solution as LeetCode's Rust users write it (every mask from the largest down whose `count_ones` is the length, each turned into its `String` by `filter(\|&i\| ..).map(..).collect()`, the list reversed so that `next` can `pop`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 17 lines: LeetCode's example (`ab true ac true
bc false`); then for n from 1 to 15, n random letters, every length from
1 to n run to the end with `has_next` asked again at random, as a caller
may: how many combinations came out (2^n - 1) and the last one (`15
letters: 32767 combinations, the last bcefgilmoqruvxz`); and a checksum
over every combination's bytes (`checksum 132271393`).
`combination_iterator.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, listed and indices arms checked clean as first
written. The successor arm stored its `characters` parameter in the
struct, and a bare parameter borrows: `E0200` said to take it as `own
String`, and `karac fix` did, in `new` and in `make`, which passes it on
(2 fixes). The solution arm takes one round of 10 fixes by `karac fix`'s
count: `Vec<..>` became `Vec[..]`, `::` paths took `.`, `&mut self`
became `mut ref self` and `&self` became `self`, the `&i` closure pattern
lost its `&`, and `!` became `not`. Its `combination_length as usize`
and `count_ones() as usize` stay, as explicit conversions Kāra accepts.
No gap was met.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every string of k of the letters, in lexicographic order, the
letters taken in turn like an odometer's digits, keeping those whose
letters strictly increase. 400 random problems of up to 8 letters, each
arm run to the end with `has_next` asked again at random; each property
is checked on every arm.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | as many combinations as n choose k |
| P3 | each combination is k of the letters, strictly increasing, and each comes after the one before |
| P4 | the combinations of length n - k, each replaced by the letters it leaves out, are this list backwards |
| P5 | the list for another set of n letters, renamed letter for letter by position: the same list |
| P6 | the ★ arm's list |

All 12,000 checks pass on every arm: `400 problems: checksum 414276944,
12000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the same
checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: letter i read from bit i, not bit n - 1 - i | P1 263, P3 263, P6 1052 |
| S2 | ★: `has_next` false once the mask is 1, not 0 | P1 135, P2 135, P4 144, P6 540 |
| L1 | listed: the search goes on from the letter just taken, not the one after | P1 258, P2 258, P3 258, P4 237, P6 258 |
| L2 | listed: `has_next` false one combination early | P1 400, P2 400, P4 273, P6 400 |
| I1 | indices: the positions after the raised one reset from two places on | P1 115, P2 115, P4 115, P6 115 |
| I2 | indices: each later position set one past the raised one, not one past its neighbour | P1 115, P2 115, P3 115, P4 198, P6 115 |
| U1 | successor: a letter's room to move counted one short | P1 274, P2 274, P4 274, P6 274 |
| U2 | successor: the search for a letter to move starts one from the right | P1 265, P2 265, P4 265, P6 265 |
| O1 | solution: the list not reversed before `pop` | P1 263, P3 263, P6 263 |
| O2 | solution: masks with k bits or more kept | P1 254, P2 254, P3 254, P4 254, P6 254 |

All ten are caught by P1, the statement read literally. O1 hands the
list out backwards, so it fails on every problem with two combinations
or more, 263 of 400; S1 fails on the same 263, since its first
combination is the last k letters, not the first k. Both keep the
count, so P2 misses them, and P3, which asks each combination to come
after the one before, sees them. S2 loses the last combination only
when it is the last letter alone, a mask of 1, so it fails on the
problems of length 1, and P4 on those of length n - 1 as well. L2 drops the last combination of every list.
P5, the same list for other letters, catches nothing: every edit works
on positions, and renaming the letters keeps them.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (the masks with k bits, from the largest down) over every length of
the 15 letters "abcdefghijklmno", 1000 rounds, every combination folded
into a checksum. Every program prints `1000 rounds of every length of 15
letters: checksum 41377550`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 2.789 to 3.023 s | 2.866 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 2.792 to 3.684 s | 2.916 s |
| Rust (`rustc -O`) | 3.044 to 3.315 s | 3.200 s |
| Rust (`rustc -O -C overflow-checks=on`) | 3.919 to 4.177 s | 4.014 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 3.716 to 4.091 s | 3.780 s |
| C (`clang -O3`) | 2.537 to 2.742 s | 2.593 s |
| C (`clang -O3 -march=x86-64-v3`) | 2.063 to 2.202 s | 2.137 s |
| Go | 5.379 to 6.218 s | 5.608 s |
| Python | 160.00 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 27% ahead of Rust with overflow checks on (2.916 s
against 4.014 s). C is about 11% ahead of Kāra (2.593 s against 2.916
s); Go takes about 1.9x Kāra's time. Python takes about 55x Kāra's time.
No profile was taken.
