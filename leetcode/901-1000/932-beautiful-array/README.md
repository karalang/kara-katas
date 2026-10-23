# 932. Beautiful Array

An array `nums` of length `n` is **beautiful** if:

- `nums` is a permutation of the integers in the range `[1, n]`.
- For every `0 <= i < j < n`, there is no index `k` with `i < k < j`
  where `2 * nums[k] == nums[i] + nums[j]`.

Given the integer `n`, return any beautiful array `nums` of length `n`.
There will be at least one valid answer for the given `n`.

```
n = 4  ->  [2,1,4,3]
n = 5  ->  [3,1,2,5,4]
```

**Constraints:** `1 <= n <= 1000`.

## Approaches

Any beautiful array is accepted, and all five arms build the same one,
the array the divide and conquer gives: `x - 1` listed in order of its
bits read backwards. For `n = 4` that is `[1, 3, 2, 4]` and for `n = 5`
`[1, 5, 3, 2, 4]`, where LeetCode's examples show `[2, 1, 4, 3]` and
`[3, 1, 2, 5, 4]`.

| file | mechanism |
|---|---|
| `beautiful_array.kara` ★ | divide and conquer: the odd values `2x - 1` over a beautiful array of `(n + 1) / 2`, then the even values `2x` over one of `n / 2`, since an odd and an even value never average to a whole number; each size's array kept in a `Map` and built once. O(n log n) |
| `beautiful_array_doubling.kara` | from `[1]`, each step maps every value to `2x - 1` and then every value to `2x`, dropping values above `n`, until all `n` are present. O(n log n) |
| `beautiful_array_lowbit.kara` | 1 to `n` sorted with `sort_by`, two values ordered by the lowest bit where `x - 1` and `y - 1` differ, the one with the 0 there first. O(n log n) |
| `beautiful_array_partition.kara` | 1 to `n` split by the lowest bit of `x - 1`, order kept, then each part by the next bit, recursively, until each part holds at most one value. O(n log n) |
| `beautiful_array_reverse.kara` | `i` counted from 0 to `2^b - 1`, with `b` bits enough for `n - 1`; each `i`'s bits reversed and kept, plus one, when below `n`. O(n log n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the arrays for LeetCode's two
examples and for `n` of 1, 2, 3, 8 and 9, each checked beautiful; every
`n` from 1 to 100 checked beautiful; every array for `n` from 1 to
1,000, LeetCode's largest, folded into a checksum (500,500 elements);
and the array for `n = 1000` checked beautiful, with its first and last
four values. The check pairs each `nums[i]` with each later `nums[k]` and
looks up where `2 * nums[k] - nums[i]` sits: it must not come after `k`.
`beautiful_array.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every value of 1 to `n` counted in the array and found once,
and every `i < k < j` tried for `2 * nums[k] == nums[i] + nums[j]`. It
checks 3,200 random `n`: 3,000 from 1 to 16 against the statement, and
200 from 1 to 500 against the other properties; 75,306 elements in all.

| | property |
|---|---|
| P1 | the statement, on the small `n` |
| P2 | a permutation of 1 to `n` |
| P3 | no progression of three, found by position as in the harness |
| P4 | the odd values all come first, and `(x + 1) / 2` over them and `x / 2` over the even ones give the same arm's arrays for `(n + 1) / 2` and `n / 2` |
| P5 | the same arm's array for `n + 1`, with `n + 1` taken out, is this one |
| P6 | each arm agrees with at least two of the other four |

P4 and P5 are properties of the array the arms share, not of every
beautiful array: they hold because it is the divide and conquer's array,
and the ordering by reversed bits does not change when `n` grows.

It prints `3200 arrays, 75306 elements, checksum 174737457, 95000 checks
over 5 arms: 0 failures` under `karac __mir-run` (25 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the odd values taken as `2x + 1` | P1 2819, P2 3019, P4 3019, P5 3200, P6 3019 |
| M2 | ★: the odd values arranged from `n / 2` | P1 2071, P2 2268, P4 605, P5 605, P6 2268 |
| M3 | ★: each array kept under the next size | P1 2393, P2 2593, P4 2411, P5 938, P6 2593 |
| M4 | doubling: starting from `[1, 2]` | P1 181, P2 181, P4 607, P5 181, P6 181 |
| M5 | doubling: `n + 1` let in among the odd values | P1 725, P2 837, P4 1294, P5 1663, P6 837 |
| M6 | doubling: the even values taken as `2x - 2` | P1 2819, P2 3019, P4 3019, P5 932, P6 3019 |
| M7 | lowbit: the one with the 1 first | P4 3019, P6 3019 |
| M8 | lowbit: the lowest bit cleared rather than kept | P1 2393, P3 2593, P4 3019, P6 3019 |
| M9 | lowbit: the highest bit compared | P1 2600, P3 2800, P4 2800, P6 2800 |
| M10 | partition: the part with a 1 never arranged | P1 2034, P3 2233, P4 2233, P6 2233 |
| M11 | partition: the part with a 0 never arranged | P1 2219, P3 2419, P4 2419, P6 2419 |
| M12 | partition: parts of three never split | P1 2071, P3 2268, P4 207, P5 1423, P6 2268 |
| M13 | reverse: one bit fewer reversed | P1 2819, P2 3019, P3 2419, P4 3019, P5 932, P6 3019 |
| M14 | reverse: `i` kept rather than its reverse | P1 2600, P2 1663, P3 2800, P4 2800, P5 1818, P6 2800 |
| M15 | reverse: `n - y` kept | P4 1588, P5 3019, P6 3019 |

P4 and P6 kill all fifteen, P1 thirteen, P5 ten, P2 eight and P3 seven.
M7 and M15 still build beautiful arrays (the even values first, and the
divide and conquer's array reflected), so the statement, P2 and P3 pass
them; only the properties of the shared array see them. M7 also passes
P5, since putting the 1 first at every bit is as stable as `n` grows. P2
misses the seven that only reorder 1 to `n` (M7 to M12 and M15), and
P3 misses M7 and M15, and the six whose wrong arrays happen to hold no
progression the position check can find (M1 to M6). M8, M9,
M10 and M11 pass P5: their wrong orders are stable when `n` grows too.

Ten other edits were tried and set aside. One was equivalent (lowbit
comparing the bits of `x` rather than `x - 1`: where they differ at all,
the lowest differing bit and the bit of `x - 1` there agree). Three
failed exactly the same checks as another edit: doubling stopping at
half and reverse with half the bits, as each other; and partition
reading the bits of `x` rather than `x - 1`, as M7. Six were sound but
beyond three an arm (★ with 2 a base case and the even values from
`(n + 1) / 2`, doubling letting the even values up to `n + 2`, lowbit
leaving `n` out, partition leaving 1 out, and reverse keeping `n + 1`).

## Verification

Every arm prints the same output as `beautiful_array.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 2.1 to 3.0 s each, except
partition at 13.7 s, which allocates two new `Vec`s at every level of
its recursion; the differential takes 25 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

