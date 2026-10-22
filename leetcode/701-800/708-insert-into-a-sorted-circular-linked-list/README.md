# 708. Insert into a Sorted Circular Linked List

Given a Circular Linked List node, which is sorted in non-descending
order, write a function to insert a value `insertVal` into the list such
that it remains a sorted circular list. The given node can be a
reference to any single node in the list and may not necessarily be the
smallest value in the circular list. If there are multiple suitable
places for insertion, you may choose any place to insert the new value.
After the insertion, the circular list should remain sorted. If the list
is empty (i.e., the given node is null), you should create a new single
circular list and return the reference to that single node. Otherwise,
you should return the originally given node.

```
head = [3, 4, 1], insertVal = 2  ->  [3, 4, 1, 2]
head = [],        insertVal = 1  ->  [1]
head = [1],       insertVal = 0  ->  [1, 0]
```

**Constraints:** the number of nodes in the list is in the range [0, 5 *
10^4]; -10^6 <= `Node.val`, `insertVal` <= 10^6.

> **Migrated to v2's borrow rules (2026-10-22).** The recursive and shared arms, and their copies in `differential.kara`, walked the ring with `let mut at = head;` and then `at = at.next.expect(...)`, where `head` is bound by `if let Some(head) = self.head` and so is a borrow. Since kara `d05a120ea5` (B-2026-10-19-13), `karac check` refuses that store: `at` is a `ref Node`, and the owned `Node` read out of `at.next` would be dropped at the end of the statement. The four walks now declare `let mut at = head.clone();`, as the diagnostic suggests: `Node` is a `shared struct`, so the copy is a retain of the same node. After the change all five Kāra files pass `karac check`; the two arms print the same output as `insert_into_a_sorted_circular_linked_list.py` under `karac __mir-run` and `karac __mir-llvm-run`, and under `karac __mir-llvm-asan` with no error, and the differential prints its `0 failures` line under all three. The legacy results below predate the change; legacy already refused these two arms at `*v`.

## Approaches

Every arm walks from the given node to the first gap the value fits:
between a value and a larger or equal one when the value lies between
them, or across the drop from the largest value to the smallest when the
value is at least the largest or at most the smallest. If the walk comes
back round to the given node, every value is equal and any gap fits, and
it takes the one after the given node. The problem allows any suitable
gap; taking the first from the given node makes every arm print the same
ring, which is what lets the harness compare them exactly. Each arm also
has a `struct CircularList` that the harness drives, with `fn
from_values`, `fn insert(mut ref self, insert_val: i64)` and `fn
values(self) -> Vec[i64]`, the ring read once round from the given node.

| file | mechanism |
|---|---|
| `insert_into_a_sorted_circular_linked_list.kara` ★ | an arena: values and next links in two `Vec`s, a node named by its index, so the ring is not a cycle of counted handles; `Ring.insert(head: Option[i64], insert_val)` returns the node to hand back |
| `insert_into_a_sorted_circular_linked_list_shared.kara` | the problem's own shape, counted `shared struct Node` cells with the last linking back to the first, compared by identity with `ref_eq`; the ring is a strong cycle, so the list holding it cuts one link in its `impl Drop` and the rest free in a chain |
| `insert_into_a_sorted_circular_linked_list_recursive.kara` | the shared arm's nodes, the walk written as recursion: the gap after a node is the answer if the value fits, the gap after the given node once the next node is the given one, and otherwise the next node's answer |
| `insert_into_a_sorted_circular_linked_list_vec.kara` | one `Vec` read from the given node, the node after the last being the first again; the same walk by index, then `insert` shifts the values after the gap, and a value that goes before the given node goes at the end, so the given node stays first |
| `differential.kara` | the four arms against the definition, four properties |

design.md § Cycles and `weak` names three ways to hold a cycle. A `weak`
back-edge cannot close a ring here: its node would have to exist before
the node it points at, and a one-node ring points at itself, which no
struct literal can say. The two left are a central store with ids, the ★
arm, which the section recommends when the structure guarantees
validity, and strong links with the cycle broken by hand, the shared
arms.

Every arm prints the same 12 lines: the three LeetCode examples; values
beyond either end, onto the drop and equal to existing values; every
value equal; a one-node ring; the extreme values; 2,000 random values
inserted into an empty list, twice; a ring of the problem's most,
50,000 values, given at a random node, with 50 inserts; and 300 random
rings of 0 to 30 values from a narrow or wide range with 1 to 5 inserts,
each with a checksum. `insert_into_a_sorted_circular_linked_list.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms and does not walk at
all: it tries each gap in turn from the given node, builds the ring with
the value put there, and takes the first whose values go down at most
once going round. 2,000 random rings are checked, sorted rings of 0 to
30 values from a span of 3 or of 1,000 read from a random node, each
with 1 to 6 values to insert from 2 below the span to 2 above it, so
ties, values beyond either end and rings of equal values are all common.

| | property |
|---|---|
| P1 | the ring after every insert is the definition's |
| P2 | every value 1,000 higher, every ring 1,000 higher |
| P3 | each ring is the one before with the value added somewhere after the given node, and goes down at most once, whichever gap the arm chose |
| P4 | the given node's own value goes in right after it |

It prints `2000 rings (495 inserts before the given node), 4 arms,
31828 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Eleven edits to the differential, two or three to each arm, each run
under `karac __mir-run`. All eleven are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a value equal to a gap's lower end not fitting it | P1 261, P4 1543 |
| M2 | ★: nothing fitting across the drop | P1 1115, P3 1088, P4 175 |
| M3 | ★: the walk stopping a node short of coming round | P1 19 |
| M4 | ★: the new node linked back to the given node | P1 1935, P3 1935, P4 1895 |
| M5 | shared: every value put after the given node | P1 1897, P3 1897 |
| M6 | shared: each gap tested against its own lower end | P1 1769, P3 1769 |
| M7 | recursive: coming round, the gap before the given node | P1 19 |
| M8 | recursive: a gap's ends tested the wrong way round | P1 1925, P3 1925 |
| M9 | vec: coming round, the gap before the given node | P1 19 |
| M10 | vec: each gap tested against its own lower end | P1 1769, P3 1769 |
| M11 | vec: the value put before the gap's lower end | P1 1971, P3 1971 |
| E1 | shared: back round tested on the next node, the same node | 0 |
| E2 | shared: the list no longer cuts the ring when dropped | 0 |
| E3 | recursive: a value equal to a gap's upper end not fitting it | 0 |

