# 346. Moving Average from Data Stream

Given a stream of integers and a window size, calculate the moving average of
all integers in the sliding window. `MovingAverage(size)` sets the window;
`next(val)` reads one value and returns the average of the last `size`
values, or of every value so far while fewer than `size` have arrived.

```
MovingAverage(3)
next(1)   ->  1.0       window [1]
next(10)  ->  5.5       window [1, 10]
next(3)   ->  4.66667   window [1, 10, 3]
next(5)   ->  6.0       window [10, 3, 5]
```

## Approaches

| file | mechanism | cost per `next` |
|---|---|---|
| `moving_average.kara` ★ | a `VecDeque` window and a running sum: push, add, and pop and subtract once full | `O(1)` time, `O(size)` space |
| `moving_average_ring.kara` | a `Vec` of exactly `size` slots allocated once; the slot about to be overwritten is the value leaving | `O(1)` time, `O(size)` space |
| `moving_average_prefix.kara` | prefix sums over the whole history; the window is a difference of two of them | `O(1)` time, `O(n)` space |
| `moving_average_naive.kara` | keep every value and add up the last `size` on each call | `O(size)` time, `O(n)` space |
| `moving_average_closure.kara` | no struct: a closure captures the window and the sum and mutates them | `O(1)` time, `O(size)` space |
| `differential.kara` | the five arms and a from-scratch oracle on 732 window/stream pairs, five properties | — |
| `bench/moving_average.kara` | 10,000,000 values through a window of 1,000, by the ★ arm | — |

Every arm prints the same 6 lines: the example, a window of one (the stream
itself), a window wider than the stream (nothing is ever dropped), negative
values, a mean that does not terminate in decimal (`1.33333`), and 100,000
values at the problem's bound of `|val| <= 100000` through a window of 1,000,
reported as the last average and the sum of all of them. Averages print with
`{a:.5}`. `moving_average.py` mirrors the ★ arm and its output is
byte-identical.

Every arm keeps the window's sum as an `i64` and divides once, so they agree
bit for bit rather than to a tolerance: the sum of at most 1,000 values of at
most 100,000 is exact, and one division of exact operands rounds the same way
everywhere. An arm that kept a running `f64` mean would drift, and the
differential would have to compare with an epsilon.

## Differential

`differential.kara` runs all five arms on every window size `1..12` against
every stream length `0..60`, 732 pairs, each stream filled pseudo-randomly
across `-100000..=100000`. It compares them with a sixth version, the oracle,
which for each position adds up the window from scratch out of the input.

| | property |
|---|---|
| P1 | all five arms equal the oracle exactly, bit for bit |
| P2 | every average lies between the smallest and largest value in its window |
| P3 | with a window at least as long as the stream, each average is the mean of everything so far |
| P4 | with a window of one, each average is the value just read |
| P5 | adding 7 to every value adds 7 to every average |

`failures 0` and all properties hold on every surface, and the sum of all the
averages it checks is `-5209717.0338`. An independent Python replay of the
input generator gives the same sum.

## Mutation testing

Eleven edits to the copies inside `differential.kara`, each run under
`karac run`. All eleven are killed.

| # | mutation | how |
|---|---|---|
| M1 | queue: trim at `>= size` | P1, 594 failures |
| M2 | queue: `pop_back` instead of `pop_front` | P1, 642 failures |
| M3 | ring: treat the ring as full one value early | P1 and P4, 22,614 failures |
| M4 | ring: advance the head by 2 | P1, 318 failures |
| M5 | ring: subtract the slot after the head | P1, 583 failures |
| M6 | prefix: divide by `n` instead of `k` | P1 and P5, 18,208 failures |
| M7 | prefix: cut over to the full window at `size - 1` | index out of bounds |
| M8 | naive: start the window one value late | P1, 583 failures |
| M9 | closure: trim at `size + 1` | P1, 642 failures |
| M10 | closure: divide by `size` before the window fills | P1, 660 failures |
| M11 | oracle: a window one value too long | P1, P2 and P5, 20,698 failures |

Two further edits survived because they change nothing: `n <= size` for
`n < size` in the prefix arm (at `n == size` both branches give `k = size`),
and wrapping the ring's head modulo `size + 1` before modulo `size` (the head
never reaches `size + 1`). They are equivalent mutants, not gaps in the
differential.

## Verification

