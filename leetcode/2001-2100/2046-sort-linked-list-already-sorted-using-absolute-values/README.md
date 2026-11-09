# 2046. Sort Linked List Already Sorted Using Absolute Values

Given the `head` of a singly linked list that is sorted in non-decreasing
order by the absolute values of its nodes, return the list sorted in
non-decreasing order by the actual values of its nodes.

```
head = [0,2,-5,5,10,-10]  ->  [-10,-5,0,2,5,10]
head = [0,1,2]            ->  [0,1,2]
head = [1]                ->  [1]
```

**Constraints:** the number of nodes is in `[1, 10^5]`; `-5000 <=
Node.val <= 5000`; the list is sorted in non-decreasing order by absolute
value. **Follow up:** can you think of an O(n) solution?

Sorted by absolute value, the non-negative values already rise, and the
negative ones fall: each negative is smaller than every value before it.
So the negatives, taken in reverse, followed by the rest in order, are the
answer, and one walk can build it.

## Approaches

| file | mechanism |
|---|---|
| `sort.kara` ★ | one walk with `while let Some(node) = cur`: each negative after the head is unlinked behind `prev` and pushed on the front, which reverses the negatives into rising order ahead of the rest. In place, O(n) |
| `sort_split.kara` | the negatives prepended to one list, the rest appended behind a dummy node's tail, the first negative seen kept to join the two. O(n) |
| `sort_values.kara` | the values collected into a `Vec[i64]`, sorted, and written back node by node, which needs `mut val`. O(n log n) |
| `sort_nodes.kara` | the nodes collected into a `Vec[ListNode]`, the order built as `nodes.iter().rev().filter(..)` of the negatives extended by the rest, and every `next` relinked by index. O(n) |
| `sort_merge.kara` | the negatives reversed onto one list and the rest kept in order, then the two merged as two sorted lists with `match (x, y)`. O(n) |
| `sort_solution.kara` | LeetCode's Rust template (`Option<Box<ListNode>>`, `i32` values, the negatives and the rest pushed onto two stacks, the rest reversed, and a `&mut` cursor walked to the negatives' tail to append it), carried by `karac fix` in three rounds: blocked by B-2026-11-09-45 |
| `differential.kara` | the five arms that check against the statement read literally, six properties |

The ★, split, merge and nodes arms relink the nodes they are given; the
values arm keeps every node where it is and moves the values. The nodes are
a `shared struct`, the reference-counted handle a linked list needs.

Every arm that checks prints the same 10 lines: LeetCode's three examples
and five more, each list and its answer; then the count of negatives and a
checksum over the answers for 2000 lists of 1 to 20 values, from `-1..1` up
to `-30..30`, and for 4 lists of 100000 values, the most the constraints
allow: values up to 5000, 100 and 1, and up to 5000 with every one
negative. `sort.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms that check and the
statement read literally: the values taken out one at a time, the smallest
left each time. It checks 1500 lists of 1 to 12 values, from `-1..1` up to
`-20..20`, sorted by absolute value, each with a value of larger absolute
value to append. Every random choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the smallest value taken out one at a time |
| P2 | every value negated gives the answer negated and reversed |
| P3 | a value of larger absolute value appended lands first if negative, last if not |
| P4 | the head dropped drops one copy of its value from the answer |
| P5 | every value doubled doubles the answer |
| P6 | each arm agrees with at least two of the other four |

The differential prints `1500 lists: checksum 847606909, 45000 checks over
5 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, six to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept, four to
each of the ★ and nodes arms and three to each of the others. Each kept one
is killed, fails the same way under both backends and not by a crash, and
no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the second node never looked at | P1 909, P2 1316, P3 130, P4 836, P6 909 |
| M2 | ★: the old head returned (`Some(first)`) | P1 1264, P2 1381, P3 779, P4 629, P6 1264 |
| M3 | ★: the positives moved instead (`> 0`) | P1 1367, P3 1500, P6 1367 |
| M4 | ★: `prev` never advanced past a kept node | P1 1022, P2 1152, P3 348, P4 635, P6 1022 |
| M5 | split: the last negative taken as the latest | P1 1085, P2 1301, P3 697, P4 20, P6 1085 |
| M6 | split: the rest never joined behind the negatives | P1 1250, P2 1279, P3 740, P4 35, P6 1250 |
| M7 | split: a list with no negative answered empty | P1 145, P2 261, P3 145, P4 35, P6 145 |
| M8 | values: the values collected without sign | P1 1355, P2 1486, P3 779, P4 508, P6 1355 |
| M9 | values: each value written back negated | P1 1486, P3 1500, P4 1028, P6 1486 |
| M10 | values: the smallest value skipped | P1 1367, P2 1367, P3 1500, P4 94, P6 1367 |
| M11 | nodes: the negatives kept in list order (`rev` dropped) | P1 975, P2 1199, P3 697, P6 975 |
| M12 | nodes: zeros dropped (`> 0`) | P1 472, P6 472 |
| M13 | nodes: the last node returned (`last`) | P1 1385, P2 1367, P3 1500, P4 150, P6 1385 |
| M14 | nodes: a -1 in neither group (`< -1`) | P1 479, P2 729, P5 479, P6 479 |
| M15 | merge: the merge taking the larger first | P1 1250, P2 458, P3 1385, P6 1250 |
| M16 | merge: the negatives left over dropped | P1 105, P2 207, P3 105, P4 74, P6 105 |
| M17 | merge: the first non-negative dropped | P1 1395, P2 1028, P3 53, P4 637, P6 1395 |

