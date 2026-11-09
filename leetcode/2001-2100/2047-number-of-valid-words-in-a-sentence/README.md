# 2047. Number of Valid Words in a Sentence

A sentence consists of lowercase letters (`'a'` to `'z'`), digits (`'0'`
to `'9'`), hyphens (`'-'`), punctuation marks (`'!'`, `'.'`, and `','`),
and spaces (`' '`) only. Each sentence can be broken down into one or more
tokens separated by one or more spaces. A token is a valid word if all
three of the following are true:

- It only contains lowercase letters, hyphens, and/or punctuation (no
  digits).
- There is at most one hyphen. If present, it must be surrounded by
  lowercase characters (`"a-b"` is valid, but `"-ab"` and `"ab-"` are not).
- There is at most one punctuation mark. If present, it must be at the end
  of the token (`"ab,"`, `"cd!"`, and `"."` are valid, but `"a!b"` and
  `"c.,"` are not).

Given a string `sentence`, return the number of valid words in it.

```
sentence = "cat and  dog"                               ->  3
sentence = "!this  1-s b8d!"                            ->  0
sentence = "alice and  bob are playing stone-game10"    ->  5
```

**Constraints:** `1 <= sentence.length <= 1000`; `sentence` only contains
lowercase English letters, digits, `' '`, `'-'`, `'!'`, `'.'`, and `','`;
there will be at least one token.

## Approaches

