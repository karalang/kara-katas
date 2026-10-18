# 702. Search in a Sorted Array of Unknown Size

This is an interactive problem. You have a sorted array of unique
elements and an unknown size. You do not have access to the array but
you can use the `ArrayReader` interface to access it:
`ArrayReader.get(i)` returns the value at the i-th index (0-indexed) of
the secret array, or 2^31 - 1 if `i` is out of the boundary of the
array. You are also given an integer `target`. Return the index `k` of
the hidden array where `secret[k] == target`, or -1 otherwise. You must
write an algorithm with O(log n) runtime complexity.

```
secret = [-1,0,3,5,9,12], target = 9  ->  4
secret = [-1,0,3,5,9,12], target = 2  ->  -1
```

**Constraints:** 1 <= `secret.length` <= 10^4; -10^4 <= `secret[i]`,
`target` <= 10^4; `secret` is sorted in strictly increasing order.

## Approaches

Every arm is `fn search(reader: mut ref ArrayReader, target: i64) ->
i64`. `ArrayReader` is a struct holding the secret `Vec` and a count of
reads; `get` takes `mut ref self` because it counts every call, which
lets the differential hold each arm to its number of reads.

| file | mechanism |
|---|---|
| `search_in_a_sorted_array_of_unknown_size.kara` ★ | a bound doubled until the value there is not below `target`, then a binary search between the last two bounds; O(log k) reads for a target at k |
| `search_in_a_sorted_array_of_unknown_size_scan.kara` | reads from the front until a value is not below `target`, which the 2^31 - 1 past the end also stops; O(k) reads, not what the problem asks, and there to be held to its own bound |
| `search_in_a_sorted_array_of_unknown_size_length.kara` | the hidden length first, by doubling until a read falls past the end and halving to the first index that does; then an ordinary binary search over [0, length); O(log n) reads, a few more than the ★ arm |
| `search_in_a_sorted_array_of_unknown_size_lifting.kara` | the last index below `target` built from its highest bit down, 2^13 first since the array holds fewer than 2^14 values; always 15 reads |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 14 lines: the two LeetCode examples; the first
and last values, targets below and above them all and one between two
values; one value searched for itself, below and above it, and two
values; 10,000 values, the problem's most, searched for every seventh
number from -10,000 up, half of them there, and for its last value and
one past it; and 1,000 random arrays of 1 to 300 values, each searched
for one target, with a checksum.
`search_in_a_sorted_array_of_unknown_size.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: look at every value
of the secret array, without the order or the reader, and answer the
index of the one equal to `target`. 3,000 random arrays are checked, of
1 to 40 values and one case in ten of up to 2,000, increasing from
-60 by 1 to a random 1 to 4, each searched for a target that is one of
its values half of the time. Every run gets a reader of its own, so its
reads are its own.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | every value and the target 5,000 higher, the same answer |
| P3 | the values negated and reversed and the target negated, the answer counted from the other end |
| P4 | no more reads than the arm's bound: up to the target or the first value past it for the scan, 2b + 2 for the ★ arm and 3b + 1 for the length arm, where b is the number of binary digits of the length, and 15 for the bit arm |

It prints `3000 arrays (2335 with the target), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Two more edits, E1 and
E2, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the bound stepped by one, not doubled | P4 1351 |
| M2 | ★: the halving turned the wrong way | P1 1840, P3 1811 |
| M3 | ★: where the target would go returned when it is missing | P1 665, P3 665 |
| M4 | scan: a value one past the target read through | P4 348 |
| M5 | scan: starting at index 1 | P1 188, P3 221 |
| M6 | scan: the first value not below the target taken as it | P1 665, P3 665 |
| M7 | length: the length taken one short | P1 221, P3 188 |
| M8 | length: the halving steps two below the middle | P1 711, P3 694 |
| M9 | length: the halving turned the wrong way | P1 2136, P3 2114 |
| M10 | bits: a step jumped to, not added | P1 1788, P3 1740 |
| M11 | bits: stepping onto the target as well | P1 2335, P3 2335 |
| M12 | bits: the last value below the target returned | P1 2335, P3 2335 |
| E1 | length: the middle written (lo + hi) / 2 | 0 |
| E2 | ★: doubling on past a value equal to the target | 0 |

P1 and P3 kill every mutant that gives a wrong answer. P4 kills the two
that only read too much: stepping the ★ arm's bound by one, which still
finds every target but in O(k) reads (M1), and the scan reading on past
a value one above the target (M4). P2 sees none, since every arm only
compares values and moving them all keeps every comparison. E1 writes
the middle as (lo + hi) / 2, the same for indices this small. E2 doubles
once more when the bound lands on the target itself; the target stays
inside the bracket and the bound still holds. An edit first meant as an
E row, the length arm's last search starting one past the last value,
finds every answer but costs one read more, and P4 caught it 11 times,
so it is not listed as equivalent.

## Verification

Every arm prints the same output as
`search_in_a_sorted_array_of_unknown_size.py` under `karac __mir-run`
(the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs clean
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer):
output identical, no error, no leak. The differential prints its line
under all three. `karac check` passes all four arms, the differential
and the bench program. All with the compiler at kara `83fab1e1e8` for
the debug build and `f5c72b653e` for the release build that runs `check`
and `__mir-run`, which differ in no `src` or `runtime` file, with
runtime archives rebuilt after the last `runtime/src` change.

The frozen legacy backends refuse all four arms at type checking, at
`next_random(mut seed)` inside the harness's `random_sorted`, whose
`seed` is already a `mut ref`: legacy wants the marker dropped, while on
v2 the marked forward is the spelling (kara B-2026-10-14-25). The legacy
`karac build` builds the differential, with an ownership warning, and it
prints the same line; `karac run --interp` does not finish it within
60 s. Legacy builds the bench program as it is. Legacy is frozen, so
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, the same in all five languages, with
the reader's read count kept. It builds 100 arrays of 10,000 increasing
values from -10,000 once, each 1 or 2 above the one before; then in each
of 5 rounds it searches every array for every even number from
-10,000 to 10,000, and adds up the answers found and the reads made.
Every implementation prints `5 rounds of 100 arrays of
10000: 2503150 found, 125246215 reads, checksum 447585667`, the Kāra
program under `karac __mir-run` included (in 116 s).

Every implementation keeps the reader as a struct, or an object in
Python, with the array and a read count, and reads through a method or
function that counts the call and checks the bounds. Spot timings on a
shared 4-core container, eight runs of each compiled program and ten of
the legacy build, five of each interleaved, and two of Python
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.28 to 0.32 s |
| Rust (`rustc -O`) | 0.25 to 0.31 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.33 to 0.39 s |
| Go | 0.38 to 0.44 s |
| Python | 18.3 to 18.9 s |
| Kāra (`karac build --mir`) | 0.36 to 0.46 s |
| Kāra, legacy (`karac build`) | 0.34 to 0.37 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` builds the same file, and
its row is above. That edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 3.7 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

So the v2 build is level with Go here, about 10% behind legacy and Rust
with overflow checks by median, and about 35% behind C and plain Rust.
The comparison with C and Rust waits until after M4.

## Compiler findings

None. `karac check` passed all four arms, the harness, the differential
and the bench program, once the harness's `find` and `show` took the
array as `own Vec[i64]`: a bare parameter borrows under v2, and the
reader's field wants an owned value.
