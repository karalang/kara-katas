# 1180. Count Substrings with Only One Distinct Letter

Given a string `s`, return the number of substrings that have only one
distinct letter.

```
s = "aaaba"       ->  8    ("aaa" once, "aa" twice, "a" four times, "b" once)
s = "aaaaaaaaaa"  ->  55
```

**Constraints:** `1 <= s.length <= 1000`, `s[i]` consists of only
lowercase English letters.

The arms are `fn count_letters(s: Str) -> i64`. The two Rust arms keep the
method LeetCode gives Rust users, over `String` returning `i32`, inside
`impl Solution`, and a one-line `count_letters` calls it.

## Approaches

A substring of one letter lies inside one maximal run of that letter, and
a run of `n` letters holds `n * (n + 1) / 2` of them. Equally, the
substrings of one letter that end at a position are as many as the run
ending there is long.

| file | mechanism |
|---|---|
| `count_letters.kara` ★ | one pass over `s.bytes()`, the length of the run ending at each position kept as it goes and added at every step. O(n) |
| `count_letters_runs.kara` | each maximal run found with two indices, `j` walked on while it repeats the letter at `i`, and its `n * (n + 1) / 2` added. O(n) |
| `count_letters_brute.kara` | every start taken in turn and its substrings counted while the letter at `j` is still the letter at the start, stopping at the first that is not. O(n^2) at worst, a string of one letter |
| `count_letters_chunks.kara` | the runs as `chunk_by(\|a, b\| a == b)` groups, each group's `n * (n + 1) / 2` summed in one chain. O(n) |
| `count_letters_solution.kara` | a Rust solution as LeetCode's Rust users write it (`s.as_bytes()`, a `usize` loop comparing each byte with the one before with `i > 0 && ..`, the run counted in an `i32`), carried to Kāra by `karac fix` |
| `count_letters_chain.kara` | another Rust solution, one iterator chain (`s.as_bytes().chunk_by(\|a, b\| a == b)`, each run's length `as i32` and its `n * (n + 1) / 2` summed), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; one letter,
two different letters, the whole alphabet once, a run at each end and runs
of one letter split by another (`small: [1, 2, 26, 23, 11]`); 300 random
strings of 1 to 40 letters over the first 1 to 3 (`300 random strings:
36919 in all, checksum 887532465`); 1000 letters, the constraints' most,
all one letter (`1000 of one letter: 500500`); and 2000 random strings of
1000 letters over the first 2 to 4 (`2000 strings of 1000 letters: 3244448
in all, checksum 225722129`). The brute-force arm counts every substring of
a string of one letter, half a million for 1000 letters, so the random
strings of 1000 have at least two letters to keep it within the corpus's
time limit under `karac run`. `count_letters.py` mirrors the ★ arm and its
output is byte-identical; with `lit` it counts the examples, the small
cases and the 300 random strings as the statement reads, every substring
whose letters form a set of one, and its output is the same. Every arm
gives the same output under `karac run` and `karac build`.

The Mend loop: three Kāra arms take no fixes. The chunks arm takes one:
`chunk_by` returns a `Vec` of runs (docs/library/collections.md), which
takes `.into_iter()` before `map`. The Rust arms take one round each, 6
fixes apiece: `struct Solution;` to `struct Solution {}`; `s.as_bytes()`
to `s.bytes()`; `&str` to `Str`; `Solution::` to `Solution.`; the
harness's `as i64` dropped, since `i32` widens to `i64` by itself; and
`&&` to `and` in the loop arm, `.into_iter()` after `chunk_by` in the
chain arm. Both arms' outputs match on the first run. No compiler gap came
up.

The differential took one fix as first written, a `.clone()` dropped from
an argument the callee only borrows, and takes none now.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every substring `s[i..j]`, its letters gathered into a `Set`,
counted when the set holds one letter. 400 random strings of 1 to 30
letters over the first 1 to 4; the first five have one letter and the
first ten one distinct letter.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the string read backwards gives the same count |
| P3 | the letters renamed by a random permutation of the alphabet give the same count |
| P4 | every letter doubled turns a run of `k` into one of `2k`, so the count becomes four times as many less the string's length |
| P5 | the last letter dropped takes away as many substrings as the run ending there is long |
| P6 | the ★ arm's answer |

All 14,400 checks pass on every arm: `400 strings: checksum 138068842,
14400 checks over 6 arms: 0 failures`, in 1.3 s under `karac __mir-run`,
and the same under `karac __mir-llvm-run` and `karac build`.

## Mutation testing

Eighteen edits to the differential, three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All eighteen are caught.

| # | mutation | failures by property |
|---|---|---|
| A1 | ★: a run grows by two a letter | P1 361, P4 400, P5 203, P6 1805 |
| A2 | ★: one substring for each position | P1 361, P4 400, P5 203, P6 1805 |
| A3 | ★: a new run starts one short | P1 400, P4 400, P5 400, P6 2000 |
| U1 | runs: a run's single letters not counted | P1 400, P4 400, P5 400, P6 400 |
| U2 | runs: a rising stretch taken as one run | P1 269, P2 208, P3 187, P5 268, P6 269 |
| U3 | runs: the letter after each run skipped | P1 273, P2 166, P4 247, P5 174, P6 273 |
| B1 | brute: a start's later equal letters counted past a different one | P1 259, P5 258, P6 259 |
| B2 | brute: the first start skipped | P1 400, P2 135, P4 400, P5 127, P6 400 |
| B3 | brute: substrings of one letter not counted | P1 400, P4 400, P5 400, P6 400 |
| C1 | chunks: a rising stretch taken as one run | P1 269, P2 245, P3 185, P5 150, P6 269 |
| C2 | chunks: each run's count `n * n / 2` | P1 400, P4 400, P5 273, P6 400 |
| C3 | chunks: only the largest run's count | P1 273, P4 273, P5 243, P6 273 |
| X1 | solution: the second letter never extends a run | P1 203, P2 135, P4 400, P5 110, P6 203 |
| X2 | solution: each position one substring short | P1 400, P4 400, P5 400, P6 400 |
| X3 | solution: a run never restarts | P1 394, P2 242, P4 400, P5 378, P6 394 |
| R1 | chain: each run's count doubled | P1 400, P4 400, P5 400, P6 400 |
| R2 | chain: each run one letter short | P1 400, P4 400, P5 400, P6 400 |
| R3 | chain: runs of unequal neighbours | P1 374, P4 400, P5 383, P6 374 |

A mutation of the ★ arm fails P6 on every arm, since P6 compares each arm
with the ★ arm; P1, P4 and P5 name the ★ arm itself. A1 and A2 fail the
same checks: both are wrong exactly when a run is longer than one letter.
P3 catches only U2 and C1, which take a rising stretch for a run and so
depend on which letter is which; P2 catches those and U3, B2, X1 and X3,
which treat one end of the string unlike the other. Three more edits look like faults and pass all
14,400 checks under both backends, since they are equivalent: the runs arm
starting `j` one past `i` (the letter at `i` always repeats itself), the
same arm stepping `i` to at least `i + 1` (`j` is always past `i`), and
the ★ arm comparing the first letter with byte 1 rather than 0 (no letter
is either).

## Benchmarks

`bench/` times the ★ arm against the same one-pass count in C, Rust, Go
and Python: 1000 strings of 1000 letters, the constraints' most, each over
the first 1 to 4 letters, built once, then 100 rounds over all of them,
every answer folded into a checksum. Every program prints `100 rounds of
1000 strings: checksum 248994674`.

Timings on a 4-core container (Intel Xeon, 2.3 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac `ace8f2a6e8`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.254 to 0.321 s | 0.278 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.253 to 0.300 s | 0.276 s |
| Rust (`rustc -O`) | 0.032 to 0.056 s | 0.036 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.257 to 0.301 s | 0.270 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.252 to 0.316 s | 0.267 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.039 to 0.077 s | 0.040 s |
| C (`clang -O3`) | 0.040 to 0.074 s | 0.044 s |
| Go | 0.244 to 0.286 s | 0.251 s |
| Python | 3.78 to 3.80 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; user time is within 2% of wall time for both Kāra
rows, so both ran on one core. Kāra takes about 1.03x the time of
overflow-checked Rust built for the same baseline, the equal-safety
comparison, 6.9x C's and 1.10x Go's; Python takes about 14x. The loop is
100 million letters, each a compare and two adds. Rust without overflow
checks takes 0.036 s, 0.13x its checked build and about C's time, so the
checked adds are nearly all of the gap to C: unchecked, the loop runs at
under half a nanosecond a letter, which suggests the compilers turn it
into something other than one letter at a time, but that was not
profiled. Go does not check overflow either and still takes about Kāra's
time; why was not profiled.
