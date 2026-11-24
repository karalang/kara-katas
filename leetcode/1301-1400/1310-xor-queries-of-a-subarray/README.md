# 1310. XOR Queries of a Subarray

You are given an array `arr` of positive integers. You are also given the
array `queries` where `queries[i] = [left_i, right_i]`.

For each query `i` compute the **XOR** of elements from `left_i` to
`right_i` (that is, `arr[left_i] XOR arr[left_i + 1] XOR ... XOR
arr[right_i]`).

Return an array `answer` where `answer[i]` is the answer to the `i`th
query.

```
arr = [1,3,4,8], queries = [[0,1],[1,2],[0,3],[3,3]]   ->  [2,7,14,8]
arr = [4,8,2,10], queries = [[2,3],[1,3],[0,0],[0,3]]  ->  [8,0,4,4]
```

**Constraints:** `1 <= arr.length, queries.length <= 3 * 10^4`, `1 <=
arr[i] <= 10^9`, `0 <= left_i <= right_i < arr.length`.

The arms are `fn xor_queries(arr: Vec[i64], queries: Vec[Vec[i64]]) ->
Vec[i64]`.

## Approaches

| file | mechanism |
|---|---|
| `xor_queries.kara` ★ | the XOR of every prefix of the array, so that a range's XOR is the XOR of the prefix ending at its right end with the prefix ending just before its left end, the numbers before it cancelling. O(n + q) |
| `xor_queries_naive.kara` | the statement as written: each range's numbers XORed one by one. O(n q) |
| `xor_queries_fenwick.kara` | a binary indexed tree whose node i holds the XOR of the `i & -i` numbers ending at i, built by XORing each number into the nodes above it; a prefix's XOR read off along `i -= i & -i`, and a range's from two prefixes. O((n + q) log n) |
| `xor_queries_blocks.kara` | the array cut into blocks of about the square root of its length, each block's XOR kept; a range takes the whole blocks inside it from that table and the numbers at its two ragged ends one by one. O(n + q sqrt n) |
| `xor_queries_solution.kara` | a Rust solution as LeetCode's Rust users write it (the prefix XORs built by `arr.iter().scan(0, \|acc, &x\| { *acc ^= x; Some(*acc) })` after a leading 0 through `std::iter::once(0).chain(..)`, the answers by `queries.iter().map(\|q\| p[q[0] as usize] ^ p[q[1] as usize + 1])`), carried to Kāra by `karac fix` |
| `xor_queries_inplace.kara` | a second Rust solution as LeetCode's Rust users write it (the array taken as `mut arr` and turned into its own prefix XORs in place, `arr[i] ^= arr[i - 1]`, each answer `arr[r]` alone when the range starts at 0 and `arr[r] ^ arr[l - 1]` otherwise, pushed onto a `Vec::with_capacity(queries.len())`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, one number
asked alone, and the largest numbers, `10^9`, over a range of two that
cancels (`2,7,14,8 8,0,4,4 7 0,999999999,1023`); then 1000 random arrays
of 1 to 300 numbers from 0 up to 1, 1000 or `10^9`, each with 1 to 300
random ranges (`1000 random arrays: 148144 answers, checksum
530880187`). `xor_queries.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`.

