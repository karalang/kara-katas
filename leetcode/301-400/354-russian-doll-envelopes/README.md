# 354. Russian Doll Envelopes

Each envelope is a pair `(width, height)`. One envelope fits inside another
when it is strictly narrower **and** strictly shorter. Return the largest
number of envelopes that can be nested one inside the next. Envelopes cannot
be rotated.

```
[[5,4],[6,4],[6,7],[2,3]]  ->  3     (2,3) inside (5,4) inside (6,7)
[[1,1],[1,1],[1,1]]        ->  1
```

**Constraints:** `1 <= envelopes.length <= 10^5`; `1 <= w, h <= 10^5`.

## Approaches

| file | mechanism | cost |
|---|---|---|
| `russian_doll.kara` ★ | sort by width ascending and, at equal width, height **descending**; then the answer is the longest strictly increasing run of heights, found by patience sorting (`tails[k]` is the smallest height ending a run of length `k + 1`, updated by a hand-written binary search) | `O(n log n)` |
| `russian_doll_dp.kara` | sort by `(width, height)` and let `best[i]` be one more than the best chain ending at any envelope that fits inside envelope `i` | `O(n^2)` |
| `russian_doll_fenwick.kara` | renumber the heights, then walk the envelopes one width at a time with a Fenwick tree of prefix maxima over height ranks; each width group reads all its answers before writing any, so no tie-break is needed | `O(n log n)` |
| `russian_doll_typed.kara` | an `Envelope` struct with derived equality and a hand-written `Ord` that carries the nesting order, and a generic `lower_bound[T: Ord]` | `O(n log n)` |
| `differential.kara` | the four arms and an independent oracle, 42,323 checks, five properties | — |

Every arm prints the same 10 lines: both LeetCode examples, seven edge cases
(one envelope, four of the same width, three of the same height, a clean chain
given forwards and backwards, a wide-but-short envelope that blocks nothing,
and a width tie that has to break the chain), and 3,000 random envelopes with
sides in `1..=1500`, which the `O(n^2)` arm has to finish under the
interpreter. `russian_doll.py` mirrors the ★ arm and its output is
byte-identical.

The descending tie-break is the whole trick. Sorted by height ascending
within a width, `(3,1) (3,2) (3,3)` would read as a run of three, although no
two of them nest.

## Differential

`differential.kara` holds copies of the four arms and an oracle that shares
no code with them: no sorting at all, just the longest chain in the "fits
inside" relation, by memoised recursion over every pair. 3,000 random sets of
0 to 12 envelopes, with sides drawn from `1..=3`, `1..=6` or `1..=20` so that
equal widths, equal heights and duplicates are all common.

| | property |
|---|---|
| P1 | every arm returns the oracle's answer |
| P2 | the answer is 0 for no envelopes, else between 1 and the number of distinct widths and of distinct heights |
| P3 | reversing or rotating the input does not change the answer |
| P4 | swapping every envelope's width and height does not change the answer |
| P5 | adding one envelope raises the answer by 0 or 1, never lowers it |

It prints `failures 0` with `42323 checks, checksum 840485200` and the answer
histogram `0x231 1x606 2x1325 3x593 4x194 5x46 6x5` on every surface. An
independent Python replay of the random sets and the oracle gives the same
check count, checksum and histogram.

## Mutation testing

Eleven edits to the copies inside `differential.kara`, each built and run.
All eleven are killed.

| # | mutation | how |
|---|---|---|
| M1 | patience: `<=` for `<` in the binary search | P1 and P3, 3692 failures |
| M2 | patience: break width ties by height ascending | P1 and P3, 2124 failures |
| M3 | DP: let an equal width fit inside | P1 and P4, 2089 failures |
| M4 | DP: never record the best chain | P1 and P4, 5538 failures |
| M5 | Fenwick: query the prefix up to the same rank | P1 and P3, 2054 failures |
| M6 | Fenwick: one envelope per width group | P1 and P3, 2124 failures |
| M7 | Fenwick: keep the smaller value when raising | P1 and P3, 4326 failures |
| M8 | typed: order equal widths by height ascending | P1, 1062 failures |
| M9 | typed: an upper bound in place of the lower bound | P1, 1846 failures |
| M10 | oracle: let an equal height fit inside | P1 to P4, 7796 failures |
| M11 | oracle: a lone envelope is a chain of 0 | P1 to P4, 19989 failures |

## Verification

