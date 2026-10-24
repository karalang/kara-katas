# 969. Pancake Sorting

Given an array of integers `arr`, sort the array by performing a series
of pancake flips. In one pancake flip we do the following steps: choose
an integer `k` where `1 <= k <= arr.length`, and reverse the sub-array
`arr[0...k-1]` (0-indexed). For example, if `arr = [3,2,1,4]` and we
performed a pancake flip choosing `k = 3`, we reverse the sub-array
`[3,2,1]`, so `arr = [1,2,3,4]` after the pancake flip at `k = 3`.

Return an array of the `k`-values corresponding to a sequence of pancake
flips that sort `arr`. Any valid answer that sorts the array within
`10 * arr.length` flips will be judged as correct.

```
arr = [3,2,4,1]  ->  [4,2,4,3]
arr = [1,2,3]    ->  []
```

**Constraints:** `1 <= arr.length <= 100`; `1 <= arr[i] <= arr.length`;
all integers in `arr` are unique (that is, `arr` is a permutation of the
integers from 1 to `arr.length`).

## Approaches

| file | mechanism |
|---|---|
| `pancake_sort.kara` ★ | the largest pancake to the bottom, one at a time: `arr` is a permutation of 1 to n, so the largest of the top `size` pancakes is `size` itself. For each size from n down to 2, find it; unless it is already the bottom one of those `size`, flip it to the top (when it is not there already), then flip the top `size`, which leaves it at the bottom for good. At most 2(n - 1) flips, each found and made in O(n): O(n^2) time |
| `pancake_sort_iter.kara` | the same flips with the library: `position` finds the largest, and a flip is the in-place `reverse` of the slice `a[0..k]` |
| `pancake_sort_positions.kara` | the same flips with no search: a table of where each pancake is, so the largest of the top `size` is at `pos[size]`; a flip reverses the stack and writes the flipped pancakes' new places back into the table |
| `pancake_sort_inverse.kara` | the same flips on the table alone, the stack itself never built: a flip of k sends the pancake at index p < k to k - 1 - p, one pass over the n places, and leaves the pancakes already at the bottom, which sit at k or below, alone |
| `pancake_sort_recursive.kara` | the same flips with no loop: sorting the top `size` pancakes sends the largest to the bottom and then sorts the top size - 1, finding it recurses down the stack, and a flip swaps its two ends and flips what lies between |
| `differential.kara` | the five arms against the statement read literally, six properties |

LeetCode accepts any sequence that sorts the stack within 10n flips, and
gives `[4,2,4,3]` for its first example; all five arms make the same
choice, so they print the same flips, `[3,4,2,3,2]` there. Every arm
prints the same 14 lines: LeetCode's two examples and eight more (one
pancake, two, two orders of three, a stack upside down that one flip
sorts, a stack whose smallest is at the bottom, and two of six), each
with whether the flips sort it; for 300 random stacks of 1 to 12
pancakes, 1,993 in all, the flips they take in total (2,194), how many
were sorted and a checksum; and three stacks of 100 pancakes, LeetCode's
largest: a random stack (186 flips), the stack upside down (1) and the
odd pancakes above the even ones (99). `pancake_sort.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a flip of k rebuilds the stack from its first k pancakes
backwards and the rest as they were. It checks 3,200 random stacks:
3,000 of up to 8 pancakes against the statement, and 200 of up to 100
pancakes against the other properties; 24,362 pancakes in all, sorted
in 30,822 flips.

| | property |
|---|---|
| P1 | the statement, on the small cases: every k from 1 to n, at most 10n flips, and the stack sorted after them |
| P2 | at most 2(n - 1) flips, none of a single pancake, and none the same as the one before, which would undo it |
| P3 | the flips sort the stack, a sorted stack needs none, and a stack upside down needs one flip of the whole |
| P4 | the stack after the first j flips asks for the rest, for j = 1 and for half the flips |
| P5 | a pancake larger than all put under the stack changes nothing, and one put on top is flipped to the bottom first, leaving the stack upside down: `[n + 1]` followed by the flips for the reversed stack |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 stacks of 24362 pancakes: 30822 flips, checksum
107239561, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
(15.6 s) and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Twenty-eight edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run` with the same results; fifteen are
kept, three to each arm, and all fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a flip one pancake short | P1 1977, P2 1293, P3 2460, P4 2291, P5 2823, P6 2170 |
| M2 | ★: the largest flipped even when at the bottom | P2 2171, P3 2823, P4 2506, P5 3200, P6 2171 |
| M3 | ★: the largest flipped to the top when already there | P2 2162, P3 2823, P4 2568, P5 3200, P6 2162 |
| M4 | iter: the second flip recorded one short | P1 2372, P2 2179, P3 2823, P4 2211, P5 3200, P6 2568 |
| M5 | iter: the first flip recorded one too deep | P1 1802, P2 1524, P3 1994, P4 1948, P6 1994 |
| M6 | iter: the higher of the two largest taken for the largest | P1 2130, P3 2823, P4 2698, P5 3200, P6 2325 |
| M7 | positions: the table never updated | P1 1966, P2 1234, P3 2258, P4 2184, P5 2639, P6 2184 |
| M8 | positions: the test for a largest on top off by one | P1 1270, P2 2290, P3 2823, P4 2568, P5 3200, P6 2500 |
| M9 | positions: the last two pancakes never sorted | P1 1304, P3 1594, P5 377, P6 1415 |
| M10 | inverse: a flip moving the pancake below it | P1 1200, P3 1392, P4 1006, P6 1392 |
| M11 | inverse: a flip sending p to k - p | P1 1769, P3 1962, P4 1785, P5 2543, P6 1962 |
| M12 | inverse: a largest just above the bottom left there | P1 1986, P3 2358, P4 275, P5 377, P6 2179 |
| M13 | recursive: a flip leaving its middle pair | P1 1759, P2 608, P3 2076, P4 1789, P5 1187, P6 1958 |
| M14 | recursive: the first flip leaving the top pancake | P1 1645, P2 809, P3 1837, P4 1831, P6 1842 |
| M15 | recursive: every other size skipped | P1 1723, P3 1917, P4 166, P5 2823, P6 1917 |

