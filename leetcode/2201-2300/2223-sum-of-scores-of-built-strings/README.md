# 2223. Sum of Scores of Built Strings

You are **building** a string `s` of length `n` **one** character at a
time, **prepending** each new character to the **front** of the string.
The strings are labeled from `1` to `n`, where the string with length
`i` is labeled `s_i`.

- For example, for `s = "abaca"`, `s_1 == "a"`, `s_2 == "ca"`,
  `s_3 == "aca"`, etc.

The **score** of `s_i` is the length of the **longest common prefix**
between `s_i` and `s_n` (Note that `s == s_n`).

Given the final string `s`, return *the **sum** of the **score** of
every* `s_i`.

```
s = "babab"      ->  9
s = "azbazbzaz"  ->  14
```

**Constraints:** `1 <= s.length <= 10^5`; `s` consists of lowercase
English letters.

`s_i` is the suffix of `s` starting at `n - i`, so its score is the
Z-function at that index, with `z[0] = n`. The Z-algorithm keeps the
box `[l, r)` of the rightmost match found, starts each `z[i]` inside it
from `z[i - l]`, capped at the box's edge, and extends past `r` by
comparing letters. O(n). The sum reaches n(n + 1)/2, past `i32` at
10^5 letters.

## Approaches

| file | mechanism |
|---|---|
| `scores.kara` ★ | the Z-algorithm over a `Vec[char]`, the box `[l, r)` in two variables, then `sum` |
| `scores_borders.kara` | counted from the other end: each end p closes as many prefixes of s as `s[..=p]` has borders, itself included; the KMP prefix function gives the longest border, and the count follows the chain, `count[p] = count[pi[p] - 1] + 1` |
| `scores_hash.kara` | each score by binary search on its length, a prefix of the suffix matching when two polynomial hashes under two moduli agree, read off prefix-hash tables held in a `struct Hasher`; O(n log n) |
| `scores_struct.kara` | a `struct ZBox` of the letters, the z values and the box, with `reach` (`ref self`) matching letters from a start and `score` (`mut ref self`) working out the next z and moving the box |
| `scores_iter.kara` | the Z-function by `map` over the indices, the closure keeping the box; each z extended past what the box knows by `zip`ping the prefix with the suffix, `take_while` the letters agree, and `count`; then `sum` |
| `scores_solution.kara` | LeetCode's Rust template: a `String` in, `i64` out, the Z-algorithm over `s.as_bytes()` with a `vec![0usize; n]` and the box a tuple of `usize`s; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one letter, one letter throughout, all different, and a repeated pair),
each with its answer; then a checksum of 3000 random strings of 1 to 40
letters from 1, 2 and 26 letters in turn; then the constraints' largest,
10^5 of one letter, whose sum of 5000050000 is past `i32`, and 10^5
random from two letters. `scores.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one round of 13 edits:
`s.as_bytes()` to `s.bytes()`, `vec![0usize; n]` to `Vec.filled(n, 0)`,
`let (mut l, mut r) = (0usize, 0usize)` to `let mut (l, r) = (0, 0)`,
`n as i64` and `z[i] as i64` to `n` and `z[i]`, as the indices are
`i64` already, `&&` to `and`, `struct Solution;` to `struct Solution {}`
and `Solution::` to `Solution.`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: `s_1` to `s_n` built by prepending one letter of `s` at a
time from the back, each compared with `s` letter by letter from the
front, and the common prefixes summed; no Z box. It checks 300 random
strings of 1 to 48 letters from 1, 2 and 3 letters in turn; then 30 of
1 to 24 letters, a pattern of 1 to 4 repeated; then 30 of 1 to 24
letters all different. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the sum is the statement read literally |
| P2 | it is at least n and at most n * (n + 1) / 2 |
| P3 | every letter renamed one along the alphabet: the same sum |
| P4 | a letter not in s appended: the sum one more |
| P5 | s written twice: at least twice the sum, and n more |
| P6 | each arm agrees with at least three of the other five |

P4 holds because the new letter matches nothing in `s`: every old
suffix keeps its score, the whole string scores one more, and the new
one-letter suffix scores 0. P5 holds because every suffix of either
copy scores at least what it scored in `s`, and the whole of `ss`
scores n more than the whole of `s`.

The first 300 strings ran to 24 letters at first, and one edit to the
iter arm survived: an extension past the box dropped when the box
already knew more than three letters, a path those strings reached
about once in three hundred. At 48 letters it is reached often enough
to kill it (M26).

The differential prints `360 cases: checksum 320057000, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading over
`os.path.commonprefix` of each suffix and `s`. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to each
of the others, each run under `karac __mir-llvm-run` and `karac
__mir-run`. Seventeen are kept, three to each Kāra arm and two to the
Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `z[0]` 0, not n | P1 360, P2 203, P4 360, P6 360 |
| M3 | ★: a z started in the box from the larger of its two bounds | P1 283, P2 123, P4 212, P6 283 |
| M4 | ★: a z started from its mirror, not capped at the box's edge | P1 204, P2 112, P4 164, P5 1, P6 204 |
| M7 | borders: the total starting at 0, the first letter uncounted | P1 360, P2 49, P6 360 |
| M8 | borders: each border counted twice | P1 311, P2 118, P6 311 |
| M9 | borders: a mismatch dropping to no border, not along the chain | P1 62, P5 50, P6 62 |
| M12 | hash: the test made "first agrees or second differs" | P1 233, P4 360, P6 233 |
| M13 | hash: the search capped one below the suffix's length | P1 251, P4 251, P5 109, P6 251 |
| M16 | hash: the suffix compared with s from its second letter | P1 162, P5 233, P6 162 |
| M17 | struct: a z started one past its mirror | P1 147, P6 147 |
| M18 | struct: every z matched afresh and capped at 5 | P1 147, P5 279, P6 147 |
| M21 | struct: each letter compared with the one after its partner | P1 212, P4 218, P6 212 |
| M22 | iter: the suffix side skipped to i, not past what is known | P1 223, P2 119, P4 158, P5 13, P6 223 |
| M24 | iter: the letters counted while they differ | P1 344, P4 360, P5 273, P6 344 |
| M26 | iter: the extension dropped when the box knows more than 3 | P1 2, P5 9, P6 2 |
| M29 | solution: every letter compared with `s[0]` | P1 145, P5 227, P6 145 |
| M30 | solution: each z capped at 7 | P1 119, P5 233, P6 119 |

