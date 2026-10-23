# 876. Middle of the Linked List

Given the `head` of a singly linked list, return the middle node of the
linked list. If there are two middle nodes, return the second middle
node.

```
head = [1,2,3,4,5]    ->  [3,4,5]
head = [1,2,3,4,5,6]  ->  [4,5,6]    (the middles are 3 and 4; return the second)
```

**Constraints:** the number of nodes in the list is in the range `[1,
100]`, and `1 <= Node.val <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `middle_node.kara` ★ | slow and fast pointers: two walks from the head, the fast one two nodes a step and the slow one one; when the fast walk cannot take two more nodes the slow one has taken half as many steps and stands on the middle, the second of the two when the length is even. One pass, O(n) |
| `middle_node_count.kara` | count, then walk half way: one walk counts the n nodes and a second takes n / 2 steps from the head. Two passes, O(n) |
| `middle_node_array.kara` | the nodes in an array: one walk pushes every node into a `Vec`, and the middle is the node at index n / 2. O(n) time and space |
| `middle_node_recursive.kara` | found as the recursion unwinds: `find(node, index)` recurses to the end, which gives the length n, and on the way back the call at index n / 2 hands its own node up as the middle. O(n) time and stack |
| `middle_node_parity.kara` | one walk and a lagging pointer: the walk counts the nodes it passes, and a second pointer moves one node on after every second node, so after n nodes it has moved n / 2 times |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm returns a node of the list itself, not a copy, and the list is
a `shared struct`. Every arm prints the same 10 lines: LeetCode's two
examples and seven more (a single node; two nodes, whose middle is the
second; three nodes; four equal values; values alternating 100 and 1;
the values 1 to 100, LeetCode's longest list, whose middle is 51; and 99
nodes of 100, LeetCode's largest value), each followed by the list read
from the middle node; and 3,000 lists, one of every length from 1 to 100
and the rest random lengths, valued 1 to 100: the middle values sum to
151,895 and 75,727 nodes are read from the middles on, with a checksum.
`middle_node.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the nodes counted from 1, an odd list's one middle at (n + 1)
/ 2, and an even list's two middles at n / 2 and n / 2 + 1, of which the
second is taken. It checks 2,000 lists: one of every length from 1 to
100 and 1,900 of random lengths up to 100, half valued 1 to 100 and half
1 to 3, so that many values repeat. Where a node sits is found by
marking its value for a moment and reading the list from the head, so
P1 checks the node itself, not its value. The ★ arm's middle values sum
to 51,873.

| | property |
|---|---|
| P1 | the statement's node, the list's own and not a copy |
| P2 | the values from the answer on are the list's last n - n / 2 values |
| P3 | the list read from the head is unchanged |
| P4 | two nodes added at the end move the middle one node on |
| P5 | a node put in front keeps an odd list's middle and moves an even list's back to the first middle |
| P6 | the list reversed: an odd list's middle value is the same, an even list's is the first middle's |

