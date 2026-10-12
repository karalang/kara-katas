# 433. Minimum Genetic Mutation

A gene string is 8 characters long, each one of `'A'`, `'C'`, `'G'` and
`'T'`. One mutation changes a single character: `"AACCGGTT"` to
`"AACCGGTA"` is one mutation. A gene bank records every valid gene, and
a gene must be in the bank to be a valid result of a mutation.

Given a start gene, an end gene and the bank, return the smallest
number of mutations that turn the start into the end, or `-1` if it
cannot be done. The start gene is valid, though it may not be in the
bank.

```
start = "AACCGGTT", end = "AAACGGTA",
bank = ["AACCGGTA","AACCGCTA","AAACGGTA"]          ->  2
```

**Constraints:** `0 <= bank.length <= 10`; every gene is 8 letters
from `A`, `C`, `G`, `T`.

## Approaches

Genes are the vertices of a graph whose edges join genes one letter
apart, and the answer is the length of a shortest path from the start
to the end through bank genes: a breadth-first search, one level per
mutation. The arms differ in how they find a gene's neighbours and how
they search.

| file | mechanism |
|---|---|
| `min_mutation.kara` ★ | breadth first; a gene's neighbours are its 24 one-letter mutants, generated as strings and looked up in a `Set` of the bank genes not yet reached. O(24 n) lookups for a bank of n |
| `min_mutation_pairs.kara` | breadth first over the bank itself: a gene's neighbours are the unreached bank genes that differ from it in exactly one place, found by comparing it with each, with one flag per gene and no set. O(8 n^2), cheaper than generating mutants for a bank as small as the problem's |
| `min_mutation_bidirectional.kara` | breadth first from both ends at once, always growing the smaller frontier, until a mutant of one frontier is in the other |
| `min_mutation_bits.kara` | the ★ search on 16-bit numbers, two bits per letter: the bank is a `Set[i64]`, and a gene's mutants are the gene with one two-bit field XORed by 1, 2 or 3, so no strings are built |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 9 lines: the three LeetCode examples, five
edge cases (an empty bank, an end not in the bank, a chain of 8
mutations, a bank holding the start, and an end with no path to it),
and for 300 random banks of up to 30 genes, most a few mutations from
the start, the number of reachable ends, the total of their answers and
a checksum of all 300 answers. The random banks are larger than the
problem's 10, to give the searches some depth. `min_mutation.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases, built as in the arms' harness: a start gene, a bank
of 0 to 30 genes, most a few random mutations from the start, and an
end drawn from the bank or not.

| | property |
|---|---|
| P1 | the answer is the reference's, a relaxation over every one-letter pair of genes until nothing changes |
| P2 | with the start added to the bank and the end in it, searching from the end to the start gives the same answer |
| P3 | a reachable answer is at least the number of places the start and end differ, and a bank holding a straight path from the start to a random gene, under noise, gives exactly that number |
| P4 | five more genes never lengthen an answer or lose a path, and the bank without the end gives -1 |
| P5 | renaming the letters and reversing every gene's places leaves the answer unchanged |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | generated: `T` is never tried | P1 136, P2 150, P3 1238, P5 134 |
| M2 | generated: the last place is never changed | P1 96, P3 1132, P5 69 |
| M3 | pairs: genes two places apart count as neighbours | P1 226, P3 1499 |
| M4 | pairs: the search stops at a level of one gene | P1 286, P2 125, P3 1500 |
| M5 | both ends: `A` is never tried | P1 159, P2 146, P3 1193, P4 7, P5 113 |
| M6 | both ends: the meeting check looks in the growing frontier | P1 362, P2 58, P3 1500, P4 3 |
| M7 | bits: a two-bit field is only XORed by 1 or 2 | P1 195, P3 1340, P5 121 |
| M8 | bits: `C` is encoded as `G` | P1 149, P3 1017, P4 73, P5 187 |

P3's straight path to a random gene is the strongest check: it needs
every letter at every place, which the random banks, grown by a few
mutations each, rarely do. P5 cannot see a mutant that treats every
letter and place alike (M3, M4, M6), since renaming and reversing
change nothing such a search depends on; it sees M2, which singles out
the last place, through the reversal. P2 misses mutants whose missing
edges are missing in both directions (M2, M3, M7, M8). P4 is the weakest:
five more genes rarely open a shorter path, so it only fails where a
mutant's wrong answer happens to change with them.

## Verification

All four arms print the same output as `min_mutation.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends:

- The three string arms and the differential do not typecheck under
  `karac run --interp`, LLJIT or `karac build`: the legacy checker does
  not take a `Str` where a `Set[String]` looks a gene up or compares it
  with a `String` (`expected 'String', found 'StringSlice'`), and it
  reads a bank gene passed to a bare, borrowing parameter as a move out
  of an index (`E_INDEX_MOVE_NON_COPY`).
- The bit arm matches under `karac run --interp`; LLJIT, `karac build`
  and `KARAC_AUTO_PAR=1 karac build` panic in the legacy code generator
  (`control_flow_for.rs`, an `i64` loop variable where a struct was
  expected).

Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. One bank of 1,000 genes grows from
`ACGTACGT`, each new gene a one-letter mutation of an earlier one, so
nearly all of it is connected; then 2,000 searches each start one
mutation away from a random bank gene and end at another, every search
building its own set from the bank as the ★ arm does. Every
implementation prints `2000 searches in a bank of 1000: 2000
reachable, checksum 339026669`; a 20-search cut of the Kāra program
under `karac __mir-run` prints the same as the C program cut the same
way.

The mirrors keep the ★ arm's structure: Rust's `HashSet<String>` hashes
with SipHash-1-3 under a random key, as Kāra's `Set` does, and Go uses
a `map[string]bool`. C has no hash table to hand, so its set is an
open-addressing table of 8-letter strings hashed with FNV-1a, with no
allocation per mutant, which is most of its lead. Spot timings on a
shared 4-core container, three runs each (`bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.42 to 0.45 s |
| Rust (`rustc -O`) | 1.32 to 1.38 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.41 to 1.51 s |
| Go | 1.30 to 1.53 s |
| Python | 4.5 to 4.7 s |

The frozen legacy `karac build` cannot build the program (see
Verification), so there is no legacy time. The Kāra program prints the
same line under `karac __mir-llvm-run` in 27 s, compile included; that
JITs the MIR's IR without optimization passes, so it is not a
benchmark.

## Compiler findings

No new findings.
