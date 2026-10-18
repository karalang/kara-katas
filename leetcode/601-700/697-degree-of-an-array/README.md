# 697. Degree of an Array

Given a non-empty array of non-negative integers `nums`, the degree of
the array is the highest number of times any one of its elements
appears. Return the smallest possible length of a (contiguous) subarray
of `nums` that has the same degree as `nums`.

```
nums = [1, 2, 2, 3, 1]        ->  2    (degree 2; [2, 2] is shortest)
nums = [1, 2, 2, 3, 1, 4, 2]  ->  6    ([2, 2, 3, 1, 4, 2])
```

**Constraints:** 1 <= `nums.length` <= 50,000; 0 <= `nums[i]` < 50,000.

## Approaches

Every arm is `fn find_shortest_sub_array(nums: Vec[i64]) -> i64`. A
shortest subarray with the degree holds every copy of some most frequent
value, so it runs from that value's first place to its last; each arm
finds those spans and takes the shortest among the most frequent values.

| file | mechanism |
|---|---|
| `find_shortest_sub_array.kara` ★ | one pass fills three `Map`s, count, first place and last place of each value; a walk over the counts keeps the highest count, ties going to the shorter span; O(n) time, O(d) space for d distinct values |
| `find_shortest_sub_array_table.kara` | the same with three `Vec`s of 50,000 indexed by value, read in a second pass over the values; O(n + 50,000), no hashing |
| `find_shortest_sub_array_running.kara` | one pass and no second walk: each value's span so far is its place less its first place, plus one; a count above the degree so far takes over the answer, a count equal to it keeps the shorter span; O(n) time, O(d) space |
| `find_shortest_sub_array_sorted.kara` | the places 0 to n - 1 sorted by value, ties by place, so each value's places form one block in increasing order; a block's length is the count and its ends the span; O(n log n) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 5 lines: the two LeetCode examples; one
element, five distinct values, two values tied for the degree with
different spans, and the largest value at both ends; one value
50,000 times, 0 to 49,999 once each, and 0 to 24,999 then back down,
where the answer is the middle pair; and 100 random arrays of up to
20,000 values drawn from up to 50,000 values, with a checksum.
`find_shortest_sub_array.py` mirrors the ★ arm and its output is
byte-identical. The ★ arm walks a `Map`, whose order changes from run to
run, but every tie for the degree is settled by the shorter span, and
two tied values with the same span give the same answer, so the output
does not depend on the order.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: find the whole
array's degree, then try every subarray, each start growing its run one
value at a time with its own counts, and keep the shortest whose degree
is the array's. 500 random arrays of 1 to 30 values are checked, each
drawn from 1 to 12 values starting at a random base, so a small range
gives many copies: 155 of the arrays have two or more values tied for
the degree, and 52 have every value distinct. The table arm clears three
tables of 50,000 on every call, so the count is kept to 500 for `karac
__mir-run` to finish well inside the corpus runner's 60 s.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | read backwards, the answer is the same |
| P3 | every value x renamed 49,999 - x, the answer is the same |
| P4 | a value the array does not hold added at the end, the answer is the same |

It prints `500 arrays, 4 arms, 8000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: ties for the degree not broken by span | P1 78, P2 68 |
| M2 | ★: the first place moved on every copy | P1 448 |
| M3 | ★: each span one short | P1 500 |
| M4 | table: a later value with the same count always wins | P1 63, P3 110 |
| M5 | table: a value first seen at place 0 seen again as new | P1 207, P2 221 |
| M6 | table: the last place never moves | P1 448 |
| M7 | running: ties never shorten the answer | P1 32, P2 70 |
| M8 | running: ties lengthen the answer | P1 113 |
| M9 | running: a new degree takes the prefix, not the span | P1 225, P2 279 |
| M10 | sorted: equal values ordered last place first | P1 448 |
| M11 | sorted: each span one short | P1 500 |
| M12 | sorted: a later value with the same count always wins | P1 63, P3 110 |

P1 kills all twelve. A mutant that gets every span wrong fails all
500 arrays (M3, M11), or the 448 that hold a value twice
(M2, M6, M10). P2 sees the mutants that treat the two ends of the array
unlike: ties settled by which value came first or last (M1, M7), a value
at place 0 counted afresh when it comes back (M5), and a new degree
answered with the whole prefix (M9). P3 sees the mutants that settle
ties by value order, the table and sorted arms letting a larger value
with the same count win (M4, M12), since renaming reverses value order.
P4 sees none: a fresh value at the end has a count of 1, which none of
the mutants mishandles. M1 walks a `Map`, so its counts vary from run to
run; the walk order decides which tied value it keeps.

## Verification

Every arm prints the same output as `find_shortest_sub_array.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`ec489d962f` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives rebuilt after the last
`runtime/src` change.

The frozen legacy backends refuse the ★ and running arms and the
differential at type checking, at `*c` on what `Map.get` returns: legacy
gives the value, not a reference, while on v2 it is a reference. They
run the table and sorted arms under `karac run` and `karac build`,
`KARAC_AUTO_PAR=1` included, with the same output; under `karac run
--interp` both pass the first four lines and time out at 60 s in the
100 random arrays. They build the bench program as it is. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the table arm, the same in all five languages; C
has no hash map, and the table arm is what a C program would write. It
builds 40 arrays of 50,000 values once, array k drawing its values from
0 up to 1 + 1,250 k, so the first holds one value 50,000 times and the
last nearly every value once; then in each of 20 rounds it answers every
array, putting each answer into a checksum. Every call allocates and
clears its three tables, as the arm does. Every implementation prints
`20 rounds of 40 arrays of 50000: shortest spans sum to
32143440, checksum 116695374`, the Kāra program under `karac __mir-run`
included (in 31 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.50 to 0.57 s |
| Rust (`rustc -O`) | 0.42 to 0.49 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.44 to 0.52 s |
| Go | 0.43 to 0.50 s |
| Python | 7.8 to 8.2 s |
| Kāra (`karac build --mir`) | 0.38 to 0.49 s |
| Kāra, legacy (`karac build`) | 0.31 to 0.35 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` builds the same file, and
its row is above. That edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 1.8 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

So the v2 build is behind legacy here, level with Rust and Go, and ahead
of C. Why both Kāra builds beat C on this workload has not been looked
into; the time is mostly random reads and writes into three tables of
400 KB each. The comparison with C and Rust waits until after M4.

## Compiler findings

None. `karac check` passed all four arms, the harness, the differential
and the bench program as first written.
