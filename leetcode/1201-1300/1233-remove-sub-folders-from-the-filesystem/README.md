# 1233. Remove Sub-Folders from the Filesystem

Given a list of folders `folder`, return the folders after removing all
**sub-folders** in those folders. You may return the answer in **any
order**.

If a `folder[i]` is located within another `folder[j]`, it is called a
**sub-folder** of it. A sub-folder of `folder[j]` must start with
`folder[j]`, followed by a `"/"`. For example, `"/a/b"` is a sub-folder
of `"/a"`, but `"/b"` is not a sub-folder of `"/a/b/c"`.

The format of a path is one or more concatenated strings of the form:
`'/'` followed by one or more lowercase English letters. For example,
`"/leetcode"` and `"/leetcode/problems"` are valid paths while an empty
string and `"/"` are not.

```
folder = ["/a","/a/b","/c/d","/c/d/e","/c/f"]  ->  ["/a","/c/d","/c/f"]
folder = ["/a","/a/b/c","/a/b/d"]              ->  ["/a"]
folder = ["/a/b/c","/a/b/ca","/a/b/d"]         ->  ["/a/b/c","/a/b/ca","/a/b/d"]
```

**Constraints:** `1 <= folder.length <= 4 * 10^4`; `2 <= folder[i].length
<= 100`; `folder[i]` contains only lowercase letters and `'/'`;
`folder[i]` always starts with the character `'/'`; each folder name is
**unique**.

The arms are `fn remove_subfolders(folder: Vec[String]) -> Vec[String]`.
The two Rust arms keep the method LeetCode gives Rust users inside `impl
Solution`, and a one-line `remove_subfolders` calls it. Since the answer
may come in any order, every harness sorts it before printing.

## Approaches

