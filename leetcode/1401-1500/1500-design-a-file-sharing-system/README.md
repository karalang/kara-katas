# 1500. Design a File Sharing System

A file is split into `m` chunks with ids `1` to `m`. Users join the system,
leave it, and request chunks from each other. Implement `FileSharing`:

- `FileSharing(m)` starts the system for a file of `m` chunks.
- `join(ownedChunks)` gives a joining user the smallest positive id no
  current user holds (ids of users who left are given out again), records
  the chunks it owns, and returns the id.
- `leave(userID)`: the user leaves, and its chunks go with it.
- `request(userID, chunkID)` returns the sorted ids of every user owning
  the chunk. If the list is not empty, the requester now owns it too.

```
FileSharing(4)
join([1, 2]) -> 1      join([2, 3]) -> 2      join([4]) -> 3
request(1, 3) -> [2]   request(2, 2) -> [1, 2]
leave(1)               request(2, 1) -> []
leave(2)               join([]) -> 1
```

**Constraints:** `1 <= m <= 10^5`; `0 <= ownedChunks.length <= min(100, m)`;
the owned chunks are distinct and in `1..=m`; every `userID` names a user in
the system; at most `10^4` calls.

## Approaches

| file | mechanism |
|---|---|
| `files.kara` ★ | each chunk's owners in a `SortedSet`, each user's chunks in a `Vec` (so leaving touches only those sets), the ids given back by `leave` in a smallest-first `PriorityQueue`. O(log) per owner touched, O(k) to read k owners |
| `files_scan.kara` | users in a table indexed by id, a `Set` of chunks per row: a join takes the first empty row, a request reads every row in id order, so the owners come out sorted. O(users) per request and join |
| `files_sorted.kara` | each chunk's owners in a sorted `Vec` kept by a hand-written binary search, free ids in a `SortedSet` (`pop_first`) |
| `files_iter.kara` | one `Map` from user to its `Set` of chunks, read with iterators: a join's id is `(1..).find(..)`, a request is `filter`, `map`, `collect`, then `sort` |
| `files_solution.kara` | LeetCode's Rust template (`HashMap`, `BTreeSet`, `BinaryHeap<Reverse<i32>>`, `&mut self`, `if let`), carried by `karac fix` to one error: blocked by B-2026-11-08-4 |
| `differential.kara` | the four arms that check against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's example, then four batches
of random systems, each driven by random calls (30% join with random
chunks, 20% leave of a random live user, 50% request of a random chunk by
a random live user): 3000 systems of up to 6 chunks with 40 calls, 300 of
up to 30 chunks with 300 calls, 10 of up to 100000 chunks with 3000 calls,
and 4 of up to 5 chunks with 5000 calls. Each batch prints its counts of
joins, requests and owners returned and a checksum of every answer in
order. `files.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms that check, behind one
`Sharing` trait driven by a generic `trace`, and the statement read
literally: users in a list in join order, a join's id found by counting up
from 1 past the ids in use, a request's owners filtered from the list and
sorted. It checks 1000 problems of 1 to 6 chunks and 1 to 30 calls. A
problem's calls are drawn before any arm runs: a join's chunks, and for a
leave or request an index into the arm's own list of live ids, so each arm
picks users from the ids it gave out. An arm's trace is every join's id
and every request's answer, in order.

| | property |
|---|---|
| P1 | the trace is the statement read literally |
| P2 | the chunks renamed one-to-one leave the trace |
| P3 | every join returns the smallest positive id not live |
| P4 | every answer is strictly ascending and names only live users |
| P5 | a request repeated at once by the same user returns the first answer with that user in it, when the first was not empty |
| P6 | each arm agrees with at least two of the other three |

The differential prints `1000 problems: checksum 911704098, 24000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property. The Rust-template arm
joins it, as a fifth, once it checks.

## Mutation testing