| file | mechanism |
|---|---|
| `valid.kara` ★ | the tokens by `split_whitespace`, each collected into a `Vec[char]` and walked once: a digit fails it, a hyphen fails it if it is the second, at either end, or not between two `is_ascii_lowercase` letters, and a mark fails it unless it is last. O(n) |
| `valid_scan.kara` | one pass over `sentence.bytes()` with no splitting: each token's state (still valid, a hyphen seen, a mark seen, the byte before) carried along in `u8` comparisons, and a token judged at the space or the end that closes it. O(n) |
| `valid_counts.kara` | `split(" ")` with the empty pieces dropped; each token judged by counting rather than walking: `chars().any(..)` for a digit, a `match` on the count of hyphens and of marks, the hyphen placed by `find` and its neighbours read by `char_at`. O(n) |
| `valid_iter.kara` | one iterator chain, `split_whitespace().filter(..).count()`, its closure asking of every character, by `chars().enumerate().all(..)` and a `match` with a range pattern, whether it may stand where it stands, through a second closure `letter`. O(n) |
| `valid_regex.kara` | `std.regex`'s `Regex`, `^([a-z]+(-[a-z]+)?)?[!.,]?$` compiled once a sentence and matched against every token. O(n) |
| `valid_solution.kara` | LeetCode's Rust template (`sentence.split_whitespace().filter(\|w\| Self::valid(w)).count() as i32`, a walk over `w.as_bytes()` with `u8::is_ascii_digit` and `is_ascii_lowercase`, `\|\|`, `&&`, `!`), carried by `karac fix` in two rounds to a clean check |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and four more,
each sentence and its count; then the total and a checksum of the counts
for 2000 sentences of 1 to 40 characters from every kind of symbol, and for
3000 sentences of 1000 characters, the longest the constraints allow, drawn
from letters weighted towards hyphens and marks. `valid.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the sentence cut into tokens at every space, and each token
tried against the three rules in turn, the characters it may hold, then
the hyphens found and their neighbours, then the marks found and where they
stand. It checks 1500 sentences of 0 to 30 characters from `a`, `b`, `c`,
hyphens, marks, the digits `0` and `9`, and spaces. Every random choice is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every space doubled, and spaces added at both ends, leave the answer |
| P3 | the tokens in reverse order leave the answer |
| P4 | the sentence written twice, a space between, doubles the answer |
| P5 | the letters `a` and `c` swapped leave the answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `1500 sentences: checksum 348114760, 54000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-six edits to the differential, six to each of its arms, each run
under `karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one is
killed, fails the same way under both backends and not by a crash, and no
two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: digits allowed | P1 530, P6 530 |
| M2 | ★: a mark allowed second to last | P1 207, P6 207 |
| M3 | ★: every one-character token counted | P1 137, P6 137 |
| M4 | scan: digits allowed | P1 538, P6 538 |
| M5 | scan: more after a mark allowed | P1 506, P6 506 |
| M6 | scan: an invalid token's state carried on | P1 663, P3 650, P4 434, P6 663 |
| M7 | counts: only a 9 taken as a digit | P1 292, P6 292 |
| M8 | counts: two marks allowed | P1 83, P6 83 |
| M9 | counts: the empty pieces counted | P1 828, P2 1500, P3 793, P6 828 |
| M10 | iter: a 9 allowed (`'0'..='8'`) | P1 267, P6 267 |
| M11 | iter: no letter needed after a hyphen | P1 66, P6 66 |
| M12 | iter: a comma allowed anywhere | P1 166, P6 166 |
| M13 | regex: a hyphen needing no letter before it | P1 68, P6 68 |
| M14 | regex: any number of marks | P1 32, P6 32 |
| M15 | regex: a comma not a mark | P1 107, P6 107 |
| M16 | solution: the adapter dropping commas | P1 210, P6 210 |
| M17 | solution: the invalid tokens counted | P1 1180, P6 1180 |

P1 and P6 kill all seventeen; P3 two, P2 and P4 one, and P5 none. Each
token is judged alone, so an edit to the rule for one token changes no
answer when the tokens are reordered, spaced out or written twice, and the
properties those make see only edits that let one token's judgment reach
another: the scan arm's invalid state carried on to the tokens after it
(M6), which reversing or doubling the sentence changes, and the empty
pieces counted (M9), which more spaces make more of. P5 swaps two letters,
and nothing here tells one letter from another.

All thirty-six were killed. The nineteen not kept fail as a kept one does,
or on checks of their own in an arm that keeps three already. Digits
allowed in the Rust arm fails as M1, a comma not taken as a mark (★) as
M12, and a hyphen needing no letter after it (regex) as M11. A mark allowed
anywhere (counts) or anywhere but first (iter, Rust) fail alike; two
hyphens allowed, in six spellings across five arms, fail on the same 4
sentences; and no letter needed after a hyphen (★), a mark allowed after a
hyphen (scan), the letter after a hyphen read before it (counts) and any
character beside a hyphen (iter) on the same 7. Two hyphens judged as one
(counts, 5 sentences), a trailing hyphen allowed (scan, 60) and anything
after the word (regex, 1177) fail on checks of their own.

## Verification

Every arm prints the same output as `valid.py` under `karac __mir-run` (the
v2 MIR interpreter), `karac __mir-llvm-run`, and `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer) with no error. `karac run` and a
`karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 6.4 s (scan) to 18.9 s (counts) and
the differential 4.2 s, on kara 531a0f19a1.

The five Kāra arms met no compiler gap and checked as written.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in two rounds (twelve edits, then one) to a clean check: `struct
Solution;` to `struct Solution {}`, `&str` to `Str`, `w.as_bytes()` to
`w.bytes()`, `Self::valid` to `Solution.valid`, `||` to `or`, `&&` to
`and`, `!` to `not`, and `as i32` kept. The adapter that hands the
harness's `Str` to it returns the `i32` count widened to `i64` without a
cast, which `karac check` would otherwise flag as unnecessary.

## Benchmarks

The bench builds 2000 sentences of 1000 characters once in all five
languages, the longest the constraints allow, and runs the ★ arm on every
sentence for 100 rounds, each from a byte offset of 0 to 6 set by the
round: 200000 calls. The Kāra, Rust and Go programs collect each token's
characters as the ★ arm does; the C program checks each token in place, by
index, with no allocation. Every implementation prints `200000 calls:
18588135 valid words, checksum 767406645`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `531a0f19a1` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.827 to 0.969 s | 0.879 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.602 to 1.738 s | 1.661 s |
| Kāra (`karac build`) | 1.566 to 1.761 s | 1.685 s |
| Go | 2.044 to 2.265 s | 2.210 s |
| Rust (`rustc -O`) | 2.239 to 2.501 s | 2.368 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.337 to 2.661 s | 2.471 s |
| Python | 15.8 s |  |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (1.666 s) is not above its real time (1.685 s).

The sequential Kāra program is 0.67x Rust under overflow checks and 1.89x
C, which allocates nothing per token.
