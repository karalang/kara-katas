# 1669. Merge In Between Linked Lists

You are given two linked lists: `list1` and `list2` of sizes `n` and `m`
respectively.

Remove `list1`'s nodes from the `a`th node to the `b`th node, and put
`list2` in their place.

Build the result list and return its head.

```
list1 = [10,1,13,6,9,5], a = 3, b = 4, list2 = [1000000,1000001,1000002]
    ->  [10,1,13,1000000,1000001,1000002,5]
list1 = [0,1,2,3,4,5,6], a = 2, b = 5, list2 = [1000000,1000001,1000002,1000003,1000004]
    ->  [0,1,1000000,1000001,1000002,1000003,1000004,6]
```

**Constraints:** `3 <= list1.length <= 10^4`; `1 <= a <= b < list1.length - 1`;
`1 <= list2.length <= 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `merge.kara` ★ | one cursor stops at node a - 1, the last kept before the cut, and goes on to node b + 1, the first kept after it; another walks to list2's end; then the two splices. O(n + m), in place |
| `merge_count.kara` | one walk over list1 with its index: node a - 1 kept, and at node b the splice, list2 walked to its end there. O(n + m), in place |
| `merge_values.kara` | list1's values before a, list2's, and list1's after b gathered into one `Vec` and built into a new list from the back. O(n + m) time and space |
| `merge_solution.kara` | LeetCode's Rust template (`Option<Box<ListNode>>`, `i32` values): `as_mut().unwrap()` down to the node before the cut, `take()` of the rest, the cut walked over by moving out of each node, list2 hung on and walked to its end. Carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

The ★, count and values arms use a `shared struct ListNode` with an
`i64` value, as #2095 does, so a cursor is a second handle on a node and
a splice is a field write through it. The solution arm keeps LeetCode's
plain `struct ListNode`, which `karac fix` gives `Option[ListNode]` for
`Option<Box<ListNode>>`; its harness converts the values at `build` and
`values_of`.

Every arm prints the same 7 lines: LeetCode's two examples, the smallest
first list with its one inner node replaced, and a cut of all three
inner nodes; then the merged lengths summed and a checksum for 3000
random problems with lists of up to 12 nodes, 300 of up to 1000 and 10
of up to `10^4`. `merge.py` mirrors the ★ arm and its output is
byte-identical.

```
[10,1,13,1000000,1000001,1000002,5]
[0,1,1000000,1000001,1000002,1000003,1000004,6]
[1,9,3]
[1,7,8,5]
3000 problems of up to 12 nodes: 35609 nodes merged, checksum 97285295
300 problems of up to 1000 nodes: 265837 nodes merged, checksum 164022511
10 problems of up to 10000 nodes: 72821 nodes merged, checksum 877433623
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally, on the values: list1's first a, then list2, then list1 after
b. The solution arm's `ListNode` is renamed `BoxNode` there, so both
node types live in one program. It checks 3000 random problems with a
first list of 3 to 12 nodes and a second of 1 to 12. Every case is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the merged values are the statement read literally |
| P2 | the merged list holds n - (b - a + 1) + m nodes |
| P3 | list2's place in the answer, cut out again for list1's cut nodes, gives list1 back |
| P4 | every value one more gives every merged value one more |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 97285295, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement gives the same checksum. (Its problems are
drawn the same way as the arms' first batch, so the checksum is the
same.) On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M4 stops on both before any property
is checked: its index runs past a - 1, so no node before the cut is
kept, and `before.unwrap()` panics on `None`. An edit that hangs list2's
end on list2's own head (a first M4 kept node a, which for a = b is the
node whose `next` was just set to list2) makes a cycle that the
harness's walk follows until memory runs out, so it was dropped.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the cursor stops at node a, not a - 1 | P1 3000, P3 3000, P5 3000 |
| M2 | ★: the walk past the cut stops one short | P1 3000, P2 3000, P3 3000, P5 3000 |
| M3 | ★: list2's end left open | P1 3000, P2 3000, P3 3000, P5 3000 |
| M4 | count: the index stepped by 2 | `called unwrap() on None` |
| M5 | count: list2's end left open | P1 3000, P2 3000, P3 3000, P5 3000 |
| M6 | count: the splice at node b + 1 | P1 3000, P2 3000, P3 3000, P5 3000 |
| M7 | values: node b kept | P1 3000, P2 3000, P3 3000, P5 3000 |
| M8 | values: list2 put first | P1 3000, P3 3000, P5 3000 |
| M9 | solution: the walk past the cut stops one short | P1 3000, P2 3000, P3 3000, P5 3000 |
| M10 | solution: the cursor stops at node a | P1 3000, P3 3000, P5 3000 |

## Benchmarks

The bench draws one list of `10^5` nodes and 10000 cuts of it, each at a
random place with 1 to 8 nodes taken out and a new list of 1 to 8 put
in, all of them first; then it builds the list and makes every cut in
turn by the ★ arm, each new list built just before its merge, in all five
languages: Kāra's `shared struct`, Rust's `Rc<RefCell<ListNode>>`,
pointer nodes in Go and Python, and nodes malloc'd one by one in C, which
frees the cut nodes as the walk steps over them. Every implementation
prints `100000 nodes, 10000 merges: 99817 nodes, checksum 160989718`.
The C build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| Go | 1.039 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 2.281 s |
| Kāra (`karac build`) | 2.294 s |
| C (`clang -O3`) | 3.504 s |
| Rust (`rustc -O -C overflow-checks=on`) | 3.514 s |
| Rust (`rustc -O`) | 3.976 s |
| Python | 10.0 s |

The sequential Kāra build is 43% faster than Rust and 35% faster than
Rust with overflow checks on, the equal-safety comparison
(BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (1.852 s and 1.859 s on one
run).

## Verification

All four arms print the same output as `merge.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★, count and values arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 22 edits: every
`Option<Box<ListNode>>` written `Option[ListNode]`, `struct Solution {}`
added, the two lists taken `own` (the method moves out of them), and in
the harness's `values_of`, which walks a plain struct's list, `cur =
node.next` written `cur = ref node.next`, a borrow rather than a move out
of a borrowed node.

The differential's P4 first compared an arm's answer with
`got.iter().map(|v| v + 1).collect()`; a comparison does not fix what
`collect` builds, and `karac fix` named it:
`Vec[i64].from_iter(got.iter().map(|v| v + 1))`. `arm_name` indexes a
list of string literals for a `Str`, as #1662's differential does
(B-2026-11-19-131).
