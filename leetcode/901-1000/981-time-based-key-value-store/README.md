# 981. Time Based Key-Value Store

Design a time-based key-value data structure that can store multiple
values for the same key at different time stamps and retrieve the key's
value at a certain timestamp.

Implement the `TimeMap` class:

- `TimeMap()` Initializes the object of the data structure.
- `void set(String key, String value, int timestamp)` Stores the key
  `key` with the value `value` at the given time `timestamp`.
- `String get(String key, int timestamp)` Returns a value such that
  `set` was called previously, with `timestamp_prev <= timestamp`. If
  there are multiple such values, it returns the value associated with
  the largest `timestamp_prev`. If there are no values, it returns `""`.

```
["TimeMap", "set", "get", "get", "set", "get", "get"]
[[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4],
 ["foo", 4], ["foo", 5]]
->  [null, null, "bar", "bar", null, "bar2", "bar2"]
```

**Constraints:** `1 <= key.length, value.length <= 100`; `key` and
`value` consist of lowercase English letters and digits;
`1 <= timestamp <= 10^7`; all the timestamps of `set` are strictly
increasing; at most `2 * 10^5` calls will be made to `set` and `get`.

## Approaches

| file | mechanism |
|---|---|
| `time_map.kara` ★ | a list per key, binary search: each key keeps its (timestamp, value) pairs in a list, sorted by appending since the timestamps only grow, and a get binary searches for the last timestamp at or before the one asked. O(1) set, O(log n) get |
| `time_map_sorted.kara` | a sorted map per key: each key keeps a `SortedMap` from timestamp to value, and a get asks it for the floor of the timestamp. It does not rely on the timestamps growing. O(log n) set and get |
| `time_map_scan.kara` | a list per key, scanned back: the same lists, but a get walks back from the newest pair to the first at or before the time asked. O(1) set, O(n) get |
| `time_map_pairs.kara` | one sorted map keyed by (key, timestamp): every key's pairs sit together in one `SortedMap`, oldest first, and the floor of (key, timestamp) is the answer when it still belongs to the same key. O(log n) set and get |
| `time_map_log.kara` | one log of every set: every set is appended to a single list whatever its key, and a get reads all of it, keeping the pair for its key with the largest timestamp at or before the one asked. O(1) set, O(n) get over all keys |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 15 lines. The first twelve are gets on one
map: LeetCode's example (bar, bar, bar2, bar2); foo at time 0, before
its first set (empty); bar, a key never set (empty); then love set to
high at 10 and low at 20 and asked at 5 (empty), 10, 15, 20 and 25
(high, high, low, low); and foo again at 25 (bar2). Empty answers are
printed in brackets. The last three are counts of values found and
checksums of every answer over random sessions, in which a set's
timestamp is 1 to 3 past the last and a get asks a random time up to 3
past the last set: 300 sessions of 12 calls on 2 keys (926 values
found), 3,000 of 60 calls on up to 8 keys (62,509) and 4 of 3,000
(5,929). `time_map.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a get tries every time from the one asked down to 1, and at
each looks through every set so far for one of its key at that time;
the first found is the value with the largest `timestamp_prev <=
timestamp`. It checks 3,200 sessions: 3,000 of 1 to 30 calls on up to
3 keys against the statement and 200 of 300 calls on up to 8 against
the other properties. Sets come one, two or three times in four by
turns, and timestamps step by 1, by up to 3 or by up to 20 (up to 1,000
in the long sessions); each value carries its timestamp, so no two sets
store the same value.

| | property |
|---|---|
| P1 | the statement's answers, on the first 3,000 sessions |
| P2 | the keys renamed, by a random permutation of names that sort in a different order, some a prefix of another, give the same answers |
| P3 | later sets never change an earlier answer: every get asked again at the end, at its own time or, if that is past the last set before it, at that set's time, answers as it did |
| P4 | each key's calls alone, on a fresh map, give that key's answers |
| P5 | at the end every set's value is found at its own timestamp, and nothing one tick before a key's first set |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 sessions of 106400 calls: 53177 gets, 40612 values
found, checksum 874323409, 95000 checks over 5 arms: 0 failures` under
`karac __mir-run` (27.6 s) and `karac __mir-llvm-run`, and the same
under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-nine edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first pair at the time, not after it | P1 1448, P3 1643, P5 3073, P6 1587 |
| M2 | ★: the search moves one too far down | P1 1483, P3 1957, P5 2720, P6 1683 |
| M3 | ★: each set starts the key afresh | P1 1762, P3 1860, P5 2720, P6 1962 |
| M4 | sorted: the ceiling for the floor | P1 2472, P3 2483, P5 2440, P6 2672 |
| M5 | sorted: one tick later asked | P1 1272, P3 1302, P5 2885, P6 1409 |
| M6 | sorted: a time before every pair answers the first | P1 1233, P3 1865, P5 2440, P6 1415 |
| M7 | scan: the first pair never read | P1 1963, P5 3073, P6 2161 |
| M8 | scan: the latest value once any is old enough | P1 1762, P3 2221, P5 2720, P6 1962 |
| M9 | scan: the last pair never read | P1 2038, P3 1860, P5 3073, P6 2224 |
| M10 | pairs: the key never checked | P1 995, P2 1064, P3 1382, P4 1158, P5 1572, P6 1158 |
| M11 | pairs: the key compared by its length | P1 716, P2 918, P3 1112, P4 865, P5 1401, P6 865 |
| M12 | pairs: only another key matches | P1 2524, P2 1064, P3 1382, P4 1158, P5 3073, P6 2724 |
| M13 | log: any key matches | P1 1574, P4 1746, P5 1800, P6 1746 |
| M14 | log: the first match kept | P1 1931, P5 2720, P6 2131 |
| M15 | log: nothing at time 1 ever kept | P1 961, P5 1387, P6 1047 |

