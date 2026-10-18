# 725. Split Linked List in Parts

Given the head of a singly linked list and an integer k, split the list
into k consecutive parts. The parts should be as equal in length as
possible: no two may differ in size by more than one, which may leave
some parts empty. The parts keep the order of the input list, and an
earlier part is never shorter than a later one. Return an array of the k
parts.

```
head = [1, 2, 3], k = 5                        ->  [[1], [2], [3], [], []]
head = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], k = 3  ->  [[1, 2, 3, 4], [5, 6, 7], [8, 9, 10]]
```

**Constraints:** the list has 0 to 1000 nodes; 0 <= `Node.val` <=
1000; 1 <= k <= 50.

## Approaches

With n nodes, every part has n / k nodes and the first n % k parts one
more, so the work is finding n and then the places to cut. Each arm also
carries the few lines that build its own kind of list from the harness's
numbers and read its parts back into numbers.

| file | mechanism |
|---|---|
| `split_linked_list_in_parts.kara` ★ | `shared struct` nodes: count them, then walk the list once, taking each part's head, stepping to its last node and cutting the link after it; parts past the end are empty; O(n + k) time, O(1) space besides the k heads |
| `split_linked_list_in_parts_arena.kara` | the same count and walk over an index arena, `vals[s]` and `next[s]` with -1 for the end, its nodes stored back to front so that following `next` is the only way along it; a part is cut by setting its last node's `next` to -1 |
| `split_linked_list_in_parts_persistent.kara` | a persistent `shared enum` list, never changed: each part a fresh copy of the first nodes of what is left, and what is left reached by skipping them, sharing the input's nodes; O(n) new nodes and O(n) stack |
| `split_linked_list_in_parts_offsets.kara` | no nodes and no walk: part i starts at i * (n / k) plus the longer parts before it, min(i, n % k), and is read straight out of the numbers |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 12 lines: the two LeetCode examples; an empty
list in 3 parts; one number in one part; six numbers in three even
parts; three numbers in one part; four numbers in four parts; seven
numbers in six parts; 1,000 random numbers, the problem's most, in
7 parts and in 1, and 999 of them in 50, the most parts, each with the
parts' lengths and whether they put back together are the list; and
300 random lists of up to 20 numbers in up to 8 parts with a checksum.
`split_linked_list_in_parts.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which gives each part in turn the numbers still left divided by the
parts still left, rounded up. 3,000 random lists are checked, each of
0 to 20 numbers in 1 to 10 parts, so empty parts, even splits and uneven
ones are all common; 2,009 split unevenly.

| | property |
|---|---|
| P1 | the parts are the definition's |
| P2 | put back together in order, the parts are the list |
| P3 | there are k parts, and their lengths never grow and differ by at most one |
| P4 | with more than one part, the list less its first part, split in k - 1 parts, gives the other parts |

It prints `3000 lists (2009 split unevenly), 4 arms, 46692 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one part too many given an extra node | P1 1467, P3 1467 |
| M2 | ★: a part never cut from the rest | P1 2372, P2 2372, P3 2358, P4 2372 |
| M3 | ★: one step too many to a part's last node | P1 2372, P3 2372, P4 548 |
| M4 | arena: a part never cut from the rest | P1 2372, P2 2372, P3 2358, P4 2372 |
| M5 | arena: the longer parts put last | P1 2009, P2 635, P3 1374, P4 635 |
| M6 | arena: a part of one node neither cut nor passed | P1 1270, P2 1270, P3 386, P4 758 |
| M7 | persistent: the rest skipping one node too few | P1 2372, P2 2372, P4 2372 |
| M8 | persistent: take copying the whole rest | P1 2372, P2 2372, P3 2358, P4 2372 |
| M9 | persistent: every node counted twice | P1 2137, P3 2137, P4 1144 |
| M10 | offsets: the longer parts before a part left out of its start | P1 1883, P2 1883, P4 1883 |
| M11 | offsets: each part one number short | P1 2805, P2 2805, P4 1863 |
| M12 | offsets: the last part missing | P1 3000, P2 2170, P3 3000 |
| E1 | ★: a part's length as size plus 1 or 0 | 0 |
| E2 | arena: a part cut when its length is at least 1 | 0 |
| E3 | persistent: take stopping at m <= 0 | 0 |

P1 kills all twelve. P2 misses M1, M3 and M9, which get the lengths
wrong but still cut the list in order, so the parts put back together
are still the list; P3 misses M7, M10 and M11, which give every part the
right length but the wrong numbers; and P4 misses M1, whose rule of one
longer part too many is as consistent with itself as the right one, and
M12, which P4 never checks, since it runs only on k parts. P4 is checked
only with more than one part, which is why the line counts fewer than
48,000 checks. M2, M4 and M8 are one mistake in three arms, each part
running on to the end of the list, and fail the same lists. E1 writes
the ★ arm's part length as size plus 1 or 0, E2 cuts a part when its
length is at least 1, and E3 stops `take` at m <= 0, which no call
reaches with a negative m.

## Verification

Every arm prints the same output as `split_linked_list_in_parts.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and under `karac __mir-llvm-asan` (AddressSanitizer)
with no error; the differential prints its line under all three. `karac
check` passes all four arms, the differential and the bench program. The
debug build that runs `__mir-llvm-run`, `__mir-llvm-asan` and `build
--mir` and the release build that runs `check` and `__mir-run` are both
at kara `a4b0967495`, whose last compiler change is `d2fb23c673`. The
runtime archives were built after the last runtime change, `3c8e763161`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse all four arms, the differential and
the bench program at type checking, at a `*` over a vector's `iter()`
(`*p` over the parts, `*h` over the arena's heads, `*v` over a part's
numbers), since legacy gives those by value where v2 gives references.
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes
20 random lists of 1,000 numbers from 0 to 999 once, and in each of
5,000 rounds splits every list into 1 to 50 parts, folds the first
number of every part into a hash, and puts the parts back together
starting from a different part, so each list's order changes from round
to round. The C program's nodes are plain `malloc`'d structs, and the
Rust program's are `Rc<RefCell<ListNode>>`, the honest twin of a `shared
struct` with a `mut` field. Every implementation prints `5000 rounds of
20 lists of 1000 numbers: hash 106070353`, the Kāra program under `karac
__mir-run` included (in 4.8 minutes).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.42 to 0.65 s |
| Rust (`rustc -O`) | 0.89 to 0.94 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.81 to 0.98 s |
| Go | 0.48 to 0.52 s |
| Python | 4.7 to 5.2 s |
| Kāra (`karac build --mir`) | 0.57 to 0.82 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 3.9 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is about a third slower than C and half again as slow as
Go at the medians of the interleaved runs (0.77 s against 0.58 and
0.51), and ahead of Rust (0.92) and of Rust under overflow checks
(0.83), whose `Rc<RefCell>` nodes pay for a borrow flag as well as a
count. Under valgrind's cachegrind it runs 4.5 billion instructions
against Rust's 6.4 and C's 1.4, and 1.2 billion branches against 1.5 and
0.25, with about the same 4 to 6 million mispredicted in all three. The
wall-clock gap to C is much smaller than the instruction gap, likely
because walking a list is bound by waiting on each next node rather than
by instructions, and C's plain pointers do no counting at all; that was
not traced. The comparison with C and Rust waits until after M4.

## Compiler findings

None new.
