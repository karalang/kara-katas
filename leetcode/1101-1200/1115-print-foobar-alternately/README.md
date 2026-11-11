# 1115. Print FooBar Alternately

Suppose you are given the following code:

```
class FooBar {
  public void foo() {
    for (int i = 0; i < n; i++) {
      print("foo");
    }
  }

  public void bar() {
    for (int i = 0; i < n; i++) {
      print("bar");
    }
  }
}
```

The same instance of `FooBar` will be passed to two different threads:

- thread A will call `foo()`, while
- thread B will call `bar()`.

Modify the given program to output `"foobar"` `n` times.

```
n = 1   ->  "foobar"
n = 2   ->  "foobarfoobar"
```

**Constraints:** `1 <= n <= 1000`.

The arms are a `sync struct FooBar` with `fn new(n: i64) -> FooBar`,
`fn foo(self, print_foo: Fn())` and `fn bar(self, print_bar: Fn())`.
LeetCode's threads are a `TaskGroup` with a task for each method,
started in either order, and its prints go to a log behind a `Mutex`.

## Approaches

| file | mechanism |
|---|---|
| `print_foobar.kara` ★ | two channels passed back and forth, each holding one method's turn: `foo` waits on its own, prints and hands the turn to `bar`, which hands it back; `foo`'s first turn is put in its channel when the pair is made |
| `print_foobar_semaphore.kara` | two of the standard library's semaphores, as the Python solutions on LeetCode write it with `threading.Semaphore`: `foo` starts with a permit and `bar` without, and each method releases the other's after it prints |
| `print_foobar_waitlist.kara` | a condition variable built from a `Mutex` and channels, as the C++ and Java solutions use one: whose turn it is sits under the lock with the method waiting, if any, and a method that prints passes the turn and wakes the waiter |
| `print_foobar_polling.kara` | an `Atomic` flag for whose turn it is, and a method whose turn has not come sleeping for no time at all between checks |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 6 lines: the logs for LeetCode's two examples
and for two runs with `bar`'s task started first, then over 2000 runs
of up to 12 rounds, either task started first, how many alternated and
a checksum of the logs (`2000 runs of up to 12 rounds: 2000
alternating, checksum 509823911`), and LeetCode's largest, `n = 1000`.
`print_foobar.py` mirrors the ★ arm with a thread per method and two
one-slot `queue.Queue`s, and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. Each print function
checks, under the log's lock, that the log is what it should be before
its word (`foobar` some number of times, then `foo` before a `bar`),
and counts a print that finds it otherwise. It checks 600 problems of
up to 12 rounds, either task started first, the four tasks of two
pairs started in a random order, and busy work of up to 2000 steps for
each of the first one to five prints, all drawn at random before any
arm runs.

| | property |
|---|---|
| P1 | the statement read literally: the log is `foobar` `n` times |
| P2 | by a second reading, each print: the log was as it should be when it printed |
| P3 | the other task started first gives the same log |
| P4 | with busy work before the first prints, the log is right and no print found it wrong |
| P5 | two pairs at once, their four tasks started interleaved, each log right and no print found it wrong |
| P6 | the run repeated gives the same log |

All 14,400 checks pass on every arm: `600 problems: checksum 188173806,
14400 checks over 4 arms: 0 failures`. A Python reading of the same
problems, writing `foobar` `n` times for each arm, gives the same
checksum.

## Mutation testing

Twenty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All twenty are caught
natively, and ten under the interpreter too.

