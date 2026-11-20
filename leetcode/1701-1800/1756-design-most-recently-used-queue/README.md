# 1756. Design Most Recently Used Queue

*Premium problem.* Design a queue-like data structure that moves the
most recently used element to the end of the queue.

Implement the `MRUQueue` class:

- `MRUQueue(int n)` constructs the `MRUQueue` with `n` elements:
  `[1, 2, 3, ..., n]`.
- `int fetch(int k)` moves the `k`-th element **(1-indexed)** to the end
  of the queue and returns it.

```
MRUQueue(8)    [1, 2, 3, 4, 5, 6, 7, 8]
fetch(3)  ->  3    [1, 2, 4, 5, 6, 7, 8, 3]
fetch(5)  ->  6    [1, 2, 4, 5, 7, 8, 3, 6]
fetch(2)  ->  2    [1, 4, 5, 7, 8, 3, 6, 2]
fetch(8)  ->  2    [1, 4, 5, 7, 8, 3, 6, 2]
```

**Constraints:** `1 <= n <= 2000`; `1 <= k <= n`; at most `2000` calls
to `fetch`.

Kāra's naming rule treats an acronym as a word in a type name, so the
class is `MruQueue` here.

## Approaches

| file | mechanism |
|---|---|
| `mru.kara` ★ | the queue is a `Vec` of its values in order; a fetch removes the k-th value, shifting the rest down one, and pushes it on the end. O(n) per fetch |
| `mru_buckets.kara` | the values in buckets of about the square root of n: a fetch walks the buckets' lengths to the one holding the k-th value, removes it there and pushes it on the last bucket, and every `size` fetches the buckets are cut afresh. O(sqrt n) per fetch, amortized |
| `mru_fenwick.kara` | every value in a slot, the first n in order and one more for each fetch at the end; a Fenwick tree counts the occupied slots, and the k-th value is found by descending its powers of two. A fetch empties that slot and fills the next free one. O(log(n + fetches)) per fetch |
| `mru_deque.kara` | the queue is a `VecDeque`, whose `remove` shifts whichever side of the k-th value is shorter; the value goes back with `push_back`. O(min(k, n - k)) per fetch |
| `differential.kara` | the four arms against the statement read literally, five properties |

The problem is premium, so there is no LeetCode Rust template; a fourth
Kāra arm stands in its place.

Every arm prints the same 5 lines: LeetCode's example, then one value
fetched twice, and the last place fetched twice and then the first;
then the sum of every value fetched and a checksum for 3000 random
queues of up to 6 values with 6 fetches each, and 100 of up to 2000
values with 2000 fetches each, LeetCode's limits. `mru.py` mirrors the ★
arm and its output is byte-identical.

```
[3, 6, 2, 2]
[1, 1]
[4, 4, 1, 2]
3000 queues of up to 6 values, 6 fetches each: fetched values add to 41204, checksum 284964321
100 queues of up to 2000 values, 2000 fetches each: fetched values add to 88040910, checksum 961670300
```

## Differential

`differential.kara` holds copies of the four arms, each type renamed, and
the statement read literally: the queue starts as 1 to n, and each fetch
builds the next queue as every value but the k-th, in order, then the
k-th. It checks 3000 random queues of 1 to 8 values, each given 1 to 10
fetches at random places. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | every fetch returns what the statement read literally returns |
| P2 | a fetch of the last place right after any fetch returns its value again |
| P3 | after the fetches, fetching the first place n times gives back each of 1 to n exactly once |
| P4 | n more fetches of the first place give the same values in the same order |
| P5 | each arm's fetched values agree with at least two of the other three |

The differential prints `3000 problems: checksum 306083509, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading, the queue as a list with `pop` and `append`, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Three first edits were replaced: two
that read past the end of a bucket or of the Fenwick tree and stopped
with an index panic rather than a wrong answer, and one equivalent, the
Fenwick descent starting from a power of two half as large, which still
reaches every slot the differential's queues use.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the fetched value put back at the front | P1 2373, P2 2613, P3 2613, P5 2373 |
| M2 | ★: the k-th place counted from the back | P1 2575, P2 2613, P3 2613, P5 2575 |
| M3 | ★: the value returned but not moved | P1 2200, P2 2514, P3 2613, P5 2200 |
| M4 | buckets: the fetched value pushed on the first bucket | P1 1884, P2 2185, P3 2136, P4 1690, P5 1884 |
| M5 | buckets: the value copied out, not removed | P1 2200, P2 2514, P3 2613, P5 2200 |
| M6 | buckets: each bucket's values read backwards when they are cut afresh | P1 2580, P2 1334, P3 2418, P4 2110, P5 2580 |
| M7 | fenwick: the new slot counted twice | P1 1663, P2 2272, P3 1964, P4 2559, P5 1663 |
| M8 | fenwick: the old slot left counted | P1 2200, P2 2514, P3 2613, P5 2200 |
| M9 | deque: the fetched value put back at the front | P1 2373, P2 2613, P3 2613, P5 2373 |
| M10 | deque: the k-th place taken modulo n, so the last fetch takes the first | P1 2613, P2 2613, P3 2613, P4 2202, P5 2613 |

## Benchmarks

The bench draws 2000 random fetch places first, then builds 10000
queues of 2000 values, LeetCode's limits, and runs the same 2000 fetches
on each by the ★ arm in all five languages: every fetch shifts the
values after the k-th down one, `Vec.remove` in Kāra and Rust, `memmove`
in C and `copy` in Go. Every implementation prints `10000 queues of 2000
values, 2000 fetches each: fetched values add to 19314190000, checksum
296905912`. The C build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `21cdf88b69` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.686 s |
| Rust (`rustc -O`) | 0.737 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.750 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.753 s |
| Kāra (`karac build`) | 0.754 s |
| Go | 1.647 s |
| Python | 5.4 s |

The sequential Kāra build is level with Rust and level with Rust with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C is the fastest here at 0.686 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.744 s and
0.745 s on one run).

## Verification

All four arms print the same output as `mru.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

Every arm first named its type `MRUQueue`, as LeetCode does, and `karac
check` flagged it under Kāra's naming rule for acronyms; one `karac fix`
per arm renamed it `MruQueue` at every use, 8 or 9 edits with the arm's
others. The ★ and Fenwick arms took nothing else.

The buckets arm first gathered its values with
`self.buckets.iter().flatten()`. Kāra's `flatten` wants items that are
iterators themselves, and a `ref Vec[i32]` is not one; the same `karac
fix` wrote `.flat_map(|v| v.iter())`.

The deque arm first wrote `self.values.remove(k as i64 - 1).unwrap()`,
as Rust's `VecDeque::remove` returns an `Option`. Kāra's returns the
value and panics out of bounds, as `Vec.remove` does, and `karac check`
refused the `.unwrap()` with a bare `no method 'unwrap' on type 'i32'`
and no fix. Since kara `21cdf88b69` (B-2026-11-20-106) the message names Kāra's `remove`
and the same `karac fix` dropped the `.unwrap()`.

The differential took one `karac fix` of 12 edits: an `as i64` on each
`i32` fetch pushed into a `Vec[i64]`, which widens by itself, was
dropped. The bench checked clean as written.
