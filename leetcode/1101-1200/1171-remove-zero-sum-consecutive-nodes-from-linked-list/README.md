# 1171. Remove Zero Sum Consecutive Nodes from Linked List

Given the `head` of a linked list, we repeatedly delete consecutive
sequences of nodes that sum to `0` until there are no such sequences.

After doing so, return the head of the final linked list. You may return
any such answer.

(Note that in the examples below, all sequences are serializations of
`ListNode` objects.)

```
head = [1,2,-3,3,1]   ->  [3,1]      ([1,2,1] is also accepted)
head = [1,2,3,-3,4]   ->  [1,2,4]
head = [1,2,3,-3,-2]  ->  [1]
```

**Constraints:** the given linked list will contain between `1` and
`1000` nodes; each node in the linked list has `-1000 <= node.val <=
1000`.

The arms are `fn remove_zero_sum_sublists(head: Option[ListNode]) ->
Option[ListNode]`. The Kāra arms take `shared struct ListNode { mut val:
i64, mut next: Option[ListNode] }`, a counted node whose links can be
rewritten in place, as LeetCode's Java and Python lists are. The two Rust
arms keep the `ListNode` LeetCode gives Rust users, a plain struct whose
`next` owns the rest of the list.

## Approaches

A run of nodes sums to 0 exactly when the running sums before it and after
it are equal, so every arm but the scan works on running sums.

| file | mechanism |
|---|---|
| `remove_zero_sum.kara` ★ | prefix sums in two passes: a dummy node in front, the first pass keeps in a `Map[i64, ListNode]` the last node at which each running sum is reached, and the second links each node past everything up to that last node. O(n) |
| `remove_zero_sum_stack.kara` | one pass with a stack: the nodes kept so far on a stack with the running sum after each, and a `Map` from each running sum to its place on the stack; a node that brings the sum back to one already there unlinks everything above that place and pops it. O(n) |
| `remove_zero_sum_scan.kara` | the statement as written: from each node in turn, walk ahead summing until the sum is 0 and unlink that run, then look again from the node now in its place. O(n²) |
| `remove_zero_sum_array.kara` | through a vector: the values copied out with their running sums, the last place of each sum found in a `Map`, the values kept by jumping from each kept place to the last place of its sum, and a new list built from them. O(n) |
| `remove_zero_sum_solution.kara` | a Rust solution as LeetCode's Rust users write it (`Option<Box<ListNode>>`, the values collected by walking `&node.next`, a `HashMap<i32, usize>` from each running sum to its place on a stack of kept values, and the answer rebuilt through a `&mut` tail), carried to Kāra by `karac fix` |
| `remove_zero_sum_fold.kara` | the same Rust solution with the answer rebuilt from the back, `stack.iter().skip(1).rev().fold(None, \|next, &(_, v)\| Some(Box::new(ListNode { val: v, next })))`, carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's three examples; a 0
alone; a list left whole; one that goes entirely; `[1, -1, 1]`, where
either `1` may stay; `[2, 0, 3, -3, 1, -1, 0, 2]`, runs of every length
side by side; then 300 random lists of 1 to 30 values from -3 to 3
(`300 random lists: 1218 kept, checksum 535544413`); and 1000 values,
the constraints' most, from -1000 to 1000, from -5 to 5, and climbing to
500 and back down but for its last step (`up 500 and down 499, then 2:
[1, 2]`). Where the statement allows more than one answer, all six arms
leave the same values on every one of these lists.
`remove_zero_sum.py` mirrors the ★ arm and its output is byte-identical;
with `lit` it reads the statement literally, deleting the leftmost run
that sums to 0 until none is left, and gives the same output. Every arm
gives the same output under `karac run` and `karac build`.

The Mend loop: the ★ and scan arms take no fixes. The stack arm takes
two, `vec![(0, dummy)]` to `[(0, dummy)]` and `place.get(sum)` to
`place.get(sum).cloned()`, since `get` lends the value and the arm
matches on its own copy; the array arm one, `vec![0]` to `[0]`.

