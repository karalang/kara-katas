# 2090. K Radius Subarray Averages

You are given a 0-indexed array `nums` of `n` integers, and an integer
`k`.

The k-radius average for a subarray of `nums` centered at some index
`i` with the radius `k` is the average of all elements in `nums`
between the indices `i - k` and `i + k` (inclusive). If there are less
than `k` elements before or after the index `i`, then the k-radius
average is `-1`.

Build and return an array `avgs` of length `n` where `avgs[i]` is the
k-radius average for the subarray centered at index `i`.

The average of `x` elements is the sum of the `x` elements divided by
`x`, using integer division. The integer division truncates toward
zero, which means losing its fractional part.

```
nums = [7,4,3,9,1,8,5,2,6], k = 3  ->  [-1,-1,-1,5,4,4,-1,-1,-1]
nums = [100000], k = 0             ->  [100000]
nums = [8], k = 100000             ->  [-1]
```

**Constraints:** `n == nums.length`; `1 <= n <= 10^5`; `0 <= nums[i], k
<= 10^5`.

Every window is `2k + 1` wide and the next one differs by a value in
and a value out, so one running sum, slid along, gives every average,
O(n). The values are not negative, so truncating toward zero is the
floor. The approaches differ in how they keep the window's sum.

## Approaches

| file | mechanism |
|---|---|
| `averages.kara` ★ | one window sliding along in a `for` over the places: each value added as it enters, the one `2k + 1` back taken out, the average written `k` places back once the window is full. O(n) |
| `averages_prefix.kara` | prefix sums in a `Vec.filled(n + 1, 0)`, each window the difference of two. O(n) |
| `averages_windows.kara` | `nums.windows(2k + 1)`, every window summed afresh with `iter().sum()`, between `k` places of -1 at each end. O(n · k) |
| `averages_scan.kara` | by iterators: the running sums from `scan`, `once(0)` chained in front, and each place `map`ped to -1 or a difference over the width. O(n) |
| `averages_deque.kara` | a `struct Window` over a `VecDeque`, whose `push` takes the oldest value out of the front and the sum once more than the width is held, and gives `Some(average)` when full. O(n) |
| `averages_solution.kara` | LeetCode's Rust template (`nums: Vec<i32>, k: i32`, `vec![-1; n]`, the first window's `i64` sum from `nums[..w].iter().map(\|&x\| x as i64).sum()`), carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and four
more, each array, radius and averages; then the sum and a checksum of
the averages for 2000 random arrays of 1 to 100 values below 10, 1000 or
100000, the radius from 0 to 59; then the constraints' largest, 100000
values up to 100000, at a radius of 10, of 49999 (one window, the whole
array but its last value) and of 50000 (no window). `averages.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each place, -1 when fewer than `k` values lie before it
or after it, and otherwise the values from `k` before to `k` after added
one by one and divided by their count. It checks 300 random arrays of 1
to 12 values below 4, 10 or 1000, the radius from 0 to 6; then 20 of
radius 0, and 20 whose radius leaves no window. All 340 are drawn before
any arm answers.

| | property |
|---|---|
| P1 | the averages are the statement read literally |
| P2 | -1 stands at the first and last `k` places and nowhere else |
| P3 | every value times the window's width gives averages that, divided by the width, are the averages |
| P4 | the array reversed gives the averages reversed |
| P5 | 7 added to every value adds 7 to every average |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 arrays: checksum 560414124, 12240 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal averages was checked against a Python reading of the same
arrays. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first value never taken out | P1 129, P4 136, P5 152, P6 129 |
| M2 | ★: the first full window skipped | P1 174, P2 174, P4 154, P6 174 |
| M3 | ★: the average rounded up | P1 104, P3 104, P6 104 |
| M4 | prefix: each prefix only its own value | P1 171, P2 36, P3 15, P4 134, P5 171, P6 171 |
| M5 | prefix: the width counted one more | P1 153, P5 172, P6 153 |
| M6 | prefix: the edges left 0 | P1 272, P2 272, P5 272, P6 272 |
| M7 | windows: one -1 too many at the end | P1 174, P2 174, P3 174, P4 174, P5 174, P6 174 |
| M8 | windows: a window as long as the array refused | P1 20, P2 20, P6 20 |
| M9 | windows: each sum divided by the array's length | P1 147, P5 154, P6 147 |
| M10 | scan: the running sums from 1 | P1 85, P2 7, P4 93, P5 7, P6 85 |
| M11 | scan: each sum divided by `k + 1` | P1 106, P5 106, P6 106 |
| M12 | scan: each running sum the one before | P1 153, P4 153, P5 167, P6 153 |
| M13 | deque: the oldest taken out once the window is full | P1 174, P2 174, P6 174 |
| M14 | deque: the oldest left in the sum | P1 145, P4 147, P5 154, P6 145 |
| M15 | deque: each value counted one less | P1 174, P2 38, P3 104, P4 121, P5 45, P6 174 |
| M16 | solution: the adapter's values halved | P1 173, P3 30, P5 174, P6 173 |
| M17 | solution: the walk starting a window late | P1 154, P2 154, P4 149, P5 16, P6 154 |

P1 and P6 kill all seventeen, P5 thirteen, P2 and P4 nine each, and P3
five. P5, which adds 7 to every value, sees every edit that is not a
true average: a wrong divisor (M5, M9, M11), the wrong values summed
(M1, M12, M14), and the halved values (M16). P4, the array reversed,
sees what treats the two ends differently: the first window skipped
(M2, M17), the first value never taken out (M1), the running sums
shifted or started at 1 (M10, M12). P2 sees a -1 put where an average
belongs or left out where one does not (M2, M6, M8, M13, M17). P3 sees
the one edit nothing else but P1 does, the average rounded up (M3): the
scaled values divide exactly, and their floor is not the ceiling.

Of the thirty, thirteen were not kept, and none survives. Eight fail as
a kept one: the prefix arm's last average left out, the scan arm's last
average dropped, the deque arm's window one wider and the Rust arm's
first window's average not set as M2; the ★ arm's sum divided by one
more as M5; the scan arm's running sums each only their own value as
M4; the Rust adapter's radius one more as M13; the Rust arm's walk that
takes nothing out as M14. Five are killed with checks of their own but
were left out because their arm keeps three: the ★ arm's value one
place later taken out (P1 135, P4 132), the prefix arm's window's last
value left out (P1 157, P4 84, P5 173), the windows arm's leading
places 0 (P1 106, P2 106, P4 106, P5 106) and its first window skipped
(P1 174, P2 174, P3 174, P4 134, P5 174), and the deque arm's averages
one more (P1 174, P3 101).

## Verification

Every arm prints the same output as `averages.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 1.1 s to 3.5 s, but for the
windows arm's 4.9 s, which sums every window afresh, and the
differential 0.7 s (timed while other work shared the machine).

