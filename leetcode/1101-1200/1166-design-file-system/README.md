# 1166. Design File System

You are asked to design a file system that allows you to create new paths
and associate them with different values.

The format of a path is one or more concatenated strings of the form: `/`
followed by one or more lowercase English letters. For example,
`"/leetcode"` and `"/leetcode/problems"` are valid paths while an empty
string `""` and `"/"` are not.

Implement the `FileSystem` class:

- `bool createPath(string path, int value)` creates a new path and
  associates a value to it if possible and returns `true`. Returns
  `false` if the path already exists or its parent path doesn't exist.
- `int get(string path)` returns the value associated with `path` or
  returns `-1` if the path doesn't exist.

```
["FileSystem","createPath","get"]
[[],["/a",1],["/a"]]                                   ->  [null,true,1]
["FileSystem","createPath","createPath","get","createPath","get"]
[[],["/leet",1],["/leet/code",2],["/leet/code"],["/c/d",1],["/c"]]
                                                       ->  [null,true,true,2,false,-1]
```

**Constraints:** `2 <= path.length <= 100`; `1 <= value <= 10^9`; each
path is valid and consists of lowercase English letters and `/`; at most
`10^4` calls in total will be made to `createPath` and `get`.

The arms are a `struct FileSystem` with `fn new() -> FileSystem`, `fn
create_path(mut ref self, path: Str, value: i64) -> bool` and `fn get(self,
path: Str) -> i64`.

## Approaches

A path may be made when it is new and its parent, the path less its last
name, was made or is the root; the arms differ in how a made path is kept
and how its parent is found.

| file | mechanism |
|---|---|
| `file_system.kara` ★ | one map: every made path a key of a `Map[String, i64]`, its parent the text before its last `/` (`rfind`), looked up as a key. O(L) a call for a path of length L |
| `file_system_trie.kara` | a tree of directories: each made path a `shared struct Dir` holding its value and a `Map` from a name to the directory under it, walked from the root one name at a time. O(L) a call |
| `file_system_sorted.kara` | a `SortedMap[Vec[String], i64]` keyed by a path's names, `/leet/code` as `["leet", "code"]`, its parent the key with the last name dropped. O(L log n) a call |
| `file_system_list.kara` | a list: every made path and its value in a `Vec` of pairs, in the order made, each call a walk of the whole list with `any` or `find`. O(n L) a call |
| `file_system_solution.kara` | a Rust solution as LeetCode's Rust users write it (`HashMap<String, i32>`, `&mut self`, `String` parameters, the parent as `&path[..idx]` up to `rfind('/')`, the answer read with `*...unwrap_or(&-1)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's examples (`1 1` and `1 1 2 0
-1`); a path made twice, the second refused and the first value kept; a
get before anything is made (-1); a child refused before its parent is
made, then made after it; and a name that begins another (`/le` and
`/leet`), so that a parent is found by its whole name. Then 300 random runs
of 1 to 60 operations over paths of 1 to 4 names (`300 random runs: made
1472, checksum 255681582`), and 10^4 operations, the constraints' most: a
chain 33 deep, its last path 99 letters long, then random paths made and
asked for in turn (`10000 operations: 9646 not -1, sum 2544621`).
`file_system.py` mirrors the ★ arm and its output is byte-identical; a
Python reading that keeps the made paths in a list and walks it for every
call gives the same output.

The Mend loop: the ★, sorted and list arms each take one fix, `mut self`
to `mut ref self` on `create_path`, the method that writes. The trie arm
takes that one and, in a second round, `.cloned()` on the two `match
at.kids.get(name)` scrutinees: `get` lends an `Option[ref Dir]`, so
`Some(next) => at = next` would drop `at` while `next` still borrows it,
and a copy of the `shared` handle borrows nothing. The Rust arm takes
three rounds (13, 2 and 2 edits): the generics to brackets, `::` to `.`,
the `use` line deleted, `&mut self` and `&self` to `mut ref self` and
`self`, the `&` of every argument and of `&-1` dropped, and `!` and `&&`
to `not` and `and`; then `HashMap` to `Map`; then `path: own String`,
since the map keeps it, and `rfind('/')` to `rfind("/")`. The `i32`
values and the `*` before `unwrap_or` are kept. Its output matches on the
first run.

