# 2471. Minimum Number of Operations to Sort a Binary Tree by Level

You are given the `root` of a binary tree with **unique values**.

In one operation, you can choose any two nodes **at the same level** and
swap their values.

Return *the minimum number of operations needed to make the values at
each level sorted in a **strictly increasing order***.

The **level** of a node is the number of edges along the path between
it and the root node.

```
root = [1,4,3,7,6,8,5,null,null,null,null,9,null,10]  ->  3
root = [1,3,2,7,6,5,4]                                 ->  3
root = [1,2,3,4,5,6]                                   ->  0
```

**Constraints:** the number of nodes is in `[1, 10^5]`;
`1 <= Node.val <= 10^5`; all the values of the tree are **unique**.

The levels are independent, since a swap never crosses one. Within a
level the values are distinct, so each place's value has one place it
belongs at in the sorted level, and those places form a permutation. A
swap can join two cycles of it or split one in two, never more, and the
level is sorted exactly when every cycle is one place, so a level of
width `w` whose permutation has `c` cycles takes `w - c` swaps, and no
fewer.

## Approaches

| file | mechanism |
|---|---|
| `swaps.kara` ★ | by cycles: the levels by a breadth-first walk; in each, a `Map` from each value to its place in the sorted level gives the permutation, and a cycle of `c` places adds `c - 1`. O(n log n) |
| `swaps_greedy.kara` | swapping into place: place by place, while a place holds the wrong value, the value that belongs there is swapped in from wherever it stands, found by a `Map` from each value to its current place; every swap puts one value home for good. O(n log n) |
| `swaps_union.kara` | union-find: the levels by one `VecDeque`, each taken as the queue's size at its start; every place joined with the place its value belongs at, found by a binary search in the sorted level, and the swaps the width less the groups. O(n log n) |
| `swaps_ranks.kara` | ranks without a map: the levels gathered by a depth-first walk that visits left before right; in each, the places sorted by value give the permutation, its cycles counted with a `seen` list. O(n log n) |
| `swaps_iter.kara` | iterators: each level the `flat_map` of the one above over its two children, `filter_map` keeping the present ones; the cycles counted by `filter` over the places that start one. O(n log n) |
| `swaps_solution.kara` | LeetCode's Rust template: `Option<Rc<RefCell<TreeNode>>>` in, `i32` out; the levels by a `VecDeque`, each node read through `borrow()`, and the cycles through a `HashMap<i32, usize>`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples; then four
more, one node, a level of two reversed, a level holding a cycle of
three, and a level split by missing children; then three trees of
`10^5` nodes, the constraints' largest, a path, a complete tree with
random values, its last level 34465 wide, and a random tree; and 3000
random trees of 1 to 40 nodes, as a checksum. A random tree takes the
values 1 to `n` in a random order and hangs each node after the first
below a random earlier one, taking a random side down from it until a
free one is found. `swaps.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 3000 random trees of 1 to
12 nodes against a breadth-first search over each level's orders one
swap apart.

`check` first reports 14 errors on the template, and `karac fix`
carries it in one call, reporting 25 edits. The three `use` lines go;
`Rc<RefCell<TreeNode>>` becomes the `TreeNode` handle, declared a
`shared struct`, and `let node = node.borrow();` goes with it;
`VecDeque::new` and `Vec::with_capacity` take a `.`; `HashMap<i32,
usize>` becomes `Map[i32, i64]`; `vec![false; size]` becomes
`Vec.filled(size, false)`; `sort_unstable` becomes `sort`; the two `!`
become `not` and the `||` `or`; the `&` in the closure's pattern and on
each map index goes; and `struct Solution;` is given its braces. The
`i32` values, `node.left.clone()`, `pop_front().unwrap()` and the
`enumerate().map(..).collect()` into the map stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each level's values read off left to right, and the fewest
swaps that sort it found by a breadth-first search over the orders one
swap apart, from the level as it stands to the level sorted. No cycle
stands in for the count. It checks 300 random trees of 1 to 9 nodes,
then 60 of up to 12, their values distinct, from 1 to 50000. All 360 are
drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the literal reading's |
| P2 | every level sorted, then reversed: half of each level's width, rounded down, summed |
| P3 | the tree mirrored and every value `v` written `100001 - v`: the same count |
| P4 | two copies under a new root, the second's values raised by 50000: twice the count |
| P5 | every level sorted, then the first two values of the widest level swapped: 1, or 0 if no level holds two |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a sorted level reversed is the swaps of its first and
last places, its second and second last, and so on, cycles of two and,
in an odd width, one place left alone. P3 holds because mirroring
reverses every level and `100001 - v` reverses the order of the values,
so each level's permutation is the same one. P4 holds because each new
level is a level of the first copy followed by the same level of the
second, all its values above the first's, so the sorted level keeps the
two halves apart. P5 holds because the swapped level is one cycle of
two away from sorted.

P2 first wrote every value `v` as `2v + 1`, which keeps the order, and
it killed no mutation: an arm that reads the order alone answers the
same. The level sorted and then reversed replaced it.

The differential prints `360 cases: checksum 469664652, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and runs the same search over tuples. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a cycle of two not counted | P1 166, P2 233, P5 233, P6 166 |
| M4 | ★: sorted descending | P1 188, P2 233, P4 360, P5 166, P6 188 |
| M6 | ★: the last level skipped | P1 62, P2 101, P5 38, P6 62 |
| M7 | greedy: the place map never updated | P1 7, P3 19, P6 7 |
| M8 | greedy: the walk stopped at the middle | P1 2, P3 2, P4 173, P6 2 |
| M9 | greedy: the walk stopped at two swaps | P1 26, P2 77, P4 80, P6 26 |
| M12 | union: levels of two left out | P1 160, P2 233, P4 160, P5 169, P6 160 |
| M13 | union: a place joined only to a home on its right | P1 14, P3 18, P6 14 |
| M15 | union: one swap a level too many | P1 360, P2 360, P4 332, P5 360, P6 360 |
| M18 | ranks: every cycle its length | P1 360, P2 360, P4 360, P5 360, P6 360 |
| M19 | ranks: every cycle one swap | P1 19, P6 19 |
| M21 | ranks: children kept on their parent's level | P1 223, P2 204, P3 251, P4 289, P5 218, P6 223 |
| M22 | iter: one swap a level at most | P1 20, P2 7, P4 173, P6 20 |
| M23 | iter: half the misplaced values, rounded up | P1 2, P4 19, P6 2 |
| M25 | iter: no cycle started at the first place | P1 360, P2 360, P3 21, P4 318, P5 360, P6 360 |
| M27 | solution: levels of even width left out | P1 163, P2 233, P4 48, P5 175, P6 163 |
| M30 | solution: the visited mark never set | P1 173, P2 233, P4 173, P5 233, P6 173 |

