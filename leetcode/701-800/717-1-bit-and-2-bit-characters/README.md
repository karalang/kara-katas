# 717. 1-bit and 2-bit Characters

We have two special characters: the first can be represented by one bit,
0, and the second by two bits, 10 or 11. Given a binary array `bits`
that ends with 0, return true if the last character must be a one-bit
character.

```
bits = [1, 0, 0]     ->  true    (10, then 0)
bits = [1, 1, 1, 0]  ->  false   (11, then 10)
```

**Constraints:** 1 <= `bits.length` <= 1000; `bits[i]` is 0 or 1.

## Approaches

The code is prefix-free: a 0 is a whole character and a 1 always starts
a two-bit one, so the bits decode one way only, and the question is
where the last character starts.

| file | mechanism |
|---|---|
| `one_bit_and_two_bit_characters.kara` ★ | read from the front, stepping past one bit on a 0 and two on a 1; the last character is one bit when a step lands on the last bit |
| `one_bit_and_two_bit_characters_ones.kara` | a 0 always ends a character, so only the run of 1s just before the final 0 decides: it pairs off into two-bit characters, and an odd one left over takes the final 0 with it; reads only that run |
| `one_bit_and_two_bit_characters_reach.kara` | a table of the bits at which a character can start, filled from the front; the answer is whether the last bit is one |
| `one_bit_and_two_bit_characters_decode.kara` | the whole string decoded into its characters as strings, "0", "10" and "11", and the last one compared with "0" |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 11 lines: the two LeetCode examples; seven
short strings, among them one bit, a lone two-bit character, and runs of
two, three and four 1s before the final 0; strings of every length from
1 to 1,000 bits, the problem's most, that are all ones but the last; and
2,000 random strings of 1 to 1,000 bits with a quarter, a half or three
quarters ones, with a checksum. `one_bit_and_two_bit_characters.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which does not decode at all: it tries every way to cut the bits into
pieces, one cut mask at a time, keeps the cuttings whose pieces are all
characters, and asks whether one of them ends in a one-bit piece.
3,000 random strings of 1 to 14 bits ending in 0 are checked, a quarter,
a half or three quarters ones.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | a 0 put in front gives the same answer |
| P3 | a two-bit character put in front gives the same answer |
| P4 | a string built from up to seven random characters gives true exactly when its last character is 0 |

It prints `3000 strings (2079 one-bit endings), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every character read as one bit | P1 921, P4 2006 |
| M2 | ★: the walk stopped a bit early | P1 1021, P2 208, P4 283 |
| M3 | ★: a step past the last bit counted too | P1 921, P4 2006 |
| M4 | ones: an odd run counted as one-bit | P1 3000, P4 3000 |
| M5 | ones: the count started a bit too far back | P1 1771, P3 208, P4 2577 |
| M6 | ones: the first bit never counted | P1 338, P2 338, P3 297, P4 511 |
| M7 | reach: the one- and two-bit steps swapped | P1 1824, P2 514, P3 252, P4 2444 |
| M8 | reach: the end of the string read as the answer | P1 921, P4 2006 |
| M9 | reach: the first start put on the second bit | P1 546, P2 546, P3 293, P4 651 |
| M10 | decode: every two-bit character recorded as 0 | P1 921, P4 2006 |
| M11 | decode: a 0 stepped over with the bit after it | P1 541, P2 1402, P4 895 |
| M12 | decode: a two-bit character's second bit read again | P1 921, P4 2006 |
| E1 | reach: a two-bit character ending on the last bit not marked | 0 |
| E2 | decode: the last character tested as not 10 | 0 |
| E3 | ★: the loop bound written as at most n - 2 | 0 |

P1 and P4 kill all twelve. Five of them, M1, M3, M8, M10 and M12, answer
true for every string, which is why their counts are the same; a fixed
answer survives anything put in front, so P2 and P3 cannot see them.
P2 catches five that go wrong depending on what the string starts with,
M2, M6, M7, M9 and M11, and P3 catches M5, M6, M7 and M9. E1 leaves
unmarked a start just past the last bit, which the answer never reads;
E2 asks whether the last character is not 10, and a string ending in
0 cannot end in 11, so that is the same question; E3 writes the loop
bound as at most n - 2, the same for integers.

## Verification

Every arm prints the same output as `one_bit_and_two_bit_characters.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and under `karac __mir-llvm-asan` (AddressSanitizer)
with no error; the differential prints its line under all three. `karac
check` passes all four arms, the differential and the bench program. The
debug build that runs `__mir-llvm-run`, `__mir-llvm-asan` and `build
--mir` and the release build that runs `check` and `__mir-run` are both
at kara `a73d3c10ad`, whose last compiler change is `3c8e763161`. The
runtime archives were built after that change.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends run all four arms and the differential with
the same output, under `karac run --interp`, the JIT, `karac build` and
an auto-par build. The legacy `karac build` refuses the bench program at
codegen, at its `for x in ...iter_mut()` over the strings, which legacy
lowers only for a vector with scalar elements (kara
B-2026-07-14-10). Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes
100 random strings of 10,000 bits ending in 0 once, a quarter, a half or
three quarters ones, and in each of 400 rounds flips one bit of every
string, the same place in each, before reading them all, counting the
one-bit endings. The flips land far enough from the ends that no answer
changes; they are there so that no round reads the same input as
another. Every implementation prints `400 rounds of 100 strings of
10000 bits: 29600 one-bit endings`, the Kāra program under `karac
__mir-run` included (in 36 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.78 to 0.90 s |
| Rust (`rustc -O`) | 0.81 to 0.86 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.72 to 0.94 s |
| Go | 0.79 to 0.86 s |
| Python | 9.6 to 10.1 s |
| Kāra (`karac build --mir`) | 0.76 to 0.85 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 2.2 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So all five compiled programs land in the same range; the medians of the
interleaved runs are 0.80 s for the v2 build against 0.82 for C and
0.81 for Rust. Under valgrind's cachegrind the v2 build runs 2.7 billion
instructions against C's 1.4 and Rust's 1.9, and 1.09 billion branches
against 0.27 and 0.55, all well predicted. The run time does not follow
the instruction count here; what the loop waits on instead was not
traced.

## Compiler findings

None new.
