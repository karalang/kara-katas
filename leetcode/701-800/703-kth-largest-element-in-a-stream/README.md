# 703. Kth Largest Element in a Stream

Design a class to find the kth largest element in a stream. Note that it
is the kth largest element in the sorted order, not the kth distinct
element. Implement the `KthLargest` class: `KthLargest(int k, int[]
nums)` initializes the object with the integer `k` and the stream of
integers `nums`; `int add(int val)` appends the integer `val` to the
stream and returns the element representing the kth largest element in
the stream.

```
KthLargest(3, [4,5,8,2]); add(3), add(5), add(10), add(9), add(4)
  ->  4, 5, 5, 8, 8
KthLargest(4, [7,7,7,7,8,3]); add(2), add(10), add(9), add(9)
  ->  7, 7, 7, 8
```

**Constraints:** 0 <= `nums.length` <= 10^4; 1 <= `k` <= `nums.length` +
1; -10^4 <= `nums[i]`, `val` <= 10^4; at most 10^4 calls to `add`.

## Approaches

Every arm is `struct KthLargest` with `fn new(k: i64, nums: Vec[i64]) ->
KthLargest`, which feeds `nums` to `add` one at a time, and `fn add(mut
ref self, val: i64) -> i64`.

| file | mechanism |
|---|---|
| `kth_largest_element_in_a_stream.kara` ★ | the k largest values so far in the stdlib `PriorityQueue`, which pops the smallest first: push, pop once it holds more than k, and `peek` the root; O(log k) per value |
| `kth_largest_element_in_a_stream_heap.kara` | the same k values in a binary min-heap written out over a `Vec`: sifted up until it holds k, then a value above the root replaces it and is sifted down; O(log k) per value, and nothing done for a value at or below the root |
| `kth_largest_element_in_a_stream_sorted.kara` | the k largest in a `Vec` in descending order: each value inserted after every larger one, found by a binary search, and the smallest popped off the end; O(k) per value for the shift |
| `kth_largest_element_in_a_stream_multiset.kara` | a `SortedMap` from each held value to how many times it is held, with the total beside it: one copy of the smallest key counted out once the total passes k; O(log k) per value, and a repeated value costs one entry |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 12 lines: the two LeetCode examples; k =
1 from no values, k = 2 from one, k reached by the first add, every
value the same, values only falling and only rising; the problem's
largest, 10,000 values and 10,000 adds for k of 1, 5,000 and
10,000 (where 9,999 values leave the first add to make k), each with its
last answer and a checksum; and 300 random streams of up to 49 values
and 50 adds from narrow ranges, so values repeat, with a checksum.
`kth_largest_element_in_a_stream.py` mirrors the ★ arm with `heapq` and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: after each add, sort
every value seen so far from largest down and take the one at place k.
3,000 random streams are checked, with k from 1 to 8, k - 1 to k +
11 values and 1 to 15 adds, all from a range of 1 to 30 numbers around
zero, so in most streams values repeat.

| | property |
|---|---|
| P1 | the answers are the definition's |
| P2 | one answer per add, and no answer below the one before |
| P3 | after each add, fewer than k values seen are above the answer and at least k are at or above it |
| P4 | every value moved by the same random amount from -50 to 50, every answer moved by it |

It prints `3000 streams (1714 with values bound to repeat), 4 arms,
48000 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run`. All ten are killed: six by the properties and four
that stop the run at the arm's own `unwrap()` on an empty queue or map.
Four more edits, E1 to E4, change nothing that can be seen, and the
differential rightly reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: popped once the queue holds k, not more | stops: `unwrap()` on `None` |
| M2 | ★: k + 1 values kept | P1 2482, P2 36, P3 2482 |
| M3 | heap: the sift up turned the wrong way | P1 2013, P2 553, P3 2013 |
| M4 | heap: the right child never looked at | P1 1661, P3 1661 |
| M5 | heap: the sift up stopping below the root | P1 411, P2 149, P3 411 |
| M6 | sorted: the largest dropped, not the smallest | P1 2861, P2 715, P3 2861 |
| M7 | sorted: the search's upper half cut one short | P1 1815, P2 1097, P3 1815 |
| M8 | multiset: a key held twice removed whole | stops: `unwrap()` on `None` |
| M9 | multiset: each value counted twice in the total | stops: `unwrap()` on `None` |
| M10 | multiset: a repeated value counted once | stops: `unwrap()` on `None` |
| E1 | heap: a value equal to the root replacing it | 0 |
| E2 | sorted: a new value put before its equals | 0 |
| E3 | sorted: the middle written `lo + (hi - lo) / 2` | 0 |
| E4 | multiset: the total not counted back down | 0 |

