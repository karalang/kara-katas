# 379. Design Phone Directory

Design a directory that hands out the numbers `0` to `maxNumbers - 1`:

- `get()` returns a number that is not in use and marks it in use, or
  `-1` if every number is in use;
- `check(number)` returns whether `number` is free;
- `release(number)` frees `number`; releasing a free number does
  nothing.

```
PhoneDirectory(3)
get() -> 0, get() -> 1, check(2) -> true, get() -> 2,
check(2) -> false, release(2), check(2) -> true
```

**Constraints:** `1 <= maxNumbers <= 10^4`; `0 <= number < maxNumbers`;
at most `2 * 10^4` calls.

## Approaches

LeetCode lets `get()` return any free number. Every arm here returns
the smallest, so that all four print the same thing; the example reads
the same either way.

| file | mechanism | get | check | release |
|---|---|---|---|---|
| `phone_directory.kara` ★ | a `SortedSet` of free numbers: `get` takes its minimum | O(log n) | O(log n) | O(log n) |
| `phone_directory_heap.kara` | a min-first `PriorityQueue` of free numbers and a `Vec[bool]` of numbers in use; `release` pushes a number back only if it was in use, so the queue never holds one twice | O(log n) | O(1) | O(log n) |
| `phone_directory_bits.kara` | a bitset of numbers in use: `get` skips full words and takes the lowest clear bit of the first one that is not, with `(~word).trailing_zeros()`; the bits past the end start set, so the last word is full exactly when every real number is in use | O(n / 64) | O(1) | O(1) |
| `phone_directory_tree.kara` | a segment tree over the numbers, padded to a power of two, each node counting the free numbers below it; `get` walks down, going left whenever the left child has a free number | O(log n) | O(1) | O(log n) |
| `differential.kara` | the four arms against a scanning oracle, 1,000 directories of 200 operations each, five properties | — | — | — |

Every arm prints the same 7 lines: the LeetCode example over two
lines, four edge cases (one number, releasing a number twice, releasing
a free number, the smallest free number coming first after two
releases), and a
checksum over 100 random directories of up to 1,000 numbers driven by
1,000 operations each: half gets, a quarter checks and a quarter
releases. `phone_directory.py` prints the same 7 lines; it keeps the
free numbers in a sorted list, since Python has no sorted set.

## Differential

`differential.kara` holds copies of the four arms behind one enum, and
an oracle that keeps a flag per number and scans for the smallest free
one. It runs 1,000 random directories of up to 40 numbers, each driven
by 200 operations with the same mix as above, applying every operation
to all five.

| | property |
|---|---|
| P1 | every operation gives the oracle's result |
| P2 | a number just handed out is no longer free |
| P3 | a number just released is free |
| P4 | `get()` returns `-1` exactly when every number is in use, as the test has counted |
| P5 | the numbers handed out and not released are distinct and in range |

It prints `1000 directories, 1839908 checks, 0 failures` under
`karac __mir-run`. `karac __mir-llvm-run` cannot run it yet, because
`SortedSet.min` is not lowered there, and the legacy backends refuse
the `*n` in the set copy; see Verification and Compiler findings.

## Mutation testing

Eight edits to the copies inside `differential.kara`, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | how |
|---|---|---|
| M1 | set: `get()` leaves the number free | P1, P2, P4 and P5, 330688 failures |
| M2 | set: the last number never starts free | P1 and P4, 9673 failures |
| M3 | heap: releasing a free number pushes it again | P1, P4 and P5, 40716 failures |
| M4 | heap: `release()` leaves the in-use flag set | P1, P3, P4 and P5, 56132 failures |
| M5 | bits: the bits past the end start clear | P1, P4 and P5, 111492 failures |
| M6 | bits: `release()` sets the bit instead of clearing it | P1, P3 and P4, 194244 failures |
| M7 | tree: goes left only when two or more numbers are free there | P1 and P5, 212279 failures |
| M8 | tree: the root's count is never updated | P1, P4 and P5, 112068 failures |

## Verification

All four arms print the same output as `phone_directory.py` under
`karac __mir-run` (the v2 MIR interpreter), and `karac check` passes on
every file. Under `karac __mir-llvm-run` (the same MIR compiled to
LLVM) the heap, bitset and tree arms match too, and the ★ arm stops
with `native SortedSet[i64].min is not lowered yet`; mir-llvm is still
being built out, so that is a missing native, not filed.

The heap, bitset and tree arms also match under the legacy backends
(`karac run --interp`, LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`). The ★ arm matched there too until it
gained `let n = *n;` (see Compiler findings): the legacy typechecker
still types `SortedSet.min()` by value and refuses the `*`. The legacy
backends are frozen, so that is not filed.

## Benchmarks

The bench program uses the segment-tree arm, because the ★ arm's
`SortedSet` has no counterpart in C or in Python's standard library and
the tree can be written the same way in every mirror language. It
drives one directory of 10,000 numbers, the problem's largest, with
20,000,000 random operations: a quarter gets, a quarter checks and half
releases, so that about half the numbers are in use and most gets walk
the tree. The Kāra build and the C, Rust, Go and Python mirrors all
print `checksum 260281127`, and so does `karac __mir-llvm-run`. Timings
are not taken yet; they need a quiet machine.

## Compiler findings

Two filed in the kara repo's bug ledger, and one in the legacy
backends, which are frozen, so it is not filed:

- **`karac fix` turns an integer `!x` into `not x`.** The bitset arm
  was first written as a Rust author would, with `!word` for the
  complement. `karac check` says that `!` is not used in Kāra and to
  use `not` instead, and `karac fix` rewrites both sites to `not`, which
  then fails with `unary 'not' requires 'bool', found 'i64'` and no
  fix. The bitwise complement in Kāra is `~`, which the arm now uses.
  Filed as B-2026-10-12-1 and fixed: a second `karac fix` now turns
  `not word` into `~ word`.
- **`SortedSet.min()` gave an `i64` where the library reference says
  `Option[ref T]`.** `let n = *n;` on the result was refused with
  `unary '*' requires 'ref T' ... found 'i64'`, while the same `*x` is
  accepted on `Vec.iter()`, `Map.get`, `Vec.first()` and
  `SortedSet.iter()`. Filed as B-2026-10-12-2 and fixed in the check
  and on the MIR path. The ★ arm now copies the number out with
  `let n = *n;` before `remove`: without it, `n` still lends from the
  set while `remove` changes it, which the MIR borrow checker refuses
  (`karac check` does not report it yet).
- **Legacy codegen panics in the differential's heap copy.** LLJIT,
  `karac build` and `KARAC_AUTO_PAR=1 karac build` stop at
  `self.used[n] = true` in `HeapDir.get` with `vec index out of bounds`,
  while the heap arm on its own runs correctly on all three, and the
  differential passed under `karac run --interp` and `karac __mir-run`.
  The copy differs from the arm only in being reached through a `match`
  on an enum of directories (`AnyDir`). Not narrowed further. This was
  measured before the set copy gained `let n = *n;`, which the legacy
  typechecker now refuses outright.
