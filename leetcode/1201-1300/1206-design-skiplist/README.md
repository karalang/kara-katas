# 1206. Design Skiplist

Design a Skiplist without using any built-in libraries. A skiplist is a
data structure that takes `O(log(n))` time to add, erase and search.
Comparing with treap and red-black tree which has the same function and
performance, the code length of Skiplist can be comparatively short and
the idea behind Skiplists is just simple linked lists.

Implement the `Skiplist` class:

- `Skiplist()` Initializes the object of the skiplist.
- `bool search(int target)` Returns `true` if the integer `target` exists
  in the Skiplist or `false` otherwise.
- `void add(int num)` Inserts the value `num` into the SkipList.
- `bool erase(int num)` Removes the value `num` from the Skiplist and
  returns `true`. If `num` does not exist in the Skiplist, do nothing and
  return `false`. If there exist multiple `num` values, removing any one
  of them is fine.

Note that duplicates may exist in the Skiplist, your code needs to
handle this situation.

```
Skiplist(), add(1), add(2), add(3), search(0) -> false, add(4),
search(1) -> true, erase(0) -> false, erase(1) -> true, search(1) -> false
```

**Constraints:** `0 <= num, target <= 2 * 10^4`; at most `5 * 10^4`
calls will be made to `search`, `add`, and `erase`.

Each arm is a `struct Skiplist` with `Skiplist.new()`, `search`, `add`
and `erase`, on `i32` in the two Rust arms as LeetCode gives Rust users,
and on `i64` in the others, which take the harness's `i32` values
widened.

## Approaches

