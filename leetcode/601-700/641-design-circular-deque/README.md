# 641. Design Circular Deque

Design a double-ended queue of at most `k` values. `MyCircularDeque(k)`
makes an empty one; `insertFront(value)` and `insertLast(value)` add a
value at the front or the rear and return whether they could, which they
cannot when it is full; `deleteFront()` and `deleteLast()` remove the
value at the front or the rear and return whether there was one;
`getFront()` and `getRear()` return the value at the front or the rear,
or -1 when it is empty; and `isEmpty()` and `isFull()` say whether it
holds no values or `k` of them. The built-in deque is not to be used.

```
["MyCircularDeque","insertLast","insertLast","insertFront",
 "insertFront","getRear","isFull","deleteLast","insertFront","getFront"]
[[3],[1],[2],[3],[4],[],[],[],[4],[]]
  ->  [null,true,true,true,false,2,true,true,true,4]
```

**Constraints:** `k` from 1 to 1,000; every value from 0 to 1,000; at
most 2,000 calls in all.

## Approaches

Every arm is `struct MyCircularDeque` with `fn new(k: i64) ->
MyCircularDeque`, the four changes as `mut ref self` methods returning
`bool` and the four reads as `self` methods. Every operation is
O(1), the stacks arm's deletes amortized.

| file | mechanism |
|---|---|
| `circular_deque.kara` ★ | a `Vec` of `k` slots used as a ring: the front value's slot and a count, a value in front taking the slot before the front, wrapping |
| `circular_deque_slots.kara` | `k + 1` slots and two indexes, the front value's slot and the slot the next rear value goes in; one slot always stays empty, so equal indexes mean empty and no count is kept |
| `circular_deque_vecdeque.kara` | the standard library's `VecDeque`, itself a growable ring, with the capacity checked before every push: the built-in deque the problem rules out, kept as a reference |
| `circular_deque_stacks.kara` | two `Vec` stacks back to back, each end's value on top of its own; a delete from an empty stack first moves the bottom half of the other across, reversed |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 9 lines: the LeetCode example; five more
(everything on an empty deque; a deque of one filled from each end and
emptied from the other; values put in front wrapping round a deque of
two; a deque used as a stack from the rear and as a queue from the
front; a full deque emptied from both ends), each as LeetCode prints its
results; a checksum of the results of 300 random scripts of 1 to
60 operations on deques of 1 to 8; and checksums for the problem's
largest, one script of 2,000 operations run on a deque of 1,000 and on a
deque of one. `circular_deque.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
the deque is the list of its values, front first, an insert putting its
value at the start or the end of the list when it is shorter than `k`
and a delete removing the first or last value when there is one. Each of
1,000 cases runs 1 to 40 random operations, inserting values from 0 to
9, on a deque of 1 to 5, and records each arm's result and its front,
rear, emptiness and fullness after every operation.

| | property |
|---|---|
| P1 | every result is the definition's |
| P2 | the ends are -1 exactly when the deque is empty, it is never both empty and full, and a value just inserted is at the end it went in at |
| P3 | an insert succeeds exactly when the deque was not full and a delete exactly when it was not empty, and the count those successes give is 0 exactly when it is empty and `k` exactly when it is full |
| P4 | the script with the two ends swapped gives the same results, with the front and rear swapped |
| P5 | a deque whose start was first moved 1 to 12 places, by inserting at the front and deleting at the rear, gives the same results and states |

It prints `1000 cases (21160 operations), 4 arms, 20000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac
__mir-llvm-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a value in front put after the front, not before | P1 269, P4 533, P5 341 |
| M2 | ★: the rear read one slot late | P1 531, P2 716, P4 786, P5 699 |
| M3 | slots: a value in front put after the front, not before | P1 692, P2 427, P3 740, P4 791, P5 691 |
| M4 | slots: full one value early | P1 742, P2 182, P3 837 |
| M5 | vecdeque: a value in front pushed at the back | P1 460, P2 604, P4 699 |
| M6 | vecdeque: a delete at the rear taken from the front | P1 305, P4 624 |
| M7 | stacks: the half moved across not reversed | P1 32 |
| M8 | stacks: the front of an empty front stack read from the top of the back one | P1 93, P4 563 |
| E1 | ★: the rear slot found with the ring's length added before the remainder | 0 |
| E2 | slots: a step back written as a step forward of one less than the ring | 0 |
| E3 | vecdeque: full when at or over the capacity | 0 |
| E4 | stacks: the whole of the other stack moved across, not half | 0 |

