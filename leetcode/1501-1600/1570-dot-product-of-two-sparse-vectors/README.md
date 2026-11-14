# 1570. Dot Product of Two Sparse Vectors

Given two sparse vectors, compute their dot product. Implement class
`SparseVector`: `SparseVector(nums)` initializes the object with the
vector `nums`, and `dotProduct(vec)` computes the dot product between the
instance of `SparseVector` and `vec`. A sparse vector is a vector that
has mostly zero values; store it efficiently and compute the dot product
between two of them.

```
nums1 = [1,0,0,2,3], nums2 = [0,3,0,4,0]               ->  8
nums1 = [0,1,0,0,0], nums2 = [0,0,0,0,2]               ->  0
nums1 = [0,1,0,0,2,0,0], nums2 = [1,0,0,0,3,0,4]       ->  6
```

**Constraints:** `n == nums1.length == nums2.length`; `1 <= n <= 10^5`;
`0 <= nums1[i], nums2[i] <= 100`.

## Approaches

Each arm is a `struct SparseVector` with `new` and `dot_product(ref self,
other)`, and a `dot(a, b)` that builds both and multiplies them.

| file | mechanism |
|---|---|
| `sparse.kara` ★ | the values other than 0 kept with their indices in index order, by `enumerate().filter(..).collect()`; the product a merge of the two lists by two pointers that multiplies where the indices meet. O(a + b) |
| `sparse_map.kara` | a `Map` from index to value; the product walks the smaller map and looks each index up in the other (`get(i).cloned().unwrap_or(0)`). A walk is in hash order, which a sum does not see. O(min(a, b)) expected |
| `sparse_search.kara` | the ★ arm's pairs, but the product finds each index of the shorter list in the longer by `partition_point`. O(a log b) for a <= b |
| `sparse_solution.kara` | LeetCode's Rust template (`new(nums: Vec<i32>) -> Self`, `dot_product(&self, vec: SparseVector) -> i32`, a `HashMap<usize, i32>`), carried by `karac fix` and one hand edit |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples, then
`[0] . [0]`, `[7] . [6]`, three values of 100 against themselves, and two
vectors that never meet; then the sum of the products and a checksum for
3000 random pairs of up to 10 values from 0 to 3, 300 of up to 1000 and
30 of up to 100000 values up to 100, each vector with its own odds of a
value other than 0. `sparse.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the dense vectors multiplied index by index and summed. It
checks 3000 pairs of 1 to 10 values from 0 to 3, each vector with its own
odds of a value other than 0, every random choice drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the two vectors swapped leave the answer |
| P3 | both vectors reversed leave the answer |
| P4 | every value of the first doubled doubles the answer |
| P5 | each vector written twice over doubles the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 725885714, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

The first M1 left the second pointer in place after a match, which the
next step moves on anyway (an index appears once in a list), and the
first M9 shifted every index the template stores by one, which both
vectors share; both were equivalent and were replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first pointer moved where the second is behind | P1 904, P2 1289, P3 820, P5 492, P6 904 |
| M2 | ★: the pointer behind compared the wrong way | P1 1511, P3 1166, P5 711, P6 1511 |
| M3 | ★: the merge stops one pair early on the left | P1 1669, P2 879, P3 1509, P5 1669, P6 1669 |
| M4 | map: the smaller map looked up in itself | P1 1427, P2 2135, P4 1615, P6 1427 |
| M5 | map: only values above 1 kept | P1 1752, P4 977, P6 1752 |
| M6 | search: the search lands past the index | P1 2270, P6 2270 |
| M7 | search: the index multiplied in place of the value | P1 2074, P2 433, P3 1994, P4 739, P5 2270, P6 2074 |
| M8 | search: the first value never kept | P1 1118, P3 1379, P5 1118, P6 1118 |
| M9 | template: values of 1 dropped and zeros kept | P1 1752, P4 977, P6 1752 |
| M10 | template: each index looked up in its own map | P1 2524, P2 2796, P4 2719, P6 2524 |

## Benchmarks

The bench builds 20 vectors of 500000 values, one in 10 of them from 1 to
100 and the rest 0, makes each sparse once, and then takes the product of
every ordered pair of them, 400 products, by the ★ arm, in all five
languages. Every implementation prints `400 products of 20 vectors of
500000 values: products sum 8124631893, checksum 377397379`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O -C overflow-checks=on`) | 0.295 s |
| Rust (`rustc -O`) | 0.299 s |
| C (`clang -O3`) | 0.326 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.353 s |
| Kāra (`karac build`) | 0.353 s |
| Go | 0.420 s |
| Python | 8.4 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.34 s and 0.36 s on one run).

Kāra is 1.20x Rust under overflow checks by median, and runs 1.47x its
instructions (callgrind: 1.20G against 0.82G). Building the vectors
alone takes 0.08 s against Rust's 0.06 s, so most of the gap is the
merge, whose loop keeps both bounds checks: the vectors are fields of the
two receivers, and the pass that drops a check a loop's guard already
makes reaches only a local vector. Filed as B-2026-11-14-28.

## Verification

All four arms print the same output as `sparse.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The ★ arm was written in Kāra and checked as written.

The map and search arms pick the shorter of the two by a tuple, as Rust
does with `(&self.pairs, &other.pairs)`. Written without a `ref`,
`(self.pairs, other.pairs)` is a move out of the two borrowed receivers,
and `karac check` offers a `.clone()` on each, which `karac fix` applies:
it checks and is right, but copies both vectors on every product. The
arms write `(ref self.pairs, ref other.pairs)`, which copies nothing and
checks; filed as B-2026-11-14-23. The map arm was also first written
with Rust's `.copied()` on the `get`, which `karac fix` rewrote to
`.cloned()` in one round.

The Rust template took three rounds of `karac fix`, 9 changed lines and 2
removed, then 2 and 2 changed:

1. the `use std::collections::HashMap;` line removed, the `HashMap<..>`
   and `Vec<..>` types to `[..]`, `HashMap::new()` to `HashMap.new()`,
   `(i, &x)` and the wrapper's `|&x|` to `(i, x)` and `|x|`, `&self` to
   `self`, and `SparseVector::` to `SparseVector.`;
2. `HashMap` to `Map`, in the field and the constructor;
3. `total`'s literal to `total: i32`, and the wrapper's `as i64` dropped.

It then stopped on `expected 'Map[usize, i32]', found 'Map[i64, i32]'`
at `SparseVector { values }`, with no fix: `enumerate()` gives `i64`
indices, and the fix that turns a written `usize` into `i64` is offered
for a `Vec[usize]` field but not a `Map[usize, _]` one. Filed as
B-2026-11-14-24. One hand edit, `values: Map[usize, i32]` to
`Map[i64, i32]`, made it check and agree.
