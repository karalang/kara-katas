# 659. Split Array into Consecutive Subsequences

Given a sorted array `nums`, decide whether it can be split into
subsequences, every number used exactly once, each of which is a run of
consecutive integers (each one more than the one before) at least
3 long.

```
nums = [1,2,3,3,4,5]      ->  true   ([1,2,3] and [3,4,5])
nums = [1,2,3,3,4,4,5,5]  ->  true   ([1,2,3,4,5] and [3,4,5])
nums = [1,2,3,4,4,5]      ->  false
```

**Constraints:** 1 to 10,000 numbers from -1,000 to 1,000, sorted
ascending.

## Approaches

Every arm is `fn is_possible(nums: Vec[i64]) -> bool`. All four rest on
the same fact: a number that can extend a sequence ending just before it
should, because that sequence's needs come first.

| file | mechanism |
|---|---|
| `split_array_into_consecutive_subsequences.kara` ★ | two `Map[i64, i64]`s, the numbers not yet placed and the sequences ending at each value; a number extends one of those, or starts a new sequence and takes the next two numbers at once; O(n) |
| `split_array_into_consecutive_subsequences_heaps.kara` | a `Map[i64, PriorityQueue[i64]]` of the lengths of the sequences ending at each value; a number extends the shortest, and every sequence is checked at the end; O(n log n) |
| `split_array_into_consecutive_subsequences_runs.kara` | each value with its count, and only three numbers of state: how many sequences end just before it with length 1, 2, and 3 or more; O(n) time, O(1) space |
| `split_array_into_consecutive_subsequences_scan.kara` | a `Vec` of the open sequences as `(end, length)` structs, the shortest extended, a sequence closed once it falls behind; O(n * open sequences) |
| `differential.kara` | the four arms against a search, five properties |

Every arm prints the same 14 lines: the three LeetCode examples; six
more (one number; three in a row; three with a gap; two runs on the same
values; one run that must be cut in two; and a run that leaves two
numbers short), each with its answer; how many of 300 random arrays
split, half of them made of runs, with a checksum; and four arrays of
the problem's size: runs cut to 10,000 numbers, runs that fit, the same
with one number repeated, and one value 10,000 times.
`split_array_into_consecutive_subsequences.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition, a
search with no greed in it: the smallest number left must start a
sequence, so try every length of 3 or more that the numbers left allow,
take that sequence out, and split what remains. Each of 1,000 random
sorted arrays has 1 to 15 numbers. Half are runs of 3 to 5, every fourth
with a number then dropped or repeated, and half are numbers at random
from 0 to 5.

| | property |
|---|---|
| P1 | the answer is the search's |
| P2 | adding the same number to every element changes nothing |
| P3 | the numbers negated give the same answer |
| P4 | an array that splits still splits with a run of three added |
| P5 | an array that splits still splits with every number twice |

It prints `1000 arrays (7912 numbers, 371 can be split), 4 arms,
20000 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a new sequence started with only the next number there | P1 97, P3 97, P4 15 |
| M2 | ★: a new sequence recorded as ending one short | P1 251, P3 76, P4 6 |
| M3 | heaps: an extended sequence keeping its old length | P1 371 |
| M4 | heaps: sequences of 2 allowed | P1 142 |
| M5 | runs: the long sequences extended dropped from the count | P1 171, P3 3, P4 24 |
| M6 | runs: a gap allowed after sequences of 2 | P1 3, P3 5, P4 2 |
| M7 | scan: the longest open sequence extended first | P1 124, P4 94 |
| M8 | scan: an extended sequence growing by 2 | P1 142 |
| E1 | ★: a used-up number recognised by a count of 0 or less | 0 |
| E2 | heaps: the check written as at most 2 | 0 |
| E3 | runs: the first value given a wider gap before it | 0 |
| E4 | scan: a sequence closed one number later | 0 |

P1 kills all eight; M3, M4 and M8, which only miscount lengths, nothing
else sees. P3 sees the four that treat the start of a sequence
differently from its end, M1, M2, M5 and M6, since reading the numbers
backwards swaps the two. P4 sees those four and M7 when an added run
lands where they go wrong. P2 and P5 see none: no arm looks at a
number's value except against its neighbours, and every mutant that
splits an array also splits it doubled. The four survivors cannot change
an answer: no count goes below 0; at most 2 is less than 3; any gap
before the first value starts it afresh; and a sequence that falls
behind can never grow again, so closing it one number later only delays
the same check.

## Verification

Every arm prints the same output as
`split_array_into_consecutive_subsequences.py` under `karac __mir-run`
(the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs clean
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer):
output identical, no error, no leak. The differential prints its line
under all three. `karac check` passes all four arms, the differential
and the bench program. All with the compiler at kara `8d40e1a762` for
the debug build and `057e29e74f` for the release build that runs `check`
and `__mir-run`, with runtime archives newer than the last `runtime/src`
change.

The frozen legacy backends do less well. Their `karac build` and JIT
crash with a segmentation fault on the heaps arm, a `Map` of
`PriorityQueue`s; their interpreter runs it and the differential, but
takes over 60 s on the ★ and scan arms. The other arms and the
differential build, with ownership warnings that `count` and
`is_possible` take their arguments owned, and print the same output.
Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes eight sorted arrays once,
each of 25,000 runs of 3 to 5 consecutive numbers starting anywhere from
0 to 20,000, the odd ones with a lone 30,000 at the end that no sequence
can take, so they are refused only at their last number; then 40 rounds
each ask whether one, picked by the round, splits, and put the answer
into a checksum. Every implementation prints `8 arrays, 40 rounds:
20 split, checksum 385317749`, the Kāra program under `karac __mir-run`
included (in 32 s).

Each implementation is the same greedy over two hash maps: Kāra's `Map`
and Rust's `HashMap`, both SipHash; Go's built-in map; Python's dict;
and in C, which has no map, two tables of open addressing with linear
probing under a multiplicative hash, made fresh for each call. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine), each including making the
arrays:

| | time |
|---|---|
| C (`clang -O3`) | 0.27 to 0.30 s |
| Rust (`rustc -O`) | 0.40 to 0.44 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.42 to 0.56 s |
| Go | 0.54 to 0.57 s |
| Python | 1.7 to 1.8 s |
| Kāra (`karac build --mir`) | 0.49 to 0.55 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program: its parameters are still owned rather than borrowed, so handing
`arrays[pick]` to `is_possible` moves an element out of a `Vec`. That
edit is by hand, on top of the `scripts/new-bench.sh` output. A copy
outside the kata with a `ref Vec[i64]` parameter builds under legacy,
with warnings that `count` takes the maps owned, and takes 0.56 to
0.60 s. Under `karac __mir-llvm-run` the program prints the same line in
6.5 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So the v2 build is a little faster than legacy and within a third of
Rust, whose `HashMap` hashes the same way. C's simpler hash makes it the
fastest by far. The comparison with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The legacy crash and
timeouts above are not filed because legacy is frozen.
