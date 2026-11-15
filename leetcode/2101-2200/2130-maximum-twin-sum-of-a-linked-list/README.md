# 2130. Maximum Twin Sum of a Linked List

In a linked list of size `n`, where `n` is even, the `i`th node
(0-indexed) of the linked list is known as the twin of the `(n-1-i)`th
node, if `0 <= i <= (n / 2) - 1`.

For example, if `n = 4`, then node `0` is the twin of node `3`, and node
`1` is the twin of node `2`. These are the only nodes with twins for
`n = 4`.

The twin sum is defined as the sum of a node and its twin.

Given the `head` of a linked list with even length, return the maximum
twin sum of the linked list.

```
head = [5,4,2,1]   ->  6
head = [4,2,2,3]   ->  7
head = [1,100000]  ->  100001
```

**Constraints:** the number of nodes in the list is an even integer in
the range `[2, 10^5]`; `1 <= Node.val <= 10^5`.

The twin of a node in the first half is as far from the end as the node
is from the start, so the list's first half read forwards meets its
second half read backwards. A list only walks forwards, so the
approaches differ in how they get the second half backwards: a copy of
the values, the first half's links turned round, a stack, or recursion.
O(n).

## Approaches

| file | mechanism |
|---|---|
| `twins.kara` ★ | the values read into a `Vec` through a `shared struct` cursor, then each value in the first half added to its twin by index |
| `twins_reverse.kara` | two runners, the slow one turning the first half's links back as it goes; then the reversed first half and the second half walked side by side. O(1) extra space; the list is changed |
| `twins_stack.kara` | one walk to count; a second pushes the first half's values onto a `Vec` and pops one against each value of the second half |
| `twins_rec.kara` | recursion to the end of the list; on the way back each node meets its twin from a front cursor passed as `mut ref Option[ListNode]`, which steps once per return. O(n) deep |
| `twins_deque.kara` | a `struct Walk` with `impl Iterator` over the nodes, `collect`ed into a `VecDeque`, then emptied from both ends at once with `while let (Some(a), Some(b))` |
| `twins_solution.kara` | LeetCode's Rust template (`Option<Box<ListNode>>` with `i32` values): the values read out through a `&head`, `&node.next` cursor, then `map` and `max` over the first half; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more (one pair, the largest twins in the middle, at the ends, and two
equal sums), each with its answer; then the total and a checksum over
2000 random lists of 2 to 20 values from 1 to 100; then the
constraints' largest, 100000 nodes of 1 to 100000 in order and 100000
random ones. `twins.py` mirrors the ★ arm and its output is
byte-identical.

No compiler gap was met in the arms; the interpreter's time on the
template is in Verification.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every node, its twin found by walking from the head to
the place as far from the start as the node is from the end, and the
largest of the sums over every node, both halves; no half is assumed.
It checks 300 random lists of 2 to 12 values from 1 to 20; then 30 of 2
to 40 values from 1 to 100000; then 30 of 2 to 12 of one value. All 360
are drawn before any arm answers. Each arm is given a freshly built list
for every question, since the reverse arm changes the list it is given.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the list reversed: the same answer |
| P3 | every value doubled: twice the answer |
| P4 | a value put at each end: the larger of the answer and their sum |
| P5 | the two halves swapped: the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 lists: checksum 325018521, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
lists. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Twenty-eight edits to the differential, four to six to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last twins never compared | P1 132, P5 144, P6 132 |
| M2 | ★: each value with the one before its twin | P1 308, P2 310, P4 321, P5 179, P6 308 |
| M3 | ★: each value with its neighbour | P1 204, P2 233, P4 322, P5 266, P6 204 |
| M7 | reverse: each turned node cut loose | P1 191, P4 326, P5 273, P6 191 |
| M8 | reverse: the outermost pair's sum kept | P1 207, P4 35, P5 273, P6 207 |
| M9 | reverse: the halves walked one node apart | P1 305, P2 267, P4 326, P6 305 |
| M10 | stack: the middle pushed as well | P1 313, P2 264, P4 329, P5 154, P6 313 |
| M11 | stack: the stack taken from the bottom | P1 226, P4 355, P6 226 |
| M12 | stack: each node counted twice | P1 360, P4 360, P6 360 |
| M14 | rec: the front never stepped | P1 256, P2 316, P4 214, P5 318, P6 256 |
| M16 | rec: each node with itself | P1 322, P4 320, P6 322 |
| M17 | rec: the end worth a value | P1 319, P3 319, P6 319 |
| M18 | deque: both taken from the front | P1 227, P4 354, P5 114, P6 227 |
| M21 | deque: each value one more | P1 360, P3 360, P4 325, P6 360 |
| M28 | deque: the deque started with an extra value | P1 310, P2 315, P3 66, P4 323, P5 72, P6 310 |
| M23 | solution: the smallest twin sum | P1 278, P4 359, P6 278 |
| M25 | solution: each value halved | P1 360, P3 243, P4 328, P6 360 |

