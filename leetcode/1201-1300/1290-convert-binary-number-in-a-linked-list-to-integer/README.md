# 1290. Convert Binary Number in a Linked List to Integer

Given `head` which is a reference node to a singly-linked list. The value
of each node in the linked list is either `0` or `1`. The linked list
holds the binary representation of a number.

Return the decimal value of the number in the linked list.

The most significant bit is at the head of the linked list.

```
head = [1,0,1]  ->  5      (101) in base 2 = (5) in base 10
head = [0]      ->  0
```

**Constraints:** the linked list is not empty; the number of nodes will
not exceed `30`; each node's value is either `0` or `1`.

The arms are `fn get_decimal_value(head: Option[ListNode]) -> i64`. The
Kāra arms take `shared struct ListNode { mut val: i64, mut next:
Option[ListNode] }`, the counted node the other linked-list katas use.
The two Rust arms keep the `ListNode` LeetCode gives Rust users, a plain
struct whose `next` owns the rest of the list.

## Approaches

| file | mechanism |
|---|---|
| `get_decimal_value.kara` ★ | one walk from the head, the value so far doubled and the node's bit added at each node, as a binary number is read from its most significant digit. O(n) |
| `get_decimal_value_shift.kara` | the same walk in bit operations: the value shifted left a place and the bit or-ed into the place freed. O(n) |
| `get_decimal_value_count.kara` | two walks: the first counts the nodes, the second adds each set bit's place value, `2.pow(place)` with `place` the number of nodes after it. O(n) |
| `get_decimal_value_string.kara` | the bits written out as a string with `char.from_digit(bit, 2)`, then read back digit by digit with `c.to_digit(2)`. O(n) |
| `get_decimal_value_recursive.kara` | recursion that returns the value of the list from a node with the number of nodes from there, so each node's bit is placed above the rest as the recursion unwinds. O(n) |
| `get_decimal_value_solution.kara` | a Rust solution as LeetCode's Rust users write it (`Option<Box<ListNode>>`, a walk over `&node.next` shifting each bit in), carried to Kāra by `karac fix` |
| `get_decimal_value_radix.kara` | a second Rust solution as LeetCode's Rust users write it (the bits pushed to a `String` with `push_str(&node.val.to_string())`, read back with `i32::from_str_radix(&s, 2).unwrap()`), carried to Kāra by `karac fix` |
| `differential.kara` | the seven arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples, a single 1,
a 1 behind three 0s, then 30 ones and 30 alternating bits from a 1
(`5 0 1 1`, `1073741823 715827882`); then 20000 random lists of 1 to 30
bits, the first a 1 unless the list has one node (`20000 random lists of
1 to 30 bits: total 1087803180735, checksum 645438766`).
`get_decimal_value.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`.

The Mend loop: the five Kāra arms share one harness, and its first draft
wrote Rust's `&&` in the random lists' head bit; `E0001` said Kāra spells
it `and`, and `karac fix` made the change in each (1 fix each). The string
arm took one more: `c.to_digit(2).unwrap() as i64` lost its `as i64` as a
widening. The two Rust arms each take one round, 18 fixes and 21 by
`karac fix`'s count: `Option<Box<ListNode>>` to `Option[ListNode]`,
`struct Solution;` to `struct Solution {}`, `::` to `.`, `let mut cur =
&head;` and `cur = &node.next;` to `ref head` and `ref node.next`, the
wrapper's `as i64` dropped as a widening, and the harness's `&&`. The
solution arm's `let mut ans = 0;` became `let mut ans: i32 = 0;`, since
the literal would otherwise settle to `i64` before it meets the `i32`
bit. The radix arm's `push_str(&node.val.to_string())` lost its `&`, and
`i32::from_str_radix(&s, 2)` became `i32.from_str_radix(s, 2)`: Kāra has
it, returning an `Option` where Rust returns a `Result`, so the
`.unwrap()` stands. Both Rust arms' outputs match on the first run. No
gap was met. (`from_str_radix` is listed in the self-hosting checklist,
not yet in `docs/library/`.)

