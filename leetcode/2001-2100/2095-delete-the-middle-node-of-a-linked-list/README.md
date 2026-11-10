# 2095. Delete the Middle Node of a Linked List

You are given the `head` of a linked list. Delete the middle node, and
return the `head` of the modified linked list.

The middle node of a linked list of size `n` is the `⌊n / 2⌋`th node
from the start using 0-based indexing, where `⌊x⌋` denotes the largest
integer less than or equal to `x`.

For `n = 1`, `2`, `3`, `4` and `5`, the middle nodes are `0`, `1`, `1`,
`2` and `2`, respectively.

```
head = [1,3,4,7,1,2,6]  ->  [1,3,4,1,2,6]
head = [1,2,3,4]        ->  [1,2,4]
head = [2,1]            ->  [2]
```

**Constraints:** the number of nodes in the list is in the range `[1,
10^5]`; `1 <= Node.val <= 10^5`.

The node to step over is the one at index `n / 2`, so the node before it
is at `n / 2 - 1`, and a list of one node becomes empty. The length is
not known in advance: it can be counted first, or found in the same
walk by a second runner moving twice as fast. The approaches differ in
how they find the node before the middle.

## Approaches

| file | mechanism |
|---|---|
| `middle.kara` ★ | two runners over the `shared struct` nodes, the slow one at the head and the fast one two nodes on, the fast moving two for each one of the slow; when the fast one runs out the slow one is just before the middle and steps over it. One walk, in place |
| `middle_count.kara` | one walk to count the nodes, a second to the node at `n / 2 - 1`. Two walks, in place |
| `middle_values.kara` | the values read out into a `Vec`, the one at `n / 2` taken out with `remove`, and a new list built from the back. O(n) space |
| `middle_rec.kara` | recursively: a `length` by `match` and a `cut(list, at)` that gives back the rest at 0 and otherwise keeps the node with the cut made further on, its `let node = list?;` ending at the list's end. O(n) deep |
| `middle_nodes.kara` | an `impl Iterator` whose items are the list's nodes, `collect`ed into a `Vec[ListNode]` of handles, and the node before the middle pointed past it by index |
| `middle_solution.kara` | LeetCode's Rust template (`Option<Box<ListNode>>` with `i32` values, counted through `&head`, then `head.as_mut().unwrap()` down to the node before the middle and `take()` of its next), carried by `karac fix` in four rounds to one refusal; see Verification |
| `differential.kara` | the five arms that check against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and four
more, each list and what is left; then the count and a checksum of what
is left of 2000 random lists of 1 to 200 values from 1 to 100000; then
the constraints' largest, the values 1 to 100000 and 1 to 99999, and
the two values either side of the gap. `middle.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms that check and the
statement read literally: the list's values with the one at index
`n / 2` left out. It checks 300 random lists of 1 to 12 values from 1
to 20; then 20 of one or two values, and 20 of 50 to 100; each with two
more values to put round it. All 340 are drawn before any arm answers.
Each arm is given a freshly built list for every question, since the
arms change the list they are given.

| | property |
|---|---|
| P1 | the values left are the statement read literally |
| P2 | one value fewer is left |
| P3 | a value put before the list and one after it are both kept, round the same values left |
| P4 | the list reversed: at an odd length the values left come out reversed; at an even one, reversed back, they are the list without the value just before the middle |
| P5 | deleting twice leaves the list without its two values from index `(n - 1) / 2`, for two values or more |
| P6 | each arm agrees with at least two of the other four |

The differential prints `340 lists: checksum 102241609, 10200 checks
over 5 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
lists. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty edits to the differential, six to each of its arms, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
four to each of the ★ and nodes arms and three to each of the others.
Each kept one is killed, fails the same way under both backends and not
by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the fast runner one node nearer | P1 142, P3 32, P4 150, P5 122, P6 142 |
| M2 | ★: the slow runner never moving | P1 246, P3 294, P4 250, P5 220, P6 246 |
| M3 | ★: the fast runner from the fourth node | P1 119, P3 30, P4 119, P5 124, P6 119 |
| M4 | ★: the list returned from its second node | P1 305, P2 254, P3 327, P4 306, P5 275, P6 305 |
| M5 | count: two nodes stepped over | P1 276, P2 276, P3 64, P4 271, P5 276, P6 276 |
| M6 | count: a list of two left whole | P1 30, P2 30, P3 30, P4 30, P5 52, P6 30 |
| M7 | count: the head dropped | P1 306, P2 306, P3 325, P4 305, P5 276, P6 306 |
| M8 | values: the new list built backwards | P1 275, P3 316, P4 126, P5 145, P6 275 |
| M9 | values: the first value read twice | P1 340, P2 340, P3 324, P4 305, P5 306, P6 340 |
| M10 | values: the values sorted first | P1 284, P3 324, P4 293, P5 268, P6 284 |
| M11 | rec: the rest dropped with the cut | P1 276, P2 276, P3 340, P4 275, P5 276, P6 276 |
| M12 | rec: two places counted for each node | P1 298, P2 154, P3 340, P4 220, P5 304, P6 298 |
| M13 | rec: the cut at a third | P1 274, P3 111, P4 279, P5 240, P6 274 |
| M14 | nodes: the iterator from the second node | P1 306, P2 306, P3 325, P4 284, P5 276, P6 306 |
| M15 | nodes: a single node kept | P1 34, P2 34, P3 34, P5 30, P6 34 |
| M16 | nodes: the node before the middle pointed at the last | P1 255, P2 255, P3 306, P4 253, P5 277, P6 255 |
| M17 | nodes: the node before the middle counted from the end | P1 150, P2 150, P3 34, P5 276, P6 150 |

