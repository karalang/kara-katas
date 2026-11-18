# 1195. Fizz Buzz Multithreaded

You have the four functions:

- `printFizz` that prints the word `"fizz"` to the console,
- `printBuzz` that prints the word `"buzz"` to the console,
- `printFizzBuzz` that prints the word `"fizzbuzz"` to the console, and
- `printNumber` that prints a given integer to the console.

You are given an instance of the class `FizzBuzz` that has four
functions: `fizz`, `buzz`, `fizzbuzz` and `number`. The same instance of
`FizzBuzz` will be passed to four different threads:

- Thread A: calls `fizz()` that should output the word `"fizz"`.
- Thread B: calls `buzz()` that should output the word `"buzz"`.
- Thread C: calls `fizzbuzz()` that should output the word `"fizzbuzz"`.
- Thread D: calls `number()` that should only output the integers.

Modify the given class to output the series `[1, 2, "fizz", 4, "buzz",
...]` where the `i`th token (1-indexed) of the series is `"fizzbuzz"` if
`i` is divisible by 3 and 5, `"fizz"` if `i` is divisible by 3 and not
5, `"buzz"` if `i` is divisible by 5 and not 3, and `i` if `i` is
divisible by neither.

```
n = 15  ->  [1,2,"fizz",4,"buzz","fizz",7,8,"fizz","buzz",11,"fizz",13,14,"fizzbuzz"]
n = 5   ->  [1,2,"fizz",4,"buzz"]
```

**Constraints:** `1 <= n <= 50`.

The arms are a `sync struct FizzBuzz` with `fn new(n: i64)`, and `fizz`,
`buzz` and `fizzbuzz`, each `fn (self, print: Fn())`, and `number`,
`fn (self, print_number: Fn(i64))`. LeetCode's threads are a
`TaskGroup` with a task for each method, started in a given order, and
the lines go to a log behind a `Mutex`.

## Approaches

| file | mechanism |
|---|---|
| `fizz_buzz_multithreaded.kara` ★ | a `Semaphore` per printer, `number`'s holding one permit: each printer walks 1 to `n`, and at each of its own numbers waits on its semaphore, prints, and releases the semaphore of whichever printer has the next number |
| `fizz_buzz_multithreaded_polling.kara` | the next number to print in a `Mutex`: each printer locks it, prints and advances it when the number is its own, and otherwise unlocks and sleeps for no time at all before it looks again |
| `fizz_buzz_multithreaded_atomic.kara` | the next number in an `Atomic`, with no lock: only the printer whose number it is ever stores, so a load and a store need no compare-and-swap; the others sleep for no time and look again |
| `fizz_buzz_multithreaded_channel.kara` | a `channel(1)` to each printer carrying the turn as the number to print, `number`'s holding a 1 to start: each printer receives, prints, and sends the next number down the channel of its printer; once the numbers run out, a 0 down every channel tells each to return |
| `differential.kara` | the four arms against the statement read literally, six more properties |

Every arm prints the same 6 lines: the logs for LeetCode's two examples,
for one number, for the first `fizz` and for LeetCode's largest, `n =
50`, then over 2000 runs of `n` from 1 to 50, the four tasks started in
a random order, how many lines were printed and how many runs printed in
order (`2000 random runs: 51067 printed, 2000 in order`).
`fizz_buzz_multithreaded.py` mirrors the ★ arm with a thread per method
and four `threading.Semaphore`s, and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement
read literally. It draws 500 problems, `n` from 1 to 50 and the four
tasks in a random order, and runs each arm three times on each: on `n`
in that order, on `n + 1` in that order, and on `n` with the tasks
started in reverse.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | `n` lines |
| P3 | each printer prints its own count: `n / 3 - n / 15` fizzes, `n / 5 - n / 15` buzzes, `n / 15` fizzbuzzes |
| P4 | the plain numbers are those divisible by neither 3 nor 5, rising |
| P5 | the run of `n` is the start of the run of `n + 1` |
| P6 | the tasks started in reverse print the same |
| P7 | the ★ arm's answer |

All 14,000 checks pass on every lane: `500 runs: 13244 printed, 14000
checks over 4 arms: 0 failures`, under `karac __mir-run`, `karac run`,
`karac build` and the AddressSanitizer build.

## Mutation testing

Eight edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`. All eight are caught on both.

