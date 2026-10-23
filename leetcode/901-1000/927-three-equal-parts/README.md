# 927. Three Equal Parts

You are given an array `arr` which consists of only zeros and ones,
divide the array into three non-empty parts such that all of these parts
represent the same binary value.

If it is possible, return any `[i, j]` with `i + 1 < j`, such that:

- `arr[0], arr[1], ..., arr[i]` is the first part,
- `arr[i + 1], arr[i + 2], ..., arr[j - 1]` is the second part, and
- `arr[j], arr[j + 1], ..., arr[arr.length - 1]` is the third part.
- All three parts have equal binary values.

If it is not possible, return `[-1, -1]`.

Note that the entire part is used when considering what binary value it
represents. For example, `[1,1,0]` represents `6` in decimal, not `3`.
Also, leading zeros are allowed, so `[0,1,1]` and `[1,1]` represent the
same value.

```
arr = [1,0,1,0,1]  ->  [0,3]
arr = [1,1,0,1,1]  ->  [-1,-1]
arr = [1,1,0,0,1]  ->  [0,2]
```

**Constraints:** `3 <= arr.length <= 3 * 10^4`; `arr[i]` is `0` or `1`.

## Approaches

Equal values hold equally many 1s, so each part holds a third of them,
and the third part ends the array, so its trailing 0s end every part.
With at least one 1 the split is therefore unique; with none, every
split works, and every arm answers `[0, n - 1]`, as LeetCode's own
solution does.

| file | mechanism |
|---|---|
| `three_equal_parts.kara` ★ | a pointer at the first 1 of each third of the 1s, all three walked forward together while their digits agree; the split holds if the last pointer reaches the end. O(n), O(1) extra space |
| `three_equal_parts_backward.kara` | each part ends as many 0s after its third's last 1 as the array ends after its last; three pointers walk left from those ends, comparing digits, until each has passed a third of the 1s, and none may cross into the part before. O(n) |
| `three_equal_parts_groups.kara` | the positions of the 1s listed: the gaps inside the three groups must agree, and between groups there must be room for the trailing 0s. O(n), O(n) space |
| `three_equal_parts_slices.kara` | copies as long as the third part from its first 1, cut from each third's first 1, compared whole with `Vec` `==`; the first two must end before the next starts. O(n), O(n) space |
| `three_equal_parts_hash.kara` | every prefix's value modulo 10^9 + 7, so any stretch's value is two prefixes and a power of two; each end of the first part between its third's last 1 and the next 1, and each start of the third part likewise, tried until the three values agree. O(n) for these arrays, O(n) space |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples and six
more (all 0s, 1s not a multiple of three, leading 0s in every part,
trailing 0s the middle part cannot hold, three single 1s, and parts
that differ only in leading 0s); for 300 random arrays of up to 1,200
digits, each a value written three times with leading 0s and half of
them with one digit flipped, how many split (159) and a checksum; and
three of LeetCode's largest, 30,000 digits: all 0s, all 1s, and `100`
repeated after three 0s. `three_equal_parts.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: try every `[i, j]` with three non-empty parts, work out each
part's value as a number, and list the splits whose three values are
equal. It checks 3,200 arrays: 3,000 small ones against the statement,
half random of 3 to 12 digits and half a value of up to 3 digits written
three times with up to two leading 0s each (perhaps one digit flipped),
and 200 written that way from values of up to 300 digits with up to 100
leading 0s, against the other properties; 144,519 digits in all, and
1,076 arrays split.

| | property |
|---|---|
| P1 | one of the statement's splits, or `[-1, -1]` when it lists none, on the small arrays |
| P2 | a split returned is three non-empty parts of equal value |
| P3 | `k` 0s in front move a split `k` to the right and leave no split as none (all 0s give `[0, n + k - 1]`) |
| P4 | the array written three times splits into its three copies, `[n - 1, 2n]` (all 0s give `[0, 3n - 1]`) |
| P5 | with a split found and some 1, the array turned to start with the second part splits into that part, the third and the first |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 arrays, 144519 digits, 1076 split, 95000 checks over 5
arms: 0 failures` under `karac __mir-run` (7 s) and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the walk not required to reach the end | P1 286, P2 286, P5 286, P6 286 |
| M2 | ★: only the first two pointers compared | P1 49, P2 49, P5 49, P6 49 |
| M3 | ★: all 0s answered `[-1, -1]` | P1 261, P3 261, P4 261, P6 261 |
| M4 | backward: the walk stopping one 1 short | P1 211, P2 211, P5 87, P6 211 |
| M5 | backward: the first and third parts compared, not the middle | P1 32, P2 32, P5 32, P6 32 |
| M6 | backward: the third part starting one late | P1 714, P2 815, P4 2939, P5 815, P6 815 |
| M7 | groups: the room for trailing 0s allowed to be equal | P1 62, P2 62, P5 41, P6 62 |
| M8 | groups: the first gap of each group skipped | P1 102, P2 102, P6 102 |
| M9 | groups: no room checked before the third part | P1 27, P2 27, P5 27, P6 27 |
| M10 | slices: the second copy not compared | P1 31, P2 31, P5 31, P6 31 |
| M11 | slices: the first two copies one digit short | P1 714, P4 2939, P6 815 |
| M12 | slices: the first two copies compared, not the third | P1 19, P2 19, P5 19, P6 19 |
| M13 | hash: the middle value never checked | P1 242, P2 288, P4 1325, P5 288, P6 288 |
| M14 | hash: the first part's ends tried only at its last 1 | P1 180, P4 1325, P6 226 |
| M15 | hash: the third part's starts tried only at its first 1 | P1 502, P4 1919, P5 128, P6 602 |