| # | mutation | `__mir-run` | `__mir-llvm-run` |
|---|---|---|---|
| M1 | ★: `foo` prints before it waits for its turn | P1 547, P2 547, P3 547, P4 547, P5 547 | P1 547, P2 547, P3 547, P4 547, P5 547 |
| M2 | ★: `bar` prints before it waits for its turn | P1 576, P2 576, P3 571, P4 576, P5 584 | P1 577, P2 577, P3 571, P4 579, P5 584, P6 26 |
| M3 | ★: `foo` hands on the turn before it prints | none | P3 1, P4 68, P5 5, P6 7; 508 to 559 in four more runs |
| M4 | ★: `bar` hands back the turn before it prints | none | P4 6; 403 to 446 in four more runs |
| M5 | ★: `foo` prints twice a turn | P1 600, P2 600, P3 600, P4 600, P5 600 | P1 600, P2 600, P3 600, P4 600, P5 600 |
| M6 | semaphore: `bar` starts with the permit | P1 600, P2 600, P3 600, P4 600, P5 600 | P1 600, P2 600, P3 600, P4 600, P5 600 |
| M7 | semaphore: `foo` releases before it prints | none | P1 42, P2 43, P3 35, P4 180, P5 46, P6 69; 1284 to 1348 in four more runs |
| M8 | semaphore: `bar` releases before it prints | none | P1 25, P2 26, P3 16, P4 81, P5 32, P6 33; 980 to 1091 in four more runs |
| M9 | semaphore: `foo` prints before it acquires | P1 547, P2 547, P3 547, P4 547, P5 547 | P1 547, P2 547, P3 547, P4 547, P5 547, P6 67 |
| M10 | semaphore: `bar` prints twice a turn | P1 600, P2 600, P3 600, P4 600, P5 600 | P1 600, P2 600, P3 600, P4 600, P5 600 |
| M11 | waitlist: a method goes on when the turn is not its own | P1 600, P2 600, P3 600, P4 600, P5 600 | P1 600, P2 600, P3 600, P4 600, P5 600 |
| M12 | waitlist: `foo` passes the turn before it prints | none | P1 11, P2 12, P3 13, P4 27, P5 10, P6 19; 1824 to 1867 in four more runs |
| M13 | waitlist: `bar` passes the turn before it prints | none | P1 21, P2 23, P3 21, P4 22, P5 11, P6 26; 1563 to 1683 in four more runs |
| M14 | waitlist: a method put on the list goes on without waiting | P1 576, P2 576, P3 571, P4 576, P5 584 | P1 570, P2 570, P3 568, P4 569, P5 584, P6 95 |
| M15 | waitlist: `foo` prints twice a turn | P1 600, P2 600, P3 600, P4 600, P5 600 | P1 600, P2 600, P3 600, P4 600, P5 600 |
| M16 | polling: `foo` passes the turn before it prints | none | P4 7; 1293 to 1400 in four more runs |
| M17 | polling: `bar` passes the turn before it prints | none | P4 6; 1074 to 1236 in four more runs |
| M18 | polling: `bar` looks once and sleeps once, not a loop | none | never ends |
| M19 | polling: `foo` looks once and sleeps once, not a loop | none | never ends |
| M20 | polling: `bar` prints twice a turn | P1 600, P2 600, P3 600, P4 600, P5 600 | P1 600, P2 600, P3 600, P4 600, P5 600 |

Eight of the ten the interpreter misses hand on the turn just before the
print rather than just after it: a send (M3, M4), a release (M7, M8),
the turn passed on the list (M12, M13), or the flag stored (M16, M17).
The interpreter runs one task at a time and switches only where a task
waits, and a send, a release or a store is not a wait, so the method
still prints before the next one runs. Natively the tasks run at once on
every core, and the next method sometimes prints first. How often
depends on how busy the machine is: in the mutation run, three programs
at a time, each of the eight failed between 6 and 415 checks; run four
more times each, one program at a time, every one of them failed every
time, between 403 and 1867 checks.

M18 and M19 turn the polling arm's wait into one look and one sleep.
Under the interpreter one sleep is always time enough for the other task
to take its turn, so the log comes out right. Natively the method that
no longer waits can run ahead and finish all its rounds, and the other,
after its first round, waits for a turn no one is left to give it: the
program never ends, and the mutation run stops it after 300 s.

