# 900. RLE Iterator

We can use run-length encoding (RLE) to encode a sequence of integers.
In a run-length encoded array `encoding` of even length, for all even
`i`, `encoding[i]` tells us the number of times that the non-negative
integer value `encoding[i + 1]` is repeated in the sequence. For
example, the sequence `[8,8,8,5,5]` can be encoded as `[3,8,2,5]`;
`[3,8,0,9,2,5]` and `[2,8,1,8,2,5]` are also valid encodings of it.

Implement the `RLEIterator` class: `RLEIterator(encoding)` initializes
the object with the encoded array, and `next(n)` exhausts the next `n`
elements and returns the last element exhausted in this way. If there is
no element left to exhaust, it returns `-1` instead.

```
RLEIterator([3,8,0,9,2,5])
next(2) -> 8, next(1) -> 8, next(1) -> 5, next(2) -> -1
```

**Constraints:** `2 <= encoding.length <= 1000`, `encoding.length` is
even, `0 <= encoding[i] <= 10^9`, `1 <= n <= 10^9`, and at most 1000
calls are made to `next`.

## Approaches

The sequence can hold up to 5 * 10^11 terms, so no arm writes it out;
each keeps a place in the encoding and moves it on by whole runs. A run
of no terms is stepped past like any other, and once a call asks for
more terms than are left, every later call answers `-1` too. In every
arm the constructor takes the encoding by value (`own Vec[i64]`), as
LeetCode's constructor is handed the array.

| file | mechanism |
|---|---|
| `rle_iterator.kara` ★ | the runs used up in place: step past every run whose count is less than what is still needed, taking its count off; then take the rest off the count of the run reached and answer its value. O(length + calls) |
| `rle_iterator_offset.kara` | the encoding left as it is: the place of the run being read and how many of its terms are used, so the encoding is never written to. O(length + calls) |
| `rle_iterator_prefix.kara` | prefix sums and a binary search: the terms through the end of each run counted once, the iterator only a place in the sequence, and the term there found by a binary search over the totals. O(log length) a call |
| `rle_iterator_stack.kara` | the runs on a stack: the first run on top and runs of no terms dropped; runs with too few terms popped, the rest taken off the run on top. O(length + calls) |
| `rle_iterator_recursive.kara` | the rest asked of the next run: a call the run being read cannot answer uses its terms, moves on and asks the rest of the next run, recursively. O(length + calls) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's example and seven more
(one run asked twice, two runs of no terms, a run used up exactly, a
first call asking for too many, a mixed three runs, a run of one between
others of the same value, and two runs of 10^9); for 300 random cases of
up to 500 runs, a third with counts up to 3, a third up to 1,000 and a
third up to 10^9, and up to 1,000 calls each asking for up to a quarter
of the largest count, 149,753 calls of which 44,867 answer `-1`, a
checksum of the answers; and two of LeetCode's largest, 500 runs of
10^9 asked for 10^9 + 1 at a time, and 500 runs of one term asked for
one at a time. `rle_iterator.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the sequence written out term by term, and a place in it
moved `n` on by each call, answering the term there or `-1` once the
place is past the last term. It checks 3,200 random cases: 3,000 of up
to 4 runs of up to 3 terms with values 1 to 3 and up to 6 calls of up to
4 against the statement, and 200 of up to 300 runs of up to 3, 1,000 or
10^9 terms and up to 300 calls against the other properties; 40,328
calls in all.

| | property |
|---|---|
| P1 | the statement's answers, on the small cases |
| P2 | `-1` exactly when the calls so far ask for more terms than there are, and otherwise the value of a run with terms |
| P3 | two neighbouring calls merged into one give the second's answer, and a call split in two gives the same answer at the second part: an answer depends only on how many terms have been asked for |
| P4 | the same answers for the encoding rewritten: a run split in two runs of the same value, and a run of no terms with a random value put in at a random place |
| P5 | the same answers with a run put in front and the first call asking for its terms as well, and each answer `v` as `2v + 1` with every value mapped so |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every case. It prints `3200 cases, 40328 calls,
95000 checks over 5 arms: 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a run used up exactly stepped past | P1 1346, P2 940, P6 1428 |
| M2 | ★: the terms used never taken off the run | P1 1195, P2 1071, P3 1072, P4 107, P6 1393 |
| M3 | ★: the runs stepped past never taken off what is needed | P1 951, P2 984, P3 384, P4 189, P5 1215, P6 1147 |
| M4 | offset: the terms used carried into the next run | P1 661, P2 842, P3 400, P4 194, P6 859 |
| M5 | offset: a run with exactly enough left stepped past | P1 1346, P2 940, P6 1428 |
| M6 | offset: one term too few counted as used | P1 968, P2 814, P3 1045, P6 1090 |
| M7 | prefix: the last term counted as past the end | P1 921, P2 940, P6 940 |
| M8 | prefix: the place left where it was after a `-1` | P1 716, P2 743, P3 1019, P5 478, P6 743 |
| M9 | prefix: the search past the run that ends at the place | P1 683, P2 78, P4 198, P6 765 |
| M10 | stack: a run with exactly enough popped | P1 1346, P2 940, P6 1428 |
| M11 | stack: the last run never put on the stack | P1 1259, P2 1297, P4 528, P6 1297 |
| M12 | stack: one term taken off the top run a call | P1 523, P2 454, P3 453, P4 82, P6 721 |
| M13 | recursive: the whole call asked of the next run | P1 951, P2 984, P3 384, P4 189, P5 1215, P6 1147 |
| M14 | recursive: a run with exactly enough passed over | P1 1346, P2 940, P6 1428 |
| M15 | recursive: a run skipped when moving on | P1 1256, P2 1248, P4 950, P5 1909, P6 1455 |