| file | mechanism |
|---|---|
| `design_skiplist.kara` ★ | a skiplist whose nodes live in a `Vec`, each node's forward links one per level it stands on (`-1` for none), node 0 the head on all 16; a new node's height by coin flips from the list's own generator, each level half as likely as the one below; an erased node's slot reused by the next add. Expected O(log n) each |
| `design_skiplist_sorted.kara` | the plain reading: one sorted `Vec`, binary search, and `insert` and `remove` at the found place. O(log n) to search, O(n) to add or erase |
| `design_skiplist_counts.kara` | a `SortedMap` from each value to how many times it is held, the entry dropped at zero. O(log n) each |
| `design_skiplist_linked.kara` | each node a `shared struct`, its links an `Option[Node]` per level, walked by cloning handles; a new node's height the trailing one bits of how many adds came before it, plus one, so every second node stands on level 2, every fourth on level 3, with no generator; erase finds the node's predecessors' links by identity, `ref_eq` |
| `design_skiplist_rc.kara` | a Rust solution as LeetCode's Rust users write it (`type Link = Option<Rc<RefCell<Node>>>`, the walk down cloning the `Rc` it stands on and reading through `borrow()`, writes through `borrow_mut()`, `Rc::ptr_eq` for identity, the height from a xorshift generator), carried to Kāra by `karac fix` |
| `design_skiplist_arena.kara` | another Rust solution (the nodes in a `Vec<Node>` indexed by `usize`, links `Vec<Option<usize>>`, the predecessors in a `[usize; MAX_LEVEL]`, the walk by `while let Some(nx) = self.nodes[cur].next[lv]`, the height from a 64-bit linear congruential generator with `wrapping_mul`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six more properties |

Every arm prints the same 11 lines: LeetCode's example, call by call;
three 5s erased four times beside a 0 and a 20000 (`[true, true, true,
false]`, and 5 gone while 0 and 20000 stay); an empty list searched, given
one value and that value erased, then searched and erased again; 0 to
999 added and every even one erased from the top down (`500 left`); 100
runs of 100 random calls on values below 10 (`checksum 273984453`); and
two runs of 50000 calls, the constraints' most, on values up to 20000
(`4440 found, 4518 erased, checksum 301645314`) and below 100 (`15380
found, 15195 erased, checksum 475175686`). `design_skiplist.py` mirrors
the ★ arm, and its output is byte-identical. Every arm gives the same
output under `karac run` and `karac build`, and under the
AddressSanitizer build.

The Mend loop: the ★, sorted, counts and linked arms check clean as
written, once the linked arm's `next` is declared `mut next`, as a
`shared struct` field written through a handle must be, and its identity
test written `ref_eq` (design.md, Equality). The rc arm takes one round
of 57 fixes (among them the two `use` lines dropped, `Node` made a
`shared struct` with `mut` fields and `Rc<RefCell<Node>>` written `Node`,
`Rc::new(RefCell::new(Node { .. }))` written `Node { .. }`, every
`.borrow()` and `.borrow_mut()` dropped, `Rc::ptr_eq(n, &target)` to
`n.ref_eq(target)`, `match &update[lv].borrow().next[lv]` to `match ref
update[lv].next[lv]`, and `&self` / `&mut self` to `self` / `mut ref
self`); the arena arm one round of 23 (among them `usize` to `i64`,
`[usize; MAX_LEVEL]` to `Array[i64, MAX_LEVEL]` and `[0usize; MAX_LEVEL]`
to `[0; MAX_LEVEL]`, `i32::MIN` to `i32.MIN`, and `vec![None; lv]` to
`Vec.filled(lv, None)`). Both outputs match. The rc arm keeps `mut val`
although nothing writes `val`: a `RefCell` lets every field be written,
and the fix keeps that.

## Gaps

None found.

## Differential

`differential.kara` holds copies of the six arms, each played through a
list of calls, and the statement read literally: the values held in a
`Vec` in the order they were added, a search looking at every one and an
erase removing the first equal one. 1000 random cases: 1 to 40 calls on
values below 2, 4 or 8.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | an erase answers as a search just before it does |
| P3 | a search just after an add finds the value |
| P4 | every value one more gives the same answers |
| P5 | after the calls, erasing each value until refused erases as many as are held |
| P6 | after that, every search finds nothing |
| P7 | the ★ arm's answers |

All 42,000 checks pass on every arm: `1000 cases: checksum 436953420,
42000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. A Python reading of
the same cases, a list searched and erased from, gives the same
checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the walk passes values equal to the target | P1 840, P3 945, P5 904, P7 4200 |
| S2 | ★: a reused slot keeps the erased value | P1 485, P3 568, P5 580, P6 228, P7 2425 |
| O1 | sorted: the search lands past the equal values | P1 840, P3 945, P5 904, P7 840 |
| O2 | sorted: a new value pushed at the end | P1 592, P3 653, P5 668, P6 115, P7 592 |
| C1 | counts: a value added again counted once | P1 360, P5 676, P7 360 |
| C2 | counts: a count of one kept at zero | P1 513, P5 945, P6 945, P7 513 |
| L1 | linked: a new node links to nothing after it | P1 623, P5 744, P7 623 |
| L2 | linked: an erased node left linked on level 0 | P1 513, P5 945, P6 945, P7 513 |
| R1 | rc: the walk passes values equal to the target | P1 840, P3 945, P5 904, P7 840 |
| R2 | rc: an erase takes the next value whatever it is | P1 561, P2 561, P5 809, P7 561 |
| A1 | arena: the walk passes values equal to the target | P1 840, P3 945, P5 904, P7 840 |
| A2 | arena: a new node links to nothing after it | P1 624, P5 745, P7 624 |

A mutation of the ★ arm fails P7 on all six arms, the ★ arm against the
other five. S1, O1, R1 and A1 are one fault in four arms, the walk or the
binary search passing values equal to the target, so a search never
lands on one, and fail alike; P3 catches each in all 945 cases with an
add (counted by a Python reading of the cases). C2 and L2 fail alike
too: a value whose last copy is erased stays findable, a count of zero
in one and a node left on level 0 in the other, so the erasing after the
calls (P5) and the searches after that (P6) fail in all 945. R2, which
erases the next greater value when the target is absent, is the only one
P2 catches: its erase answers true where a search just before answers
false. S2 reuses an erased node's slot without writing the new value, so
the slot keeps the old value at the place the list gives the new one. P4, every value
one more, catches none of the twelve: no arm treats a value specially,
the rc arm's head holding -1 and the arena arm's `i32.MIN` below every
value either way.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (a skiplist whose nodes live in a `Vec`, each node's forward links
one per level it stands on, heights by coin flips from the list's own
generator, erased slots reused) on 50000 calls drawn once, the
constraints' most, a third each of search, add and erase, on values up
to 20000; then 10 rounds, each on a new list, every answer folded into a
checksum. Every program prints `10 rounds of 50000 calls: checksum
54857688`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.160 to 0.378 s | 0.174 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.163 to 0.359 s | 0.180 s |
| Rust (`rustc -O`) | 0.161 to 0.197 s | 0.174 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.158 to 0.191 s | 0.176 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.152 to 0.255 s | 0.159 s |
| C (`clang -O3`) | 0.098 to 0.122 s | 0.103 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.096 to 0.122 s | 0.107 s |
| Go | 0.161 to 0.188 s | 0.172 s |
| Python | 2.457 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (0.176 s
against 0.180 s), and the two ranges overlap. Kāra takes about 1.7x C's
time (0.180 s against 0.103 s); Go runs level with Kāra (0.172 s against
0.180 s). Python takes about 14x Kāra's time. No profile was taken.
