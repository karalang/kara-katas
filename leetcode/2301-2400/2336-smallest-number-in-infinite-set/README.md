# 2336. Smallest Number in Infinite Set

You have a set which contains all positive integers `[1, 2, 3, 4, 5,
...]`.

Implement the `SmallestInfiniteSet` class:

- `SmallestInfiniteSet()` Initializes the **SmallestInfiniteSet** object
  to contain **all** positive integers.
- `int popSmallest()` **Removes** and returns the smallest integer
  contained in the infinite set.
- `void addBack(int num)` **Adds** a positive integer `num` back into
  the infinite set, if it is **not** already in the infinite set.

```
["SmallestInfiniteSet", "addBack", "popSmallest", "popSmallest", "popSmallest",
 "addBack", "popSmallest", "popSmallest", "popSmallest"]
[[], [2], [], [], [], [1], [], [], []]
->  [null, null, 1, 2, 3, null, 1, 4, 5]
```

**Constraints:** `1 <= num <= 1000`; at most `1000` calls will be made
**in total** to `popSmallest` and `addBack`.

The set is everything from some number on, plus a few numbers below it
that were added back. So a cursor `next`, every number from which is
still in the set, and an ordered set of the numbers added back below
it, describe it exactly: popping takes the least added-back number if
there is one, and otherwise `next`, moving it on; adding back a number
below `next` puts it in the ordered set, and one at or past `next` is
already there.

## Approaches

| file | mechanism |
|---|---|
| `infinite.kara` ★ | a cursor and a `SortedSet[i64]` of the numbers added back below it: popping takes its `min` or the cursor. O(log n) a call |
| `infinite_naive.kara` | a `Vec[bool]` of which numbers are popped, grown as the pops reach past its end: popping walks it from 1 to the first not popped, and adding back clears the mark. O(n) a pop |
| `infinite_heap.kara` | a cursor and a `PriorityQueue` of the numbers added back below it, with a `Set` beside it so that none goes in twice. O(log n) a call |
| `infinite_sorted.kara` | a cursor and a `Vec` of the numbers added back below it, kept from largest to least: each placed where `partition_point` finds and skipped when it is there, and the least popped off the end. O(n) an add back |
| `infinite_iter.kara` | iterators: a `Set` of the numbers popped and not added back, and popping the first number from 1 that `find` sees missing from it, which comes within one past its size. O(n) a pop |
| `infinite_solution.kara` | LeetCode's Rust template: a cursor and a `BTreeSet<i32>` read through `iter().next()` with a `&x` pattern, under `&mut self` methods; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

The harness runs a sequence of calls on a fresh set, written as numbers:
0 for `popSmallest` and `n` for `addBack(n)`, and gives what the pops
returned. Every arm prints the same 5 lines: LeetCode's example; pops
alone; a number added back while still in the set; 1000 pops with
every tenth popped number added back, its last pop and their sum; then
2000 random sequences of 1 to 40 calls, half of them pops, numbers
added back from 1 to 30, with a checksum of every pop and their count.
`infinite.py` mirrors the ★ arm, its ordered set a sorted list kept by
`bisect`, and its output is byte-identical.

The ★ arm was first written with Rust's `mut self` receivers and its
`BTreeSet`'s `first()`. `karac check` refuses the receivers, a writing
receiver being `mut ref self`, and `karac fix` rewrote them and
`first()` to the `SortedSet`'s `min().cloned()`, four edits.

`karac fix` carries the template in one call, reporting 13 edits.
`check` first reports eight errors and offers 10 edits for them: the
`use std::collections::BTreeSet;` line deleted, since `SortedSet` is in
the prelude; the brackets of `BTreeSet<i32>`; `BTreeSet::new` and
`SmallestInfiniteSet::new` to `.`; the two `&mut self` to
`mut ref self`; `Some(&x)` from `iter().next()` to `Some(x)` from
`iter().next().cloned()`, two edits; and the `&` of
`self.added.remove(&x)` dropped. The other three follow from those:
`BTreeSet` to `SortedSet` in the type and the call, and, in the
harness, the `as i64` on the `i32` pop dropped, since it widens on its
own. `fn new() -> Self` and the `op as i32` handed to `add_back` stand
as Kāra.

## Differential

`differential.kara` holds copies of the six arms, each struct renamed
for its arm, and the statement read literally: the set holds every
positive integer, of which a sequence of `c` calls can only reach 1 to
`c + 1`, so a `Set[i64]` starts with those; `popSmallest` removes and
gives its `min`, and `addBack` inserts. No cursor and no order kept. It
checks 300 random sequences of 1 to 40 calls, half of them pops,
numbers added back from 1 to 30; then 30 of up to 300 calls, three in
four pops, numbers up to 100; then 30 of up to 100 calls, three in four
add backs, numbers up to 10. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the pops are the literal reading's |
| P2 | every pop is at least 1, and no number is popped twice without an add back of it between |
| P3 | each add back made twice in a row: the same pops |
| P4 | an add back of 1000, never popped, after every call: the same pops |
| P5 | a pop right after adding back `n` gives at most `n` |
| P6 | each arm agrees with at least three of the other five |

