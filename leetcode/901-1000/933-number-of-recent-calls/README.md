# 933. Number of Recent Calls

You have a `RecentCounter` class which counts the number of recent
requests within a certain time frame.

Implement the `RecentCounter` class:

- `RecentCounter()` initializes the counter with zero recent requests.
- `int ping(int t)` adds a new request at time `t`, where `t` represents
  some time in milliseconds, and returns the number of requests that has
  happened in the past 3000 milliseconds (including the new request).
  Specifically, return the number of requests that have happened in the
  inclusive range `[t - 3000, t]`.

It is guaranteed that every call to `ping` uses a strictly larger value
of `t` than the previous call.

```
ping(1), ping(100), ping(3001), ping(3002)  ->  1, 2, 3, 3
```

**Constraints:** `1 <= t <= 10^9`; each test case will call `ping` with
strictly increasing values of `t`; at most `10^4` calls will be made to
`ping`.

## Approaches

| file | mechanism |
|---|---|
| `recent_counter.kara` ★ | a queue of the recent pings in a `VecDeque`: each ping pushed at the back, pings older than `t - 3000` dropped from the front, and the queue's length is the answer. O(1) a call amortized |
| `recent_counter_search.kara` | every ping kept in a `Vec`; the pings in the window run from the first at or after `t - 3000`, found by binary search, to the end. O(log n) a call |
| `recent_counter_stacks.kara` | a queue made of two stacks: pings pushed on an inbox, the oldest on top of an outbox refilled from the whole inbox when it runs empty; old pings popped from the outbox, and the answer is what is left in both. O(1) a call amortized |
| `recent_counter_start.kara` | every ping kept in a `Vec` with the index of the oldest one in the window, which only moves forward, since `t - 3000` only grows. O(1) a call amortized |
| `recent_counter_back.kara` | every ping kept in a `Vec`, counted back from the newest while at or after `t - 3000`. O(k) a call for `k` pings in the window |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's example and six more (a
ping at the largest time, pings exactly 3000 apart, 3001 apart, one a
millisecond, a burst, a gap and a burst, and pings that keep landing on
the window's edge); for 300 random streams of up to 2,000 pings, each
ping from 1 to a random gap of up to 6,000 after the one before, the
answers' sum and a checksum; and three streams of LeetCode's largest,
10,000 pings: one a millisecond, one every 1,000, and random gaps up to
100,000, each answer summed. `recent_counter.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for each ping, every request so far, the new one included,
counted when its time is in `[t - 3000, t]`. It checks 3,200 random
streams, each ping from 1 to a random gap of up to 6,000 after the one
before: 3,000 of 1 to 30 pings against the statement, and 200 of 1 to
2,000 against the other properties; 245,173 calls in all.

| | property |
|---|---|
| P1 | the statement's answers, on the small streams |
| P2 | one answer a ping, each from 1 to one more than the answer before, and 1 exactly when the ping before is more than 3000 earlier |
| P3 | the same answers with every time moved later by a random amount up to 10^6 |
| P4 | a random prefix answers as the stream's first pings did, and a ping 3001 after it answers 1 |
| P5 | the stream played backwards, each time `t` becoming `first + last - t`, has answers with the same sum, since each pair of pings within 3000 is counted once either way |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 streams, 245173 calls, answers summing to 3509621, 95000
checks over 5 arms: 0 failures` under `karac __mir-run` (26 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: at most one ping dropped a call | P1 2264, P2 1164, P4 2753, P5 2323, P6 2462 |
| M2 | ★: a window of 2000 | P1 2500, P2 1679, P6 2699 |
| M3 | ★: a ping at time 0 there from the start | P1 2593, P2 2755, P3 2671, P5 1356, P6 2755 |
| M4 | search: one more than the pings found | P1 3000, P2 3200, P4 3200, P6 3200 |
| M5 | search: a window of 300 | P1 2835, P2 2860, P6 3035 |
| M6 | search: a window of 6000 | P1 2464, P2 1220, P4 3200, P6 2662 |
| M7 | stacks: the inbox never counted | P1 2894, P2 3094, P5 1373, P6 3094 |
| M8 | stacks: the outbox refilled with one ping left | P1 2464, P2 1220, P4 3200, P5 1807, P6 2662 |
| M9 | stacks: the outbox never counted | P1 2292, P2 2490, P5 1373, P6 2490 |
| M10 | start: a window of 1000 | P1 2694, P2 2372, P6 2893 |
| M11 | start: a window of 4000 | P1 2400, P2 1152, P4 3200, P6 2598 |
| M12 | start: a window of 3001 | P1 35, P2 14, P4 3200, P6 140 |
| M13 | back: a ping exactly 3000 earlier left out | P1 38, P2 21, P6 136 |
| M14 | back: the first ping never counted | P1 3000, P2 3200, P5 1807, P6 3200 |
| M15 | back: a window of 100 | P1 2872, P2 3018, P6 3072 |

P1, P2 and P6 kill all fifteen, P4 and P5 six each, and P3 one. P2's
rule that an answer is 1 exactly when the ping before is over 3000
earlier sees every wrong window, even M12 and M13, which differ from the
right answers only when two pings are exactly 3000 or 3001 apart. P3
kills only M3: every other mistake depends on the differences between
times, which moving them all leaves alone, while M3's ping at time 0
falls out of reach once the times move. P4 kills the six that still
count a ping 3001 earlier (the wide windows M6, M11 and M12, M8's
outbox, which stops dropping once it has refilled out of order, and M1,
which falls behind) or count one too many (M4); a narrow window still
answers 1 there. P5 kills the six whose miscount is not the same either
way round: the counts that leave out the inbox or the outbox (M7, M9),
the first ping (M14) or a ping at time 0 (M3), and the queues that drop
too little (M1, M8). A wrong window is the same window played backwards,
so P5 misses those.

Twelve other edits were tried and set aside. Four failed exactly the
same checks as M13, the same mistake written in each of the other arms;
three the same as M1 or M12, written in other arms (start passing at
most one ping, and ★ and back with a window of 3001); and three the same as M4
(★ leaving the new ping out, start one short and back starting its count
at 1). One was equivalent (search ending its range one short, which
never matters since the new ping is always in the window) and one was
sound but beyond three an arm (stacks with a window of 3002).

## Verification

Every arm prints the same output as `recent_counter.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 1.6 to 2.6 s each, except back at
7.5 s, which counts every ping in the window on each call; the
differential takes 26 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

Legacy refuses all five arms, the differential and the bench program at
the first `*` on an element of a `Vec[i64]`'s `.iter()` ("unary '*'
requires 'ref T', ... found 'i64'"), legacy's older rule; under v2 the
element is a reference and the `*` is required. Legacy is frozen, so
none of this is filed.

A first ring arm (3001 time slots stamped with each ping's time, the
times that left the window cleared on each call) gave the right output
but took 94 s under `karac __mir-run`, since each call can visit up to
3001 slots; it was replaced by the start arm.

## Benchmarks

The bench program builds 100 streams of 10,000 pings once, LeetCode's
largest, each ping from 1 to a gap after the one before, the gap from 1
to 600 for each stream, so the window holds from about 10 to 3,000
pings; in each of 50 rounds it plays every stream into a new ★ counter,
each round starting from a different stream. Every implementation
prints `50 rounds over 100 streams of 10000 pings: answers summing to
2331137100, checksum 809360549`. Rust uses a `VecDeque`, Python a
`deque`, C a ring buffer whose size is a power of two, doubled when
full, as `VecDeque` does, and Go a slice with the front resliced away.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.39 to 0.45 s | 0.41 s |
| Rust (`rustc -O`) | 0.51 to 0.57 s | 0.53 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.52 to 0.58 s | 0.54 s |
| Go | 0.71 to 0.81 s | 0.78 s |
| Python | 9.07 s | |
| Kāra (`karac build --mir`) | 1.46 to 1.58 s | 1.51 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about 22 times C's.

v2 takes 2.80 times Rust's median time under overflow checks and 3.70
times C's. Under valgrind's cachegrind v2 runs 11.41 billion
instructions and 1.90 billion branches, 100 million of them indirect,
with 40.8 million mispredicted; Rust with overflow checks runs 2.45
billion, 0.51 billion with 76,000 indirect, and 40.2 million; C 1.23
billion, 0.20 billion and 39.1 million. The mispredictions are the same
in all three, so the gap is in the instructions: 4.7 times Rust's. About
two indirect branches for each of the 50 million pings suggest the
`VecDeque` calls are not inlined; that is inferred, not profiled.
