# 383. Ransom Note

Given two strings `ransom_note` and `magazine`, return whether the note
can be built from the magazine's letters, each letter of the magazine
used at most once.

```
ransom_note = "a",  magazine = "b"    -> false
ransom_note = "aa", magazine = "ab"   -> false
ransom_note = "aa", magazine = "aab"  -> true
```

**Constraints:** `1 <= ransom_note.len(), magazine.len() <= 10^5`; both
hold lowercase English letters only.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `ransom_note.kara` ★ | count the magazine's letters in 26 slots, then spend one count per letter of the note; fail when a count goes below zero | O(m + n) | O(1) |
| `ransom_note_map.kara` | the same counting with a `Map[char, i64]`, which works for any characters | O(m + n) average | O(k) for k distinct characters |
| `ransom_note_sort.kara` | sort both strings' bytes, then walk them together, matching each note byte to an equal magazine byte | O((m + n) log(m + n)) | O(m + n) |
| `ransom_note_remove.kara` | keep the magazine's bytes in a `Vec` and take each note byte out with `swap_remove` | O(m * n) | O(m) |
| `differential.kara` | the four arms against answers known by construction, 3,000 magazines, five properties | — | — |

Every arm prints the same 11 lines: the three LeetCode examples, seven
edge cases (an empty note from a non-empty and from an empty magazine, a
letter from an empty magazine, an anagram, one letter short and one
letter spare, a 16-letter anagram), and how many of 2,000 random pairs
over the letters a to f can be built, with a checksum of the answers in
order. `ransom_note.py` mirrors the ★ arm and its output is
byte-identical.

The sorting and removing arms copy the bytes with
`magazine.bytes().to_vec()`. They were first written with
`magazine.bytes().collect()`, which `karac check` refuses, since
`bytes()` is a `Slice[u8]` and not an iterator; its hint,
`magazine.bytes().iter().collect(...)`, checks, and then stops
`karac __mir-run` at `an iterator value is not lowered yet`, a gap the
MIR builder already has parked.

## Differential

`differential.kara` holds copies of the four arms as `can_count`,
`can_map`, `can_sort` and `can_remove`. For each of 3,000 random
magazines of up to 40 letters from a to h it builds notes whose answer
is known: a random part of the magazine's own letters, shuffled; one
letter repeated once more than the magazine has it; and a random note
for the arms to agree on.

| | property |
|---|---|
| P1 | a note drawn from the magazine's own letters can be built |
| P2 | a note with one letter more than the magazine has cannot |
| P3 | all four arms agree on a random note |
| P4 | a note that can be built still can after the magazine gains a letter |
| P5 | every magazine can be built from itself, and not with one more letter |

It prints `3000 magazines, 60000 checks, 0 failures` under
`karac __mir-run`.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | how |
|---|---|---|
| M1 | count: lets a count go one below zero | P2, P3 and P5, 8148 failures |
| M2 | count: the note spends nothing | P2, P3 and P5, 10275 failures |
| M3 | map: a letter with no copies left still passes once | P2, P3 and P5, 6716 failures |
| M4 | map: the note does not spend its letter | P2, P3 and P5, 5285 failures |
| M5 | sort: skips magazine bytes equal to the note byte | P1, P3 and P5, 7127 failures |
| M6 | sort: a matched magazine byte is used again | P2, P3 and P5, 5285 failures |
| M7 | remove: a found letter is not removed | P2, P3 and P5, 5285 failures |
| M8 | remove: a missing letter is skipped | P2, P3 and P5, 7425 failures |

M4, M6 and M7 are one mistake in three arms (each magazine letter can
be used any number of times), and give the same counts.

## Verification

All four arms print the same output as `ransom_note.py` under
`karac __mir-run` (the v2 MIR interpreter), and `karac check` passes on
every file. The counting and Map arms also match under
`karac run --interp`. Under `karac __mir-llvm-run` (the same MIR
compiled to LLVM) every file stops with `native String.as_str is not
lowered yet`, where a `String` is passed to a `Str` parameter; mir-llvm
is still being built out, so that is a missing native, not filed. The
legacy backends fail as Compiler findings describes.

## Benchmarks

The bench program uses the ★ arm. It builds a pool of 1,000,000 random
lowercase letters once, then checks 10,000 pairs of windows of it: a
note of 30,000 to 69,999 letters and a magazine of 40,000 to 79,999
(the problem allows 100,000). The windows are `Str` slices of the pool,
so no pair copies text. The C, Rust, Go and Python mirrors print
`6562 of 10000 can be built, checksum 138002484`, in 0.79 s, 0.82 s and
0.84 s on a shared 4-core container (spot timings; `bench.sh` timings
need a quiet machine); Python takes 56 s. The Kāra program cannot run yet: the
legacy native build stops in codegen (see Compiler findings), and
`karac __mir-llvm-run` stops at the missing `String.as_str` native.

## Compiler findings

Nothing filed. One missing native in the new compiled backend, noted
above, and two in the legacy backends, which are frozen:

- **Legacy codegen panics on a `for` over `Str.bytes()`.** LLJIT,
  `karac build` and `KARAC_AUTO_PAR=1 karac build` panic in
  `src/codegen/control_flow_for.rs` with `Found IntValue ... but
  expected the StructValue variant` on the counting and Map arms, at
  the loop over the `Str` parameter's bytes, and the bench program fails
  the same way.
- **The legacy typechecker refuses `*b` on the items of a `Vec[u8]`
  iterator.** The sorting and removing arms read `*b` and `*x` from
  `note.iter()` and `left.iter().position(...)`, and `karac run
  --interp` and LLJIT stop with `unary '*' requires 'ref T' ... found
  'u8'`; the differential stops the same way on its `Vec[char]` loops.
  `karac check` and the MIR interpreter accept both.
