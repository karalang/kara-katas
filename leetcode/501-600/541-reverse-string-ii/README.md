# 541. Reverse String II

Given a string `s` and an integer `k`, reverse the first `k` characters
for every `2k` characters counting from the start of the string. If
there are fewer than `k` characters left, reverse all of them. If there
are less than `2k` but greater than or equal to `k` characters, then
reverse the first `k` characters and leave the other as original.

```
s = "abcdefg", k = 2  ->  "bacdfeg"
s = "abcd", k = 2     ->  "bacd"
```

**Constraints:** `1 <= s.length <= 10^4`; `s` consists of only
lowercase English letters; `1 <= k <= 10^4`.

## Approaches

Every arm is `fn reverse_str(s: Str, k: i64) -> String`.

| file | mechanism |
|---|---|
| `reverse_str.kara` ★ | the characters collected into a `Vec[char]`, the first k of each block of 2k reversed by swapping from both ends, collected back into a `String` |
| `reverse_str_bytes.kara` | the bytes copied into a `Vec[u8]` (the letters are one byte each), each block's first k reversed as a mutable slice, `String.from_utf8` |
| `reverse_str_blocks.kara` | a fresh `String`: per block, the first k characters pushed last to first, then the rest of the block as it is |
| `reverse_str_index.kara` | for each place, the place it takes its letter from worked out from its block |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 15 lines: both examples, one letter, k of 1,
of half the word, of the whole word and beyond it, and a short last
piece; then for 300 random words of 1 to 60 letters with k from 1 to
70 a checksum over the answers; and last a word of 10,000 letters (the
problem's longest) with k of 1, 7, 100, 4,999, 5,000 and 10,000.
`reverse_str.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
the word cut into pieces of k, the 1st, 3rd, 5th, ... reversed and the
rest kept. Each arm is held to the properties below on 1,000 random
words of 1 to 60 letters, from the whole alphabet or every other time
from `a` to `c`, with k from 1 to 70.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the answer has the word's letters, as many of each |
| P3 | done twice, it gives the word back |
| P4 | with k at least the word's length the word comes back reversed, and with k = 1 unchanged |
| P5 | after a word of a whole number of blocks of 2k, the answer is the two words' answers one after the other |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every piece of k reversed, not every other | P1 406 |
| M2 | ★: k + 1 characters reversed where the word allows | P1 448, P4 969 |
| M3 | bytes: a short last piece reversed without its last byte | P1 642, P4 976 |
| M4 | bytes: each block taken one byte longer than 2k | P1 197, P5 961 |
| M5 | blocks: the kept half of each block dropped | P1 448, P2 448, P3 448, P4 981 |
| M6 | blocks: the first half pushed in its own order | P1 956, P4 971 |
| M7 | index: the blocks taken k long, not 2k | P1 406 |
| M8 | index: a kept character taken from one place back | P1 444, P2 377, P3 447, P4 969 |
| E1 | ★: the middle character swapped with itself | 0 |
| E2 | bytes: the end written `n.min(start + k)` | 0 |
| E3 | blocks: the block's end counted from `mid` | 0 |
| E4 | index: the block start written `i / (2 * k) * (2 * k)` | 0 |

M1 and M7 are one mistake in two arms, and only the definition sees it.
Reversing every piece of k is still its own inverse (P3), still keeps
the letters (P2), still reverses a word no longer than k and leaves one
alone at k = 1 (P4), and still works block by block (P5); it differs
only where a second, fourth, ... piece has two letters or more and is
not a palindrome, 406 of the 1,000 words. M2, M3, M5, M6 and M8 change
what a piece becomes, and P4's k = 1 or whole-word cases catch each of
them. P5 sees only M4, the one edit that moves where blocks start.

## Verification

Every arm prints the same output as `reverse_str.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `20000 checks, 0 failures` on the first two and runs clean under
the third. `karac check` passes on every arm, the differential and the
bench program.

The frozen legacy backends: `karac run --interp` prints the eight short
cases right on every arm and then stops at the harness's `w.as_str()`
("method 'as_str' not found on type 'String'"). `karac run` and `karac
build` fail on every arm and on the bench program at the first `len` or
`bytes` on the `Str` parameter ("no handler for method"). The
differential stops at type checking, on taking a `String` out of a `Vec`
by index (E_INDEX_MOVE_NON_COPY). Legacy is frozen, so this is noted,
not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 200 random words of
10,000 letters (the problem's longest) once; then 100 times over every
word is answered with a k from 1 to 500 picked by the round and the
word, and one letter of the answer, picked the same way, goes into the
checksum. Every implementation prints `200 words, 100 times each:
200000000 letters, checksum 62111259`, the Kāra program under `karac
__mir-run` included (in 538 s).

Every mirror makes the same round trip through 32-bit characters:
Rust collects `chars()` into a `Vec<char>` and back into a `String`, Go
converts to `[]rune` and back, Python to a list and back with `join`.
C widens each byte to a `uint32_t`, since the words are ASCII, and
narrows it back; its loops vectorize, which is why it is so far ahead.
Spot timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.10 to 0.13 s |
| Rust (`rustc -O`) | 0.66 to 0.69 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.52 to 0.58 s |
| Go | 1.66 to 1.82 s |
| Python | 4.9 to 5.0 s |
| Kāra (`karac build --mir`) | 1.99 to 2.08 s |

The legacy `karac build` refuses this program (see Verification). So
`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`2649217dc8`. Under `karac __mir-llvm-run` the program prints the same
line in 14.9 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

The Kāra row is about three times Rust's, and the reversal itself costs
nothing measurable: with the swaps taken out the program still takes
2.02 s. About 0.7 s of it is `chars()` collected into the `Vec[char]`,
the cost of walking `chars()` (kara B-2026-10-13-31), and about 1.25 s
is collecting the chars back into a `String` (kara B-2026-10-13-35,
below). The bytes arm, timed on the same bench, takes 0.06 s.

## Compiler findings

kara B-2026-10-13-35 (open), filed from this kata: collecting chars into
a `String` on the v2 compiled backend is a chain of three runtime calls
per char (`karac_mir_string_push_char`, `string_push_str`,
`vec_reserve`), with nothing reserved up front, about 6 ns a char. It is
most of the ★ arm's time in the bench.

kara B-2026-10-13-31 (open, filed from kata 520) is the other part:
walking a `Str`'s `chars()` costs about 3.5 ns a char against 1 for its
`bytes()`.
