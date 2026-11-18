# 1188. Design Bounded Blocking Queue

Implement a thread-safe bounded blocking queue with the following
methods:

- `BoundedBlockingQueue(int capacity)` initializes the queue with a
  maximum capacity.
- `void enqueue(int element)` adds an element to the front of the queue.
  If the queue is full, the calling thread is blocked until the queue is
  no longer full.
- `int dequeue()` returns the element at the rear of the queue and
  removes it. If the queue is empty, the calling thread is blocked until
  the queue is no longer empty.
- `int size()` returns the number of elements currently in the queue.

Your implementation will be tested using multiple threads at the same
time. Each thread will either be a producer thread that only makes calls
to `enqueue` or a consumer thread that only makes calls to `dequeue`. The
`size` method will be called after every test case.

```
capacity 2, 1 producer, 1 consumer
enqueue(1) dequeue() dequeue() enqueue(0) enqueue(2) enqueue(3) enqueue(4) dequeue()
                                                    ->  [1,0,2,2]
capacity 3, 3 producers, 4 consumers
enqueue(1) enqueue(0) enqueue(2) dequeue() dequeue() dequeue() enqueue(3)
                                                    ->  [1,0,2,1]
```

The answer is what each `dequeue` returned, then the final `size`. With
more than one producer or consumer the order is not fixed: the second
example may also give `[0,1,2,1]`, or take `3` before `2`.

**Constraints:** `1 <= Number of Producers <= 8`,
`1 <= Number of Consumers <= 8`, `1 <= size <= 30`,
`0 <= element <= 20`; the number of calls to `enqueue` is greater than or
equal to the number of calls to `dequeue`; at most 40 calls are made to
each of `enqueue`, `dequeue` and `size`.

The arms are a `sync struct BoundedBlockingQueue` with `fn new(capacity:
i64)`, `fn enqueue(self, element: i64)`, `fn dequeue(self) -> i64` and
`fn size(self) -> i64`. LeetCode's threads are a `TaskGroup` with a task
per producer and per consumer; the `i`th enqueue goes to producer `i %
producers` and the `i`th dequeue to consumer `i % consumers`, each task
making its calls in order, and the dequeued values go to a `Vec` behind a
`Mutex`.

## Approaches

The queue is first in, first out: "the front" and "the rear" in the
statement are the two ends of one line, as LeetCode's examples show.

| file | mechanism |
|---|---|
| `bounded_blocking_queue.kara` ★ | two counting semaphores and a lock, as the textbook writes it: `slots` starts with a permit for each place and `items` with none; an enqueue takes a slot, pushes under the lock and gives an item, a dequeue the mirror image |
| `bounded_blocking_queue_channel.kara` | a bounded channel is a bounded blocking queue: `channel(capacity)`, `send` and `recv`, with an atomic count for `size`, exact whenever no call is under way, as when LeetCode asks |
| `bounded_blocking_queue_waitlist.kara` | a monitor, as the Java solutions write it with a `ReentrantLock` and two `Condition`s: the values and two lists of waiting tasks under one lock, each waiter holding a one-shot channel, since the standard library has no condition variable |
| `bounded_blocking_queue_polling.kara` | the values under a lock and nothing to wait on: a call that finds no room, or nothing to take, lets the lock go, sleeps for no time at all and looks again |
| `bounded_blocking_queue_ring.kara` | a ring of `capacity` places with semaphores of free places and of values, as the C solutions write it with an array and `sem_t`s |
| `differential.kara` | the five arms against the statement read literally, seven properties |

Every arm prints the same 5 lines: LeetCode's two examples (`[1,0,2,2]`;
`3 dequeued, size 1, every value accounted for: true`, since the second's
values are not fixed); a queue of one place (`[5,6,7,8,0]`); 40 values
through 30 places with 10 dequeues; and 2000 random runs of up to 8
producers and 8 consumers, a capacity of 1 to 30, up to 40 values and
never more left over than the capacity (`2000 random runs: 11707 left
over, 2000 with every value accounted for, 25 in order with one of
each`). `bounded_blocking_queue.py` mirrors the ★ arm with a thread per
producer and consumer, `threading.Semaphore`s and a `deque`, and its
output is byte-identical.