## Differential

`differential.kara` holds copies of the seven arms and the statement read
literally: each bit times two to the power of the number of bits after it,
each power built by doubling, summed. 3000 lists of 1 to 29 bits, so that
a bit added before or after keeps to the constraints' 30 nodes: a third
lead with a 1, a third with a run of 0s a third of their length, and a
third are mostly one bit, so that long runs of either come up. Every list
is drawn before any arm answers; each property is checked on every arm.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | a 0 after the last bit: twice the answer |
| P3 | a 1 after the last bit: twice the answer, plus 1 |
| P4 | a 0 in front: the same answer |
| P5 | every bit flipped: `2^n - 1` less the answer |
| P6 | the ★ arm's answer |

All 126,000 checks pass on every arm: `3000 lists: checksum 235570125,
126000 checks over 7 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac __mir-llvm-run` and the AddressSanitizer build. Python gives
the same checksum.

## Mutation testing

Fifteen edits to the differential, two to each arm and three to the
recursive arm, each run under both `karac __mir-llvm-run` and `karac
__mir-run`. Every one is killed, fails the same way under both backends
and not by a crash. Ten are kept, at least one to each arm, so that no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the bit added at twice its weight | P1 2790, P2 2847, P3 3000, P5 3000, P6 16740 |
| M2 | ★: the value started at 1 | P1 3000, P4 3000, P5 3000, P6 18000 |
| M4 | shift: two places shifted | P1 2727, P2 2847, P3 2847, P5 2902, P6 2727 |
| M5 | count: the first place counted from n | P1 2847, P3 3000, P5 3000, P6 2847 |
| M7 | string: the digits read from the end | P1 2561, P2 2847, P3 2799, P4 2847, P6 2561 |
| M8 | string: the first digit skipped | P1 1545, P4 1545, P5 3000, P6 1545 |
| M15 | recursive: the rest of the list dropped | P1 2717, P3 3000, P4 1545, P5 2902, P6 2717 |
| M11 | solution: shifted right, not left | P1 2727, P2 1530, P3 1530, P5 2902, P6 2727 |
| M13 | radix: every bit written flipped | P1 3000, P2 3000, P3 3000, P4 3000, P6 3000 |
| M14 | radix: every `01` written as `10` | P1 2540, P3 1470, P4 1545, P5 2646, P6 2540 |

The five left out each fail exactly as a kept one does, since they make
the same wrong answer in another arm: the shift arm's bit or-ed in before
the shift, the count arm's first place counted from n and the recursive
arm's empty list counted one wide all double the value; the recursive
arm's width that never grows, like a shift of two places, is right only
on a list with at most one 1; and the count arm adding the 0 bits, like
the solution arm flipping each bit as it goes in, reads the complement.

P1 and P6 kill all ten, P3 and P5 eight each, P4 six and P2 five. When
the ★ arm is the one mutated, P6 fails on every arm that disagrees with
it, so its count runs past the number of lists. P5, the complement, misses
only the edits that read the bits in the wrong order or flip them,
since a list read backwards or flipped is still read backwards or flipped
after its bits flip; P4, a 0 in front, misses the edits that keep the
leading 0's weight at nothing.

## Benchmarks

The bench builds 10^4 lists of 30 nodes, the constraints' longest, once
from its own generator, then makes 500 passes; each sets one bit of every
list from the checksum so far, by walking to it, so no answer carries
over, then reads every list back with the ★ arm, folding the value plus
the pass into the checksum. Every node is its own allocation in all five
languages: a counted `shared struct` in Kāra, LeetCode's `Box`ed
`ListNode` in Rust, `malloc` in C, a pointer in Go and an object with
`__slots__` in Python. Every implementation prints `500 passes over 10^4
lists of 30 bits: checksum 606237803`.

BENCHTAB