P1, P2 and P6 kill all fifteen. Four mutants in four arms fail exactly
the same cases (M1, M5, M10, M14): a call that ends on the last term of
a run answers the first term of the next run with terms instead. That
answer depends only on the place reached, and splitting a run puts the
new end between two terms of the same value, so P3 to P5 hold; P2 sees
it when the call ends on the last term of all, which these mutants
answer `-1`. M9 goes wrong at the same places except the last term,
where it answers the last run's value whatever that run's count, which
is why P4's run of no terms put in at the end catches it. M7 goes wrong
only at the last term of all, so only P1, P2 and the agreement see it. M3 and M13 fail the same cases: both ask the next run for
the whole call rather than the rest. P3 kills the mutants that lose
count of the terms used (M2, M4, M6, M12), of what the runs stepped past
gave (M3, M13), or of the place after a `-1` (M8), since merging or
splitting calls changes how often each slip happens. P5's run in front
moves every place by the same number of terms, so it kills the mutants
whose answers do not move with it: M8, whose place left behind after a
`-1` is then inside the new run, and the ones that go wrong by whole
runs (M3, M13, M15), where the new first run changes which runs those
are.

No mutant had to be replaced.

## Verification

Every arm prints the same output as `rle_iterator.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 1.2 to 1.4 s
each and the differential 13 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

Every frozen legacy lane, the interpreter, the JIT and `karac build
--legacy` with and without auto-par, refuses all five arms and the
differential: `*n` on an element of `.iter()` is rejected, because
legacy's iterator gives the value itself. The bench program reads no
iterator element and legacy's build of it prints the right output.
Legacy is frozen, so this is not filed.

## Benchmarks

The bench program uses the offset arm, which never writes to the
encoding, so that one encoding can be built once and read every round:
200,000 runs of 1 to 1,000 terms with values up to 10^9. Each round
moves the encoding into a fresh iterator, asks for 1 to 1,000 terms at a
time until it answers `-1`, folds the answers into a checksum, takes the
encoding back and changes one run's count; 140 rounds. C hands the
iterator a pointer to the same array. Every implementation prints `140
rounds over 200000 runs: 28022383 calls, checksum 790201718`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.27 to 0.34 s | 0.31 s |
| Rust (`rustc -O`) | 0.28 to 0.41 s | 0.31 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.33 to 0.42 s | 0.35 s |
| Go | 0.43 to 0.52 s | 0.44 s |
| Python | 19.7 s | |
| Kāra (`karac build --mir`) | 0.32 to 0.39 s | 0.34 s |
| Kāra (`karac build --legacy`) | 0.38 to 0.42 s | 0.39 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 899's does.

v2 takes 0.96 times Rust's median time under overflow checks, 1.07 times
C's and 0.85 times legacy's. Under valgrind's cachegrind C runs 1.30
billion instructions and 112 million branches, Rust with overflow checks
1.66 billion and 309 million, v2 1.66 billion and 337 million, and
legacy 1.68 billion and 339 million. All four mispredict about 22
million branches, roughly one in every call: whether the run being read
has enough terms left turns on a random count, and that branch is the
same in every language. The comparison with C and Rust waits until after
M4.
