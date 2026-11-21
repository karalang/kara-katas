# 2502. Design Memory Allocator

You are given an integer `n` representing the size of a **0-indexed**
memory array. All memory units are initially free.

You have a memory allocator with the following functionalities:

1. **Allocate** a block of `size` consecutive free memory units and
   assign it the id `mID`.
2. **Free** all memory units with the given id `mID`.

**Note** that:

- Multiple blocks can be allocated to the same `mID`.
- You should free all the memory units with `mID`, even if they were
  allocated in different blocks.

Implement the `Allocator` class:

- `Allocator(int n)` Initializes an `Allocator` object with a memory
  array of size `n`.
- `int allocate(int size, int mID)` Find the **leftmost** block of
  `size` **consecutive** free memory units and allocate it with the id
  `mID`. Return the block's first index. If such a block does not
  exist, return `-1`.
- `int freeMemory(int mID)` Free all memory units with the id `mID`.
  Return the number of memory units you have freed.

```
Allocator(10); allocate(1,1) allocate(1,2) allocate(1,3) freeMemory(2)
allocate(3,4) allocate(1,1) allocate(1,1) freeMemory(1) allocate(10,2)
freeMemory(7)  ->  0, 1, 2, 1, 3, 1, 6, 3, -1, 0
```

**Constraints:** `1 <= n, size, mID <= 1000`; at most `1000` calls will
be made to `allocate` and `freeMemory`.

The approaches differ in what the allocator keeps: the owner of every
unit, the blocks held, the runs left free, or a tree over the units
that knows where its longest free run is.

## Approaches

| file | mechanism |
|---|---|
| `alloc.kara` ★ | every unit's owner in a `Vec`, 0 for free; `allocate` scans for the first run of `size` free units, `free_memory` clears every unit of the id. O(n) a call |
| `alloc_blocks.kara` | the blocks held, as (start, size, id) in order of their starts; `allocate` walks the gaps between them and inserts at the first that fits, `free_memory` sums the id's blocks and `retain`s the rest. O(blocks) a call |
| `alloc_freelist.kara` | a free list: the free runs as (start, length) in order, and a `Map` from each id to its blocks; `allocate` shortens the first run long enough, `free_memory` puts each block back where `partition_point` says and merges it with the runs it touches |
| `alloc_tree.kara` | a segment tree over the units, each node holding its longest free run and the free runs at its two ends; `allocate` descends to the leftmost run that fits, through a child or across the children's meeting ends, `self`-recursive methods throughout. O(size log n) to allocate |
| `alloc_iter.kara` | iterators over the owners: `allocate` `find`s the first start whose units are `all` free and `fill`s them; `free_memory` `filter`s `iter_mut` and clears in a `for_each` |
| `alloc_solution.kara` | LeetCode's Rust template: `struct Allocator` with `fn new(n: i32) -> Self` and `&mut self` methods in `i32`; the owners in a `vec![0; n as usize]`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm drives its allocator through the same calls, each `(0, size,
id)` an allocation and `(1, id, _)` a free, and prints the same 8
lines: LeetCode's example and three more (a single unit, a whole
memory freed and refilled, and gaps left by a free); then 2000 random
sequences of 1 to 60 calls on 1 to 50 units, an allocation of 1 to `n /
3 + 1` units two times in three, ids to 3 and to 20, each as a count of
refused allocations and a checksum; then the constraints' largest:
1000 random calls on 1000 units, sizes to 20; and 999 allocations of
one unit, then a free. `alloc.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 3000 random sequences of
1 to 25 calls on 1 to 12 units, ids to 4, against the statement read
literally, and the two agreed on every sequence.

`check` first reports 3 errors on the template: `Vec<i32>`, and the
two `&mut self` receivers. `karac fix` carries it in one call,
reporting 8 edits: the brackets; `vec![0; n as usize]` becomes
`Vec.filled(n, 0)`; `mut ref self` for both receivers; and `let size =
size as usize` becomes `size as i64`, the type a `Vec`'s length and
index already have. `-> Self` and the `as i32` on the returned start
stand.

## Differential

`differential.kara` holds copies of the six arms, each allocator
renamed after its arm, and the statement read literally: every unit's
owner, an allocation tried at every start from 0 up and taken at the
first whose `size` units are all free, and a free that counts and
clears the id's units. It checks 300 random sequences of 1 to 30 calls
on 1 to 20 units, ids to 3 or to 10; then 20 of 8 calls on one unit;
and 40 of 60 calls on 50 units. All 360 are drawn before any arm
answers; they make 4867 allocations, of which the statement refuses
2246.