Legacy refuses all five arms, the differential and the bench program at
the first `*` on an element of a `Vec[i64]`'s `.iter()` ("unary '*'
requires 'ref T', ... found 'i64'"), legacy's older rule; under v2 the
element is a reference and the `*` is required. Legacy is frozen, so
none of this is filed.

## Benchmarks

The bench program runs the ★ arm, its memo new on each call, for every
`n` from 1 to 1,000 in each of 100 rounds, each round starting from a
different `n`, and folds in each array's middle and last value. Every
implementation prints `100 rounds over n from 1 to 1000: middles summing
to 16963000, checksum 352128606`. Rust uses a `HashMap`, Go a `map` and
Python a `dict` for the memo, as Kāra uses a `Map`; C keeps it in an
array indexed by `n`. Each size's array is copied into the memo and
copied out again on a hit, in every language.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.27 to 0.31 s | 0.29 s |
| Rust (`rustc -O`) | 0.57 to 0.64 s | 0.61 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.57 to 0.65 s | 0.61 s |
| Go | 1.98 to 2.44 s | 2.14 s |
| Python | 5.27 s | |
| Kāra (`karac build --mir`) | 0.47 to 0.71 s | 0.52 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about 18 times C's.

v2 takes 0.86 times Rust's median time under overflow checks and 1.81
times C's. Under valgrind's cachegrind v2 runs 6.53 billion
instructions and 1.08 billion branches with 41.4 million mispredicted,
Rust with overflow checks 6.75 billion, 1.12 billion and 43.0 million,
and C 2.78 billion, 1.15 billion and 12.4 million. v2 and Rust are that
close in instructions, so v2's lead is not in the code run; that it
comes from the allocator, and C's from indexing an array where the
others hash, is inferred, not profiled.
