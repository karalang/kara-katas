# 705. Design HashSet

Design a HashSet without using any built-in hash table libraries.
Implement `MyHashSet`: `void add(key)` inserts the value `key` into the
HashSet; `bool contains(key)` returns whether the value `key` exists in
the HashSet or not; `void remove(key)` removes the value `key` in the
HashSet, and if `key` does not exist in the HashSet, does nothing.

```
MyHashSet(); add(1), add(2), contains(1), contains(3), add(2),
contains(2), remove(2), contains(2)
  ->  null, null, true, false, null, true, null, false
```

**Constraints:** 0 <= `key` <= 10^6; at most 10^4 calls will be made to
`add`, `remove`, and `contains`.

## Approaches

Every arm is `struct MyHashSet` with `fn new() -> MyHashSet`, `fn
add(mut ref self, key: i64)`, `fn remove(mut ref self, key: i64)` and
`fn contains(self, key: i64) -> bool`.

| file | mechanism |
|---|---|
| `design_hashset.kara` ★ | 1,009 buckets (a prime), each a `Vec` of the keys with that remainder: `add` appends a key its bucket lacks, `remove` swaps it out with the bucket's last key, `contains` scans one bucket |
| `design_hashset_bits.kara` | a bitmap with one bit for every key from 0 to 1,000,000, 15,626 words of 64 bits, about 122 KiB; O(1) for each call whatever the number of keys |
| `design_hashset_probing.kara` | open addressing: one table of slots that are empty, hold a key, or are tombstones for a removed key; a search steps on from the key's hash past tombstones, `add` reuses the first tombstone it passed, and the table doubles, dropping tombstones, once keys and tombstones fill half of it |
| `design_hashset_stdlib.kara` | the stdlib `Set`, a hash set, which the problem rules out; there as a reference, and nothing walks it, so its per-run iteration order never shows |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 9 lines: the LeetCode example; the smallest
and largest keys; removing a key never added and one twice, and adding
one back; keys that share a remainder by 1,009 and by 64, the sizes two
arms lean on; the problem's most, 10,000 random calls, on keys up to
1,000,000 and on keys below 100, and 5,000 keys added, the odd ones
removed and 2,500 looked up; and 300 random sequences of 1 to 200 calls
on keys below 1 to 3,000, each with a checksum. `design_hashset.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: a list of the keys
held, in no order, searched from end to end on every call. 1,000 random
sequences are checked, of 1 to 60 calls on key numbers below a random
1 to 200, each sequence spreading its key numbers one of four ways: as
they are, times 1,009 so they share a ★ bucket, times 64 so they share a
bit position, or counted down from 1,000,000.

| | property |
|---|---|
| P1 | the answers are the definition's |
| P2 | every key k replaced by 1,000,000 - k, the same answers |
| P3 | every `add` and `remove` made twice in a row, the same answers to the `contains` calls |
| P4 | the same calls followed by a `contains` for every key number below the bound, the definition's answers |

It prints `1000 sequences (956 lookups found), 4 arms, 16000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`. It runs 1,000 sequences rather than
3,000 because every one builds each arm's set 16 times, and the bitmap
is 15,626 words to fill each time: at 3,000 the differential took 57 s
under `karac __mir-run`, at the corpus's 60 s limit.

## Mutation testing

Eleven edits to the differential, two or three to each arm, each run
under `karac __mir-run`. All eleven are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a key added again though its bucket holds it | P1 22, P4 78 |
| M2 | ★: a lookup in the next bucket | P1 423, P4 972 |
| M3 | ★: a removal taking the bucket's first key | P1 27, P3 26, P4 100 |
| M4 | bits: a key set at bit k % 63 | P1 299, P2 55, P4 818 |
| M5 | bits: a removal flipping the bit, not clearing it | P1 392, P3 411, P4 951 |
| M6 | bits: a lookup in word k / 65 | P1 343, P2 338, P4 779 |
| M7 | probing: a tombstone ending the search | P1 22, P2 3, P4 67 |
| M8 | probing: a removed key's slot emptied, not marked | P1 22, P2 3, P4 67 |
| M9 | probing: key 0 dropped when the table grows | P1 4, P2 5, P4 36 |
| M10 | stdlib: one above the key looked up | P1 471, P2 264, P4 972 |
| M11 | stdlib: a removal that only looks | P1 85, P4 419 |
| E1 | probing: a different hash multiplier | 0 |
| E2 | ★: 1,013 buckets, not 1,009 | 0 |
| E3 | probing: a new key put in the empty slot, past any tombstone | 0 |

P1 and P4 kill all eleven; P4 most heavily, since it looks up every key
a sequence could have used. P3 catches the removals that do the wrong
thing when repeated: taking the bucket's first key (M3) and flipping a
bit rather than clearing it (M5). P2 catches the mutants whose damage
depends on the key's value, such as the bitmap's wrong bit or word
(M4, M6) and the probing table's lost key 0 (M9). E1 starts the probing
search from a different hash; any start finds the key, since the search
runs on to an empty slot. E2 uses 1,013 buckets in place of
1,009. E3 puts a new key in the empty slot that ended its search rather
than the first tombstone it passed; the key is still found, because
tombstones never stop a search.

## Verification

Every arm prints the same output as `design_hashset.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`79a6c2eb9a` for the debug build and `9297cca254` for the release build
that runs `check` and `__mir-run`, which differ in no `src` or `runtime`
file, with runtime archives rebuilt after the last `runtime/src` change.

The frozen legacy backends refuse three arms at type checking, at
`next_random(mut seed)` inside the harness's `random_calls`, whose
`seed` is already a `mut ref`: legacy wants the marker dropped, while on
v2 the marked forward is the spelling (kara B-2026-10-14-25). They
refuse the probing arm and the differential at `*s` over
`self.slots.iter()` in `grow`, since legacy gives those items by value
where v2 gives references. Legacy builds the bench program as it is and
prints the same line, but takes 222 to 235 s over four runs, more than
300 times the v2 build. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, the same in all five languages. Each
of five rounds makes ten sets and feeds each 300,000 random calls, a
third each `add`, `remove` and `contains`, on keys below 50,000, so a
set fills toward half of them, about 25 keys a bucket; every answer goes
into a checksum. Every implementation prints `5 rounds of 10 sets of
300000 calls: 1885915 found, checksum 934664639`, the Kāra program under
`karac __mir-run` included (in 261 s).

Every implementation keeps 1,009 growable arrays of keys, `Vec`, slice
or list, and C one `realloc`'d block per bucket, and removes by moving
the bucket's last key into the gap. Spot timings on a shared 4-core
container, eight runs of each compiled program, five of them
interleaved, four of the legacy build and two of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.62 to 0.69 s |
| Rust (`rustc -O`) | 0.55 to 0.68 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.57 to 0.60 s |
| Go | 0.78 to 0.87 s |
| Python | 19.4 to 19.9 s |
| Kāra (`karac build --mir`) | 0.65 to 0.76 s |
| Kāra, legacy (`karac build`) | 222 to 235 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` builds the same file, and
its row is above. That edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 3.1 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

So the v2 build is about 5% behind C by median, 20% behind Rust either
way, and 20% ahead of Go; legacy is far behind, as above. The comparison
with C and Rust waits until after M4.

## Compiler findings

None. `karac check` passed all four arms, the harness, the differential
and the bench program as first written, and every v2 surface agreed.