| # | mutation | `__mir-run` | `karac run` |
|---|---|---|---|
| S1 | ★: `fizz`'s semaphore starts with a permit | P1 469, P5 153, P6 484, P7 1407 | P1 469, P5 184, P6 484, P7 1407 |
| S2 | ★: `fizz` prints before it waits for its turn | P1 469, P5 126, P6 484, P7 1407 | P1 469, P5 128, P6 482, P7 1407 |
| L1 | polling: `fizz` takes the multiples of 15 too | P1 181, P3 181, P6 371, P7 181 | P1 185, P3 185, P5 35, P6 359, P7 185 |
| L2 | polling: the counter skips a number | P1 490, P2 490, P3 460, P4 490, P5 500, P7 490 | the same |
| A1 | atomic: `number` prints `i + 1` | P1 500, P4 500, P7 500 | the same |
| A2 | atomic: `fizzbuzz` skips the number after its own | P1 354, P2 354, P4 354, P5 371, P7 354 | the same |
| C1 | channel: the turns end one number early | P1 490, P2 490, P3 231, P4 259, P5 500, P7 490 | the same |
| C2 | channel: a multiple of 15 goes to `fizz` | P1 371, P3 371, P7 371 | the same |

A mutation of the ★ arm fails P7 on the other three arms, 469 times on
each. S1 and S2 let `fizz` print before its turn, and
L1 races `fizz` with `fizzbuzz` for each multiple of 15; which printer
gets there first depends on the schedule, so their counts move between
the lanes, and P6, the same problem started in another order, is what
those three fail most. The other five break the sequence on every
schedule and fail the same on both lanes. The two that print the right
lines in the wrong order (S1, S2) keep P2 to P4, which count and sort
what was printed; P1, P5, P6 and P7 catch them.

## Verification

Every arm prints the same output as `fizz_buzz_multithreaded.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac run`, `karac build`
and `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer), with
no error. `karac check --output=json` reports nothing on any file. The
polling arm took one round of 4 fixes from `karac fix`: `g.value = i +
1` on the lock's guard to `*g.value = i + 1`, and three `.to_string()`s
on string literals in its copy of the harness dropped. The kata found
no gap.

## Benchmarks

`bench/` times the ★ arm in 3 runs of n = 200000, past LeetCode's 50
so the hand-offs dominate, the four tasks started in three orders; each
printer appends its line to a shared list under a lock, and each run's
lines are folded into a checksum. Every program prints `3 runs of n =
200000: checksum 463202482`. Each language starts real concurrency for
every run: Kāra four tasks in a `TaskGroup` with a `Semaphore` per
printer, C a POSIX thread per printer with a `sem_t` each, Rust OS
threads with a count under a `Mutex` and a `Condvar` per printer (its
standard library has no semaphore), Go a goroutine per printer with a
count under a `sync.Mutex` and a `sync.Cond`, and Python a thread per
printer with `threading.Semaphore`s.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and two of Python (user is the median CPU time in user mode, summed over the threads), with karac `e8dc4f7aa2`
plus the typechecker fix pushed as `ab7613763c`, on LLVM 22. A plain
`karac build` targets x86-64-v2, so the C and overflow-checked Rust
programs are also built at x86-64-v3 for comparison:

| | time | median | user (median) |
|---|---|---|---|
| Kāra (`karac build`) | 0.586 to 0.667 s | 0.631 s | 0.721 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.582 to 0.695 s | 0.616 s | 0.696 s |
| Rust (`rustc -O`) | 6.143 to 6.588 s | 6.343 s | 0.630 s |
| Rust (`rustc -O -C overflow-checks=on`) | 6.071 to 6.453 s | 6.284 s | 0.637 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 6.113 to 6.474 s | 6.294 s | 0.653 s |
| C (`clang -O3`) | 6.127 to 6.611 s | 6.294 s | 0.797 s |
| C (`clang -O3 -march=x86-64-v3`) | 6.127 to 6.472 s | 6.310 s | 0.793 s |
| Go | 0.207 to 0.250 s | 0.232 s | 0.250 s |
| Python | 12.98 to 14.23 s | | 8.291 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 10x faster than C and Rust (0.616 s against 6.29
s), whose threads hand the turn on about 200000 times a run. Kāra's
tasks run on a pool of workers, so a hand-off from one printer to the
next is a switch within the pool, where a hand-off between C's or Rust's
OS threads goes through the kernel; about a tenth of their wall time is
user time. Go's goroutines hand off within its own scheduler too, and Go
takes about 38% of Kāra's time. Python takes about 22x Kāra's time.
