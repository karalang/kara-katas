# 716. Max Stack

Design a max stack data structure that supports the stack operations and
supports finding the stack's maximum element.

`MaxStack()` makes an empty stack. `push(x)` pushes `x` onto the stack.
`pop()` removes the element on top of the stack and returns it. `top()`
gets the element on the top of the stack without removing it.
`peekMax()` retrieves the maximum element in the stack without removing
it. `popMax()` retrieves the maximum element in the stack and removes
it; if there is more than one maximum element, only the top-most one is
removed. The follow-up asks for O(1) `top` and O(log n) for every other
call.

```
push(5); push(1); push(5)
top()      ->  5
popMax()   ->  5   (the top-most 5)
top()      ->  1
peekMax()  ->  5
pop()      ->  1
top()      ->  5
```

**Constraints:** -10^7 <= `x` <= 10^7; at most 10^5 calls; the stack
holds at least one element whenever `pop`, `top`, `peekMax` or `popMax`
is called.

## Approaches

The stack calls are easy; the arms differ in how they find the max and
take it out of the middle.

| file | mechanism |
|---|---|
| `max_stack.kara` ★ | beside each value, the largest value at or below it, so the max is always on top of that second stack; `pop_max` pops into a buffer until the max is on top, drops it, and pushes the buffer back, which rebuilds the maxima above it; O(1) per call but `pop_max`, which is O(n) |
| `max_stack_heap.kara` | every value with an id in push order, on a stack and on a largest-first heap of (value, id) pairs, so among equal values the heap gives the top-most first; a value taken from one side is only marked removed, and each side drops marked values when they reach its top; O(log n) per call, amortized |
| `max_stack_sorted.kara` | the values in a doubly linked list held in vectors of previous and next ids, and a `SortedMap` from each distinct value to its ids, oldest first; the map's last key is the max and its last id the top-most copy, which `pop_max` unlinks from the middle of the list; O(log n) per call, which meets the follow-up |
| `max_stack_scan.kara` | one vector; the max calls scan it for the last, top-most, of the largest values, and `pop_max` removes that element, shifting the rest down; O(n) for the max calls |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 10 lines: the LeetCode example; one value
through every call; rising values taken by max pops, and falling ones;
equal maxima, where only the top-most goes each time; the problem's
extremes; 20,000 random calls with values up to 10^7, and with values up
to 5 so that ties are common; 10,000 calls that are mostly pushes; and
2,000 rising pushes followed by 2,000 max pops. The random lines print
their number of answers and a checksum. `max_stack.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition, a
plain list whose max calls look down from the top for the first value no
smaller than every other, found by comparing each value with all of
them. 3,000 random sequences of up to 40 calls are checked, half of them
pushes, with values from -s to s for s from 0 to 5, so equal maxima are
common.

| | property |
|---|---|
| P1 | every answer is the definition's |
| P2 | popped empty after the calls, what is left is the definition's, top first |
| P3 | every value raised by the same amount, up to 10^7, raises every answer by it |
| P4 | emptied by max pops after the calls, what is left comes out largest first, and is what popping it empty gives |

It prints `3000 call sequences (28328 answers), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed, M7 and M8 by stopping the
program. Three more edits, E1 to E3, change nothing that can be seen,
and the differential rightly reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the running minimum kept instead of the maximum | P1 2041, P2 2041, P4 2149 |
| M2 | ★: the buffer pushed back in reverse order | P1 351, P2 834 |
| M3 | ★: the top popped as the max without looking down | P1 1116, P2 1531, P4 1996 |
| M4 | heap: values removed by a max pop left on the stack | P1 477, P2 1578, P4 1400 |
| M5 | heap: a popped value not marked removed | P1 790, P2 874, P4 1665 |
| M6 | heap: the oldest of equal maxima popped first | P1 117, P2 560 |
| M7 | sorted: the oldest copy of the max unlinked | stops: a missing map key |
| M8 | sorted: the next node not linked back past an unlinked one | stops: a missing map key |
| M9 | sorted: the max sought among values up to 4 only | P1 137, P2 137, P3 2400 |
| M10 | scan: the bottom-most of equal maxima taken | P1 117, P2 560 |
| M11 | scan: the second value never considered | P1 905, P2 905, P4 1272 |
| M12 | scan: the top removed in place of the max | P1 1531, P2 1531, P4 1996 |
| E1 | ★: an equal value taking the running max below it | 0 |
| E2 | heap: an empty heap read as -1, not 0 | 0 |
| E3 | scan: the first value compared with itself too | 0 |

