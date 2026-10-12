# 432. All O`one Data Structure

Design a data structure that stores strings with their counts and can
return the strings with the smallest and the largest count.

- `AllOne()` makes an empty structure.
- `inc(key)` adds 1 to the count of `key`, inserting it with count 1
  if it is not there.
- `dec(key)` takes 1 from the count of `key`, and removes it when the
  count reaches 0. The key is present before every `dec`.
- `getMaxKey()` returns one of the keys with the largest count, or `""`
  when there are none.
- `getMinKey()` returns one of the keys with the smallest count, or
  `""` when there are none.

Every function must run in O(1) average time.

```
inc("hello"), inc("hello")
getMaxKey()  ->  "hello"
getMinKey()  ->  "hello"
inc("leet")
getMaxKey()  ->  "hello"
getMinKey()  ->  "leet"
```

**Constraints:** `1 <= key.length <= 10`, lowercase English letters;
at most `5 * 10^4` calls in all.

## Approaches

Each arm is a `struct AllOne` with the five operations as methods
(`get_max_key` and `get_min_key` in Kāra's naming); keys come in as
`Str` and are stored as `String`.

| file | mechanism |
|---|---|
| `all_one.kara` ★ | a doubly linked list of buckets in ascending count order between two sentinels, each bucket the set of keys with its count, and a map from key to bucket. `inc` and `dec` move a key to the neighbouring bucket, linking in a new one if that count has none, and unlink a bucket left empty. The buckets are a `shared struct` with strong `next` links and `weak` `prev` links, so the list holds no cycle and frees itself. O(1) |
| `all_one_sorted.kara` | a map from key to count, and a `SortedMap` from count to the set of keys with it; the queries take the sorted map's last and first entries. O(log n) |
| `all_one_arena.kara` | the bucket list of the ★ arm with the buckets in a vector, linked by index; an unlinked bucket's slot goes on a free list for reuse. O(1), with no reference counting |
| `all_one_scan.kara` | a map from key to count, and queries that scan every key. O(1) updates, O(n) queries: the plain reference |
| `differential.kara` | the four arms on 1,500 random scripts, five properties |

The problem lets a query return any key with the extreme count, and
which one a set of keys yields depends on its iteration order, which
varies from run to run. So the harness keeps its own count of every
key and checks each answer against it: the answer's count must be the
largest (or smallest), and the answer `""` exactly when no key is
present. It prints the key when it is the only one with that count,
and otherwise only the count and how many keys share it, so the output
is the same on every run and in every arm.

Every arm prints the same 8 lines: the LeetCode example, six edge
scripts (queries on an empty structure, a key added and removed,
counts that pass each other, ties at both ends), and for 20,000 random
operations on 50 keys the number of queries, failures, keys left,
their total count and a checksum of the answers. `all_one.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms, each renamed, and
runs all four on the same 1,500 random scripts. Each answer is checked
against plain counts the harness keeps, as in the arms' own harness.
A script runs in five phases, one per property:

| | property |
|---|---|
| P1 | max answers among random incs and decs on 1 to 8 keys |
| P2 | min answers in that same random phase |
| P3 | answers as every key is lowered to nothing, ending empty |
| P4 | answers on a staircase, key i raised to count i + 1, then each key lowered once |
| P5 | answers as a present key is raised past every other count, then lowered back |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | bucket list: a new bucket one count too high | P1 759, P2 801, P3 1458, P4 1500, P5 1009 |
| M2 | bucket list: `dec` leaves an emptied bucket linked | P1 538, P2 159, P3 1231, P4 1482, P5 1432 |
| M3 | sorted map: the min query starts at count 2 | P2 1092, P3 736, P4 1500, P5 843 |
| M4 | sorted map: an emptied count stays in the sorted map | P1 538, P2 650, P3 1231, P4 1482, P5 1432 |
| M5 | vector: the max query reads the lowest bucket | P1 917, P3 811, P4 1264, P5 1150 |
| M6 | vector: `inc` leaves an emptied bucket linked | P2 602, P3 107, P5 741 |
| M7 | scan: the max scan never raises its best count | P1 855, P3 691, P5 1043 |
| M8 | scan: `dec` keeps a key at count 0 | P2 482, P3 1458, P4 236, P5 205 |

The random phase asks max and min separately, so a mutant that only
breaks one query fails only P1 or only P2 there (M3, M5 to M8). M6
leaves an empty bucket below the key it moved, which only the min
query can reach. M8 keeps a key at count 0 that only shows when it is
the smallest, so the max query never notices it. M2 and M4 both leave
an empty count behind and fail alike, except that M4's shared `shift`
also leaves one behind on `inc`, which shows in P2. Two first picks
for the vector arm were replaced: a reused slot keeping its old count,
and an unlink that leaves the next bucket's `prev` pointing at the
freed slot, both let two buckets share a slot, so a key loses its count
and a later `dec` of a present key panics, ending the run.

## Verification

All four arms print the same output as `all_one.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak, so the `weak`
back links leave no cycle behind.

The frozen legacy front end (`karac run --interp`, LLJIT, `karac build`
and `KARAC_AUTO_PAR=1 karac build`) rejects every file, the bench
program included, at type checking: it does not take a `Str` where a
`String`-keyed map or set looks a key up (`expected 'String', found
'StringSlice'`), and it types `*m.get(k).expect(...)` as a deref of an
`i64`. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It runs 2,000,000 random operations
on 10,000 keys, `k0` to `k9999`: half `inc`, three in ten `dec` of a
key that is present (an `inc` when the drawn key is not), and one in
ten each `getMaxKey` and `getMinKey`. Which key a query returns
depends on set iteration order, so the program keeps its own count of
each key and folds the count of every answer into a checksum; that
count is the same whichever key the structure picks. Every
implementation prints `2000000 operations on 10000 keys: 400299
queries, checksum 572577989`; a 100,000-operation cut of the Kāra
program under `karac __mir-run` prints the same as the C program cut
the same way.

The mirrors keep the ★ arm's structure: Rust's buckets are
`Rc<RefCell<Bucket>>` with a `Weak` back link, and its `HashMap` and
`HashSet` hash with SipHash-1-3 under a random key, as Kāra's `Map`
and `Set` do; Go uses its maps for both. C has no hash table to hand,
so its key-to-bucket map is an open-addressing table of key text, and a
bucket's keys are an array of entries that each know their position,
removed by a swap with the last: the same O(1) operations, with no
hashing per bucket and no reference counts, which is most of its lead.
Spot timings on a shared 4-core container, three runs each (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.14 to 0.15 s |
| Rust (`rustc -O`) | 0.46 to 0.51 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.47 to 0.59 s |
| Go | 0.49 to 0.61 s |
| Python | 2.9 to 3.0 s |

The frozen legacy `karac build` cannot build the program (see
Verification), so there is no legacy time. The Kāra program prints the
same line under `karac __mir-llvm-run` in 14 s, compile included; that
JITs the MIR's IR without optimization passes, so it is not a
benchmark. Dropping the queries does not shorten it, so the time is in
`inc` and `dec`.

## Compiler findings

One new finding, filed as kara B-2026-10-12-20, and two known gaps; the
finding and the first gap are fixed.

- **B-2026-10-12-20 (fixed).** The ★ arm's `link_after(at: Bucket,
  count)` first stores `at` in the new bucket's `weak` `prev` field and
  then links `at.next` to the new bucket. `karac check` refused that as
  a use after move: storing a parameter in a `weak` field counted as
  moving it, whether the parameter was bare, `ref` or `own`. The same
  two statements on local bindings checked clean, as did a strong store
  of the parameter, and `karac __mir-run` ran the refused program
  correctly. The arm made the `weak` store last until kara f70fec32cd
  fixed it; it is back in its first order.
- **B-2026-10-12-9 (fixed).** The harness and the scan arm walk a count
  map with `for (_, c) in counts`. The library's iteration table gives
  `c` the type `ref i64`, and `karac check` accepted `*c`, but
  `karac __mir-run` refused it ("found 'i64'"), so the files used `c`
  bare. Kara 09efbb8db0 fixed it and the files read `*c` again.
- **The MIR borrow checker is not part of `karac check` yet.** The ★
  arm's `dec` first held the bucket it got from
  `self.bucket_of.get(key)` while removing the key from that map.
  `karac check` passed it; `karac __mir-run` refused it (E0516, a
  mutable borrow of `bucket_of` while it is borrowed), which is right,
  as in Rust. The arm takes its own handle with `.clone()`. Thread A
  has this class in hand (see katas 382 and 400).

Two smaller things, not filed. `counts[key]` with a `Str` key on a
`Map[String, i64]` is refused, while `counts.get(key)` takes the view;
the library documents view lookups for the named methods only, not for
indexing. And `self.tail.prev.expect(...)` draws the
`chained_field_receiver` error, a lint for a limit of the frozen legacy
code generator, so the queries bind `self.tail` to a local first.
