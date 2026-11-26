# 1790. Check if One String Swap Can Make Strings Equal

You are given two strings `s1` and `s2` of equal length. A string swap
is an operation where you choose two indices in a string, not
necessarily different, and swap the characters at them. Return `true` if
it is possible to make both strings equal by performing at most one
string swap on exactly one of the strings. Otherwise, return `false`.

```
s1 = "bank",   s2 = "kanb"    ->  true
s1 = "attack", s2 = "defend"  ->  false
s1 = "kelb",   s2 = "kelb"    ->  true
s1 = "abcd",   s2 = "dcba"    ->  false
```

**Constraints:** `1 <= s1.length, s2.length <= 100`, `s1.length ==
s2.length`, and both consist of lowercase English letters.

The arms are `fn are_almost_equal(s1: String, s2: String) -> bool`.

## Approaches

| file | mechanism |
|---|---|
| `are_almost_equal.kara` ★ | the positions where the strings differ, gathered over `bytes()` and given up past two: none, and they are equal already; exactly two, `i` and `j`, and one swap mends them when `s1[i] == s2[j]` and `s1[j] == s2[i]`. O(n) |
| `are_almost_equal_counts.kara` | each letter counted up in `s1` and down in `s2` over the zipped `chars()`, with the positions that differ: the strings must hold the same letters, and then 0 or 2 differences, since two differences with the same letters on both sides always cross. O(n) |
| `are_almost_equal_brute.kara` | every swap of two positions in `s1` tried on a `Vec[char]` and undone, the strings compared after each. O(n^3) |
| `are_almost_equal_zip.kara` | the pairs of letters that differ, gathered by zipping the strings into a `Vec[(char, char)]` and filtering: none, or two that are each other's reverse. O(n) |
| `are_almost_equal_solution.kara` | a Rust solution as LeetCode's Rust users write it (`s1.as_bytes()`, `(0..a.len()).filter(\|&i\| a[i] != b[i]).collect()` into a `Vec<usize>`, `&&`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's four examples (`true false
true false`); five edges, one letter alike and not, a swap of two
letters alike, two differences one swap cannot mend, and three
differences a cycle of three would (`true false true false false`); the
constraints' most, 100 letters against themselves, one swap apart at the
ends, and two swaps apart (`the most: true true false`); and 3000 random
pairs of 1 to 12 letters from the first 1 to 4, a word against itself
after 0 to 2 random swaps or against another word (`3000 random cases:
checksum 986900565`). `are_almost_equal.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, counts, brute and zip arms and the harness check
clean as first written. The Rust solution takes one round of 9 fixes by
`karac fix`'s count, and its diff is: `struct Solution;` to `struct
Solution {}`, `as_bytes()` to `bytes()`, `Vec<usize>` to `Vec[i64]`,
`|&i|` to `|i|`, `&&` to `and`, and `Solution::` to `Solution.`. Every
arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: no swap, or one swap of any two positions in `s1` or in `s2`,
after which the strings are equal, while there are at most 10 letters.
LeetCode's examples, the edges and `"zz"` against `"zy"`, the three of
100 letters, and 1987 random pairs, nine in ten of 1 to 10 letters from
the first 1 to 4 and the rest of up to 30 from all 26, drawn as the
harness draws them. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally, while there are at most 10 letters |
| P2 | the strings the other way round give the same answer |
| P3 | one letter more, the same, on the end of both gives the same answer |
| P4 | both strings reversed give the same answer |
| P5 | each letter moved one on in the alphabet in both, `z` to `a`, gives the same answer |
| P6 | the ★ arm's answer |

The differential checks clean as first written. All 59,295 checks pass
on every arm: `2000 cases: checksum 97303519, 59295 checks over 5 arms:
0 failures`, under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. Python, running the ★ arm's mirror over the same
cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: only one of the two crossings checked | P1 2, P2 7, P4 7, P6 8 |
| M2 | ★: equal strings refused | P1 1186, P6 4776 |
| M3 | counts: the letters never compared | P1 38, P6 38 |
| M4 | counts: the second string's letters counted up, not down | P1 1505, P6 1577 |
| M5 | brute: no swap of two neighbours tried | P1 137, P6 143 |
| M6 | brute: a swap tried never undone | P1 213, P2 97, P3 38, P4 100, P6 277 |
| M7 | zip: only the pairs whose first letter is smaller kept | P1 373, P2 110, P5 1, P6 437 |
| M8 | zip: the two pairs required alike, not each other's reverse | P1 335, P6 399 |
| M9 | solution: the positions that agree gathered | P1 1486, P3 271, P6 1583 |
| M10 | solution: any other count of differences accepted | P1 316, P6 385 |

## Benchmarks

The bench builds 2000 pairs of 100 random letters once, the second
string 0, 1 or 2 random swaps from the first or with 3 letters changed,
and makes 4000000 calls of the ★ arm, each pair drawn from the checksum
so far. Check gave one warning, a redundant `as u8` on a byte already
`u8`, and `karac fix` dropped it, 1 fix. Every implementation prints
`4000000 calls over 2000 pairs: checksum 248486302`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.46 s against Rust's 0.47 s (0.46 s with
overflow checks on), C's 0.31 s and Go's 0.42 s; Python takes 8.9 s.
