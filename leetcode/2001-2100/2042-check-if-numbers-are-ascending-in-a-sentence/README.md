# 2042. Check if Numbers Are Ascending in a Sentence

A sentence is a list of tokens separated by a single space with no leading
or trailing spaces. Every token is either a positive number made of digits
`0` to `9` with no leading zeros, or a word made of lowercase English
letters. Given a string `s` representing a sentence, check whether all the
numbers in `s` are strictly increasing from left to right, each number
smaller than the number to its right. Return `true` if so, or `false`
otherwise.

```
s = "1 box has 3 blue 4 red 6 green and 12 yellow marbles"              ->  true
s = "hello world 5 x 5"                                                  ->  false
s = "sunset is at 7 51 pm overnight lows will be in the low 50 and 60 s" ->  false
```

**Constraints:** `3 <= s.length <= 200`; `s` consists of lowercase English
letters, spaces, and digits from `0` to `9`, inclusive; the number of
tokens in `s` is between 2 and 100, inclusive; the tokens are separated by
a single space and there are at least two numbers; each number is a
positive number less than 100, with no leading zeros; `s` has no leading
or trailing spaces.

A word never parses as a number, so the numbers are the tokens that parse,
and strictly increasing means each one is above the one before it. A
running `last`, starting below every positive number, decides it in one
pass.

## Approaches

| file | mechanism |
|---|---|
| `ascending.kara` ★ | `s.split(" ")`, each token tried with `if let Ok(n) = i64.parse(token)` and compared with the last. O(n) |
| `ascending_windows.kara` | the numbers collected by `filter_map(\|token\| i64.parse(token).ok())`, then `windows(2).iter().all(\|pair\| pair[0] < pair[1])`. O(n) |
| `ascending_bytes.kara` | one scan over `bytes()`, a digit (`b'0'` to `b'9'`) extending the number being read by `b - b'0'`, a space or the end finishing it. O(n), no allocation |
| `ascending_fold.kara` | one `fold((0, None, true), \|(last, reading, rising), c\| ..)` over `chars().chain(" ".chars())`, a `match` on `(c.to_digit(10), reading)`, the number being read an `Option`. O(n) |
| `ascending_digits.kara` | `split_whitespace`, a number known by `is_ascii_digit` on its first char, its value folded from `to_digit` by hand, then `zip` with `skip(1)` and `all`. O(n) |
| `ascending_solution.kara` | LeetCode's Rust template (`impl Solution`, `split_whitespace`, `if let Ok(n) = w.parse::<i32>()`), carried by `karac fix` in one round to a clean check |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's three
examples and six more, then how many of 4000 random sentences (up to 32
tokens, numbers that climb by up to 1 to 20 and fall by up to 3) have
rising numbers, with a checksum of the answers in order. `ascending.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the sentence walked a character at a time into tokens, a token
of digits only taken as a number, and every earlier number compared with
every later one. It checks 1500 sentences of 3 to 14 tokens, each with a
place to cut it. Every random choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the words dropped, the numbers alone, leave the answer |
| P3 | a number above all the others appended leaves the answer |
| P4 | the last number repeated at the end makes the answer `false` |
| P5 | a sentence whose numbers rise still does when cut after any token |
| P6 | each arm agrees with at least three of the other five |

The differential prints `1500 sentences: checksum 297517314, 54000 checks
over 6 arms: 0 failures` under every lane in Verification; 757 of the 1500
rise, and the checksum is also computed by a few lines of Python. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept, three to
each Kāra arm and two to the Rust-template arm. All thirty are killed, each
fails the same way under both backends, none by a crash, and no two kept
ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an equal number accepted (`<` for `<=`) | P1 287, P4 1044, P6 287 |
| M2 | ★: tokens past the tenth ignored | P1 97, P2 97, P4 335, P6 97 |
| M3 | ★: each number wanting a gap of two | P1 179, P3 578, P6 179 |
| M4 | windows: windows of three, the last pair unchecked | P1 177, P3 177, P4 757, P6 177 |
| M5 | windows: any pair rising enough (`any` for `all`) | P1 621, P3 122, P4 1378, P5 721, P6 621 |
| M6 | windows: only the tens digits compared | P1 662, P4 1419, P6 662 |
| M7 | bytes: a one-digit number never finished | P1 393, P3 96, P4 180, P6 393 |
| M8 | bytes: 0 not taken as a digit (`b'1'` for `b'0'`) | P1 201, P3 61, P6 201 |
| M9 | bytes: 9 not taken as a digit | P1 178, P3 53, P4 27, P6 178 |
| M10 | fold: a number's later digits read as zeros | P1 426, P3 260, P6 426 |
| M11 | fold: the last number never moved on | P1 743, P4 1500, P6 743 |
| M12 | fold: a word resetting the last number | P1 193, P2 193, P6 193 |
| M13 | digits: a number read from its first digit | P1 550, P3 164, P6 550 |
| M14 | digits: each number paired with the one two on | P1 462, P4 1018, P6 462 |
| M15 | digits: the one-digit numbers left out | P1 320, P4 298, P6 320 |
| M16 | solution: the first token skipped | P1 49, P2 151, P6 49 |
| M17 | solution: a one-digit number never failing | P1 324, P4 299, P6 324 |

P1 and P6 kill all seventeen, P4 eleven, P3 eight, P2 three and P5 one. P2
sees only the edits that depend on where the numbers sit among the words: a
count of tokens (M2), a word that resets the last number (M12), and the
first token dropped (M16). P3 appends a number above all the others, so the
last number's pair is checked again with a gap of at least one: it sees the
edits that misread a number's value (M8, M9, M10, M13), a gap wanted wider
than one (M3), and the edits whose verdict changes once the old last number
is no longer last (M4, M5, M7). P4 sees every edit that can accept a
repeated last number: an equal pair taken as rising (M1, M6, M17), the last
pair compared wrongly or not at all (M2, M4, M7, M9, M11, M14, M15), and
`any`, which a rising pair elsewhere satisfies (M5). P5 sees only M5: every
other edit still checks a sentence's numbers pair by pair, so a prefix of a
sentence they pass passes too, while `any` fails a prefix with a single
number, which has no pair.

The other thirteen fail as a kept one does, or with a signature of their
own that adds nothing. An equal number accepted fails alike in the
windows, bytes, fold, digits and Rust arms as M1; the ★ and Rust arms'
last number never kept fail as M11; the bytes arm's end never finishing the
last number and the fold arm's space not appended fail as M4. The ★ and
Rust arms' numbers held above 1 from the start fail alike with a count of
their own (P1 21), and the windows arm's first number dropped and the
digits arm's numbers taken as falling with counts of their own. Two first
drafts were replaced. The bytes arm's number never reset kept growing
across the sentence and stopped on an integer overflow, a crash. The fold
arm's digits summed, `Some(n + d)`, was refused at the type check: with the
accumulator's number still open, `n + d` against a `u32` digit made it a
`u32`, which the `Some(d as i64)` beside it contradicts, as Rust's
inference would refuse it.

## Verification

Every arm prints the same output as `ascending.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error. `karac
run` and a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 0.9 s (bytes) to 1.7 s (fold) and the
differential 3.8 s, on kara 991c45adcd.

