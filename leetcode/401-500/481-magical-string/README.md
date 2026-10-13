# 481. Magical String

A magical string `s` consists of only `'1'` and `'2'` and obeys the
following rule: concatenating the number of contiguous occurrences of
the characters `'1'` and `'2'` generates the string `s` itself.

The first few elements of `s` are `s = "1221121221221121122……"`. If we
group the consecutive 1s and 2s in `s`, it will be `"1 22 11 2 1 22 1
22 11 2 11 22 ......"` and the occurrences of 1s or 2s in each group
are `"1 2 2 1 1 2 1 2 2 1 2 2 ......"`. You can see that the occurrence
sequence is `s` itself.

Given an integer `n`, return the number of 1s in the first `n` numbers
in the magical string `s`.

```
n = 6  ->  3     (the first six are "122112")
n = 1  ->  1
```

**Constraints:** `1 <= n <= 10^5`.

## Approaches

Every arm is `fn magical_string(n: i64) -> i64`. The string is the
Kolakoski sequence: its runs alternate between 1s and 2s, starting with
1s, and the `j`-th run is as long as the `j`-th digit says.

| file | mechanism |
|---|---|
| `magical_string.kara` ★ | the digits in a `Vec`, started as 1, 2, 2; a read position walks behind the end, and each digit it reads appends a run that long of the other digit; then the 1s among the first `n` are counted. O(n) time and memory |
| `magical_string_queue.kara` | only the digits written and not yet read, in a `VecDeque`: each run's length is popped from the front and the run pushed on the back, and the 1s are counted as they are written, up to `n` |
| `magical_string_levels.kara` | a tower of readers, one `Level` (current digit, how much of its run is left) per level: from index 2 on, the string is its own run lengths, so each level takes a new run's length from the level above, which is a reader of the same kind. O(n) time, O(log n) memory |
| `magical_string_expand.kara` | the string as its own fixed point: reading a correct prefix as run lengths gives a longer one (`"122"` gives `"12211"`), so a `String` is expanded until it is `n` long and the 1s counted with `chars().take(n).filter(..).count()` |
| `differential.kara` | the four arms on 1,500 random `n`, three properties |

Every arm prints the same 7 lines: the two LeetCode examples, the counts
for `n` from 1 to 20, the first 60 digits read back from the counts (a
digit is 1 exactly where the count goes up), `n = 99999` and `n =
100000` (the problem's largest, 49972 both), and for 300 random `n`
(from 1 to 3,000, or to 100,000 for one case in fifty) the sum of the
counts and a checksum of them. `magical_string.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random `n` from 1 to 1,000, or from 1 to 20,000 for one case in
fifty. Its reference is the string built by the definition and then
checked against it: the runs read off its digits must alternate
starting with 1s and be as long as the digits say. Only one string
passes that, so the reference does not depend on being built right.

| | property |
|---|---|
| P1 | the count is the number of 1s among the reference's first `n` digits |
| P2 | the first `n` runs are `2n - count` digits long (each digit is a run of 1 or 2), and the arm's count of 1s among those digits is the sum of the run lengths at even positions, the runs of 1s |
| P3 | `n + 1` gives the same count or one more, and `n = 1` gives 1 |

P2 asks the arm about a second, longer prefix, and ties it to the first
by the rule that defines the string, so it holds for the true string
and fails for most others whatever the reference says.

It prints `1500 cases, 4 arms, 18000 checks, 0 failures` under
`karac __mir-run`, in about 52 s, and a count for each property when
anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: reading starts at index 1 | P1 1029, P2 1069 |
| M2 | ★: the first digit is not counted | P1 1500, P2 736, P3 1500 |
| M3 | queue: the count runs one digit past `n` | P1 244, P2 123, P3 266 |
| M4 | queue: the runs start with 2s | P1 1144, P2 1133 |
| M5 | levels: a new level starts with both 2s of its run left | P1 1069, P2 1062 |
| M6 | levels: a run is 2 long where the length read is 1, and 1 where it is 2 | P1 1194, P2 1330 |
| M7 | expand: a 1 is written twice instead of a 2 | P1 1254, P2 1298, P3 2 |
| M8 | expand: the expansion stops while the text is one short of `n` | P1 7, P2 5, P3 4 |

M1, M4, M5 and M6 each build some other string of 1s and 2s that starts
with a 1, so P3, which only looks at the steps, never sees them; P1 and
P2 see them on about two cases in three. M8 is the subtle one: an
expansion is about half as long again each time (3, 5, 7, 10, 15, 23,
34, ..., 75, 113, 170, 255, ...), so it matters only when `n` is one
more than one of those lengths and the missing last digit is a 1, which
is 16 checks in 18,000; the failures it prints first are at `n` = 76
and 256, one past 75 and 255. M3 is wrong only when the last run
written goes past `n` with a 1. Starting the expansion from `"12"`
instead of `"122"` would be an equivalent mutant, not tried as one:
`"12"` expands to `"122"`, so it only adds a round.

## Verification

All four arms print the same output as `magical_string.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file, the bench program included. The
differential prints `18000 checks, 0 failures` on both. The four arms
and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

The frozen legacy backends agree as well: `karac run --interp`, LLJIT,
legacy `karac build` and a `KARAC_AUTO_PAR=1` build print the same
output on every arm, and `0 failures` on the differential.

## Benchmarks

The bench program uses the ★ arm. It runs 1,000 rounds, with `n` from
100,000 (the problem's most) down to 99,001, and builds the string
afresh each round. Every implementation prints `1000 rounds of n =
99001 to 100000: 1s add up to 49721739, checksum 999036197`, the Kāra
program under `karac __mir-run` included (in 70 s).

Every mirror keeps the digits in a growable array of 64-bit integers
(Rust `Vec<i64>`, Go `[]int64` with `append`, a Python list, and in C an
array doubled with `realloc`) and runs the same loops. Spot timings on a
shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.20 to 0.22 s |
| Rust (`rustc -O`) | 0.23 to 0.25 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.27 to 0.33 s |
| Go | 2.41 to 2.48 s |
| Python | 12.4 to 13.1 s |
| Kāra (`karac build`) | 1.03 to 1.28 s |
| Kāra (`karac build --mir`) | 0.38 to 0.46 s |

Go is ten times slower than C here, and it is not the collector: with
`GOGC=off` it takes 3.1 s. Where the time goes was not profiled. The
legacy `karac build` builds and runs this program correctly, so
`bench.sh` is the `scripts/new-bench.sh` output unchanged and times
that build. The `--mir` row is the v2 compiled backend, timed for
comparison, and is between two and three times faster than the legacy
build on this program. Both Kāra rows are timed at kara `b0b1557b39`.
Under `karac __mir-llvm-run` the program prints the same line in 1.3 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

None. Every arm, the differential and the bench program ran first time
on every backend.
