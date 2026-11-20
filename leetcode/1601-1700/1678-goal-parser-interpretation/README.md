# 1678. Goal Parser Interpretation

You own a **Goal Parser** that can interpret a string `command`. The
`command` consists of an alphabet of `"G"`, `"()"` and/or `"(al)"` in
some order. The Goal Parser will interpret `"G"` as the string `"G"`,
`"()"` as the string `"o"`, and `"(al)"` as the string `"al"`. The
interpreted strings are then concatenated in the original order.

Given the string `command`, return *the **Goal Parser**'s interpretation
of* `command`.

```
command = "G()(al)"          ->  "Goal"
command = "G()()()()(al)"    ->  "Gooooal"
command = "(al)G(al)()()G"   ->  "alGalooG"
```

**Constraints:** `1 <= command.length <= 100`; `command` consists of
`"G"`, `"()"`, and/or `"(al)"` in some order.

## Approaches

| file | mechanism |
|---|---|
| `interpret.kara` ★ | one pass over the bytes: a `G` is itself, a `(` followed by `)` is `o`, any other `(` starts `(al)`, which is `al`; each token is stepped over whole. O(n) |
| `interpret_replace.kara` | `command.replace("()", "o").replace("(al)", "al")`; the two patterns cannot overlap. O(n) |
| `interpret_chars.kara` | every letter kept (`G`, `a`, `l`), and an `o` for each `)` that comes right after a `(`; the other parentheses dropped. O(n) |
| `interpret_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `match` on the bytes of `as_bytes()` with `b'G'` and a guard on `b')'`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's three examples and one
command of each token alone; then the letters of the answers summed and
a checksum of every answer for 3000 random commands of up to 10 tokens,
300 of up to 50 and 30 of up to `10^4`. `interpret.py` mirrors the ★ arm
and its output is byte-identical.

```
Goal
Gooooal
alGalooG
G
o
al
3000 commands of up to 10 tokens: 21954 letters, checksum 283533559
300 commands of up to 50 tokens: 10254 letters, checksum 541218429
30 commands of up to 10000 tokens: 204627 letters, checksum 821958450
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the command is read from the front, and whichever of the
three tokens it starts with there is replaced by its interpretation, in
order. It checks 3000 random commands of 1 to 12 tokens. Every case is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the command twice gives the answer twice |
| P3 | the answer holds no parenthesis, and as many `G`s as the command |
| P4 | the answer read back (`o` as `()`, `al` as `(al)`) gives the command |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 742618424, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement gives the same checksum. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. A first M1 read `(a` as the start of
`()`; the walk then stepped two bytes into the middle of `(al)` and
indexed past the end, so it stopped on both backends before any check,
and it was replaced by one that the properties see. An `o` for a `)`
after any letter but `l` would be no mutation at all, since a `)` only
ever follows `(` or `l`; M6 adds `l` instead.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a `G` read as `o` | P1 2535, P3 2535, P4 2535, P5 2535 |
| M2 | ★: `(al)` read as `la` | P1 2496, P4 2496, P5 2496 |
| M3 | ★: `()` read as `O` | P1 2486, P4 2486, P5 2486 |
| M4 | replace: `()` dropped | P1 2486, P4 2486, P5 2486 |
| M5 | replace: `al)` replaced, the `(` left | P1 2496, P3 2496, P4 2496, P5 2496 |
| M6 | chars: an `o` also for the `)` after `l` | P1 2496, P4 2496, P5 2496 |
| M7 | chars: the previous character never kept | P1 2486, P4 2486, P5 2486 |
| M8 | chars: a `(` kept | P1 2864, P3 2864, P4 2864, P5 2864 |
| M9 | solution: a `G` written `g` | P1 2535, P3 2535, P4 2535, P5 2535 |
| M10 | solution: `(al)` read as `a` | P1 2496, P4 2496, P5 2496 |

## Benchmarks

The bench draws 100000 random commands of up to 100 characters,
LeetCode's longest, all of them first, then interprets each 20 times by
the ★ arm in all five languages, each building a new string per answer.
Every implementation prints `100000 commands, 20 rounds: 56766200
letters, checksum 987952233`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.328 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.339 s |
| Kāra (`karac build`) | 0.342 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.344 s |
| Rust (`rustc -O`) | 0.349 s |
| Go | 0.407 s |
| Python | 4.3 s |

The sequential Kāra build is level with Rust and level with Rust with
overflow checks on, the equal-safety comparison (BENCHMARKS.md). C is
the fastest here at 0.328 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.343 s and 0.354 s on one
run).

## Verification

All four arms print the same output as `interpret.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ arm's first draft took the bytes with Rust's `command.as_bytes()`;
`karac check` named Kāra's `.bytes()`, a `Slice[u8]`, and `karac fix`
wrote it. The replace and chars arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 3 edits:
`struct Solution {}` added, `as_bytes()` written `bytes()`, and
`String::new` written `String.new`; the `b'G'` byte literals and the
`match` guard carried over as written.

The differential's P3 first asked `got.contains('(')`, a `char` pattern
as Rust takes; Kāra's `contains` takes a `Str`, and `karac fix` wrote
`"("`. The bench first bound `let token = tokens[..]` from the list of
literals, a move out of an index of `String`s (E_INDEX_MOVE_NON_COPY),
and gave a byte `as i64` that widens by itself; `karac fix` wrote
`ref tokens[..]` and dropped the cast. `arm_name` in the differential
indexes a list of string literals for a `Str`, as #1662's does (B-2026-11-19-131).
