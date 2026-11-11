# 1114. Print in Order

Suppose we have a class:

```
public class Foo {
  public void first() { print("first"); }
  public void second() { print("second"); }
  public void third() { print("third"); }
}
```

The same instance of `Foo` will be passed to three different threads.
Thread A will call `first()`, thread B will call `second()`, and thread
C will call `third()`. Design a mechanism and modify the program to
ensure that `second()` is executed after `first()`, and `third()` is
executed after `second()`.

Note: we do not know how the threads will be scheduled in the operating
system, even though the numbers in the input seem to imply the
ordering. The input format you see is mainly to ensure our tests'
comprehensiveness.

```
nums = [1,2,3]  ->  "firstsecondthird"
nums = [1,3,2]  ->  "firstsecondthird"
```

**Constraints:** `nums` is a permutation of `[1, 2, 3]`.

The arms are a `Foo` with `fn new() -> Foo` and `fn first(self,
print_first: Fn())`, `fn second(self, print_second: Fn())` and `fn
third(self, print_third: Fn())`. LeetCode's threads are a `TaskGroup`
with a task per method, started in the order `nums` gives, and the
prints go to a log behind a `Mutex`.

## Approaches

| file | mechanism |
|---|---|
| `print_in_order.kara` ★ | two one-shot channels: `first` sends on the first once it has printed, `second` waits on it, prints and sends on the second, and `third` waits on that. A `recv` is a suspension point, so a waiting task lets the others run |
| `print_in_order_closed.kara` | a channel's close as the signal: `first` and `second` each hold the only `Sender` of a channel nothing is ever sent on, and drop it once they have printed; the next method's `recv` returns `None` as soon as that channel closes |
| `print_in_order_waitlist.kara` | a condition variable built from a `Mutex` and channels: the stage reached and a list of waiters sit under one lock; a method whose turn has not come puts a one-shot channel on the list and waits on it, and each method that finishes raises the stage and wakes every waiter whose turn it now is |
| `print_in_order_polling.kara` | an `Atomic` stage, and a waiting method that checks it and sleeps between checks for no time at all. The sleep is still a suspension point, so the method waiting lets the others run; a loop that only re-reads the stage would not, and core-semantics.md §11.1 does not promise it ever ends |
| `print_in_order_rust.kara` | two channels as Rust writes them with `std::sync::mpsc`, each end behind a `Mutex` because Rust's `Receiver` is not `Sync`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: the log for each of the six orders,
then over 2000 runs, each in a random one of the six orders, how many
printed in order and a checksum of the logs (`2000 runs in random
orders: 2000 printed in order, checksum 55319996`).
`print_in_order.py` mirrors the ★ arm with a thread per method and two
`threading.Event`s, and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms. Each print function
checks, under the log's lock, that the log holds every word before its
own, and counts a print that finds one missing. It checks 600 problems:
each of the six orders 100 times, each with a second order, an
interleaving of the tasks of two `Foo`s, and busy work of up to 2000
steps before each print, all drawn at random before any arm runs.

| | property |
|---|---|
| P1 | the statement read literally: the log is `firstsecondthird` |
| P2 | by a second reading, each print: every word before its own was in the log when it printed |
| P3 | the same run started in the second order gives the same log |
| P4 | with busy work before each print, the log is in order and no print is early |
| P5 | two `Foo`s at once, their six tasks started interleaved, each log in order and no print early |
| P6 | the run repeated gives the same log |

All 18,000 checks pass on every arm: `600 problems, 18000 checks over
5 arms: 0 failures`.

## Mutation testing

Twenty-five edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All twenty-five are caught
natively, and seventeen under the interpreter too.

