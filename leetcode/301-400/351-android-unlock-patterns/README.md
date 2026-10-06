# 351. Android Unlock Patterns

The keys of an Android lock screen form a 3x3 grid:

```
1 2 3
4 5 6
7 8 9
```

A pattern joins at least `m` and at most `n` distinct keys. The line from
one key to the next may pass over a third key only if that key is already in
the pattern: `1 -> 3` needs `2` first and `1 -> 9` needs `5` first. A move
like `1 -> 6` passes between keys, not over one, so it is always allowed.
Count the patterns.

```
m = 1, n = 1  ->  9
m = 1, n = 2  ->  65
```

**Constraints:** `1 <= m, n <= 9`. When `m > n` there are no patterns.

## Approaches

| file | mechanism | cost |
|---|---|---|
| `unlock_patterns.kara` ★ | a table of the key each line passes over, and a depth-first search that counts every pattern whose length is in `m..=n`; the four corners start equally many patterns, and so do the four edges, so the search runs from `1`, `2` and `5` only, weighted 4, 4 and 1 | `O(9!)` worst case, `O(9)` space |
| `unlock_patterns_geometry.kara` | no table: the key passed over is the midpoint of the two keys' positions, when both coordinate sums are even; the search runs from all nine keys | `O(9!)` worst case |
| `unlock_patterns_bitmask_dp.kara` | dynamic programming over (keys used as a 9-bit mask, last key); a pattern's length is its mask's population count | `O(2^9 * 9 * 9)`, whatever `m` and `n` are |
| `unlock_patterns_stack.kara` | the star arm's search without recursion: an explicit stack of the path and the last key tried at each depth, the used keys as a bitmask | `O(9!)` worst case |
| `differential.kara` | the four arms and an independent oracle, 328 checks, six properties | — |
| `bench/unlock_patterns.kara` | the ★ arm on all 81 `(m, n)` pairs, 48 times | — |

Every arm prints the same 16 lines: the two examples, the count for each
length from 1 to 9 and their sum, every pattern (`m = 1, n = 9`, 389,497),
the classic lock screen's at least four keys (`m = 4, n = 9`, 389,112), a
middle range, and `m > n`. `unlock_patterns.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and an oracle that shares
no code with them. The oracle allows a move from `a` to `b` when every grid
point strictly inside the segment is a visited key, finding those points
with a `gcd` of the coordinate differences rather than from a table or a
midpoint rule. It searches from every key and records the count for each
start key and length.

| | property |
|---|---|
| P1 | all four arms equal the oracle on every length 1..=9 on its own |
| P2 | every arm's count for `(m, n)` is the sum of the oracle's lengths `m..=n`, for every `m <= n` with `n <= 6`, and for `(1, 9)` and `(4, 9)` |
| P3 | every arm gives 0 for each of the 36 pairs with `m > n` |
| P4 | the oracle counts the same patterns from all four corners, and from all four edges, at every length |
| P5 | there are as many 9-key patterns as 8-key ones: the last key left can always be reached, since any key a line to it passes over is already in the pattern |
| P6 | the oracle's 2-key count is the number of ordered pairs of keys whose line passes over no key, counted directly from their coordinates: 56 |

It prints `failures 0` and all properties hold on every surface, with
`328 checks: 389497 patterns in all, checksum 977748243`. An independent
Python replay, which enumerates every ordered sequence of distinct keys with
`itertools.permutations` and validates each one whole, gives the same total
and checksum.

P2 stops at `n = 6` apart from two pairs because the interpreter is the
slowest surface and the arms without the symmetry search all nine starts:
the full 81 pairs took 6.5 minutes under `karac run --interp`.

## Mutation testing

Thirteen edits to the copies inside `differential.kara`, each run under
`karac run`. All thirteen are killed.

| # | mutation | how |
|---|---|---|
| M1 | table: weight the centre 4 instead of 1 | P1 and P2, 32 failures |
| M2 | table: count a pattern only when its length is greater than `m` | P1 and P2, 32 failures |
| M3 | table: do not unmark a key when the search backs out of it | P1 and P2, 30 failures |
| M4 | geometry: a line passes over a key when either coordinate sum is even | P1 and P2, 30 failures |
| M5 | geometry: the midpoint's key number is one too small | P1 and P2, 30 failures |
| M6 | dp: count each mask one length short | P1 and P2, 31 failures |
| M7 | dp: require the key passed over to be unused | P1 and P2, 29 failures |
| M8 | dp: sum lengths `m..n`, dropping `n` | P1 and P2, 32 failures |
| M9 | stack: keep a key marked used after backing out of it | P1 and P2, 30 failures |
| M10 | stack: count a pattern only when its depth is greater than `m` | P1 and P2, 24 failures |
| M11 | stack: extend a pattern that already has `n` keys | P1 and P2, 29 failures |
| M12 | oracle: the larger coordinate difference instead of the `gcd` | P1, P2 and P6, 121 failures |
| M13 | line table: drop the `3 -> 7` diagonal | P1 and P2, 87 failures |

P3, P4 and P5 kill none of them. P3 checks the `m > n` early return, which
no mutant touches. P4 and P5 check the oracle, which only M12 changes, and
both still hold under it.

## Verification

All four arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build` (`scripts/surface-sweep.py`, 5
programs, 0 divergences), and the four arms match `unlock_patterns.py` byte
for byte. Built with `KARAC_AUTO_PAR=0`, all five are valgrind-clean:
`0 errors` and `0 bytes in use at exit`. The differential takes 2 minutes
53 seconds under `karac run --interp`, measured while a compiler build shared
the machine.

