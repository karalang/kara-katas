# 816. Ambiguous Coordinates

A two-dimensional coordinate such as `"(1, 3)"` or `"(2, 0.5)"` had its
commas, points and spaces removed, leaving a string `s` such as `"(13)"`
or `"(205)"`. Return every coordinate it could have been, in any order.
The original numbers never had extra zeros: no `"00"`, `"0.0"`,
`"0.00"`, `"1.0"`, `"001"` or `"00.01"`, and no number like `".1"` with
no digit before its point. A coordinate is written with a comma and one
space, `"(x, y)"`.

```
s = "(123)"    ->  ["(1, 2.3)", "(1, 23)", "(1.2, 3)", "(12, 3)"]
s = "(0123)"   ->  ["(0, 1.23)", "(0, 12.3)", "(0, 123)", "(0.1, 2.3)", "(0.1, 23)", "(0.12, 3)"]
s = "(00011)"  ->  ["(0, 0.011)", "(0.001, 1)"]
```

**Constraints:** `4 <= s.length <= 12`, `s[0] == '('`, `s[s.length - 1]
== ')'`, and the rest of `s` is digits.

## Approaches

Every coordinate puts its comma in one of the gaps between the digits
and at most one point in each half. A half spells a number when its
whole part has no leading 0, unless it is just `"0"`, and its fraction,
if any, has no trailing 0.

| file | mechanism |
|---|---|
| `ambiguous_coordinates.kara` ★ | cut the digits at every gap and pair every number the left part spells with every number the right part spells; a part spells a number for each place to put its point, or none, that passes the test. O(n^3) candidates for n digits |
| `ambiguous_coordinates_rules.kara` | the same cuts, but a part's numbers come from its first and last digit alone: one digit is itself; 0 at both ends spells nothing; a leading 0 spells only `"0."` and the rest; a trailing 0 spells only the part; any other part spells itself and itself with a point after each digit but the last |
| `ambiguous_coordinates_canon.kara` | put the comma and a point in each half every way, and keep a half when it is exactly how its value prints at its shortest: the extra zeros the statement rules out are what the shortest form leaves out |
| `ambiguous_coordinates_iter.kara` | one `filter_map` over every triple of comma and two points, keeping those whose halves both pass the ★ arm's test |
| `differential.kara` | the four arms against every way to put back a comma and points, four properties |

The answer may come in any order, so every arm's output is sorted before
it is printed or compared. Every arm prints the same 14 lines:
LeetCode's three examples; `(100)`, `(00)`, `(000)` with no coordinate
at all, `(10)`, `(1010)` and `(0010)`; LeetCode's longest, ten digits,
as `(1234567891)` with 165 coordinates, a 1 followed by nine 0s and the
reverse, one coordinate each, and `(1010101010)`, each with a count and
a checksum; and 300 random rounds of 2 to 10 digits, with a total and a
checksum. `ambiguous_coordinates.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement
played out on strings: put the comma in one gap and points in any set of
the other gaps, `2^(n-2)` sets for each of the n - 1 commas, and keep
each coordinate whose two halves have at most one point, digits on both
sides of it, no 0 leading a whole part longer than `"0"` and no 0 ending
a fraction. Its 1,600 cases have 2 to 10 digits and come in four kinds
of 400: any digits; a 0 one time in two; a 0 four times in five; and
only 0s and 1s. 166 cases have no coordinate at all, and the most any
case has is 165.

| | property |
|---|---|
| P1 | the statement's list, both sorted |
| P2 | each coordinate gives back the digits with its comma, points and space taken out |
| P3 | no coordinate twice |
| P4 | as many coordinates as the parts' spellings multiply to, summed over the cuts, each part's count read off its ends as in the rules arm |

It prints `1600 cases (166 with no coordinates, at most 165), 25600
checks over 4 arms: 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a whole part of just 0 refused | P1 1170, P4 1170 |
| M2 | ★: a fraction ending in 0 allowed | P1 1145, P4 1145 |
| M3 | ★: the comma never after the first digit | P1 1203, P4 1203 |
| M4 | rules: a part from 0 to 0 not ruled out | P1 781, P4 781 |
| M5 | rules: a part led by 0 taken whole | P1 727 |
| M6 | rules: no point after the first digit | P1 781, P4 781 |
| M7 | shortest form: one trailing 0 kept | P1 970, P4 970 |
| M8 | shortest form: no 0 before the point | P1 727, P4 727 |
| M9 | shortest form: the left number always has a point | P1 1339, P4 1339 |
| M10 | iter: the left number always has a point | P1 1339, P4 1339 |
| M11 | iter: a whole part of just 0 refused | P1 1170, P4 1170 |
| M12 | iter: the comma never after the first digit | P1 1203, P4 1203 |