| # | mutation | `__mir-run` | `__mir-llvm-run` |
|---|---|---|---|
| M1 | ★: `second` never waits | P1 300, P2 300, P3 310, P4 300, P5 447 | P1 300, P2 300, P3 310, P4 302, P5 447, P6 4 |
| M2 | ★: `third` never waits | P1 500, P2 500, P3 503, P4 500, P5 578 | P1 523, P2 523, P3 517, P4 517, P5 573, P6 36 |
| M3 | ★: `first` hands on its turn before it prints | none | P3 2, P4 14; 190 to 223 in four more runs |
| M4 | ★: `second` hands on its turn before it prints | none | P1 2, P2 2, P3 4, P4 56, P5 7, P6 2; 271 to 291 in four more runs |
| M5 | ★: `second` prints twice | P1 600, P2 600, P3 600, P4 600, P5 600 | P1 600, P2 600, P3 600, P4 600, P5 600 |
| M6 | closed: `first` closes its channel before it prints | none | P1 15, P2 15, P3 8, P4 129, P5 18, P6 26; 397 to 440 in four more runs |
| M7 | closed: `second` never waits | P1 300, P2 300, P3 310, P4 300, P5 447 | P1 300, P2 300, P3 311, P4 303, P5 446, P6 36 |
| M8 | closed: `third` never waits | P1 500, P2 500, P3 503, P4 500, P5 578 | P1 500, P2 500, P3 503, P4 501, P5 579, P6 3 |
| M9 | closed: `second` closes its channel before it prints | none | P3 1, P4 7, P5 1, P6 6; 572 to 646 in four more runs |
| M10 | closed: `third` waits on `first`'s channel | P1 300, P2 300, P3 305, P4 300, P5 467 | P1 300, P2 300, P3 322, P4 280, P5 461, P6 287 |
| M11 | waitlist: a method let go a stage early | P1 400, P2 400, P3 417, P4 400, P5 542 | P1 261, P2 261, P3 261, P4 252, P5 487, P6 134 |
| M12 | waitlist: a waiter woken a stage early | P1 100, P2 100, P3 98, P4 100, P5 196 | P1 162, P2 162, P3 153, P4 178, P5 247, P6 78 |
| M13 | waitlist: `second` waiting for nothing | P1 300, P2 300, P3 310, P4 300, P5 447 | P1 299, P2 299, P3 306, P4 296, P5 447 |
| M14 | waitlist: `third` waiting only for `first` | P1 300, P2 300, P3 305, P4 300, P5 467 | P1 300, P2 300, P3 305, P4 299, P5 466, P6 2 |
| M15 | waitlist: `first` finishing before it prints | none | P4 1; 404 to 461 in four more runs |
| M16 | polling: a method let go a stage early | P1 400, P2 400, P3 417, P4 400, P5 542 | P1 397, P2 397, P3 414, P4 373, P5 543, P6 171 |
| M17 | polling: `first` sets the stage to two | P1 300, P2 300, P3 305, P4 300, P5 467 | P1 303, P2 303, P3 301, P4 294, P5 467, P6 49 |
| M18 | polling: `second` sets the stage before it prints | none | P1 15, P2 15, P3 17, P4 68, P5 17, P6 28; 359 to 438 in four more runs |
| M19 | polling: `third` waiting only for `first` | P1 300, P2 300, P3 305, P4 300, P5 467 | P1 298, P2 298, P3 303, P4 298, P5 465, P6 9 |
| M20 | polling: one look and one sleep, not a loop | P1 100, P2 100, P3 98, P4 100, P5 196 | P1 103, P2 103, P3 99, P4 106, P5 197, P6 5 |
| M21 | rust: `first` sends before it prints | none | P4 6; 243 to 281 in four more runs |
| M22 | rust: `second` never waits | P1 300, P2 300, P3 310, P4 300, P5 447 | P1 301, P2 301, P3 309, P4 301, P5 447, P6 11 |
| M23 | rust: `third` never waits | P1 500, P2 500, P3 503, P4 500, P5 578 | P1 523, P2 523, P3 520, P4 500, P5 577, P6 37 |
| M24 | rust: `second` sends before it prints | none | P1 2, P2 2, P4 110, P5 2, P6 2; 293 to 335 in four more runs |
| M25 | rust: `third` prints twice | P1 600, P2 600, P3 600, P4 600, P5 600 | P1 600, P2 600, P3 600, P4 600, P5 600 |