P1 and P6 kill all seventeen, P5 ten, P4 eight, P2 six and P3 none. P3
renames every letter, and no arm looks at which letter it reads, only
whether two agree, so no edit can tell the names apart; it stays as a
check that no arm leans on the alphabet. P5's doubled string is where
capped and truncated matches show (M16, M18, M26, M29, M30), and P4's
new letter is where an edit that lets a mismatch through, or misses the
end, shows (M12, M21, M24).

Of the thirty-one, fourteen were not kept. Six survive and are
equivalent, since the Z box only saves work: the ★ arm's box never
consulted or never moved (M2, M6), the iter arm's z always started from
0 (M25), and the template's start one short of the box's edge and its
box never grown (M28, M31) leave the letter-by-letter extension to find
the same z, only more slowly; and the struct arm's `z[0]` of 1 (M20) is
never read, as the box never starts at 0. One crashes under both
backends, as it should: the struct arm's box moved without its left
edge sends a later z to a mirror not yet worked out (M19). The other seven are
killed, and none differs between the backends. Six fail as a kept one
does: the hash arm's, the iter arm's and the template's total without
`z[0]` (M15, M23, M27) as the ★ arm's (M1); the ★ arm's extension
stopping one short of the end (M5) as the hash arm's search capped one
below (M13); the borders arm's count taken from the border's length
(M10) as the struct arm's z one past its mirror (M17); and the hash
arm's lengths below 3 always accepted (M14) as its "or" test (M12). One
fails its own way and is left out for the count of three: the borders
arm's fallback one step short (M11).

## Verification

Every arm prints the same output as `scores.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, borders, struct and template arms take
0.7 s to 1.0 s, the iter arm 2.4 s, the hash arm 6.4 s, and the
differential 1.1 s.

## Benchmarks

The bench draws 20 strings of 10^5 letters once, each `'a'` or `'b'`,
then punches each string 5 times, one letter drawn again each time, and
answers it after each punch with the ★ arm in all five languages. Every
implementation prints `20 strings of 10^5, 5 punches: checksum
176606982`.

BENCHTAB
