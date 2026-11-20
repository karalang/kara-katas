# 1721. Swapping Nodes in a Linked List

You are given the `head` of a linked list, and an integer `k`.

Return *the head of the linked list after **swapping** the values of
the* `kth` *node from the beginning and the* `kth` *node from the end
(the list is **1-indexed**).*

```
head = [1,2,3,4,5], k = 2                       ->  [1,4,3,2,5]
head = [7,9,6,6,7,8,3,0,9,5], k = 5             ->  [7,9,6,6,8,7,3,0,9,5]
```

**Constraints:** the number of nodes in the list is `n`;
`1 <= k <= n <= 10^5`; `0 <= Node.val <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `swap.kara` ★ | the kth node from the end is as far from the last node as the head is from the kth node, so once a cursor reaches the kth node, a runner from it to the end drags a second cursor from the head to the kth from the end; the two values swap and no node moves. O(n), in place |
| `swap_length.kara` | the length n counted first, then the two nodes walked to, k - 1 and n - k places from the head. O(n), in place |
| `swap_handles.kara` | a `shared struct` handle is a counted reference to its node, so every node's handle goes into a vector and the two are indexed, `nodes[k - 1]` and `nodes[n - k]`. O(n) time and handles |
| `swap_solution.kara` | a Rust solution as LeetCode's Rust users write it (`Option<Box<ListNode>>` with `i32` values): the values walked out through `&node.next` into a vector and swapped there, and a new list built behind a dummy head with `tail.next.as_mut().unwrap()`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

The ★, length and handles arms share a `shared struct ListNode` with
`mut val: i64`; the solution arm keeps LeetCode's plain `ListNode` with
`i32` values, and its harness converts them at `build` and `values_of`.

Every arm prints the same 8 lines: LeetCode's two examples, one node,
two nodes, and the middle node of an odd list swapped with itself; then
the nodes counted and a checksum for 3000 random lists of up to 12
nodes, 300 of up to 1000, and 10 of up to `10^5`, each with a random k.
`swap.py` mirrors the ★ arm and its output is byte-identical.

```
[1,4,3,2,5]
[7,9,6,6,8,7,3,0,9,5]
[1]
[2,1]
[1,2,3]
3000 lists of up to 12 nodes: 19582 nodes, checksum 254406322
300 lists of up to 1000 nodes: 144679 nodes, checksum 655796649
10 lists of up to 100000 nodes: 153661 nodes, checksum 497065662
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: each node counted from the beginning and from the end, the
kth from the beginning given the value of the kth from the end and the
kth from the end the value of the kth from the beginning, every other
node keeping its own. It checks 3000 random lists of 1 to 12 nodes of
values up to 100 and a k from 1 to the length. Every case is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | a list of 1 to n, each node's place, comes back with places k and n + 1 - k swapped |
| P3 | the list reversed gives the answer reversed |
| P4 | k and n + 1 - k give the same answer |
| P5 | each arm agrees with at least two of the other three |

P2 is there because random values up to 100 are often equal, and a
swap of two equal values cannot be seen.

The differential prints `3000 problems: checksum 657539674, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, the list's values swapped at `k - 1` and
`len - k`, gives the same checksum. On a failure it prints the first ten
and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M3, M6 and M7 all leave both nodes
holding one of the two values, in three arms, and fail the very same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first cursor one node short | P1 1913, P2 1918, P4 2282, P5 1913 |
| M2 | ★: the second cursor starting at the kth node, not the head | P1 2231, P2 2236, P3 1744, P4 2548, P5 2231 |
| M3 | ★: the swap's two writes in the wrong order | P1 2534, P2 2555, P3 2534, P4 2534, P5 2534 |
| M4 | length: the node from the end walked one place short | P1 2279, P2 2281, P3 1956, P4 2554, P5 2279 |
| M5 | length: the count stopped at the kth node | P1 2276, P2 2281, P3 1743, P4 2548, P5 2276 |
| M6 | handles: the node from the end never given the first value | P1 2534, P2 2555, P3 2534, P4 2534, P5 2534 |
| M7 | handles: the value kept from the node from the end | P1 2534, P2 2555, P3 2534, P4 2534, P5 2534 |
| M8 | solution: the value swapped with itself | P1 2534, P2 2555, P5 2534 |
| M9 | solution: the rebuilt list missing its first value | P1 3000, P2 3000, P3 2773, P5 3000 |
| M10 | solution: the values collected in reverse | P1 2771, P2 2773, P5 2771 |

## Benchmarks

The bench builds 10 random lists of `10^5` nodes, LeetCode's longest,
once, and draws a k for every list and round first; each of 100 rounds
then swaps every list once more in place by the ★ arm, in all five
languages, and the head's value after each swap goes into the checksum.
Every implementation prints `10 lists of 100000 nodes, 100 rounds:
heads sum to 56400, checksum 198416564`. Kāra, Go and Python allocate
each node on its own; the C mirror allocates each list's nodes in one
array, linked by pointers in order, and the Rust mirror holds them in a
vector linked by index, since `Option<Box<ListNode>>` gives no second
cursor into a list the first one is in. The C build also runs clean
under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| Go | 0.209 s |
| C (`clang -O3`) | 0.213 s |
| Kāra (`karac build`) | 0.312 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.313 s |
| Rust (`rustc -O`) | 0.611 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.614 s |
| Python | 2.0 s |

The sequential Kāra build is 49% faster than Rust and 49% faster than
Rust with overflow checks on, the equal-safety comparison
(BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.302 s and 0.310 s on one
run).

## Verification

All four arms print the same output as `swap.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ and handles arms checked clean as first written. The length arm
first bound its two nodes `let mut front` and `let mut back`; writing a
`mut` field of a `shared struct` goes through the handle, so the
bindings need no `mut`, the `unused_mut` lint said so, and `karac fix`
dropped both.

LeetCode's Rust template took one `karac fix` of 25 edits: every
`Option<Box<ListNode>>` written `Option[ListNode]`, `struct Solution {}`
added, `vec![]` written `Vec.new()`, `&head` and `&node.next` written
`ref head` and `ref node.next`, `k as usize` written `k as i64`,
`Box::new(ListNode::new(..))` written `ListNode.new(..)`, `&mut dummy`
written `mut ref dummy`, and in the harness's `values_of`, which walks
a plain struct's list, `cur = node.next` written `cur = ref node.next`.
`tail.next.as_mut().unwrap()` and `dummy.next` carried over as written.

The differential checked clean as first written. `arm_name` in it
indexes a list of string literals for a `Str`, as #1662's does
(B-2026-11-19-131).
