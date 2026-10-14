# 588. Design In-Memory File System

Design a data structure that simulates an in-memory file system.
Implement the `FileSystem` class: `FileSystem()` initializes the object
of the system. `ls(path)`: if `path` is a file path, returns a list that
only contains this file's name; if `path` is a directory path, returns
the list of file and directory names in this directory, in lexicographic
order. `mkdir(path)` makes a new directory according to the given path;
the given directory path does not exist, and if the middle directories
in the path do not exist, they are created as well.
`addContentToFile(filePath, content)`: if `filePath` does not exist,
creates that file containing the given content; if it already exists,
appends the given content to the original content.
`readContentFromFile(filePath)` returns the content in the file at
`filePath`.

```
ls("/")                            ->  []
mkdir("/a/b/c")
addContentToFile("/a/b/c/d", "hello")
ls("/")                            ->  ["a"]
readContentFromFile("/a/b/c/d")    ->  "hello"
```

**Constraints:** `1 <= path.length, filePath.length <= 100`; `path` and
`filePath` are absolute paths which begin with `/` and do not end with
`/`, except that the path is just `/`; all directory and file names
contain only lowercase letters, and the same names will not exist in the
same directory; all operations are passed valid parameters, and no one
reads a file or lists a path that does not exist; `1 <= content.length
<= 50`; at most 300 calls are made to `ls`, `mkdir`, `addContentToFile`
and `readContentFromFile`.

## Approaches

Every arm is a `FileSystem` with `fn new() -> FileSystem`, `ls(self,
path: Str) -> Vec[String]`, `mkdir(mut ref self, path: Str)`,
`add_content_to_file(mut ref self, file_path: Str, content: Str)` and
`read_content_from_file(self, file_path: Str) -> String`. The statement
does not say what adding to a file does when a directory above it is
missing; every arm makes it, as `mkdir` would, and the harness relies on
that.

| file | mechanism |
|---|---|
| `file_system.kara` ★ | a tree of `shared` nodes, each directory's entries in a `SortedMap` by name; a handle walks down from the root and changes the node at the end in place; O(path length) for each step |
| `file_system_owned.kara` | a tree of owned nodes: making a path is a recursion that hands each child on as a `mut ref`, and reading one walks `ref` borrows down from the root; O(path length) |
| `file_system_flat.kara` | no tree: a `Map` from each file's full path to its content and a `Set` of every directory's full path; `ls` scans both for the paths one level down and sorts them; O(every path) for `ls` |
| `file_system_arena.kara` | every node an entry in one `Vec`, each directory's `SortedMap` mapping names to indices; O(path length) |
| `differential.kara` | the four arms against the definition, five properties |

The harness runs a list of commands on a new file system and prints what
`ls` and `read` return. Every arm prints the same 11 lines: eight
scripts at the edges (the LeetCode example, an empty root, a file at the
root, a file listed by its own path, content added twice, entries in
order whatever order they were made in, a deep path made at once, and
directories and files side by side), a count and checksum over
300 random scripts of 1 to 40 commands, and the problem's largest,
300 commands, over ten names three deep and over two names up to
30 deep. The random scripts list and read only paths they have made and
never make a directory where a file is or the reverse, so they stay
within what the problem allows. `file_system.py` mirrors the ★ arm and
its output is byte-identical.

The owned arm does not build today; see Compiler findings. It is kept as
written. A copy outside this directory prints the same output; it
differs from the arm in four places: the recursion's argument passed
without its `mut` marker; the path's names kept as `String`s, cloned
from `split`, in place of `Str`s; `keys().iter().cloned()` in place of
`keys().cloned()`; and, in place of `find`, which walks a `ref` local
down the tree and returns it, two recursions, one for `ls` and one for
`read`, each answering at the node it reaches.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: a history of every `mkdir` and add in
order; a read joins every add to that path, in order; and `ls` gives a
file's own name, or else the next name below the path of every path in
the history that starts with it, each once, sorted. Each arm's output is
held to the properties below on 1,000 random scripts of 1 to 30 commands
over two or three names, up to three deep.

| | property |
|---|---|
| P1 | the output is the definition's |
| P2 | one line for each `ls` and read, every listing sorted with no name twice |
| P3 | every `mkdir` done twice gives the same output |
| P4 | every directory above an added file made first gives the same output |
| P5 | every content of two or more letters added a letter at a time gives the same output |