P3 and P6 kill all fifteen, P4 fourteen (all but M9), P1 thirteen (all
but M2 and M3), P5 twelve (all but M5, M10 and M14) and P2 nine (M1 to
M5, M7, M8, M13, M14). M2 and M3 still sort every stack within 10n
flips, so the statement accepts them; they waste flips, a flip
repeated or a flip of one pancake, which P2 refuses. P2 misses the edits
that leave the stack unsorted in as few flips as before. M9 stops before
the last two pancakes, and the stack after any of its flips still asks
for exactly the rest, so only P4 misses it.

Thirteen other edits were tried and set aside. Three failed exactly the
same checks as a kept one: iter flipping the largest to the top when it
is already there, as M3, and flipping it even when it is at the bottom,
as M2, and recursive never sorting the last two pancakes, as M9. Five
were sound but beyond three an arm: ★ never sorting the last two
pancakes and recording the first flip one short, positions making the
second flip one pancake short, inverse skipping the first flip for a
largest second from the top, and recursive recording the first flip one
short. Two were equivalent: positions leaving the deepest flipped
pancake out of its table, since a first flip is always followed by a
second that rewrites its deepest pancake's place, and a second flip's
deepest is the largest, just sent to the bottom and never looked up
again; and inverse never moving pancake 1, whose place is never asked
for. Three crashed and were
not counted: iter never placing the largest pancake, flipping one
pancake too deep, and taking the sizes smallest first; each leaves a
size that is no longer among the top `size` pancakes, so `position`
finds nothing and `unwrap` stops the program.

## Verification

Every arm prints the same output as `pancake_sort.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `e04ae2b46b`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` the arms
take 0.16 s (inverse and recursive) to 0.21 s (iter), and the
differential 15.6 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program makes 200 random stacks of 100 pancakes once. In each
of 100 rounds it runs the ★ arm on every stack, each round starting from
a different one, and folds every flip into a checksum. Every
implementation prints `100 rounds over 200 stacks of 100 pancakes:
3705500 flips, checksum 626017205`. Every call copies its stack and
grows a list of flips: a `Vec` in Kāra and Rust, a slice in Go, a list
in Python, and two `malloc`ed arrays in C.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `e04ae2b46b`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.135 to 0.152 s | 0.143 s |
| Rust (`rustc -O`) | 0.142 to 0.183 s | 0.155 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.147 to 0.186 s | 0.162 s |
| Go | 0.196 to 0.214 s | 0.207 s |
| Python | 7.9 s | |
| Kāra (`karac build --mir`) | 0.161 to 0.248 s | 0.174 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 55 times
C's.

v2 took 1.07 times Rust's median time under overflow checks and 1.22
times C's. Under valgrind's cachegrind v2 ran 1.82 billion instructions
and 473 million branches with 6.4 million mispredicted, Rust with
overflow checks 1.35 billion, 351 million and 6.3 million, and C 962
million, 134 million and 6.0 million. Kāra and Rust check every index
in the search and the swaps where C checks none, which likely accounts
for most of their extra branches; that was not measured separately.