| | property |
|---|---|
| P1 | every answer is the statement read literally |
| P2 | an allocation answers -1 or a start from 0 to `n - size`, a free from 0 to `n`, and no more is ever freed than was allocated |
| P3 | every id `d` written `1001 - d`: the same answers |
| P4 | a free of an id never used, first: 0, then the same answers |
| P5 | twice the units and every size doubled: every start and every count doubled, -1 kept |
| P6 | each arm agrees with at least three of the other five |

P5 holds because every block then starts at an even unit and covers an
even number of them, so every free run does too, and a run of `2 size`
free units starts at `2 s` exactly when one of `size` starts at `s`.

The differential prints `360 cases, 2246 refusals: checksum 769441241,
12960 checks over 6 arms: 0 failures` under every lane in Verification;
the checksum of the literal answers was checked against a Python
reading that builds the same cases and runs the same scan. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a run counted across held units | P1 118, P6 118 |
| M2 | ★: the start one late | P1 356, P2 163, P5 356, P6 356 |
| M6 | ★: a run one longer needed | P1 356, P5 318, P6 356 |
| M7 | blocks: a gap one short taken | P1 292, P2 25, P5 292, P6 292 |
| M9 | blocks: the new block put last | P1 153, P2 21, P6 153 |
| M10 | blocks: a free counting blocks | P1 204, P5 256, P6 204 |
| M12 | freelist: the shortened run not moved | P1 304, P6 304 |
| M13 | freelist: an exact fit refused | P1 268, P6 268 |
| M14 | freelist: the run after never merged | P1 116, P6 116 |
| M17 | tree: the meeting ends never asked | P1 299, P5 303, P6 299 |
| M18 | tree: the prefix never extended | P1 97, P5 124, P6 97 |
| M19 | tree: the suffix never extended | P1 168, P5 224, P6 168 |
| M22 | iter: the last start never tried | P1 236, P6 236 |
| M23 | iter: the id's own units counted free | P1 284, P6 284 |
| M24 | iter: the block's last unit left free | P1 342, P5 342, P6 342 |
| M29 | solution: the start one later | P1 356, P2 236, P5 356, P6 356 |
| M31 | solution: freed begun at 1 | P1 330, P2 237, P4 360, P5 330, P6 330 |

P1 and P6 kill all seventeen, P5 ten, P2 five, and P4 one, the
template's freed begun at 1, whose leading free answers 1. P3 kills
none: every arm uses an id only to compare it with another, and no
edit touches one, so renaming the ids cannot show an edit; the
property stays as a check on that.

Fourteen are not kept, and none survives. Five fail exactly as a kept
one: the ★ arm's block's last unit left free and the template's block
written one short (M3, M28) as the iter arm's block's last unit left
free (M24); the blocks arm's end gap one short refused (M8) as the iter
arm's last start never tried (M22); the free list's free counting
blocks (M16) as the blocks arm's (M10); and the template's count kept
across held units (M27) as the ★ arm's run counted across them (M1).
Six fail as one another, in two sets: the ★ arm's free that counts
nothing and the iter arm's count never kept (M4, M25), every free
answering 0; and the ★ arm's free that leaves the units held, the
blocks arm's blocks never let go, the iter arm's free that clears
nothing, and the template's free counted but not cleared (M5, M11, M26,
M30), no unit ever coming back, which P2 sees as more freed than was
ever allocated. Three fail in ways of their own, but their arms
already hold their kept edits: the free list's run before never merged
(M15), and the tree arm's longest run blind to the meeting ends and
freed unit left marked in the tree (M20, M21).

## Verification

Every arm prints the same output as `alloc.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.9 to 7.2 s and the differential 4.1 s; under `karac __mir-llvm-asan` the arms take 0.6 to 1.8 s and the differential 1.3 s; and under `karac run` the differential takes 0.7 s.

## Benchmarks

The bench makes 400 sessions, each a fresh allocator of 1000 units and
1000 calls. Each call is an allocation of 1 to 20 units when the next
draw of its own generator plus the checksum so far leaves 0 or 1 by 3,
and otherwise a free; ids run to 50. Each answer, plus 1 plus the
session, is folded into the checksum. The bench uses the ★ arm in all
five languages, each scanning an array of owners. Every implementation
prints `400 sessions of 1000 calls on 1000 units: checksum 79671663`.

BENCHTAB
