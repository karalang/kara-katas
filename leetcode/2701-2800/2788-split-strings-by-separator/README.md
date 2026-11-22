# 2788. Split Strings by Separator

Given an array of strings `words` and a character `separator`, **split**
each string in `words` by `separator`.

Return *an array of strings containing the new strings formed after the
splits, **excluding empty strings***.

**Notes**

- `separator` is used to determine where the split should occur, but it
  is not included as part of the resulting strings.
- A split may result in more than two strings.
- The resulting strings must maintain the same order as they were
  initially given.

```
words = ["one.two.three", "four.five", "six"], separator = "."  ->  ["one", "two", "three", "four", "five", "six"]
words = ["$easy$", "$problem$"], separator = "$"                ->  ["easy", "problem"]
words = ["|||"], separator = "|"                                ->  []
```

**Constraints:** `1 <= words.length <= 100`, `1 <= words[i].length <=
20`, the characters of `words[i]` are lowercase English letters or
characters from `".,|$#@"`, and `separator` is one of `".,|$#@"`.

## Approaches

| file | mechanism |
|---|---|
| `split.kara` ★ | each word split at the separator by `split`, the empty pieces dropped by `filter`, and the rest gathered across the words by `flat_map`, each piece copied out of its word. O(total length) |
| `split_scan.kara` | by hand: each word's characters walked once, a piece grown in a `String` and pushed when the separator or the word's end closes it with something in it. O(total length) |
| `split_cuts.kara` | by byte offsets: the separator's places in each word by `char_indices`, the word's two ends added, and the slice between each pair of neighbouring cuts by `windows(2)` kept when it is not empty. O(total length) |
| `split_joined.kara` | the words joined into one text by the separator itself, which can only add empty pieces, and the whole split once by `split`, the empty pieces dropped. O(total length) |
| `split_solution.kara` | a Rust solution as LeetCode's Rust users write it, `words.iter().flat_map(\|w\| w.split(separator)).filter(\|s\| !s.is_empty())` and each piece made a `String`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's three examples; a
separator only between words, at their ends, and doubled; 100 words of
20, LeetCode's most, every other character the separator; and 3000
random cases of 1 to 5 words of 1 to 8 characters from a, b, `.` and
`|`, split by `.` or `|`, with the number of pieces and a checksum.
`split.py` mirrors the ★ arm and its output is byte-identical.

```
[one, two, three, four, five, six]
[easy, problem]
[]
[a, b, c, d, e, f]
1000
3000 small cases: 12662 pieces, checksum 317824624
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: in each word every slice from a start, the word's start or
just after a separator, to an end, the word's end or a separator, with
no separator inside and something in it, taken in the order of the
words and of their starts; no `split`. It draws 2000 random cases of 1
to 5 words of 1 to 8 characters from a, b, `.` and `|`, split by `.` or
`|`; then 50 of up to 100 words of up to 20 characters, LeetCode's most,
from a, b, c and the six separators, split by one of them, all before
any arm answers; the literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 5 words, the pieces are the literal reading's |
| P2 | the words joined into one by the separator: the same pieces |
| P3 | the words and each word reversed: the pieces reversed, each reversed |
| P4 | every separator doubled: the same pieces |
| P5 | no piece empty or holding the separator, and their letters all the letters of the words that are not the separator |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 695994497, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same slices gives the same checksum. On
a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the empty pieces kept | P1 1578, P4 1845, P5 1628, P6 1628 |
| M2 | ★: only each word's first piece kept | P1 1612, P2 1500, P3 1747, P5 1662, P6 1662 |
| M3 | scan: a word's last piece never pushed | P1 1871, P2 1510, P3 1752, P5 1921, P6 1921 |
| M4 | scan: a piece not started again after a separator | P1 1624, P2 1627, P3 1787, P4 1674, P5 1674, P6 1674 |
| M5 | cuts: a piece cut one character short | P1 1980, P3 1827, P5 2030, P6 2030 |
| M6 | cuts: the empty pieces kept | P1 1578, P4 1845, P5 1628, P6 1628 |
| M7 | joined: the words run together with nothing between | P1 1274, P2 1324, P6 1324 |
| M8 | joined: a piece of one character dropped | P1 1540, P5 1588, P6 1588 |
| M9 | solution: only the empty pieces kept | P1 2000, P4 1845, P5 2050, P6 2050 |
| M10 | solution: every piece upper-cased | P1 1932, P6 1982 |

## Benchmarks

The bench draws 20000 lists of 100 words of up to 20 characters,
LeetCode's most, all of them first, then splits each 10 times by the ★
arm in all five languages. Every implementation prints `20000 lists of
100 words, 10 rounds: 55305980 pieces, checksum 92418645`.

BENCHTAB

## Verification

All five arms print the same output as `split.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

Three of the own arms checked clean as first written. The joined arm
was refused: `karac check` said `words.join(sep)` moved `sep`, so the
`split(sep)` after it used a moved value. `join` only reads its
separator, as `Str.join` already knew. That was kara
`B-2026-11-20-150`, fixed at `0d28296389`: a `Vec`'s methods now take their
borrowed arguments by the same table as a string's.

LeetCode's Rust solutions mostly write the last step as
`.map(String::from)`. `karac fix` carries that to `.map(String.from)`,
which checks, and then the MIR lowering refuses a type's function named
as a value, "this path is not lowered yet". That is kara
`B-2026-11-20-151`, open; the solution arm writes the closure
`.map(|s| s.to_string())`, the other common form.

LeetCode's Rust template took 12 `karac fix` edits, the wrapper
included: `struct Solution {}` added; the `Vec<String>`s became
`Vec[String]`; `split(separator)` by a `char` pattern became
`split(separator.to_string())`, Kāra's `split` taking a string; `!`
became `not`; and `Solution::` became `Solution.`.