P1 and P6 kill all fifteen, P2 and P5 eleven each, P4 six and P3 one.
P2 accepts `[-1, -1]` by design, so it misses the four mutants that only
answer none where a split exists (M3, M11, M14 and M15). P5 misses M3,
whose mistake is confined to arrays with no 1, which P5 skips, and M8,
M11 and M14, which, whenever they find a split, find the right one in
the turned array too. P4 builds arrays that always split at a known
place, so it sees the mutants that miss that split there: the four
that only answer none wrongly, and M6 and M13. P3 sees only M3: every
other mutant's mistake concerns how the parts compare, and 0s in front
only lengthen the first part's leading 0s, so the mutant makes the same
mistake shifted along.

Twelve other edits were tried and set aside. Two are equivalent:
backward allowing `y < 0` rather than `y <= end1` (the third pointer's
own bound fires first) and slices without its overlap check (an
overlapping copy then fails the comparison anyway). Nine failed exactly
the same checks as a kept mutant: ★ ending the first part at `a` rather
than `a - 1`, and slices starting the third part one early, as M6;
groups not comparing the third group's gaps, as M5; hash shifting the
third part one short, backward pushing each third's last 1 at `k + 1`
and slices cutting the third copy one short, as M11; backward ending the
first or the second part at its last 1, as M14; and slices cutting the
second copy from the first start, as M10. One was sound but beyond three
an arm (★ letting through 1s that are not a multiple of three).

## Verification

Every arm prints the same output as `three_equal_parts.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 0.4 to 0.9 s each and the
differential 7 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy compiler refuses every arm, the differential and the
bench program at the first `*` on an element of a `Vec[i64]`'s
`.iter()` ("unary '*' requires 'ref T', ... found 'i64'"), legacy's
older rule; under v2 the element is a reference and the `*` is
required. Legacy is frozen, so none of this is filed.

## Benchmarks

The bench program builds 100 arrays of 30,000 digits once, LeetCode's
largest: each a value of 9,000 random digits written three times, every
copy after up to 1,000 leading 0s, the array filled up with 0s in front,
and every other array with one digit flipped. In each of 30 rounds it
runs the ★ arm on every array, each round starting from a different
one. Every implementation prints `30 rounds over 100 arrays of 30000:
1500 split, checksum 39190265`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.24 to 0.28 s | 0.27 s |
| Rust (`rustc -O`) | 0.26 to 0.31 s | 0.30 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.28 to 0.35 s | 0.30 s |
| Go | 0.33 to 0.39 s | 0.35 s |
| Python | 4.6 s | |
| Kāra (`karac build --mir`) | 0.34 to 0.40 s | 0.38 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about 17 times C's.

v2 takes 1.24 times Rust's median time under overflow checks and 1.39
times C's. Under valgrind's cachegrind all three mispredict about 20.2
million branches; beside that, v2 runs 1.78 billion instructions and 0.58
billion branches, Rust with overflow checks 1.31 billion and 0.47
billion, and C 0.69 billion and 0.22 billion. That v2's extra
instructions are bounds checks on the three pointers' reads is
inferred, not profiled.
