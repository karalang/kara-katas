# 706. Design HashMap

Design a HashMap without using any built-in hash table libraries.
Implement `MyHashMap`: `MyHashMap()` initializes the object with an
empty map; `void put(int key, int value)` inserts a `(key, value)` pair
into the HashMap, and if the `key` already exists in the map, updates
the corresponding `value`; `int get(int key)` returns the `value` to
which the specified `key` is mapped, or -1 if this map contains no
mapping for the `key`; `void remove(key)` removes the `key` and its
corresponding `value` if the map contains the mapping for the `key`.

```
MyHashMap(); put(1, 1), put(2, 2), get(1), get(3), put(2, 1), get(2),
remove(2), get(2)
  ->  null, null, 1, -1, null, 1, null, -1
```

**Constraints:** 0 <= `key`, `value` <= 10^6; at most 10^4 calls will be
made to `put`, `get`, and `remove`.

## Approaches

Every arm is `struct MyHashMap` with `fn new() -> MyHashMap`, `fn
put(mut ref self, key: i64, value: i64)`, `fn get(self, key: i64) ->
i64` and `fn remove(mut ref self, key: i64)`.

| file | mechanism |
|---|---|
| `design_hashmap.kara` ★ | 1,009 buckets (a prime), each a `Vec` of `(key, value)` pairs: `put` replaces the pair of a key its bucket holds or appends one, `get` scans one bucket, `remove` swaps the pair out with the bucket's last |
| `design_hashmap_paged.kara` | a slot for every key from 0 to 1,000,000, holding its value or -1, split into 1,001 pages of 1,000 that are filled with -1 only when a key is first put on them; two indexes a call, and no 8 MB up front |
| `design_hashmap_probing.kara` | open addressing over parallel key and value tables: a key slot is empty, holds a key, or is a tombstone; a search steps on from the key's hash past tombstones, `put` reuses the first tombstone it passed, and the tables double, dropping tombstones, once keys and tombstones fill half |
| `design_hashmap_stdlib.kara` | the stdlib `Map`, a hash map, which the problem rules out; there as a reference, and nothing walks it, so its per-run iteration order never shows |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 8 lines: the LeetCode example; the smallest
and largest keys and values, with a key put twice; removing a key never
put and one twice, and putting it back; keys that share a remainder by
1,009; the problem's most, 10,000 random calls, on keys up to
1,000,000 and on keys below 100, and 5,000 keys put, the odd ones
removed and 2,500 read; and 300 random sequences of 1 to 200 calls on
keys below 1 to 3,000, each with a checksum. `design_hashmap.py` mirrors
the ★ arm and its output is byte-identical.

A first version of the paged arm was one `Vec.filled(1000001, -1)`, the
plainest direct table. It gave the same answers, but the harness builds
about 300 maps, and filling 8 MB for each made it the one arm that took
16 s under `karac __mir-run` against under 1 s for the others; the
differential, which builds 12,000 maps of each arm, would not have
finished inside the corpus's 60 s. The paged arm keeps the idea and
fills only the pages used.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: for each `get`, read
the calls so far back from the newest for the last `put` or `remove` of
that key. 3,000 random sequences are checked, of 1 to 60 calls on key
numbers below a random 1 to 200, with values from 0 to 1,000,000, each
sequence spreading its key numbers one of four ways: as they are, times
1,009 so they share a ★ bucket, times 1,000 so each takes a page of its
own, or counted down from 1,000,000.

| | property |
|---|---|
| P1 | the answers are the definition's |
| P2 | every key k replaced by 1,000,000 - k, the same answers |
| P3 | every value v replaced by 1,000,000 - v, every value read back the same way and every miss still a miss |
| P4 | the same calls followed by a `get` for every key number below the bound, the definition's answers |

