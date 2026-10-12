# 381. Insert Delete GetRandom O(1) - Duplicates allowed

Implement a multiset of integers with:

- `insert(val)`: add a copy of `val`; return whether `val` was absent
  before;
- `remove(val)`: remove one copy of `val` if there is one; return
  whether there was;
- `get_random()`: return an element, each copy with the same
  probability, so a value comes up in proportion to its count; it is
  only called on a non-empty collection.

Each operation should take O(1) time on average.

```
insert(1) -> true, insert(1) -> false, insert(2) -> true,
get_random() -> 1 with probability 2/3, 2 with probability 1/3,
remove(1) -> true, get_random() -> 1 or 2 with equal probability
```

**Constraints:** `-2^31 <= val <= 2^31 - 1`; at most `2 * 10^5` calls.

## Approaches

As in #380, the elements live in a `Vec`, so a random element is a
random position, and removing one moves the last element into its slot.
A value now has several positions. Every arm removes the copy of the
value that was inserted most recently and is still present, so all of
them lay the `Vec` out the same way, and draws from the same seeded LCG
give the same values in every arm. They differ in how they find that
copy and repair the element that moves.

| file | finding the copy to remove | insert / remove | get_random |
|---|---|---|---|
| `randomized_collection.kara` ★ | a `Map` from each value to the list of its positions, in insertion order; `slot[p]` is position p's index in its list, so the moved element's entry is fixed in O(1) | O(1) average | O(1) |
| `randomized_collection_sorted.kara` | the same lists in a `SortedMap` | O(log n) | O(1) |
| `randomized_collection_scan.kara` | no index: each element carries the number of the insert that added it, and remove scans for the copy with the largest | O(n) | O(1) |
| `randomized_collection_linked.kara` | one doubly linked list per value threaded through the positions (`older[p]`, `newer[p]`), and a `Map` from each value to its newest copy; moving an element repoints its two neighbours | O(1) average | O(1) |
| `differential.kara` | the four arms against a counting oracle, 1,000 workloads of 300 operations, five properties | — | — |

Every arm prints the same 9 lines: the LeetCode example over three
lines (the first draw is printed as whether it is 1 or 2), removing
from an empty collection, three copies inserted and then removed one by
one, the share of 2s in 400 draws from one 1 and three 2s, the sum of
100 draws after removing copies from the front, middle and end of the
`Vec`, and a checksum over 100 random workloads of 1,000 operations on
values from -10 to 9. `randomized_collection.py` mirrors the ★ arm and
its output is byte-identical.

The ★ arm was first written with `Map.get_mut`, as the library
reference documents it, and `karac check` refused every call; see
Compiler findings. It now uses `entry(val).or_insert(Vec.new())` in
`insert`, and `contains_key` with `positions[val].pop()` and
`positions[moved][k] = p` in `remove`. Go back to `get_mut` once
B-2026-10-12-3 is fixed.

## Differential

`differential.kara` holds copies of the four arms behind one enum, each
with a test helper that counts the copies of a value, and drives all
four with the same operations. The oracle is one count per value. The
values run from -5 to 4, so that most values have several copies.

| | property |
|---|---|
| P1 | `insert` and `remove` answer as the oracle does |
| P2 | `get_random` returns a value with a copy present |
| P3 | all four arms draw the same value |
| P4 | `len()` is the oracle's total |
| P5 | after each workload, every arm holds the oracle's number of copies of each value |

It prints `1000 workloads, 2794088 checks, 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`. The legacy backends cannot
run it; see Compiler findings.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed: four by the properties, four by a panic inside the
mutated copy.

| # | mutation | how |
|---|---|---|
| M1 | map: a moved element's list entry is not updated | P2, P3 and P5, 83933 failures |
| M2 | map: `insert` says new for a value with one copy already | P1, 22052 failures |
| M3 | sorted: a moved element's entry is written at index 0 | panics: the removed list entry points past the end of the `Vec` |
| M4 | scan: `remove` takes the oldest copy | P3, 40452 failures |
| M5 | scan: `insert` always says new | P1, 93688 failures |
| M6 | linked: the next older copy still points at the removed one | panics: index out of bounds |
| M7 | linked: a moved newest copy leaves the `Map` at its old position | panics: index out of bounds |
| M8 | linked: a moved copy's newer neighbour keeps its old link | panics: index out of bounds |

