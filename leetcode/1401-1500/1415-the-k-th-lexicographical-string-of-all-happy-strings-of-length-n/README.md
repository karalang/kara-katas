# 1415. The k-th Lexicographical String of All Happy Strings of Length n

A happy string is a string that consists only of letters of the set
`['a', 'b', 'c']` and has `s[i] != s[i + 1]` for all values of `i` from
`1` to `s.length - 1` (the string is 1-indexed). For example, strings
`"abc"`, `"ac"`, `"b"` and `"abcbabcbcb"` are all happy strings and
strings `"aa"`, `"baa"` and `"ababbc"` are not happy strings. Given two
integers `n` and `k`, consider a list of all happy strings of length `n`
sorted in lexicographical order. Return the kth string of this list or
return an empty string if there are less than `k` happy strings of
length `n`.

```
n = 1, k = 3  ->  "c"
n = 1, k = 4  ->  ""
n = 3, k = 9  ->  "cab"
```

**Constraints:** `1 <= n <= 10`, `1 <= k <= 100`.

Each arm is `fn get_happy_string(n: i32, k: i32) -> String`. The harness
prints an empty answer as `-`.

## Approaches

| file | mechanism |
|---|---|
| `get_happy_string.kara` ★ | there are 3 * 2^(n - 1) happy strings: the first letter is the (k - 1) / 2^(n - 1)-th of `abc`, and each letter after it the lower or the higher of the two that differ from the one before, by the bits of what is left of k - 1, highest first. O(n) |
| `get_happy_string_backtrack.kara` | the happy strings built letter by letter by a recursion, `a` before `b` before `c`, a letter added only where the string does not `ends_with` it, and the k-th one finished kept. O(min(k, 3 * 2^(n - 1)) n) |
| `get_happy_string_levels.kara` | the happy strings of each length from those one shorter, each extended in order with `f"{s}{c}"`, so every level stays sorted, and the k-th of the last. O(3 * 2^n n) |
| `get_happy_string_count.kara` | every string of n letters from `abc`, in order, as a number counted up in base 3, the happy ones counted until the k-th, its digits mapped back to letters. O(3^n n) |
| `get_happy_string_solution.kara` | a Rust solution as LeetCode's Rust users write it (a block of `1 << (n - 1 - i)` strings per letter, the choices for each `['a', 'b', 'c'].iter().filter(\|&&c\| c != prev).cloned().collect()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and four
more (`c - cab - a cb cbcb`); the constraints' most, and every k for n =
3 (`n = 10: abacbabacb ababababab | n = 3: aba abc aca acb bab bac bca
bcb cab cac cba cbc -`); and 2000 random cases of n from 1 to 10 and k
from 1 to 100 (`2000 random cases: 846 empty, checksum 461317632`).
`get_happy_string.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the harness's `shown` hands back its bare `String`
parameter, which a bare parameter cannot give (core-semantics.md §4.1),
and `karac fix` writes `s: own String`, 1 fix in every arm. The ★ arm's
`let per_first = 1 << (n - 1)` kept the literal's default beside the
shift and was refused against `k`; `karac fix` declares `per_first: i32`
and then drops the `as i64` on the index, which the declaration made
redundant, 3 fixes in all. The backtrack arm takes 4: `s.ends_with(c)`
with `c` a `char` to `c.to_string()`, since a `Str` search takes a `Str`
pattern, and two `as i64` casts the widening makes unneeded. The levels
and count arms take 2 each, the harness's and an unneeded cast. The Rust
solution takes one round of 13 fixes by `karac fix`'s count: `struct
Solution;` to `struct Solution {}`, `String::new` to `String.new`,
`Vec<char>` to `Vec[char]`, the closure's `&&c` to `c`, `let block = 1
<< ..` declared `i32`, the harness's `own`, and `Solution::` to
`Solution.`. Its `(k / block) as usize` is taken as written. Every arm's
output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally, for every n at once: every string of n letters from `a`, `b`
and `c`, built from those one shorter and sorted with `sort`, and the
happy ones kept in order. Every n from 1 to 10 with every k from 1 to
100, and 1003 random pairs.

The differential first bound `let list = happy[n];`, moving a
`Vec[String]` out of an index; check refuses it, and `karac fix` writes
`ref happy[n]`, since the binding is only read, 1 fix.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | n letters, or none exactly when k is past the 3 * 2^(n - 1) happy strings |
| P3 | only `a`, `b` and `c`, and no letter beside itself |
| P4 | the next k gives a later string, while there is one |
| P5 | every shorter happy string has two happy extensions, in order, so the k-th of n letters starts with the (k + 1) / 2-th of n - 1 |
| P6 | the ★ arm's answer |

All 51,850 checks pass on every arm: `2003 cases: checksum 316581668,
51850 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by
`itertools.product` over `abc`, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the lower and the higher of the two letters that may follow swapped | P1 1183, P4 1150, P6 4732 |
| M2 | ★: the strings that start with `c` refused as past the last | P1 135, P2 135, P6 540 |
| M3 | backtrack: two strings counted for each one found | P1 1297, P2 722, P5 360, P6 1297 |
| M4 | backtrack: a letter allowed to follow itself | P1 1465, P2 282, P3 1338, P5 1416, P6 1465 |
| M5 | levels: the strings grown in the order a, c, b | P1 1144, P4 377, P6 1144 |
| M6 | levels: the string taken at (k - 1) modulo 3 | P1 1133, P4 374, P5 582, P6 1133 |
| M7 | count: the second letter never compared with the first | P1 1286, P2 103, P3 755, P5 12, P6 1286 |
| M8 | count: the string after the k-th taken | P1 1190, P2 15, P5 609, P6 1190 |
| M9 | solution: the letter before always taken as the first choice | P1 1171, P4 1175, P6 1171 |
| M10 | solution: k equal to the count of happy strings taken as too large | P1 15, P2 15, P5 10, P6 15 |

## Benchmarks

The bench runs the ★ arm on 10^6 cases of n from 1 to 10 and k from 1 to
100, each drawn. Every implementation prints `10^6 cases: checksum
254721341`.

BENCHTAB

Kāra takes about one and a half times Rust's time here, measured by hand
at 0.17 to 0.19 s against Rust's 0.12 s, with overflow checks on or off,
C's 0.09 s and Go's 0.09 s.
