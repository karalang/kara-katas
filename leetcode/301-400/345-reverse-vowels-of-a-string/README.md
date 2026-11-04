# 345. Reverse Vowels of a String

Given a string `s`, reverse only its vowels and return the result. The vowels
are `a`, `e`, `i`, `o` and `u`, in lower and upper case, and may appear more
than once. Every other character keeps its place.

```
"IceCreAm"  ->  "AceCreIm"
"leetcode"  ->  "leotcede"
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `reverse_vowels.kara` ★ | two indices walk inward, each stepping past consonants; two vowels swap | `O(n)` time, `O(n)` space |
| `reverse_vowels_stack.kara` | push the vowels in order, then rebuild, popping one at each vowel | `O(n)` time, `O(n)` space |
| `reverse_vowels_positions.kara` | record the vowels' indices, then swap them in pairs from both ends | `O(n)` time, `O(n)` space |
| `reverse_vowels_closure.kara` | `filter(...).collect()` the vowels, then `map(...)` the string, popping from the vowels | `O(n)` time, `O(n)` space |
| `reverse_vowels_bytes.kara` | the ★ walk over the UTF-8 bytes, with `b'a'` byte literals | `O(n)` time, `O(n)` space |
| `differential.kara` | the five arms and a by-rank oracle on every length `0..300`, five properties | — |
| `bench/reverse_vowels.kara` | 1,000 punches, each reversing the vowels of 200,000 characters in place, by the ★ loop | — |

The `O(n)` space is the character array a `String` is unpacked into; the
problem's in-place bound applies to that array, as it does in every language
whose strings are immutable.

Every arm prints the same 12 lines: the two examples, the empty string, one
vowel, no vowels, only vowels, two vowels of different case, three
sentences, a string with accented letters, and a 100,000-letter string whose
vowels are reversed twice. Case travels with the letter, so `"Euston saw I
was not Sue."` becomes `"euston saw I was not SuE."`. The accented line is
`"Kāra, señor, über alles" -> "Kāre, sañer, übor ellas"`: `ā`, `ñ` and `ü`
are not among the ten vowels, so they keep their places like any consonant.

The byte arm gets that line right for a reason worth stating. Every byte of a
multi-byte UTF-8 character is `0x80` or above, so none of them equals an ASCII
vowel, and the walk never splits a character. That is why
`String.from_utf8(bs).unwrap()` cannot fail on its output. `reverse_vowels.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` runs all five arms on every length in `0..300`, each
filled pseudo-randomly from an alphabet of all ten vowels, consonants of both
cases, digits, punctuation, and two-, three- and four-byte code points, three
of which (`ā`, `é`, `ü`) look like vowels and are not. It compares them with
a sixth version, the oracle, which counts how many vowels precede each
position and reads the vowel that many places from the end of the vowel list.
It shares no loop shape with the five.

| | property |
|---|---|
| P1 | all five arms equal the oracle |
| P2 | reversing twice gives the input back (★ and byte arms) |
| P3 | every non-vowel keeps its place |
| P4 | the vowels of the result are the vowels of the input, reversed |
| P5 | the character count and the byte length are unchanged |

`failures 0` and all properties hold on every surface: 13,212 vowels,
checksum 243578990. An independent Python replay of the input generator and
checksum gives the same two numbers.

## Mutation testing

Eleven edits to the copies inside `differential.kara`, each run under
`karac run`. All eleven are killed.

| # | mutation | how |
|---|---|---|
| M1 | ★: `while i < j - 1` | P1, 42 failures |
| M2 | ★: never step `j` past a consonant | P1 and P2, 590 failures |
| M3 | stack: `stack.remove(0)` instead of `pop()` | P1, 294 failures |
| M4 | positions: stop at `(m - 1) / 2` | P1, 146 failures |
| M5 | positions: partner `m - 2 - k` | P1, 294 failures |
| M6 | closure: replace only `'a'` in the `map` | P1, 294 failures |
| M7 | bytes: drop `b'U'` from the byte vowels | P1, 265 failures |
| M8 | bytes: swap with `j - 1` | P1 and P2, then `from_utf8` fails |
| M9 | bytes: stop the right-hand skip at `j - 1` | P2, then `from_utf8` fails |
| M10 | oracle: read `vs[rank]` | P1 and P4, 12,172 failures |
| M11 | the char arms: drop `'U'` from the vowels | P1, 265 failures |

M7 survived the first run, with `failures 0`. The input alphabet then held
`AEIO` and no `U`, so no input could tell a byte set without `U` from one
with it. Adding `U` to the alphabet killed it; the numbers above are from the
corrected differential. M8 and M9 are the byte arm's real risk: an index
that lands inside a multi-byte character makes the swap produce invalid
UTF-8, and the program stops at the `unwrap()` rather than printing a wrong
string.

## Verification