M4 changes nothing but which copy is removed, so only P3 sees it: the
scanning copy then lays the `Vec` out differently from the other three.

## Verification

All four arms print the same output as `randomized_collection.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run` (the
same MIR compiled to LLVM) and `karac run --interp`, and `karac check`
passes on every file. Under LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build` only the scanning arm matches; see
Compiler findings.

## Benchmarks

The bench program uses the ★ arm. It drives one collection with
20,000,000 random operations on values from 0 to 99,999, a third each
insert, remove and `get_random`; removes of an absent value fail, so
the collection grows to 868,683 elements. The Rust mirror uses
`std::collections::HashMap`, the Go mirror a built-in `map`, the Python
mirror a `dict`, and the C mirror a hand-written open-addressing table,
so the comparison includes each language's own hash map. All five print
`checksum 52748481 size 868683`. The C mirror takes 1.4 s, Rust 1.8 s, Go 2.1 s and
Python 30 s on a shared 4-core container; these are spot timings, and
`bench.sh` timings need a quiet machine. The Kāra bench program was not
run to the end: `Map.remove` is O(n) on both MIR backends
(B-2026-10-12-4), and under `karac __mir-llvm-run` the program took
0.83 s, 3.1 s and 20.1 s for 20,000, 40,000 and 80,000 operations, where
the mirrors grow linearly. The legacy native build cannot compile the ★
arm (see Compiler findings).

`get_random` draws a position as `(seed / 65536) % len`, and `seed / 65536`
is below 32,768, so above that size it reaches only the first 32,768
positions. The bench's collection is far larger, so its draws are not
uniform; every mirror draws the same way, and the program's own tests
stay below that size.

## Compiler findings

Two filed in the kara repo's bug ledger, one seen again, and four in
the legacy backends, which are frozen, so they are not filed:

- **`Map.get_mut` and `SortedMap.get_mut` are documented but missing.**
  The library reference lists
  `fn get_mut(mut ref self, key: K) -> Option[mut ref V]`, and
  `karac check`, `karac __mir-run` and `karac run --interp` all refuse
  it with `no method 'get_mut' on type 'Map'`. The ★ and sorted arms use
  `entry` and `Map` indexing instead (see Approaches). Filed as
  B-2026-10-12-3.
- **`Map.remove` is O(n) on both MIR backends.** The tables keep their
  entries in insertion order and close the gap after a remove by moving
  every later entry, and the compiled runtime also rebuilds its whole
  hash index on each remove. 20,000 removes from a `Map` take 98 s under
  `karac __mir-llvm-run` and 2.5 s under `karac __mir-run`, and each
  doubling costs four times as much. Filed as B-2026-10-12-4.
- **`or_insert_with(Vec.new)` is refused.** The library reference's own
  example for `entry`, a builtin constructor passed as a function value,
  fails with `no associated function 'new' on type 'Vec'`; already open
  as B-2026-10-06-118. `or_insert(Vec.new())` works and is what the arms
  use.
- **Legacy codegen has no `len` on the list `entry` hands back.** LLJIT,
  `karac build` and `KARAC_AUTO_PAR=1 karac build` refuse the ★ and
  sorted arms with `no handler for method 'len' on variable 'list'` at
  `self.slot.push(list.len())`.
- **Legacy codegen crashes on the linked-list arm.** LLJIT, `karac build`
  and `KARAC_AUTO_PAR=1 karac build` print nothing and end with a
  segmentation fault.
- **The legacy typechecker refuses the differential.** `*x` on the
  elements of `self.vals.iter()` in the scanning and linked copies'
  test helper is refused with `unary '*' requires 'ref T' ... found
  'i64'`, so `karac run --interp` and LLJIT stop before running.
- **`karac check` puts the arms in false mutual-recursion groups**, as
  in #380. It notes that `AnyArm.len` and every arm's `len` form a
  recursion group, and likewise `AnyArm.insert` with `LinkedArm.insert`
  and `AnyArm.remove` with four arms' `remove`. No arm calls `AnyArm`;
  each calls `len`, `insert` or `remove` on its own `Vec` or `Map`
  field, which the legacy effect checker appears to match by name. It is
  a note, not an error, and the v2 effect pass (`karac __mir-effects`)
  does not report it.
