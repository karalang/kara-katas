# 622. Design Circular Queue

Design a circular queue of fixed capacity `k`, a first in, first out
queue whose last slot is followed by its first, so that the space a
value leaves can be used again. `enQueue(value)` adds a value at the
rear and `deQueue()` removes the front value, each returning whether it
succeeded; `Front()` and `Rear()` return the front and rear values, or
-1 when the queue is empty; `isEmpty()` and `isFull()` say whether it
is. Do not use a built-in queue.

```
MyCircularQueue(3)
enQueue(1) enQueue(2) enQueue(3) enQueue(4) Rear() isFull() deQueue() enQueue(4) Rear()
->  [null,true,true,true,false,3,true,true,true,4]
```

**Constraints:** `k` from 1 to 1,000; values from 0 to 1,000; at most
3,000 calls.

## Approaches

Every arm is a `MyCircularQueue` with `new(k)`, `en_queue`, `de_queue`,
`front`, `rear`, `is_empty` and `is_full`, each O(1).

| file | mechanism |
|---|---|
| `circular_queue.kara` ★ | a `Vec` of `k` slots used as a ring, with the front value's slot and a count of the values after it; the rear is `count - 1` slots after the front, wrapping past the end |
| `circular_queue_slots.kara` | a `Vec` of `k + 1` slots with a front index and a tail index, the slot the next value goes in; one slot always stays unused, so equal indexes mean empty and the tail just before the front means full, with no count |
| `circular_queue_linked.kara` | a singly linked list of `shared` cells, values entering at the tail and leaving at the head, with a count checked against the capacity; each value gets a cell when it enters |
| `circular_queue_deque.kara` | the standard library's `VecDeque`, itself a growable ring, with the capacity kept beside it and checked before every push; this is the built-in queue the problem rules out, kept as the reference the others can be read against |
| `differential.kara` | the four arms against the definition, five properties |

The harness runs a list of operations on a new queue and prints what
each returns, in LeetCode's form with `null` first for the constructor.
Every arm prints the same 8 lines: the LeetCode example; four more
(every operation on an empty queue, a queue of one filled and emptied
twice, values wrapping around a queue of two several times, and a full
queue emptied to its last value); a length and checksum over 300 random
scripts of 1 to 60 operations on queues of 1 to 8; and the same for one
script of 3,000 operations, the problem's most, on a queue of 1,000 and
on a queue of one. `circular_queue.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms, each with a driver
that runs a script on a new queue and records what every operation
returns and, after every operation, the queue's front, rear and whether
it is empty or full. The definition is the statement read literally: the
queue is the list of its values, front first; `enQueue` appends when the
list is shorter than `k`, `deQueue` removes the first value, and `Front`
and `Rear` are its first and last values or -1. Each of 1,000 random
cases is a queue of 1 to 5 and 1 to 40 operations, values from 0 to 9.

| | property |
|---|---|
| P1 | every operation returns what the definition's does |
| P2 | after every operation, `Front` and `Rear` are -1 exactly when the queue is empty, and it is never both empty and full |
| P3 | an `enQueue` succeeds exactly when the queue was not full and a `deQueue` exactly when it was not empty, and the count of values those successes give is 0 exactly when it is empty and `k` exactly when it is full |
| P4 | first in, first out: the front before each successful `deQueue` is the next value that went in, and the rear after each successful `enQueue` is its value |
| P5 | with the queue's start moved 1 to 12 places first, by putting a value in and taking it out, the script gives the same results and states |

It prints `1000 cases (20842 operations), 4 arms, 20000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a value put `count` slots from slot 0, not from the front | P1 493, P4 649, P5 525 |
| M2 | ★: `Front` reading the rear's slot | P1 404, P4 620 |
| M3 | slots: no spare slot, so one value fewer fits | P1 739, P2 186, P3 825 |
| M4 | slots: `Rear` read two slots before the tail | P1 623, P4 952, P5 882 |
| M5 | linked: the tail kept when the last value leaves | P1 561, P2 649, P3 517, P5 1000 |
| M6 | linked: the tail moved only onto the first cell | P1 536, P2 467, P3 293, P4 702 |
| M7 | deque: full only past the capacity | P1 608, P3 608 |
| M8 | deque: `Front` reading the back | P1 404, P4 620 |
| E1 | ★: the count raised as `count = count + 1` | 0 |
| E2 | slots: the empty test written the other way round | 0 |
| E3 | linked: full tested with `>=` | 0 |
| E4 | deque: success as not `is_none` | 0 |

Only P1 kills all eight; each other property sees the mutants that break
what it checks. P3, the counting property, sees the mutants that get
full or empty wrong: M3, whose queue holds one value fewer, M7, whose
queue never fills, and M5 and M6, whose tail goes stale. P4 sees the
mutants that hand back the wrong value: M1, M4 and M6 read or write the
wrong slot or cell, and M2 and M8 both make `Front` return the rear, so
they fail the same counts. P5 sees the mutants whose answers depend on
where the queue's start is: M1 ignores it, M4 reads a slot outside the
queue, whose content depends on where the start is, and M5 fails every
case, since the warm-up empties the queue and leaves its tail behind.
P2 sees M3's queue of one, which is empty and full at once, and the
stale tails of M5 and M6.

## Verification

Every arm prints the same output as `circular_queue.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes every arm, the
differential and the bench program. All at kara `ea2a2da2be` for the
debug build and `1bc18c7695` for the release build that runs `check` and
`__mir-run`.

The frozen legacy backends refuse every file at type checking. They
still hold the old rule that an argument which is already a `mut ref`,
as `seed` is inside `script`, drops its call-site `mut` marker, and they
type the items of a `Vec`'s `iter()` by value, so the differential's
`*value` is an error. Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes one script of 100,000 random
operations, each a number (0 to 1,000 an `enQueue` of that value, -1 to
-5 the other five operations), once; then 300 times runs it on a new
queue of 1 to 1,000 slots, picked by the round, putting every result
into a checksum. Every implementation prints `300 queues,
100000 operations each: checksum 648452552`, the Kāra program under
`karac __mir-run` included (in 81 s).

Each implementation is the ★ arm's ring with a front index and a count
over an array of `k` values: Rust with a `Vec<i64>` in a struct, Go with
a slice, C with a `calloc`'d array freed after each round, and Python
with a list in a class with `__slots__`. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.33 to 0.40 s |
| Rust (`rustc -O`) | 0.34 to 0.37 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.37 to 0.39 s |
| Go | 0.36 to 0.41 s |
| Python | 8.1 to 8.2 s |
| Kāra (`karac build --mir`) | 0.37 to 0.39 s |

So `bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses it for the
same reasons; that edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
2.0 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

The five compiled rows are within a few hundredths of a second of each
other, the spread of runs on this machine. The program is not profiled
here; every operation does a few comparisons and a modulo, and updates
the checksum with another, so there is little for one compiler to do
better than another.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
