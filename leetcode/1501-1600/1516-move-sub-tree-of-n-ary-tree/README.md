# 1516. Move Sub-Tree of N-Ary Tree

Given the `root` of an N-ary tree of unique values, and two nodes of the
tree `p` and `q`, move the subtree of the node `p` to become a direct
child of node `q`. If `p` is already a direct child of `q`, do not change
anything. Node `p` must be the last child in the children list of node
`q`. Return the root of the tree after adjusting it.

There are three cases for `p` and `q`:

1. `q` is in the subtree of `p`.
2. `p` is in the subtree of `q`.
3. Neither is in the subtree of the other.

In cases 2 and 3 you move `p` (with its subtree) to be a child of `q`. In
case 1 the tree may be disconnected, so you also need to reconnect it:
first move `q` (with its subtree) out of its parent and put it where `p`
was, then make `p` the last child of `q`.

LeetCode's example tree is 1 over 2 and 3, 2 over 4 and 5, 3 over 6, and
4 over 7 and 8, written here as `1(2(4(7 8) 5) 3(6))`:

```
p = 4, q = 1  ->  1(2(5) 3(6) 4(7 8))
p = 7, q = 4  ->  1(2(4(7 8) 5) 3(6))       7 is already a child of 4
p = 3, q = 8  ->  1(2(4(7 8(3(6))) 5))
```

**Constraints:** the tree has between 2 and 1000 nodes; values are unique;
`p != null`, `q != null`, `p != q`.

## Approaches

| file | mechanism |
|---|---|
| `move.kara` ★ | find p's and q's parents by a walk from the root, ask whether q is in p's subtree by a walk from p, and splice: `retain` drops a child, `position` finds p's slot. O(n) |
| `move_map.kara` | one breadth-first walk (`VecDeque`) records every node's parent in a `Map[i64, Node]`; q is in p's subtree when the walk up from q meets p. O(n) |
| `move_rebuild.kara` | copy the tree into lists of child values by value (`Map[i64, Vec[i64]]`), move the values there, and grow fresh nodes from the lists; the input tree is left as it was. O(n) |
| `move_iter.kara` | the ★ arm's walks with iterator adapters: `find_map` for the parent, `any` for the subtree, `position` and `remove` for the slot |
| `differential.kara` | the four arms against the statement read literally, six properties |

LeetCode offers no Rust template for this problem (its N-ary tree problems
have none), so there is no Rust-template arm.

The node is `shared struct Node { val: i64, mut children: Vec[Node] }`:
the tree is changed in place through handles, as LeetCode's `Node` is.

Every arm prints the same 8 lines: LeetCode's three examples, `2` moved
under its own descendant `7`, the root moved under `8`, and `5` moved under
its own parent `2`, each printed as above, then a checksum of the printed
answers' bytes for 3000 random trees of 2 to 12 nodes and 300 of 2 to 300,
with `p` and `q` drawn at random. `move.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally on another representation: each node is a parent and a rank
among its siblings. "Move p to be the last child of q" sets p's parent to
q and its rank above every other; "first move q out and put it where p
was" gives q p's parent and p's rank; nothing happens when p's parent is
already q. The answer is printed from those links. It checks 3000 trees
of 2 to 12 nodes, every random choice drawn before any arm answers, and
each arm gets a freshly built tree, since every arm but one changes the
tree it is given.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer holds every node once |
| P3 | p is a child of q in the answer |
| P4 | every value mapped to `3 v + 7` maps the answer the same way |
| P5 | when q is outside p's subtree, p's subtree keeps its shape |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 722281419, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Fourteen edits to the differential, three to five to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run`. Thirteen are killed,
each the same way under both backends: seven by a property, four by an
`unwrap()` on `None`, and two by a stack overflow, because the edit made
a cycle and the printer recursed around it. One survives and is
equivalent.

