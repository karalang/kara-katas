# 2156. Find Substring With Given Hash Value

The hash of a **0-indexed** string `s` of length `k`, given integers `p`
and `m`, is computed using the following function:

- `hash(s, p, m) = (val(s[0]) * p^0 + val(s[1]) * p^1 + ... + val(s[k-1]) * p^(k-1)) mod m`.

Where `val(s[i])` represents the index of `s[i]` in the alphabet from
`val('a') = 1` to `val('z') = 26`.

You are given a string `s` and the integers `power`, `modulo`, `k`, and
`hashValue`. Return `sub`, *the **first substring** of* `s` *of length*
`k` *such that* `hash(sub, power, modulo) == hashValue`.

The test cases will be generated such that an answer always **exists**.

A **substring** is a contiguous non-empty sequence of characters within a
string.

```
s = "leetcode", power = 7, modulo = 20, k = 2, hashValue = 0     ->  "ee"
s = "fbxzaad", power = 31, modulo = 100, k = 3, hashValue = 32   ->  "fbx"
```

**Constraints:** `1 <= k <= s.length <= 2 * 10^4`; `1 <= power, modulo
<= 10^9`; `0 <= hashValue < modulo`; `s` consists of lowercase English
letters only; the test cases are generated such that an answer always
exists.

The first letter weighs least, so a window's hash is the next window's
times `power`, with its own first letter added and the letter that falls
off its end taken away at `power^k`. Rolled from the left, the same step
would divide by `power`, which `modulo` need not allow; rolled from the
right, it only multiplies. The last match met on the way left is the
first window. O(n).

## Approaches

| file | mechanism |
|---|---|
| `substring.kara` ★ | one walk from the right: the hash times the power, the new letter added, the fallen letter taken away at `top`, the power's k-th power; the last match met kept |
| `substring_suffix.kara` | every suffix's hash by Horner's rule from the right into a `Vec`, the powers up to k in a table; a window's hash is its suffix's less the next suffix's at `powers[k]`, and the first window by `find` over the starts |
| `substring_struct.kara` | a `struct Window` made `of` the power, modulo and k, that `take`s a letter at the front and `drop`s one at the back (`mut ref self`) and says whether it `matches` (`ref self`) |
| `substring_iter.kara` | `scan` over the starts from the right hands on each start with its window's hash, `filter` keeps the matches, and the first window is their `last`; the k-th power by `fold` |
| `substring_fold.kara` | one `fold` over the starts from the right carrying the hash and the first window seen as a tuple; the k-th power by squaring, in a recursion that halves the exponent |
| `substring_solution.kara` | LeetCode's Rust template: `s.as_bytes()`, `k as usize`, the hash rolled in `i64` with `(bytes[i] - b'a' + 1) as i64`; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples and five
more (the whole string, one letter, a power of 1 so that the hash is the
sum, a modulo of 1 so that every hash is 0 and the first window is the
answer, and two windows of the hash, the first of them taken), each with
its answer; then a checksum over 2000 random strings of 1 to 12 letters
from the first 3, 4 or 26 in turn, with power and modulo up to 10, 1000
or 10^9 in turn and the hash that of a window drawn at random; then the
constraints' largest, 20000 letters with power and modulo near 10^9,
for windows of 1, 100, 10000 and 20000 letters. `substring.py` mirrors
the ★ arm and its output is byte-identical.

No compiler gap was met. `karac fix` carries the template in three
rounds of 4, 3 and 3 edits: Rust's spellings (`&&` to `and`, `struct
Solution;` to `struct Solution {}`, the adapter's `&String` to `ref
String`, `Solution::` to `.`); then `as_bytes()` to `bytes()`, `k as
usize` to `k as i64`, and `hash_value as i64` dropped, since an `i32`
widens where it meets an `i64`; then the two `as i64`s on the letters
dropped, since a `u8` widens too, and the `ref` dropped from the
adapter's parameter, which borrows already. The bench was first written
with Rust's `as_bytes()` and its `as i64`s, and `karac fix` made the
same changes there.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the windows tried from the first, each one's hash summed term
by term with every power of the power multiplied out afresh, and the
first that matches taken; nothing rolled. It checks 300 random strings
of 1 to 10 letters from the first 2, 3 or 26 in turn, with power and
modulo up to 10, 1000 or 10^6 in turn and the hash that of a window
drawn at random; then 30 with a modulo of 1 to 3, so that many windows
match; then 30 asking for the hash of the last window. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the window is the statement read literally |
| P2 | a letter put at the end: the same window |
| P3 | the string written twice: the same window |
| P4 | the window has k letters and, by the statement, the hash asked |
| P5 | a letter put in front: the same window, or the new first window when that one has the hash |
| P6 | each arm agrees with at least three of the other five |

P2 and P3 hold since a letter or a copy at the end only adds windows
after the first match. P5 puts a `z` in front, which moves every window
on by one place and adds one window before them all.

The differential prints `360 strings: checksum 934686277, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
strings by the same summing. On a failure it prints the first ten and
then the count by property.