All five arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build` (`scripts/surface-sweep.py`, 6
programs, 0 divergences). Built with `KARAC_AUTO_PAR=0`, all six are
valgrind-clean: `0 errors` and `0 bytes in use at exit`.

The benchmark kernel's sink matches all four language twins and Python
(`sink 629446893`), and `karac run --interp` prints the same sink.

## Benchmarks

`bench/reverse_vowels.kara` and its four mirrors time the ★ loop. 200,000
characters are drawn once from a 32-letter alphabet, `a` to `z` and `A` to
`F`, so seven of the 32 letters are vowels. Each of 1,000 punches replaces
one character at a random position, reverses the vowels of the whole array in
place, and reads one character back at another random position, which is
folded into a rolling hash, the sink. The kata's function unpacks a `String`
into a character array and packs it back; the bench keeps the array and times
the loop between, in every language, so the workload is the algorithm and
not each language's string conversion.

### Apple M5 Pro, 2026-11-04

30 runs each, 5 warmups, on the Apple M5 Pro, karac `0.8.0-dev.14374+gf0017054a`
(gf0017054a, the v2/MIR backend), measured 2026-11-04, with the Kāra binary built
`KARAC_AUTO_PAR=0`. Python was not run on this host. Its row in the history
below was last measured 2026-10-05, on the container, and not re-run. The last
column is Kāra's mean over that row's mean.

| implementation | mean | Kāra / this |
|---|---|---|
| c `clang -O3` | 277.1 ms ± 0.8 | 1.02× |
| **kāra `karac build`, seq** | **281.9 ms ± 1.3** | **—** |
| rust `-O` | 321.8 ms ± 1.7 | 0.88× |
| rust `-O -C overflow-checks=on` (equal-safety) | 322.0 ms ± 1.1 | 0.88× |
| go `go build` | 623.0 ms ± 2.0 | 0.45× |

Kāra is 0.88× both Rust builds, level with C at 1.02×, and 0.45× Go. None of
these gaps was investigated on this host.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 42.3 ms ± 0.6 | 32.7 KiB | 1.8 MiB |
| rust | 79.5 ms ± 0.7 | 455.7 KiB | 1.9 MiB |
| kāra | 99.2 ms ± 1.0 | 50.7 KiB | 1.9 MiB |
| go | — | 2450.4 KiB | 3.4 MiB |

`karac build` is 2.3× clang's cold compile and 1.2× rustc's. Kāra's binary
is 1.5× clang's and 9.0× smaller than rustc's. Raw numbers are in
[`bench/results.json`](bench/results.json). The sink matches across the Kāra,
Rust, C and Go builds (`sink 629446893`).

### Container x86-64 history

> **Host:** these are the x86-64 Linux cloud container figures, kept as history,
> from [`bench/results.container-x86.json`](bench/results.container-x86.json).
> Absolute milliseconds are NOT comparable between hosts. Only the
> **within-file cross-language ratios** are.

30 runs each, 5 warmups, on a 4-core x86-64 Linux container, karac
`0.1.0-dev.10448+g76727438c`, measured 2026-10-05, with the timed lane built
with `KARAC_AUTO_PAR=0`. Python is its own lane at 3 runs.

| implementation | mean | vs fastest |
|---|---|---|
| **kāra `karac build`** | **943.2 ms ± 22.9** | **1.00×** |
| c `-march=x86-64-v3` (matched-ISA) | 958.2 ms ± 22.4 | 1.02× |
| c `clang -O3` | 959.4 ms ± 26.2 | 1.02× |
| rust `-O` | 982.9 ms ± 13.5 | 1.04× |
| rust `-O -C overflow-checks=on` (equal-safety) | 984.4 ms ± 35.0 | 1.04× |
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 1004 ms ± 37 | 1.06× |
| go `go build` | 1775 ms ± 33 | 1.88× |
| python 3 | 10995 ms ± 468 | 11.7× |

**Kāra, C and Rust tie; Go is 1.9× behind.** The first six are within two
standard deviations of each other. Which index moves next depends on the
characters just read, so the loop is a chain of data-dependent branches. The
C binary contains no vector instructions at all, so its loop is scalar. Kāra
and Rust match it, which suggests theirs are scalar too; that was not checked
instruction by instruction. Kata 344's swap loop, which rustc does vectorize,
put Rust 4× ahead; nothing like that happens here.

Note (2026-11-04): on the M5 feed Rust does not tie: Kāra leads it by 12% and
C by 14%, and Go is 2.21× Kāra. Kata 344's Rust lead on this host is 2.47×,
not 4×.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 97.0 ms ± 2.6 | 15.7 KiB | 2.1 MiB |
| rust | 135.1 ms ± 5.6 | 3863.5 KiB | 2.9 MiB |
| kāra | 342.8 ms ± 17.7 | 337.4 KiB | 3.1 MiB |
| go | — | 2178.9 KiB | 2.5 MiB |
| python | — | — | 9.3 MiB |

`karac build` is 3.5× clang's cold compile and 2.5× rustc's. Its binary is
21× clang's and 11× smaller than rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

Writing this kata turned up one gap in the compiler's diagnostics, fixed in
the kara repo.

- **B-2026-10-05-75 (diagnostics): an iterator method called on a `Slice`
  named the wrong fix or none.** The byte arm's first draft wrote
  `s.bytes().collect()`, since `bytes()` returns a `Slice[u8]`. The error
  said only "no method 'collect' on type 'Slice'". On `v.as_slice().map(...)`
  it said "did you mean 'swap'?". A `Vec` already got the right advice,
  "write `v.iter().map(...)`"; a slice is iterable the same way and was left
  out of that check. It now gets the same hint, with the receiver as written
  (`s.bytes().iter().collect(...)`) rather than a placeholder name. The kata
  keeps `s.bytes().to_vec()`, the shorter spelling for a copy.

The author already knows the language, so none of this counts toward the
machine-fix rate.
