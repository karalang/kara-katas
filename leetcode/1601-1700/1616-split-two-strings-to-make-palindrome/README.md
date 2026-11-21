# 1616. Split Two Strings to Make Palindrome

You are given two strings `a` and `b` of the same length. Choose an index
and split both strings **at the same index**, splitting `a` into two
strings: `a_prefix` and `a_suffix` where `a = a_prefix + a_suffix`, and
splitting `b` into two strings: `b_prefix` and `b_suffix` where
`b = b_prefix + b_suffix`. Check if `a_prefix + b_suffix` or
`b_prefix + a_suffix` forms a palindrome.

When you split a string `s` into `s_prefix` and `s_suffix`, either
`s_suffix` or `s_prefix` is allowed to be empty. For example, if
`s = "abc"`, then `"" + "abc"`, `"a" + "bc"`, `"ab" + "c"`, and
`"abc" + ""` are valid splits.

Return `true` *if it is possible to form a palindrome string, otherwise
return* `false`.

**Notice** that `x + y` denotes the concatenation of strings `x` and `y`.

```
a = "x",      b = "y"       ->  true
a = "xbdef",  b = "xecab"   ->  false
a = "ulacfd", b = "jizalu"  ->  true
```

**Constraints:** `1 <= a.length, b.length <= 10^5`;
`a.length == b.length`; `a` and `b` consist of lowercase English letters.

## Approaches

| file | mechanism |
|---|---|
| `split.kara` ★ | two pointers over `bytes()`: `a` from the front against `b` from the back as far as they agree, then whether the middle left over, of `a` or of `b`, is a palindrome by itself; then the roles swapped. O(n) |
| `split_center.kara` | from the centre out: the longest palindrome about the centre of `a` and of `b`, the longer one kept, then the outer letters of `a` against `b`'s and of `b` against `a`'s, compared from the outside in with `all` as far as that centre does not reach. O(n) |
| `split_every.kara` | every split tried: both joined strings built with an f-string of slices (`a[..i]`, `b[i..]`), each compared with itself reversed (`chars().eq(chars().rev())`). O(n^2) |
| `split_solution.kara` | LeetCode's Rust template (`as_bytes`, two closures with `&[u8]` and `usize` pointers, `\|\|`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and three
more (`"ab"` and `"cd"`, a palindrome `a` already, and a split that must
take `b`'s prefix), then the count that can split and a checksum for 3000
pairs of up to 6 letters from 2, 300 of up to 1000 letters from 3, and 30
of up to 20000 letters from 26. Half of each batch is made to split
(a prefix of `a`, mirrored at the end of `b`, around a middle of `b` that
is a palindrome), and one in four of those is then spoiled by a letter of
`a` changed at random. `split.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: for every split index, both joined strings built letter by
letter as `Vec[char]` and compared with their reverse. It checks 3000
pairs of 1 to 10 letters from 2 to 4, half of them built to split, every
random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | `a` and `b` swapped leave the answer |
| P3 | `a` and `b` each reversed, then swapped, leave the answer |
| P4 | every letter renamed (`a` to `b`, `b` to `c`, ..., the last to `a`) leaves the answer |
| P5 | when `a` or `b` is a palindrome already, the answer is `true` |
| P6 | each arm agrees with at least two of the other three |

P3 holds because `rev(b)[..i] + rev(a)[i..]` is the reverse of
`a[..n-i] + b[n-i..]`, and a string is a palindrome exactly when its
reverse is.

The differential prints `3000 problems, 2207 can split: checksum
606945058, 72000 checks over 4 arms: 0 failures` under every lane in
Verification. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, one to four to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M3 and M8 fail in the same places: each
drops one of the two joins, which only P2, swapping the strings, sees
directly.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a's front matched against b's front | P1 1028, P3 318, P6 1028 |
| M2 | ★: only a's middle tried | P1 237, P3 274, P6 237 |
| M3 | ★: only a's prefix with b's suffix tried | P1 90, P2 721, P6 90 |
| M4 | ★: the middle's last pair of letters not compared | P1 136, P6 136 |
| M5 | center: an even string's centre taken as one letter | P1 338, P3 165, P5 92, P6 338 |
| M6 | center: the shorter palindromic centre taken | P1 713, P5 386, P6 713 |
| M7 | center: the outermost letters not compared | P1 260, P6 260 |
| M8 | every: b's prefix joined to b's own suffix | P1 90, P2 721, P6 90 |
| M9 | template: b's middle checked one letter short | P1 356, P3 347, P6 356 |
| M10 | template: each letter compared with the one inside its mirror | P1 642, P3 369, P5 231, P6 642 |

## Benchmarks

The bench makes 10 pairs of 500000 letters from two that split, one
letter of b then changed one time in two, all of it first. Then: each
pair checked 30 times with two pointers. Every implementation prints `10
pairs of 500000 letters from 2, each checked 30 times: 240 split,
checksum 725862079`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `21cdf88b69` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.050 s |
| Rust (`rustc -O`) | 0.068 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.072 s |
| Kāra (`karac build`) | 0.077 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.083 s |
| Go | 0.115 s |
| Python | 5.1 s |

The sequential Kāra build takes 1.22x Rust's time and 1.15x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.050 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.071 s and 0.083 s on one
run).

## Verification

All four arms print the same output as `split.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`21cdf88b69`.

## Writing it

The harness, the same in every arm, first wrote
`b = f"{b.chars().take(k).collect::[String]()}{middle}{tail}"`.
`karac check` refused the turbofish, Rust's and not Kāra's, and `karac
fix` deleted it, which left a `collect()` nothing fixes in an f-string
hole. That was reported by the MIR builder as E0516 "an expression whose
type does not lower (UnsolvedParam("C")) is not lowered yet", where the
same `collect()` bound by a bare `let` gets the type checker's E0238
asking for an annotation. It now gets E0238 there too, and in a `println`
argument (B-2026-11-18-10), and since kara e05a5afee6 handed to a generic
parameter as well (B-2026-11-18-14). The harness binds
`let front: String = b.chars().take(k).collect()` first.

The three Kāra arms were written in Kāra and check as written.

The Rust template took one `karac fix` of 25 edits: `struct Solution;`
to `struct Solution {}`, `as_bytes()` to `bytes()`, the closures'
`&[u8]` to `Slice[u8]` and `usize` to `i64`, their `mut l` and `mut r`
parameters to `let mut` rebindings, `let (mut l, mut r)` to
`let mut (l, r)`, `&&` and `||` to `and` and `or`, `-> bool` taken off
the closures, and `Solution::` to `Solution.`. It then checks and agrees
with no hand edit.