P1 kills all eleven. Three of them, M3, M7 and M9, only P1 kills, and
only in the 19 rings whose values are all equal while the value inserted
is not: each takes the gap before the given node instead of the one
after it, which is just as sorted, so P3, which accepts any suitable
gap, rightly passes them. P3 kills the seven that leave the ring
unsorted or lose the given node's place. P4 catches M1, whose value
equal to a gap's lower end skips that gap and lands later, and the two
that break the walk outright, M2 and M4. P2 kills nothing: every mutant
here goes wrong on the order of the values, which adding 1,000 to all of
them preserves. E1 tests for coming round on the next node rather than
the current one, which at that point are the same node; E3 lets a value
equal to a gap's upper end pass that gap, and the next gap then always
fits it, so it lands beside an equal value and the ring reads the same.

E2 deletes the shared arm's `impl Drop`, so the ring is never cut and
every node leaks. No property can see a leak, which is what a sanitizer
is for, and the v2 sanitizer lane could not see it either (kara
B-2026-10-18-31, below).

## Verification

Every arm prints the same output as
`insert_into_a_sorted_circular_linked_list.py` under `karac __mir-run`
(the v2 MIR interpreter) and `karac __mir-llvm-run`, and under `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. All with the compiler
at kara `2bfc20c2ad` for the debug build and `222fb9e2d8` for the
release build that runs `check` and `__mir-run`; the one compiler commit
between them, `082e3de2d8`, adds `\xHH` escapes, which these programs do
not use, and the runtime archives were rebuilt after the last
`runtime/src` change.

The sanitizer lane as shipped cannot see a leak at all (kara
B-2026-10-18-31, below), so its silence on leaks here is no evidence.
The leak check was done by running the lane's own executables with a
preloaded shim that refuses the lane's hand-made stack, so `main` runs
on a thread LeakSanitizer knows: all four arms and the differential
report no leak, and a copy of the shared arm without its `impl Drop`
reports `1917792 byte(s) leaked in 59931 allocation(s)`, which the lane
as shipped does not report.

The frozen legacy backends refuse all four arms and the differential at
type checking, at `list.insert(*x)` and the like over `iter()`, since
legacy gives those items by value where v2 gives references, and at
`next_random(mut seed)` inside the harness's `random_ring`, whose `seed`
is already a `mut ref` (kara B-2026-10-14-25). They build the bench
program, which has neither. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm, the arena, the same algorithm in all
five languages; C, Rust and Go hold the values and links in growable
arrays and Python in lists. Each of five rounds makes ten rings of
20,000 random values from -1,000,000 to 1,000,000, sorted and linked
round from a random node, then inserts 1,000 more random values from
that node, each walking about half the ring; each final ring, read from
the given node, goes into a checksum. Every implementation prints
`5 rounds of 10 rings of 20000 values, 1000 inserts each: checksum
923925810`, the Kāra program under `karac __mir-run` included (in
200 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.13 to 1.28 s |
| Rust (`rustc -O`) | 0.83 to 0.91 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.80 to 0.93 s |
| Go | 1.00 to 1.09 s |
| Python | 47.7 to 48.5 s |
| Kāra (`karac build --mir`) | 0.77 to 0.87 s |
| Kāra, legacy (`karac build`) | 0.78 to 0.93 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` builds the same program,
and its time is the last row. That edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 4.2 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

So the v2 build is level with the legacy build and with Rust either way,
inside the spread of the runs, and ahead of Go and C. Under valgrind's
cachegrind the compiled programs run about the same number of
instructions (C 9.18 billion, Rust 9.32, v2 9.28), but C's take half as
many branches (1.65 billion against 3.47) with few mispredicted in any
of them, which suggests clang has turned the walk's comparisons into
branch-free selects; why that makes C the slowest was not measured. The
comparison with C and Rust waits until after M4.

## Compiler findings

kara **B-2026-10-18-31** (open, high): the v2 sanitizer lane, `karac
__mir-llvm-asan`, cannot see a leak. Its runtime runs `main` on a stack
it maps and switches to by hand, and LeakSanitizer does not track what
is allocated there. The shared arm without its `impl Drop` was meant as
the check that the lane sees the leaked ring, and it came back clean; so
did a two-node cycle, and with every LeakSanitizer root turned off the
lane still reported nothing. The same executable reports both once the
switch is refused, and a C program that switches stacks the same way
loses its leak report too. Every clean leak verdict from the lane since
kara `8969be0434` (2026-10-13) is therefore vacuous, those of earlier
katas included; use-after-free and double-free detection do not depend
on it. The kata itself needed no change.
