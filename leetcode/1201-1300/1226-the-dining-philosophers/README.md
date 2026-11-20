# 1226. The Dining Philosophers

Five silent philosophers sit at a round table with bowls of spaghetti.
Forks are placed between each pair of adjacent philosophers.

Each philosopher must alternately think and eat. However, a philosopher
can only eat spaghetti when they have both left and right forks. Each
fork can be held by only one philosopher and so a philosopher can use the
fork only if it is not being used by another philosopher. After an
individual philosopher finishes eating, they need to put down both forks
so that the forks become available to others. A philosopher can take the
fork on their right or the one on their left as they become available,
but cannot start eating before getting both forks.

Eating is not limited by the remaining amounts of spaghetti or stomach
space; an infinite supply and an infinite demand are assumed.

Design a discipline of behaviour (a concurrent algorithm) such that no
philosopher will starve; i.e., each can forever continue to alternate
between eating and thinking, assuming that no philosopher can know when
others may want to eat or think.

The philosophers' ids are numbered from `0` to `4` in a clockwise order.
Implement the function `void wantsToEat(philosopher, pickLeftFork,
pickRightFork, eat, putLeftFork, putRightFork)` where:

- `philosopher` is the id of the philosopher who wants to eat.
- `pickLeftFork` and `pickRightFork` are functions you can call to pick
  the corresponding forks of that philosopher.
- `eat` is a function you can call to let the philosopher eat once they
  have picked both forks.
- `putLeftFork` and `putRightFork` are functions you can call to put
  down the corresponding forks of that philosopher.
- The philosophers are assumed to be thinking as long as they are not
  asking to eat (the function is not being called with their number).

Five threads, each representing a philosopher, will simultaneously use
one object of your class to simulate the process. The function may be
called for the same philosopher more than once, even before the last
call ends.

```
n = 1  ->  [[4,2,1],[4,1,1],[0,1,1],[2,2,1],[2,1,1],[2,0,3],[2,1,2],[2,2,2],[4,0,3],
            [4,1,2],[0,2,1],[4,2,2],[3,2,1],[3,1,1],[0,0,3],[0,1,2],[0,2,2],[1,2,1],
            [1,1,1],[3,0,3],[3,1,2],[3,2,2],[1,0,3],[1,1,2],[1,2,2]]
```

`n` is the number of times each philosopher calls the function. Each
output entry `[a, b, c]` is a call: `a` the philosopher, `b` the fork (1
left, 2 right, 0 for eating), `c` the operation (1 pick, 2 put, 3 eat).
Any order a valid discipline can produce is accepted.

**Constraints:** `1 <= n <= 60`.

The statement does not say which fork is whose. LeetCode's example is
valid only when philosopher `i`'s left fork is the one they share with
philosopher `i + 1` and their right fork the one they share with
philosopher `i − 1`; the kata numbers the forks so that philosopher
`i`'s left fork is fork `i` and the right fork is fork `(i + 4) % 5`.

The arms are a `sync struct DiningPhilosophers` with `fn new()` and
`fn wants_to_eat(self, philosopher: i64, pick_left_fork: Fn(),
pick_right_fork: Fn(), eat: Fn(), put_left_fork: Fn(), put_right_fork:
Fn())`. LeetCode's threads are a `TaskGroup` with a task for each
philosopher, calling `wants_to_eat` `n` times, started in a given order;
each callback appends its `[a, b, c]` to a log behind a `Mutex`. Since a
run may log its calls in any valid order, every harness judges the log
rather than printing it.

## Approaches