## Gaps

The kata found three gaps writing a sixth arm, the ★ arm generic over
its element as a library would write it (`sync struct
BoundedBlockingQueue[T: CrossTask]` with `impl[T: CrossTask]`).

- **An impl's `CrossTask` bound refused every type.** Every call on a
  `BoundedBlockingQueue[String]`, or `[i64]`, was refused, "`String` does
  not implement `CrossTask`", where `fn f[T: CrossTask](x: T)` takes a
  `String`: the impl's gate looked for an impl of a bound the compiler
  computes. kara B-2026-11-17-131, fixed in `dd8e046918`.
- **A view stored through a `Mutex` is accepted.** With the harness
  unchanged, `queue.enqueue(v)` for `v` in `mine.iter()` infers `T = ref
  i64`, and the queue keeps views of a slot that has moved on: LeetCode's
  first example prints `[2,2,4,2]`, not `[1,0,2,2]`. A view may not be
  stored in a field of a `sync` type (core semantics §5.7), and the same
  store into a plain `Vec[ref i64]` is refused. kara B-2026-11-17-132,
  open, so the generic arm waits on it and is not here.
- **A struct's type parameter left open inside `Mutex.new(..)` is never
  fixed.** `let h = Holder { values: Mutex.new(VecDeque.new()) }`, its
  `T` fixed by a later `h.put(5)`, stopped at lowering with an internal
  "type does not lower" error. kara B-2026-11-17-133.

## Differential

`differential.kara` holds copies of the five arms, each behind a trait
the checks are generic over (`fn run[Q: BoundedQueue + CrossTask](queue:
Q, ..)`). 400 problems drawn before any arm runs: a capacity of 1 to 30,
up to 8 producers and 8 consumers, up to 40 values of 0 to 20, never more
dequeues than values nor more left than the capacity, busy work of up to
2000 steps before each of up to 5 calls in turn, and up to 40 calls from
one task that never wait.

| | property |
|---|---|
| P1 | the statement read literally: with one producer and one consumer, the dequeues give the first values in the order they went in, and the rest are left |
| P2 | with many of each, every value that went in came out or is left, and the size is the values less the dequeues |
| P3 | with one consumer and busy work, each producer's values come out in its order |
| P4 | with many of each and busy work, every value accounted for |
| P5 | an enqueue on a full queue waits: a task fills it and enqueues one more, and its flag stays down until a dequeue makes room (every tenth problem, after 3 ms) |
| P6 | a dequeue on an empty queue waits for an enqueue, and gets its value (every tenth problem, after 3 ms) |
| P7 | the size after each call of a sequence from one task |

P5 and P6 can only fail a wrong arm: a right one cannot raise its flag
early, however long the wait. All 10,400 checks pass on every arm:
`400 problems: checksum 321959145, 10400 checks over 5 arms: 0
failures`, under `karac __mir-run`, `karac __mir-llvm-run`, `karac
run` and `karac build`. A Python reading of the same problems gives the
same checksum.

## Mutation testing