## Mutation testing

Thirty-two edits to the differential, four to seven to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Fourteen are
kept: three to the ★, struct and fold arms, two to the iterator arm and
the Rust template, and one to the suffix arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the power's k-th power one short | P1 100, P2 228, P3 11, P4 99, P5 17, P6 100 |
| M3 | ★: a fallen letter's hash left negative | P1 43, P2 100, P3 4, P4 42, P5 11, P6 43 |
| M4 | ★: the last letter never falling off | P1 118, P2 250, P3 19, P4 110, P5 37, P6 118 |
| M25 | suffix: a window matching when its hash is at least the hash asked | P1 82, P4 82, P5 214, P6 82 |
| M9 | struct: a letter taken weighed by the power | P1 113, P2 249, P3 13, P4 109, P5 25, P6 113 |
| M10 | struct: a letter dropped with no weight | P1 111, P2 232, P3 10, P4 107, P5 25, P6 111 |
| M12 | struct: the power's k-th power one over | P1 95, P2 227, P3 17, P4 94, P5 14, P6 95 |
| M13 | iter: the first match met from the right | P1 45, P2 52, P5 63, P6 45 |
| M29 | iter: a window matching when its hash is at most the hash asked | P1 104, P4 104, P5 82, P6 104 |
| M18 | fold: the power's zeroth power 0 | P1 116, P2 258, P3 29, P4 108, P5 34, P6 116 |
| M19 | fold: a match carrying the hash from before the letter fell off | P1 19, P2 16, P3 33, P4 11, P5 16, P6 19 |
| M31 | fold: the half squared into the base | P1 74, P2 177, P3 11, P4 73, P5 14, P6 74 |
| M21 | solution: the letters counted from 0 | P1 131, P2 266, P3 34, P4 122, P5 44, P6 131 |
| M22 | solution: the adapter's power and modulo swapped | P1 99, P2 196, P3 8, P4 80, P5 54, P6 99 |

P1, P5 and P6 kill all fourteen, P4 thirteen, P2 twelve and P3 eleven.
Most wrong edits get the hash wrong, which every property sees; the
properties are there for the two kinds of edit that keep it right. P4
asks only that the window have the hash, so it misses M13, which
returns a window that has it but the last such window rather than the
first; P2 sees M13, since the letter added at the end can make a new
last match. P2 and P3 miss the edits that take a window whose hash is
at least, or at most, the hash asked (M25, M29), since a letter or a
copy at the end leaves the first such window where it was; P4 sees
them. M19 is the one edit P3 sees more often than P1: it goes wrong only
after a match met where a letter has already fallen off the window, and
the doubled string has more of those.

Of the thirty-two, eighteen were not kept. Eight crash: the suffix and
iterator arms take the first match with `unwrap`, as the statement
promises one, so an edit that gets every hash wrong leaves no match and
panics there: the suffix arm's table one power short (M5), the power on
the letter rather than the suffix (M6), the next suffix not taken away
(M8) and the suffixes summed from the left (M28); and the iterator
arm's power one short (M14), its letters counted from 0 (M15), a
fallen letter's hash left negative (M16) and each start handed the hash
of the window after it (M27). One is equivalent: the struct arm's last
window never asked (M11), since the start begins there. Eight fail as a
kept one does: the ★ arm stopping at the match furthest right and the
suffix arm finding the last match, as M13; the template's fallen letter
left negative, as M3, and its power one short, as M1; the fold arm's
last two letters never falling off, as M4, and its odd power not
multiplied, as M10; and the iterator arm's at-least and the suffix
arm's at-most, as M25 and M29. One fails in a way of its own but was
left out to keep three to the fold arm: a fallen letter added back
(M32).

## Verification

Every arm prints the same output as `substring.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.5 s to 0.9 s and the
differential 0.6 s.

## Benchmarks

The bench builds 4 strings of 20000 random letters once; then solves
every string 50 times, one letter at a random place changed before each
solve so that no solve repeats one before, with a window of 1 to 20000
letters, power and modulo near 10^9, and the hash of a window drawn at
random, which each language sums term by term as the statement writes
it; the ★ arm in all five languages. Every implementation prints `200
solves: 1898825 letters in all, checksum 212895848`.

BENCHTAB
