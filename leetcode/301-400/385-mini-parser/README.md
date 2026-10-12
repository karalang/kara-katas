# 385. Mini Parser

Given a string `s` that serializes a nested list, parse it and return
the deserialized `NestedInteger`. Each element is either an integer or a
list whose elements may also be integers or lists.

```
s = "324"                 -> the integer 324
s = "[123,[456,[789]]]"   -> a list of 123 and a list of 456 and a list of 789
```

**Constraints:** `1 <= s.len() <= 5 * 10^4`; `s` holds digits, `[`, `-`,
`,` and `]`; `s` is a valid serialization; every integer is in
`[-10^6, 10^6]`.

## Approaches

Every arm returns `enum NestedInteger { Int(i64), List(Vec[NestedInteger]) }`.

| file | mechanism | time | extra space |
|---|---|---|---|
| `mini_parser.kara` ★ | recursive descent: one function for a value, which reads either an integer or `[`, values separated by commas, `]`, moving one position forward through the bytes | O(n) | O(d) stack for d levels of nesting |
| `mini_parser_stack.kara` | an explicit stack of the lists still open: `[` opens one, a number goes into the top one, `]` closes it into the one below | O(n) | O(d) |
| `mini_parser_tokens.kara` | split the string into open, close and number tokens first, then build the value from the tokens | O(n) | O(n) for the tokens |
| `mini_parser_split.kara` | strip a list's brackets, cut the inside at the commas no inner list encloses, and parse each piece the same way | O(n * d) | O(n) |
| `differential.kara` | the four parsers against values whose shape is known by construction, 2,000 random values, five properties | — | — |

Every arm prints the same 10 lines: the two LeetCode examples and seven
edge cases (an empty list, a negative integer, 0, a list with empty
lists in it, five levels of nesting, the extremes +-10^6, a tree of
empty lists), each serialized back with its depth, number of integers
and sum, then how many of 2,000 random values nested up to 6 deep
serialize back to the string they were parsed from, with a checksum.
`mini_parser.py` mirrors the ★ arm and its output is byte-identical.

The stack and splitting arms read their numbers with `i64.parse(piece)`.
They were first written with `piece.parse_int()`, which does not exist.
The Rust spelling, `piece.parse()`, works on a `String` receiver where
an `Option[i64]` is expected. The pieces here are `Str` values, though,
and on a `Str` receiver `karac check` refuses it, naming the type as
`String` and giving no hint; see Compiler findings.

## Differential

`differential.kara` holds copies of the four arms as
`deserialize_descent`, `deserialize_stack`, `deserialize_tokens` and
`deserialize_split`. It builds 2,000 random values nested up to 6 deep,
with integers leaning to the edges (0, one digit, +-10^6 and anything
between), keeping the depth, number of integers and sum it built.

| | property |
|---|---|
| P1 | every parser's value serializes back to the string it was given |
| P2 | every parser finds the depth, number of integers and sum the generator built |
| P3 | all four parsers agree |
| P4 | `[` + a value + `]` parses to a list of one item, that value |
| P5 | `[` + one value + `,` + another + `]` parses to a list of those two items |

It prints `2000 values, 40000 checks, 0 failures` under
`karac __mir-run`.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | how |
|---|---|---|
| M1 | descent: ignores the minus sign | P1 to P5, 9767 failures |
| M2 | descent: no special case for an empty list | P1 to P5, 7072 failures |
| M3 | descent: keeps only the last 6 digits | P1 to P5, 5941 failures |
| M4 | stack: stops at the first list that closes inside another | P1 to P5, 5360 failures |
| M5 | stack: a closed inner list is dropped | P1 to P5, 5360 failures |
| M6 | tokens: ignores the minus sign | P1 to P5, 7101 failures |
| M7 | split: the last item is dropped | P1 to P5, 6841 failures |
| M8 | split: items before the last go to the front | P1, P3, P4 and P5, 3304 failures |

M3 changes only the integers +-10^6, the only ones with 7 digits; the
generator leans to the edges so that they come up often. M4 and M5 give
the same counts: stopping at the first inner list that closes and
dropping every inner list both lose the same lists whenever a value
has one.

## Verification

All four arms print the same output as `mini_parser.py` under
`karac __mir-run` (the v2 MIR interpreter), and `karac check` passes on
every file. Every file also prints the same output under
`karac __mir-llvm-run` (the same MIR compiled to LLVM), since compiler
commit 62f5f6de04 added the `String.as_str` native. The descent, stack
and tokens arms also match under `karac run --interp`. The legacy
backends fail as Compiler findings describes.

## Benchmarks

The bench program uses the ★ arm. It builds one serialized value of
49,038 bytes (the problem allows 50,000) once, a list of random values
nested up to 5 deep, then parses it 2,000 times; each parse is walked
for its depth, number of integers and sum, folded into a checksum. The
Kāra program under `karac __mir-run` and the C, Rust, Go and Python
mirrors all print
`49038 bytes parsed 2000 times, checksum 394674954`. Spot timings on a
shared 4-core container (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| Rust (`rustc -O`) | 0.80 s |
| C (`clang -O3`) | 1.35 s |
| Go | 2.2 s |
| Python | 23 s |
| Kāra, `karac __mir-run` (the MIR interpreter) | 3 min 22 s |

The Kāra program also prints the same line under
`karac __mir-llvm-run` in 4.0 s, compile included; that JITs the MIR's
IR without optimization passes, so it is not a benchmark. The legacy
native build stops in codegen.

## Compiler findings

- **`.parse()` on a `Str` is refused** (kara `B-2026-10-12-5`).
  `let n: Option[i64] = s.parse();` checks and runs when `s` is a
  `String`, but when `s` is a `Str` parameter or a slice `s[a..b]`,
  `karac check` and `karac __mir-run` refuse it with
  `no method 'parse' on type 'String'`, which names the wrong type and
  gives no hint. `i64.parse(s)` works on both.

Two failures in the legacy backends, which are frozen, so not filed:

- **Legacy codegen has no `bytes` on a `Str` parameter.** LLJIT,
  `karac build` and `KARAC_AUTO_PAR=1 karac build` stop with `no handler
  for method 'bytes' on variable 's'` on the descent, stack and tokens
  arms and on the bench program.
- **The legacy typechecker takes a slice of a `Str` for a move out of
  an index.** `karac run --interp` and LLJIT refuse the splitting
  arm's `s[start..i]` and the differential with
  `E_INDEX_MOVE_NON_COPY: cannot move out of an index expression`.
  `karac check` and the MIR interpreter accept both.