| file | mechanism |
|---|---|
| `the_dining_philosophers.kara` ★ | a `Mutex` for each fork, every philosopher locking the lower-numbered of their two forks first: philosopher 0 reaches left first and the others right first, so no cycle of philosophers can each hold one fork and wait for the next. Both forks are put down before their locks are released |
| `the_dining_philosophers_table.kara` | one `Mutex` for the whole table, held from the first pick to the last put: one philosopher eats at a time |
| `the_dining_philosophers_butler.kara` | a butler: a `Semaphore` of four seats, and a `Semaphore` of one permit for each fork, taken left then right; with at most four at the table, one of them always has both forks within reach |
| `the_dining_philosophers_lefty.kara` | a `Mutex` for each fork, the even philosophers locking left first and the odd ones right first |
| `the_dining_philosophers_polling.kara` | which forks are in use in a `Vec[bool]` under one `Mutex`: a philosopher takes both forks when both are free, and otherwise unlocks and yields (`sleep(Duration.ms(0))`) before looking again, so nobody holds one fork while waiting for the other |
| `the_dining_philosophers_atomic.kara` | an `Atomic[bool]` for each fork and no lock: the lower-numbered fork first, each taken by `compare_exchange(false, true)`, yielding while it is taken |
| `the_dining_philosophers_channel.kara` | each fork a `channel(1)` holding a token while it lies on the table: picking it up receives the token and putting it down sends it back, the lower-numbered fork first |
| `the_dining_philosophers_backoff.kara` | backing off, LeetCode's common Java answer: a `Mutex` for each fork; a philosopher waits for the left fork, only tries the right one, by `try_lock`, and when it is taken lets the left one go, yields and starts again, so nobody holds one fork while waiting for the other |
| `differential.kara` | the eight arms against the statement read literally, five more properties |