The eight the interpreter misses each hand on the turn just before the
print rather than just after it: a send (M3, M4, M21, M24), a close (M6,
M9), or the stage raised (M15, M18). The interpreter runs one task at a
time and switches only where a task waits, and a send, a close or a
store is not a wait, so the method still prints before the next one
runs. Natively the tasks run at once on every core, and the next method
sometimes prints first. How often depends on how busy the machine is: in
the mutation run, three programs at a time, each of the eight failed
between 1 and 211 checks; run four more times each, one program at a
time, every one of them failed every time, between 190 and 646 checks.
Natively P4 catches all twenty-five, since its busy work before each
print holds that window open.

The other seventeen break the order outright and fail on both lanes.
Natively the counts move with the schedule, and P6 fails too, since a
broken run's log changes from one run to the next; the interpreter's
schedule is the same on every run, so P6 passes there.

## Verification

Every arm prints the same output as `print_in_order.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing
on any file, and `karac fix` has nothing to apply.

The kata found four gaps, three of them fixed. The polling arm waits for
its turn with `sleep(Duration.ms(0))` between looks at an `Atomic`, and
a sleep whose pause had passed when it was first asked never let another
task run, so on the interpreter and on a one-worker build the arm never
finished (B-2026-11-11-32): a sleep now parks the first time it is
asked, even for no time. Rust backs off a spin like that for
microseconds, `Duration::from_micros(50)`, and Kāra's `Duration` has no
unit below the millisecond, so the arm can pause for nothing or for
twenty times as long (B-2026-11-11-33, open). Rust's
`Duration::from_millis(1)` became `Duration.from_millis(1)` and then had
no fix (B-2026-11-11-30); `from_millis` and `from_secs` now become `ms`
and `secs`. The Rust arm, two `std::sync::mpsc` channels behind
`Mutex`es, kept its `use std::sync::mpsc::..`, a `.unwrap()` on each
`MutexGuard` and each send and receive on the guard rather than its
value, with no fix for any (B-2026-11-11-31). `karac fix` now carries it
to a clean check in four rounds: the types, paths and `self` in Kāra's
spelling with the `mpsc` import gone, then `use std::sync::Mutex` as an
`import`, then the `.unwrap()`s gone, then each send and receive through
`.value`. Rust's `channel()` takes no capacity and Kāra's channels are
bounded, so no fix can pick one; the message says what `channel(n)`
takes, and the arm says `channel(1)` by hand. The other four arms were
written as Kāra.

## Benchmarks

The bench runs the ★ arm 10^4 times, each run starting its three tasks
in one of the six orders in turn, and prints `10000 runs: 10000 printed
in order, checksum 383636124`. Each language starts real concurrency for
every run: C a POSIX thread per method with two semaphores, Rust OS
threads in a `thread::scope` with two `mpsc` channels behind `Mutex`es,
Go a goroutine per method with two channels of capacity one and a
`WaitGroup`, and Python a thread per method with two `threading.Event`s.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python (user is the median CPU
time in user mode, summed over the threads), with karac `3402c1954a` on
LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median | user |
|---|---|---|---|
| Go | 0.024 to 0.041 s | 0.028 s | 0.023 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.296 to 0.482 s | 0.391 s | 1.350 s |
| Kāra (`karac build`) | 0.318 to 0.474 s | 0.398 s | 1.418 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.988 to 1.311 s | 1.062 s | 0.150 s |
| C (`clang -O3`) | 0.942 to 1.294 s | 1.070 s | 0.188 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.181 to 1.516 s | 1.254 s | 0.417 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 1.136 to 1.339 s | 1.257 s | 0.422 s |
| Rust (`rustc -O`) | 1.157 to 1.389 s | 1.273 s | 0.426 s |
| Python | 4.286 s | | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 2.7x faster than C and 3.2x faster than Rust, each
of which starts three OS threads for every one of the 10^4 runs. Kāra's
tasks run on a pool of workers, so a hand-off from one method to the
next is a switch within the pool, where a hand-off between C's or Rust's
OS threads goes through the kernel; little of their wall time is user
time. Go's goroutines hand off within its own scheduler too, and Go
takes about a fourteenth of Kāra's time. Kāra's user time is about 3.5x
its wall time: its workers stay busy between hand-offs. An idle
program's workers do sleep (a task waiting two seconds on a channel used
0.05 s of CPU), so this is presumably a short spin before a worker
parks; it was not traced further. Python takes about 11x Kāra's time.