P1, P5 and P6 kill all fifteen, P3 eleven (all but M7, M13, M14 and
M15), P4 four (M10 to M13) and P2 three (M10 to M12). P2 and P4 can
see only an edit that lets one key's pairs answer for another: the ★,
sorted and scan arms keep each key in a map of its own, so the key's
name and the other keys' calls never reach its answers, and only
pairs, which orders every key in one map, and log, which keeps every
key in one list, have a key check to break. P3 misses the edits whose
wrong answer is the same at the end as when first asked, such as
reading the oldest match (M14) or never the first pair (M7). M6 fails
P3 because a get on a key not yet set answers `""`, but asked again at
the end, once the key has pairs, all later than the time asked, it
answers the first of them.

Fourteen other edits were tried and set aside. Nine failed exactly the
same checks as a kept one: sorted, scan, pairs and log each never
finding the time asked itself, as M1; sorted and scan starting the key
afresh at each set, as M3; pairs taking the ceiling, as M4, and asking
one tick later, as M5; and sorted answering `none` when nothing is
found, as M6, since both change only the answer before a key's first
pair. Three were sound but beyond three an arm: ★ never finding the
first pair (the checks M7 fails) and stopping its search one short;
and pairs matching a key that begins the one asked, which the statement
never sees: its sessions use foo, bar and love, none of which begins
another, and only the renamed keys (k and key, a and ab) and the long
sessions, which hold both k and key2, show it (P2 203, P3 41, P4 37,
P5 50, P6 37). Two are equivalent: log keeping the last match rather
than the latest, and log never raising the best time it has seen. The
log holds the sets in the order they came, which is the order of their
timestamps, so the last match at or before the time asked is the
latest either way.

## Verification

Every arm prints the same output as `time_map.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `e04ae2b46b`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` the arms
take 1.5 s (★, sorted and scan) to 4.9 s (log), and the differential
27.6 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

The arms were first written with `set(mut ref self, key: String, ...)`,
a bare parameter, which borrows. Handing it on as `Map.entry`'s owned
key, or inside a tuple pushed onto a list, is refused with a type
mismatch, `expected 'String', found 'ref String'`, which suggests
`.clone()` for the key and nothing for the tuple, where pushing the
bare parameter itself gets a message that names the parameter and
offers `own`. The arms take `own String`, as a setter that stores its
arguments should; the missing hint is kara's `B-2026-10-24-30`.

## Benchmarks

The bench runs the ★ arm in all five languages on LeetCode's largest
sessions. Each of 20 rounds builds a fresh map and makes 200,000
calls on 1,000 keys, a set or a get by turns of a coin: a set's
timestamp is 1 to 3 past the last and its value one of 100, and a get
asks a random time up to 3 past the last set. Every get's answer is
folded into a checksum. Every implementation prints `20 rounds of
200000 calls on 1000 keys: 1825591 values found, checksum 48288503`.

The implementations do not copy the same strings. Kāra and Rust copy
the key and the value into every set, the key's copy dropped when the
key is already there, and copy the value out of every get that finds
one, as the signatures `set(key: own String, ...)` and `get(...) ->
String` ask. C copies a key only the first time it is set and a value
into every set, and returns the stored value without copying it. Go
and Python share their immutable strings and copy nothing. The maps
differ too: Kāra's `Map` and Rust's `HashMap` hash with SipHash-1-3, C
uses open addressing on an FNV-1a hash, and Go and Python their own
built-in maps.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `e04ae2b46b`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.474 to 0.615 s | 0.526 s |
| Rust (`rustc -O`) | 0.561 to 0.700 s | 0.622 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.548 to 0.671 s | 0.602 s |
| Go | 0.409 to 0.498 s | 0.449 s |
| Python | 8.5 s | |
| Kāra (`karac build --mir`) | 0.509 to 0.647 s | 0.595 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 14 times
Kāra's.

v2 took 0.99 times Rust's median time under overflow checks and 1.13
times C's. Under valgrind's cachegrind v2 ran 3,514 million
instructions and 453 million branches with 16.9 million mispredicted,
Rust with overflow checks 3,233 million, 428 million and 16.6 million,
and C 2,272 million, 302 million and 18.8 million. v2 and Rust do the
same copies through the same hash, and v2 runs 9% more instructions
for about the same time. Go is the fastest of the compiled four,
which fits its copying no strings at all (inferred, not measured).
