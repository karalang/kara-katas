# 609. Find Duplicate File in System

Given a list of directory lines, each a path followed by its files,
every file a name with its content in parentheses, return the groups of
files with the same content, two or more to a group, each file as its
full path. The groups and the paths in them may come in any order.

```
["root/a 1.txt(abcd) 2.txt(efgh)", "root/c 3.txt(abcd)", "root/c/d 4.txt(efgh)", "root 4.txt(efgh)"]
  ->  [["root/a/2.txt", "root/c/d/4.txt", "root/4.txt"], ["root/a/1.txt", "root/c/3.txt"]]
```

**Constraints:** 1 to 2 * 10^4 lines of 1 to 3,000 characters, 1 to 5 *
10^5 characters in all, of letters, digits, `/`, `.`, parentheses and
spaces; one space between a line's directory and each file, no two files
in one directory with one name, and no directory on two lines.

## Approaches

Every arm is `fn find_duplicate(paths: Vec[String]) ->
Vec[Vec[String]]`.

| file | mechanism |
|---|---|
| `find_duplicate.kara` ★ | each line `split` at its spaces into the directory and its files, each file cut at its `(` into a name and a content, and the path filed in a `Map` under the content; the groups of two or more; O(total length) |
| `find_duplicate_sorted.kara` | the same in a `SortedMap`, each line's parts `collect`ed into a `Vec[Str]` and each group taken out and put back as it grows; O(total length * log files) |
| `find_duplicate_pairs.kara` | each line read a character at a time into the directory and each file's name and content, every file listed as a pair of content and path, the pairs sorted, and every run of two or more with one content a group; O(total length * log files) |
| `find_duplicate_size.kara` | the problem's follow-up: each line cut with `find`, the files first grouped by the length of their content in a `Map`, and contents compared only within one length; O(total length + the comparisons) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 9 lines: the two LeetCode examples; five more
(no duplicates, one directory whose files are all alike, one file name
in three directories, contents that are prefixes of each other, and
contents of digits); totals and a checksum over 300 random systems of
1 to 8 directories; and the same for a system of 5,000 directories with
up to 6 files each. The groups are put in one order first, each one's
paths sorted and the groups sorted by their first path, since the
problem allows any. `find_duplicate.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every file listed as its path and content by reading each line a
character at a time, then each file not yet placed taking every later
file with the same content, keeping the groups of two or more. Each of
1,000 random cases is a system of 1 to 6 directories with up to 4 files
each, holding 1 to 6 contents of 1 to 4 letters from a and b, so
contents are often alike and often prefixes of each other. Every answer
is compared in the one order above.

| | property |
|---|---|
| P1 | the groups are the definition's |
| P2 | the lines in reverse order, and each line's files in reverse order, change nothing |
| P3 | one more directory with a file whose content no other file holds changes nothing |
| P4 | one more directory with a copy of a random file puts the copy in that file's group, or makes a group of the two |
| P5 | a letter added at the end of every content changes nothing |

It cannot run as written: it holds the ★ and sorted arms, refused at
their `split` (B-2026-10-12-7), and the pairs arm's `clear`
(B-2026-10-14-36). Its copy with the same lines changed as the arm
copies under Verification prints `1000 cases (1443 groups), 4 arms,
20000 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`
on a copy of the differential with only its `split` lines changed, as
under Verification. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a content held by one file kept as a group | P1 582, P3 1000, P4 444 |
| M2 | ★: the path without its directory | P1 822, P4 1000 |
| M3 | sorted: the files grouped by name, not content | P1 822, P4 1000 |
| M4 | sorted: the content cut one letter short | P1 128, P4 128, P5 128 |
| M5 | pairs: a file's name never cleared | P1 616, P2 640, P4 649 |
| M6 | pairs: a run of one kept as a group | P1 582, P3 1000, P4 444 |
| M7 | size: contents of one length compared by their first letter | P1 156, P4 156 |
| M8 | size: only the first file of each line read | P1 616, P2 547, P4 649 |
| E1 | ★: the content kept with its `)` | 0 |
| E2 | sorted: a group as `>= 2` | 0 |
| E3 | pairs: the pairs sorted by content alone | 0 |
| E4 | size: the files bucketed by length modulo 3 | 0 |

P3 sees M1 and M6 on every case, since the file it adds always makes a
group of its own once a group of one is kept. P4 sees M2 and M3 on every
case: M2 writes the copy's path without `root/new`, and M3 never groups
the copy, whose name no other file has. Both fail P1 on the 822 cases
with any group at all, M3 because every name in a system is different.
M4 cuts the letter that P5 adds, so on a renamed system it gives the
right groups, which are not its own; P5 fails it wherever P1 does.
E1 keeps one `)` at the end of every content, which changes none of them
relative to each other; E3 leaves the paths of one content in any order,
which the comparison's one order undoes.

## Verification

The pairs and size arms print the same output as `find_duplicate.py`
under `karac __mir-run` (the v2 MIR interpreter), and `karac check`
passes both. The size arm also prints it under `karac __mir-llvm-run`
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. Every compiled
v2 lane refuses the pairs arm at its `name.clear()`, which the MIR's
LLVM lowering does not handle for a `String` (B-2026-10-14-36, filed
from here). The ★ arm, the sorted arm, the differential and the bench
program are refused by every `karac` command, `check` included, at their
`split` (B-2026-10-12-7). So each blocked file was also run as a copy
outside this directory with the fewest lines changed: the ★ copy walks
`line.split(" ").into_iter()`, the sorted copy takes the parts as a
`Vec[String]` and reads each with `as_str()`, and the pairs copy, like
the differential's `reversed`, starts a fresh `String` where the arm
clears one. The three arm copies print the mirror's output under
`__mir-run` and `__mir-llvm-run` and run clean under `__mir-llvm-asan`;
the bench copy prints the mirrors' line. All at kara `d8c605558f`.

The frozen legacy backends run the size arm right under `karac run
--interp`, `karac run` and `karac build`. They run the pairs arm right
under `karac run` and `karac build`, and `run --interp` stops at its
`name.clear()` ("method 'clear' not found on type 'String'"). They
refuse the ★ arm, the sorted arm, the differential and the bench program
at the same `split`, and the copies get no further: the ★ copy runs
under `--interp` only, the compiled lanes stopping at its
`Iterator.next()` on an iterator of `String`s, and the sorted copy stops
at its `as_str()` everywhere. Legacy is frozen, so these are noted, not
filed.

## Benchmarks

The bench program uses the ★ arm. It makes 10 random systems of
2,000 directories with 1 to 6 files each, every file holding one of
3,000 contents of 8 to 20 letters from a to d, once; then 300 times
searches one of them, picked by the round, and adds up the groups, the
files in them, and for each group its size times the total length of its
paths, which does not depend on the order of the groups. Every
implementation prints `10 systems, 300 rounds: 613050 groups,
1905000 files, checksum 151629180`, and so does the Kāra copy described
below, under `karac __mir-run` too (in 33 s).

No Kāra build of the bench program as written exists yet: every `karac`
command refuses its `split` (B-2026-10-12-7), and the legacy `karac
build` refuses the copy as well, at the `all[(r * 3) % systems]` it
passes by value ("cannot move out of an index expression"). So
`bench.sh` builds it with `karac build --mir`, the v2 compiled backend,
and will time it once the row is fixed; that edit is by hand, on top of
the `scripts/new-bench.sh` output.

Every mirror splits each line at its spaces and files each path under
its content, a fresh string for each path: Rust a `HashMap<String,
Vec<String>>` filled through `entry`, Go a `map[string][]string`, Python
a `dict` through `setdefault`, and C an open-addressing table hashed by
FNV-1a whose keys and paths are `malloc`'d copies. Spot timings on a
shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.45 to 0.55 s |
| Rust (`rustc -O`) | 0.62 to 0.68 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.62 to 0.70 s |
| Go | 0.56 to 0.63 s |
| Python | 1.58 to 1.78 s |
| Kāra (`karac build --mir`), the `Vec[String]` copy | 1.16 to 1.31 s |

The Kāra row times the copy, at kara `d8c605558f`, and is not quite the
★ arm's cost: the copy's `split` makes a `String` of every part of every
line, where a `split` of views would make none. Under `karac
__mir-llvm-run` the copy prints the same line in 7.9 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

The Kāra row is about twice Rust's and Go's. valgrind counts
1.65 million heap allocations in 30 searches of the copy, the difference
between runs at 0 and at 30 rounds, to Rust's 0.72 million: about
55,000 a search to Rust's 24,000, over a system of some 7,000 files on
2,000 lines. By the program's reading, the copy's `split` alone makes a
`String` of every part of every line and a `Vec` of every line, some
11,000 a search that Rust's `split` of views does not; the rest of the
difference is not broken down here.

## Compiler findings

kara B-2026-10-14-36 (open), filed from here: the MIR's LLVM lowering
handles `clear` on a `Vec` but not on a `String`, so `__mir-llvm-run`,
`__mir-llvm-asan` and `karac build --mir` refuse any program that calls
it ("native `String.clear` is not lowered yet"), while `__mir-run` runs
it. It blocks the pairs arm and the differential in every compiled
v2 lane.

kara B-2026-10-12-7 (open), filed from kata 388: `split` returns an
eager `Vec[String]` of copies, where `docs/library/strings.md` gives it
`impl Iterator[Item = Str]` of views, so the ★ arm's `parts.next()` and
the sorted arm's `collect()` into a `Vec[Str]` are refused ("no method
'next' on type 'Vec'"). It blocks those two arms, the differential and
the bench program under every `karac` command; the copies run right.

The legacy failures above are not filed because legacy is frozen.