P1 and P6 kill all seventeen, P4 fifteen, P5 nine, P2 six and P3 four.
P4 puts a new pair round the list, which every edit that pairs the
wrong nodes, keeps the wrong sum or counts the wrong length answers
wrongly; it misses only an answer that is wrong in the middle and right
at the ends (M1) and a constant added to the answer (M17), whose new
pair is still beaten. P5 swaps the halves, which keeps every twin
pair, so it sees the edits that pair by place rather than by twin: the
last twins left out (M1), a node with its neighbour or one off (M2, M3,
M10), or the sum of the outermost or innermost pair alone (M7, M8). P2
reverses the list, which sees the pairings that are not symmetric
(M2, M3, M9, M10, M14, M28). P3 doubles every value, which sees an
error that does not double with it: a unit or a constant added (M17,
M21, M28) and halving's rounding (M25).

Of the twenty-eight, eleven were not kept. One cannot be kept: the
adapter handing over the list without its head, `head.unwrap().next`,
is refused, since the adapter's parameter borrows and `unwrap` would
move out of it. None is equivalent, none survives, and none fails by a
crash. Eight fail as a kept one does: the ★ arm keeping the last pair's
sum as M7; the reverse arm's fast runner stepping one node at a time as
M12; the stack and deque arms taking the larger of two twice as M16;
the rec arm keeping only the first twins as M8; the deque arm's walk
starting at the second node as M9; the template pairing each value
with the one half a list on as M11; and the deque arm taking both from
the back as M18. Two are killed with checks of their own but were left
out because their arms keep their share: the ★ arm doubling the first
half's values (P1 315, P2 297, P4 319, P5 297, P6 315) and the template
comparing the first half with the middle (P1 222, P2 240, P4 324, P5
239, P6 222).

## Verification

Every arm prints the same output as `twins.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.2 s to 2.3 s, except the
template arm, 22 minutes, and the differential 0.8 s. The template's
list is a plain struct, `next: Option[ListNode]`, not a `shared` one, and
the interpreter walks it in quadratic time: 10000 nodes take 4 s, 20000
take 18 s, and the 100000 of the last line nearly all of the 22 minutes,
where the compiled arm takes 0.2 s. Each reference into the list is an
address whose path grows by a step per node. That is filed as karac
B-2026-11-14-61.

`karac fix` carries the template in three rounds of 20, 6 and 2 edits:
Rust's spellings (`Option<Box<ListNode>>` to brackets, `&head` and
`&node.next` to `ref head` and `ref node.next`, `struct Solution;` to
`struct Solution {}`, `Solution::` and `Box::new` to `.`); then
`Box[ListNode]` to `ListNode` and `Box.new(..)` dropped, since a
struct's recursive field needs no box; then `vec![]` to `Vec.new()` and
the adapter's `as i64` dropped, since an `i32` widens on return. The
definition's `#[derive(..)]` and `#[inline]` are kept as they are.

## Benchmarks

The bench builds 10 lists of 100000 nodes of 1 to 100000 once, then
solves every list 50 times, one node a random way along given a new
value of 1 to 200000 before each solve so that no solve repeats one
before, with the ★ arm in all five languages; Rust's list is
`Option<Box<ListNode>>` and C's malloc'd nodes. Every implementation
prints `500 solves: 99672700 in all, checksum 815354695`.

BENCHTAB
