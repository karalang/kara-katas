# 2287. Rearrange Characters to Make Target String

You are given two **0-indexed** strings `s` and `target`. You can take
some letters from `s` and rearrange them to form new strings.

Return *the **maximum** number of copies of* `target` *that can be
formed by taking letters from* `s` *and rearranging them.*

```
s = "ilovecodingonleetcode", target = "code"   ->  2
s = "abcba", target = "abc"                     ->  1
s = "abbaccaddaeea", target = "aaaaa"           ->  1
```

**Constraints:** `1 <= s.length <= 100`; `1 <= target.length <= 10`;
`s` and `target` consist of lowercase English letters.

Count the letters of both strings. Each letter `target` needs allows
`have / need` copies, rounded down, and the answer is the least of
those. O(|s| + |target|).

## Approaches

| file | mechanism |
|---|---|
| `copies.kara` ★ | two `[0; 26]` counts over `bytes()`, indexed by `b - b'a'`, and the least quotient, starting from `s.len()` |
| `copies_naive.kara` | `target` spelled out of a `Vec[char]` of `s` again and again, each letter used struck with `position` and `remove`, until one cannot be found. O(copies * |target| * |s|) |
| `copies_map.kara` | a `Map[char, i64]` of what `target` needs, a second of those letters in `s`, and the least quotient over the first |
| `copies_struct.kara` | `struct Tally` of an `Array[i64, 26]` built by `of`; `copies_of` says how many times one tally holds another |
| `copies_iter.kara` | over the letters of `target`, `filter` and `count` in each string, the quotient by `map`, and `min` |
| `copies_solution.kara` | LeetCode's Rust template: `String` twice in, `i32` out; two `[0i32; 26]` over `bytes()`, then `(0..26).filter(..).map(..).min().unwrap()`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples, a target
longer than `s`, one letter alone, and `s` that is `code` ten times
over; then 3000 random cases of `s` of 1 to 100 letters and `target` of
1 to 10, both from the first 1 to 26 letters, with a checksum and the
copies in all. `copies.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one round, reporting 3 edits: the
closure pattern `|&i|` to `|i|`, `struct Solution;` to `struct
Solution {}`, and in the adapter the `as i64` on the template's `i32`
answer dropped, since an `i32` widens to the adapter's `i64` return.
The `[0i32; 26]` arrays and the `(c - b'a') as usize` indexes stay as
written.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the most copies `k` such that the letters of `target` written
`k` times, sorted, can be picked in order out of the letters of `s`,
sorted. No counts. It checks 300 random cases drawn as the arms'
harness draws them; then 30 where `s` is `target` 1 to 8 times over,
shuffled, with a letter added or dropped or not; then 30 where `target`
holds a letter `s` lacks, half of them a `z` added to the end of
`target`. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | `answer * |target| <= |s|` |
| P3 | `s` reversed: the same answer |
| P4 | `target` written twice: half the answer, rounded down |
| P5 | `target` appended to `s`: one copy more |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 701794151, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading by
`collections.Counter`. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the first letter of s never counted | P1 37, P3 22, P6 37 |
| M4 | ★: the bound from the target length | P1 78, P4 70, P5 92, P6 78 |
| M6 | ★: the letter 'z' never checked | P1 10, P6 10 |
| M9 | naive: each copy counted twice | P1 234, P2 60, P4 136, P5 360, P6 234 |
| M10 | naive: a copy counted before it is spelled | P1 234, P5 360, P6 234 |
| M11 | naive: the letter after the one found struck | P1 212, P3 150, P5 229, P6 212 |
| M12 | map: each letter needed once | P1 114, P2 44, P4 255, P5 68, P6 114 |
| M13 | map: a letter s lacks allows one copy | P1 86, P2 5, P4 37, P5 86, P6 86 |
| M16 | map: the copies one less | P1 360, P4 262, P6 360 |
| M18 | struct: the tallies swapped | P1 233, P2 1, P4 7, P5 360, P6 233 |
| M19 | struct: no letter needed: one copy | P1 166, P4 166, P5 234, P6 166 |
| M20 | struct: the letter 'a' never checked | P1 33, P2 5, P4 12, P5 12, P6 33 |
| M22 | iter: max for min | P1 283, P2 81, P6 283 |
| M24 | iter: the first letter of target alone | P1 161, P2 28, P6 161 |
| M26 | iter: the need one more | P1 219, P4 73, P5 183, P6 219 |
| M27 | solution: each letter of s counted twice | P1 252, P2 63, P5 360, P6 252 |
| M29 | solution: the letters shifted by one | P1 228, P5 340, P6 228 |

P1 and P6 kill all seventeen, P5 twelve, P4 nine, P2 eight and P3 two.
P5, one copy more once `target` is appended, catches every edit that
miscounts what a copy needs or what `s` holds. P4, `target` written
twice, catches the edits that lose the counts of what one copy needs.
P3, `s` reversed, fails only where an arm treats one end of `s`
differently: its first letter never counted, or the letter struck
after the one found.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Twelve fail as a kept one does: the need counted
once per letter in the ★ arm and not counted in the iter arm (M3, M23)
as the map arm's each letter needed once (M12); the ★ arm's largest
quotient and the struct and template arms' most for least (M5, M17,
M31) as the iter arm's max for min (M22); the naive arm's first letter
of `s` out of reach (M8) as the ★ arm's first letter never counted
(M2); the map arm's only the letters not needed counted (M14) as the
naive arm's copy counted before it is spelled (M10), both always 0; the
map arm's bound from the target length (M15) as the ★ arm's (M4).
Five fail together in two ways no kept edit does and are left out
because their arms keep enough: the quotient rounded up or one more
(M1, M21), and the copies from 1 or the target counted in with `s`
(M7, M25, M28). The template's quotient as a product (M30) fails in a
way of its own.

Five edits of the first draft were replaced. The ★ arm's letter `z`
never checked passed every check: no drawn case had `z` as the letter
that limits the answer, so half of the 30 cases where `s` lacks a
letter now lack a `z` added to `target`. The naive arm's letters struck
from the end and the map arm's every letter of `s` counted change
nothing, the struct arm's each letter counted twice doubles both
tallies alike, and the template's zeros of the need kept divides by
zero; they are now M11, M14, M20 and M27.

## Verification

Every arm prints the same output as `copies.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.7 to 1 s, except the
iterator arm, which counts each letter of `target` over both strings
again: 1.8 s. The differential takes 3 s.

## Benchmarks

The bench builds 10^4 pairs once, `s` of 1 to 100 letters and `target`
of 1 to 10, both from the first 1 to 6 letters so that most answers are
not 0, then makes 200 passes over all of them summing the answers, with
the ★ arm in all five languages. Every implementation prints `200
passes over 10^4 pairs: checksum 559235982`. C keeps the strings
NUL-terminated and counts `s`'s length as it walks it.

BENCHTAB