The five Kāra arms met no compiler gap. `karac fix` removed three casts
that widen implicitly: `(bytes[i] - b'0') as i64` in the bytes arm, and a
`u32` digit's `as i64` in the fold and digits arms (the fold arm keeps the
cast in `Some(d as i64)`, which fixes the `Option`'s type).

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in one round to a clean check: `w.parse::<i32>()` to `i32.parse(w)`,
since Kāra has no call-site type arguments and names the type before the
call, and the adapter's `Solution::are_numbers_ascending` to
`Solution.are_numbers_ascending`.

## Benchmarks

The bench builds 1000 sentences of up to 32 tokens once in all five
languages, and runs the ★ arm over all of them for 1000 rounds: 1000000
calls. Every implementation prints `1000000 calls: 318000 ascending,
checksum 642381920`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `991c45adcd` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.180 to 0.218 s | 0.194 s |
| Rust (`rustc -O`) | 0.222 to 0.257 s | 0.223 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.218 to 0.263 s | 0.224 s |
| Kāra (`karac build`) | 0.365 to 0.407 s | 0.379 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.376 to 0.437 s | 0.382 s |
| Go | 1.075 to 1.173 s | 1.104 s |
| Python | 5.5 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.375 s) is not above its real time (0.379 s).

The sequential Kāra program is 1.71x Rust under overflow checks and 1.97x
C.
