# 1636. Sort Array by Increasing Frequency

Given an array of integers `nums`, sort the array in **increasing** order
based on the frequency of the values. If multiple values have the same
frequency, sort them in **decreasing** order.

Return the *sorted array*.

```
nums = [1,1,2,2,2,3]               ->  [3,1,1,2,2,2]
nums = [2,3,1,3,2]                 ->  [1,3,3,2,2]
nums = [-1,1,-6,4,5,-6,1,4,1]      ->  [5,-1,4,4,-6,-6,1,1,1]
```

**Constraints:** `1 <= nums.length <= 100`; `-100 <= nums[i] <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `frequency.kara` ★ | each value counted in a `Map`, then a copy sorted with `sort_by_key(\|x\| (count[x], -x))`: the count smallest first, and on a tie the negated value, so the larger value first. O(n log n) |
| `frequency_buckets.kara` | no comparison sort: the values lie in -100 to 100, so a fixed `Array[i64, 201]` of counters holds every count, and for each count from 1 up the values with it are written out from the largest down. O(n + 201m) for a largest count m |
| `frequency_pairs.kara` | only the distinct values sorted: the counts turned into `(count, value)` pairs, sorted with `sort_by` and a comparator, `a.0.cmp(b.0).then(b.1.cmp(a.1))`, then each value written out as often as it occurs. O(n + d log d) for d distinct values |
| `frequency_solution.kara` | LeetCode's Rust template: counts in a `HashMap`, the array sorted in place by a comparator on the counts with the value reversed as tie-break. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples, one value,
four distinct values, and one value three times; then a checksum for 3000
random arrays of up to 8 values from -3 to 3, 300 of up to 100 from -100
to 100, and 5 of up to 100000 from -100 to 100. `frequency.py` mirrors
the ★ arm and its output is byte-identical. The pairs arm counts in a
`Map`, whose walk order is random per process, and sorts the pairs
before anything is printed; its output is the same under
`KARAC_HASH_SEED` 1, 2 and 3.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the value that comes first is the one that occurs least often
in the array, the largest of those on a tie; take one of it out, and
repeat with what is left, every count read by scanning the whole array.
It checks 3000 random arrays of 1 to 10 values, every other one from -2
to 2, so counts tie often, the rest -20 to 20. Every array is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the order is the statement read literally |
| P2 | the array reversed gives the same order |
| P3 | the order is a rearrangement of the array |
| P4 | every value plus one gives the same order, every value plus one |
| P5 | the counts never fall along the order, and equal counts put larger values first |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 244413828, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. The first M3 tried, every count
starting at 1 rather than 0, survived and is equivalent: one more on
every count keeps their order. It was replaced. A sort that leaves ties
in the order they came (M2, M9) agrees with the literal reading whenever
the input happens to hold them largest first; P2, the array reversed,
catches it more often than P1.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: on a tie, the smaller value first | P1 2428, P5 2428, P6 2428 |
| M2 | ★: the key the count alone, ties left as they came | P1 2061, P2 2368, P5 2061, P6 2061 |
| M3 | ★: every count 1 | P1 1187, P5 1187, P6 1187 |
| M4 | buckets: the values of one count written smallest first | P1 2428, P5 2428, P6 2428 |
| M5 | buckets: the largest count never written | P1 3000, P3 3000, P6 3000 |
| M6 | buckets: each value written once too few | P1 3000, P3 3000, P6 3000 |
| M7 | pairs: the largest count first | P1 1475, P5 1475, P6 1475 |
| M8 | pairs: each value counted once | P1 1562, P3 1562, P5 1187, P6 1562 |
| M9 | template: no tie-break | P1 2061, P2 2368, P5 2061, P6 2061 |
| M10 | template: the value compared first, the count second | P1 1187, P5 1187, P6 1187 |

## Benchmarks

The bench draws 50000 random arrays of 100 values from -100 to 100,
LeetCode's own sizes, all of them first, then sorts each by the ★ arm in
all five languages. Kāra's `sort_by_key` calls its key on every
comparison, as Rust's `sort_by_key` does, so each comparison looks up two
counts in the hash map: Kāra's `Map`, Rust's `HashMap` (both SipHash),
Go's `map` under `sort.SliceStable`, and an open-addressing table
written out in C under `qsort`. Python's `sorted(key=..)` computes each
key once, so its lookups are n rather than n log n; it is the one mirror
that does less work. Every implementation prints `50000 arrays of 100
values: checksum 858247459`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ee08f070a` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.473 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.986 s |
| Rust (`rustc -O`) | 0.990 s |
| Kāra (`karac build`) | 1.154 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.165 s |
| Go | 1.853 s |
| Python | 3.5 s |

The sequential Kāra build takes 1.18x Rust's time and 1.18x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.473 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (1.101 s and
1.135 s on one run).

## Verification

All four arms print the same output as `frequency.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★, buckets and pairs arms checked clean as first written: the key
closure indexing a captured `Map` and negating a borrowed `i32`, the
fixed `[0; 201]` array indexed by `x + 100`, the inclusive `1..=most`,
and a comparator chained with `then`.

LeetCode's Rust template takes one `karac fix` of 20 edits, among them
`HashMap` to `Map` with the `use` line dropped, `for &x in &nums` to
`for x in ref nums`, `cnt[a].cmp(&cnt[b])` to `cnt[a].cmp(cnt[b])`, and
`nums: own Vec[i32]` on both `frequency_sort`s, since
`let mut nums = nums;` takes the array over to sort it in place, and a
bare parameter only borrows. The arm then checks and agrees with no hand
edit.
