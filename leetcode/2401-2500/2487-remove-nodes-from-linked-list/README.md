# 2487. Remove Nodes From Linked List

You are given the `head` of a linked list.

Remove every node which has a node with a greater value anywhere to the
right side of it.

Return *the* `head` *of the modified linked list.*

```
head = [5,2,13,3,8]  ->  [13,8]
head = [1,1,1,1]     ->  [1,1,1,1]
```

**Constraints:** the number of nodes in the given list is in the range
`[1, 10^5]`; `1 <= Node.val <= 10^5`.

A node stays exactly when its value is at least every value after it,
so what is left never rises, ends with the list's last node, and holds
every copy of the greatest value. Equal values do not remove each
other. The approaches differ in which way they read the list.

## Approaches

| file | mechanism |
|---|---|
| `remove.kara` ★ | by a stack: one walk, each node popping the nodes on the stack with a smaller value before it is pushed; what is left on the stack is relinked in order. O(n) |
| `remove_reverse.kara` | by reversing: the list reversed in place, one walk unlinking every node smaller than the last one kept, and the list reversed back. In place, O(n) |
| `remove_rec.kara` | recursively: the rest cleared first, its head then the greatest value to the right, and a node smaller than that dropped for the cleared rest. O(n) deep |
| `remove_values.kara` | by values: the values read out into a `Vec`, walked from the back with the greatest so far, and a new list built of those at least that great. O(n) space |
| `remove_iter.kara` | iterators: an `impl Iterator` over the nodes, its handles `collect`ed and folded from the back into the kept list, a `match` with a guard passing over a node smaller than the kept head |
| `remove_solution.kara` | LeetCode's Rust template (`Option<Box<ListNode>>` with `i32` values, each node taken off the list by `take()` onto a `Vec<Box<ListNode>>` that pops the smaller ones, then popped back into a list), carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's two examples and six
more, each list and what is left; then, as a count and a checksum, 2000
random lists of 1 to 200 values from 1 to `10^5`, and 2000 from 1 to 5,
where ties are common; then the constraints' largest, `10^5` values
falling, rising, all the same, and random. `remove.py` mirrors the ★
arm and its output is byte-identical, and the mirror was checked on
20000 random lists of 1 to 12 values from 1 to 3 or to 20 against the
statement read literally. The two agreed on every list.

The arms other than the template keep their nodes as a `shared struct`,
so a node is a handle and the arms relink the list they are given. The
template's nodes are its own `i32` struct, owned; its harness converts
the `i64` values at `build` and `values_of`.

`check` first reports 8 errors on the template, all Rust's spellings:
`Option<..>` and `Vec<..>` in angle brackets, `Vec::new`, `struct
Solution;`, and the two `while let Some(mut node)`. `karac fix` carries
it in one call, reporting 25 edits: the brackets, with `Box` dropped
since a struct field of the struct's own type is already a link; `.`
for `::`; `struct Solution {}`; each `mut node` taken out of its
pattern and rebound as `let mut node = node;` inside the loop; `own` on
the method's parameter and the adapter's, which hand the list over; and
`ref` in the harness's `values_of`, whose cursor walks a borrowed list
of owned nodes and so must borrow each `next`. The `#[derive]` and
`#[inline]` attributes, the two-space struct and `take()` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a value kept when no value after it, compared one by one, is
greater. The template's struct is renamed `BoxNode` there, beside the
shared `ListNode` of the others, and its adapter copies the values into
a list of `BoxNode`s and the answer back. It checks 300 random lists of
1 to 12 values, from 1 to 3 or from 1 to 20; then 20 of one or two
values, and 40 of 50 to 100 values from 1 to `10^5`. All 360 are drawn
before any arm answers. Each arm is given a freshly built list for
every question, since the arms change the list they are given.

| | property |
|---|---|
| P1 | the values kept are the statement read literally |
| P2 | the values kept never rise, and the last is the list's last |
| P3 | the values kept are the list's in order, every copy of its greatest among them |
| P4 | a value greater than every other put at the end: it alone is kept |
| P5 | removing again keeps every value |
| P6 | each arm agrees with at least three of the other five |

P2 and P3 are the shape of every right answer, which a wrong one can
still have; P4 and P5 ask the arm two questions whose answers follow
from the statement without reading it: a new greatest value at the end
is greater than everything before it, and a list that never rises loses
nothing.

