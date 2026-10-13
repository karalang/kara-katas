# 460. LFU Cache

Design a least frequently used (LFU) cache. `LFUCache(capacity)`
creates it; `get(key)` returns the key's value if it is cached and
`-1` otherwise; `put(key, value)` sets or inserts the value. When a put
of a new key finds the cache full, it first evicts the least frequently
used key, and of several with the same count, the least recently used
one. A key's use count starts at 1 when it is inserted and goes up with
every `get` or `put` on it. Both calls must run in O(1) on average.

```
LFUCache(2); put(1, 1); put(2, 2); get(1) -> 1; put(3, 3); get(2) -> -1;
get(3) -> 3; put(4, 4); get(1) -> -1; get(3) -> 3; get(4) -> 4
```

**Constraints:** `1 <= capacity <= 10^4`; `0 <= key <= 10^5`;
`0 <= value <= 10^9`; at most `2 * 10^5` calls.

## Approaches

Every arm is a `struct LFUCache` with `fn new(capacity: i64)`,
`fn get(mut ref self, key: i64) -> i64` and
`fn put(mut ref self, key: i64, value: i64)`.

| file | mechanism |
|---|---|
| `lfu_cache.kara` ★ | the nodes live in one `Vec` and link by index; the keys used `c` times form a circular list behind a sentinel node of their own, oldest first, and `least` is the smallest count whose list is not empty. A use moves a node to the next count's list; an eviction takes the first node of `least`'s list and is reused for the new key. O(1) a call |
| `lfu_cache_buckets.kara` | a `Map` from key to value, count and last-use time, and for each count a `SortedMap` from time to key; the oldest key of the `least` bucket is evicted. O(log capacity) |
| `lfu_cache_set.kara` | one `SortedSet` of (count, time, key), whose first element is the key to evict. O(log capacity) |
| `lfu_cache_scan.kara` | the plain reference: a `Vec` of (key, value, count, time), searched from the front, and scanned for the least (count, time) to evict. O(capacity) |
| `differential.kara` | the four arms on 1,500 random sessions, five properties |

Every arm prints the same 8 lines: the answers of the gets in the
LeetCode example, in a one-key cache, after a put to a cached key (which
counts as a use), on a tie broken toward the older key, on misses, with
one frequent key that outlives newer ones, and with puts that count as
uses, and for 300 random sessions (capacity 1 to 10 or to 100, 1 to 300
calls over keys up to twice the capacity, half of them gets) how many
gets hit and a checksum. `lfu_cache.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random sessions.

| | property |
|---|---|
| P1 | on capacity 1 to 4, keys 0 to 5 and 1 to 40 calls, the answers are brute force's, which keeps the history of every successful call and, at each eviction, recounts each cached key's uses since it was last inserted |
| P2 | with room for every key, a get returns the key's last put |
| P3 | renaming the keys keeps the answers |
| P4 | adding a constant to every value adds it to every hit and leaves the misses |
| P5 | with capacity 1, a get hits exactly the key put last |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | buckets: the newest key of the least count is evicted | P1 313 |
| M2 | buckets: a put to a cached key is not a use | P1 297 |
| M3 | set: a use does not advance the clock | P1 36 |
| M4 | set: the cache holds one key too many | P1 762, P5 1168 |
| M5 | ★: the least count moves up while keys remain at it | P1 422 |
| M6 | ★: the newest key of the least count is evicted | P1 313 |
| M7 | scan: a tie goes to the newest key | P1 313 |
| M8 | scan: a put to a cached key is not a use | P1 246 |

P1, the only property that knows which key to evict, sees all eight.
P2 to P5 test what any cache must do (no eviction with room for every
key, names and values passed through untouched, one slot) and so see
only M4, the one mutant that holds the wrong number of keys. M1, M6 and
M7 break the tie the same way and fail the same 313 sessions. M3 is
the faintest: with the clock standing still on a use, two keys can share
a time, and their tie is then broken by key order in the set; it errs
only when such a tie decides an eviction.

A first M1, which kept a bucket emptied by an eviction, survived: the
emptied bucket is never the least one again, because every put of a new
key resets `least` to 1. It was an equivalent mutant and was replaced.

## Verification

All four arms print the same output as `lfu_cache.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`.
The differential prints `30000 checks, 0 failures` on both. The four
arms and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

`karac check` passes the ★ and scan arms and refuses the buckets and set
arms and the differential, on `*time`, `*victim` and `*first`: check
types the items of `iter().next()` by value, where the library spec's
iteration table makes them `ref` (B-2026-10-06-74, below). The arms keep
the spec's form.

On the frozen legacy backends the ★ and scan arms match under
`karac run --interp`. LLJIT and `karac build` stop in the legacy code
generator on the harness's index into an array literal ("Index operator
applied to non-array type"). The buckets and set arms and the
differential stop on the same lines as check. The bench program builds
and matches under legacy `karac build`. Legacy is frozen, so this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm: one cache of 4,096 keys and
10,000,000 calls, each on the product of two random numbers below 200
(so small keys, and 0 above all, come up often), half of them puts of a
random value and half gets. Every implementation prints `10000000 calls
on a cache of 4096: 2848332 hits, checksum 37853023`, the Kāra program
under `karac __mir-run` included (in 86 s).

The mirrors keep the ★ arm's structure: nodes in one array linked by
index, a sentinel per count, a hash map from key to node and one from
count to sentinel. Rust's `HashMap` hashes with SipHash-1-3, as Kāra's
`Map` does by default; Go's map uses its own hash, Python's dict hashes
an integer to itself, and C has no hash map, so the C mirror carries a
small open-addressing one with a multiplicative hash. Spot timings on a
shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.30 to 0.33 s |
| Rust (`rustc -O`) | 0.73 to 0.81 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.70 to 0.75 s |
| Go | 0.81 to 0.89 s |
| Python | 16.7 to 17.2 s |
| Kāra (legacy `karac build`) | 1.07 to 1.21 s |
| Kāra (`karac build --mir`) | 1.04 to 1.18 s |

The hash maps carry the work in every language, and C's is the
cheapest hash of the lot. Under `karac build --mir`, callgrind on a
500,000-call run puts 70% of the instructions under
`karac_mir_map_find`, the hashed `Map`'s lookup, which hashes each key
more than once (B-2026-10-12-29, filed from kata 454). That took the
run to 1.85 to 2.04 s; the row above is re-timed at kara `5f01de4c5c`,
after the fix in `8acdc0bdb5`, and the callgrind share was measured
before it. Under
`karac __mir-llvm-run` the program prints the same line in 20 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

- **B-2026-10-13-1** (stdlib, open): `Map.keys()` / `values()` and
  `SortedMap.keys()` / `values()` return a `Vec` where the library spec
  says `impl Iterator`, so `m.keys().next()` is refused on every front
  end, and the smallest key of a `SortedMap` costs a copy of all of
  them. The buckets arm takes the oldest entry with
  `self.buckets[least].iter().next()`, also in the spec; with this fixed
  it can go back to `let Some(time) = self.buckets[least].keys().next()`.
- **B-2026-10-06-74** (`karac check`, open, widened by this kata):
  `c.iter().next()` yields its item by value under check, for every
  collection, so `*k` is refused; the MIR backends follow the spec and
  type it `ref`, except for `VecDeque`. The buckets and set arms keep
  `*time`, `*victim` and `*first`.
- `Map.get_mut`, the spec's way to change a value in place, does not
  exist yet (B-2026-10-12-3); the arms write `self.entries[key].count =
  ...` through `IndexMut`, which the spec also offers.