Eleven edits to the differential, two or three to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run`. All eleven are
caught on both.

| # | mutation | `__mir-run` | `__mir-llvm-run` |
|---|---|---|---|
| M1 | ★: one slot more than the capacity | P5 40 | P5 40 |
| M2 | ★: a dequeue takes the newest value | P1 376, P3 350, P5 39 | P1 373, P3 346, P5 39 |
| M3 | channel: room for one more than the capacity | P5 40 | P5 40 |
| M4 | channel: a dequeue counted twice | P1 383, P2 383, P3 383, P4 383, P5 40, P6 40, P7 383 | P1 383, P2 383, P3 383, P4 383, P5 40, P6 40, P7 383 |
| M5 | waitlist: room when the queue holds the capacity | P5 40 | P5 40 |
| M6 | waitlist: a dequeue takes the newest value | P1 376, P3 350, P5 39 | P1 369, P3 345, P5 39 |
| M7 | polling: room when the queue holds the capacity | P5 40 | P5 40 |
| M8 | polling: a dequeue takes the newest value | P1 376, P3 350, P5 39 | P1 373, P3 345, P5 39 |
| M9 | ring: an enqueue writes one place too far on | P1 382, P2 319, P3 372, P4 319, P5 39, P6 35 | P1 382, P2 364, P3 372, P4 359, P5 39, P6 35 |
| M10 | ring: a dequeue leaves the head where it was | P1 376, P2 376, P3 377, P4 376 | P1 372, P2 375, P3 374, P4 371 |
| M11 | ring: an enqueue not counted | P1 400, P2 400, P3 400, P4 400, P5 40, P6 40, P7 400 | P1 400, P2 400, P3 400, P4 400, P5 40, P6 40, P7 400 |

A queue with one place too many (M1, M3, M5, M7) is caught only by P5:
no other property fills a queue and looks before a dequeue, and the
answers stay right. Taking the newest value (M2, M6, M8) breaks the order
P1 and P3 read, and P5's, whose first dequeue must give the first value;
P2 and P4 compare values as a bag, so they pass it. The ring's faults
(M9 to M11) put values in the wrong place or read one place twice, which
P1 to P4 all see. M4 counts a dequeue twice, so the size comes out short and
the values left are never taken. The two lanes differ by a few failures
on the order mutations, the native one running the tasks at once.

## Verification

Every arm prints the same output as `bounded_blocking_queue.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac run`, a `karac build`
binary, and `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer)
with no error, and so does the differential. `karac check
--output=json` reports nothing on any arm, and `karac fix` has nothing
to apply. The differential took one round of 12 fixes: a `ref` on
`problems[i]`, read only, and eleven `.clone()`s dropped from arguments
a bare parameter borrows.

## Benchmarks

`bench/` times the ★ arm against the same algorithm in C, Rust, Go and
Python: 100 rounds, each a fresh queue of 16 places through which 4
producers enqueue 2500 values each and 4 consumers dequeue 2500 each.
Every program prints `100 rounds of 4 producers and 4 consumers moving
10000 values through 16 places: checksum 339850330`, a fold of each
round's dequeued sum. Each is two counting semaphores and a lock over a
deque: the standard library's `Semaphore` in Kāra and Python's
`threading.Semaphore`, POSIX `sem_t` in C, and in Rust and Go, whose
standard libraries have none, a count under a mutex with a condition
variable. Each language starts a thread or task per producer and per
consumer, 8 a round.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python (user is the median CPU
time in user mode, summed over the threads), with karac `dd8e046918` on
LLVM 22:

| | time | median | user |
|---|---|---|---|
| Go | 0.608 to 0.698 s | 0.662 s | 1.790 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.347 to 1.627 s | 1.518 s | 3.418 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.429 to 1.821 s | 1.614 s | 2.125 s |
| Rust (`rustc -O`) | 1.475 to 1.899 s | 1.619 s | 2.230 s |
| Kāra (`karac build`) | 1.274 to 1.841 s | 1.712 s | 3.754 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 1.430 to 1.917 s | 1.751 s | 2.772 s |
| C (`clang -O3`) | 1.735 to 1.967 s | 1.792 s | 0.925 s |
| C (`clang -O3 -march=x86-64-v3`) | 1.659 to 1.848 s | 1.806 s | 0.847 s |
| Python | 11.408 s | | 6.145 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. The work is hand-offs: every value wakes a consumer and every
dequeue a producer, a million of each over a run. Kāra is level with
Rust and a little ahead of C. Go is about 2.3x faster than Kāra, its
goroutines handing off inside its own scheduler. C spends the least user
time and the most wall time: its threads sleep in the kernel between
hand-offs. Kāra's user time is about 2.2x its wall time, its pool's
workers staying busy between hand-offs, as in kata 1117; it was not
traced further. Python takes about 7.5x Kāra's time.
