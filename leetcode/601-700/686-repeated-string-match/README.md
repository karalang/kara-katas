# 686. Repeated String Match

Given two strings `a` and `b`, return the fewest times `a` has to be
repeated, joined end to end, for `b` to be a substring of the result, or
-1 if no number of repeats will do.

```
a = "abcd", b = "cdabcdab"  ->  3    ("abcdabcdabcd")
a = "a",    b = "aa"        ->  2
```

**Constraints:** 1 <= `a.length`, `b.length` <= 10^4; `a` and `b` hold
lowercase English letters.

## Approaches

Every arm is `fn repeated_string_match(a: String, b: String) ->
i64`. Below, n and m are the lengths of `a` and `b`, and q is the fewest
copies of `a` at least as long as `b`.

| file | mechanism |
|---|---|
| `repeated_string_match.kara` ★ | a match must start within the first copy of `a`, so it ends within q + 1 copies: build q copies and test with `String.contains`, then q + 1 |
| `repeated_string_match_kmp.kara` | Knuth-Morris-Pratt for `b` over the repetition of `a`, read as `a[i mod n]` without building it, for n + m bytes; a match ending at byte e takes e / n copies, rounded up |
| `repeated_string_match_hash.kara` | a rolling polynomial hash of an m-byte window, moved over every start in the first copy, each hash match checked byte by byte |
| `repeated_string_match_brute.kara` | every start in the first copy, compared against `b` a byte at a time until the first mismatch |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 17 lines: the two LeetCode examples; ten
corners, among them `b` equal to `a`, `b` shorter than `a`, two that
need q + 1 copies, a `b` that is `a` reversed, and ten copies of a
single letter; how many of the 7,620 pairs of `a` of 1 to 4 letters and
`b` of 1 to 7 over two letters need each number of copies, with a
checksum; 300 random pairs, half of them `b` cut from the repetition of
`a` and some of those with a letter changed, with a checksum; and three
pairs of 10,000-letter strings over 26 letters, `b` cut from the
repetition of `a`, and the same `b` with its last letter changed.
`repeated_string_match.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: join 1, 2, 3, ...
copies of `a`, up to three more than `b` needs to fit, and compare `b`
against every start, letter by letter. 2,000 random pairs are checked,
`a` of up to 8 letters in three quarters of them and up to 60 in the
rest, over one to three letters, half of them with `b` cut from the
repetition of `a` and a quarter of those with a letter changed; the
1,558 with `a` of up to 8 letters go against the definition.

| | property |
|---|---|
| P1 | the answer is the definition's (`a` of up to 8 letters) |
| P2 | every letter of both strings moved on alike changes nothing |
| P3 | both strings reversed changes nothing |
| P4 | `b` made of k copies of `a` needs exactly k |

It prints `2000 pairs (1231 with an answer), 4 arms, 30232 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: q + 1 copies never tried | P1 166 |
| M2 | ★: q rounded down | P1 94 |
| M3 | kmp: the text only m bytes long | P1 362, P3 164 |
| M4 | kmp: copies counted to the byte before the match ends | P1 376, P3 152, P4 166 |
| M5 | hash: the byte leaving the window added back | P1 257, P3 196 |
| M6 | hash: the copies taken as (s + m) / n + 1 | P1 338, P3 137, P4 2000 |
| M7 | brute: the last start never tried | P1 204, P3 135, P4 166 |
| M8 | brute: the copies rounded down | P1 735, P3 137 |
| E1 | ★: two more copies added for the second test | 0 |
| E2 | kmp: the text n bytes longer | 0 |
| E3 | hash: base 137, not 131 | 0 |
| E4 | brute: one more start, n | 0 |

P1 kills all eight. M1 and M2, the ★ arm's two, are seen by P1 alone:
each answers the same for a string and its reverse, and k copies of `a`
are found in exactly k copies, which q already is. P3 sees the six
others, which all count copies or starts from the left. P4 sees M4 and
M7 only where `a` is one letter long, the one case in which they get k
copies wrong, and M6, which adds a copy whenever the match ends on a
copy's last letter, as k copies always do. P2 sees none: no arm looks at
which letters it is given, only at whether two are equal, so moving
every letter on alike changes nothing for a mutant either. The four
survivors change no answer. A match that two more copies would hold is
already held by one more, so the extra copy is never needed; every match
starts within the first copy, so the KMP text never needs more than n +
m bytes, and running n more finds nothing new; every hash match is
checked byte by byte, so the base changes only which windows get
checked; and a start at n is the start at 0 one copy later, so it can
only match where 0 already did.

## Verification

Every arm prints the same output as `repeated_string_match.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`e765966014` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives rebuilt after the last
`runtime/src` change.

The frozen legacy interpreter prints the same output for all four arms.
The legacy JIT and `karac build` stop every arm with `free(): double
free detected in tcache 2`, and the `KARAC_AUTO_PAR=1` build's output
differs too; where was not looked into. The legacy backends refuse the
differential at type checking, at `*c`, since legacy gives the items of
`x.iter()` by value where v2 gives references. Legacy is frozen, so this
is noted, not filed.

## Benchmarks

The bench program uses the KMP arm, the one that is the same algorithm
in all five languages; the ★ arm's speed is that of each language's own
substring search. It builds 100 pairs once, `a` of 1,000 to
10,000 letters over two letters and `b` of 10,000 cut from the
repetition of `a`, half of them with the last letter changed, then
answers every pair in each of 30 rounds, putting each answer into a
checksum. Every implementation prints `3000 pairs answered: 990 with no
answer, checksum 782377184`, the Kāra program under `karac __mir-run`
included (in 92 s).

Each implementation is the same KMP search over a freshly allocated
failure table per pair. Spot timings on a shared 4-core container, six
runs each, three of them interleaved (two for Python; `bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.34 to 0.43 s |
| Rust (`rustc -O`) | 0.33 to 0.36 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.34 to 0.36 s |
| Go | 0.43 to 0.45 s |
| Python | 6.4 to 6.5 s |
| Kāra (`karac build --mir`) | 0.35 to 0.38 s |
| Kāra, legacy (`karac build`, a copy) | 0.29 to 0.34 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program at type checking: `repeated_string_match(firsts[c], seconds[c])`
moves elements out of `firsts` and `seconds` under legacy, where a bare
parameter is owned, but v2 borrows them. That edit is by hand, on top of
the `scripts/new-bench.sh` output. A copy outside the kata whose
parameters are `ref String` builds under legacy, and its row is above.
Under `karac __mir-llvm-run` the program prints the same line in 2.0 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is level with C and Rust here, a little ahead of Go, and
a little behind legacy; why legacy is ahead was not looked into. The
comparison with C and Rust waits until after M4.

## Compiler findings

B-2026-10-15-61, new, filed from this kata. The harness first changed a
letter of `b` with `let mut t = b.bytes(); t[9999] = ...;`, and `karac
check` accepted it, though `bytes()` gives a `Slice[u8]` and writing
through a slice needs a `mut Slice[u8]`. The two v2 backends then
disagreed: `__mir-run` wrote into a copy, while `__mir-llvm-run` and
`build --mir` wrote into `b` itself, so the last line printed `long:
-1` there and `long: 2` here. The harness now copies first,
`b.bytes().to_vec()`, which is the correct program anyway; nothing needs
reverting when the row is fixed. The same row records that `let mut w =
v[0..2]; w[0] = 9;` changes a `v` that is not `mut`, on both backends.
