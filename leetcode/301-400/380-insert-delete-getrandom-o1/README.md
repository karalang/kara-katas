# 380. Insert Delete GetRandom O(1)

Implement a set of integers with:

- `insert(val)`: add `val` if it is absent; return whether it was added;
- `remove(val)`: remove `val` if it is present; return whether it was
  removed;
- `get_random()`: return an element, each with the same probability;
  it is only called on a non-empty set.

Each operation should take O(1) time on average.

```
insert(1) -> true, remove(2) -> false, insert(2) -> true,
get_random() -> 1 or 2, remove(1) -> true, insert(2) -> false,
get_random() -> 2
```

**Constraints:** `-2^31 <= val <= 2^31 - 1`; at most `2 * 10^5` calls.

## Approaches

The values live in a `Vec`, so a random element is a random position.
Removing a value moves the last value into its slot and pops the end,
so the `Vec` never has a hole and only the moved value's position
changes. Every arm keeps this layout and draws positions from the same
seeded LCG, so the same calls give the same draws in every arm; the
arms differ in how they find a value's position.

| file | finding a position | insert / remove | get_random |
|---|---|---|---|
| `randomized_set.kara` ★ | a `Map[i64, i64]` from value to position | O(1) average | O(1) |
| `randomized_set_sorted.kara` | a `SortedMap[i64, i64]` | O(log n) | O(1) |
| `randomized_set_scan.kara` | no index: scan the `Vec` | O(n) | O(1) |
| `randomized_set_probe.kara` | an open-addressing table written out: a multiplicative hash picks the home slot, collisions probe forward, deletion shifts later entries of the run back into the gap (no tombstones), and the table doubles when half full | O(1) expected | O(1) |
| `differential.kara` | the four arms against a membership oracle, 1,000 workloads of 300 operations, five properties | — | — |

Every arm prints the same 8 lines: the LeetCode example over three
lines (the first draw is printed as whether it is 1 or 2, since the
problem allows either), three edge cases (removing from an empty set,
negative values, removing the only value), the sum of 100 draws after
removing values from both ends and the middle of the `Vec`, and a
checksum over 100 random workloads of 1,000 operations on values from
-50 to 49. `randomized_set.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms behind one enum and
drives all four with the same operations. The oracle is one flag per
value.

| | property |
|---|---|
| P1 | `insert` and `remove` answer as the oracle does |
| P2 | `get_random` returns a value in the set |
| P3 | all four arms draw the same value |
| P4 | `len()` is the oracle's count |
| P5 | after each workload, 20 draws per element reach every element |

It prints `1000 workloads, 2965456 checks, 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`. The legacy backends cannot
run it; see Compiler findings.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | how |
|---|---|---|
| M1 | map: the moved value keeps its old position | P2, P3 and P5, 36385 failures |
| M2 | map: `get_random` never draws the last position | P3 and P5, 278566 failures |
| M3 | sorted: `insert` does not check for the value | P1 to P5, 374828 failures |
| M4 | sorted: a value removed next to the end is not filled | P1 to P5, 19314 failures |
| M5 | scan: the search skips position 0 | P1 to P4, 228478 failures |
| M6 | probe: an entry whose home is the end of the run stays put | P1 to P5, 185391 failures |
| M7 | probe: a moved entry is also left where it was | P1 to P5, 16805 failures |
| M8 | oracle: every insert is new | P1 and P4, 1154248 failures |

## Verification

All four arms print the same output as `randomized_set.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run` (the
same MIR compiled to LLVM) and `karac run --interp`, and `karac check`
passes on every file. The scanning and open-addressing arms also match
under LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac build`; the `Map`
and `SortedMap` arms stop there with a double free (see Compiler
findings).

## Benchmarks

The bench program uses the open-addressing arm, the one every mirror
language can write the same way; the other arms lean on each language's
own hash map, whose hashing and probing differ. It drives one set with
20,000,000 random operations on values from 0 to 199,999, a third each
insert, remove and `get_random`, which keeps about half the values in
the set. The C, Rust, Go and Python mirrors print
`checksum 828319335 size 100176`, and so does `karac __mir-llvm-run`.
On a shared 4-core container it takes 2.7 s, compile included, against
1.1 s for `cc -O2`; these are spot timings, and `bench.sh` timings need
a quiet machine. `karac build` (the legacy backend) prints the right
checksum but slows down much faster than the work grows: 0.7 s at
20,000 operations, 4.1 s at 40,000 and 23.6 s at 80,000, against
0.41 s, 0.41 s and 0.46 s under `karac __mir-llvm-run`. The full run
was stopped after 10 minutes.

## Compiler findings

Nothing filed. One gap in the v2 MIR builder, fixed by its owner
without a ledger row, and four in the legacy backends, which are frozen:

- **An enum variant named `Map` hid the `Map` type in the MIR build.**
  `differential.kara` wraps the arms in
  `enum AnyArm { Map(MapArm), Sorted(SortedArm), Scan(ScanArm), Probe(ProbeArm) }`,
  and `Map.new()` inside `MapArm.new` failed with `a call with no
  resolved callee is not lowered yet`. Fixed in kara `b3c895e9fa`; the
  differential now runs under both MIR backends.
- **Legacy codegen double-frees in the `Map` and `SortedMap` arms.**
  LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac build` print the
  first lines and then stop with `free(): double free detected in tcache
  2`.
- **The legacy backends cannot run the differential.**
  `karac run --interp` panics in `src/interpreter/method_call_seq.rs`,
  where a `len()` call reaches the builtin on an enum value, and the
  `karac build` binary ends with a segmentation fault.
- **`karac check` puts the arms in a false mutual-recursion group.** It
  notes that `AnyArm.insert`, `MapArm.insert` and `SortedArm.insert`
  form a recursion group resolved by fixed-point inference, and the
  same for `remove`. None of them calls `AnyArm`; `MapArm.insert` calls
  `self.index.insert` on its `Map`. It is a note, not an error, and it
  comes from the legacy effect checker; the v2 effect pass
  (`karac __mir-effects`) does not report it.
- **The legacy build of the bench slows down much faster than the work
  grows**, as the Benchmarks section measures. Its checksums are
  right. Not narrowed further.