P1 kills all twelve and P4 all but M5, which swaps `"0.12"` for `"012"`
one for one and so keeps every count. P2 and P3 kill none: every edit
still writes the digits in order and lists each candidate once, and the
two properties are there to catch an arm that garbles or repeats, which
none of these edits does. The pairs that fail on the same cases make the
same mistake by different code: M1 and M11 refuse every `"0"`, M3 and
M12 lose the cuts after one digit, M9 and M10 lose the left numbers with
no point, and M5 and M8 both lose `"0.x"`, one by writing it `"0x"` and
one by taking its shortest form to be `".x"`.

## Verification

Every arm prints the same output as `ambiguous_coordinates.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` is at kara
`d0ad6409f5`, whose last compiler change is `c120cafada`; the release
build that runs `check` and `__mir-run` is at `f6f2efb14`, one parser
change behind it. The runtime archives were built after the last runtime
change in that tree, `45d6c491fc`.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`) prints the same
output for the rules and shortest-form arms; the legacy JIT (`karac
run`) and `karac build` refuse both in codegen, finding no handler for
`len` on a `Str` parameter. Legacy refuses the ★ and iterator arms, the
differential and the bench program in every lane, reading a slice such
as `part[0..point]` bound with `let` as moving a `StringSlice` out of an
index (`E_INDEX_MOVE_NON_COPY`). Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 strings of 10
digits, LeetCode's longest, a 0 one time in four, are drawn once. Each
of 400,000 rounds sets one digit of the next string afresh and lists its
coordinates, folding the length of each into a checksum, so the work is
building strings: every number of every part and every coordinate is a
fresh string, with 55 coordinates a round on average. Every
implementation prints `400000 rounds of 10 digits: 22013630 coordinates,
checksum 649696706`, the Kāra program under `karac __mir-run` included,
in 178 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 2.24 to 2.50 s |
| Rust (`rustc -O`) | 3.39 to 3.60 s |
| Rust (`rustc -O -C overflow-checks=on`) | 3.38 to 3.71 s |
| Go | 6.83 to 7.87 s |
| Python | 13.12 to 13.81 s |
| Kāra (`karac build --mir`) | 2.19 to 2.44 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 8.9 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 2.30 s,
against C's 2.29, Rust's 3.47 (3.46 under overflow checks) and Go's
7.25. Under valgrind's cachegrind v2 runs 24.0 billion instructions, C
27.6 billion and Rust 41.2 billion. C writes each coordinate with
`snprintf` and Rust with `format!`, both through a general formatting
routine, which most likely accounts for their extra instructions over
v2's f-string (not traced); 7% of Rust's indirect branches are
mispredicted, against under 1% of v2's. Built for `x86-64-v3`, the
target `karac build` uses, C (`clang -O3 -march=x86-64-v3`) takes 1.97
to 2.16 s and runs the same 27.6 billion instructions, and Rust with
overflow checks (`-C target-cpu=x86-64-v3`) 3.19 to 3.30 s, against v2's
2.03 to 2.23 s in the same five interleaved runs. Legacy refuses the
bench program (see Verification), so there is no legacy timing to set v2
against. The comparison with C and Rust waits until after M4.

## Compiler findings

The iterator arm was first written with the cut as a `flat_map` and, for
each cut, every left number paired with every right one by a second
`flat_map` with a `map` inside it. `karac check` and the MIR borrow
checker refuse it: the inner `map` closure reads the middle closure's
`String` parameter `x` and the outer closure's `cut`, and lives on
inside the iterator the middle closure returns, but is given both by
`ref` (E0516 and E0509). core-semantics.md §9.1 moves in a captured
place that dies while the closure is still live, whatever its type. That
is B-2026-10-20-34, filed for kata 812's `Copy` case and widened by this
kata to a non-`Copy` one. The arm is now one `filter_map` over every
triple of comma and two points, right on every v2 surface; it goes back
to the nested `flat_map` once the row is fixed. A pattern `let (mut n,
mut k) = ..` in the shortest-form arm is refused by `karac check` with a
diagnostic naming the Kāra spelling, `let mut (n, k) = ..`.