| # | mutation | killed by |
|---|---|---|
| M1 | ★: no early return when p is already q's child | P1 148, P4 148, P6 148 |
| M2 | ★: the subtree test asked the wrong way round (p in q's) | `unwrap()` on `None` |
| M3 | ★: the old root kept when p was the root | P1, P2, P3, P4, P6 600 each |
| M4 | ★: p made q's first child, not its last | P1 226, P4 226, P6 226 |
| M5 | ★: q's old parent drops p rather than q | stack overflow (a cycle) |
| M6 | map: the walk up from q looks for q, not p | `unwrap()` on `None` |
| M7 | map: q appended to p's old parent instead of taking p's slot | P1, P2, P4, P6 275 each |
| M8 | map: the walk up from q stops after one step | `unwrap()` on `None` |
| M9 | rebuild: the root becomes p, not q | P1, P2, P3, P4, P6 600 each |
| M10 | rebuild: p's old parent also drops q | P1 to P6 448 each |
| M11 | rebuild: q inserted before p's slot, p's entry left | P1, P2, P4, P6 275 each |
| M12 | iter: `contains` with `and` for `or` | `unwrap()` on `None` |
| M13 | iter: q's parent drops its first child, not q | stack overflow (a cycle) |

P1 and P6 kill all seven that a property kills, P4 all seven, P2 five,
P3 three, P5 one (M10). The survivor is the iterator arm skipping the
early return when p is q's only child: it then takes p out of q and puts
it back, the same tree.

## Benchmarks

The bench builds a random tree of 100000 nodes once (node `i` under a
random earlier node) and then makes 1000 moves of random `p` under random
`q` by the ★ arm, in all five languages; Rust holds the tree in
`Rc<RefCell<Node>>` as LeetCode's Rust trees do, C and Go in plain
pointers. Every implementation prints
`1000 moves in a tree of 100000 nodes: checksum 898591048`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `d8a8878fe` on LLVM 22. The
runs spread widely (C from 1.16 to 1.86 s): the walks chase pointers
through 100000 nodes, and the host's memory traffic shows.

| | median |
|---|---|
| Go | 1.64 s |
| C (`clang -O3`) | 1.80 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.62 s |
| Rust (`rustc -O`) | 2.68 s |
| Kāra (`karac build`) | 4.86 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 5.21 s |
| Python | 12.2 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (4.540 s and 4.548 s on one run).

Kāra is 1.98x Rust under overflow checks by median. Not traced; the IR
shows where it may go. `children` is a `mut` field of a `shared` struct,
so each `for child in node.children.iter()` takes the run-time borrow
flag of core semantics §6.2 and gives it back after the loop (one
`karac_mir_flag_acquire` and up to seven `karac_mir_flag_release` call
sites in `parent_of`), and the flag table is a short list searched by
address, which a walk holds one entry of per level of the recursion.
Rust's `RefCell` pays a borrow too, but in the cell itself.

## Verification

All four arms print the same output as `move.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them.
Under `karac __mir-run` the arms take 1.6 to 2.2 s and the differential
4.2 s.

## Writing it

The rebuild arm took 3 `karac fix` edits and then checked:
`parent.get(p) == Some(q)` compared an `Option[ref i64]` with an
`Option[i64]` and became `parent.get(p).cloned() == Some(q)`, and two
`retain(|c| *c != q)` closures lost the `*` (their `c` is an `i64`, while
`position(|c| *c == p)` on the same list takes the `*`). The other arms
were written in Kāra and `karac fix` had nothing to change.

## B-2026-11-08-31

The harness first folded the printed answer into its checksum with
`for b in show(root).bytes().iter() { check = mix(check, b as i64); }`.
`karac check` warned that `as i64` is an unnecessary cast, since a `u8`
widens to `i64` implicitly, and `karac fix` removed it. The result is
wrong on both backends: compiled, the call passes the address of the
`ref u8` the slice iterator yields (a two-byte string's checksum of 195
printed as 279565490929665), and the interpreter stops with
`Add on Int(0) and Ref(...)`. The same widening is right through
`let x: i64 = b`, `total += b`, `*b`, a `Vec[u8]`'s `iter()`, or
`for b in s.bytes()` without `iter()`, which the harness now uses. That
is B-2026-11-08-31: `karac fix` turns a correct program into a
miscompiled one.