It prints `3000 sequences (3001 reads found), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

## Mutation testing

Eleven edits to the differential, two or three to each arm, each run
under `karac __mir-run`. All eleven are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a pair appended though its key is held | P1 260, P4 1300 |
| M2 | ★: a second put keeping the old value | P1 236, P4 1266 |
| M3 | ★: a removal taking the bucket's first pair | P1 65, P4 267 |
| M4 | paged: a new page filled with 0, not -1 | P1 1320, P2 163, P3 1320, P4 1410 |
| M5 | paged: a put at slot k % 999 | P1 673, P2 180, P4 1601 |
| M6 | paged: a read on page k / 1001 | P1 791, P2 1407, P4 1613 |
| M7 | probing: a tombstone ending the search | P1 34, P2 4, P4 198 |
| M8 | probing: a removed key's slot emptied, not marked | P1 38, P2 5, P4 195 |
| M9 | probing: key 0 dropped when the table grows | P1 7, P2 10, P4 112 |
| M10 | stdlib: a missing key read as 0 | P1 2887, P3 2887, P4 2999 |
| M11 | stdlib: a removal that only reads | P1 280, P4 1283 |
| E1 | probing: a different hash multiplier | 0 |
| E2 | ★: 1,013 buckets, not 1,009 | 0 |
| E3 | probing: a new key put in the empty slot, past any tombstone | 0 |

P1 and P4 kill all eleven, P4 most heavily since it reads every key a
sequence could have used. P3 catches the two mutants that invent a value
for a missing key, a fresh page filled with 0 (M4) and the `Map` read
defaulting to 0 (M10): a 0 does not turn into 1,000,000 when every value
is flipped. P2 catches the mutants whose damage depends on the key's
value, such as the wrong page or slot (M5, M6) and the probing table's
lost key 0 (M9). E1 starts the probing search from a different hash,
E2 uses 1,013 buckets in place of 1,009, and E3 puts a new key in the
empty slot that ended its search rather than the first tombstone it
passed; tombstones never stop a search, so the key is still found.

## Verification

Every arm prints the same output as `design_hashmap.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`2bfc20c2ad` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives rebuilt after the last
`runtime/src` change.

The frozen legacy backends refuse the ★ arm, the differential and the
bench program at type checking, at `*k` and `*v` over a bucket's
`iter()` in `get`, since legacy gives those items by value where
v2 gives references; a copy of the bench program without the two `*`s
passes legacy's type checking and then fails in its codegen with
"indexed-receiver `.iter()` requires the outer container to be a named
variable in v1". They refuse the other three arms at `next_random(mut
seed)` inside the harness's `random_calls`, whose `seed` is already a
`mut ref`: legacy wants the marker dropped, while on v2 the marked
forward is the spelling (kara B-2026-10-14-25). Legacy is frozen, so
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, the same in all five languages. Each
of five rounds makes ten maps and feeds each 300,000 random calls, a
third each `put`, `get` and `remove`, on keys below 50,000 with values
below 1,000,000, so a map fills toward half of the keys, about 25 a
bucket; every value read goes into a checksum. Every implementation
prints `5 rounds of 10 maps of 300000 calls: 1887580 found, checksum
322827366`, the Kāra program under `karac __mir-run` included (in
205 s).

Every implementation keeps 1,009 growable arrays of key and value pairs,
`Vec`, slice or list, and C one `realloc`'d block per bucket, and
removes by moving the bucket's last pair into the gap. Spot timings on a
shared 4-core container, eight runs of each compiled program, five of
them interleaved, and two of Python (`bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.70 to 0.76 s |
| Rust (`rustc -O`) | 0.68 to 0.74 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.68 to 0.72 s |
| Go | 0.86 to 0.96 s |
| Python | 31.4 to 32.1 s |
| Kāra (`karac build --mir`) | 0.72 to 0.78 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it, and a copy it
accepts fails in its codegen, as above, so there is no legacy row. That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 3.1 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is about 5% behind C and Rust by median and about 17%
ahead of Go. The comparison with C and Rust waits until after M4.

## Compiler findings

None. `karac check` passed all four arms, the harness, the differential
and the bench program, and every v2 surface agreed.