P1 and P3 kill every mutant that gives a wrong answer, and P2 five of
the six. P4 sees none: every arm only compares values, so moving them
all keeps every comparison; it is there for an arm that does arithmetic
on values, which none of these needs. E1 lets a value equal to the
heap's root replace it, which leaves the same multiset. E2 puts a new
value before its equals in the sorted list rather than after, the same
list. E3 writes the middle as `lo + (hi - lo) / 2`, the same for indices
this small. E4 never counts the multiset's total back down: once past k
it stays past k, so every later add counts one copy out, which is what
the counted total also does at k.

## Verification

Every arm prints the same output as `kth_largest_element_in_a_stream.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. The differential prints its line under all three. `karac check`
passes the ★, heap and sorted arms and the bench program; it warns on
the ★ arm's `self.top.pop();` (B-2026-10-18-16) and refuses the multiset
arm and the differential (B-2026-10-14-24). All with the compiler at
kara `79a6c2eb9a` for both the debug build and the release build that
runs `check` and `__mir-run`, with runtime archives rebuilt after the
last `runtime/src` change.

The frozen legacy backends refuse all four arms and the differential at
type checking, at `s.add(*x)` over `nums.iter()` in `new`, since legacy
gives those items by value where v2 gives references. Legacy is frozen,
so this is noted, not filed.

## Benchmarks

The bench program uses the heap arm, the one that is the same algorithm
in all five languages; C has no priority queue. It makes ten streams of
prices that move by a random step from -90 to 110, so they drift up and
most new prices reach the k largest. Each starts from 1,000 prices with
k from 50 to 500 and is fed 200,000 more, every answer folded into a
checksum, and the whole runs five rounds. Every implementation prints
`5 rounds of 10 streams of 200000 prices: answer changed 9091273 times,
checksum 314600129`, the Kāra program under `karac __mir-run` included
(in 92 s).

Every implementation keeps the heap in a growable array, `Vec`, slice or
list, and C in one `malloc`'d block of k; Rust swaps with `Vec::swap`,
Go and Python with a tuple assignment. Spot timings on a shared 4-core
container, eight runs of the `--mir` build and of each other compiled
program, five of each interleaved, five of the legacy copy and two of
Python (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.50 to 0.54 s |
| Rust (`rustc -O`) | 0.57 to 0.62 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.56 to 0.61 s |
| Go | 0.62 to 0.67 s |
| Python | 14.5 to 14.7 s |
| Kāra (`karac build --mir`) | 0.68 to 0.75 s |
| Kāra, legacy (`karac build`), a copy | 0.64 to 0.68 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend. The legacy `karac build` refuses it at `s.add(*x)`
over `nums.iter()`, since legacy gives those items by value; the legacy
row times a copy with `s.add(x)` there, which prints the same line. That
edit to `bench.sh` is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
2.9 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So the v2 build is about 7% behind the legacy copy by median, 10% behind
Go, 20% behind Rust either way and a third behind C. The comparison with
C and Rust waits until after M4.

## Compiler findings

kara **B-2026-10-18-19** (fixed by `a2fbdd9c11`): a function declared
`-> i64` whose tail is a `ref i64` from a call, here the ★ arm's
`self.top.peek().unwrap()`, handed the reference itself back as the
`i64`. The harness keeps each answer in a `Vec[i64]` after the queue is
gone, so `karac __mir-run` stopped with "use of a2 after it was freed"
and the compiled surfaces printed the reference's address, while `karac
check` passed it. It was the sibling of B-2026-10-18-4, where the
referent outlives the use and only the compiled surfaces were wrong. The
fix for that row reads the value through the reference in the built MIR,
which fixed both; the kata was written against the broken compiler and
needed no change.

kara **B-2026-10-18-16** (open, low): `karac check` warns `discarded
Option value` on the ★ arm's `self.top.pop();`, though design.md exempts
`Vec.pop` and `VecDeque.pop_front`, whose result is the value removed;
`PriorityQueue.pop` is the same shape and is missing from the list. The
arm keeps the statement as written.

kara B-2026-10-14-24 (open): `karac check` types the items of
`iter().next()` on a `SortedMap` by value, so it refuses the multiset
arm's `*first` and `*count` and the same lines in the differential,
while every MIR surface runs them. The multiset arm reads the smallest
key with `iter().next()` because `keys().next()` is refused too, by
B-2026-10-13-1 (`keys` returns a `Vec`, not an iterator). Both are left
as written.