The bench met a compiler gap. It asks each array for ten radii, written
`let radii = [0, 1, 3, ...]` and walked with `for k in radii.iter()`,
and `get_averages(nums, k)` was refused with "expected 'i64', found 'ref
i64'": a borrowed element handed to a by-value parameter is read as a
copy, but not while the array's literals were still open, and the call
did not fix them. It does now, as the element's own value would be
fixed. Probing it found two more: `Vec.filled(2, k)` over the same loop
was a vector of borrows of the element, which the compiled backends read
as a pointer and crashed on, where the interpreter printed the right
sum; and `let fs = [1.0, 3.0];` was typed `f64` at once, so its elements
could not reach an `f32` parameter, though a list of integer literals is
left open for its use to fix. Both are fixed with the first, in kara
81aca4606b, test `tests/kata_2090_literal_ref_arg.rs`.

The scan arm first chained the running sums after `[0].iter()`, which
yields borrows where `scan` yields values, and was refused as Rust
refuses it; it chains them after `once(0)`, the library's spelling.

The Rust arm was written as LeetCode's Rust template. `karac fix`
carries it in three rounds of 16, 2 and 3 edits: Rust's spellings
(`Vec<i32>` to brackets, the `&` of `|&x|` and `|&a|` dropped, `struct
Solution;` to `struct Solution {}`, `Solution::` to `.`, the adapter's
`&Vec<i64>` to `ref`); then `k as usize` to `k as i64` and `vec![-1;
n]` to `Vec.filled(n, -1)`; then the `as i64` of `w as i64`, which is
one already, and the adapter's `ref` parameter to a bare one, which
borrows already. The fixed arm reads as the template does.

## Benchmarks

The bench builds 30 arrays of 100000 values up to 100000, the
constraints' limit, and asks each for ten radii from 0 to 20000 with the
★ arm in all five languages, the averages of each answer in a fresh
growable array (a `Vec`, a `Vec`, a slice, a `list`, a `malloc`'d
buffer): 300 slides down `10^5` values. Every implementation prints `300
answers: sum 467294040895, checksum 140895764`.

BENCHTAB