All four arms and the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build`, and the four arms match
`russian_doll.py` byte for byte. The bench program prints `912696348` under
LLJIT and both builds, as do its C, Rust, Go and Python mirrors. Built at
`-O0` with `KARAC_AUTO_PAR=0`, the four arms free every block and the bench
program loses none; it ends with 6.4 MB "still reachable", which is the
runtime's recycling cache for buffers of 1 MiB and more
(`runtime/src/alloc.rs`), not a leak. The differential is not: it loses one byte per zero-length
table, 924 blocks in all, from **B-2026-10-06-111** below. The typed arm
needs kara at or after the **B-2026-10-06-108** fix; older compilers refuse
it at type-check. The differential takes about a minute under
`karac run --interp` on a debug build.

## Benchmarks

`bench/russian_doll.kara` and its four mirrors time the ★ arm's algorithm:
sort by width ascending and height descending, then a patience-sorting
longest increasing subsequence over the heights. Each of 20 rounds draws
200,000 envelopes from a linear congruential generator seeded by the round,
with sides in `1..=100000`, and folds the answer into the sink, so no round
can be skipped or hoisted.

### Apple M5 Pro, 2026-11-06

30 runs each, 5 warmups, on the Apple M5 Pro, karac `0.8.0-dev.14606+g162ee7a0e`
(g162ee7a0e, the v2/MIR backend), measured 2026-11-06, with the Kāra binary built
`KARAC_AUTO_PAR=0`. Python was not run on this host, and this kata has
no Python timing on any host. The last column is Kāra's mean over that row's mean.

| implementation | mean | Kāra / this |
|---|---|---|
| rust `-O` | 127.0 ms ± 4.0 | 2.05× |
| rust `-O -C overflow-checks=on` (equal-safety) | 127.3 ms ± 3.9 | 2.04× |
| **kāra `karac build`, seq** | **260.2 ms ± 6.9** | **—** |
| c `clang -O3` | 355.3 ms ± 6.1 | 0.73× |
| go `go build` | 2317 ms ± 26 | 0.11× |

Kāra is 2.05× `rustc -O` and 2.04× equal-safety Rust, and ahead of C (0.73×) and
Go (0.11×). Against the legacy backend (exact counts, dd86e3955,
`KARAC_AUTO_PAR=0`) Kāra executes 0.81× the instructions but takes 1.46× the
cycles (see Bug ledger). The Rust gap was not investigated. The mirrors do not
sort the same way: Kāra and Rust call `sort_by` with a closure, C calls `qsort`
with a comparator function, and Go calls `sort.SliceStable`, an in-place stable
merge whose swaps go through a reflection-based swapper. That is the likeliest
source of Go's 8.9×, but it was not measured.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 45.2 ms ± 1.8 | 32.8 KiB | 7.2 MiB |
| rust | 127.2 ms ± 5.4 | 472.5 KiB | 14.6 MiB |
| kāra | 138.3 ms ± 2.4 | 67.0 KiB | 12.5 MiB |
| go | — | 2451.9 KiB | 19.8 MiB |

`karac build` is 3.1× clang's cold compile and 1.1× rustc's. Kāra's binary
is 2.0× clang's and 7.1× smaller than rustc's. Raw numbers are in
[`bench/results.json`](bench/results.json). The sink matches across the Kāra,
Rust, C and Go builds (`912696348`).

## Compiler findings

- **B-2026-10-06-108 (fixed in kara, typecheck): a derived supertrait did
  not satisfy a hand-written trait impl.** `#[derive(PartialEq, Eq)]` on
  `Envelope` beside a hand-written `impl PartialOrd` and `impl Ord` was
  refused with "impl PartialOrd for Envelope requires impl PartialEq". Fixed in kara `4c67adb10`.
- **B-2026-10-06-109 (open, high, interp + codegen): `sort()`,
  `is_sorted()`, `binary_search()`, `SortedSet` and `SortedMap` ignore a
  hand-written `impl Ord`** and order by the fields instead, on every
  surface. The typed arm's natural `order.sort()` returned 4 for four
  envelopes of one width, identically under the interpreter, the JIT and
  `karac build`, so no run/build comparison could see it; only the oracle
  did. The arm calls `order.sort_by(|a, b| a.cmp(b))` instead, with a comment
  to go back to `order.sort()` once the row is fixed.
- **B-2026-10-06-110 (open, codegen): indexing a collection literal fails
  `karac build`.** The differential's `[3, 6, 20][case % 3]` is refused with
  "Index operator applied to non-array type", for `vec![..]` and `Vec[..]`
  literals as well. It indexes a `let`-bound table instead, with a comment
  to revert.
- **B-2026-10-06-111 (open, codegen): `vec![x; 0]` leaks a one-byte
  buffer.** See Verification.
- **B-2026-10-06-113 (fixed in kara, interp): `--interp` ignored an enum's
  hand-written `impl Ord` for `.cmp()` and `<`.** An enum version of
  `Envelope`'s order printed `Small < Large` as true under the interpreter
  and false compiled. Fixed in kara `8eaf5220e`.
- **B-2026-10-06-112 (fixed in kara `b659d03377`, resolve): a hand-written `impl Clone`,
  `impl Default` or `impl Copy` is refused as an undefined type.** Found
  while trying every way to give `Envelope` its traits; the derives work.

The author already knows the language, so none of this counts toward the
machine-fix rate.

## Bug ledger

**Surfaced [`B-2026-11-06-1`](../../../../kara/docs/bugs-v2.md)** (perf, low, fixed in kara `d70e6d474a`). Against legacy dd86e3955 (`KARAC_AUTO_PAR=0`), kata 354 executes 0.81× the instructions in 1.46× the cycles, on karac g162ee7a0e (2026-11-06); it runs 2.05× `rustc -O`. The fix lowers an integer `cmp` as one three-way compare, so the comparator no longer branches on the less test in the sort's partition loop: on the M5, 0.954× legacy's cycles; on x86, 0.53 s against `rustc -O`'s 0.52 s.

**Surfaced [`B-2026-11-06-8`](../../../../kara/docs/bugs-v2.md)** (perf, low, open). After that fix, kata 354 on the M5 still runs 1.36× `rustc -O`'s cycles (757.1M against 556.6M, kara 4471044a8a), though it is level with Rust on x86.