All five arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build` (`scripts/surface-sweep.py`, 6
programs, 0 divergences). Built with `KARAC_AUTO_PAR=0`, all six are
valgrind-clean with `0 errors`.

The prefix and naive arms report one 1,048,576-byte block "still reachable"
at exit, and that is by design rather than a leak. Their history `Vec` grows
to 131,072 slots, 1 MiB, and the runtime parks a freed buffer of 1 MiB or
more in a recycling cache (`runtime/src/alloc.rs`, `BUF_CACHE_MIN_BYTES`) so
that the next large allocation reuses its pages. With `KARAC_BUF_CACHE=0`,
which turns the cache off, both report `0 bytes in use at exit`.

## Benchmarks

`bench/moving_average.kara` and its four mirrors time the ★ arm as written:
one moving average with a window of 1,000 reads 10,000,000 pseudo-random
values in `-100000..=100000`, and every average it returns is added to a
running total, the sink. The window fills after 1,000 values, so almost every
call pushes one value and pops one. Rust uses `std::collections::VecDeque`;
C and Go have no deque in their standard libraries, so they use a small
growable ring with a head index, which is the same algorithm.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each, 5 warmups, on a 4-core x86-64 Linux container, karac
`0.1.0-dev.10448+g76727438c`, measured 2026-10-05, with the timed lane built
with `KARAC_AUTO_PAR=0`. Python is its own lane at 3 runs.

| implementation | mean | vs fastest |
|---|---|---|
| rust `-O` | 34.2 ms ± 4.9 | 1.00× |
| rust `-O -C overflow-checks=on` (equal-safety) | 37.1 ms ± 4.1 | 1.09× |
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 37.6 ms ± 3.1 | 1.10× |
| c `clang -O3` | 80.6 ms ± 1.8 | 2.36× |
| c `-march=x86-64-v3` (matched-ISA) | 85.9 ms ± 20.6 | 2.51× |
| go `go build` | 119.0 ms ± 2.9 | 3.47× |
| **kāra `karac build`** | **685.5 ms ± 140.5** | **20.0×** |
| python 3 | 3837 ms ± 132 | 112× |

**Kāra is 20× behind Rust here, and the cause is a known gap in how
`VecDeque` is compiled (kara B-2026-10-05-79).**
A compiled `VecDeque` has the same three fields as a `Vec` (pointer, length,
capacity), so it has nowhere to record where its contents start, and
`pop_front` shifts every remaining element down one slot with a `memmove`.
The compiler does avoid that for a deque that is a plain local variable: it
keeps a hidden start index beside it, and `pop_front` costs nothing extra
(B-2026-07-30-5). The ★ arm's deque is a field of the `MovingAverage` struct,
which that rewrite does not cover. So every call here moves 999 values, and
callgrind puts 95% of the program's instructions in `memmove`.

The same loop with the window as a local `VecDeque` in `main` runs in 38 ms
against 631 ms for the struct version on the same build, and prints the same
sink. That puts it level with Rust, which supports the reading that the whole
gap is the `pop_front` lowering. The kata keeps the struct, because a window
held in a struct is how this problem is naturally written; the row stays open
until the compiler handles it. The C and Go gap to Rust (2.4× and 3.5×) was
not investigated.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 98.2 ms ± 5.7 | 15.7 KiB | 1.6 MiB |
| rust | 125.1 ms ± 2.4 | 3888.6 KiB | 2.2 MiB |
| kāra | 319.3 ms ± 13.3 | 361.6 KiB | 2.5 MiB |
| go | — | 2178.8 KiB | 1.8 MiB |
| python | — | — | 8.4 MiB |

`karac build` is 3.3× clang's cold compile and 2.6× rustc's. Its binary is
23× clang's and 11× smaller than rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

Writing this kata turned up two gaps in the compiler, both filed in the kara
repo's ledger. The diagnostics one is fixed; the performance one is open.

- **B-2026-10-05-78 (diagnostics): a closure written with a Rust-style
  return type got a parse error that named neither.** The closure arm's first
  draft was `let mut next = |val: i64| -> f64 { .. };`. `karac check` said
  "Expected expression, found Arrow", then "Expected expression, found
  Semicolon" at the closing `};`, twice over for the file's two closures. A
  Kāra closure declares no return type; the body gives it. The error now says
  that and names the `-> f64` to remove, and `karac fix` removes it.

- **B-2026-10-05-79 (perf, open): `pop_front` on a `VecDeque` held in a struct
  field moves the whole deque.** See Benchmarks above: the struct-held window
  runs 17× slower than the same loop over a local deque. The ★ arm is not
  changed to dodge it.

The author already knows the language, so none of this counts toward the
machine-fix rate.