Every arm prints the same 5 lines: LeetCode's example output judged
(`25 calls, valid`), the logs of runs with `n` = 1, 2 and 60 judged, then
over 1000 runs of `n` from 1 to 60, the five tasks started in a random
order, how many calls were logged and how many logs were valid
(`1000 random runs: 746375 calls, 1000 valid`). The judge is the
statement read literally: it replays the log on five forks, and a fork
is picked up only when it lies on the table and put down only by
whoever holds it, a philosopher eats only holding both their forks,
every philosopher eats `n` times, and every fork is back on the table at
the end. `the_dining_philosophers.py` mirrors the ★ arm with a thread
for each philosopher and a `threading.Lock` for each fork, and its
output is byte-identical. Every arm gives the same output under `karac
run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: all eight arms check clean as written. The back-off arm
waited on a gap: `Mutex` had no `try_lock` (B-2026-11-19-30), so
`self.forks[right].try_lock()` was refused with "no method 'try_lock' on
type 'Mutex'". `Mutex.try_lock` landed at `b8a882bfda`, and the arm
joined as first written.

## Gaps

Two, both fixed.

- B-2026-11-19-30, fixed at `b8a882bfda`: `Mutex` had no `try_lock`,
  which Rust, Go, Java, C and Python each have, and which the back-off
  arm needs.
- B-2026-11-19-31, fixed at `58c8e6269c`: a deadlock among `Mutex` waits,
  which the mutation S1 below produces, was reported as "every task
  waits on a channel that no running task sends to or receives from" on
  every backend, with no location, though no task waits on a channel.
  The report now names the waits and their places: "every task waits on
  a lock or a task that no running task can free; the other tasks wait
  on a lock at ...".

## Differential

`differential.kara` holds copies of the eight arms, each with the
harness's run, and the statement read literally. Every callback yields
the processor (`sleep(Duration.ms(0))`), a pick-up and the meal once
logged and a put-down before, so that the philosophers interleave on the
MIR interpreter too, which runs one task at a time and switches only
when one waits or yields. It draws 300 problems, `n` from 1 to 60 and the five
tasks in a random order, and runs each arm on each problem twice: in
that order and in reverse.

| | property |
|---|---|
| P1 | the statement read literally: a fork picked up only from the table, put down only by its holder, a meal only with both forks |
| P2 | `25 n` calls |
| P3 | each philosopher's own calls come in meals of five: both forks picked up, the meal, both forks put down |
| P4 | every philosopher eats `n` times |
| P5 | every fork back on the table at the end |
| P6 | the tasks started in reverse, the statement read literally |

All 14,400 checks pass on every arm: `300 problems: 1807600 calls, 14400
checks over 8 arms: 0 failures`, under `karac __mir-run`, `karac run`,
`karac build` and the AddressSanitizer build.

## Mutation testing

Sixteen edits to the differential, two to each arm, each run under
`karac __mir-run` and `karac run`, each stopped at 240 s.

| # | mutation | `karac __mir-run` | `karac run` |
|---|---|---|---|
| S1 | ★: every philosopher reaches left first | not caught | deadlock reported |
| S2 | ★: the right fork never locked | P1 300, P6 300 | P1 300, P6 300 |
| T1 | table: the table let go before the forks are put down | P1 300, P6 300 | P1 300, P6 300 |
| T2 | table: the left fork put down twice, the right never | P1 300, P3 300, P6 300 | P1 300, P3 300, P6 300 |
| B1 | butler: five seats | hangs | hangs |
| B2 | butler: the right fork released before it is put down | P1 295, P6 295 | P1 295, P6 295 |
| L1 | lefty: every philosopher reaches left first | deadlock reported | deadlock reported |
| L2 | lefty: the odd philosophers never lock the left fork | P1 217, P6 234 | P1 292, P6 296 |
| P1 | polling: only the left fork looked at | P1 300, P6 300 | P1 300, P6 300 |
| P2 | polling: the forks marked free before they are put down | P1 300, P6 300 | P1 300, P6 300 |
| A1 | atomic: a fork taken by a load and a store | not caught | P1 14, P6 15 |
| A2 | atomic: the right fork's flag never cleared | hangs | hangs |
| C1 | channel: the forks sent back before they are put down | P1 300, P6 300 | P1 300, P6 300 |
| C2 | channel: every philosopher reaches left first | not caught | deadlock reported |
| O1 | back-off: the right fork waited for, not tried | not caught | deadlock reported |
| O2 | back-off: the right fork let go before the meal | P1 300, P6 300 | P1 300, P6 300 |

All sixteen are caught under `karac run`, and twelve under the
interpreter. Nine fail the properties on both. Four deadlock: with
every philosopher reaching for the left fork first (S1, L1, C2), or
waiting for the right one where the back-off arm only tries it (O1),
five of them can each hold one fork and wait for the next, and the
runtime stops with its deadlock report, which names the lock waits and
their places since B-2026-11-19-31. Under the interpreter, which
switches tasks only at a wait or a yield, S1, C2 and O1 take both forks
with no switch between the two, so the cycle never forms there, while
L1 picks up its first fork, a callback that yields, before reaching for
the second, and deadlocks there too. Two hang: with five seats (B1)
every philosopher can hold a left fork and wait for the right, and each
`acquire` waits out its 60 s timeout; with the right fork's flag never
cleared (A2) the next philosopher to want it spins, yielding, forever,
which no deadlock check can see, since nobody waits. B2, P2, C1 and O2
let a fork go before it is put down, a window with no wait in it, and a
callback's yield lets another philosopher take the fork there while the
log still has it in a hand. A1 takes a fork by a load and then a store,
a race the interpreter cannot show, since nothing switches between the
two, and `karac run` catches it in 29 of its 600 runs, the narrowest
margin of the sixteen. L2's counts move from run to run under `karac
run`, as a schedule's do. P3, meals of five, catches T2 alone, which
puts the left fork down twice; P2, P4 and P5 catch none, since a broken
discipline still makes `25 n` calls, `n` meals each, and puts every fork
back.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm over 3 runs of n = 50000, the five tasks started in three orders;
each log is judged by the statement read literally. The ★ arm: a `Mutex`
for each fork, every philosopher taking the lower-numbered of their two
forks first. Philosopher `i`'s left fork is fork `i` and the right fork
is fork `(i + 4) % 5`. Both forks are put down before their locks are
released. Every program prints `3 runs of n = 50000: 3750000 calls, 3
valid`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.895 to 1.089 s | 0.946 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.921 to 1.032 s | 0.974 s |
| Rust (`rustc -O`) | 0.307 to 0.360 s | 0.330 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.311 to 0.349 s | 0.337 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.313 to 0.342 s | 0.332 s |
| C (`clang -O3`) | 0.407 to 0.491 s | 0.444 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.389 to 0.492 s | 0.431 s |
| Go | 0.608 to 0.866 s | 0.726 s |
| Python | 2.501 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra takes about 2.9x Rust with overflow checks on's time (0.974
s against 0.337 s). Kāra takes about 2.2x C's time (0.974 s against
0.444 s); Go is about 25% ahead of Kāra (0.726 s against 0.974 s).
Python takes about 3x Kāra's time. No profile was taken.
