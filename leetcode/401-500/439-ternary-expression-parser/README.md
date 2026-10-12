# 439. Ternary Expression Parser

Given a string holding arbitrarily nested ternary expressions, evaluate
it and return the result. The expression holds only digits, `'T'`,
`'F'`, `'?'` and `':'`; every number is a single digit; and ternaries
group right to left, as in most languages. The value of a condition is
always `'T'` or `'F'`, and the result is a digit, `'T'` or `'F'`.

```
"T?2:3"        ->  "2"
"F?1:T?4:5"    ->  "4"     (F ? 1 : (T ? 4 : 5))
"T?T?F:5:3"    ->  "F"     (T ? (T ? F : 5) : 3)
```

**Constraints:** `5 <= expression.length <= 10^4`; the expression is
valid.

## Approaches

Every arm is `fn parse_ternary(expression: Str) -> char`: the result is
one character, so the arms return it as a `char` rather than a
one-character `String`.

| file | mechanism |
|---|---|
| `parse_ternary.kara` ★ | a stack, scanning from the right: a character whose right-hand neighbour is `'?'` is a condition, and when one arrives the stack holds `'?'`, the yes value, `':'` and the no value on top, already reduced, so the condition replaces those four with the one it picks. O(n) |
| `parse_ternary_recursive.kara` | recursive descent from the left: reading an expression returns its value and the index just past it, so the no branch starts one past the end of the yes branch. O(n), with recursion as deep as the nesting |
| `parse_ternary_skip.kara` | a short-circuit walk from the left: `T` steps into the yes branch, and `F` skips the yes branch to the `':'` that closes its `'?'`, counting the pairs nested inside it. No stack and no recursion; O(n) |
| `parse_ternary_rewrite.kara` | the plain reference: the rightmost `'?'` always heads a ternary whose branches are single characters, so overwrite its condition with the branch it picks, remove the four characters after it, and move left to the next `'?'`. O(n^2) |
| `differential.kara` | the four arms on 1,500 random expressions, five properties |

Every arm prints the same 9 lines: the three LeetCode examples, five
edge cases (a letter as the result, a condition nested in a no branch,
a chain of eight conditions nested to the right, a chain of five nested
to the left, and nesting on both sides), and for 300 random expressions
of 1 to 10 levels the total length, how many values are digits, `T`
and `F`, and a checksum of the values. `parse_ternary.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random expressions of 1 to 10 levels, each branch a lone
character with chance 1 in 3. The generator knows the value of what it
builds, and where that value comes from.

| | property |
|---|---|
| P1 | the value is the one the generator chose as it built the expression |
| P2 | `"T?e:f"` and `"F?f:e"` have the value of `e`, for a random `f` |
| P3 | putting `f` in place of the leaf the value comes from gives `f`'s value, and in place of any other leaf changes nothing |
| P4 | the mirror image, every condition flipped and its branches swapped, has the same value |
| P5 | k conditions nested to the right pick the branch of the first `T` (the last leaf when none is `T`), and k `T` conditions nested to the left pick the innermost yes value |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | stack: every condition read the wrong way round | P1 1359, P2 1369, P3 1409, P5 1500 |
| M2 | stack: an `F` condition reduces to `F` | P1 976, P2 416, P3 1215, P4 817, P5 1344 |
| M3 | recursive: the yes branch's first character is read as the condition | P1 1083, P2 958, P3 1317, P4 1242, P5 1500 |
| M4 | recursive: a ternary ends where its yes branch ends | P1 631, P2 1174, P3 1006, P4 1011 |
| M5 | skip: an `F` skips to the first `':'`, ignoring nesting | P1 631, P2 1174, P3 1006, P4 1011 |
| M6 | skip: an `F` returns the last character of its yes branch | P1 971, P2 1374, P3 1227, P4 1358, P5 1247 |
| M7 | rewrite: an `F` condition also takes the yes branch | P1 983, P2 1388, P3 1227, P4 1358, P5 1247 |
| M8 | rewrite: the no value is left behind | P1 677, P2 1058, P3 1040, P4 1010 |

P4 cannot see M1: a parser that reads every condition backwards gets
the mirror image's value wrong in exactly the same way. P5's chains
never nest a ternary inside a yes branch that an `F` has to skip, so
the three mutants that only go wrong there (M4, M5, M8) pass it. M4 and
M5 are one mutant written two ways, so their counts agree on every
property: ending a ternary where its yes branch ends makes every
enclosing yes branch end at the first `':'` inside it, which is where
M5's skip stops. P3 was first a relabelling of the
digits, which no mutant could fail, since no arm treats one digit
differently from another; it was replaced by the substitution, which
fails every one.

## Verification

All four arms print the same output as `parse_ternary.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends:

- `karac run --interp` prints the eight fixed cases right in every arm
  but a different random section (`20448 characters: 293 digits, 1 T,
  6 F, checksum 116616683`): from the same seed it builds different
  random expressions, already different at the first one's yes leaf
  (`T?6:...` where the MIR backends and Python build `T?5:...`).
- LLJIT and `karac build` stop in the legacy code generator, which has
  no `bytes()` on a `Str` parameter.
- The differential does not typecheck: the legacy checker reads a
  range slice of a `Str`, `expression[0..at]`, as a move out of an
  index (`E_INDEX_MOVE_NON_COPY`).

Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 200 random expressions of
exactly 2,499 ternaries (9,997 characters, the problem's limit), each a
random split of the ternaries below the root between its two branches,
then evaluates every one 20 times over, folding the round into the
checksum. Every implementation prints `200 expressions of 9997
characters, 20 rounds: 3300 digits, checksum 376816918`, the Kāra
program under `karac __mir-run` included. The C time grows in step
with the number of rounds (0.02 s for one, 0.70 s for 80), so the
optimizer does not lift the evaluation out of the loop.

The mirrors keep the ★ arm's structure: each evaluation grows its own
stack, a `Vec<u8>` in Rust and a slice in Go. C allocates the stack at
the expression's length once per evaluation. Spot timings on a shared
4-core container, three runs each (`bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.18 to 0.20 s |
| Rust (`rustc -O`) | 0.15 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.15 to 0.17 s |
| Go | 0.21 to 0.22 s |
| Python | 3.2 to 3.7 s |

The frozen legacy `karac build` cannot build the program (see
Verification), so there is no legacy time. The Kāra program prints the
same line under `karac __mir-llvm-run` in 3.1 s, compile included; that
JITs the MIR's IR without optimization passes, so it is not a
benchmark.

## Compiler findings

No new findings. Two first drafts were wrong, not the compiler: the
recursive arm took the bytes as a `Vec[u8]` and the rewrite arm called
`split_off` and `append`, but `Str.bytes()` is a `Slice[u8]` and the
library's `Vec` has neither method; `karac check` and `karac __mir-run`
both said so.
