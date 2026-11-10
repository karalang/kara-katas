# 2040. Kth Smallest Product of Two Sorted Arrays

Given two sorted 0-indexed integer arrays `nums1` and `nums2` as well as an
integer `k`, return the `k`-th (1-based) smallest product of `nums1[i] *
nums2[j]` where `0 <= i < nums1.length` and `0 <= j < nums2.length`.

```
nums1 = [2,5], nums2 = [3,4], k = 2                          ->  8
nums1 = [-4,-2,0,3], nums2 = [2,4], k = 6                    ->  0
nums1 = [-2,-1,0,1,2], nums2 = [-3,-1,2,4,5], k = 3          ->  -6
```

**Constraints:** `1 <= nums1.length, nums2.length <= 5 * 10^4`; `-10^5 <=
nums1[i], nums2[j] <= 10^5`; `1 <= k <= nums1.length * nums2.length`; both
arrays are sorted in non-decreasing order.

There are up to `2.5 * 10^9` products, too many to list, but their count at
most `x` grows with `x`, so the answer is the least `x` whose count reaches
`k`, and a binary search over `-10^10 ..= 10^10` finds it in about 35
counts. Each count is quick because `nums2` is sorted: for a positive `a`
the `b`s with `a b <= x` are a prefix, for a negative `a` a suffix (the
product falls as `b` grows), and for `a = 0` all of them or none.

## Approaches

| file | mechanism |
|---|---|
| `product.kara` ★ | binary search on the answer; each count a `partition_point(\|b\| a * b <= x)` per `a`, the suffix for a negative `a` by `partition_point(\|b\| a * b > x)`. O(n log m log V) |
| `product_pointers.kara` | the same search, each count by two pointers: the positive `a`s walked so that `x / a` only grows (downward when `x >= 0`, upward when not), the negative ones so that the suffix's first index only moves right; `filter(..).cloned().collect()` splits the signs. O((n + m) log V) |
| `product_division.kara` | the bounds by division: `b <= floor(x / a)` for a positive `a`, `b >= -floor(x / -a)` for a negative one, both by `div_euclid`, each found by a hand-written search for the first value above it. O(n log m log V) |
| `product_signs.kara` | the sign groups first: the negative, zero and positive products counted from the groups' sizes, which says where the `k`-th lies; `0` answered at once, or a `Signs` struct's two groups searched over one side of zero only, `let mut (groups, rank, lo, hi) = if .. { .. } else { .. }`. O(n log m log V) |
| `product_iter.kara` | the count as `nums1.iter().map(..).sum()` in a closure, the search a `(lo, hi)` pair halved in a `loop` by `lo, hi = if .. { (lo, mid) } else { (mid + 1, hi) }` |
| `product_solution.kara` | LeetCode's Rust template (`impl Solution`, `Vec<i32>`, a closure `\|x: i64\| -> i64`, `for &a in &nums1`, `partition_point(\|&b\| ..)`, `as i64` throughout, `-10_000_000_000i64`), carried by `karac fix` in two rounds to a clean check |
| `differential.kara` | the five arms that check against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's
three examples and five more; then the sum and a checksum of the answers
for 2000 problems of 1 to 8 values a side up to 1 to 20 either side, and
for 4 large problems (50000 values a side, the most the constraints allow,
then 10000, 5000 and 1000, values up to 100000, 3, 1000 and 100000 either
side). `product.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the
statement read literally: every product formed, sorted, and the `k`-th
taken. It checks 1500 problems of 1 to 6 values a side up to 1 to 30 either
side, each with a value to add. Every random choice is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the two arrays swapped leave the answer |
| P3 | both arrays negated (and reversed, to stay sorted) leave the answer |
| P4 | one array negated turns the `k`-th smallest into minus the `k`-th largest |
| P5 | a value added to the first array never raises the answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `1500 problems: checksum 232636948, 54000 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum of
the literal answers is also computed by a few lines of Python. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, five or six to each of its arms,
each run under `karac __mir-run` and `karac __mir-llvm-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. All
thirty-one are killed, each fails the same way under both backends, none
by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a product counted only below the bound (`<` for `<=`) | P1 694, P2 708, P3 1349, P4 1419, P6 694 |
| M2 | ★: the search stopping past `k` (`> k` for `>= k`) | P1 1253, P4 1419, P6 1253 |
| M3 | ★: a negative `a`'s suffix taken as a prefix | P1 1211, P2 753, P3 1037, P4 1038, P6 1211 |
| M4 | pointers: the positive `a`s always walked upward | P1 171, P2 194, P3 306, P4 342, P6 171 |
| M5 | pointers: the negative `a`s always walked upward | P1 179, P2 199, P3 328, P4 347, P5 22, P6 179 |
| M6 | pointers: the last `b` never reached by a positive `a` | P1 462, P2 544, P3 590, P4 828, P6 462 |
| M7 | division: the positive bound truncated (`/` for `div_euclid`) | P1 328, P2 641, P3 640, P4 675, P6 328 |
| M8 | division: the negative bound one too high | P1 759, P2 1041, P3 1358, P4 1424, P6 759 |
| M9 | division: the first value at the bound taken as above it | P1 1371, P2 1374, P3 1381, P6 1371 |
| M10 | signs: zero times zero counted twice | P1 9, P4 19, P6 9 |
| M11 | signs: the positive rank not past the zeros | P1 126, P4 251, P6 126 |
| M12 | signs: negative times negative taken as positive times positive | P1 528, P3 672, P4 1034, P6 528 |
| M13 | iter: a zero `a` counted as nothing at a bound of zero (`x > 0` for `x >= 0`) | P1 82, P2 114, P4 96, P6 82 |
| M14 | iter: only the first array's first value counted (`take(1)`) | P1 1141, P2 709, P3 358, P4 1248, P5 99, P6 1141 |
| M15 | iter: a positive `a`'s bound one too high (`x + 1`) | P1 683, P2 712, P3 1350, P4 1424, P6 683 |
| M16 | solution: the adapter reversing the second array | P1 859, P2 1076, P3 664, P6 859 |
| M17 | solution: the search's upper end overshot (`hi = mid - 1`) | P1 667, P4 952, P6 667 |

P1 and P6 kill all seventeen, P4 fifteen, P2 twelve, P3 twelve and P5
two. P2
swaps the arrays, so it sees the edits that treat `nums1` and `nums2`
differently: every edit to the count per `a` over a sorted `nums2` (M1,
M3 to M9, M13 to M15) and the adapter's `nums2` reversed (M16). It misses the edits
that see only how many products there are on each side of a bound, which
the swap leaves alone: the search past `k` or overshooting (M2, M17) and
the signs arm's three, whose groups pair the arrays symmetrically (M10,
M11; M12 doubles the positive pairs from both sides). P3 negates both
arrays, which keeps every product, so it misses the same edits less M12,
whose error is about which sign a value has, and also the iterator arm's
zero `a` (M13), which a negation leaves a zero. P4 negates one array, which
turns the products' order around; it misses only the division arm's value
at the bound (M9) and the adapter's reversal (M16), whose wrong answers
happen to keep that relation. P5 adds a value to `nums1`, which only adds
products, so an answer can rise only if a count can fall when a value
joins: every edit counts per `a` and sums except two. M5's one pointer is
shared by the negative `a`s walked the wrong way, so a new `a` can carry it
past the `b`s a later one needed; and M14 counts only the first `a`, which a
smaller new value replaces.

The other fourteen fail as a kept one does, or with a signature of their
own that adds nothing. The Rust arm's product counted only below the bound
fails as M1, and so do the iterator arm's; its search stopping past `k`
fails as M2 and its negative `a`'s suffix taken as a prefix as M3. The
zeros counted only above zero in the division and Rust arms fail as M13. A zero product counted at every bound fails alike in the ★
and pointers arms, and a negative `a`'s products at the bound left out alike in
the pointers and Rust arms, each with counts of their own. The ★ arm's
search starting at zero, the division arm's search overshooting in its own
partition point, and the signs arm's last zero product missed and its
positive products searched from 2 fail with counts of their own.

## Verification

Every arm prints the same output as `product.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error. `karac
run` and a `karac build` binary print the same output for every arm and
the differential. `karac check --output=json` reports nothing on
any of them. Under `karac __mir-run` the arms take 10 s (division) to 28 s
(Rust) and the differential 20 s, on kara 991c45adcd.

