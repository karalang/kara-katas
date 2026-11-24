# 1313. Decompress Run-Length Encoded List

We are given a list `nums` of integers representing a list compressed
with run-length encoding.

Consider each adjacent pair of elements `[freq, val] = [nums[2*i],
nums[2*i+1]]` (with `i >= 0`). For each such pair, there are `freq`
elements with value `val` concatenated in a sublist. Concatenate all the
sublists from left to right to generate the decompressed list.

Return the decompressed list.

```
nums = [1,2,3,4]  ->  [2,4,4,4]
nums = [1,1,2,3]  ->  [1,3,3]
```

**Constraints:** `2 <= nums.length <= 100`, `nums.length % 2 == 0`,
`1 <= nums[i] <= 100`.

The arms are `fn decompress_rl_elist(nums: Vec[i64]) -> Vec[i64]`.

## Approaches

| file | mechanism |
|---|---|
| `decompress_rl_elist.kara` ★ | the list read two numbers at a time by `chunks(2)`, each pair's value pushed as many times as its count. O(total) |
| `decompress_rl_elist_repeat.kara` | each pair from `chunks(2)` turned into `repeat(value).take(count)`, and the runs joined by `flat_map` and collected. O(total) |
| `decompress_rl_elist_sized.kara` | the counts added up first, the answer made that long at once, and each run written into its place by index. O(total) |
| `decompress_rl_elist_runs.kara` | the pairs' places taken by `step_by(2)`, each run made whole by `Vec.filled(count, value)` and moved onto the end of the answer by `extend`. O(total) |
| `decompress_rl_elist_solution.kara` | a Rust solution as LeetCode's Rust users write it (`nums.chunks(2).flat_map(\|p\| vec![p[1]; p[0] as usize]).collect()`), carried to Kāra by `karac fix` |
| `decompress_rl_elist_extend.kara` | a second Rust solution as LeetCode's Rust users write it (the pairs' places by `(0..nums.len()).step_by(2)`, each run added by `res.extend(std::iter::repeat(nums[i + 1]).take(nums[i] as usize))`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, one pair, a
value repeated across neighbouring pairs, and the largest count and
value, 100 of 100, shown by its length and sum (`2,4,4,4 1,3,3 7,7,7
5,5,5,6 100:10000`); then 1000 random lists of 1 to 50 pairs, the
constraints' most, with counts up to 1, 5 or 100 and values up to 100
(`1000 random lists: 443063 numbers, checksum 370841033`).
`decompress_rl_elist.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`.

The Mend loop: the four Kāra arms checked clean as first written. The
first Rust arm takes one round of 18 fixes by `karac fix`'s count, from 9
errors: `struct Solution;` to `struct Solution {}`, `Vec<..>` to
`Vec[..]`, `|&x|` to `|x|`, `::` to `.`, then the `flat_map`, whose
closure must give an iterator in Kāra, not a `Vec`: `vec![p[1]; p[0] as
usize]` to `Vec.filled(p[0], p[1]).into_iter()`, and `chunks(2)`, a `Vec`
of slices in Kāra, to `chunks(2).into_iter()`. The second Rust arm takes
one round of 18 fixes from 11 errors: the same rewrites, `Vec::new` to
`Vec.new`, `std::iter::repeat` to `repeat`, which Kāra's prelude has, and
`take(nums[i] as usize)` to `take(nums[i])`. Both outputs match on the
first run. No gap was met.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the decompressed list's length is the counts added up, and
each of its places k takes the value of the first pair whose running
count passes k. 2000 lists of 1 to 10 pairs in four kinds, 500 each:
counts and values up to 3, so that neighbouring runs often share a value;
every count 1; counts and values up to 100; and one value throughout with
counts up to 5. Every list, cut, split and raise is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the pairs in the reverse order: the same answer back to front, since each run is one value |
| P3 | the list cut between two pairs: the two answers joined |
| P4 | one count of 2 or more split over two pairs of the same value: the same answer |
| P5 | every value raised: every number of the answer raised |
| P6 | the ★ arm's answer |

All 72,000 checks pass on every arm: `2000 lists: checksum 127241061,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum. The run takes
about 40 s under `karac __mir-run`.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under both
`karac __mir-llvm-run` and `karac __mir-run`. Every one is killed, fails
the same way under both backends and not by a crash, and no two fail the
same checks, so all twelve are kept.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each run one short | P1 2000, P4 1221, P6 10000 |
| M2 | ★: the count pushed in place of the value | P1 1974, P4 1221, P5 2000, P6 9870 |
| M3 | iterator: each run as long as its value | P1 1967, P4 1221, P5 2000, P6 1967 |
| M4 | iterator: each run one too long | P1 2000, P4 1221, P6 2000 |
| M5 | sized: every run written from the start | P1 1805, P2 1805, P3 1203, P4 479, P5 1805, P6 1805 |
| M6 | sized: the values added into the length too | P1 2000, P2 2000, P3 1203, P4 1221, P5 2000, P6 2000 |
| M7 | runs: count and value swapped | P1 1974, P4 1221, P5 2000, P6 1974 |
| M8 | runs: the first pair skipped | P1 2000, P2 1699, P3 1203, P4 365, P6 2000 |
| M9 | solution: the pairs taken last first | P1 1317, P3 901, P6 1317 |
| M10 | solution: each run cut to two | P1 1376, P4 968, P6 1376 |
| M11 | extend: the last pair dropped | P1 2000, P2 1699, P3 1203, P4 351, P6 2000 |
| M12 | extend: each run replacing the ones before | P1 1805, P2 1660, P3 1203, P4 351, P6 1805 |

P1 and P6 kill all twelve, P4 eleven, P3 six, and P2 and P5 five each.
Splitting a count over two pairs (P4) changes the answer of every edit
that gets a run's length wrong or treats one pair apart, and misses only
M9, whose runs come out last first but each still whole. Raising every
value (P5) catches the edits that mix counts with values (M2, M3, M7) and
the two that leave zeros in the answer, which a raise does not move (M5,
M6). Cutting the list between two pairs (P3) catches the edits that drop
the first or the last pair (M8, M11), that let one run overwrite another
(M5, M12), that pad with zeros (M6), and the runs taken last first (M9).
Turning the pairs round (P2) and the answer back again undoes M9 and every
edit that gets each run wrong on its own, and so sees only the five whose
answer depends on where a pair stands (M5, M6, M8, M11, M12).

## Benchmarks

The bench builds 100 lists of 50 pairs, the constraints' longest, with
counts and values up to 100, once from its own generator; then makes 2000
passes, each setting one count and one value of every list from the
checksum so far, so no answer carries over, decompressing it with the ★
arm and folding its length, two of its numbers at places chosen by the
checksum, and the pass into the checksum. Each answer is a fresh list that
grows as it is pushed to, by doubling in C. Every implementation prints
`2000 passes over 100 lists of 50 pairs: checksum 312431918`.

BENCHTAB
