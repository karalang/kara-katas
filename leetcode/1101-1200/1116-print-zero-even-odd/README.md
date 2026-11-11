# 1116. Print Zero Even Odd

You have a function `printNumber` that can be called with an integer
parameter and prints it to the console. For example, calling
`printNumber(7)` prints `7`.

You are given an instance of the class `ZeroEvenOdd` that has three
functions: `zero`, `even`, and `odd`. The same instance of
`ZeroEvenOdd` will be passed to three different threads:

- Thread A: calls `zero()` that should only output `0`'s.
- Thread B: calls `even()` that should only output even numbers.
- Thread C: calls `odd()` that should only output odd numbers.

Modify the given class to output the series `"010203040506..."` where
the length of the series must be `2n`.

```
n = 2   ->  "0102"
n = 5   ->  "0102030405"
```

**Constraints:** `1 <= n <= 1000`.

The arms are a `sync struct ZeroEvenOdd` with `fn new(n: i64)`, and
`zero`, `even` and `odd`, each `fn (self, print_number: Fn(i64))`.
LeetCode's threads are a `TaskGroup` with a task for each method,
started in any of the six orders, and the numbers go to a log behind a
`Mutex`. The series is `2n` long only while `n < 10`; it is `0` before
each of 1 to `n`, so `n = 1000` prints 3893 characters.

## Approaches

| file | mechanism |
|---|---|
| `zero_even_odd.kara` ★ | three channels passed around, each holding one method's turn: `zero` waits on its own, prints and hands the turn to `odd` or `even` by the number that comes next, and that one prints and hands it back |
| `zero_even_odd_payload.kara` | the numbers through channels: `zero` prints its 0 and sends the next number to `odd` or `even`, which prints what it receives and says so on a channel back; the two printers never count |
| `zero_even_odd_waitlist.kara` | a condition variable built from a `Mutex` and channels, as the C++ and Java solutions use one: the count of numbers printed under the lock, each method waiting for the count its next print needs, and every print waking every waiter to look again |
| `zero_even_odd_polling.kara` | an `Atomic` count of the numbers printed, and a method whose turn has not come sleeping for no time at all between checks |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 6 lines: the logs for LeetCode's two examples
and for two runs started from `odd` and from `even`, then over 2000
runs of up to 15 numbers, the tasks started in a random order, how many
printed in order and a checksum of the logs (`2000 runs of up to 15
numbers: 2000 in order, checksum 227638611`), and LeetCode's largest,
`n = 1000`. `zero_even_odd.py` mirrors the ★ arm with a thread per
method and three one-slot `queue.Queue`s, and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms. Each print function
checks, under the log's lock, that the log is what it should be before
its number and that its number is the one that comes next, and counts a
print that finds otherwise. It checks 600 problems of up to 15 numbers:
each of the six orders 100 times, with a second order, the six tasks of
two printers started in a random order, and busy work of up to 2000
steps for each of the first one to five prints, all drawn at random
before any arm runs.

| | property |
|---|---|
| P1 | the statement read literally: the log is `0` before each of 1 to `n` |
| P2 | by a second reading, each print: the log was as it should be when it printed, and the number was the next one |
| P3 | the tasks started in the second order give the same log |
| P4 | with busy work before the first prints, the log is right and no print found it wrong |
| P5 | two printers at once, their six tasks started interleaved, each log right and no print found it wrong |
| P6 | the run repeated gives the same log |

All 14,400 checks pass on every arm: `600 problems: checksum 995490502,
14400 checks over 4 arms: 0 failures`. A Python reading of the same
problems, writing `0` before each of 1 to `n` for each arm, gives the
same checksum.

## Mutation testing

Twenty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Nineteen are caught
natively, and eleven of them under the interpreter too.

| # | mutation | `__mir-run` | `__mir-llvm-run` |
|---|---|---|---|
| M1 | ★: `zero` prints before it waits for its turn | P1 552, P2 552, P3 552, P4 552, P5 552 | P1 552, P2 552, P3 552, P4 552, P5 552, P6 3 |
| M2 | ★: `even` hands back the turn before it prints | none | P4 5; 245 to 279 in four more runs |
| M3 | ★: `odd` hands back the turn before it prints | none | P4 14, P6 1; 329 to 363 in four more runs |
| M4 | ★: `even` prints the number after its own | P1 552, P2 552, P3 552, P4 552, P5 552 | P1 552, P2 552, P3 552, P4 552, P5 552 |
| M5 | ★: `zero` prints twice a turn | P1 600, P2 600, P3 600, P4 600, P5 600 | P1 600, P2 600, P3 600, P4 600, P5 600 |
| M6 | payload: `zero` sends the number before it prints its zero | none | P4 8; 532 to 581 in four more runs |
| M7 | payload: `even` says it has printed before it waits | P1 281, P2 281, P3 266, P4 281, P5 411 | P1 283, P2 283, P3 273, P4 300, P5 413, P6 21 |
| M8 | payload: `even` prints the number before the one it gets | P1 552, P2 552, P3 552, P4 552, P5 552 | P1 552, P2 552, P3 552, P4 552, P5 552 |
| M9 | payload: `odd` says it has printed before it waits | P1 279, P2 279, P3 264, P4 279, P5 423 | P1 291, P2 291, P3 275, P4 296, P5 431, P6 29 |
| M10 | payload: `zero` prints twice a turn | P1 600, P2 600, P3 600, P4 600, P5 600 | P1 600, P2 600, P3 600, P4 600, P5 600 |
| M11 | waitlist: a method goes on once at least its count is printed | none | none |
| M12 | waitlist: `even` counts its print before it prints | none | P4 13, P5 1, P6 1; 163 to 181 in four more runs |
| M13 | waitlist: `odd` counts its print before it prints | none | P4 3; 217 to 240 in four more runs |
| M14 | waitlist: `zero` prints before it waits | P1 552, P2 552, P3 552, P4 552, P5 552 | P1 552, P2 552, P3 552, P4 552, P5 552, P6 1 |
| M15 | waitlist: `zero` prints twice a turn | P1 600, P2 600, P3 600, P4 600, P5 600 | P1 600, P2 600, P3 600, P4 600, P5 600 |
| M16 | polling: `zero` counts its print before it prints | none | P4 9; 1523 to 1644 in four more runs |
| M17 | polling: `even` counts its print before it prints | none | P4 3; 637 to 702 in four more runs |
| M18 | polling: `odd` counts its print before it prints | none | P1 5, P2 5, P3 10, P4 35, P5 14, P6 16; 617 to 744 in four more runs |
| M19 | polling: `zero` prints before it waits | P1 552, P2 552, P3 552, P4 552, P5 552 | P1 552, P2 552, P3 551, P4 552, P5 552, P6 76 |
| M20 | polling: one look and one sleep, not a loop | P1 534, P2 534, P3 533, P4 534, P5 543 | P1 540, P2 544, P3 538, P4 550, P5 546, P6 398 |

