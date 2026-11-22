# 2734. Lexicographically Smallest String After Substring Operation

Given a string `s` consisting of lowercase English letters. Perform the
following operation:

- Select any non-empty substring then replace every letter of the
  substring with the preceding letter of the English alphabet. For
  example, 'b' is converted to 'a', and 'a' is converted to 'z'.

Return the **lexicographically smallest** string **after performing the
operation**.

```
s = "cbabc"     ->  "baabc"
s = "acbbc"     ->  "abaab"
s = "leetcode"  ->  "kddsbncd"
```

**Constraints:** `1 <= s.length <= 3 * 10^5`, `s` consists of lowercase
English letters.

## Approaches

Moving a letter back makes the string smaller only where it is not an
'a', and earlier places weigh more: the best substring starts at the
first letter that is not an 'a' and runs on to the next 'a' or the end.
A string of 'a's only must still change, and the least harm is its last
letter made 'z'.

| file | mechanism |
|---|---|
| `smallest.kara` ★ | the bytes in a `Vec[u8]`: past the leading 'a's, every byte up to the next 'a' made one less, and `String.from_utf8` at the end. O(n) |
| `smallest_chars.kara` | the letters in a `Vec[char]`, the run's start by `position`, each letter moved back through its byte, and the string built again by `collect`. O(n) |
| `smallest_split.kara` | the string cut in three by finding the first letter that is not an 'a' and then the next 'a': the leading 'a's, the run moved back by `map`, and the rest, joined in an f-string. O(n) |
| `smallest_build.kara` | one pass builds the answer with a three-state `enum Stage`, before the run, inside it and after it, each letter kept or moved back by the state it is read in. O(n) |
| `smallest_solution.kara` | a Rust solution as LeetCode's Rust users write it, `s.into_bytes()`, two `while` loops and `String::from_utf8(cs).unwrap()`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples; one 'a';
four 'a's; one 'b'; a run to the end after two 'a's; a run cut short by
an 'a'; and 5000 random words of 1 to 30 letters, an 'a' 1 time in 1 to
4, with the answers' letters summed and a checksum. `smallest.py`
mirrors the ★ arm and its output is byte-identical.

```
baabc
abaab
kddsbncd
z
aaaz
a
aayyy
aabadef
5000 words: letters sum to 511361, checksum 154700664
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every non-empty substring tried, each of its letters moved
back one, 'a' to 'z', and the least string kept, with no greedy run. It
draws 1000 random words of 1 to 8 letters, an 'a' 1 time in 1 to 4,
then 500 of 1 to 100 letters, an 'a' 1 time in 1 to 30, each with a
random word of 1 to 10 letters to put after it, all before any arm
answers; the literal reading is asked only of the first 1000.

| | property |
|---|---|
| P1 | up to 8 letters, the answer is the literal reading's |
| P2 | the answer is as long as the word and differs from it on one run of places, each letter there one back round the alphabet |
| P3 | a word with a letter other than 'a': the answer is less than it; a word of 'a's only: its last letter made 'z' |
| P4 | "a" put in front of a word with a letter other than 'a': "a" in front of the answer |
| P5 | "a" and a random word put after a word with a letter other than 'a': the same put after the answer |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1500 cases: checksum 869222217, 45000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases, the least over every substring, gives the
same checksum. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M4 and M10 fail the same checks: both leave a
word of 'a's with no 'z', one by writing a 'y' and one by never seeing
the word as all 'a's.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a word of 'a's has its first made 'z' | P1 229, P3 244, P6 244 |
| M2 | ★: only the run's first letter moved | P1 387, P6 823 |
| M3 | chars: the run looked for from the first 'a' | P1 1000, P2 1500, P3 1500, P4 241, P5 241, P6 1500 |
| M4 | chars: a word of 'a's ends in 'y' | P1 292, P2 309, P3 309, P6 309 |
| M5 | split: a run to the end stops one short | P1 273, P2 103, P3 103, P5 348, P6 348 |
| M6 | split: the leading 'a's dropped | P1 222, P2 281, P3 276, P4 1191, P6 281 |
| M7 | build: a later run moved too | P1 307, P2 711, P5 1137, P6 711 |
| M8 | build: the run kept as it was | P1 708, P2 1191, P3 1191, P6 1191 |
| M9 | solution: the run's first letter skipped | P1 708, P2 368, P3 368, P6 1191 |
| M10 | solution: the last 'a' never reached | P1 292, P2 309, P3 309, P6 309 |

## Benchmarks

The bench draws 100 words of `10^5` letters, each with up to `5 · 10^4`
'a's first and then letters with an 'a' 1 time in 5000, so that the run
moved back is long, all of them first, then answers each 20 times by the
★ arm in all five languages and counts the letters that changed. Every
implementation prints `100 words of 100000 letters, 20 rounds: letters
moved sum to 10743720, checksum 280524698`.

BENCHTAB

## Verification

All five arms print the same output as `smallest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★ arm's harness first summed `(b - b'a') as i64`; `karac check`
warns that a `u8` widens to `i64` by itself, and `karac fix` dropped the
casts. The build arm checked clean as first written. The chars arm
wrote Rust's `(letters[i] as u8 - 1) as char`, and `karac fix` made the
`char` to `u8` cast `as u32 as u8`, which Kāra asks for since a `char`
does not fit 8 bits.

The split arm wrote Rust's `s.find(|c| c != 'a')`. Kāra's `find` takes a
`Str` pattern, not a test, and `karac check` refused the closure with a
message older than that and no fix; that was kara `B-2026-11-20-140`,
fixed at `0d28296389`, and `karac fix` now writes the first letter that is
not an 'a' as `s.char_indices().find(..)` with `.map(|(i, _)| i)`.

LeetCode's Rust template took one `karac fix` of 10 edits, the wrapper
included: `struct Solution {}` added, `Vec<u8>` became `Vec[u8]`,
`s.into_bytes()` became `s.bytes().to_vec()`, `&&` became `and`,
`String::from_utf8` became `String.from_utf8`, and in the wrapper
`Solution::` became `Solution.` with the `.clone()` dropped.
