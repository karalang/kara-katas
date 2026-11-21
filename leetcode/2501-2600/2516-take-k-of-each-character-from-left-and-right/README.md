# 2516. Take K of Each Character From Left and Right

You are given a string `s` consisting of the characters `'a'`, `'b'`,
and `'c'` and a non-negative integer `k`. Each minute, you may take
either the **leftmost** character of `s`, or the **rightmost** character
of `s`.

Return *the **minimum** number of minutes needed for you to take **at
least*** `k` *of each character, or return* `-1` *if it is not possible
to take* `k` *of each character.*

```
s = "aabaaaacaabc", k = 2  ->  8
s = "a", k = 1             ->  -1
```

**Constraints:** `1 <= s.length <= 10^5`; `s` consists of only the
letters `'a'`, `'b'`, and `'c'`; `0 <= k <= s.length`.

What is taken is a prefix and a suffix, so what is left is one window in
the middle, and the window may hold all but `k` of each letter. The
fewest minutes are `n` less the longest such window, and `-1` when the
whole string holds fewer than `k` of some letter. The approaches differ
in how they find the split.

## Approaches

| file | mechanism |
|---|---|
| `take.kara` ★ | the longest window that leaves `k` of each letter outside it, found by sliding: its right end grows a letter at a time and its left end moves in while the newest letter is overdrawn. O(n) |
| `take_search.kara` | prefix counts, and for each length taken from the left the shortest part from the right bisected over the suffix counts, which only grow with its length. O(n log n) |
| `take_shrink.kara` | two pointers from the left: the whole string taken from the left, then given back a letter at a time from the left part's end, letters taken from the right end each time one given back would leave fewer than `k`. O(n) |
| `take_rec.kara` | recursion: a bisection over the number of minutes, recursing into the half that holds the least that works; a number works when one sweep of the split point between prefix and suffix finds `k` of each. O(n log n), about 17 deep |
| `take_iter.kara` | iterators: the letters' totals a `fold` over the bytes, and the longest window a `fold` over the right ends carrying the left end, the counts inside and the longest so far |
| `take_solution.kara` | LeetCode's Rust template: `String` and `i32` in, `i32` out; the window slid over `s.as_bytes()` with `usize` ends and `[i32; 3]` counts taken out as the window grows; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 15 lines: LeetCode's two examples and six
more; then 2000 random strings of 1 to 20 letters with `k` from 0 to 4,
and 2000 of 1 to 2000 letters with `k` up to a third of the length,
each as the misses, the sum of the other answers and a checksum; then
the constraints' largest, `10^5` letters: a random string with `k`
33000 and with `k` 0; `10^5` a's with `k` 1; and `abc` 33333 times with
`k` 33333 and 33332. `take.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 3000 random strings of 1
to 14 letters with `k` from 0 to 5 against a search of every prefix and
suffix, and the two agreed on every string.

`check` first reports 3 errors on the template: `struct Solution;` and
the `&` before the patterns of `for &c in b` and `|&x|`. `karac fix`
carries it in one call, reporting 13 edits: `struct Solution {}`;
`s.as_bytes()` becomes `s.bytes()`; the two `&`s dropped; the
`0usize` suffixes dropped, the ends being `i64`; the `as usize` casts of
the two indexes dropped, a `u8` already indexing, and the third, on
`let c`, written `as i64`; and the wrapper's `s.clone()` and lossless
`as i64` dropped. The `[0i32; 3]` counts and the `(n - best) as i32`
stand as written.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each number of minutes from 0 up, every split of them
between the left end and the right end, the letters taken counted by a
scan of both parts; the answer is the first number with a split that
holds `k` of each. No window is slid. It checks 300 random strings of 1
to 10 letters with `k` from 0 to 3; then 20 of 12 letters from `a` and
`b` only, `k` 1; and 40 of 12 letters, `k` 2. All 360 are drawn before
any arm answers, and 185 of them hold too few of some letter.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | `-1` exactly when some letter is there fewer than `k` times, and otherwise from `3 k` to `n` |
| P3 | the string reversed: the same answer |
| P4 | every `a` written `b`, `b` written `c`, and `c` written `a`: the same answer |
| P5 | for `k - 1`, while `k` is at least 1 and there is an answer: from 0 to the answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases, 185 with too few: checksum
487420460, 12960 checks over 6 arms: 0 failures` under every lane in
Verification; the checksum of the literal answers was checked against a
Python reading that builds the same cases and tries every prefix and
suffix. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: the answer one more | P1 175, P2 9, P6 175 |
| M4 | ★: the last window, not the longest | P1 52, P3 63, P6 52 |
| M6 | ★: every c counted as an a | P1 157, P2 89, P4 72, P6 157 |
| M7 | search: the bisection one past | P1 34, P2 26, P3 29, P6 34 |
| M9 | search: the suffix one longer | P1 109, P2 87, P3 19, P6 109 |
| M10 | search: each prefix one letter only | P1 154, P2 89, P3 47, P6 154 |
| M13 | shrink: the first letter never given back | P1 93, P3 19, P6 93 |
| M14 | shrink: the right part one more | P1 166, P6 166 |
| M16 | shrink: one letter taken back at most | P1 75, P2 73, P3 18, P6 75 |
| M17 | rec: the sweep one split short | P1 12, P3 19, P6 12 |
| M19 | rec: the suffix one short | P1 81, P2 20, P3 54, P6 81 |
| M21 | rec: the bound n - 1 | P1 9, P2 9, P6 9 |
| M22 | iter: the totals begun at 1 | P1 195, P2 195, P6 195 |
| M24 | iter: the newest letter not counted | P1 89, P2 89, P6 89 |
| M26 | iter: too few as n | P1 185, P2 185, P6 185 |
| M29 | solution: a letter put back twice | P1 46, P2 43, P3 32, P6 46 |
| M30 | solution: the answer one less | P1 175, P2 149, P5 40, P6 175 |