The iterator arm was blocked until kara `b415f2e55f`. Its search carries
`(lo, hi)` and halves it with Rust's destructuring assignment, `(lo, hi) =
if at_most(mid) >= k { (lo, mid) } else { (mid + 1, hi) };`. Kāra refused
it with E_ASSIGN_TARGET_NOT_PLACE, whose advice was to drop the
parentheses, `karac fix` had no edit for it, and `lo, hi = if ..` was then
a parse error ("2 target(s) but 1 value(s)"): a parallel assignment took
only a literal list of values. That was B-2026-11-09-38. Now a parallel
assignment takes a single tuple value apart, and `karac fix` drops the
parentheses, so the arm checks after one fix. A parenthesized tuple stays a
value, not a place, as the review thread's ruling on the row has it.
Before that, `karac fix` removed the closure's `-> i64`, which Kāra does
not write.

The signs arm's `let (mut groups, mut rank, mut lo, mut hi)` became `let
mut (groups, rank, lo, hi)` through `karac fix`. The other three Kāra arms
checked as written.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in two rounds (twelve edits, then six) to a clean check: `Vec<i32>` to
`Vec[i32]`, the closure's `-> i64` dropped, `for &a in &nums1` to `for a in
ref nums1`, `|&b|` to `|b|`, the `as i64` on each count and the `0i64` and
`i64` suffixes dropped (a `usize` count is an `i64` in Kāra), and `let (mut
lo, mut hi)` to `let mut (lo, hi)`. `a * b as i64` and `(hi - lo) / 2`
carry as they are.

## Benchmarks

The bench builds 4 pairs of sorted arrays of 50000 values a side once in
all five languages, and runs the ★ arm on each for 3 values of `k`: 12
calls. Every implementation prints `12 calls: sum -19589870, checksum
934614517`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `991c45adcd` on LLVM 22:

| | time | median |
|---|---|---|
| Go | 0.536 to 0.597 s | 0.547 s |
| Rust (`rustc -O`) | 0.542 to 0.614 s | 0.557 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.554 to 0.600 s | 0.563 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.661 to 0.691 s | 0.679 s |
| Kāra (`karac build`) | 0.673 to 0.707 s | 0.690 s |
| C (`clang -O3`) | 0.781 to 0.819 s | 0.790 s |
| Python | 40.7 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.682 s) is not above its real time (0.690 s).

The sequential Kāra program is 1.21x Rust under overflow checks and 0.86x
C.
