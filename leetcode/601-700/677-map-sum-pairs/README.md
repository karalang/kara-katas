# 677. Map Sum Pairs

Design a map from strings to numbers with two calls: `insert(key, val)`
sets a key's value, replacing any value it had, and `sum(prefix)`
returns the total of the values of all keys that start with the prefix.

```
insert("apple", 3)
sum("ap")   -> 3
insert("app", 2)
sum("ap")   -> 5
```

**Constraints:** keys and prefixes of 1 to 50 lowercase letters; values
from 1 to 1,000; at most 50 calls.

## Approaches

Every arm is a `struct MapSum` with `new()`, `insert(mut ref self, key:
own String, val: i64)` and `sum(ref self, prefix: String) -> i64`. The
key is `own`, since every arm keeps it.

| file | mechanism |
|---|---|
| `map_sum_pairs.kara` ★ | a `Map` from key to value; a sum walks every key and adds those that start with the prefix, in the map's order, which a sum does not depend on; O(keys * prefix) a sum |
| `map_sum_pairs_trie.kara` | a trie whose every node holds the sum of the values below it; an insert adds the change in the key's value along its path, and a sum reads the node the prefix ends at; O(length) a call |
| `map_sum_pairs_prefixes.kara` | a `Map` from every prefix of every key to its sum, updated by the change on each insert; a sum is one lookup; O(length^2) an insert |
| `map_sum_pairs_sorted.kara` | the keys sorted; a sum finds the first key not below the prefix by binary search and adds while the keys start with it; O(log n) plus the keys touched |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 7 lines: the LeetCode example; a key replaced,
and a prefix longer than every key; keys that are prefixes of each
other; a key replaced by a smaller value; a sum before any insert, and
the largest value; keys of 50 letters, the problem's longest; and a
checksum of 15,000 random calls in 300 runs of 50. The first six are
printed as LeetCode prints the calls' results. `map_sum_pairs.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which answers each sum by reading the calls before it backwards, taking
each key's last value, and comparing the first letters of each key with
the prefix. 400 random scripts of 50 calls, the problem's most, half
inserts and half sums, with words of up to 6 letters over 2 to
4 letters, are each played into every arm, then probed on their final
state.

| | property |
|---|---|
| P1 | every sum is the definition's |
| P2 | no sum is below 0 or above 1,000 for each key inserted |
| P3 | a prefix's sum is its own key's value, if any, plus the sums of the prefixes one letter longer |
| P4 | the final keys inserted afresh, in another order, give the same sums |
| P5 | a key inserted again with its current value changes no sum |

It prints `400 scripts (10047 sums), 4 arms, 8000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: keys that are prefixes of the prefix summed | P1 333, P3 377 |
| M2 | ★: keys counted, not their values | P1 400 |
| M3 | trie: a replaced value left in the sums | P1 339, P2 67, P3 134, P4 180, P5 74 |
| M4 | trie: each node set to the change, not added to | P1 398, P2 257, P3 154, P4 158, P5 74 |
| M5 | prefixes: the whole key left out of its prefixes | P1 392, P3 42 |
| M6 | prefixes: a replaced value left in the sums | P1 339, P2 67, P3 134, P4 180, P5 74 |
| M7 | sorted: a replaced value added to the old one | P1 339, P2 67, P3 134, P4 180, P5 74 |
| M8 | sorted: every key from the prefix on summed | P1 400, P3 323 |
| E1 | trie: the root's sum not kept | 0 |
| E2 | ★: the key's length tested before the prefix | 0 |
| E3 | prefixes: the empty prefix summed too | 0 |
| E4 | sorted: a key found as not above its place's key | 0 |

P1 kills all eight. M3, M6 and M7 make one mistake in three arms,
keeping a replaced value in the sums, and fail the same checks: P2 sees
sums grow past 1,000 a key, P4 sees the history matter where only the
final values should, and P5 sees a repeated insert change a sum.
M2, which counts keys instead of adding values, breaks only P1, since a
count obeys every other property too. M1, M5 and M8 sum the wrong set of
keys, which P3 sees where the set stops splitting by the next letter.
The four survivors cannot change an answer: no prefix is empty, so the
trie's root and the empty prefix are never asked for; `starts_with`
already fails a key shorter than the prefix; and at the first place not
below the key, the key there equals it exactly when the key is not below
it.

## Verification

Every arm prints the same output as `map_sum_pairs.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`5e4d49c205` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives newer than the last
`runtime/src` change.

The frozen legacy backends refuse every arm under the interpreter, the
JIT and `karac build`. The harness passes `parts[1]`, an element of a
`Vec[String]`, to `sum`, and legacy stops at `E_INDEX_MOVE_NON_COPY`,
where v2 borrows it (a bare parameter borrows since D5). They run the
differential to the same line under the interpreter and `karac build`.
`karac build` warns there that `key` is moved and used again, and builds
anyway. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the sorted arm, since C has no map: it is the one
arm that is the same algorithm in all five languages. Each of 100 rounds
makes a new map, inserts 2,000 keys of up to 12 letters over `a` to `c`,
then asks 2,000 sums of prefixes of up to 3 letters, all from the same
generator in every language. That is far past the problem's 50 calls, so
the sums have keys to add. Each sum goes into a checksum. Every
implementation prints `100 rounds of 2000 inserts and 2000 sums:
checksum 769201556`, the Kāra program under `karac __mir-run` included
(in 44 s).

Each implementation is the same binary search, shifting insert and
prefix scan, with its strings allocated by the generator, so this
measures string comparison, the shifts and the allocator. Spot timings
on a shared 4-core container, three runs each (five more, interleaved,
for the two Kāra rows, and two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.23 to 0.24 s |
| Rust (`rustc -O`) | 0.19 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.21 to 0.23 s |
| Go | 0.25 to 0.29 s |
| Python | 6.7 to 7.9 s |
| Kāra (`karac build --mir`) | 0.35 to 0.39 s |
| Kāra, legacy (`karac build`) | 0.22 to 0.31 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the frozen legacy `karac build` builds it too, and
its row is above. Under `karac __mir-llvm-run` the program prints the
same line in 4.0 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

So the v2 build is about 1.5 times legacy, which is the M2 bar. It is
also about 1.6 times C and Rust under `overflow-checks=on`, while Go is
level with legacy. Under callgrind, 45% of the v2 binary's instructions
are spent inside `karac_mir_str_test`. That is the runtime call that
every `starts_with` and String `<` makes, where legacy tests the length
and calls memcmp inline. It is filed as kara B-2026-10-15-55. The
comparison with C and Rust waits until after M4.

## Compiler findings

B-2026-10-15-55 (perf, open): on the MIR compiled backend,
`starts_with`, `contains`, `ends_with` and String `<` each call out to
the runtime, where legacy inlines a length test and memcmp. The bench
makes 48.2M such calls. Their own cost is 45% of its instructions, and
it runs at about 1.5 times legacy.

Otherwise, all four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends.