## Benchmarks

`bench/unlock_patterns.kara` and its four mirrors time the ★ arm as written:
48 rounds, each counting the patterns for all 81 `(m, n)` pairs the
constraints allow, `m > n` included. Every count is folded into the sink with
its round, so no call can be skipped or hoisted; all five print
`sink 701253957`. Each mirror builds its line table and its visited flags on
every call, as the Kāra arm does.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each, 5 warmups, on a 4-core x86-64 Linux container, karac
`0.1.0-dev.10502+ga703616a1` (kara main at the B-2026-10-05-108 fix),
measured 2026-10-06, with the timed lane built with `KARAC_AUTO_PAR=0`.
Python is its own lane at 3 runs.

| implementation | mean | vs fastest |
|---|---|---|
| c `clang -O3` | 918 ms ± 13 | 1.00× |
| c `-march=x86-64-v3` (matched-ISA) | 926 ms ± 22 | 1.01× |
| rust `-O` | 1017 ms ± 22 | 1.11× |
| rust `-O -C overflow-checks=on` (equal-safety) | 1051 ms ± 18 | 1.14× |
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 1058 ms ± 31 | 1.15× |
| go `go build` | 1490 ms ± 24 | 1.62× |
| **kāra `karac build`** | **1530 ms ± 21** | **1.67×** |
| python 3 | 37133 ms ± 1805 | 40.4× |

**Kāra is 1.46× behind equal-safety Rust and 1.67× behind C, level with Go.**
That is a wider gap than the hash-table katas just before it (#349 was 1.35×
behind equal-safety Rust, #350 1.18×). This bench is almost nothing but a
recursive search that indexes two small `Vec`s passed by reference, so the
cost is per call and per index. Where the extra half goes was not
investigated. Python is 40× behind here because the work is all interpreted
recursion, with no C-implemented container to lean on.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 95.0 ms ± 3.0 | 15.8 KiB | 1.5 MiB |
| rust | 161.7 ms ± 40.9 | 3864.3 KiB | 2.1 MiB |
| kāra | 440.9 ms ± 16.1 | 341.6 KiB | 2.4 MiB |
| go | — | 2179.0 KiB | 3.7 MiB |
| python | — | — | 7.8 MiB |

`karac build` is 4.6× clang's cold compile and 2.7× rustc's. Its binary is
22× clang's and 11× smaller than rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

Probing the other ways to write this kata turned up three gaps in the
compiler, fixed in the kara repo, and a fourth, filed there. All of them came
from one natural idea: the table of which key each line passes over is a
constant, so it could be a module-level `const` or `let` instead of a
function that builds a `Vec`. The arms keep the function, which every
surface runs.

- **B-2026-10-06-41 (typecheck): a `const` declared as a fixed array was
  refused.** `const LINES: Array[(i64, i64, i64), 8] = [(1, 3, 2), ...];`
  failed with "expected 'Array[(i64, i64, i64), 8]', found 'Vec[...]'" on
  every surface, while the same annotation on a `let` was accepted. The
  const's literal was inferred before its annotation was consulted, so it
  always took the `Vec` form. It now takes the form the annotation names.
- **B-2026-10-06-40 (typecheck): `.len()` on an array of tuples was refused.**
  `LINES.len()` failed with "no method 'len' on type 'Array'" because `len`
  and `is_empty` sat behind the gate for methods that read elements, which
  holds only for arrays of numbers, `bool` and `char`. Neither reads an
  element, and both now work for every element type.
- **B-2026-10-06-42 (typecheck and codegen): a module-level `Vec` literal was
  miscompiled.** `let NUMS: Vec[i64] = [1, 2, 3];` at module scope ran under
  `karac run --interp`, but the built binary panicked "vec index out of
  bounds" on `NUMS[2]` and segfaulted on `for x in NUMS`. The language
  forbids heap data in a module binding, so the compiler now refuses it and
  offers `Array[i64, 3]` as a fix.
- **B-2026-10-06-43 (codegen, open): a `const` or module-level `Array` used
  directly fails to build.** With the first fix in place, a `const` array
  used directly as an index base, a `.len()` receiver or a `for` iterable
  runs under `karac run --interp`, but `karac build` stops with a codegen
  error on each. A `const` `Vec` fails the same way, and so do a module-level
  `let` array's `len` and `for` (its index works). Copying the constant into
  a local first builds. The arms use neither form.

The author already knows the language, so none of this counts toward the
machine-fix rate.