It prints `2000 lists, middle values sum to 51873, 60000 checks over 5
arms: 0 failures` under `karac __mir-run` and `karac __mir-llvm-run`,
and the same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the fast walk one node a step | P1 1965, P2 1965, P4 2000, P5 1028, P6 1628 |
| M2 | ★: the first of two middles returned | P1 1028, P2 1028, P4 1028, P5 2000, P6 838 |
| M3 | ★: the fast walk returned | P1 1986, P2 1986, P4 2000, P5 2000, P6 1831 |
| M4 | count: half of one less walked | P1 1028, P2 1028, P4 1028, P5 2000, P6 838 |
| M5 | count: the count started at 1 | P1 972, P2 972, P4 972, P5 2000, P6 801 |
| M6 | count: the count capped at 64 nodes | P1 685, P2 685, P4 732, P5 346, P6 557 |
| M7 | array: the first of two middles taken | P1 1028, P2 1028, P4 1028, P5 2000, P6 838 |
| M8 | array: the last node left out | P1 1042, P2 1042, P4 1028, P5 1986, P6 852 |
| M9 | array: a copy of the middle node returned | P1 2000, P4 2000, P5 1028 |
| M10 | recursive: the first of two middles handed up | P1 1028, P2 1028, P4 1028, P5 2000, P6 838 |
| M11 | recursive: the length counted one too many | P1 972, P2 972, P4 972, P5 2000, P6 801 |
| M12 | recursive: every node up to the middle handed up | P1 1986, P2 1986, P4 2000, P5 972, P6 1642 |
| M13 | parity: the pointer moved after odd counts | P1 972, P2 972, P4 972, P5 2000, P6 801 |
| M14 | parity: the pointer moved after every third node | P1 1967, P2 1967, P4 1986, P5 1009, P6 1643 |
| M15 | parity: the pointer starting a node late | P1 2000, P2 2000, P4 2000, P5 21, P6 1642 |

P1 kills all fifteen. M2, M4, M7 and M10 are one fault in four arms, the
first of two middles taken, and fail the same 1,028 even-length lists;
M5, M11 and M13 are one fault in three, a node too far on an odd list,
and fail the 972 odd-length lists. M9 returns a node with the middle's
value and the rest of the list behind it, so every property that reads
values (P2, P6) passes and only the ones that find the node in the list
catch it. P3 kills none: no mutation here changes the list.

## Verification

Every arm prints the same output as `middle_node.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `e3f5faf572` and the runtime
archives at `e903d5b111`, with no runtime change between them. Under
`karac __mir-run` the arms take 1 to 2 s each and the differential 18 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy interpreter prints the same output for every arm and
the differential. Legacy's JIT, `karac build` and auto-par print it for
the ★, count, array and parity arms, and abort with glibc's `malloc():
unaligned tcache chunk detected` (heap corruption) on the recursive arm,
whose `find` returns a tuple holding a node, and on the differential,
which holds a copy of it. v2 runs both with no error under the
sanitizer. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 2,000 lists of
1 to 100 nodes valued 1 to 100, LeetCode's sizes, built once; then
2,000,000 searches, each finding the middle of one of the lists, in an
order that visits them all, and summing the middle values and a
checksum. Each search walks about 50 nodes, so the run follows some 10^8
pointers. The node is a `shared struct` in Kāra, `Option<Box<ListNode>>`
in Rust (LeetCode's signature, walked by reference), a pointer in Go, an
object in Python and a `malloc`'d struct in C. Every implementation
prints `2000000 searches over 2000 lists: middle values sum to
101271000, checksum 873989216`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.46 to 0.54 s | 0.49 s |
| Rust (`rustc -O`) | 0.52 to 0.66 s | 0.57 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.52 to 0.56 s | 0.55 s |
| Go | 0.28 to 0.36 s | 0.30 s |
| Python | 6.3 s | |
| Kāra (`karac build --mir`) | 0.77 to 0.86 s | 0.83 s |
| Kāra legacy (`karac build`) | 0.60 to 0.74 s | 0.64 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 875's does.

v2 takes 1.5 times Rust's median time under overflow checks, 1.7 times
C's and 1.3 times legacy's. Under valgrind's cachegrind C runs 0.55
billion instructions, Rust with overflow checks 0.62 billion, legacy
2.20 billion and v2 1.79 billion, nearly all in `main`. The node is
reference-counted in Kāra, and v2's walk raises the count of each node
a pointer moves onto and lowers the count of the node it leaves, with a
test for a count reaching zero (read from the disassembly), where C's
pointers and Rust's borrowed walk only load the next pointer. Go is the
fastest of all here; its 16-byte nodes, against the 32 bytes C's
`malloc` takes for each, put the 100,000 nodes in half the memory,
which most likely keeps more of them in the cache (inferred, not
traced). The comparison with C and Rust waits until after M4.
