# 389. Find the Difference

String `t` is made by shuffling string `s` and adding one more letter at
a random position. Return the letter that was added.

```
s = "abcd", t = "abcde"  -> 'e'
s = "",     t = "y"      -> 'y'
```

**Constraints:** `0 <= s.len() <= 1000`; `t.len() == s.len() + 1`;
both hold lowercase English letters only.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `find_the_difference.kara` ★ | XOR every byte of both strings; each letter of `s` cancels its copy in `t`, leaving the added one | O(n) | O(1) |
| `find_the_difference_sum.kara` | the sum of `t`'s bytes minus the sum of `s`'s | O(n) | O(1) |
| `find_the_difference_count.kara` | count `s`'s letters in 26 slots, spend one per letter of `t`; the first letter with nothing left is the added one | O(n) | O(1) |
| `find_the_difference_sort.kara` | sort both strings' letters; the first position where they differ holds the added letter in `t`, or it is `t`'s last | O(n log n) | O(n) |
| `find_the_difference_map.kara` | the counting arm with a `Map[char, i64]`, for any characters | O(n) expected | O(k) |
| `differential.kara` | the five arms against pairs whose answer is known by construction, 3,000 random strings, five properties | — | — |

Every arm prints the same 7 lines: the two LeetCode examples, four edge
cases (an added copy of the only letter, an added copy of one letter
among two, a run of one letter grown by one, an added letter put first),
and for 3,000 random pairs (s of 0 to 60 letters) how many answers are
right, with a checksum. `find_the_difference.py` mirrors the ★ arm and
its output is byte-identical.

The map arm walks the map with
`for (c, n) in count.iter() { if *n > 0 { return *c; } }`, as the
library's iteration table types the items (`(ref K, ref V)`). Until
kara 6c7e55c2f3, `karac __mir-run` refused the `*n` (kara
`B-2026-10-12-9`) and the arm walked the map by value; it is back in
the spec form. A by-value `count.into_iter()` stopped `karac __mir-run`
at `a for loop over a collection is not lowered yet`; the MIR builder
lowered a by-value `for` over a `Map` or `Set` only when it was written
without `.into_iter()`, a gap noted for the MIR builder's owner and not
filed.

## Differential

`differential.kara` holds copies of the five arms. For each of 3,000
random strings `s` of 0 to 60 letters it builds pairs whose answer is
known.

| | property |
|---|---|
| P1 | every arm finds a random letter added at a random place, then shuffled |
| P2 | every arm finds a letter put in front of `s` without shuffling |
| P3 | every arm finds an added copy of a letter `s` already has |
| P4 | every arm finds the letter of a run of one letter grown by one |
| P5 | a second letter added to `t` is found from `t` |

It prints `3000 strings, 75000 checks, 0 failures` under
`karac __mir-run`.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | how |
|---|---|---|
| M1 | xor: skips the bytes of `s` | P1 to P5, 13185 failures |
| M2 | xor: ORs `t`'s bytes in | P1, P2, P3 and P5, 11780 failures |
| M3 | sum: adds `s`'s bytes too | P1 to P5, 14688 failures |
| M4 | count: a letter of `t` is never spent | P1 to P5, 11503 failures |
| M5 | count: answers when a count is about to run out | P1, P2, P3 and P5, 8580 failures |
| M6 | sort: returns the letter of `s` at the first difference | P1, P2, P3 and P5, 10869 failures |
| M7 | sort: no difference returns `t`'s first letter | P1, P2, P3 and P5, 948 failures |
| M8 | map: `s`'s letters are counted up, not down | P1, P3 and P5, 7898 failures |

M7 only shows when the added letter sorts last, about one pair in 13,
which is why its count is low.

## Verification

All five arms print the same output as `find_the_difference.py` under
`karac __mir-run` (the v2 MIR interpreter), and `karac check` passes on
every file. Every file also prints the same output under
`karac __mir-llvm-run`, since compiler commit 62f5f6de04 added the
`String.as_str` native. The legacy interpreter, LLJIT and
`karac build` refuse every arm at the harness's `*c` on the items of a
`Vec[char]` iterator, the frozen legacy typechecker gap of katas 382 to
388; not filed.

## Benchmarks

The bench program uses the ★ arm. It builds a pool of 1,000,000 random
letters once, then reads 8,000,000 pairs out of it without copying: `s`
is a window of 0 to 1,000 letters at a random place and `t` the same
window one letter longer, so the added letter is the one after `s` (an
input the problem allows: the letter is added at the end, and the
shuffle leaves the order unchanged). A fresh window per pair keeps the
compiler from reusing one answer across rounds, which a first version
over 200 fixed pairs let clang do (0.05 s for the whole run). Every
implementation prints
`8000000 pairs, 8000000 right, checksum 918021542`; for Kāra that was
checked on a 30,000-pair cut under `karac __mir-run`, which matches the
C program cut the same way. Spot timings on a shared 4-core container
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.57 s |
| Rust (`rustc -O`) | 0.59 s |
| Go | 4.3 s |
| Python | 183 s |

The legacy `karac build` of the Kāra program panics in codegen on the
`for` over `Str.bytes()`, as in kata 383. The MIR interpreter takes
16 s for the 30,000-pair cut. The full Kāra program prints the same
line under `karac __mir-llvm-run` in 20.7 s, compile included; that
JITs the MIR's IR without optimization passes, so it is not a
benchmark.

## Compiler findings

- **`Map`/`SortedMap` `iter()` items were typed as values** (kara
  `B-2026-10-12-9`). The library gives them as `(ref K, ref V)`.
  `for (c, n) in m.iter() { if *n > 0 { .. } }` passed `karac check`,
  but `karac __mir-run` refused the `*n`, with no location in the
  message. Kara 6c7e55c2f3 fixed the `__mir-run` side and the map arm
  uses the spec form again; the row stays open for what remains, such
  as `karac check` refusing `*p.0` on an undestructured item.