The Mend loop: the four Kāra arms checked clean as first written. The
first Rust arm takes one round of 30 fixes by `karac fix`'s count, from
16 errors: `struct Solution;` to `struct Solution {}`, `Vec<..>` to
`Vec[..]`, `std::iter::once` to `once`, which Kāra's prelude has, `|&x|`
to `|x|`, `::` to `.`, and Rust's `scan`, whose closure updates the state
through a `&mut`, to Kāra's, whose closure takes the state by value and
returns the next state beside the item: `scan(0i32, |acc, x| { let acc =
acc ^ x; Some((acc, acc)) })`, the start written `0i32` beside the `i32`
items. `karac fix` writes that closure on one line, and it is laid out
here as `karac fmt` lays it out. The second Rust arm takes one round of 27
fixes from 15 errors: the same rewrites, the parameter `mut arr: Vec<i32>`
to `arr: own Vec[i32]` with `let mut arr = arr;` as the body's first line,
and `Vec::with_capacity` to `Vec.with_capacity`. Both outputs match on the
first run. No gap was met.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a bit of each answer set when an odd number of the range's
numbers have that bit set, over 31 bits. 2000 arrays of 1 to 12 numbers,
each with 1 to 6 ranges, in four kinds, 500 each: numbers 0 and 1; up to
7; up to `10^9`; and one number throughout, so that a range of even length
cancels to 0. Every array, range and mask is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the array reversed and every range mirrored with it: the same answers |
| P3 | a range joined to a range just after it: the two answers XORed |
| P4 | every number XORed with a mask: each answer XORed with it where its range is odd in length |
| P5 | the ranges asked in the reverse order: the answers reversed |
| P6 | the ★ arm's answer |

All 69,744 checks pass on every arm: `2000 arrays: checksum 303349115,
69744 checks over 6 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Thirteen edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. One is left out: the Rust arm
leaving out a range's last number fails exactly the same checks as the
every-number arm doing so. The twelve kept, two to each arm, are each
killed, fail the same way under both backends and not by a crash, and no
two fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each prefix only the number at its end | P1 1616, P2 1609, P4 1542, P6 8080 |
| M2 | ★: a range's first number left out | P1 1844, P2 1194, P3 1477, P4 2000, P6 9220 |
| M3 | every number: a range's last number left out | P1 1845, P2 1194, P3 1489, P4 2000, P6 1845 |
| M4 | every number: the numbers added, not XORed | P1 1573, P3 1371, P4 1738, P6 1573 |
| M5 | Fenwick: the prefix walked down one node at a time | P1 1585, P2 1416, P4 1608, P6 1585 |
| M6 | Fenwick: the last node never written | P1 980, P2 1083, P4 684, P6 980 |
| M7 | blocks: a block taken from any place, not only its start | P1 711, P2 870, P3 617, P6 711 |
| M8 | blocks: each block holding only its last number | P1 1065, P2 1042, P3 886, P4 738, P6 1065 |
| M9 | solution: the two prefixes ORed, not XORed | P1 1105, P2 1150, P3 1266, P4 1176, P6 1105 |
| M10 | solution: the scan started from 1 | P1 1342, P2 1430, P6 1342 |
| M11 | in place: the second number never folded in | P1 1246, P2 1455, P4 1464, P6 1246 |
| M12 | in place: a range from the start losing its first number | P1 1136, P2 1323, P4 1342, P6 1136 |

P1 and P6 kill all twelve, P2 eleven, P4 ten and P3 six; P5 kills none.
Every arm answers each range on its own, so the order the ranges are
asked in (P5) reaches no edit. Reversing the array (P2) misses only M4,
whose sums, like XOR, do not care about order. A mask (P4) misses the two
edits whose error keeps the count of numbers in an answer: M7 takes a
whole block of the same length in place of the numbers it skips, and M10
flips the low bit of every answer that starts at 0, mask or no mask. A
joined range (P3) passes any answer read from one table at the range's
left end and just past its right end, however wrong the table (M1, M5,
M6, M10, M11, M12), since the shared boundary cancels; it catches an end
read at the wrong place (M2, M3), answers not made by XOR (M4, M9), and
the block arm's wrong mix of blocks and single numbers (M7, M8).

## Benchmarks

The bench builds 10 arrays of `3 * 10^4` numbers up to `10^9`, each with
`3 * 10^4` ranges, the constraints' most, once from its own generator;
then makes 100 passes, each setting one number and one range of every
array from the checksum so far, so no answer carries over, answering every
range with the ★ arm and folding two of the answers, at places chosen by
the checksum, plus the pass into the checksum. Each call builds a fresh
prefix table and answer array in every language, a `malloc` in C. Every
implementation prints `100 passes over 10 arrays of 3 * 10^4: checksum
402243117`.

BENCHTAB
