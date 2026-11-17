# 1600. Throne Inheritance

A kingdom consists of a king, his children, his grandchildren, and so
on. Every once in a while, someone in the family dies or a child is
born.

The kingdom has a well-defined order of inheritance that consists of the
king as the first member. Let's define the recursive function
`Successor(x, curOrder)`, which given a person `x` and the inheritance
order so far, returns who should be the next person after `x` in the
order of inheritance.

```
Successor(x, curOrder):
    if x has no children or all of x's children are in curOrder:
        if x is the king return null
        else return Successor(x's parent, curOrder)
    else return x's oldest child who's not in curOrder
```

Implement the `ThroneInheritance` class:

- `ThroneInheritance(string kingName)` initializes an object of the
  class. The name of the king is given as part of the constructor.
- `void birth(string parentName, string childName)` indicates that
  `parentName` gave birth to `childName`.
- `void death(string name)` indicates the death of `name`. The death of
  the person doesn't affect the `Successor` function nor the current
  inheritance order. You can treat it as just marking the person as dead.
- `string[] getInheritanceOrder()` returns a list representing the
  current order of inheritance excluding dead people.

```
birth(king, andy), birth(king, bob), birth(king, catherine),
birth(andy, matthew), birth(bob, alexander), birth(bob, asha)
getInheritanceOrder  ->  [king, andy, matthew, bob, alexander, asha, catherine]
death(bob)
getInheritanceOrder  ->  [king, andy, matthew, alexander, asha, catherine]
```

**Constraints:** `1 <= kingName.length, parentName.length,
childName.length, name.length <= 15`; names are lowercase English
letters; all `childName` and `kingName` are distinct; every name given
to `death` was given to the constructor or as a `childName` first; for
each `birth(parentName, childName)`, `parentName` is alive; at most
`10^5` calls to `birth` and `death`; at most 10 calls to
`getInheritanceOrder`.

## Approaches

The order is a preorder of the family tree, children in birth order,
with the dead left out and their children kept.

| file | mechanism |
|---|---|
| `throne.kara` ★ | each person's children in a `Map[String, Vec[String]]`, the dead in a `Set[String]`, and the preorder walked with an explicit stack of `Str`s, children pushed in reverse. O(1) a birth or death, O(n) an order |
| `throne_recursive.kara` | everyone numbered at birth, a `Map[String, i64]` from name to number, children in a `Vec[Vec[i64]]` and the living in a `Vec[bool]`; the preorder a recursive method. O(1) a birth or death, O(n) an order |
| `throne_tree.kara` | the family as a tree of `shared struct Person` nodes (name, alive, children), with a `Map[String, Person]` from each name to its node, so a birth appends to the parent's own list and a death marks the node. O(1) a birth or death, O(n) an order |
| `throne_solution.kara` | LeetCode's Rust template (a `HashMap<String, Vec<String>>`, a `HashSet<String>`, and a recursive `dfs(&self, &String, &mut Vec<String>)`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's example and the order once
more after the king dies and a grandchild of the dead `bob` is born,
then the count of orders and a checksum for 3000 random reigns of up to
10 calls, 300 of up to 200 and 3 of up to 5000: a birth to someone alive
half the time, a death of someone alive an eighth, and the order asked
for the rest. `throne.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms, each struct renamed
and driven by its own copy of one `drive`, and the statement read
literally: the order built by its `Successor` function from the king,
one call at a time until it answers no one, with each person's parent
and children kept as the births give them, and then the dead taken out.
It checks 3000 reigns of 1 to 12 calls, every random choice drawn before
any arm answers.

| | property |
|---|---|
| P1 | every order asked for is the statement's `Successor` read literally |
| P2 | every name but the king's renamed renames every order |
| P3 | each order asked for twice in a row gives it twice |
| P4 | one more death at the end takes exactly that name out of the order |
| P5 | one more child of the king at the end is last in the order |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 771429197, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: children pushed in birth order, so walked youngest first | P1 1037, P5 1673, P6 1037 |
| M2 | ★: the king never leaves the order | P1 1688, P4 512, P6 1688 |
| M3 | ★: a new child put first among its siblings | P1 1037, P5 1673, P6 1037 |
| M4 | recursive: only the two eldest children walked | P1 477, P5 991, P6 477 |
| M5 | recursive: every child recorded as the king's | P1 459, P6 459 |
| M6 | tree: a dead person with no children still listed | P1 1886, P4 962, P5 946, P6 1886 |
| M7 | tree: a death removes the children, not the person | P1 2222, P4 1247, P6 2222 |
| M8 | template: a dead person's line skipped | P1 308, P4 329, P6 308 |
| M9 | template: a death removes the children, not the person | P1 2222, P4 1247, P6 2222 |
| M10 | tree: children walked youngest first | P1 1037, P5 1673, P6 1037 |

## Benchmarks

The bench runs the ★ arm through 10 reigns of 50000 calls, drawn first:
a birth to someone alive half the time, a death of someone alive an
eighth, and the order asked for once in 1000 calls, in all five
languages. Every implementation prints `10 reigns of 50000 calls:
3490819 names in the orders, checksum 136311609`. C has no map, so the C
mirror keeps each name in an open-addressing table hashed by FNV-1a
(linear probing, grown at half full) whose entries hold each person's
children as a growable array of names and whether they are dead; the
preorder is walked with a stack and each name in the order is copied, as
Kāra's `to_string` does.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5dc4418bbd` on LLVM 22:

| | median |
|---|---|
| Go | 0.659 s |
| C (`clang -O3`) | 0.681 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.794 s |
| Rust (`rustc -O`) | 0.800 s |
| Kāra (`karac build`) | 0.952 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.972 s |
| Python | 1.6 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is below its real time (0.892 s and 0.911 s on one run).

## Verification

All four arms print the same output as `throne.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. No output
depends on a `Map` or `Set` walk: the arms only look names up. Checked
at kara `5dc4418bbd`.

## Writing it

The recursive and tree arms were written in Kāra and checked as written.
The ★ arm first took its names as bare `String` parameters and stored
them; `karac fix` wrote `own` on each, as a bare parameter borrows. The
shared harness wrote `"king".to_string()` and the like for each name
handed to the arm, `b as i64` for a byte, and `child.clone()` for a
name it keeps; `karac fix` dropped the `to_string()`s and the cast, and
the `.clone()` stayed, as `birth` now takes its names by value. The
differential's `Op` enum was cloned without a `#[derive(Clone)]`, and
`karac fix` added it.

The Rust template took one `karac fix`, of 32 edits: the `use` line
dropped, `HashMap<String, Vec<String>>` and `HashSet<String>` to
`Map[String, Vec[String]]` and `Set[String]`, the `String` parameters to
`own String`, `&self` and `&mut self` to `self` and `mut ref self`,
`&String` to `String`, `&mut Vec<String>` to `mut ref Vec[String]`,
`::new` to `.new`, the calls' `&` and `&mut` dropped or made `mut`, and
`!` to `not`. It then checks and agrees with no hand edit.
