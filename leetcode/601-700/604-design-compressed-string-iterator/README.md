# 604. Design Compressed String Iterator

Design an iterator over a compressed string, given as letters each
followed by a positive count of how many times it stands in the original
string. `next()` returns the next letter of the original string, or a
space once there are none left; `hasNext()` returns whether any letter
is left.

```
StringIterator("L1e2t1C1o1d1e1")
next, next, next, next, next, next, hasNext, next, hasNext
->  L, e, e, t, C, o, true, d, true
```

**Constraints:** the compressed string has 1 to 1,000 characters, upper
and lower case English letters and digits; each count is from 1 to
10^9; at most 100 calls are made to `next` and `hasNext`.

## Approaches

Every arm is a `struct StringIterator` with `fn new(compressed: Str) ->
StringIterator`, `fn next(mut ref self) -> char` and `fn has_next(self)
-> bool`.

| file | mechanism |
|---|---|
| `string_iterator.kara` ★ | the text as characters, a position in it, the letter in hand and how many of it are left; `next` reads the next letter and its count only when the one in hand runs out, so a count of 10^9 costs nothing until it is reached; O(1) a call, plus each count's digits once |
| `string_iterator_runs.kara` | the text parsed once into runs, a letter and a count each, and the run in use with how many of it are used; O(n) to build, O(1) a call |
| `string_iterator_search.kara` | the runs' letters and running totals, and the number of letters given out; the next letter is that of the first run whose total passes it, by binary search; O(n) to build, O(log n) a call |
| `string_iterator_expand.kara` | since at most 100 calls are made, the first 100 letters written out, a longer text stopping there with a note that more is left; O(n + 100) to build, O(1) a call |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 10 lines: the example above; six more
(`a2b1` and `Q1` with calls past the end, `a12B3` and `x10y1` with
counts of two digits, `k100` with `hasNext` between the calls, and
`a1A1a1`, one letter in both cases); `z1000000000` with 99 calls of
`next` and then `hasNext`; `a1b1...z1` and calls past its end; and a
count and checksum over 300 random texts and calls. `string_iterator.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: the text written out in full, every letter
as many times as its count says, and a position in it; `next` gives the
letter at the position and moves on, or a space past the end, and
`hasNext` says whether the position is before the end. Each of
1,000 random cases has 1 to 6 runs of the letters `a`, `b` and `A`, so
that a letter often follows itself, with counts from 1 to 12, and 1 to
60 calls, two in three of them `next`; in 440 of them the calls go past
the end.

| | property |
|---|---|
| P1 | the results are the definition's |
| P2 | a `hasNext` put in at a random place changes none of the other results |
| P3 | the first run of two or more split in two runs of the same letter changes nothing |
| P4 | two iterators on one text, called in turn, each give what one alone would |
| P5 | with a short text in front, once its letters are all taken, the rest is an iterator on the text that follows |

It prints `1000 cases (440 going past the end), 4 arms, 20000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `hasNext` blind to the letter in hand | P1 406, P3 57 |
| M2 | ★: a count read as its last digit | P1 418, P3 147 |
| M3 | runs: each run given once too often | P1 781, P3 714, P5 917 |
| M4 | runs: a count's digits added, not shifted | P1 443, P3 74 |
| M5 | search: the run whose total reaches the count given, not passes it | P1 577, P5 669 |
| M6 | search: `hasNext` true at the end | P1 450 |
| M7 | expand: `hasNext` false one letter early | P1 165 |
| M8 | expand: only 10 letters written out | P1 582, P5 903 |
| E1 | ★: the end tested by `>=` | 0 |
| E2 | runs: the end tested directly, not through `hasNext` | 0 |
| E3 | search: the middle as `low + (high - low) / 2` | 0 |
| E4 | expand: 200 letters written out | 0 |

P2 and P4 kill nothing, and could only see a `hasNext` that changes the
iterator or two iterators that share state; no arm has either, so they
stand as properties of the interface rather than as tests of these arms.
P3 sees the mutants that misread the counts, since a split rewrites
them; M3, which gives the split run's extra letter twice; and M1 where a
text of one run becomes two. P5 sees the mutants that go wrong only
after many letters: M3 gives a letter too many in every run, M5 is wrong
at the first letter of every run after the first, and M8 runs out after
10 letters, which the text in front uses up. M6 and M7 go wrong only at
the end, which every property but P1 compares with an end that is just
as wrong. The differential's texts hold at most 99 letters, the joined
texts of P5 included, so the expand arm's note that more is left is
never set there, and E4 is safe for the same reason; the
`z1000000000` line of the harness is what reads the note.

## Verification

Every arm prints the same output as `string_iterator.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes every arm, the differential and the bench program. All at kara
`2d241d9b05`.

The frozen legacy backends do not get through. Every arm prints the same
output under `karac run --interp`, but `karac run` and `karac build`
panic in codegen (`control_flow_for.rs`), naming `ops`, the `Str`
parameter whose characters the harness's `run` loops over. `karac build`
panics on the differential too, and under `karac run --interp` the
differential ran past 60 seconds. The bench program is refused by `karac
build` at type checking: it passes `texts[..]` to the borrowing
parameter, which legacy reads as a move out of an index
(E_INDEX_MOVE_NON_COPY); a copy outside this directory that passes
`texts[..].clone()` fails in codegen instead, with no handler for `len`
on the `Str` parameter `compressed`. Legacy is frozen, so these are
noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 1,000 compressed texts of up
to 1,000 characters, the problem's longest, with counts from 1 to 20 and
one in ten up to 10^9, once, and then 200 times over makes a fresh
iterator on every one and spends the problem's 100 calls on it,
`hasNext` before every `next`. Every implementation prints `1000 texts,
200 rounds: 10000000 letters left, checksum 467264283`, the Kāra program
under `karac __mir-run` included (122 s).

Each implementation copies the text when the iterator is made, as the ★
arm collects it: a `Vec<char>` in Rust, a `[]rune` in Go, a list in
Python, and in C a `malloc`'d buffer of bytes. Spot timings on a shared
4-core container, three runs each (two for Python; `bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.08 to 0.09 s |
| Rust (`rustc -O`) | 0.24 to 0.30 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.23 to 0.28 s |
| Go | 0.70 to 0.88 s |
| Python | 3.64 to 3.80 s |
| Kāra (`karac build --mir`) | 0.84 to 0.95 s |

So `bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` builds neither it
nor the copy described above; that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 2.72 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

The Kāra row is about 3 times Rust's and a little slower than Go's. Each
iterator copies up to 1,000 characters and reads at most 50 letters, so
the copy is most of the work; that is a reading of the program. In
callgrind profiles at 20 rounds, the v2 program runs 0.92 billion
instructions to Rust's 0.52 billion, and valgrind counts 9 heap
allocations an iterator to Rust's 3, the difference between runs at
0 and at 20 rounds. That fits a `Vec` grown from empty by doubling
against Rust's `collect`, which starts from a size taken from the text's
length; it is a reading, not measured. The v2 binary carries no line
information, so the profiles do not say how the 0.54 billion
instructions in its own code divide. C's row, 3 times faster than
Rust's, copies one byte a letter where the others decode UTF-8 into
4-byte characters; that this is the difference is a reading of the
programs, not measured.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
