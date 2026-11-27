# 1830. Minimum Number of Operations to Make String Sorted

You are given a string `s` (0-indexed). You are asked to perform the
following operation on `s` until you get a sorted string: find the
largest index `i` such that `1 <= i < s.length` and `s[i] < s[i - 1]`;
find the largest index `j` such that `i <= j < s.length` and `s[k] <
s[i - 1]` for all the possible values of `k` in the range `[i, j]`
inclusive; swap the two characters at indices `i - 1` and `j`; reverse
the suffix starting at index `i`. Return the number of operations needed
to make the string sorted. Since the answer can be too large, return it
modulo `10^9 + 7`.

```
s = "cba"                       ->  5
s = "aabaa"                     ->  2
s = "cdbea"                     ->  63
s = "leetcodeleetcodeleetcode"  ->  982157772
```

**Constraints:** `1 <= s.length <= 3000`, `s` consists only of lowercase
English letters.

The arms are `fn make_string_sorted(s: String) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `make_string_sorted.kara` ★ | each operation steps the string back to the order of its letters just before it, so the count is the string's rank among those orders. Walking from the right, a place adds the orders of its suffix that start with a smaller letter: `(m - 1)!` times the smaller letters of the suffix, over the factorials of its letter counts, with the factorials and their inverses mod 10^9 + 7 in tables. O(26 n) |
| `make_string_sorted_forward.kara` | the ★ arm's rank counted from the left: the letters not yet placed are counted, and each place adds, for every smaller letter still to come, the orders of the rest with that letter first; the product of the inverse factorials of the counts is kept as letters are placed, each placing multiplying it by the letter's count. O(26 n) |
| `make_string_sorted_fermat.kara` | the ★ arm's walk from the right with no table of inverses: each place's count is a fraction whose denominator, the product of the suffix's count factorials, is inverted by Fermat, raised to the power 10^9 + 5 by a recursive `power`. O(n (26 + log p)) |
| `make_string_sorted_running.kara` | the number of distinct orders of the suffix kept as one running value: a letter put in front of a suffix of `m - 1` letters multiplies it by `m` and divides it by the letter's new count, both inverses of numbers up to `n` read from a table made by `inv[i] = -(p / i) inv[p mod i]`; the orders starting below the letter are that value times the smaller letters, over `m`. O(26 n) |
| `make_string_sorted_solution.kara` | a Rust solution as LeetCode's Rust users write it (the ★ arm's tables, with `usize` counts and a free `pow_mod`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's four examples; five edges,
one letter, a string already sorted, one letter many times, the last
order of `a b c d`, `4! - 1` steps from the first, and `z` then `a`, one
step (`0 0 0 23 1`); the constraints' most, 3000 letters, the alphabet
backwards over and over, and random letters (`the most: 528293403
340180279`); and 3000 random strings of 1 to 12 letters from `a` to `e`
(`3000 random strings: checksum 400963452`). `make_string_sorted.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`.

The Mend loop: the ★, fermat and running arms and the harness check
clean as first written. Check warned that the forward arm's
`count[(b - b'a') as i64]` casts a `u8` that widens to an `i64` index
without one, and `karac fix` wrote `count[b - b'a']`, 1 fix. The Rust
solution takes 26 fixes by `karac fix`'s count, and its diff is: `fn
pow_mod(mut b: i64, mut e: i64)` to `fn pow_mod(b: i64, e: i64)` with
`let mut b = b; let mut e = e;` at its top; `struct Solution {}` added
above the `impl`; `vec![1i64; n + 1]` to `Vec.filled(n + 1, 1)`; `i as
i64` taken off twice, as `s.len()` is an `i64`; `s.as_bytes()` to
`s.bytes()`; `let mut ans = 0i64` to `let mut ans = 0`; `for &k in
cnt.iter()` to `for k in ..`; `Solution::` to `Solution.` at the
harness's 12 calls; and the harness's `as i64` on the result taken off.
`const MOD: i64 = 1_000_000_007`, `[0usize; 26]`, `(bytes[i] - b'a') as
usize`, `cnt[..c].iter().sum()`, `smaller as i64` and `ans as i32` are
Kāra as they stand. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the four steps of an operation done on the letters until they
are sorted, and the operations counted. It runs 2000 random strings of 1
to 7 letters, from `a` to `b` in a quarter of them and from `a` to `e`
in the rest. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | no operations exactly when the letters are already sorted |
| P3 | fewer operations than the letters have orders, `n!` over each count's factorial |
| P4 | every letter moved three on keeps the count |
| P5 | the letters in falling order are the last of their orders |
| P6 | the ★ arm's answer |

It checks clean as first written. All 60,000 checks pass on every arm:
`2000 cases: checksum 387019690, 60000 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, over the same cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a place's own letter counted among the smaller | P1 2000, P2 675, P3 1613, P5 2000, P6 8000 |
| M2 | ★: the suffix's factorial taken one place too long | P1 1325, P3 1086, P5 1582, P6 5300 |
| M3 | forward: a placed letter's count left in the denominator | P1 893, P3 723, P5 1013, P6 893 |
| M4 | forward: the letter itself counted as starting smaller | P1 2000, P2 675, P3 1613, P5 2000, P6 2000 |
| M5 | fermat: each count taken in place of its factorial | P1 434, P3 276, P5 562, P6 434 |
| M6 | fermat: the denominator raised one power short of its inverse | P1 1040, P3 695, P5 1246, P6 1040 |
| M7 | running: the suffix's orders not divided by the new count | P1 1040, P3 745, P5 1246, P6 1040 |
| M8 | running: the orders divided by m + 1 | P1 1325, P3 1266, P5 1582, P6 1325 |
| M9 | solution: each count's inverse factorial read at half the count | P1 1040, P3 745, P5 1246, P6 1040 |
| M10 | solution: the inverse factorials built a step off | P1 1325, P3 1325, P5 1582, P6 1325 |

## Benchmarks

The bench builds one string of 4500 random letters once and makes 500
calls of the ★ arm on runs of 1500 to 2999 of its letters, each run's
start and length drawn from the checksum so far. Each call makes its run
a string of its own. It checks clean as first written. The workload was
first written on a string of 3000 letters, where a run could end past
the last letter; the Kāra, Rust and Go builds stopped there with an
index out of bounds, while the C build read past the string and Python
cut the run short, and both printed a checksum. Every implementation
prints `500 calls: checksum 19228023`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.15 s against Rust's 0.14 s (0.15 s with overflow checks
on), C's 0.13 s and Go's 0.15 s; Python takes 2.2 s.