Writing the trie arm found a gap in the Mend loop: the error on `at =
next` named the repair, `.cloned()` on the `Option[ref Dir]`, and an `if
let` or `while let` over the same `get` got it as a fix, but a `match`
got none. That is kara B-2026-11-15-49, fixed at `1bdebaaa70`.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the made paths and their values in a list; a path is one or
more names each after a `/`, and it may be made when no made path equals
it and, unless it has one name, the path of all its names but the last
was made. It checks 1200 runs in four kinds of 300: 1 to 12 operations
over paths of 1 to 3 names from the first 1 or 2 of six (`a`, `b`, `ab`,
`le`, `leet`, `code`, some beginning others); 1 to 60 over 1 to 4 names
from the first 1 to 6; 50 to 150, three in four of them creates, over 1
to 5 names from all six; and 1 to 40 over the prefixes of one path of 6
to 20 names, so that a chain is made out of order. Every random choice the
properties make is drawn before any arm answers, among them a renaming
of the six names and a second value for every create.

| | property |
|---|---|
| P1 | every answer is the literal one |
| P2 | every name renamed alike keeps every answer |
| P3 | after the operations, a get of each path a create named gives the value of the create that answered `true` for it, or -1 |
| P4 | each create repeated at once with another value: the repeat answers `false` and every other answer stays |
| P5 | everything moved under a new `/root`, made first, keeps every answer |
| P6 | the gets left out keep every create's answer |

All 36,000 checks pass on every arm: `1200 runs: checksum 357109051,
36000 checks over 5 arms: 0 failures`, in 47 s under `karac __mir-run`.
A Python reading of the same draws, with the mirror against the literal
reading, gives the same checksum.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. Fourteen are caught and one is
equivalent: the list arm reading the last match rather than the first
(L1), since a path is made at most once.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the parent never checked | P1 1142 |
| M2 | ★: a made path made again, its value replaced | P1 771, P4 974 |
| M3 | ★: a path never made read as 0 | P1 1108, P3 1083 |
| T1 | trie: a made directory made again, emptied | P1 771, P3 504, P4 974 |
| T2 | trie: a get walking from the second name | P1 731, P3 974, P5 561 |
| T3 | trie: a create walking half the way to its parent | P1 747, P3 721, P5 976 |
| S1 | sorted: a parent of one name never checked | P1 805, P5 805 |
| S2 | sorted: a path never made read as 0 | P1 1108, P3 1083 |
| S3 | sorted: the parent as the path less its first name | P1 593, P5 974 |
| L2 | list: a made path made again | P1 771, P3 771, P4 974 |
| L3 | list: any made prefix of the text taken for the parent | P1 799, P2 341, P5 1082 |
| X1 | solution: a top-level path's empty parent looked up | P1 974, P5 1200 |
| X2 | solution: every value stored one more | P1 652, P3 974 |
| X3 | solution: the parent cut at the first `/` | P1 1142 |

P1 catches all fourteen, P3 seven, P5 six, P4 three, P2 one and P6 none.
An unchecked parent (M1, and X3, whose parent is always empty) is seen by
P1 alone: a run made without the check answers every other property
consistently with itself. P2 sees only L3, the one edit that compares a
parent by its letters rather than as a whole path, where `/le` passes for
`/leet`'s parent; the six names, some beginning others, are there for it.
P6 sees none, since no edit gives a get an effect; it stays as a check
that a get changes nothing. The edit first
written as T3, a create walking from the second name, stopped on the
first one-name path with an out-of-bounds slice before any property could
answer, so it was replaced by one that runs.

## Benchmarks

`bench/` times the ★ arm against one hash map from a made path to its
value in C (open addressing, FNV-1a, its own table), Rust (`HashMap`, the
default SipHash), Go (`map`) and Python (`dict`). 16 lists of 10^4
operations over paths of 1 to 5 names from six (`a`, `b`, `ab`, `le`,
`leet`, `code`), three in four of them creates, are built once; each of
100 rounds runs every list from a random place in its first half on a new
file system. Every program prints `100 rounds over 16 lists of 10^4
operations: made 1795608, checksum 567776439`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `1bdebaaa70`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Go | 0.523 to 0.653 s | 0.613 s |
| Rust (`rustc -O`) | 0.613 to 0.703 s | 0.625 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.598 to 0.694 s | 0.644 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.645 to 0.701 s | 0.657 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.630 to 0.732 s | 0.660 s |
| C (`clang -O3`) | 0.652 to 0.745 s | 0.672 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.637 to 0.794 s | 0.683 s |
| Kāra (`karac build`) | 0.645 to 0.785 s | 0.697 s |
| Python | 3.3 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; a plain `karac build` gives the same binary, so the
two Kāra rows are one program timed twice. Every compiled program is
within about 0.1 s of the others: the work is building each path's text
and hashing it, which all of them do alike. Kāra takes about 1.06x
overflow-checked Rust's time, the equal-safety comparison, and about
1.02x C's. Go is the fastest by its median, with a user time (0.69 s)
above its wall time, so some of its garbage collection runs on another
core. Python takes about 4.8x Kāra's time.
