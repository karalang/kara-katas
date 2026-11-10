# 2074. Reverse Nodes in Even Length Groups

You are given the `head` of a linked list.

The nodes in the linked list are sequentially assigned to non-empty
groups whose lengths form the sequence of the natural numbers (`1, 2, 3,
4, ...`). The length of a group is the number of nodes assigned to it. In
other words,

- The 1st node is assigned to the first group.
- The 2nd and the 3rd nodes are assigned to the second group.
- The 4th, 5th, and 6th nodes are assigned to the third group, and so on.

Note that the length of the last group may be less than or equal to
`1 + the length of the second to last group`.

Reverse the nodes in each group with an even length, and return the
`head` of the modified linked list.

```
head = [5,2,6,3,9,1,7,3,8,4]  ->  [5,6,2,3,9,1,4,8,3,7]
head = [1,1,0,6]              ->  [1,0,1,6]
head = [1,1,0,6,5]            ->  [1,0,1,5,6]
```

**Constraints:** the number of nodes in the list is in the range
`[1, 10^5]`; `0 <= Node.val <= 10^5`.

A group is even or odd by the nodes it actually has, not by the length
it should have, and only the last group can fall short; that is the one
catch, in the third example, where the last group should hold three
nodes and holds two. One walk counts each group's nodes up to the length
it should have and turns an even group round in place: O(n). The
approaches differ in whether they relink the nodes, move the values, or
build a new list.

## Approaches

| file | mechanism |
|---|---|
| `groups.kara` ★ | nodes a `shared struct`; from the node before each group, its nodes counted up to the length it should have, and an even group's links turned round in place, its first node becoming the node before the next group. O(n) |
| `groups_values.kara` | the values out into a `Vec`, `reverse()` on each even group's range of it, and a new list built from the back |
| `groups_swap.kara` | the links kept and the values moved: each group's nodes gathered as a `Vec` of handles, and in an even group the first and last values, the second and second last and so on swapped with a parallel assignment |
| `groups_rec.kara` | recursive, a group a call: `take` peels a group's values off the front, `regroup` handles the rest with the next length first and then puts the group in front of it, turned round when its length is even; a new list |
| `groups_iter.kara` | a `struct Groups` implementing `Iterator`, yielding each group's values as a `Vec`, folded into the answer's values with an even group `rev()`ed on the way in |
| `groups_solution.kara` | LeetCode's Rust template (`Option<Box<ListNode>>` of `i32`s, the values read out through `&head` and `&node.next`, `vals[i..end].reverse()` on each even group, a new list of `Box::new(ListNode::new(v))` built from the back), carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more, each list and its answer; then a checksum of the answers for 500
random lists of 1 to 200 values up to `10^5`; then the checksum, first
and last value of the answer for the constraints' largest, 100000
values. `groups.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each place's group found by counting groups of 1, 2, 3, ...
places, the last as long as the list leaves it, and a place in a group
of even length given the value at its mirror in that group. It checks
300 random lists of 1 to 40 values below 2, 3 or 10; then 20 whose
length is a sum `1 + 2 + ... + k`, so the last group is whole, and 20
one longer, so the last group has one node. All 340 are drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer's answer is the list again |
| P3 | the list of places `0` to `n - 1` is answered with places each in its own group, and a place in a group of odd length where it was |
| P4 | the answer holds the list's values, as many of each |
| P5 | the answer for the whole groups at the front is the front of the answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 lists: checksum 87552344, 12240 checks over
6 arms: 0 failures` under every lane in Verification; the checksum of
the literal answers was checked against a Python reading of the same
lists. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-two edits to the differential, five to six to each of its arms,
each run under `karac __mir-llvm-run`, and the kept ones under `karac
__mir-run` too. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every group one longer | P1 302, P3 287, P5 200, P6 302 |
| M2 | ★: a short last group never turned | P1 93, P6 93 |
| M3 | ★: the turned group not linked in | P1 320, P2 320, P3 310, P4 320, P5 259, P6 320 |
| M4 | values: the first node's value never read | P1 340, P2 340, P3 329, P4 340, P5 268, P6 340 |
| M5 | values: the list built back to front | P1 322, P2 309, P3 329, P5 266, P6 322 |
| M6 | values: each reversal from the group's second value | P1 303, P6 303 |
| M7 | swap: the middle pair left unswapped | P1 292, P6 292 |
| M8 | swap: a value copied, not swapped | P1 301, P2 301, P4 277, P6 301 |
| M9 | swap: a group of two never turned | P1 228, P6 228 |
| M10 | rec: a group's length taken as it should be, not as it is | P1 90, P3 40, P6 90 |
| M11 | rec: the odd groups turned instead | P1 307, P3 296, P6 307 |
| M12 | rec: the first group of two | P1 321, P3 329, P5 108, P6 321 |
| M13 | iter: no group reversed | P1 301, P6 301 |
| M14 | iter: the groups growing by two | P1 300, P3 118, P5 135, P6 300 |
| M15 | iter: every group one short | P1 340, P2 340, P4 340, P6 340 |
| M16 | solution: the adapter's values one more | P1 340, P2 340, P3 340, P4 340, P6 340 |
| M17 | solution: the adapter's last value dropped | P1 340, P2 340, P4 340, P5 268, P6 340 |