P1 and P6 kill all seventeen, P2 thirteen, P3 nine, P5 one, the
template's answer one less, and P4 one, the ★ arm's every `c` counted
as an `a`.

One of the first thirty-one edits survived and was replaced: the search
arm's `i` short of `n` never tries the whole string from the left, but
the split with all `n` letters from the right is the same count, so it
is equivalent. It became the bisection's top one short (M8).

Fourteen are not kept, and none survives. Ten fail exactly as a kept
one: the ★, iter and template arms' window one short (M1, M23, M27) as
the shrink arm's right part one more (M14), each one more minute
whenever any letter can be left; the ★ arm's one overdrawn letter
allowed and the shrink arm's nothing given back (M2, M15) as the iter
arm's newest letter not counted (M24), each wrong on just the 89
strings with enough letters and an answer above 0; the rec arm's
bisection one more (M20) as the ★ arm's answer one more (M3); the
search arm's bisection's top one short, the shrink arm's best from `n -
1` and the iter arm's longest at least 1 (M8, M12, M25) as the rec
arm's bound `n - 1` (M21), each wrong only when every letter must be
taken; and the rec arm's all-right split skipped (M18) as the shrink
arm's first letter never given back (M13), each blind to a take from
the right end alone. The ★ and template arms' too few as 0 (M5, M28)
fail as each other. Two fail in ways of their own, but their arms
already hold their kept edits: the search arm's first fitting `i` kept
(M11) and the template's first letter left out of the window (M31).

## Verification

Every arm prints the same output as `take.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 8.7 to 142.6 s, the search arm's bisections the slowest, and the differential 0.7 s; under `karac __mir-llvm-asan` the arms take 1.1 to 27.1 s and the differential 0.7 s; and under `karac run` the differential takes 0.6 s.

## Benchmarks

The bench builds 40 random strings of `10^5` letters once from its own
generator, then makes 7 passes. Each pass asks every string with `k` the
checksum so far modulo 30001, folding each answer plus 1 and the pass
into the checksum. The bench uses the ★ arm in all five languages.
Every implementation prints `7 passes over 40 strings of 10^5: checksum
731170754`.

BENCHTAB