Since the owned arm does not build, the differential does not either.
Its definition also reads `*path` in three comparisons, twice `h.0 ==
*path` and once `*path == "/"`, as the spec spells a comparison through
a reference; `karac check` refused those until kara B-2026-10-14-27 was
fixed (`1be6eb5497`), while both MIR backends always ran them. A copy
outside this directory that holds the owned arm's workaround copy prints
`1000 cases, 4 arms, 20000 checks, 0 failures` under `karac __mir-run`
and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`. Rechecked at kara `7adae1f0aa`: that copy now passes
`karac check`, and the differential as written is refused only in its
copy of the owned arm.

## Mutation testing

Twelve edits to the workaround copy of the differential, two to each arm
that change its output and one to each that does not, each run under
`karac __mir-llvm-run`. All eight that change output are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: files left out of a listing | P1 668 |
| M2 | ★: a file never marked as one | P1 512 |
| M3 | owned: a file's content replaced, not added to | P1 121, P5 378 |
| M4 | owned: only the first name of a path kept | P1 771 |
| M5 | flat: the listing not sorted | P1 463, P2 463 |
| M6 | flat: the last directory of a path not made | P1 567 |
| M7 | arena: a new entry filed under its parent's index | P1 875 |
| M8 | arena: the listing reversed | P1 666, P2 666 |
| E1 | ★: the two tests the other way round | 0 |
| E2 | owned: an empty name found by its length | 0 |
| E3 | flat: repeats removed from the listing | 0 |
| E4 | arena: a missing name found with `get` | 0 |

M3 fails P5 more often than P1: its replaced content shows in P1 only
when a script adds to a file twice and then reads it, while P5 splits
every longer content into adds of one letter, so the file keeps only the
last. P3 and P4 see no mutant. They are there for an arm that empties a
directory made again, or that treats a directory differently when it was
made before a file below it; the first mutant written that way, a
directory emptied when it is made again, made a later read look for a
file that was gone, and that arm panicked rather than answering, so it
was replaced by M1. E3 changes nothing because no name is listed twice
to begin with.

## Verification

The ★, flat and arena arms print the same output as `file_system.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. `karac check` passes on those three and on the bench program; it
refuses the owned arm and the differential, and so do both MIR backends.
The workaround copy of the owned arm prints the same output under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`. The `--mir` builds and the timings below are at kara
`f6052c659c`; `karac check` and `karac __mir-run` at `8139c5e826`.

The frozen legacy backends refuse every arm, the differential and the
bench program under `karac run --interp`, `karac run` and `karac build`.
The ★ and arena arms stop at type checking on the harness's checksum,
which reads each byte of `as_bytes()` as `*b` where legacy gives the
byte itself ("unary '*' requires 'ref T' ... found 'u8'"); the flat arm
stops comparing a slice of a path with `"/"` ("cannot compare
'StringSlice' and 'String'"); the owned arm and the differential stop at
the `mut` marker, as on every backend; and the bench program passes type
checking but legacy codegen has no handler for `split` on a path. Legacy
is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 200 random scripts of
300 commands once (the problem's most), directories named `a` to `e` and
files `f` to `j` so no path is ever both, listing and reading only paths
already made; then 200 times over each script is run on a new file
system, and the length of every name listed and every content read is
folded into a checksum. Every implementation prints `200 scripts of
300 commands, 200 rounds: 4760200 answers, checksum 153088437`, the Kāra
program under `karac __mir-run` included (195 s).

Rust keeps each node in an `Rc<RefCell<..>>`, as a Kāra `shared struct`
is a counted handle, and its entries in a `BTreeMap`, as the Kāra arm
keeps them in a `SortedMap`. C has no sorted map, so each directory
keeps an array of entries sorted by name, found by binary search and
grown by insertion, and each file system is freed whole after its
script. Go and Python keep each directory's entries in a hash map and
sort them when they are listed. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 2.25 to 2.38 s |
| Rust (`rustc -O`) | 3.05 to 3.25 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.96 to 3.33 s |
| Go | 3.93 to 4.33 s |
| Python | 9.2 to 9.5 s |
| Kāra (`karac build --mir`) | 5.55 to 5.69 s |

So `bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 24.7 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

Re-timed on 2026-10-14 at kara `2d241d9b05`. The row first published
here, 6.54 to 7.93 s, was taken with a runtime archive older than kara
`8969be0434`, which runs `main` on a second thread, and once a process
has two threads glibc's `malloc` and `free` take a lock on every call.
Linked against that older runtime and against the current one by the
same compiler, three runs each, the program takes 6.49 to 6.53 and
5.83 to 6.09 s: the older runtime alone costs this program about 8%.

The Kāra row is about 1.8 times Rust's and 1.4 times Go's. Where the gap
comes from is not measured.

## Compiler findings

The owned arm meets four open kara rows. Its recursion `make(mut child,
names[1..], content)`, where `child` is the `mut ref` that
`entry(..).or_insert(..)` returns, is refused by `karac check` and both
MIR backends with "this argument is already a mut-ref; drop the `mut`
marker", though design.md § Call-site `mut` markers requires the marker
whatever the argument's root (B-2026-10-14-25, filed from this kata).
Its `find` walks a `ref` local down from `ref self.root` and returns it,
which `karac check` refuses with "returned borrow does not originate
from a `ref` parameter" and the MIR backends cannot lower, since `ref`
on a field is not built (B-2026-10-14-26, filed from this kata). It
keeps a path's names as `Str`s, and `split` gives `String`s, not the
`Str` slices the spec gives (B-2026-10-12-7), so `names.push(name)` is
refused with "expected 'StringSlice', found 'String'". And
`node.children.keys().cloned()` is refused because `keys()` gives a
`Vec`, not an iterator (B-2026-10-13-1). The arm keeps the spec's
spelling everywhere.

The differential's definition compares with `*path`, a `ref String` from
matching a borrowed `Op`, as design.md § `*` and `ref` in expressions
prescribes. `karac check` refused it with `borrow_projection_copy` and
accepted the unstarred form the spec calls a type error, while both MIR
backends ran it (B-2026-10-14-27, filed from this kata, fixed in kara
`1be6eb5497`; rechecked at `7adae1f0aa`).

Not filed: the ★, owned and arena arms index a directory's
`SortedMap[String, ..]` with a name from `split`. Today that name is a
`String`. Once `split` gives `Str`s as the spec says, the index needs a
`Str` key, which `karac check` refuses today ("expected 'String', found
'Str'"); docs/library/collections.md gives `m[key]` through `Index` and
does not say whether a `Str` may index a map keyed by `String`. The
legacy failures above are not filed because legacy is frozen.
