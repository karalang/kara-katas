# 533. Lonely Pixel II

Given an `m x n` `picture` consisting of black `'B'` and white `'W'`
pixels and an integer `target`, return the number of black lonely
pixels. A black lonely pixel is a character `'B'` located at a
specific position `(r, c)` where:

- row `r` and column `c` both contain exactly `target` black pixels;
- for all rows that have a black pixel at column `c`, they should be
  exactly the same as row `r`.

```
picture = WBWBBW    target = 3  ->  6
          WBWBBW
          WBWBBW
          WWBWBW

picture = WWB       target = 1  ->  0
          WWB
          WWB
```

**Constraints:** `1 <= m, n <= 200`; `picture[i][j]` is `'W'` or
`'B'`; `1 <= target <= min(m, n)`.

## Approaches

Every arm is `fn find_black_pixel(picture: Vec[Vec[char]], target:
i64) -> i64`. Lonely pixels come in whole columns: when one pixel of a
column is lonely, all `target` of them are.

| file | mechanism |
|---|---|
| `find_black_pixel.kara` ★ | count each row, written as a `String`, in a `Map`, and each column; a row with `target` black pixels that occurs exactly `target` times answers `target` for every column where it is black and the column holds `target`; O(mn) |
| `find_black_pixel_brute.kara` | the rule as written: for each black pixel, count its row and column and compare every row black in its column with its own |
| `find_black_pixel_columns.kara` | column by column: a column holding `target` passes when its first black row holds `target` and every other black row equals it |
| `find_black_pixel_ids.kara` | no hashing: the rows sorted by content and each run of equal rows given one number, so a column compares numbers instead of rows |
| `differential.kara` | the four arms against a definition by sets, five properties |