The two Rust arms each take one round, 65 edits and 60: the generics to
brackets, `Option<Box<ListNode>>` to `Option[ListNode]` and
`Box::new(..)` to the value, `::` to `.`, `struct Solution {}`,
`HashMap<i32, usize>` to `Map[i32, i64]`, `vec![..]` to `[..]`, the
`&v` and `&(_, v)` patterns to `v` and `(_, v)`, `seen.get(&sum)` to
`seen.get(sum).cloned()`, and the walk's `let mut cur = &head;` and `cur
= &node.next;` to `let mut cur = ref head;` and `cur = ref node.next;`.
One of them is in the harness, written in Kāra over the Rust arms'
`ListNode`: its own walk's `cur = node.next` to `cur = ref node.next`.
Both arms' outputs match on the first run.

Three compiler gaps came up on the way, each fixed in kara
`756fad5000`:

- Over a borrowed list, `let mut cur = head; while let Some(node) = cur
  { cur = node.next; }` was refused by the MIR's move check with no fix
  (kara B-2026-11-16-177). `cur` is a `ref`, since `head` is
  borrowed, so `node.next` cannot move into it; the fix is now `cur =
  ref node.next`.
- A first draft of the harness read the second node with `match head {
  Some(n) => n.next, None => None }` over a borrowed `head`, and `karac
  fix` offered `#[derive(Copy, Clone)]` on `ListNode`, which holds
  itself; `karac check` on that derive then overflowed its stack (kara
  B-2026-11-16-178). A type that holds itself is boxed and never
  `Copy`: the derive is now refused, and the fix offers
  `#[derive(Clone)]` and `.clone()`.
- `stack.iter().skip(1).rev()`, the fold arm's spelling, had no `rev`:
  `skip` and `take` were not `DoubleEndedIterator` (kara
  B-2026-11-16-176). They now are over an iterator that knows its
  length, as in Rust.

The differential takes one round of 2 edits: `vec![c.pair, -c.pair]` to
`[c.pair, -c.pair]`, and `out.push(node.val as i64)` to
`out.push(node.val)` in the fold arm's walk, where `out` is already a
`Vec[i64]`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: no run of the answer sums to 0, and the answer is the list with
runs that each sum to 0 taken out before, between and after its values,
each answer value matched to the earliest place where the list's sum
before it is the answer's sum before it. It checks 600 lists in four
kinds of 150: 1 to 8 values from -2 to 2; 1 to 30 from -5 to 5; 30 to
120 from -50 to 50; and 1 to 40 values that are each 1, 2 or 3 either
way, so that sums come back often and runs overlap. Every random choice
the properties make is drawn before any arm answers. The walk that reads
an arm's answer stops one node past the list's length, so an arm that
links a cycle fails P1 rather than running on.

| | property |
|---|---|
| P1 | the answer is one the statement allows |
| P2 | the answer has nothing left to remove |
| P3 | every value negated negates the answer |
| P4 | every value doubled doubles the answer |
| P5 | a pair `p, -p` in front changes nothing |
| P6 | the list followed by itself reversed and negated leaves nothing |

All 21,600 checks pass on every arm: `600 lists: checksum 202463000, 21600
checks over 6 arms: 0 failures`, in 5 s under `karac __mir-run`, and the
same under `karac __mir-llvm-run` and `karac build`.

## Mutation testing

Eighteen edits to the differential, three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. All eighteen are caught.