Twenty-three edits to the differential, five to each arm and eight to the
iterator arm, each run under `karac __mir-run` and `karac
__mir-llvm-run`. Twelve are kept, three to each arm. All twenty-three are
killed and each fails the same way under both backends; one of them by a
crash. No two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the requester never recorded as owning what it got | P1 150, P4 115, P6 150 |
| M2 | ★: a request hands the chunk over even when no one owns it | P1 517, P6 517 |
| M3 | ★: new ids start at 2 | P1 1000, P3 1000, P6 1000 |
| M4 | scan: owners collected highest id first | P1 545, P4 545, P5 587, P6 545 |
| M5 | scan: `leave` does nothing | P1 787, P3 776, P4 577, P6 787 |
| M6 | scan: the requester left out of its own answer | P1 700, P5 640, P6 700 |
| M7 | sorted: the requester added again when it already owns the chunk | P1 313, P5 520, P6 313 |
| M8 | sorted: a join takes the largest free id | P1 348, P3 348, P6 348 |
| M9 | sorted: `leave` removes each chunk's first owner, not the leaver | P1 298, P4 270, P6 298 |
| M10 | iter: a join records only its first chunk | P1 549, P6 549 |
| M11 | iter: the chunk handed over only when two or more own it | P1 295, P5 480, P6 295 |
| M12 | iter: `leave` removes user `min(id, 2)` | P1 359, P3 267, P4 287, P5 121, P6 359 |

P1 and P6 kill all twelve, P5 five, P3 four, P4 five, and P2 none. P2 is
blind by construction: no arm reads a chunk id except to look it up or
compare it for equality, so a one-to-one renaming keeps every answer. It
stays as a guard on that fact.

The other eleven fail as a kept one does, or by a crash. The ★ arm never
freeing an id and the sorted arm never freeing one fail alike; the ★ arm's
`leave` leaving the owners' sets alone fails as M1 with counts of its own.
The scan arm starting its free-row search at 2 fails as M3 does with other
counts, and the iterator arm's first five edits (answer reversed, ids from
2, `leave` doing nothing, requester left out, no hand-over) fail exactly as
the scan arm's matching edits do: both arms read every user per request. The
sorted arm's join pushing an owner at the end instead of in order leaves a
list unsorted, and a later `remove` at its binary-searched place runs out of
bounds under both backends: the one crash.

## Rust template

The Rust arm was written as LeetCode's Rust template plus a thin wrapper
from the harness's `i64` calls to its `i32` ones. `karac fix` carries it in
three rounds (39 edits, then 11, then 1) to one error it has no fix for:
the field `free: BinaryHeap<Reverse<i32>>` becomes
`PriorityQueue[Release[i32]]`. The fix drops `Reverse` around the heap's
items (`push(Reverse(id))`, `Some(Reverse(id))`) and builds a
smallest-first `PriorityQueue`, but in the type it takes the resolver's
did-you-mean for an unknown type, `Release` (an atomic ordering), where
the item type alone, `i32`, is meant. With that one type written by hand
the arm checks and prints the ★ arm's output. B-2026-11-08-4 tracks it.

## Benchmarks

The bench runs one batch: 40 systems of up to 2000 chunks, 40000 calls
each, joins owning up to 30 chunks, in all five languages with the same
structure: each chunk's owners in a sorted array kept by binary search,
each user's chunks in an array indexed by id, free ids in a min-heap
(`bench/files.kara`; C writes its own heap). Every implementation prints
`40 systems of up to 2000 chunks, 40000 calls each: 478929 joins, 800547
requests, 91464790 owners returned, checksum 457821312`. The work is
mostly copying owner lists into answers (91 million ids) and shifting
sorted arrays on insert.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `92cb060c1` on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 1.010 to 1.124 s | 1.052 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.932 to 1.097 s | 1.063 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.029 to 1.137 s | 1.075 s |
| Rust (`rustc -O`) | 1.018 to 1.149 s | 1.087 s |
| C (`clang -O3`) | 1.007 to 1.245 s | 1.158 s |
| Go | 1.749 to 1.845 s | 1.806 s |
| Python | 15.7 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (1.025 s) is below its real time (1.032 s).

Kāra is level with Rust under overflow checks (0.99x by median), inside
the spread of every native language but Go.

## Verification

Every arm but the Rust template prints the same output as `files.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check` reports nothing on any of
them. Under `karac __mir-run` the arms take 6.7 s (sorted) to 11.0 s (★),
but the iterator arm 25.6 s, and the differential 3.4 s.

## Writing it

The arms were written in Kāra. `karac fix` made four kinds of edit: `!`
before a bool is `not` (applied by hand from the parse error, which has no
fix), a join's `chunks` stored in the struct takes `own Vec[i64]` (by
hand, from the error's help), a `ref Vec[i64]` parameter is a bare one,
and `*` on an `i64` closure parameter of a `Copy` iterator goes.