Eight of the nine the interpreter misses hand on the turn just before
the print rather than just after it: the turn sent back (M2, M3), the
number sent before `zero` prints its `0` (M6), or the print counted
(M12, M13, M16, M17, M18). The interpreter runs one task at a time and
switches only where a task waits, and a send or a store is not a wait,
so the method still prints before the next one runs. Natively the tasks
run at once on every core, and the next method sometimes prints first.
How often depends on how busy the machine is: in the mutation run, three
programs at a time, each of the eight failed between 3 and 85 checks;
run four more times each, one program at a time, every one of them
failed every time, between 163 and 1644 checks.

M11 is caught on neither lane, nor in four more native runs, and cannot
be: the waitlist arm lets a method go on once exactly `printed` numbers
are out, and the edit once at least that many are, but the number after
`printed` is printed only by the method waiting for it, so the count
never passes a waiter and the two tests agree on every schedule.

The other eleven break the order outright and fail on both lanes.
Natively the counts move with the schedule, and P6 fails too, since a
broken run's log changes from one run to the next; the interpreter's
schedule is the same on every run, so P6 passes there.

## Verification

Every arm prints the same output as `zero_even_odd.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file, and `karac fix` has nothing to apply.

The kata found one gap, now fixed, which kata 1114 found first: the
polling arm waits for its turn with `sleep(Duration.ms(0))` between
looks at an `Atomic`, and a sleep whose pause had passed when first
asked never let another task run, so on the interpreter and on a
one-worker build the arm never finished (B-2026-11-11-32); a sleep now
parks the first time it is asked. Every arm was written as Kāra, and
`karac fix` had nothing to change in any of them.

## Benchmarks

The bench runs the ★ arm 1000 times over 1 to 200, the three tasks
started in one of the six orders in turn, and prints `1000 runs over 1
to 200: 1000 in order, checksum 418255395`. Each language starts real
concurrency for every run: C a POSIX thread per method with three
semaphores, `zero`'s holding one permit, Rust OS threads in a
`thread::scope` with three `sync_channel(1)`s, each end behind a
`Mutex`, Go a goroutine per method with three channels of capacity one,
`zero`'s filled when the printer is made, and a `WaitGroup`, and Python
a thread per method with three `threading.Semaphore`s.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python (user is the median CPU
time in user mode, summed over the threads), with karac `3402c1954a` on
LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median | user |
|---|---|---|---|
| Go | 0.096 to 0.125 s | 0.107 s | 0.118 s |
| Kāra (`karac build`) | 0.664 to 1.168 s | 0.996 s | 1.894 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.776 to 1.175 s | 1.018 s | 1.904 s |
| C (`clang -O3`) | 5.600 to 6.028 s | 5.800 s | 0.559 s |
| C (`clang -O3 -march=x86-64-v3`) | 5.568 to 6.129 s | 5.890 s | 0.542 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 5.950 to 6.548 s | 6.124 s | 1.311 s |
| Rust (`rustc -O`) | 5.950 to 6.456 s | 6.202 s | 1.290 s |
| Rust (`rustc -O -C overflow-checks=on`) | 6.000 to 6.430 s | 6.206 s | 1.282 s |
| Python | 10.5 s | | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 6x faster than C and Rust, whose three threads hand
the turn on 400 times a run. Kāra's tasks run on a pool of workers, so a
hand-off from one method to the next is a switch within the pool, where
a hand-off between C's or Rust's OS threads goes through the kernel;
little of their wall time is user time. Go's goroutines hand off within
its own scheduler too, and Go takes about a tenth of Kāra's time. Kāra's
user time is about twice its wall time: its workers stay busy between
hand-offs. An idle program's workers do sleep (a task waiting two
seconds on a channel used 0.05 s of CPU), so this is presumably a short
spin before a worker parks; it was not traced further. Python takes
about 10x Kāra's time.
