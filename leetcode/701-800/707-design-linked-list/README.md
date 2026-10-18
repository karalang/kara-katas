# 707. Design Linked List

Design your implementation of the linked list. You can choose to use a
singly or doubly linked list. A node in a singly linked list should have
two attributes: `val` and `next`; `val` is the value of the current
node, and `next` is a pointer/reference to the next node. If you want to
use the doubly linked list, you will need one more attribute `prev` to
indicate the previous node in the linked list. Assume all nodes in the
linked list are 0-indexed.

Implement the `MyLinkedList` class: `MyLinkedList()` initializes the
`MyLinkedList` object; `int get(int index)` gets the value of the
`index`th node in the linked list, and if the index is invalid, returns
-1; `void addAtHead(int val)` adds a node of value `val` before the
first element of the linked list, and after the insertion the new node
will be the first node of the linked list; `void addAtTail(int val)`
appends a node of value `val` as the last element of the linked list;
`void addAtIndex(int index, int val)` adds a node of value `val` before
the `index`th node in the linked list, and if `index` equals the length
of the linked list, the node will be appended to the end of the linked
list, and if `index` is greater than the length, the node will not be
inserted; `void deleteAtIndex(int index)` deletes the `index`th node in
the linked list, if the index is valid.

```
MyLinkedList(); addAtHead(1), addAtTail(3), addAtIndex(1, 2), get(1),
deleteAtIndex(1), get(1)
  ->  null, null, null, 2, null, 3      (the list is 1->2->3, then 1->3)
```

**Constraints:** 0 <= `index`, `val` <= 1000; please do not use the
built-in LinkedList library; at most 2000 calls will be made to `get`,
`addAtHead`, `addAtTail`, `addAtIndex` and `deleteAtIndex`.

## Approaches

Every arm is `struct MyLinkedList` with `fn new() -> MyLinkedList`, `fn
get(self, index: i64) -> i64` and `fn add_at_head`, `fn add_at_tail`,
`fn add_at_index` and `fn delete_at_index`, each taking `mut ref self`.

| file | mechanism |
|---|---|
| `design_linked_list.kara` ★ | singly linked `shared struct Node` cells with a sentinel in front, so every insert and delete happens after some node: walk to the node before the position, then link a new node in after it or link past the one after it; a size rejects positions past the end |
| `design_linked_list_arena.kara` | doubly linked, in an arena: values and both links in parallel `Vec`s, linked by index, with sentinel slots 0 and 1 at either end and a free list of deleted slots; a walk starts from whichever end is nearer |
| `design_linked_list_vec.kara` | one `Vec`, the array list a linked list is usually compared with: `get` is an index, and `insert` and `remove` shift the values after the position |
| `design_linked_list_persistent.kara` | an immutable `shared enum List { Nil, Cons(i64, List) }`, never changed in place: inserting or deleting builds new cells for the part before the position and shares the rest, written as recursion on the position |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 7 lines: the LeetCode example; calls on an
empty list, an index one past the end, which appends, and two past it,
which does nothing; deleting the first and the last; the problem's most,
2,000 random calls, twice; 1,000 values added at the tail and every
other one deleted from the front; and 300 random sequences of 1 to
100 calls, each with a checksum. Random calls are a fifth of each kind,
with values from 0 to 1,000 and indexes from 0 to two past the size, so
some fall outside the list. `design_linked_list.py` mirrors the ★ arm
and its output is byte-identical.

The persistent arm is written to design.md § Patterns, which binds the
parts of a `shared enum` pattern as `ref`, so it reads them as `*v` and
`*rest`. `karac check` accepts that, but every v2 surface binds them by
value and refuses the `*`s (kara B-2026-10-18-30, below), so that arm
and the differential, which holds a copy of it, do not run on v2 as
written. A scratch copy of each with the `*`s removed prints the output
above and the differential's line on every v2 surface; that copy is not
committed.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: it keeps the list as
a `Vec` built afresh for every call that changes it, from the values
before the position, the new value and the values after it, and treats a
call at a position outside the list as changing nothing. 2,000 random
sequences are checked, of 1 to 60 calls of the five kinds, with values
from 0 to 1,000 and indexes from 0 to three past the size, so some fall
outside.

| | property |
|---|---|
| P1 | the answers and the list left are the definition's |
| P2 | every value v replaced by 1,000 - v, every value read back and every value left the same way, and every -1 still -1 |
| P3 | the calls at positions outside the list left out, the same answers and list |
| P4 | after the calls, `get(0)` and `delete_at_index(0)` until the list is empty read its values in order, then -1, with nothing left |

Its line is `2000 sequences (6655 reads found), 4 arms, 32000 checks,
0 failures`. As written it does not run on v2, because of the persistent
arm's `*`s (B-2026-10-18-30); the scratch copy without them prints that
line under `karac __mir-run` and `karac __mir-llvm-run` and runs clean
under `karac __mir-llvm-asan`.

## Mutation testing

