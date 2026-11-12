# 1144. Decrease Elements To Make Array Zigzag

Given an array `nums` of integers, a move consists of choosing any element
and decreasing it by 1.

An array `A` is a zigzag array if either:

- every even-indexed element is greater than adjacent elements, ie.
  `A[0] > A[1] < A[2] > A[3] < A[4] > ...`
- OR, every odd-indexed element is greater than adjacent elements, ie.
  `A[0] < A[1] > A[2] < A[3] > A[4] < ...`

Return the minimum number of moves to transform the given array `nums`
into a zigzag array.

```
nums = [1,2,3]          ->  2
nums = [9,6,1,6,2]      ->  4
```

**Constraints:** `1 <= nums.length <= 1000`; `1 <= nums[i] <= 1000`.

The arms are `fn moves_to_make_zigzag(nums: Vec[i64]) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `moves_to_make_zigzag.kara` ★ | one pass for each choice of which places are lowered, the even ones or the odd ones, stepping over every second place with `step_by(2)`: each lowered place is brought to one below its smaller neighbour when it is not there already, and the cheaper choice is the answer. O(n) |
| `moves_to_make_zigzag_windows.kara` | the array fenced at both ends by `i64.MAX` and read in `windows(3)`: each middle element's moves go to the count for its place's parity, both counts in one pass. O(n) |
| `moves_to_make_zigzag_iter.kara` | the moves for each parity as an iterator: the places of that parity filtered from the indices, each mapped to how far it stands above one below its smaller neighbour, summed. O(n) |
| `moves_to_make_zigzag_lowered.kara` | the zigzag itself built for each parity: a copy of the array with each place of that parity cut to one below its smaller neighbour; the moves are what the copy has lost. O(n) |
| `moves_to_make_zigzag_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `nums: Vec<i32>`, a `[0, 0]` pair of counts, 1001 standing in for a missing neighbour, `std::cmp::max` and `std::cmp::min`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five properties |

Lowering a place never helps the places of the other parity, so for each
choice the cheapest zigzag lowers only the places that must sit below
their neighbours, and lowers each just far enough. The two choices are
the statement's two kinds of zigzag.

Every arm prints the same 11 lines: LeetCode's two examples; one element
(0); two alike (1); a zigzag already (0); seven alike (3); 1 to 10 rising
(8). Then over 2000 random arrays of 1 to 50 values from 1 to 1000 or,
every third array, 1 to 10, the answers summed and a checksum (`2000
random arrays: answers total 3307119, checksum 428616873`), and three of
the longest arrays the constraints allow, 1000 values: all 1000 (500), 1
to 1000 rising (998), and 1 to 1000 at random (109146).
`moves_to_make_zigzag.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way to lower each element to any value from itself down
to 0, the fewest moves that leave an array whose even places all stand
above their neighbours or whose odd places all do. The search stops a way
once its moves reach the best found, or once two neighbours stand equal
or two rises or two falls run together, which no zigzag has. It checks
2000 arrays of 1 to 8 values in four kinds of 500: from 1 to 20; from 1
to 3, so neighbours tie; all one value; and from 1 to 20 sorted, rising
or falling, which pushes the answers up (to 28 at most). Every random
choice, P3's lift, P5's place and rise and P6's cut among them, is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | the array backwards gives the same answer |
| P3 | every element raised by the same 1 to 50 gives the same answer |
| P4 | every element doubled gives no fewer moves and no more than twice as many |
| P5 | one element raised by 1 to 50 raises the answer by no more than that |
| P6 | past one element, the array cut in two: the two parts' answers sum to no more than the whole's |

All 58,875 checks pass on every arm: `2000 arrays: checksum 907216185,
58875 checks over 5 arms: 0 failures`. A Python reading of the same
arrays, by the same search, with the six properties asserted against the
★ arm's mirror, gives the same line.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. Twenty-eight are caught; two are
equivalent. The windows arm adding each place's moves to the other
parity's count swaps the two counts, and the answer is the smaller of
them either way. The lowered arm reading a place's left neighbour from
the copy it is cutting reads a place of the other parity, which that pass
never cuts. Fifteen are kept, no two failing the same checks; one of them
stops the run.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only the even places lowered | P1 836, P2 711, P6 212 |
| M2 | ★: a place level with its neighbour left alone | P1 961, P5 3 |
| M3 | ★: the right neighbour only, when there are two | P1 501, P2 785, P6 44 |
| M4 | windows: the left neighbour only | P1 895, P2 853 |
| M5 | windows: the fence after the array at 0 | P1 588, P2 825, P3 301, P6 214 |
| M6 | windows: the dearer count | P1 1437, P6 153 |
| M7 | iter: a place already low counted as negative moves | stops: integer overflow |
| M8 | iter: the odd places a move dearer | P1 836, P2 711, P6 158 |
| M9 | iter: below the larger neighbour | P1 1428 |
| M10 | lowered: the right cut tested on the place as given | P1 141, P2 242, P6 12 |
| M11 | lowered: every place cut | P1 1573, P2 1083 |
| M12 | lowered: the first place of the parity left alone | P1 1212, P2 664 |
| M13 | solution: the first place's missing neighbour 0 | P1 601, P2 825, P3 292, P6 200 |
| M14 | solution: each count the last place's moves | P1 1150, P2 659, P6 383 |
| M15 | solution: places counted in pairs | P1 978, P2 378, P6 35 |

P1 catches all fourteen edits that let the run finish. P2 catches eleven,
the edits that treat the two ends of the array unlike: an array of even
length read backwards swaps its parities, so an edit that favours one
parity fails it (M1, M8), as do edits that favour one neighbour (M3, M4,
M10) or one end (M5, M11, M12, M13, M14, M15). The three P2
misses are symmetric: ties left alone (M2), the dearer count (M6), and
the larger neighbour (M9). P6 catches nine, the edits whose answer for
the whole can fall below what its two parts cost apart: a choice of
parity tied to where the array starts, or the dearer choice taken (M1,
M6, M8); counts that are not each parity's sum (M14, M15); and a cost at
a place that changes when the cut leaves it at an end (M3, M5, M10,
M13). P3 catches only the two edits
that compare an element with a fixed 0 standing in for a missing
neighbour, rather than with another element (M5, M13). P5 catches only
the ties left alone (M2), on three arrays: an array whose only fault is a
tie, such as `[6, 18, 18, 19]`, answers 0, and raising one of the tied
pair by 5 turns the tie into a cost of 6. P4 catches none of the thirty:
every edit still answers with the smaller or larger of two sums of
per-place moves, each how far a place stands above a neighbour plus at
most one, and doubling every height at most doubles such a sum and never
shrinks it. The edit that stops the run is the iterator arm's moves left
negative: a place at an end, whose missing neighbour stands at
`i64.MAX`, counts nearly `-i64.MAX` moves, and two of them overflow.

Of the thirteen caught and not kept, two fail exactly as a kept one: the
even places for both parities in the iterator arm and the even count
always in the solution arm, as M1. Three pairs fail alike: a place
brought level with its neighbour in the ★ and solution arms; the odd
places' moves always in the ★ arm and only the odd places lowered in the
lowered arm; and the first place never lowered in the windows arm and
never counted in the solution arm. The other five (the last element never
a neighbour in the ★ arm, the first element dropped in the windows arm,
the last place its own neighbour and the second place's left neighbour
ignored in the iterator arm, and a place cut level with its left
neighbour in the lowered arm) each fail in a way of their own and were
not needed.

## Verification

Every arm prints the same output as `moves_to_make_zigzag.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The ★, windows, iterator and lowered arms were written as Kāra and
checked clean as written. `karac fix` carried the solution arm in three
rounds: `Vec<i32>` to `Vec[i32]`, `std::cmp::max` and `std::cmp::min` to
`max` and `min`, and `Solution::` to `Solution.`; then `struct Solution
{}` declared; then `0i32` on the first literal of the counts and the `as
i64` that widens the call's `i32` for nothing dropped.