The other ten break the order outright and fail on both lanes. Natively
the counts move with the schedule, and P6 fails too, since a broken
run's log changes from one run to the next; the interpreter's schedule
is the same on every run, so P6 passes there.

## Verification

Every arm prints the same output as `print_foobar.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file, and `karac fix` has nothing to apply.

The kata found three gaps. The polling arm waits for its turn with
`sleep(Duration.ms(0))` between looks at an `Atomic`, and a sleep whose
pause had passed when first asked never let another task run, so on the
interpreter and on a one-worker build the arm never finished
(B-2026-11-11-32, fixed, found first by kata 1114): a sleep now parks
the first time it is asked. The natural semaphore arm is the Python
solutions' two `threading.Semaphore`s, written with the standard
library's `Semaphore`: `Semaphore.new(1)` for `foo` and
`Semaphore.new(0)` for `bar`, each method releasing the other's. It
printed `foofoobarbar` for `n = 2`, because `acquire` on an exhausted
semaphore failed at once rather than waiting for another task's
`release`, and `release` never counted above the starting permits, so a
semaphore made with none could never be released (B-2026-11-11-34, fixed
in c47fd80f23). The semaphore arm built its semaphores from channels
until then and now uses the standard library's. With it, a compiled run
of the differential sometimes takes 63 s rather than 3 s, in 6 of 120
runs across a built binary, `karac __mir-llvm-run` and `karac run`,
though its output is right: an `acquire` waits out its whole 60 s
timeout after the permit it waits for was released (B-2026-11-11-66,
open). Every arm was written as Kāra, and `karac fix` had nothing to
change in any of them.

## Benchmarks

The bench runs the ★ arm 1000 times, 200 rounds each, `bar`'s task
started first in every other run, and prints `1000 runs of 200 rounds:
1000 alternating, checksum 15346702`. Each language starts real
concurrency for every run: C a POSIX thread per method with two
semaphores, `foo`'s holding one permit, Rust OS threads in a
`thread::scope` with two `sync_channel(1)`s, each end behind a `Mutex`,
Go a goroutine per method with two channels of capacity one, `foo`'s
filled when the pair is made, and a `WaitGroup`, and Python a thread per
method with two `threading.Semaphore`s.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python (user is the median CPU
time in user mode, summed over the threads), with karac `3402c1954a` on
LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median | user |
|---|---|---|---|
| Go | 0.088 to 0.111 s | 0.099 s | 0.108 s |
| Kāra (`karac build`) | 0.612 to 0.878 s | 0.754 s | 1.392 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.606 to 0.913 s | 0.798 s | 1.453 s |
| C (`clang -O3 -march=x86-64-v3`) | 5.290 to 5.689 s | 5.574 s | 0.484 s |
| C (`clang -O3`) | 5.136 to 5.715 s | 5.586 s | 0.483 s |
| Rust (`rustc -O`) | 5.590 to 6.053 s | 5.808 s | 1.139 s |
| Rust (`rustc -O -C overflow-checks=on`) | 5.671 to 6.000 s | 5.836 s | 1.165 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 5.736 to 6.054 s | 5.898 s | 1.100 s |
| Python | 10.2 s | | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 7x faster than C and Rust, whose two threads hand
the turn back and forth 400 times a run. Kāra's tasks run on a pool of
workers, so a hand-off from one method to the next is a switch within
the pool, where a hand-off between C's or Rust's OS threads goes through
the kernel; little of their wall time is user time. Go's goroutines hand
off within its own scheduler too, and Go takes about an eighth of Kāra's
time. Kāra's user time is about twice its wall time: its workers stay
busy between hand-offs. An idle program's workers do sleep (a task
waiting two seconds on a channel used 0.05 s of CPU), so this is
presumably a short spin before a worker parks; it was not traced
further. Python takes about 13x Kāra's time.