Eleven edits to the differential, two or three to each arm, each run
under `karac __mir-run` on the scratch copy with the persistent arm's
`*`s removed, the one that runs on v2. All eleven are killed. Three more
edits, E1 to E3, change nothing that can be seen, and the differential
rightly reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a read of the node before the position | P1 1957, P2 1956, P3 1583, P4 1861 |
| M2 | ★: a delete refusing the last position | P1 773, P3 506, P4 1960 |
| M3 | ★: an insert refusing the end, so no tail adds | P1 1957, P3 1583, P4 1956 |
| M4 | arena: a walk from the back one node too far | P1 1831, P3 942, P4 1789 |
| M5 | arena: a delete leaving the back link | stops: index out of bounds |
| M6 | arena: a reused slot keeping its old value | P1 1541, P3 673 |
| M7 | vec: add at head appending | P1 1779, P3 1390 |
| M8 | vec: an insert refusing the end | P1 898, P3 503, P4 804 |
| M9 | persistent: a read one position late | P1 1957, P3 1583, P4 1956 |
| M10 | persistent: an insert at 0 dropping the rest | P1 1820, P3 1435, P4 1820 |
| M11 | persistent: a delete one position late | P1 1354, P3 844 |
| E1 | arena: the walk from the front kept two positions longer | 0 |
| E2 | arena: a deleted slot never reused | 0 |
| E3 | vec: no negative-index test in delete | 0 |

P1 kills every mutant that runs to the end. M5 does not run to the end:
once a delete leaves a stale back link, the next walk from the back runs
off the front sentinel's -1 link and the program stops with an index out
of bounds, which kills it too. P3 catches every one of those too, since
leaving out the calls that change nothing does not hide damage done by
the calls that do. P4 catches six, M2, M3, M4, M8, M9 and M10, whose
list read back with `get` has the wrong length or disagrees with the
same list emptied from the front; M6, M7 and M11 leave the right number
of values, in the wrong places, and read the same both ways. P2 catches
only M1, whose read at position 0 returns the sentinel's 0, a value no
call put there; the other mutants misplace or lose values without ever
inventing one, and flipping every value flips their wrong answers with
them. E1 walks from the front up to two positions further, which is
slower and still right; E2 never reuses a deleted slot, which only grows
the arena; E3 drops the vec arm's `index >= 0` test from
`delete_at_index`, which the problem's indexes never need.

## Verification

The ★, arena and vec arms print the same output as
`design_linked_list.py` under `karac __mir-run` (the v2 MIR interpreter)
and `karac __mir-llvm-run`, and run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. The persistent arm and the differential stop at MIR type checking
on `*v` (B-2026-10-18-30); the scratch copies without the `*`s pass all
three surfaces the same way. `karac check` passes all four arms, the
differential, both scratch copies and the bench program. All with the
compiler at kara `2bfc20c2ad` for the debug build and `ffe92ee37c`, a
ledger-only commit later, for the release build that runs `check` and
`__mir-run`, with runtime archives rebuilt after the last `runtime/src`
change.

The frozen legacy backends refuse the ★, arena and vec arms at
`next_random(mut seed)` inside the harness's `random_calls`, whose
`seed` is already a `mut ref`: legacy wants the marker dropped, while on
v2 the marked forward is the spelling (kara B-2026-10-14-25). They
refuse the persistent arm at `*v`, as v2 does, and the differential at
`*a` and `*v` over `iter()`, since legacy gives those items by value
where v2 gives references. They build the bench program, which has
neither. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, singly linked with a sentinel, the
same in all five languages. Each of five rounds makes ten lists and
feeds each 6,000 random calls, a fifth of each kind as in the harness,
so a list grows to about 2,400 values and every call but `add_at_head`
walks a few hundred to a few thousand nodes; every `get` goes into a
checksum and every final size into a count. Every implementation prints
`5 rounds of 10 lists of 6000 calls: 119969 values left, checksum
773058780`, the Kāra program under `karac __mir-run` included (in
242 s).

Every implementation allocates one node per value: C with `malloc` and
`free`, Rust as `Option<Box<Node>>`, Go and Python as garbage-collected
objects, and Kāra as a counted `shared struct`. Spot timings on a shared
4-core container, eight runs of each compiled program, five of them
interleaved, three more of C and Rust, and two of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.54 to 0.63 s, and one run of 0.76 s |
| Rust (`rustc -O`) | 0.54 to 0.63 s, and one run of 1.13 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.56 to 0.59 s |
| Go | 0.31 to 0.35 s |
| Python | 2.9 to 3.1 s |
| Kāra (`karac build --mir`) | 0.81 to 0.86 s |
| Kāra, legacy (`karac build`) | 0.45 to 0.50 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` builds the same program,
and its time is the last row. That edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 3.3 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

So the v2 build takes about 1.75 times as long as the legacy build by
median, inside the M2 bar of 2 for any one kata, about 1.5 times C and
Rust and 2.6 times Go. Under valgrind's cachegrind, the times follow
simulated L1 data misses, not instructions: the v2 build runs
2.57 billion instructions with 140 million misses, legacy 2.03 billion
with 60 million, and C 0.30 billion with 76 million, which suggests
every version spends its time waiting for the walk's next node. The
v2 node is a 32-byte block, two counts, the value and the link, where
C's is 16 bytes, and in the IR before optimization each step of the
v2 walk also adds a count to the next node and takes one from the node
it leaves. Why legacy misses less often than C was not established. The
comparison with C and Rust waits until after M4.

## Compiler findings

kara **B-2026-10-18-30** (open, medium): every v2 surface binds the
parts of a `shared enum` pattern by value, so the persistent arm's
`List.Cons(v, rest) => ... *v ... *rest` is refused ("unary '*' requires
'ref T' ... found 'i64'", and `List` for `*rest`). design.md § Patterns
binds those parts as `ref`, and `karac check` follows it, accepting `*v`
and also accepting `v`; the v2 surfaces accept only `v`. The arm and the
differential keep the spelling the spec gives.
