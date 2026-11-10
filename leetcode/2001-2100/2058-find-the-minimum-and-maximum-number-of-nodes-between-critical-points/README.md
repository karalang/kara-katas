# 2058. Find the Minimum and Maximum Number of Nodes Between Critical Points

A critical point in a linked list is either a local maximum or a local
minimum. A node is a local maximum if its value is strictly greater than
the values of the nodes before and after it, and a local minimum if its
value is strictly smaller than both. A node can only be a critical point
if there is a node both before and after it. Given the `head` of a linked
list, return `[minDistance, maxDistance]`, the least and the greatest
distance between any two distinct critical points, counted in places
along the list. If there are fewer than two critical points, return
`[-1, -1]`.

```
head = [3, 1]                         ->  [-1, -1]
head = [5, 3, 1, 2, 5, 1, 2]          ->  [1, 3]
head = [1, 3, 2, 2, 3, 2, 2, 2, 7]    ->  [3, 3]
```

**Constraints:** the number of nodes is in `[2, 10^5]`;
`1 <= Node.val <= 10^5`.

The greatest distance is always the last critical point less the first,
and the least is always between two that come one after the other, so a
single walk that remembers the first, the last and the value before each
node is enough. The approaches differ in whether they copy the values out
of the list and how they read three neighbours at once.

## Approaches

| file | mechanism |
|---|---|
| `critical.kara` ★ | one walk with `while let Some(node) = cur`, the value before each node kept, and `if let Some(after) = node.next` for the one after; the first and last critical place and the least gap between neighbouring ones carried along. O(n), O(1) space |
| `critical_brute.kara` | the statement read directly: the values copied into a `Vec`, every critical place listed, and the distance taken between every pair of them. O(n + k²) for k critical places |
| `critical_windows.kara` | the values copied out and read through `windows(3)` with `enumerate` and `filter_map` for the critical places, then `windows(2)` over those for the gaps and `min` for the least |
| `critical_zip.kara` | the values copied out and three iterators over them `zip`ped, each a place behind the next, so each item is a node and its two neighbours; a `fold` carries the first and last place and the least gap |
| `critical_nodes.kara` | three node handles walked down the list together, no value copied out, each critical place pushed to a `Vec` and the least gap found by a second pass over it |
| `critical_solution.kara` | LeetCode's Rust template (`Option<Box<ListNode>>`, `i32` values, `head.as_ref().unwrap().val` for the first value, a `while let` walk with `if let Some(next) = &node.next`, `i32::MAX` for no gap yet, and `vec![..]` answers), carried by `karac fix` in four rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

The five Kāra arms keep the nodes in a `shared struct`, the
reference-counted handle a linked list needs, so a walk copies handles,
not nodes. The Rust arm keeps LeetCode's plain recursive struct.