| # | mutation | failures by property |
|---|---|---|
| A1 | ★: the second pass's sum not restarted | P1 567 |
| A2 | ★: the second pass started past the dummy | P1 153, P5 600, P6 600 |
| A3 | ★: the original head returned | P1 250, P5 600, P6 600 |
| K1 | stack: popped sums left in the map | a crash: `index out of bounds` |
| K2 | stack: the empty prefix's sum 0 not entered | P1 153, P5 600, P6 600 |
| K3 | stack: the kept node not relinked past the run | P1 531, P5 600, P6 600 |
| C1 | scan: only single zero nodes cut | P1 505, P5 323, P6 550 |
| C2 | scan: each run's first node left out of its sum | P1 520, P2 156, P5 600, P6 591 |
| C3 | scan: only the run's first node cut | P1 469, P2 352, P5 593, P6 595 |
| R1 | array: the running sums kept instead of the values | P1 478, P2 478 |
| R2 | array: a zero-sum prefix not skipped | P1 153, P5 600, P6 600 |
| R3 | array: the list rebuilt backward | P1 432, P2 432 |
| X1 | solution: each sum's place one too low, so one entry too many popped | P1 473, P6 485 |
| X2 | solution: popped sums left in the map | P1 343, P5 9, P6 363 |
| X3 | solution: the dummy's 0 kept in the answer | P1 600, P6 600 |
| F1 | fold: the list rebuilt backward | P1 432, P2 432 |
| F2 | fold: the empty prefix's sum 0 not entered | P1 153, P5 600, P6 600 |
| F3 | fold: each value stored as its own running sum | P1 491, P2 31, P6 471 |

K1 is caught as a crash rather than by a property: a sum left in the map
names a place already popped, and `stack[k]` indexes past the stack's
top. A1 is caught by P1 alone: with the sum carried over from the first
pass, every arm-0 answer is empty, and an empty answer passes every
property but the literal one.

Two first drafts of the ★ and array mutations, keeping the first node or
place of each sum instead of the last, linked a cycle or jumped back, and
ran on without end; the array one had filled 10 GB under `karac
__mir-llvm-run` when it was stopped.
The differential's walk now stops one node past the list's length, and
those two were replaced by the A2 and R1 above, since an arm that loops
inside itself is caught only by a timeout.

## Benchmarks

`bench/` times the ★ arm against the same two passes in C, Rust, Go and
Python. 32 lists of 1000 values, the constraints' most, in four kinds
(within 2, within 5, within 50, and 1 to 3 either way) are built once;
each of 400 rounds gives one value of every list a new value, builds the
list afresh, removes its zero-sum runs and folds what is left into a
checksum. The nodes are Kāra's `shared struct`, Rust's
`Rc<RefCell<ListNode>>`, C's `malloc`'d structs (freed after each list
is read), Go's `*ListNode` and Python objects; the map from running sum
to node is Kāra's `Map`, Rust's `HashMap`, Go's `map`, Python's `dict`,
and in C an open-addressing table of 4096 slots cleared for each call.
Every program prints `400 rounds over 32 lists of 1000 values: 512581
kept, checksum 645694797`.

Timings on a 4-core container (Intel Xeon, 2.3 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac
`737519435c` on LLVM 22. karac builds for the x86-64-v3 baseline, so the
C and overflow-checked Rust programs are also built at
`-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.458 to 0.546 s | 0.482 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.453 to 0.540 s | 0.466 s |
| Rust (`rustc -O`) | 0.505 to 0.653 s | 0.524 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.509 to 0.654 s | 0.525 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.513 to 0.611 s | 0.531 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.161 to 0.214 s | 0.164 s |
| C (`clang -O3`) | 0.161 to 0.270 s | 0.163 s |
| Go | 0.470 to 0.615 s | 0.544 s |
| Python | 2.0 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; user time equals wall time for both Kāra rows, so
both ran on one core. Kāra takes about 0.89x overflow-checked Rust's
time, the equal-safety comparison, and 0.86x Go's. Overflow checks cost
Rust nothing measurable here: the work is allocation, reference counts
and hashing, not arithmetic. C takes about 0.35x Kāra's time: its nodes
carry no count, its table is a flat array probed with one multiply,
where Kāra's `Map` and Rust's `HashMap` hash with SipHash, and every
node Kāra and Rust store in the map or step to is a count raised and
lowered (in Rust also a `RefCell` borrow flag checked). Go's time
includes its collector, whose threads take its user time above its wall
time. Python takes about 4.3x Kāra's time, closer than on most katas,
since its share of the work, the `dict` and the allocation, runs in C.
These causes are read from the programs, not profiled.
