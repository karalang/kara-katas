# 767. Reorganize String

Rearrange the letters of `s` so that no two neighbours are the same
letter, and return any such rearrangement, or the empty string if there
is none.

```
"aab"   ->  "aba"
"aaab"  ->  ""
```

**Constraints:** `s` has from 1 to 500 lowercase English letters.

## Approaches

A letter can be kept from its neighbours only if it takes at most every
other place, so there is an answer exactly when no letter fills more
than half of the string, rounded up. The arms build an answer in four
ways.

| file | mechanism |
|---|---|
| `reorganize_string.kara` ★ | the commonest letter dealt into places 0, 2, 4 and so on, then every other letter, one after another, into the even places left and then the odd ones; O(n) |
| `reorganize_string_heap.kara` | a `PriorityQueue` of the letters by how many are left; the top letter is written, or the next one if the top would repeat the last; O(n log 26) |
| `reorganize_string_sorted.kara` | the letters sorted commonest first, each letter's copies together, and written into the even places and then the odd ones, with a check for neighbours at the end; O(n log n) |
| `reorganize_string_greedy.kara` | one place at a time, the letter with most copies left that differs from the last; O(26 n) |
| `differential.kara` | the four arms against the definition, four properties |

The arms may give different rearrangements, so the harness checks each
answer instead of printing it: that it is a rearrangement of `s` with no
two neighbours equal, or that it is empty. Every arm prints the same
12 lines: the two LeetCode examples; a single letter, one letter twice,
and two different letters; five and six letters from two; `vvvlo`; nine
letters with the commonest at four, five and six; then 300 random
strings of up to 40 letters, from up to five letters with the first
drawn twice as often, with how many have an answer and a checksum of the
answers' lengths. A wrong answer would print on a line of its own.
`reorganize_string.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which tries every letter in every place for an order with no two
neighbours equal. The 1,800 random strings are drawn like the harness's;
the first 1,500, of up to 9 letters from up to four, are checked against
the definition, and the last 300, of up to 500 letters from up to
26, against the other properties.

| | property |
|---|---|
| P1 | there is an answer exactly when the definition finds one (the 1,500 short strings) |
| P2 | an answer is a rearrangement of the string with no two neighbours equal |
| P3 | renaming the letters and shuffling the string changes nothing about whether there is an answer |
| P4 | there is an answer exactly when no letter fills more than half the places, rounded up |

It prints `1800 strings (1085 rearranged), 4 arms, 27600 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error; the count is the ★
arm's.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a letter filling exactly half, rounded up, refused | P1 393, P4 396 |
| M2 | ★: letters dealt into consecutive places | P2 804 |
| M3 | ★: z never taken as the commonest | P3 29 |
| M4 | heap: the passed-over letter never put back | P1 195, P2 586, P3 48, P4 219 |
| M5 | heap: a letter's last copy dropped | P1 180, P2 985, P4 181 |
| M6 | heap: the top letter taken even if just written | P1 690, P2 1246, P4 715 |
| M7 | sorted: the least common letters first | P1 221, P4 222 |
| M8 | sorted: the final check skipped | P1 690, P2 715, P4 715 |
| M9 | sorted: sorted by letter alone | P1 103, P3 148, P4 103 |
| M10 | greedy: the least common letter that fits | P1 426, P4 696 |
| M11 | greedy: the letter just written never recorded | P1 690, P2 1246, P4 715 |
| M12 | greedy: the first letter that fits, whatever its count | P1 183, P3 253, P4 424 |

P1 and P4 kill all but M2 and M3. M2 still answers exactly when it
should, with the right letters, so only P2 sees its neighbours. M3 is
seen by P3 alone: the harness's strings use a to e and the
differential's make a the commonest letter, so z leads only once the
letters are renamed, and where it fills more than half the edit answers
anyway. P2 sees the six edits that write a wrong answer, and is blind to
M1, M7, M9, M10 and M12, which only refuse strings that have one.
P3 sees the edits whose failures depend on which letter is which,
M3, M9 and M12, and M4, whose lost letter depends on the queue's order;
M1 depends on the counts alone, and on these strings M7 and M10 failed
the same way however the letters were named. No first choice survived.

## Verification

Every arm prints the same output as `reorganize_string.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`8a2af7d554`, whose last compiler change is `60d9973e03`. The runtime
archives were built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept all four arms, the differential and,
through a copy, the bench. Each arm prints the same output under the
legacy interpreter, `karac run`, `karac build` and an auto-par build,
and the differential prints its line under the legacy interpreter and
`karac build`, each with a warning that a borrowed `s` is used after a
move, since legacy predates borrowed parameters. Legacy refuses the
bench at `reorganize_string(pool[round % 64])`, as a move out of an
index; its timing below is of a copy whose parameter is `ref String`.
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. Sixty-four
random strings of 500 letters, the most LeetCode allows, are built once,
each from a random number of letters with the first drawn twice as
often; each of 400,000 rounds reorganizes the next of them and folds the
answer's length and one of its letters into a checksum. Every
implementation prints `400000 strings of 500 letters: 343750 rearranged,
checksum 767838531`, the Kāra program under `karac __mir-run` included
(in 175 s). Each language allocates a new answer every round; C and Kāra
also count over bytes, Python over characters.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.33 to 0.40 s |
| Rust (`rustc -O`) | 0.36 to 0.45 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.37 to 0.47 s |
| Go | 0.50 to 0.58 s |
| Python | 18.6 to 19.3 s |
| Kāra (`karac build --mir`) | 0.57 to 0.71 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
3.6 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 0.58 s,
against C's 0.35, Rust's 0.38 (0.38 under overflow checks) and Go's
0.55. Under valgrind's cachegrind v2 runs 7.1 billion instructions, Rust
3.8 billion and C 2.2 billion. The legacy build of the copy ran 0.35 to
0.42 s, a median of 0.38 s in the interleaved runs, so v2 takes
1.5 times as long as legacy, inside M2's limit of twice legacy; new
katas' benches are outside M2's frozen set in any case. The comparison
with C and Rust waits until after M4.

## Compiler findings

None new.