The differential prints `360 cases: checksum 919441890, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and adds up the same sums. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: the first node passed over | P1 123, P2 32, P3 123, P5 328, P6 123 |
| M5 | ★: one node popped at most | P1 224, P2 224, P4 307, P5 224, P6 224 |
| M6 | ★: a greater top popped | P1 319, P2 243, P3 270, P4 360, P6 319 |
| M8 | reverse: never reversed back | P1 225, P2 225, P3 199, P5 225, P6 225 |
| M10 | reverse: the walk moving onto the unlinked node | P1 238, P2 238, P4 328, P5 238, P6 238 |
| M11 | reverse: the walk begun at the second node | P1 187, P2 187, P3 32, P4 360, P6 187 |
| M12 | rec: a tie dropped | P1 148, P3 123, P6 148 |
| M13 | rec: a dropped node keeping its old rest | P1 295, P2 295, P4 360, P6 295 |
| M15 | rec: only the next node compared | P1 267, P2 267, P4 328, P5 32, P6 267 |
| M18 | values: the greatest one short | P1 135, P2 135, P4 360, P6 135 |
| M20 | values: the first value as the floor | P1 120, P2 120, P5 139, P6 120 |
| M21 | values: each value read twice | P1 360, P3 360, P4 360, P5 360, P6 360 |
| M24 | iter: folded from the front | P1 300, P2 280, P3 213, P4 360, P5 237, P6 300 |
| M25 | iter: every other node | P1 360, P2 314, P3 253, P4 360, P5 328, P6 360 |
| M26 | iter: the kept list dropped at a smaller node | P1 295, P2 262, P3 274, P4 360, P6 295 |
| M29 | solution: the last node never pushed | P1 360, P2 311, P3 135, P4 360, P5 328, P6 360 |
| M31 | solution: the bottom node left off | P1 360, P2 75, P3 360, P4 360, P5 285, P6 360 |

P1 and P6 kill all seventeen, P2 fifteen, P4 thirteen, and P3 and P5
eleven each.

Fourteen are not kept, and none survives. Nine fail exactly as a kept
one. Every arm's tie edit, the ★ arm's and the template's tie popped,
the reverse arm's tie unlinked, the values arm's tie left out and the
iter arm's tie passed over (M1, M27, M7, M17, M22), fails as the rec
arm's tie dropped (M12): each loses the earlier of two equal values with
nothing greater after them, which P1, P3 and P6 see on the 148 cases
with such a tie. The ★ arm's nothing ever popped (M2) fails as the rec
arm's dropped node keeping its old rest (M13), both keeping
nodes that should go; the rec arm's value one smaller kept and the template's value one
smaller popped too late (M16, M30) as the values arm's greatest one
short (M18); and the values arm's values walked from the front (M19) as
the iter arm's fold from the front (M24). The other five fail as one
another, in two sets, and no member of either is kept, since their arms
already hold three kept edits, or two in the template's case, with
failures of their own: the ★ arm's kept nodes never linked, the rec
arm's kept node losing the rest and the iter arm's kept node linked to
nothing (M3, M14, M23) each answer the greatest value alone (P1 285, P2
225, P3 123); the reverse arm's rest cut at a smaller node and the
template's stack cleared by a greater node (M9, M28) each keep only the
values after the last node to be removed, losing the kept ones before
it, and fail P1, P3 and P6 on 202 cases.

## Verification

Every arm prints the same output as `remove.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 4.5 to 12 s and the differential 1.0 s; under `karac __mir-llvm-asan` the arms take 1.3 to 3.8 s and the differential 0.6 s; and under `karac run` the differential takes 0.5 s.

## Benchmarks

The bench builds 22000 lists of 1000 nodes, each node's value falling
by 10 from the one before with a noise of 0 to 36 added, the noise
drawn from the list's number, the node's place and the checksum so far,
so no list is built before the last is answered; about half the nodes
are removed. Each list is cleared by the ★ arm's stack and the kept
nodes folded into the checksum. The bench uses the ★ arm in all five
languages: Rust's nodes are `Rc<RefCell<ListNode>>`, the model of a
`shared struct`; C's are `malloc`'d and freed, a popped node at once;
Go's are pointers. Every implementation prints `22000 lists of 1000
nodes: 11308000 kept, checksum 223091611`.

BENCHTAB