P3 and P4 are the "if it is not already in the set" of `addBack`: a
second add back of the same number, and one of a number never taken
out, change nothing.

The differential prints `360 sequences: checksum 827252444, 12960
checks over 6 arms: 0 failures` under every lane in Verification; the
checksum of the literal pops was checked against a Python reading that
builds the same sequences and takes the `min` of a Python `set`. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the cursor never advanced | P1 333, P2 333, P6 333 |
| M3 | ★: a number added back never taken out | P1 222, P2 222, P6 222 |
| M6 | ★: the cursor starting at 2 | P1 339, P6 339 |
| M8 | naive: an add back marking the number popped | P1 245, P5 205, P6 245 |
| M9 | naive: a number past the end never marked | P1 314, P2 314, P6 314 |
| M11 | naive: the number below added back | P1 241, P2 219, P5 60, P6 241 |
| M12 | heap: the largest added back popped first | P1 100, P5 70, P6 100 |
| M13 | heap: a popped number left marked queued | P1 95, P5 71, P6 95 |
| M15 | heap: the cursor read after it moves | P1 350, P5 49, P6 350 |
| M18 | sorted: a number added twice | P1 35, P2 35, P3 221, P6 35 |
| M19 | sorted: any number added back | P1 324, P2 83, P4 235, P6 324 |
| M21 | sorted: each number placed one further on | P1 78, P2 16, P3 67, P5 4, P6 78 |
| M22 | iter: the search starting at 2 | P1 350, P5 64, P6 350 |
| M23 | iter: the largest number missing | P1 83, P5 50, P6 83 |
| M24 | iter: the number above added back | P1 241, P2 215, P5 189, P6 241 |
| M27 | solution: a number at the cursor added back | P1 90, P2 90, P6 90 |
| M31 | solution: the cursor starting at 0 | P1 350, P2 350, P6 350 |

P1 and P6 kill all seventeen, P2 ten, P5 nine, P3 two and P4 one. P2,
no number popped twice without an add back between, fails where an
edit lets a number out twice: the cursor never advanced or starting at
0, a number added back never taken out, one at the cursor added back,
one past the end never marked. P5, a pop right after adding back `n`
giving at most `n`, fails where an edit pops the wrong end of what was
added back or skips past it: the largest first, the cursor read late,
an add back marking the number popped. P3, each add back made twice,
fails only where a second add back is not a no-op: a number added
twice to the sorted arm's list, and each placed one further on. P4,
an add back of 1000 after every call, fails only where a number not
yet popped can be added back, which the sorted arm's any number added
back allows.

Of the thirty-one, fourteen were not kept. A number at the cursor added
back fails alike in the ★ (M1), heap (M16), sorted (M20) and template
(M27) arms, and only the template's is kept. The largest added back
popped first fails alike in the ★ (M4), heap (M12), sorted (M17, the
list kept least first) and template (M28) arms, and only the heap
arm's is kept. The ★ arm's any number added back (M5) fails as the
sorted arm's (M19); its cursor never advanced (M2) as the naive arm's
walk stopping one short (M10) and the iter arm's popped number not
recorded (M25) or recorded one higher (M26); its number added back
never taken out (M3) as the template's (M30). The naive arm's walk
starting at 2 (M7) fails as the iter arm's search starting at 2 (M22),
the heap arm's number queued twice (M14) as the sorted arm's number
added twice (M18), and the template's cursor read after it moves (M29)
as the heap arm's (M15).

## Verification

Every arm prints the same output as `infinite.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.2 to 0.4 s but the iter arm,
whose every pop hashes each number up to the one it finds, 0.8 s. The
differential takes 1.9 s there and 0.5 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds a sequence of `2 * 10^5` calls once from a scramble
that never repeats, two in three pops and the rest adding back a number
from 1 to 5000, then runs it 50 times, each on a fresh set, with the ★
arm in all five languages. Every implementation prints `50 passes over
2*10^5 calls: checksum 568313555`. The ordered set is Kāra's
`SortedSet` and Rust's `BTreeSet`, both B-trees; C, Go and Python have
none in their standard libraries, so theirs is a binary min-heap with a
flag per number, or Python's `heapq` and a `set`, for membership. The
sets differ there, the lightest being C's and Go's heaps.

BENCHTAB