Every arm prints the same 10 lines: LeetCode's three examples and five
more, each list and its answer; then how many have two critical points,
the sum of the answers and a checksum for 2000 random lists of 2 to 40
values from 1 to between 2 and 10, so that neighbours are often equal;
then the same for 4 lists of 2000 values, from 1 to 100000, 3, 2 and 1.
The brute-force arm compares every pair, so the longer lists are 2000
values, not the constraints' 100000; the bench takes the ★ arm to the
limit. `critical.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every place with a place on each side whose value is above
both or below both, the distance between every two distinct ones, sorted,
and the first and last of those. It checks 1000 random lists, drawn as
the harness draws its short ones, before any arm answers. The Rust arm
builds its own list from the values.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is [-1, -1], or a least distance of at least 1 that is at most the greatest, itself at most the list's length less three |
| P3 | the list reversed has the same answer |
| P4 | every value v made 11 - v, which swaps peaks and troughs, has the same answer |
| P5 | the list with a copy of its first value put in front has the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `1000 lists: checksum 629305983, 36000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty-two edits to the differential, five to six to each of its arms,
each run under `karac __mir-run` and `karac __mir-llvm-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a peak only, never a trough | P1 873, P4 702, P6 873 |
| M2 | ★: a node equal to one neighbour critical | P1 492, P3 499, P5 771, P6 492 |
| M3 | ★: the largest gap the last place itself | P1 880, P2 457, P3 595, P5 880, P6 880 |
| M4 | brute: each pair with itself | P1 937, P2 937, P6 937 |
| M5 | brute: only neighbouring pairs | P1 817, P6 817 |
| M6 | brute: the second place left out | P1 449, P3 576, P5 449, P6 449 |
| M7 | windows: the greatest gap as the least | P1 778, P6 778 |
| M8 | windows: the largest gap the second place less the first | P1 817, P3 514, P6 817 |
| M9 | windows: a peak against its left neighbour only | P1 465, P3 587, P4 625, P6 465 |
| M10 | zip: the neighbours zipped one place apart | P1 880, P6 880 |
| M11 | zip: the last place not moved on | P1 790, P3 531, P6 790 |
| M12 | zip: a plateau's edge critical | P1 483, P3 499, P6 483 |
| M13 | nodes: the first gap kept | P1 356, P3 514, P6 356 |
| M14 | nodes: a trough against its left neighbour only | P1 446, P3 577, P4 625, P6 446 |
| M15 | nodes: the walk stepping two nodes | P1 864, P3 340, P5 714, P6 864 |
| M16 | solution: the first place counted twice | P1 91, P2 57, P3 76, P5 91, P6 91 |
| M17 | solution: the adapter adding one to each value but the last | P1 137, P3 260, P4 270, P6 137 |

P1 and P6 kill all seventeen, P3 twelve, P5 five, P4 four and P2 three.
Reversing the list (P3) keeps peaks peaks and every distance the same, so
it passes the edits that are wrong the same way from either end: a peak
alone (M1), a pair with itself (M4), neighbouring pairs only (M5), the
greatest gap as the least (M7), and neighbours one place apart (M10).
P4 turns peaks into troughs, so it catches only the edits that treat
the two differently (M1, M9, M14) and the adapter's shifted values (M17).
P5 puts a copy of the first value in front, which moves every place one
on and adds no critical point, so it catches the edits that count places
from the head rather than from each other (M3, M6, M15, M16) and the one
that lets a node equal to a neighbour count (M2). P2 sees only answers
out of shape: a least gap of 0 (M4), and a greatest that is a place, not
a distance (M3, M16).

Of the thirty-two, fifteen were not kept. Five are equivalent: four shift
every place by the same amount, which no distance sees (the ★ arm's
places counted from 2, the windows arm's window's first place, the zip
arm's place one short, and the Rust arm's `idx` from 0), and the brute
arm's last neighbour clamped to the end is never reached. One crashes:
the windows arm with one critical place enough takes `min` of no gaps
and unwraps `None`. Three fail as M13, each keeping a gap that is not
between neighbours: the ★ arm's gap from the first place, the zip arm's
first gap kept, and the nodes arm's gaps from the first place. The brute
arm's trough against the wrong neighbour fails as M14. The ★ and Rust
arms' value before never moved on fail alike, as do the nodes arm's walk
stopped a node early and the Rust adapter's last value dropped. The Rust
arm's trough only fails on checks of its own, and was left out because
that arm keeps two.

## Verification

Every arm prints the same output as `critical.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them.
Under `karac __mir-run` the Kāra arms take 0.5 s (nodes) to 1.1 s
(brute), the Rust arm 11.3 s, most of it the copy of each list described
below, and the differential 6.0 s.

The five Kāra arms met no compiler gap and checked as written.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in four rounds of 19, 2, 5 and 1 edits to a clean check: `struct
Solution;` to `struct Solution {}`, Rust's spellings (`Option<..>` and
`Vec<..>` to brackets, `i32::MAX` to `i32.MAX`, `&&` and `||` to `and` and
`or`, `&node.next` to `ref node.next`, `vec![..]` to a list), `mut` moved
out of the tuple pattern to `let mut (first, last, min_d)`, `Box<ListNode>`
to `ListNode` (Kāra has no box), and `idx`, `first` and `last` declared
`i32`, since a method or an operator does not fix a literal's type.

One fix is worth a look. `head.unwrap()` moves out of `head`, which Rust
owns and Kāra's parameter borrows, and `karac fix` writes
`head.clone().unwrap()`: correct, but a copy of the whole list, where
`head: own Option[ListNode]` gives the list away for nothing. The fix is
`.clone()` on purpose: making the parameter `own` would change what every
caller must pass, and the adapter here would then need `own` too, which
no single edit can know. It costs: under the interpreter the Rust arm
takes 11.3 s as fixed, and 2.2 s with `own` written on it and on the
adapter by hand. The arm keeps the fixed form.

## Benchmarks

The bench answers 50 lists of 100000 values, the constraints' limit, from
1 to 2, 3, 10 and 100000 in turn, with the ★ arm in all five languages:
five million nodes built and walked. Building the lists is part of the
work timed, and is most of it. Kāra's nodes are reference-counted `shared
struct`s; Rust's are `Box`es, unlinked in a loop after each answer; C's
are `malloc`ed and freed in a loop; Go's are left to the collector.
Every implementation prints `50 lists: sum 4999696, checksum 3033112`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `093c72b97d`, on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.103 to 0.121 s | 0.108 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.118 to 0.142 s | 0.119 s |
| Kāra (`karac build`) | 0.118 to 0.137 s | 0.121 s |
| Rust (`rustc -O`) | 0.122 to 0.134 s | 0.129 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.125 to 0.155 s | 0.132 s |
| Go | 0.190 to 0.238 s | 0.200 s |
| Python | 3.1 s |  |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.119 s) is not above its real time (0.121 s).

The sequential Kāra program is 0.90x Rust under overflow checks and 1.10x
C. Building and freeing five million nodes is most of the work, and C,
Rust and Kāra are within a quarter of each other; Go, whose collector
frees the lists, takes about twice as long as C.
