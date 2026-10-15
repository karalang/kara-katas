# 664. Strange Printer

A printer prints one letter at a time, any number of copies of it in a
row, each turn covering a range of the paper and printing over whatever
was there. Given a string `s`, return the fewest turns that print it.

```
s = "aaabbb"  ->  2   ("aaa", then "bbb")
s = "aba"     ->  2   ("aaa", then "b" over the middle)
```

**Constraints:** 1 to 100 lowercase English letters.

## Approaches

Every arm is `fn strange_printer(s: String) -> i64` and fills a table of
the fewest turns for each range of the text. They differ in which end of
a range they lead with and in how they split it. The key fact is that a
turn printing one copy of a letter can be stretched to a later copy at
no cost, with the letters between printed over it.

| file | mechanism |
|---|---|
| `strange_printer.kara` ★ | each range by its last letter: printed alone, one turn more, or riding the turn of an earlier copy, with the letters between printed on their own; ranges filled bottom up, starting points falling; O(n^3) |
| `strange_printer_memo.kara` | each range by its first letter, top down with a table remembering each range: printed alone, or its turn stretched to a later copy that the rest then shares; O(n^3) |
| `strange_printer_runs.kara` | each run squashed to one letter, then the first-letter recurrence bottom up by length, visiting only the later copies of the first letter through links from each letter to its next copy; O(m^3) over `m` runs |
| `strange_printer_split.kara` | a range whose ends match costs what it does without its last letter; any other is split into two parts at the cheapest place; O(n^3) |
| `differential.kara` | the four arms against a breadth-first search over turns undone from the finished text, five properties |

Every arm prints the same 14 lines: the two LeetCode examples; one
letter, a palindrome, `abab`, `tbgtgb` and `abcabc`; four texts of the
problem's longest, 100 letters: one letter, `ab` 50 times, the alphabet
nearly four times over and the alphabet up and down twice; a checksum of
300 random texts of 1 to 20 letters from 2 to 5 letters; and random
texts of 100 letters from 3 and from 26. `strange_printer.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which runs the printing backwards. The last turn leaves one letter over
its whole range, so it can be undone from the finished text, freeing
that range; any earlier turn can then be undone over a range whose
letters not yet undone are all one letter. A breadth-first search over
the sets of undone letters finds the fewest turns that undo the whole
text, which is the fewest that print it. Each of 1,500 random texts is
1 to 8 letters long, drawn from 2 to 4 letters, small enough for the
search's 2^8 sets.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the text reversed takes as many turns |
| P3 | so does the text with each letter swapped for its mirror in the alphabet |
| P4 | at least one turn for each letter used, at most one for each run |
| P5 | the first letter added again at the end costs nothing, since the first turn can stretch to it |

It prints `1500 texts (6929 letters), 4 arms, 30000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the earlier copy's turn counted again | P1 1168, P4 1001, P5 1500 |
| M2 | ★: no copy at the interval's own start | P1 861, P2 515, P4 285, P5 791 |
| M3 | memo: the shared letter left out after the copy | P1 975, P4 817, P5 1500 |
| M4 | memo: no copy at the interval's own end | P1 880, P2 515, P4 297, P5 775 |
| M5 | runs: the first letter printed for free | P1 1500, P4 1500 |
| M6 | runs: only the next copy of the first letter tried | P1 1, P5 9 |
| M7 | split: matching ends charged a turn more | P1 1168, P4 1001, P5 1500 |
| M8 | split: the last place to cut never tried | P1 316, P2 472, P4 105 |
| E1 | ★: the empty middle tested as `k + 1 < j` | 0 |
| E2 | memo: a remembered interval taken only above 0 | 0 |
| E3 | runs: every letter kept, runs not squashed | 0 |
| E4 | split: the cheapest pair started 5 higher | 0 |

P1 kills all eight, P4 all but M6, and P5 all but M5 and M8, which give
the same answer, right or wrong, with the extra letter as without it.
P2, the text reversed, sees the three that miss a copy or a cut at one
end of a range, M2, M4 and M8, since reversing the text moves it to the
other end. P3 sees none: no arm asks which letter a letter is, only
whether two match, so renaming them cannot change an answer, right or
wrong; it stays as a check on the arms themselves. M6, which stretches
the first letter's turn only as far as its next copy, is the hardest to
catch at this size: one text in the 1,500 shows it, and nine of P5's one
letter longer. The four survivors cannot change an answer: `k + 1 <= j -
1` and `k + 1 < j` are the same test; a remembered range never takes
0 turns; the first-letter recurrence is exact on the text as it is, so
squashing runs only makes its table smaller; and the cheapest pair of
parts never costs more than the range's length.

## Verification

Every arm prints the same output as `strange_printer.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` for the debug build and `72739d54d6` for the release build
that runs `check` and `__mir-run`, with runtime archives newer than the
last `runtime/src` change.

The frozen legacy backends refuse every arm and the differential at type
checking: the harness's `random_text` hands `seed`, already a `mut ref`
parameter, on with the `mut` marker design.md asks for, and the runs arm
and the differential read through `*` a byte that `bytes().iter()` hands
them, which legacy types as a plain `u8`. Legacy rejects both. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 64 random texts of the
problem's longest, 100 letters, once, from 2 to 26 letters; then each of
2,000 rounds solves one, picked by the round, and puts its turns into a
checksum. Every implementation prints `64 texts of 100 letters,
2000 rounds: checksum 160360074`, the Kāra program under `karac
__mir-run` included (in 251 s).

Each implementation is the same table, made afresh for each text: Kāra's
and Rust's a `Vec` of `Vec`s, Go's a slice of slices, Python's a list of
lists, and C's one `calloc`ed block. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine), each including making the texts:

| | time |
|---|---|
| C (`clang -O3`) | 0.61 to 0.63 s |
| Rust (`rustc -O`) | 0.63 to 0.73 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.66 to 0.68 s |
| Go | 0.68 to 0.82 s |
| Python | 19 to 20 s |
| Kāra (`karac build --mir`) | 0.73 to 0.89 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program at type checking: `main` hands `texts[r % 64]` to
`strange_printer` without copying it, which design.md allows, since a
parameter borrows, and which legacy rejects as a move out of an index.
That edit is by hand, on top of the `scripts/new-bench.sh` output. A
copy outside the kata that clones the text builds under legacy and takes
0.71 to 0.74 s. Under `karac __mir-llvm-run` the program prints the same
line in 2.8 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

So the v2 build is level with legacy and within about a fifth of Rust
and C, all of them spending the time in the same triple loop. The
comparison with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The legacy refusal
above is not filed because legacy is frozen.