P1 and P6 kill all seventeen, P2 and P4 twelve each, P5 ten, and P3
five.

Fourteen are not kept. Six fail exactly as a kept one: the greedy and
ranks arms' sorted descending, the iter arm's children swapped in order
and the template's children taken right first (M11, M20, M26, M31) as
the ★ arm's sorted descending (M4), since a level read backwards against
its sorted order is the same mistake as a level sorted backwards; the
union arm's find that never climbs (M16) as the greedy arm's place map
never updated (M7); and the iter arm's one swap a level too few (M24) as
the union arm's one swap a level too many (M15), each wrong on every
level that holds a cycle. Five fail alike, apart from every kept one:
dropping one side's children (M2, M14, M17, M28) leaves every level one
node, so each answers 0, and the ★ arm's cycle walk one step short (M5)
fails on the same checks. Three survive and are equivalent: the ★ arm's
root level skipped (M3), since a level of one node needs no swap; the
greedy arm's last place never checked (M10), since once every earlier
place holds its value the last holds the one left; and the template's
last place never walked (M29), since the last place is home already or
in a cycle walked from an earlier place. Every other edit is killed.

Twelve edits were replaced before this table was drawn. Ten of a first
round failed exactly as the edits that answer 0 or as sorted descending,
and two of their replacements, the greedy arm's first place never fixed
and the union arm's join made only toward a later group, survived every
check.

## Verification

Every arm prints the same output as `swaps.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 6.2 to 8.7 s, the iter arm 22.0 s, and the differential 2.5 s; under `karac __mir-llvm-asan` the arms take 1.5 to 3.5 s and the differential 1.0 s, and under `karac run` the differential takes 0.8 s.

## Benchmarks

The bench builds 20 random trees of `10^4` nodes once from its own
generator, as the arms build theirs, then makes 110 passes; each
answers every tree, folding the count plus the pass into the checksum,
then swaps the values of two of its nodes chosen by the checksum, so no
answer carries over. The bench uses the ★ arm in all five languages,
the map from each value to its sorted place a hash map in each: C,
which has none, keeps it in an open-addressing table of `2^15` slots,
emptied after every level. Every implementation prints `110 passes over
20 trees of 10^4: checksum 98437537`.

BENCHTAB
