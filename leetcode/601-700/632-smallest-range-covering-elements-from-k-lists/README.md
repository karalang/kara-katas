# 632. Smallest Range Covering Elements from K Lists

Given `k` lists of integers, each sorted in nondecreasing order, return
the smallest range `[a, b]` that includes at least one number from each
list. A range `[a, b]` is smaller than `[c, d]` when `b - a < d - c`, or
when the widths are equal and `a < c`.

```
nums = [[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]  ->  [20, 24]
nums = [[1,2,3],[1,2,3],[1,2,3]]                   ->  [1, 1]
```

**Constraints:** 1 to 3,500 lists of 1 to 50 values each; every value
from -100,000 to 100,000.

## Approaches

Every arm is `fn smallest_range(nums: Vec[Vec[i64]]) -> Vec[i64]`,
returning `[a, b]`. The best range starts and ends at values in the
lists, since moving either end in to the nearest value keeps every list
covered. Each arm keeps a candidate only when it is strictly narrower
than the best so far, and meets equally wide candidates in order of
their start, so of equal widths the one starting lowest stays.

| file | mechanism |
|---|---|
| `smallest_range.kara` ★ | one value from each list in a smallest-first `PriorityQueue` of (value, list, index), with the largest of them tracked beside it; the smallest is replaced by the next value of its list until a list runs out; O(n log k) for n values in k lists |
| `smallest_range_window.kara` | every value tagged with its list and all of them sorted together, then a sliding window over that run that counts the values of each list; each right end moves the left end up while the window covers every list; O(n log n) |
| `smallest_range_pointers.kara` | a position in each list, and each step a scan of the k values under them for the smallest and the largest, then the smallest one's position moved on; O(n k) |
| `smallest_range_search.kara` | each distinct value tried as the start in increasing order, a hand-written binary search in every list for its first value at least that large, and the largest of those the end; stops once some list has nothing that large; O(n k log m) for lists of at most m |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 10 lines: the two LeetCode examples; six more
(one list of one value; two ranges of the same width, of which the lower
is kept; the widest values allowed; repeated values; one value in each
list; a value every list shares); a total width and checksum over
300 random cases of 1 to 8 lists of 1 to 10 values from -50 to 50; and
the range for 100 lists of 50 values from the whole allowed span.
`smallest_range.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition: of
every range from one value in the lists to another that covers every
list, the narrowest, and of those the one that starts lowest. Each of
1,000 cases has 1 to 5 lists of 1 to 6 values from -12 to 12, so that
many ranges tie for the narrowest.

| | property |
|---|---|
| P1 | the range is the definition's |
| P2 | the range covers every list, and both ends are values in the lists |
| P3 | the lists in reverse order give the same range |
| P4 | every value plus 7 gives the range plus 7 |
| P5 | one more random list never makes the range narrower |

It prints `1000 cases (total width 3573), 4 arms, 20000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a range as narrow as the best kept in its place | P1 277 |
| M2 | ★: the largest held value set to the value just added | P1 658, P2 658, P3 117, P5 52 |
| M3 | window: a list counted as newly covered by its second value too | P1 742, P2 742, P3 107, P5 44 |
| M4 | window: the tagged values left unsorted | P1 763, P2 763, P3 793, P5 551 |
| M5 | pointers: a value one above the largest not taken as the largest | P1 203, P2 203, P3 314 |
| M6 | pointers: stopping one value before a list runs out | P1 343 |
| M7 | search: the first value above the start found, not at least it | P1 997, P2 111, P4 114, P5 126 |
| M8 | search: the end set to the last list's value alone | P1 704, P2 704, P3 734, P5 92 |
| E1 | ★: the largest starting from far below every value | 0 |
| E2 | window: the window shrunk while it covers at least every list | 0 |
| E3 | pointers: of equal smallest values, the last list's moved on | 0 |
| E4 | search: repeated starts tried again | 0 |

P1 kills all eight. M1 and M6 fail P1 alone: M1 keeps, of two equally
narrow ranges, the one that starts higher, and M6 stops before reaching
a narrower range, but both still return a range that covers every list
and ends on values in them. P2 sees the six whose range can miss a list.
P3 sees five, M2, M3, M4, M5 and M8, whose wrong ranges also depend on
the order of the lists: M8, for one, ends at the last list's value.
P4 sees only M7: when its search makes no start cover every list, it
returns the `[0, 0]` it began with, which does not move when the values
do. The four survivors cannot change an answer: the largest of the first
values is the same whatever it starts from below; a window never covers
more lists than there are; of two lists at the same smallest value,
moving either on leaves the other there, so the next range starts at
that value again; and a repeated start gives the same range, which is
not strictly narrower.

## Verification

Every arm prints the same output as `smallest_range.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes every arm, the
differential and the bench program. All at kara `ea2a2da2be` for the
debug build and `1be6f04ca6` for the release build that runs `check` and
`__mir-run`.

The frozen legacy backends refuse every file at type checking. They
still hold the old rule that an argument which is already a `mut ref`,
as `seed` is inside `random_lists`, drops its call-site `mut` marker;
and they type the items of a `Vec`'s `iter()` by value, so `*value` in
the window and search arms and in the differential is an error. Legacy
is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 10 inputs of 3,500 lists of
50 random values from -100,000 to 100,000, the problem's largest, once;
then 30 rounds each answer one of them, picked by the round, adding up
the widths and putting each range into a checksum. Every implementation
prints `10 inputs of 3500 lists, 30 rounds: total width 721137, checksum
867705835`, the Kāra program under `karac __mir-run` included (in
171 s).

Each implementation keeps a heap of (value, list, index) triples ordered
in that order: Rust uses `BinaryHeap` with `Reverse`, Go
`container/heap`, Python `heapq` and C a hand-written binary heap. Kāra
and Rust pass the input by reference and so does Go's slice; C passes a
pointer to an array of lists. Spot timings on a shared 4-core container,
three runs each (two for Python; `bench.sh` timings need a quiet
machine), each including making the inputs:

| | time |
|---|---|
| C (`clang -O3`) | 0.59 to 0.63 s |
| Rust (`rustc -O`) | 0.42 to 0.48 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.45 to 0.48 s |
| Go | 1.38 to 1.44 s |
| Python | 5.39 to 5.45 s |
| Kāra (`karac build --mir`) | 0.84 to 0.94 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses it as above
and also for taking `smallest_range`'s parameter by value, so passing
`inputs[...]` is "cannot move out of an index expression"; that edit is
by hand, on top of the `scripts/new-bench.sh` output. A copy outside the
kata that drops the forwarded `mut` markers and takes `nums` as `ref
Vec[Vec[i64]]` builds under legacy and takes 0.78 to 0.88 s, so the
v2 build is level with legacy. Under `karac __mir-llvm-run` the program
prints the same line in 3.1 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

The Kāra build is about twice the Rust build and 1.4 times the C build.
Copies of the bench outside the kata with one round instead of 30 take
0.06 to 0.07 s in Kāra and Rust and 0.11 s in C, two runs each, so
making the inputs is a small part of every row, and C's extra time there
is likely its `qsort`. The rest is the heap loop: by the difference,
about 27 ms a round in Kāra against 14 in Rust and 17 in C. That is
inferred from the timings, not profiled.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