| file | mechanism |
|---|---|
| `remove_sub_folders_from_the_filesystem.kara` ★ | sorted, a sub-folder comes after its parent and before anything outside it, so each folder is kept unless it begins with the last kept folder and a `/`. O(n log n · L) |
| `remove_sub_folders_from_the_filesystem_prefixes.kara` | every folder in a `Set[String]`; a folder is a sub-folder when the text before one of its `/`s, past the first, is a folder. No sort. O(n · L²) |
| `remove_sub_folders_from_the_filesystem_trie.kara` | a trie of the folders' names, each node's children a `Map[String, i64]` from name to node, with a mark where a folder ends; a folder is kept when the walk down its names meets no mark before its own end. O(n · L) |
| `remove_sub_folders_from_the_filesystem_parts.kara` | each folder split into its names, the `Vec[Vec[String]]` sorted by them, and a folder kept unless the last kept one's names begin its own |
| `remove_sub_folders_from_the_filesystem_sorted.kara` | a Rust solution as LeetCode's Rust users write it (the folders taken `mut` and sorted in place, moved one by one into the answer unless `if let Some(last) = ans.last()` and `starts_with(&format!("{}/", last))`), carried to Kāra by `karac fix` |
| `remove_sub_folders_from_the_filesystem_hashset.kara` | another Rust solution (the folders as `&str`s in a `HashSet`, kept by a `filter` over `char_indices().skip(1).any(..)`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 7 lines: LeetCode's three examples and one
folder, the total and a checksum of the folders kept from 1000 random
lists of up to 30 folders, 1 to 4 names deep, the names drawn from `a`,
`b`, `ab` and `ba` so that they share prefixes (`5147`, `244034938`),
and 4 · 10^4 folders of 1 to 4 names, a first of four letters and the
rest of two, of which 7610 are kept. `remove_sub_folders_from_the_filesystem.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac run` and `karac build`, and under the
AddressSanitizer build.

The Mend loop: the ★ and prefixes arms check clean as written. The trie
and parts arms were first written with Rust's `f.split('/')`, which the
fix makes `f.split("/")` (a separator is a `Str`), and collected its
pieces straight into a `Vec[String]`, which the fix makes `.map(|p|
p.to_string()).collect()`; the trie arm also inserted a piece as a map
key, which the fix makes `name.to_string()`. The sorted arm takes one
round of 15 fixes (among them `mut folder: Vec<String>` to `folder: own
Vec[String]` and a `let mut folder = folder`, `for f in folder` to `for
f in folder.into_iter()`, `&format!("{}/", last)` to `f"{last}/"`) and
the hashset arm one round of 16 (among them `HashSet<&str>` to
`Set[Str]`, `!` to `not`, `&&` to `and`, `&f[..i]` to `f[..i]`), and
both check clean.

## Gaps

None found.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a folder is removed when it begins with another folder and a
`/`, every pair tested, for lists of up to 60 folders. 2000 cases, a
third with up to 10 folders 3 deep, a third with 11 to 60 folders 4 deep
and a third with 61 to 600 folders 6 deep, the names drawn from `a`,
`b`, `ab` and `ba`.

| | property |
|---|---|
| P1 | the statement read literally (up to 60 folders) |
| P2 | every folder kept is given, none twice |
| P3 | the folders in reverse give the same answer |
| P4 | no folder kept lies within another kept |
| P5 | every folder given is kept or lies within one kept |
| P6 | the ★ arm's answer |

All 72,000 checks pass on every arm: `2000 cases: checksum 793844657,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python's answers for
the same cases, every pair tested, give the same checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the last kept compared without its `/` | P1 1007, P5 1661, P6 8305 |
| S2 | ★: compared with the first kept | P1 1035, P4 1689, P6 8445 |
| X1 | prefixes: the `/` kept on the prefix | P1 1103, P4 1757, P6 1757 |
| X2 | prefixes: a parent of one letter never counted | P1 902, P4 1556, P6 1556 |
| R1 | trie: a folder's own end counted | P1 1346, P5 2000, P6 2000 |
| R2 | trie: the parent itself never counted | P1 1003, P4 1657, P6 1657 |
| P1 | parts: the last name of the kept one not compared | P1 588, P5 592, P6 592 |
| P2 | parts: never sorted | P1 1060, P3 1492, P4 1714, P6 1714 |
| O1 | sorted: never sorted | P1 1060, P3 1492, P4 1714, P6 1714 |
| O2 | sorted: the last kept compared without its `/` | P1 1007, P5 1661, P6 1661 |
| H1 | hashset: the text before any letter | P1 1156, P4 1733, P5 1661, P6 1810 |
| H2 | hashset: the text one short of the `/` | P1 1121, P4 1733, P5 371, P6 1775 |

All twelve are caught, and P1, the statement read literally, catches
every one. A mutation of the ★ arm fails P6 on the five other arms. The
two invariants split the rest by which way an arm errs. Those that keep
a sub-folder fail P4, two kept folders one within the other: compared
with the first kept rather than the last (S2), the prefix tested with its
`/` (X1), parents of one letter (X2) or the parent itself (R2) never
counted. Those that drop a folder nothing holds fail P5: the last kept
compared without its `/` (S1, O2, the same mistake in two arms, so that
`/a/b/c` takes `/a/b/ca` with it), a kept folder's last name not compared
(P1, which drops its siblings), and a folder's own end counted (R1,
which drops every folder, in every case). H1 and H2, which test the
wrong prefixes, do both. Left unsorted (P2, O1, again the same mistake
in two arms) an arm answers by the order it is given, so P3, the folders
in reverse, catches those two alone. P2, every folder kept given and
none twice, catches none: every arm only ever keeps folders it was
given, each once.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm, sorted and each folder kept unless it begins with the last kept one
and a `/`, over 10 random lists of 4 · 10^4 folders of 1 to 4 names,
drawn once and each solved 10 times. Every program prints `10 lists of
40000 folders, 10 passes: 772940 kept`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.501 to 0.586 s | 0.516 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.296 to 1.420 s | 1.376 s |
| Rust (`rustc -O`) | 1.466 to 1.606 s | 1.562 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.480 to 1.720 s | 1.537 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 1.503 to 1.764 s | 1.573 s |
| C (`clang -O3`) | 0.909 to 1.031 s | 0.934 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.886 to 1.008 s | 0.942 s |
| Go | 1.405 to 1.566 s | 1.466 s |
| Python | 2.724 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` gives a different binary
here, with a loop its cost gate accepts compiled to run in parallel; its
median is 0.516 s, with 1.228 s of user time spread over the cores. Kāra
is about 10% ahead of Rust with overflow checks on (1.376 s against
1.537 s). C is about 32% ahead of Kāra (0.934 s against 1.376 s); Kāra
is about 6% ahead of Go (1.376 s against 1.466 s). Python takes about 2x
Kāra's time. No profile was taken.
