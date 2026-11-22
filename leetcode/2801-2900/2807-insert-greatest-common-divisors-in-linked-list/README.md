# 2807. Insert Greatest Common Divisors in Linked List

Given the head of a linked list `head`, in which each node contains an
integer value.

Between every pair of adjacent nodes, insert a new node with a value
equal to the **greatest common divisor** of them.

Return *the linked list after insertion*.

The **greatest common divisor** of two numbers is the largest positive
integer that evenly divides both numbers.

```
head = [18, 6, 10, 3]   ->  [18, 6, 6, 2, 10, 1, 3]
head = [7]              ->  [7]
```

**Constraints:** the number of nodes in the list is in the range `[1,
5000]`; `1 <= Node.val <= 1000`.

## Approaches

The four own arms share a `shared struct ListNode` whose `next` is a
`mut` field, so a node reached through any handle can be relinked; the
solution keeps LeetCode's plain `ListNode` with `i32` values, and its
harness converts at `build` and `values_of`.

| file | mechanism |
|---|---|
| `gcd.kara` ★ | one walk in place: at each node with a next, a node holding their gcd by Euclid's remainders linked between them, the walk stepping on to the old next; `let ... else` stops at the end |
| `gcd_rec.kara` | by recursion: the rest of the list done first, then a gcd node put in front of it; the gcd itself recursive |
| `gcd_values.kara` | out and back: the values read into a `Vec`, each pair's gcd put between them by `windows(2)`, and a fresh list built from the end |
| `gcd_binary.kara` | Stein's binary gcd, by shifts and subtraction, and the walk a `loop` with a `match` on the node's next |
| `gcd_solution.kara` | a Rust solution as LeetCode's Rust users write it, `Option<Box<ListNode>>`, a nested recursive `fn gcd`, and a walk by `head.as_mut()` that `take`s each next and links a boxed gcd node in front of it, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; 5000 nodes,
LeetCode's most, all 1000; 5000 counting up, each next to a coprime
neighbour, these two with the length and a digest; 3000 random lists of
1 to 12 values up to 30; and 50 of up to 5000 values up to 1000, every
other one of multiples of 12, the last two with the sum of the values
and a checksum. `gcd.py` mirrors the ★ arm and its output is
byte-identical.

```
[18, 6, 6, 2, 10, 1, 3]
[7]
9999 467263528
9999 845803542
3000 short lists: values sum to 343025, checksum 481417647
50 long lists: values sum to 63559872, checksum 832478521
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the values in order, and between each two the largest number
from the smaller of them down that divides both; no Euclid and no list.
The own arms share one `shared` list; the solution's plain one is
renamed `BoxNode` there. It draws 2000 random lists of 1 to 12 values up
to 30, then 50 of up to 5000 values up to 1000, every other one of
multiples of 12, all before any arm answers; the literal reading is
asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 12 values, the list is the literal reading's |
| P2 | 2n - 1 values, the given ones at the even places in order |
| P3 | each inserted value from 1 to the lesser neighbour, dividing both |
| P4 | every value doubled: every value of the answer doubled |
| P5 | the values reversed: the answer reversed |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 781606050, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M8 never ends: with the odd parts left out of
order the subtraction never reaches zero, and both backends were stopped
at 600 s.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the gcd node holding the later value | P1 1801, P3 1851, P5 1871, P6 1851 |
| M2 | ★: the walk stepping two nodes past the pair | P1 1680, P2 1730, P3 1730, P5 834, P6 1730 |
| M3 | rec: the gcd taken with the inserted node, not the old next | P1 1741, P3 1675, P4 1876, P5 1799, P6 1791 |
| M4 | rec: the gcd's remainder taken the wrong way | P1 1765, P3 1815, P5 1871, P6 1815 |
| M5 | values: the last value left off | P1 2000, P2 2050, P3 2050, P5 1871, P6 2050 |
| M6 | values: each pair's gcd put before it | P1 1812, P2 1862, P3 1862, P5 1871, P6 1862 |
| M7 | binary: the shared twos never put back | P1 1240, P4 1876, P6 1290 |
| M8 | binary: the odd parts never swapped into order | killed under both: timed out (600 s) |
| M9 | solution: the new node linked to nothing | P1 1826, P2 1876, P3 1876, P5 1869, P6 1876 |
| M10 | solution: the gcd's base case returning b | P1 1826, P3 1876, P6 1876 |

## Benchmarks

The bench draws 200 lists of 5000 values, LeetCode's most, up to 1000,
every other one of multiples of 12, all of them first, then builds each
afresh as a list and answers it 10 times by the ★ arm in all five
languages, since the answer changes the list in place; the list is read
back to a sum each time, and C frees its nodes as it reads them. Rust
uses LeetCode's `Option<Box<ListNode>>` and the same walk by `as_mut`
and `take`. Every implementation prints `200 lists of 5000, 10 rounds:
values sum to 5206514480, checksum 828860268`.

BENCHTAB

## Verification

All five arms print the same output as `gcd.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★ arm's gcd was first written with Rust's `let (mut a, mut b) =
(a, b);` and `(a, b) = (b, a % b);`. `karac fix` made them `let mut (a,
b) = (a, b);` and `a, b = b, a % b;`, and the other arms were written
that way from the start. The rest checked clean as first written.

LeetCode's Rust template took 30 `karac fix` edits, the wrapper
included: `Option<Box<ListNode>>` became `Option[ListNode]` throughout
and `Box::new(...)` went, Kāra's `Option` holding a recursive type
directly; the nested `fn gcd` was hoisted above `impl Solution` and
`struct Solution {}` added; the `mut head` parameter became `head: own
Option[ListNode]` with a `let mut head = head;`; and `ListNode::new` and
`Solution::` took `.`. The walk itself, `head.as_mut()`, `while let
Some(node) = cur`, `node.next.take()` and
`node.next.as_mut().unwrap().next.as_mut()`, is Kāra as written.