P1 and P6 kill all seventeen, P3 fifteen, P2 fourteen, P4 twelve and P5
one. P2 and P3 see nearly every edit: negating every value turns each
negative into a positive and each positive into a negative, so an edit that
mishandles one sign mishandles the other list, and a value larger than any
other lands at an end an honest answer leaves free. P4 compares the answer
for the list without its head with this answer less one copy of the head's
value, so it passes the edits that misplace values the same way with the
head or without it: the positives moved instead (M3), the negatives kept in
list order (M11), zeros dropped (M12), a `-1` in neither group (M14), and
the larger value taken first (M15). P5 doubles every value, which keeps
every sign and every order, so it sees only an edit that compares a value
with a fixed number: a `-1` in neither group (M14), whose `-1` doubled is a
`-2` and is kept again.

Of the first thirty, two were not kept. Zeros moved to the front too (★)
and zeros counted negative (split) both survived: in a list sorted by
absolute value every zero comes before any negative, so moving a zero to
the front, or reversing the zeros among the negatives, puts each where it
already was. The second node never looked at and the negatives never
chained replaced them.

The rest fail as a kept one does, or are left out because their arm keeps
three or four. The front never moved to a moved node (★) fails as M2, and
the values sorted falling as M3. The values kept in absolute order and the
write-back started past the end both leave the values as they were and fail
alike; a `-1` left where it is (★) and a `-1` sent with the rest (merge)
fail alike too. The last negative never recorded, the tail never moved and
the negatives never chained (split), the rest reversed too and the order
never relinked (nodes), and the rest left over dropped and the dummy merged
in (merge) each fail on checks of their own.

## Verification

Every arm that checks prints the same output as `sort.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error. `karac
run` and a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 5.2 s (★) to 7.4 s (nodes) and
the differential 4.0 s, on kara 531a0f19a1.

The values arm was written with the struct the other arms use, `val: i64`
beside `mut next`, and its `node.val = v` was refused with "shared struct
field 'ListNode.val' is not declared mut" and no fix. `karac check` now
says "declare it `mut val` in `ListNode`", and `karac fix` writes the `mut`
at the field (kara 1dc1f0fa05). The other four checked as written.

The Rust arm was written as LeetCode's Rust template. Three of its refusals
had no fix, and now have one (kara 531a0f19a1): `Option<Box<ListNode>>`
became `Option[Box[ListNode]]` and stopped at "undefined type 'Box'", where
`Box.new(n)` already fixed to `n`, and now fixes to `Option[ListNode]`; the
template moves the list out of its parameter (`let mut cur = head; ..
cur = node.next.take()`), which in Kāra borrows, and the fix was a
`.clone()` of each node moved into `Some(node)`, a copy of the whole rest
of the list, where it is now the parameter's `own`, as Rust's by-value
parameter means; and `for v in [10, -10, 5, -5, 2, 0] { ListNode::new(v) }`
narrowed an `i64` to the `i32` field, and now fixes as `10i32`, which types
the array. `karac fix` carries it in three rounds (31 edits, eight, then
two: `Box` dropped, `::` to `.`, `Vec<..>` to `Vec[..]`, `while let
Some(mut node) = cur` to a `let mut node = node;` in the body, `&mut neg`
to `mut ref neg`, `struct Solution;` to `struct Solution {}`, `own` on
`head`, and the suffix) to one refusal: the cursor walk `while
tail.is_some() { tail = mut ref tail.as_mut().unwrap().next; }`. `Option`
has no `as_mut`, and the walk has no other spelling: `while let Some(n) =
tail { tail = mut ref n.next; }` is refused by both borrow checks, since
the rebinding reads as a use of `tail` while it still borrows from itself.
B-2026-11-09-45 tracks it, and the arm is not in the differential. Its harness
converts the template's `i32` values at `build` and `values_of`.

With the walk written as a recursive append, the arm prints the expected
output under `karac __mir-llvm-run` in 1.8 s, but `karac __mir-run` runs
past 300 s on the first 100000-node list: the interpreter builds a list of
plain (not `shared`) nodes in quadratic time, B-2026-11-09-46.

## Benchmarks

The bench builds a fresh list of 1000 nodes in all five languages, sorted
by absolute value with signs set by the round, sorts it in place with the ★
arm and folds it into a checksum, for 20000 rounds: 20 million nodes built,
walked, relinked and freed. The nodes are Kāra's `shared struct`, Rust's
`Rc<RefCell<ListNode>>`, C's `malloc`'d structs and Go's `*ListNode`. Every
implementation prints `20000 rounds: 6653334 negatives, checksum
34732757`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `531a0f19a1` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.295 to 0.412 s | 0.311 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.357 to 0.405 s | 0.379 s |
| Kāra (`karac build`) | 0.349 to 0.486 s | 0.408 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.477 to 0.636 s | 0.484 s |
| Rust (`rustc -O`) | 0.472 to 0.657 s | 0.517 s |
| Go | 0.670 to 0.811 s | 0.751 s |
| Python | 7.0 s |  |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.401 s) is not above its real time (0.408 s).

The sequential Kāra program is 0.78x Rust under overflow checks and 1.22x
C.