P1, P3, P5 and P6 kill all seventeen, P4 fifteen and P2 eleven. P2, the
length, misses only the edits that still take out exactly one node, the
wrong one (M1, M2, M3, M8, M10, M13). P4 misses the two that differ from
the truth only at one length or one parity: a list of one node kept (M15),
and the node before the middle counted from the end, which is the right
node at every even length and leaves an odd-length list whole, so its
reversal agrees with itself (M17). P3, a value put at each end, sees every
edit, since it moves the middle by one and catches an arm that does not
find the middle from the length.

Of the thirty, thirteen were not kept, and none survives. Six fail as a
kept one: two nodes stepped over, in the ★ and nodes arms, as M5; a
single node kept, in the ★ and values arms, as M15; the nodes arm's head
dropped as M7; the count arm's walk to `(n - 1) / 2` and its count halved
rounded up as M1. Four fail the same way as another not kept, in pairs,
and were left out together: the values arm's value at `(n - 1) / 2` and
the rec arm's length one short (P1 149, P4 149, P5 145); the rec arm's
cut never made and cut one further (P1 322, P2 64, P3 64, P4 299, P5
294). Two crash and are not kept: the count arm's count from 1 unwraps
past the last node, and the values arm's last value lost too empties a
list of two, whose second deletion then removes from an empty `Vec`. A
deletion from an empty list is outside the constraints, which is why the
differential's P5 asks only of lists of two or more.

## Verification

Every arm that checks prints the same output as `middle.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for each of
them and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 3.9 s to 5.5 s, and the
differential 1.5 s (timed while other work shared the machine).

The nodes arm met a compiler gap. `karac check` took it, but every run
refused it: "ordering operators on the shared type 'ListNode' need a
hand-written comparator", at a line past the end of the file. `Iterator`'s
default methods are copied into every `impl Iterator`, and `min` and
`max` among them, whose bodies compare items under `where Self.Item:
Ord`, were type-checked for an `Item` with no order: a struct, a `Map`, an
`Option` of a struct. `karac check` keeps only the program's own errors
and dropped them, so only the run saw them. A copy whose bound the impl
does not meet is now left unchecked, and calling `max` on such an
iterator is still refused at the call. Fixed in kara FIXSHA, test
`tests/kata_2095_iterator_unordered_items.rs`.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in four rounds of 19, 5, 1 and 1 edits: Rust's spellings
(`Option<Box<ListNode>>` to brackets, `&` to `ref`, `Solution::` to `.`,
`struct Solution;` to `struct Solution {}`); then `Box[ListNode]` to
`ListNode`; then `own` on the method's parameter and on the adapter's,
which move the list. That leaves one refusal, the cursor walk down to the
node before the middle: `let mut cur = head.as_mut().unwrap(); for _ in
0..n / 2 - 1 { cur = cur.next.as_mut().unwrap(); }`. `Option` has no
`as_mut`, and a `mut ref` cursor rebound to a part of its own referent
has no other spelling, the gap kata 2046 found and B-2026-11-09-45
tracks. The arm stays as the fix left it and is not in the differential.
Its harness converts the template's `i32` values at `build` and
`values_of`.

## Benchmarks

The bench builds 20000 lists of 1000 nodes in all five languages, each
afresh, deletes its middle 50 times with the ★ arm's two runners, and
folds what is left into a checksum: 20 million nodes built, a million
deletions each walking about 500 steps, and every node freed. The nodes
are Kāra's `shared struct`, Rust's `Rc<RefCell<ListNode>>`, C's
`malloc`'d structs, Go's `*ListNode` and Python objects. Every
implementation prints `20000 rounds: 19000000 nodes left, checksum
51829925`.

BENCHTAB
