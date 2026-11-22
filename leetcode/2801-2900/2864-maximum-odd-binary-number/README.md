# 2864. Maximum Odd Binary Number

You are given a **binary** string `s` that contains at least one `'1'`.

You have to **rearrange** the bits in such a way that the resulting
binary number is the **maximum odd binary number** that can be created
from this combination.

Return *a string representing the maximum odd binary number that can be
created from the given combination.*

**Note** that the resulting string **can** have leading zeros.

```
s = "010"   ->  "001"
s = "0101"  ->  "1001"
```

**Constraints:** `1 <= s.length <= 100`; `s` consists only of `'0'` and
`'1'`; `s` contains at least one `'1'`.

## Approaches

| file | mechanism |
|---|---|
| `odd.kara` ★ | an odd number ends in a one, and the largest arrangement of the rest puts every other one first: the ones less one, then the zeros, then the last one, by `repeat` and `+` |
| `odd_sorted.kara` | the characters sorted largest first with `sort_by`, which puts every one before every zero, then the last one moved to the end with `rposition`, `remove` and `push` |
| `odd_swap.kara` | in place over the bytes: one pointer walks the string and swaps every one it meets to the front, as a partition does, then the last of the front ones trades places with the final byte |
| `odd_build.kara` | built a character at a time: one pass counts the ones, then each place from the left takes a one while more than one is left to place, else a zero, and the final place takes the kept one |
| `odd_solution.kara` | a Rust solution as LeetCode's Rust users write it: `s.bytes().filter(\|&b\| b == b'1').count()`, then `"1".repeat(cnt - 1) + &"0".repeat(s.len() - cnt) + "1"`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's two examples and a lone
one; 100 bits, LeetCode's most, all ones and then one one at the front;
then 3000 random strings of 1 to 8 bits and 3000 of up to 100, each
with at least one one, as a count of ones and a checksum of the
answers' bytes. `odd.py` mirrors the ★ arm and its output is
byte-identical.

```
001 1001 1
true true
3000 short strings: 6413 ones, checksum 225129521
3000 long strings: 51974 ones, checksum 471568563
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every string of n bits with as many ones as s, written
as a number, the odd ones kept, and the largest taken. It draws 2000
random strings of 1 to 8 bits, then 50 of up to 100, each with at least
one one, all before any arm answers; the literal reading, which tries
2^n numbers, is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 8 bits, the answer is the literal reading's |
| P2 | as long as s, as many ones, and ending in a one |
| P3 | s reversed: the same answer |
| P4 | a zero added to s: the answer with a zero before its last bit |
| P5 | a one added to s: a one put before the answer |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, 5139 ones: checksum 277609166,
61500 checks over 5 arms: 0 failures` under every lane in Verification,
and a Python reading of the same cases gives the same checksum. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. A first draft of M5 crashed with an index out
of bounds before any property was asked, and was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the zeros put before the ones | P1 1147, P4 1327, P5 1655, P6 1195 |
| M2 | ★: every one kept at the front | P1 1606, P2 1655, P4 2050, P6 1655 |
| M3 | sorted: the bits sorted smallest first | P1 1147, P4 1327, P5 1655, P6 1195 |
| M4 | sorted: the last zero moved, not the last one | P1 1606, P2 1655, P4 2050, P6 1655 |
| M5 | swap: the ones left where they are | P1 1296, P2 882, P3 1429, P4 1154, P5 1655, P6 1345 |
| M6 | swap: the first front one sent to the end | P1 1147, P4 132, P5 1655, P6 1195 |
| M7 | build: a one placed while one is left | P1 1606, P2 1655, P4 395, P6 1655 |
| M8 | build: the last place given a zero | P1 2000, P2 2050, P4 2050, P6 2050 |
| M9 | solution: one one too few at the front | P1 2000, P2 2050, P4 2050, P6 2050 |
| M10 | solution: the zeros counted as ones | P1 1586, P2 1636, P4 1655, P5 2050, P6 1636 |

## Benchmarks

The bench draws 10^4 strings of 100 bits, LeetCode's most, about a third
of them ones and at least one, all of them first, then answers each 50
times by the ★ arm in all five languages, folding every answer into the
checksum byte by byte, so the fold costs about as much as the answer;
C allocates each answer, as the other languages' strings are. Every
implementation prints `10000 strings of 100, 50 rounds: 17027150 ones,
checksum 846517534`.

BENCHTAB

## Verification

All five arms print the same output as `odd.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The harness, as first written, folded the checksum over `s.bytes()`
directly, and `karac check` reported E0236: iterator adaptors need an
explicit `.iter()` in Kāra; `karac fix` wrote `s.bytes().iter().fold`.
The four own arms checked clean.

LeetCode's Rust template took 6 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`;
`s.bytes().filter` took `.iter()`, as the harness did, and `|&b|` lost
its `&`; `&"0".repeat(..)` lost its `&`; `&str` became `Str`, and `Solution::` took
`.`. `b'1'` and `"1".repeat(cnt - 1)` were accepted as written.