The ids arm sorts with `picture[a].cmp(picture[b])`, which design.md
allows (`impl[T: Ord] Ord for Vec[T]`). `karac check` refused it ("no
method 'cmp' on type 'Vec'") until kara B-2026-10-06-92 was fixed in
`d3f7020d95`; the arm and the differential kept that spelling, and both
now run as written.

Every arm prints the same 9 lines: both examples, one black and one
white pixel, two different rows that share a column, two equal rows,
and three rows with the right counts that differ; then for 300 random
pictures the lonely pixels in all, how many have none and a checksum;
and last the largest case. A random picture plants rows with exactly
`target` black pixels, each written `target` times (a quarter of the
time once more), adds rows of random pixels, and shuffles them, since
pictures of random pixels almost never hold a lonely one. The 300 are
1 to 20 wide for a target from 1 to 4; the largest is 200 wide with
20 planted rows for a target of 5 and 80 more rows, 186 in all.
`find_black_pixel.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and a definition by
sets: a black pixel is lonely when its row and its column each hold
`target` black pixels and the rows black in its column, written as
strings, form a `SortedSet` of one. Each arm is held to the properties
below on 1,000 random pictures 1 to 10 wide, for a target from 1 to
3. They are made like the harness's, with two kinds of near miss: a
quarter of the planted rows have one black pixel fewer than `target`,
and one copy in three has a black pixel moved to another column.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the rows in a shuffled order give the same answer |
| P3 | the columns in a shuffled order, the same in every row, give the same answer |
| P4 | the answer is a multiple of `target`, and at most the number of black pixels |
| P5 | one more white row and one more white column give the same answer |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed. They were first run on a copy that
sorts the rows' `String`s, while B-2026-10-06-92 was open, and run again
on the differential as written once it was fixed, with the same counts.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a column with more than `target` black pixels accepted (`>=`) | P1 224 |
| M2 | ★: rows with more than `target` black pixels kept (`>=`) | P1 139 |
| M3 | brute: rows compared by their first pixel only | P1 145, P3 95, P4 73 |
| M4 | brute: the row's count never tested | P1 179 |
| M5 | columns: the first row's count never tested | P1 179 |
| M6 | columns: row 0 taken as the first black row | P1 188, P2 128 |
| M7 | ids: every row given the same number | P1 104 |
| M8 | ids: rows with fewer than `target` black pixels let through (`>`) | P1 40 |
| E1 | ★: a row written more than `target` times accepted (`<`) | 0 |
| E2 | brute: the column looked down from the bottom | 0 |
| E3 | columns: the rows compared the other way round | 0 |
| E4 | ids: the rows sorted in descending order | 0 |

E1 was first written as a mutant that should be killed. A row written
more than `target` times puts more than `target` black pixels in each
of its black columns, so the column test refuses it anyway; the ★ arm
needs only one of the two tests. M7 and M8 need the near misses: with
the harness's pictures alone they failed 12 and 7 checks, since equal
counts in a column almost always came from equal rows. M4 and M5 are
one mistake in two arms and fail the same 179 cases. P5 kills nothing:
a white row and column change no count and no comparison, so it is
there for an arm that indexes past the picture or confuses the two
sides, and none of these edits does.

## Verification

Every arm prints the same output as `find_black_pixel.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. The ids arm and the differential
were rechecked at kara `83fab1e1e8` (debug build) and `f5c72b653e`
(release build, for `check` and `__mir-run`), which differ in no `src`
or `runtime` file, after B-2026-10-06-92 was fixed; until then they
stopped at type checking, and copies that sorted the rows' `String`s
were checked instead.

On the frozen legacy backends, `karac run --interp` runs the brute and
columns arms and prints the mirror's output. LLJIT and legacy `karac
build` fail on those two at codegen, "no handler for method 'len' on
variable 'row' in `parse`", a `Str` in a slice's `iter()`. The ★ arm,
the bench program and the differential are refused at type checking:
legacy types the items of a `Map`'s and a slice's `iter()` by value, so
it refuses `*count` and `*ch` ("unary '*' requires 'ref T' ... found
'i64'"). The ids arm is refused there at `picture[a].cmp(picture[b])`
("no method 'cmp' on type 'Vec'"): the fix for B-2026-10-06-92 is on the
v2 pipelines only. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 pictures 200 wide (the
problem's most) once, the `p`-th with 20 rows planted for a target of
`1 + p % 8` and 80 more black with a chance of 1%; then it answers
each picture for every target from 1 to 8, in 100 rounds. Every
implementation prints `20 pictures 200 wide, targets 1 to 8, 100
rounds: total 192000, checksum 661658600`, the Kāra program under
`karac __mir-run` included (in 292 s).

Every mirror builds a key for every row and counts the keys in a
fresh map per call. Rust uses `HashMap<String, i64>` with its default
SipHash-1-3, the hasher Kāra's `Map` uses too; Go uses its built-in
map, Python a dict. C has no map, so its mirror copies each row into
a key buffer allocated at its full length and counts the keys in a
fresh open-addressing table with FNV-1a, a much cheaper hash; Kāra,
Rust and Go grow each key a `char` at a time. Spot timings on a
shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.38 to 0.39 s |
| Rust (`rustc -O`) | 1.29 to 1.53 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.39 to 1.62 s |
| Go | 3.44 to 3.59 s |
| Python | 29.6 to 30.0 s |
| Kāra (`karac build --mir`) | 1.44 to 1.60 s |

The legacy `karac build` refuses this program (see Verification). So
`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. The table was re-timed at kara
`7609de871d`, after B-2026-10-13-30 was fixed; the Python row is from
the first timing, at kara `21ffa33dff`.

The Kāra row is now level with Rust with overflow checks. It was 3.78
to 3.90 s at first, and most of that gap was the keys: pushing a `char`
onto a `String` was a call into the runtime for every char on the v2
compiled backend. A loop that builds 2,000,000 keys of 200 chars and
nothing else took 2.78 s under `karac build --mir` against 0.77 s for
Rust with overflow checks. Filed as kara B-2026-10-13-30, and fixed in
kara `16cbe03472`, which gives an ASCII `String.push` an inline path.

Under `karac __mir-llvm-run` the program prints the same line in
33.9 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

## Compiler findings

kara B-2026-10-06-92 (false-positive), filed from kata 49 and met again
here, fixed in kara `d3f7020d95`: `Vec[T: Ord]` was not `Ord` to the
type checker, though design.md declares `impl[T: Ord] Ord for Vec[T]`,
so `picture[a].cmp(picture[b])` was refused. It blocked the ids arm and
the differential under every `karac` command; both now run as written
(see Verification).

kara B-2026-10-13-30 (perf), filed from this kata and fixed in kara
`16cbe03472`: on the v2 compiled backend `String.push(c)` was an
out-of-line runtime call per char, through
`karac_mir_string_push_char`, `push_str` and `vec_reserve`, so a loop
that builds keys a `char` at a time ran 3.6 times slower than Rust's.
The bench now runs level with Rust's (see Benchmarks).