P1 and P6 kill all seventeen, P3 nine, P2 and P5 seven each, and P4
six. P3, which hands each arm the list of its own places, sees an edit
that moves a value out of its group or moves one in an odd group: groups
of the wrong lengths (M1, M12, M14), the odd groups turned (M11), or the
last group judged by the length it should have (M10, the statement's
one catch). It cannot see an even group turned wrongly within itself
(M6, M7, M9, M13), and those are told apart only by how often they are
wrong; the lists drawn from two or three values are there so that how
often differs. P2 sees an edit whose answer is not its own inverse,
and P4 one that loses or invents a value: links dropped (M3), a value
copied over another (M8), an adapter's value lost (M17).

Of the thirty-two, fifteen were not kept, and none survives. All fail
as a kept one: the ★ and iter arms' odd groups turned as M11; the ★
arm's group's last node left out of the turn as M3; the values, rec,
iter and Rust arms' groups one longer, first group of two or a group
taking one value too many as M12; the values and Rust arms' length as
it should be as M10; the values arm's no group reversed as M13; the swap
arm's value swapped with its mirror's neighbour and the Rust arm's
reversal one short at the end as M6; the swap and rec arms' groups
growing by two as M14; the Rust adapter's answer read backwards as M5.
Two edits first written crashed and were replaced before the run (the
first value dropped through `unwrap()` and `[1..]`, which meet the empty
list P2 hands back).

## Verification

Every arm prints the same output as `groups.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error, but
the Rust arm under `karac __mir-run`. `karac run` and a `karac build`
binary print the same output for every arm and the differential. `karac
check --output=json` reports nothing on any of them.

Under `karac __mir-run` the Kāra arms take 1.6 s to 2.9 s and the
differential 2.5 s (timed while other work shared the machine).

The Rust arm's nodes are a plain struct, not `shared`, and the
interpreter builds a list of them in quadratic time (B-2026-11-09-46):
under `karac __mir-run` it prints the examples and the 500 random lists
and was stopped at 600 s on the 100000-node list. Under the compiled
lanes it takes 0.3 s.

The iter arm's fold was first written `|acc: Vec[i64], group| { let mut
acc = acc; .. }`, Rust's `|mut acc, group|`; an annotated bare closure
parameter borrows, and `karac fix` made it `acc: own Vec[i64]`.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in three rounds of 25, 6 and 1 edits: Rust's spellings (`Vec<..>` and
`Option<..>` to brackets, `&head` and `&node.next` to `ref`, the `&` of
`for &v` dropped, `let (mut i, mut k)` to `let mut (i, k)`, `struct
Solution;` to `struct Solution {}`, `::` paths to `.`); then `Box`
dropped, in the field, the signatures and `Box::new(..)`; then `vec![]`
to `Vec.new()`. The fixed arm reads as the template does, `i32`s and
all.

## Benchmarks

The bench runs the ★ arm in all five languages for 2000 rounds, each a
fresh list of 10000 to 10006 values turned group by group in place and
folded into a checksum: 20 million nodes built, walked, relinked and
freed. The nodes are Kāra's `shared struct`, Rust's
`Rc<RefCell<ListNode>>`, C's `malloc`'d structs and Go's `*ListNode`.
Every implementation prints `2000 rounds: checksum 836982902`.

BENCHTAB