P1 and P2 kill every mutant that runs to the end. M7 unlinks the oldest
copy of the max while the map drops its newest id, and M8 leaves a
node's link pointing back at a node already unlinked; either way a later
call asks the map for a value it no longer holds, and `ids[x]` on a
missing key panics, so the program stops instead of answering wrong.
P4 misses four. M2 pushes the buffer back reversed and M6 and M10 take
the oldest of equal maxima, which change the order of what is left but
not which values a max pop takes; M9 misreads only `peek_max`. P3 kills
only M9, whose limit of 4 the raised values pass; every other mutant
compares values with each other, so raising them all changes nothing.
E1 lets an equal value take the running max below it, which is the same
number; E2 changes what an empty heap reads, which no call ever asks;
E3 also compares the first value with itself, which keeps it.

## Verification

Every arm prints the same output as `max_stack.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`9ddda04add`, whose last compiler change is `fa73802a05`. No
`runtime/src` change has landed since the runtime archives were built.

The sanitizer lane cannot see a leak (kara B-2026-10-18-31), so the leak
check copied each arm's and the differential's lane executable as it was
linked and ran it with the preloaded shim from kata 708, which refuses
the lane's hand-made stack so that LeakSanitizer sees `main` (kata
708 showed it reporting a leak the lane misses): all five print their
output and report no leak.

The frozen legacy backends refuse all four arms, the differential and
the bench program at type checking: at `*call` over `iter()` in the
harness and the bench program, and at `*x` on what `floor` finds in the
sorted-map arm, since legacy gives those by value where v2 gives
references; and at `next_random(mut seed)` inside the harness's
`random_calls`, whose argument is already a `mut ref`, where legacy
wants the marker dropped and design.md § Call-site `mut` markers now
requires it (kara B-2026-10-14-25). Legacy is frozen, so this is noted,
not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages: C has no sorted
map or heap of pairs in its standard library, so neither O(log n) arm
could be the same algorithm in all of them. It makes ten lists of
100,000 random calls once, half of them pushes of values up to 10^6 and
the rest spread over the four reads, never reading an empty stack, and
runs each list on a fresh stack in 10 rounds, summing every answer.
Since only two of the four reads shrink the stack, it grows to about
25,000 values by the end of a list, and a max pop moves 121 values to
its buffer on average. Every implementation prints `10 rounds of
10 lists of 100000 calls: sum 3310293676360`, the Kāra program under
`karac __mir-run` included (in 11.5 minutes).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.61 to 0.81 s, one run at 1.06 s |
| Rust (`rustc -O`) | 0.73 to 0.96 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.74 to 0.95 s |
| Go | 1.60 to 1.84 s |
| Python | 35.2 to 35.8 s |
| Kāra (`karac build --mir`) | 0.77 to 1.02 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 6.2 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is behind C and Rust, by about a third and a fifth at
the medians of the interleaved runs (0.98 s against 0.73 and 0.81), and
ahead of Go. Under valgrind's cachegrind it runs 12.3 billion
instructions against C's 10.4 and Rust's 9.9, and 2.44 billion branches
against 2.08 and 2.30, all well predicted, so the gap is about the size
of the instruction gap; where those extra instructions come from was not
traced. The comparison with C and Rust waits until after M4.

## Compiler findings

None new.
