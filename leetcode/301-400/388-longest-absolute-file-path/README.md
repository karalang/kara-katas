# 388. Longest Absolute File Path

A file system is listed one entry per line: a line's leading tabs give
its depth, and the rest is its name. Names with a `.` are files and the
others are directories; a file has no children. Return the length of
the longest absolute path to a file, counting the `/` between names, or
0 if there is no file.

```
"dir\n\tsubdir1\n\tsubdir2\n\t\tfile.ext"  -> 20   ("dir/subdir2/file.ext")
"dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext"
                                             -> 32   ("dir/subdir2/subsubdir2/file2.ext")
"a"                                          -> 0
```

**Constraints:** `1 <= input.len() <= 10^4`; `input` holds lowercase or
uppercase letters, digits, `.`, spaces, `\n` and `\t`; every name has
length at least 1.

## Approaches

| file | mechanism | time | extra space |
|---|---|---|---|
| `length_longest_path.kara` ★ | one pass over the bytes, keeping `len[d]`, the length of the path to the directory open at depth d with its `/`; deeper entries left from earlier lines are overwritten | O(n) | O(d) for the deepest nesting d |
| `length_longest_path_split.kara` | split into lines; count each line's leading tabs; a stack of path lengths, popped to the line's depth | O(n) | O(n) for the lines |
| `length_longest_path_tree.kara` | build the tree first (the most recent node at each depth is the parent of the next deeper line), then a recursive walk | O(n) | O(n) |
| `length_longest_path_map.kara` | the ★ arm's idea with a `Map[i64, i64]` from depth to path length and the lines from `split` | O(n) expected | O(n) |
| `differential.kara` | the four arms against listings whose answer is known by construction, 2,000 random listings, five properties | — | — |

Every arm prints the same 11 lines: the two LeetCode examples, eight edge
cases (no files, one and three files at the root, a dotted name, a deep
file losing to a long shallow one, empty directories, a file after a
deep directory, names with spaces),
and for 2,000 random listings of 1 to 30 entries the longest answer, how
many have no file, and a checksum. `length_longest_path.py` mirrors the
★ arm and its output is byte-identical.

The splitting arm counts a line's leading tabs with a loop over
`line.chars()`. A first draft used `line.trim_start_matches('\t')`,
which is Rust's; the strings library has only `trim`, and the second
draft's `line.len() - line.trim().len()` was wrong for names that start
or end with a space, which the problem allows. The names-with-spaces
case was added for that.

## Differential

`differential.kara` holds copies of the four arms and a generator that
works out the longest file path while it builds each listing: it keeps
the path length of every open directory, so the answer is known without
running any arm.

| | property |
|---|---|
| P1 | every arm gives the generator's answer |
| P2 | moving everything one level down under a new directory `root` adds 5 (`root/`) to a non-zero answer and leaves 0 alone |
| P3 | a file `x.y` added at the top gives the larger of the answer and 3 |
| P4 | with every file line taken out, the answer is 0 |
| P5 | reversing the order of the top-level entries, each with everything below it, changes nothing |

It prints `2000 listings, 40000 checks, 0 failures` under
`karac __mir-run`. The differential collects the lines with
`text.split("\n")`, which returns a `Vec[String]`; see Compiler findings.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | how |
|---|---|---|
| M1 | depths: an overwritten level leaves out the `/` | P1, P2, P3 and P5, 4507 failures |
| M2 | depths: a level already seen is never overwritten | P1, P2, P3 and P5, 4432 failures |
| M3 | depths: a name is one byte shorter | P1, P2, P3 and P5, 7640 failures |
| M4 | split: pops one level too few | P1, P2, P3 and P5, 6880 failures |
| M5 | split: a directory pushes no `/` | P1, P2, P3 and P5, 5954 failures |
| M6 | tree: no `/` between a directory and its children | P1, P2, P3 and P5, 5954 failures |
| M7 | tree: the parents of deeper levels are never dropped | P1, P2, P3 and P5, 4805 failures |
| M8 | map: the tabs count as part of the name | P1, P2, P3 and P5, 6032 failures |

P4 catches none of them: with no files every arm answers 0 whatever its
path arithmetic. It stays as a check that no arm counts a directory as a
file. M5 and M6 are one mistake in two arms and give the same counts.

## Verification

All four arms print the same output as `length_longest_path.py` under
`karac __mir-run` (the v2 MIR interpreter), and `karac check` passes on
every file. Every file also prints the same output under
`karac __mir-llvm-run`, since compiler commit 62f5f6de04 added the
`String.as_str` native. The by-depth, splitting and map arms also match
under `karac run --interp`. The legacy backends fail as Compiler
findings describes.

## Benchmarks

The bench program uses the ★ arm. It builds 200 random listings of 800
entries each (1,583,883 bytes in all, about 7,900 bytes a listing, the
problem allowing 10,000) once, then runs the arm over all of them 150
times and folds the answers into a checksum. The C, Rust, Go and Python
mirrors print `1583883 bytes in 200 listings, 150 rounds, checksum
780154256`, and a 3-round cut of the Kāra program prints the same as the
C program cut the same way. Spot timings on a shared 4-core container
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| Rust (`rustc -O`) | 0.69 s |
| C (`clang -O3`) | 0.73 s |
| Go | 0.80 s |
| Python | 24 s |

`karac __mir-run` was killed for memory after 2 min 10 s at 8.6 GB,
because every `bytes()` call keeps a copy of the string (kara
`B-2026-10-12-8`), and the legacy native build stops in codegen. The
Kāra program prints the same line under `karac __mir-llvm-run` in
2.4 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

## Compiler findings

- **`.bytes()` copies are kept until exit in the MIR interpreter**
  (kara `B-2026-10-12-8`). Each call copies the string into one
  interpreter value per byte, about 63 bytes of memory per byte, and
  keeps the copy until the program ends. Reading a 10,000-byte string
  with `bytes()` 400 times peaks at 286 MB, against 43 MB for the same
  walk with `chars()`.
- **`T.parse` returns `Option`, but the v1 spec says `Result`**
  (kara `B-2026-10-12-6`). `docs/library/core-types.md` gives
  `fn parse(s: Str) -> Result[Self, ParseError]` and matches on
  `Ok`/`Err`; the compiler returns `Option[Self]`, has no `ParseError`,
  and refuses the spec's own example. Found while looking up string
  methods; katas up to 385 call `.unwrap()` on the `Option`.
- **`split`, `lines` and `split_whitespace` return `Vec[String]`, but
  the v1 spec says a lazy iterator of `Str` views** (kara
  `B-2026-10-12-7`). `docs/library/strings.md`'s own example,
  `let parts: Vec[Str] = line.split(",").collect();`, is refused with
  `no method 'collect' on type 'Vec'`.

Two failures in the legacy backends, which are frozen, so not filed:

- **Legacy codegen has no `bytes` or `split` on a `Str` parameter.**
  LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac build` stop with
  `no handler for method 'bytes'` (by-depth and tree arms, the bench) or
  `no handler for method 'split'` (splitting and map arms).
- **The legacy typechecker refuses `*c` on the items of a `Vec[i64]`
  iterator**, in the tree arm and the differential, as in katas 382,
  383 and 386.
