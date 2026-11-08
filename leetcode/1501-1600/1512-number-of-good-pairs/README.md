# 1512. Number of Good Pairs

Given an array of integers `nums`, return the number of good pairs. A
pair `(i, j)` is called good if `nums[i] == nums[j]` and `i < j`.

```
nums = [1, 2, 3, 1, 1, 3]  ->  4   (0,3), (0,4), (3,4), (2,5)
nums = [1, 1, 1, 1]        ->  6
nums = [1, 2, 3]           ->  0
```

**Constraints:** `1 <= nums.length <= 100`; `1 <= nums[i] <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `pairs.kara` ★ | walking left to right, each number pairs with every earlier copy of itself: add how many copies have been seen, then count it. Values are at most 100, so the counts sit in a table. O(n) |
| `pairs_map.kara` | the same walk with the counts in a `Map`, so any values do. O(n) |
| `pairs_sort.kara` | sorted, equal numbers sit in runs, and a run of `r` makes `r (r - 1) / 2` pairs. O(n log n) |
| `pairs_iter.kara` | the counts by `fold` into a `Map`, then each count's pairs summed over `values()` (a sum, so the map's order does not show) |
| `pairs_solution.kara` | LeetCode's Rust template (`HashMap::new()`, `for &x in nums.iter()`, `count.entry(x).or_insert(0)`), the ★ arm's walk, carried by `karac fix`. It checks and runs under the interpreter, and crashes compiled: B-2026-11-08-18 |
| `differential.kara` | the four arms that run on every lane against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples and two
more, then a checksum of the answers for 3000 arrays of 1 to 100 numbers
up to 10, 300 up to 100, and 3 of 1 to 100000 numbers up to 100.
`pairs.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every pair `i < j` compared. It checks 3000 arrays of 1 to 12
numbers drawn from 1 to `top`, `top` itself from 1 to 6, so most arrays
repeat. Every random choice of a problem is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the numbers in another order leave the answer |
| P3 | every number mapped one to one (`x` to `101 - x`) leaves the answer |
| P4 | one more copy of a number adds as many pairs as it had copies |
| P5 | the array written twice over has `4 a + n` pairs: each pair four ways, and each number with its own twin |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 736056119, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property. The Rust arm joins it
once it runs compiled.

## Mutation testing

Seventeen edits to the differential, four or five to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run`. Twelve are kept. All
seventeen are killed, each the same way under both backends and none by
a crash.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the number counted before its copies are added | P1 3000, P4 3000, P5 3000, P6 3000 |
| M2 | ★: at most three earlier copies added | P1 804, P4 967, P5 1894, P6 804 |
| M3 | ★: counted at `x % 50` | P3 2506 |
| M4 | ★: odd numbers' pairs only | P1 1590, P3 2267, P4 1100, P5 2240, P6 1590 |
| M5 | map: each count reset to 1 | P1 1894, P4 2155, P5 2506, P6 1894 |
| M6 | map: each step's pairs rounded down to even | P1 2506, P4 1721, P5 2823, P6 2506 |
| M7 | map: counted at `x / 2` | P1 2393, P2 1260, P3 1805, P4 2807, P5 3000, P6 2393 |
| M8 | sort: a run ends only at a gap of two | P1 2012, P3 522, P4 1704, P6 2012 |
| M9 | sort: each new run started one place early | P1 2224, P5 2224, P6 2224 |
| M10 | sort: not sorted | P1 1676, P2 1397, P4 1782, P5 2224, P6 1676 |
| M11 | iter: each count grown by the number, not 1 | P1 2416, P3 3000, P4 1760, P5 2416, P6 2416 |
| M12 | iter: each count capped at 2 | P1 1269, P4 1495, P5 2506, P6 1269 |

P1 and P6 kill eleven of the twelve, P5 ten, P4 nine, P3 five, and P2
two. M3 is seen only by P3: the differential's numbers stay below 50, so
`x % 50` changes nothing until they are mapped to 95..100. P2 sees the
two edits that make the answer depend on where equal numbers sit: no
sort, and counts kept at `x / 2`, where 2 and 3 share a slot.

The other five: the ★ arm counting twice per number (P1 2506, P4 3000, P5
3000, P6 2506), the map arm's counts starting at 1 and the iterator arm's
`c (c + 1) / 2` (both as M1), the iterator arm's `(c - 1)^2` (as M5), and
the sort arm's `run * run / 2` (as M6).

## Rust template: B-2026-11-08-18

The Rust arm was written as LeetCode's Rust template plus a thin `i64`
wrapper. `karac fix` makes 9 edits, then 1 and 1 (`HashMap::new()` to
`Map.new()`, `for &x` to `for x`, the `use` dropped), and the arm checks
and prints the expected output under `karac __mir-run`. Compiled, it
dies: `karac __mir-llvm-run` exits 101 with nothing on stdout or stderr,
and `karac run` and a `karac build` binary with SIGSEGV. ASan names
`hash.ref i32`. With `count` untyped, its key type is taken from `x`, the
element binding of `nums.iter()`, as `ref i32`, while the key the compiled
code hands the hash is the copied value. Seven lines reproduce it (in the
row); writing `let mut count: Map[i32, i32] = Map.new();` makes it run on
every lane. This is a run-vs-build divergence, so the arm is kept as
`karac fix` left it and out of the differential until the row lands.

## Benchmarks

The bench builds 50 arrays of 200000 numbers from 1 to 100 once and
counts each four times by the ★ arm in all five languages. Every
implementation prints `200 counts over 50 arrays of 200000 numbers:
checksum 827870611`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `1dce193ad` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.118 s |
| C (`clang -O3`) | 0.126 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.130 s |
| Kāra (`karac build`) | 0.140 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.141 s |
| Go | 0.170 s |
| Python | 3.94 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.106 s and 0.146 s on one run).

Kāra is 1.08x Rust under overflow checks by median. Building the ten
million numbers is part of every timing.

## Verification

The ★, map, sort and iterator arms print the same output as `pairs.py`
under `karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`,
and `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any arm. The
Rust arm prints the expected output under `karac __mir-run` only (see
above; ASan reports a stack-buffer-overflow READ of size 8 in
`hash.ref i32`). Under `karac __mir-run` the arms take 0.3 to 0.8 s and
the differential 1.0 s.

## Writing it

The arms were written in Kāra and `karac fix` had nothing to change.