The kata found one gap. `let mut res = [0, 0]`, its elements added to
with `i32` amounts and `min(res[0], res[1])` returned as the `i32`
answer, was refused with only "write an explicit `as i32`": an array of
literals takes its type from its first, which an operator leaves at the
default `i64`, and only a fill (`Vec.filled(2, 0)`) or a lone literal was
offered its suffix. An array of literals bound whole now offers its first
literal's suffix at a narrowing read of an element (B-2026-11-12-16,
fixed).

The bench found one gap in speed: a `step_by(2)` loop over a range costs
about 1.2x the same loop with `while` (B-2026-11-12-17, open; see
Benchmarks).

## Benchmarks

The bench builds 20 arrays of 1000 values from 1 to 1000 once,
LeetCode's longest. Each of 5000 rounds draws one value of every array
again and answers every array with the ★ arm: 100,000 calls, each two
passes over half the array. Every implementation prints `5000 rounds
over 20 arrays of 1000 values: answers total 12036077501, checksum
284778734`. Kāra and Rust step over the places with `step_by(2)`, C and
Go with `i += 2`, Python with `range(low, n, 2)`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `9049969b63`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.055 to 0.113 s | 0.062 s |
| C (`clang -O3`) | 0.063 to 0.116 s | 0.076 s |
| Rust (`rustc -O`) | 0.096 to 0.169 s | 0.102 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.317 to 0.381 s | 0.328 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.282 to 0.380 s | 0.336 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.369 to 0.531 s | 0.489 s |
| Kāra (`karac build`) | 0.390 to 0.534 s | 0.490 s |
| Go | 0.613 to 0.763 s | 0.687 s |
| Python | 20.8 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust under overflow checks takes about 0.67x Kāra's median time,
and most of that gap is the `step_by(2)` loop: over seven interleaved
runs the Kāra program took a median 484 ms, the same program with the
loop written `while i < n { ... i += 2; }` 403 ms, and Rust under
overflow checks 408 ms. Kāra's `step_by` over a range goes through the
general iterator, a first-item flag and an advance of `step - 1` each
returning an `Option`, where Rust's is specialized for ranges
(B-2026-11-12-17). Without the checks, Rust takes about 0.21x Kāra's time
and C about 0.13x to 0.16x: every lowered place adds its moves to a sum,
and the checked builds test each addition, but this README has not
measured how much of the unchecked builds' lead that is. Go takes about 1.4x Kāra's time and
Python about 43x.
