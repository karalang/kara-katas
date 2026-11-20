# 2405. Optimal Partition of String

Given a string `s`, partition it into one or more substrings such that
the characters in each substring are **unique**: no letter appears in a
single substring more than once.

Return *the **minimum** number of substrings in such a partition*.

Note that each character should belong to exactly one substring.

```
s = "abacaba"   ->  4      ("a","ba","cab","a")
s = "ssssss"    ->  6
```

**Constraints:** `1 <= s.length <= 10^5`; `s` consists of only English
lowercase letters.

Running each part as long as it can is optimal: cutting later never
leaves the rest harder, since a suffix of a part with distinct letters
has distinct letters too. One arm takes no greedy argument and computes
the fewest parts of every prefix.

## Approaches

| file | mechanism |
|---|---|
| `partition.kara` ★ | greedy with a bitmask: the current part's letters are bits of an `i64`, and a letter whose bit is set starts the next part, the mask reset to that letter. O(n) |
| `partition_last.kara` | the last index of each letter in a `Vec` of 26: a letter last seen at or after the current part's start is a repeat, and the next part starts here. O(n) |
| `partition_set.kara` | a `Set[char]` of the current part's chars, cleared at a repeat; only membership is asked, so its order never shows. O(n) |
| `partition_dp.kara` | dynamic programming, no greedy: the fewest parts of each prefix, over every last part ending there with distinct letters, found by walking back until a letter repeats, at most 26 steps. O(26 n) |
| `partition_iter.kara` | iterators: one `fold` over the bytes carrying (mask, parts). O(n) |
| `partition_solution.kara` | LeetCode's Rust template: a `[false; 26]` over `s.chars()`, each slot `as usize`, reset to a fresh array at a repeat; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; one letter;
the alphabet once and twice; `10^5` letters of all 26 and `10^5` of the
first 3; then 3000 random strings of 1 to 30 letters from the first 1 to
26, with a checksum and the total of the answers. `partition.py` mirrors
the ★ arm and its output is byte-identical, and the mirror was checked
on 20000 random strings of up to 14 letters against the fewest parts
over every cutting.

`check` first reports 1 error on the template, `struct Solution;`, and
`karac fix` carries it in one call, reporting 2 edits: `struct
Solution;` given its braces, and `c as u8`, a cast Kāra does not take
from a `char`, written `c as u32 as u8`. `[false; 26]`, its reset by
assignment and `seen[i]` indexed by a `usize` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to cut the string, each part's letters compared
pair by pair, and the fewest parts of any cutting whose parts all have
distinct letters. No greedy and no masks. It checks 300 random strings
of 1 to 12 letters from the first 1 to 6, which the literal reading
answers; then 30 of up to 3000 letters of all 26; then 30 of up to 3000
letters of the first 2 to 4. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 12 letters, the answer is the literal reading's |
| P2 | the answer is at least `n / 26` rounded up, at least the most times any letter appears, and at most `n` |
| P3 | the string reversed: the same answer |
| P4 | every letter renamed one along the alphabet, `z` to `a`: the same answer |
| P5 | the string written twice: twice the answer, or one less |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a part holds each letter at most once, so at most 26
letters, and the copies of one letter must be in different parts. P3
holds because the parts of a cutting, reversed, cut the reversed string.
P4 holds because renaming is one to one. P5 holds because the two
halves' best cuttings together cut the whole in `2a`, and splitting the
part that straddles the middle of any cutting, if one does, cuts the two
halves with one part more, so no cutting has fewer than `2a - 1`.

The differential prints `360 cases: checksum 533802666, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tries every cutting. On a failure it prints the
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
| M1 | ★: a z never remembered | P4 22, P6 25 |
| M5 | ★: letters merged in pairs | P1 172, P4 198, P6 232 |
| M6 | ★: the first letter skipped | P1 160, P2 119, P3 109, P5 138, P6 183 |
| M7 | last: a repeat of the part's first letter missed | P1 210, P2 192, P3 91, P6 269 |
| M8 | last: the cutting letter left out of its part | P1 164, P2 142, P6 223 |
| M10 | last: nothing remembered | P1 249, P2 309, P6 309 |
| M12 | set: the letters never cleared at a cut | P1 123, P5 274, P6 183 |
| M14 | set: a repeat in a one-letter part missed | P1 166, P2 155, P3 121, P6 225 |
| M15 | set: no part counted at the start | P1 300, P2 232, P5 292, P6 360 |
| M17 | dp: each part counted twice | P1 300, P2 191, P5 50, P6 360 |
| M18 | dp: no part starting at the first letter | P1 300, P2 360, P6 360 |
| M20 | dp: the empty prefix needing a part | P1 300, P2 86, P5 68, P6 360 |
| M23 | iter: only the last letter remembered | P1 137, P2 157, P6 197 |
| M24 | iter: z taken for a | P4 28, P6 29 |
| M25 | iter: a repeated a never cutting | P1 127, P2 95, P4 181, P6 183 |
| M27 | solution: every letter cutting after the first cut | P1 161, P3 165, P5 199, P6 221 |
| M28 | solution: letters 13 apart taken as one | P6 30 |

P6 kills all seventeen, P1 fourteen, P2 eleven, P5 six, and P3 and P4
four each. The three that P1 misses touch only letters the small cases
never hold, since those draw from the first 1 to 6: a `z` never
remembered (M1) and `z` taken for `a` (M24) fail P4, whose renaming
carries `y` to `z` and `z` to `a` in the cases of all 26, and the
template's letters 13 apart taken as one (M28) fails only P6, outvoted
in those same cases.

Of the thirty-one, fourteen were not kept, each failing the same checks
as a kept one or, for one, left over: the letters never cleared at a cut
(M2, M26) as the set arm's (M12); only the last letter remembered (M3)
as the iter arm's (M23); a repeated `a` never cutting (M4) as M25; the
first letter skipped or the first part starting at 1 (M9, M16, M31) as
the ★ arm's first letter skipped (M6); no part counted at the start
(M11) as M15; the cutting letter left out of its part (M13, M22) as the
last arm's (M8); nothing remembered or a repeat allowed in a part (M19,
M29) as M10; and the template's letters merged in pairs (M30) as M5.
The dp arm's letters kept across ends (M21) fails apart from every kept
one, and was left out because that arm keeps three already. Four were
replaced by edits that fail apart from every kept one: the ★ arm's, the
iter arm's and the template's no part counted at the start (M1, M24,
M27), which failed as M15, are now a `z` never remembered, `z` taken
for `a`, and every letter cutting after the first cut; and the
template's letters never cleared at a cut (M28), which failed as M12,
is now letters 13 apart taken as one.

## Verification

Every arm prints the same output as `partition.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.62 to 1.8 s. The differential
takes 5 s there, 1.3 s under `karac __mir-llvm-asan` and 0.4 s under
`karac run`.

## Benchmarks

The bench builds 26 strings of `10^5` letters, string `i` from the first
`i + 1` letters, once from the harness's generator, then makes 50
passes, answering every string and folding each answer plus the pass
into the checksum, with the ★ arm in all five languages. Every
implementation prints `50 passes over 26 strings of 10^5 letters:
checksum 853909308`. Each keeps the mask in a 64-bit integer; Kāra
reads the string's bytes, Rust `str::bytes`, Go indexes the string, C a
fixed byte array and Python a `bytes` object.

BENCHTAB