P1 kills all eight. P4 sees every mutant that treats the two ends
differently, which is all but M4 and M7. P5 sees only the ring arms'
mistakes that depend on where the ring starts, M1 to M3: moving the
start of a `VecDeque` or of two stacks leaves them as they were. P2 sees
the mutants that show a wrong end right after an insert, M2, M3 and
M5, and M4, which on a deque of one calls it full while it is empty.
P3 sees two, M3 and M4, whose counts of successes stop matching what the
deque reports. M7 is the hardest to see, killed by P1 alone in 32 cases:
a half moved across in the wrong order only shows when more than one
value moves and those values are then read. The four survivors cannot
change an answer: the sum before the remainder is never negative, so
adding the ring's length changes nothing; a step back and a step forward
of one less than the ring land on the same slot; the deque never holds
more than its capacity; and moving the whole stack keeps every answer,
losing only the amortized bound.

## Verification

Every arm prints the same output as `circular_deque.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes every arm, the
differential and the bench program. All at kara `d6111aa22a` for the
debug build, with the runtime archives rebuilt from that tree, and
`14acd67779` for the release build that runs `check` and `__mir-run`.

The frozen legacy backends refuse every arm and the differential at type
checking. Each hands `seed`, already a `mut ref` parameter, on to
`next_random(mut seed)` with the `mut` marker design.md asks for, and
legacy rejects that marker, saying the argument is already a mut-ref.
The differential also stops on `*value`, because legacy types the
payload matched from an item of `ops.iter()` by value. Legacy is frozen,
so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes a script of 100,000 random
operations once, in the same mix as the harness's; then 300 rounds each
run it on a new deque of 1 to 1,000 slots, picked by the round, putting
every result into a checksum. Every implementation prints `300 deques,
100000 operations each: checksum 365258286`, the Kāra program under
`karac __mir-run` included (in 76 s).

Each implementation is the same ring of `k` slots with the front value's
slot and a count, run over the same script of operations written as
numbers: Rust with a `Vec<i64>`, C with a `calloc`'d array, Go with a
slice and Python with a list. Spot timings on a shared 4-core container,
three runs each (two for Python; `bench.sh` timings need a quiet
machine), each including making the script:

| | time |
|---|---|
| C (`clang -O3`) | 0.35 to 0.39 s |
| Rust (`rustc -O`) | 0.37 to 0.38 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.38 to 0.40 s |
| Go | 0.40 to 0.42 s |
| Python | 7.55 to 7.74 s |
| Kāra (`karac build --mir`) | 0.38 to 0.41 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program: it rejects the `mut` markers above, and reads `*op` over
`ops.iter()` as a deref of a plain `i64`. That edit is by hand, on top
of the `scripts/new-bench.sh` output. A copy outside the kata that
leaves out the markers and the `*` builds under legacy and takes 0.71 to
0.74 s. Under `karac __mir-llvm-run` the program prints the same line in
2.1 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So the v2 build takes about half of legacy's time, and sits with C, Rust
and Go, its overflow checks on. Every operation is a compare, a
remainder and a load or store, so the compiled programs differ by
little; the comparison with C and Rust waits until after M4.

## Compiler findings

None. The legacy refusals above are not filed because legacy is frozen.
