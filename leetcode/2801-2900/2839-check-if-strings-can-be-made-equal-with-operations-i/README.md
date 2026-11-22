# 2839. Check if Strings Can be Made Equal With Operations I

You are given two strings `s1` and `s2`, both of length `4`, consisting
of **lowercase** English letters.

You can apply the following operation on any of the two strings **any**
number of times:

- Choose any two indices `i` and `j` such that `j - i = 2`, then
  **swap** the two characters at those indices in the string.

Return `true` *if you can make the strings* `s1` *and* `s2` *equal, and*
`false` *otherwise*.

```
s1 = "abcd", s2 = "cdab"  ->  true
s1 = "abcd", s2 = "dacb"  ->  false
```

**Constraints:** `s1.length == s2.length == 4`; `s1` and `s2` consist
only of lowercase English letters.

## Approaches

| file | mechanism |
|---|---|
| `equal.kara` ★ | a swap two apart never moves a letter between the even and odd places, and each pair can be swapped or not, so the even places hold the same two letters either way round, checked by a closure, and so do the odd ones |
| `equal_reach.kara` | every string s1 can reach: the swap at 0 and 2 made or not and the one at 1 and 3 made or not, by a two-bit mask over a `Vec[u8]`, any of the four equal to s2 |
| `equal_count.kara` | letter counts by parity of place in one table of 2 x 26, each s1 letter counted up and each s2 letter down, all back to zero |
| `equal_sorted.kara` | each string's even and odd letters pulled out with `step_by` and `skip`, sorted, and joined into a `(String, String)` key; the strings match when the keys do |
| `equal_solution.kara` | a Rust solution as LeetCode's Rust users write it: the strings as `as_bytes()` slices and a closure over `usize` places that checks one pair either way round, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 3 lines: LeetCode's two examples and a word
against itself; then every pair of four-letter words over a, b and c,
81 x 81, and 20000 random pairs over all 26 letters, half of them the
first word with one pair swapped, as counts and checksums. `equal.py`
mirrors the ★ arm and its output is byte-identical.

```
true false true
6561 pairs over abc: 225 true, checksum 786817866
20000 random pairs: 10112 true, checksum 494471378
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every string s1 reaches by swaps two apart, found by a
search to a fixed point over a `Set[String]`, and whether s2 is among
them. It draws 2000 pairs of words over a, b and c, then 50 over all 26
letters: a third of the second words random, a third the first with
random swaps made, and a third that with one letter changed too, all
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | s1 and s2 the other way round: the same answer |
| P3 | s1 against itself: true |
| P4 | every letter of both moved on one, z to a: the same answer |
| P5 | both words reversed: the same answer |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, 923 true: checksum 633220624,
61500 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python reading of the same cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the even pair only in the order given | P1 531, P6 531 |
| M2 | ★: the odd places never compared | P1 294, P5 665, P6 294 |
| M3 | reach: the odd swap never tried | P1 315, P5 416, P6 315 |
| M4 | reach: the swap made across parities | P1 342, P2 8, P5 429, P6 342 |
| M5 | count: one table for both parities | P1 923, P3 2050, P6 923 |
| M6 | count: s2 counted up too | P1 923, P3 2050, P6 923 |
| M7 | sorted: the odd letters left unsorted | P1 315, P5 416, P6 315 |
| M8 | sorted: the odd letters taken from the start | P1 294, P5 665, P6 294 |
| M9 | solution: the pairs read as 0 with 1 and 2 with 3 | P1 524, P6 524 |
| M10 | solution: either pair enough | P1 665, P6 665 |

## Benchmarks

The bench draws 10^6 pairs of four-letter words over a to d, half the
second words the first with its even pair swapped, all of them first,
then answers each 20 times by the ★ arm in all five languages. Kāra,
Rust, Go and Python collect each word's letters into a vector on every
call, as the ★ arm does; C reads the bytes in place. Every
implementation prints `1000000 pairs, 20 rounds: 10126040 true,
checksum 128355298`.

BENCHTAB

## Verification

All five arms print the same output as `equal.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The harness, as first written, spelt a word's letters with
`letters.pow(i)` for `i` from a range, and `karac check` reported
E0200, "pow expects an exponent of type `u32`, got `i64` (cast with
`as u32`)", in every arm; `karac fix` added the `as u32`, as Rust also
wants. The counting arm's `(c - b'a') as i64` drew W0310, the `u8`
widening to `i64` by itself as an index, and `karac fix` took the casts
out. The other arms checked clean.

LeetCode's Rust template took 10 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`;
`as_bytes()` became `bytes()`; `&&` and `||` became `and` and `or`;
`&str` became `Str`, and `Solution::` took `.`. The closure's `usize`
parameters were accepted as written.
