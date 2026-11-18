# 2262. Total Appeal of A String

The **appeal** of a string is the number of **distinct** characters
found in the string. For example, the appeal of `"abbca"` is 3 because
it has 3 distinct characters: `'a'`, `'b'`, and `'c'`.

Given a string `s`, return *the **total appeal of all of its
substrings**.* A **substring** is a contiguous sequence of characters
within a string.

```
s = "abbca"  ->  28
s = "code"   ->  20
```

**Constraints:** `1 <= s.length <= 10^5`; `s` consists of lowercase
English letters.

There are about n^2 / 2 substrings, too many to visit at 10^5. Counted
the other way round, each position adds one to the appeal of every
substring in which its letter appears first: the substrings that start
after the letter's previous position and at or before this one, and end
at or after it. That is `(i - last) * (n - i)`, and the total is O(n).

## Approaches

| file | mechanism |
|---|---|
| `appeal.kara` ★ | `(i - last[c]) * (n - i)` summed over the positions, the last positions in an `Array[i64, 26]` of `-1` |
| `appeal_dp.kara` | by the substrings that end at each position: `ending += i - last`, the new first appearances, then `total += ending`; the last positions in a `Map[char, i64]` over `chars()` |
| `appeal_gaps.kara` | letter by letter: of all `n (n + 1) / 2` substrings, those that hold a letter are the ones not inside a gap between its occurrences, a gap of `g` holding `g (g + 1) / 2`; 26 passes |
| `appeal_struct.kara` | `struct Reader` of the last positions and the running totals; `read` (`mut ref self`) takes one letter |
| `appeal_iter.kara` | one `fold` over `char_indices`, the state the last positions as a `Vec` of 26 and the ★ arm's running sum, destructured in the closure's parameters |
| `appeal_solution.kara` | LeetCode's Rust template: `String` in, `i64` out; `as_bytes`, a `[-1i64; 26]`, and the dp arm's running `cur`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four
more (one letter, one letter three times, every letter once, and
`racecar`), each with its total; then 3000 strings of 1 to 40 letters
from the first 1, 2, 3, 5 or 26 of the alphabet, with a checksum; then
three of the constraints' longest, 10^5 letters: all `a`
(5000050000), `abc` repeated (14999850001), and random from all 26
(129936420165). `appeal.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one round of 6 edits: `as_bytes()`
to `bytes()`, `[-1i64; 26]` to `[-1; 26]`, the pattern `&b` to `b`, the
two `i as i64` casts dropped, since `enumerate`'s index is already an
`i64`, and `struct Solution;` to `struct Solution {}`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every substring `s[i..=j]` in turn, its appeal counted as
the letters that differ from every earlier letter of that substring,
and the appeals summed. No last positions and no running totals. It
checks 300 random strings of 1 to 12 letters from the first 1, 2, 3, 5
or 26 of the alphabet; then 30 palindromes of up to 13 letters from
the first 4; then 30 strings of up to 12 different letters, five apart
round the alphabet. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the total is the literal reading's |
| P2 | the string reversed: the same total |
| P3 | every letter moved 7 on round the alphabet: the same total |
| P4 | no less than `n (n + 1) / 2` and no more than that times the number of different letters |
| P5 | the last letter put on the end again: the total plus one plus the different letters of every suffix |
| P6 | each arm agrees with at least three of the other five |

P5 holds because the last letter is already in every suffix, so each
suffix extended by it keeps its appeal, and the one new substring of
that letter alone adds one.

The differential prints `360 cases: checksum 963819177, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that sums
`len(set(s[i:j + 1]))` over every substring. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the ends counted from the start | P1 243, P2 126, P4 48, P5 249, P6 243 |
| M3 | ★: every letter as `a` | P1 249, P5 249, P6 249 |
| M4 | ★: the starts one short | P1 360, P4 221, P5 360, P6 360 |
| M7 | dp: the running appeal not carried | P1 321, P2 126, P4 264, P5 360, P6 321 |
| M8 | dp: the total before the new letter | P1 360, P2 126, P4 161, P5 360, P6 360 |
| M10 | dp: the first position kept | P1 193, P2 98, P4 104, P5 242, P6 193 |
| M12 | gaps: the final gap forgotten | P1 360, P2 127, P4 360, P5 360, P6 360 |
| M13 | gaps: a gap's substrings as g squared | P1 321, P4 221, P5 360, P6 321 |
| M14 | gaps: only the letters to `y` | P1 21, P3 35, P4 1, P5 21, P6 21 |
| M17 | struct: the letters folded by 7 | P1 62, P3 50, P5 62, P6 62 |
| M20 | struct: the last position recorded one late | P1 264, P2 126, P4 88, P5 360, P6 264 |
| M21 | struct: each letter counted one more | P1 360, P4 232, P5 360, P6 360 |
| M24 | iter: the letters folded by 13 | P1 29, P5 29, P6 29 |
| M25 | iter: the starts squared | P1 249, P2 144, P4 230, P5 249, P6 249 |
| M26 | iter: the first position never counted | P1 360, P4 136, P5 360, P6 360 |
| M27 | solution: the current appeal added twice | P1 360, P4 294, P5 360, P6 360 |
| M30 | solution: the letters by their byte mod 3 | P1 117, P3 48, P5 117, P6 117 |

P1, P5 and P6 kill all seventeen, P4 thirteen, P2 seven, and P3 three.
P5 catches every miscount, since the harness works out the change
itself from the suffixes. P4 misses four of the five edits that only
merge letters, since a total over fewer letters is still in range, and
P3 catches three of them, those whose merges change when the letters
move: `y` and `z` lost from the gaps arm, and letters folded by 7 or by
byte mod 3. Every letter as `a` and the fold by 13 pass P3 on every
case. P2 catches the edits that favour one end.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Eleven fail as a kept one does or as a group:
the ★, iter and template arms' last positions never kept (M2, M23,
M28) all alike; the ★ arm's last position one late (M6) as the struct
arm's (M20); the dp arm's new letter's start at 0 (M9) as its total
taken before the new letter (M8); the dp and struct arms' position
never advanced, the struct arm's running appeal reset and the
template's restarted (M11, M18, M19, M29) as the dp arm's running
appeal not carried (M7); the iter arm's ends counted from the start
(M22) as the ★ arm's (M1); and the template's answer less the length
(M31) as the iter arm's first position never counted (M26). Three fail
in ways of their own and are left out because their arms keep enough:
the ★ arm's ends one more (M5), the gaps arm's gap never reset (M15),
and its whole taken as `n^2 / 2` (M16).

Three struct edits of the first draft were replaced, none of them
equivalent: the total taken before the new letter and the start
positions at 0 failed as M8, and the total overwritten, tried in
place of the second, as M7. They are now M17 and M21.

## Verification

Every arm prints the same output as `appeal.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the struct and ★ arms take 0.7 s, the differential
0.8 s, the iter arm 0.9 s, the dp arm and the template 1.0 s, and the
gaps arm 6.2 s, which reads the string once per letter.

## Benchmarks

The bench answers 40 strings of the constraints' longest, 10^5 letters,
the t-th from the first `t % 26 + 1` letters of the alphabet, with the ★
arm in all five languages. Every implementation prints `40 strings of
10^5: checksum 131792896`. Each builds its string a letter at a time
from the same generator and keeps the last positions in a fixed array
of 26.

BENCHTAB
