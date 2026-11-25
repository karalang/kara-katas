# 1352. Product of the Last K Numbers

Design an algorithm that accepts a stream of integers and retrieves the
product of the last `k` integers of the stream.

Implement `ProductOfNumbers`:

- `ProductOfNumbers()` starts with an empty stream.
- `add(num)` appends `num` to the stream.
- `getProduct(k)` returns the product of the last `k` numbers in the
  current list. You can assume the current list always has at least `k`
  numbers.

The test cases are generated so that, at any time, the product of any
contiguous sequence of numbers fits into a single 32-bit integer without
overflowing.

```
add(3); add(0); add(2); add(5); add(4)
getProduct(2)  ->  20      (5 * 4)
getProduct(3)  ->  40      (2 * 5 * 4)
getProduct(4)  ->  0       (0 * 2 * 5 * 4)
add(8)
getProduct(2)  ->  32      (4 * 8)
```

**Constraints:** `0 <= num <= 100`, `1 <= k <= 4 * 10^4`, at most `4 *
10^4` calls to `add` and `getProduct`.

Each arm is a `struct ProductOfNumbers` with `fn new() ->
ProductOfNumbers`, `fn add(mut ref self, num: i32)` and `fn
get_product(self, k: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `product_of_numbers.kara` ★ | the running products of the numbers since the last zero, after a leading 1; a zero ends every product that reaches back past it, so it starts the list over. The last k numbers' product is the last running product divided by the one k places before it, or 0 when the last k reach back to a zero. O(1) for each call |
| `product_of_numbers_walk.kara` | every number kept; a product walks back over the last k, stopping early at a zero. O(1) to add, O(k) for a product |
| `product_of_numbers_blocks.kara` | the numbers in blocks of 200, each full block's product kept; a product takes the loose numbers at the end, whole blocks while k allows, and the loose numbers at the start. O(1) to add, O(k / 200 + 200) for a product |
| `product_of_numbers_tree.kara` | a segment tree over the numbers, each node the product of its range, doubling its leaves when they run out; a product is the tree's answer for the last k places. O(log N) for each call, amortized |
| `product_of_numbers_solution.kara` | a Rust solution as LeetCode's Rust users write it (the running products since the last zero in a `Vec<i32>` started over as `vec![1]`, the last read as `*self.prefix.last().unwrap()`, and `let k = k as usize;`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's example (`20 40 0 32`);
one number, k reaching back to the first number, a product past a zero
and the one after it, and a product just below 2^31, 65536 * 32767 * 1
(`7 42 0 9 2147418112`); 4 * 10^4 calls, the constraints' most, 39,000
numbers, mostly 1, then 1000 products of the last 1 to 4 * 10^4 (`4 *
10^4 calls: checksum 25082075`); and 500 random sessions of 1 to 60
calls, adds and products mixed (`500 random sessions: products total
101673060492, checksum 147483824`). Every number is drawn so that no
product since the last zero reaches 2^31, as the statement promises.
`product_of_numbers.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`.

The Mend loop: the walk and blocks arms check clean. The ★ arm was
written `last * num as i64`, and `karac check` warns that the cast is
unnecessary, an `i32` widening to `i64` implicitly (W0310,
`lossless_cast`), as on one line of the harness; `karac fix` drops both.
The tree arm was written with Rust's `let (mut l, mut r) = ..`; `karac
check` says that `mut` goes before the whole pattern (E0001), and `karac
fix` writes `let mut (l, r)`. The Rust solution takes one round of 7
fixes by `karac fix`'s count: `Vec<i32>` to `Vec[i32]`, each `vec![1]`
to `[1]`, `&mut self` and `&self` to `mut ref self` and `self`, and `k as
usize` to `k as i64`; `*self.prefix.last().unwrap()` stands. Every arm
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the numbers kept in a list, and each product taken over the
last k of them, first to last. 2000 sessions in four kinds, 500 each,
every call after the first an add two times in three and otherwise a
product of the last 1 to all of the numbers: 1 to 30 calls, a zero one
number in 4 and a number above 1 one in 2; a zero one in 12 and above 1
one in 3; no zero; and 300 to 700 calls, a zero one in 400 and above 1
one in 40, long enough to fill blocks of 200. Every session is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | 7, 3, 5 and a zero added before the session: no product reaches back to them, so the same answers |
| P3 | a 1 added after every number and each k doubled: the same answers |
| P4 | every number above 1 made 1: each product 0 where it was 0 and 1 elsewhere |
| P5 | every product asked as the product of the last 1: the last number added |
| P6 | the ★ arm's answers |

All 60,000 checks pass on every arm: `2000 sessions: checksum
638837539, 60000 checks over 5 arms: 0 failures`, under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`. Python, answering 0
when the last zero lies within the last k and multiplying otherwise,
gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: k reaching the first number since a zero answered 0 | P1 1434, P3 304, P5 921, P6 5736 |
| M2 | ★: the product one number short | P1 1364, P5 1439, P6 5456 |
| M3 | walk: one number too many multiplied | P1 1284, P2 1281, P3 1284, P5 1442, P6 1284 |
| M4 | walk: the first k numbers multiplied | P1 1589, P2 1839, P5 1615, P6 1589 |
| M5 | blocks: a block's product one number short | P1 3, P2 7, P3 18, P6 3 |
| M6 | blocks: the numbers after the last full block left out | P1 1751, P2 384, P3 473, P5 1561, P6 1751 |
| M7 | tree: a node's product taken from its left child alone | P1 1187, P2 1003, P6 1187 |
| M8 | tree: the last number left out | P1 1473, P3 1473, P5 1562, P6 1473 |
| M9 | solution: a zero added as a fresh 1, the list kept | P1 733, P4 565, P5 219, P6 733 |
| M10 | solution: each number put on the leading 1 | P1 1463, P3 1485, P4 1071, P5 1309, P6 1463 |

P1 and P6 kill all ten, P5 eight, P3 six, P2 five and P4 two. The
product of the last 1 (P5) is the last number added, and catches every
edit that is wrong at k = 1; it misses only a block's product (M5),
which a single number never reaches, and a node's left child (M7),
since one number is one leaf. Numbers and a zero before the session
(P2) move every position by four, and catch the edits that count
places from the start of the stream (M4, M5, M6, M7) or reach one
number too far, into that zero (M3). A 1 after every number (P3) doubles
every k and every count since a zero, and catches the edits whose
error depends on those counts (M1, M3, M5, M6, M8, M10). Making every
number 0 or 1 (P4) leaves only the zeros to get right, which only the
solution's edits get wrong (M9, M10). The weakest edit, a block's
product one number short (M5), shows only where a product spans a full
block of 200, in 3 of the 2000 sessions, all of the long kind.

## Benchmarks

The bench makes 10^7 rounds, each adding a number, 0 one time in 1000,
otherwise 1, or 2 to 100 one time in 20, taken back to 1 when the
product since the last zero would reach 2^31, and asking the product of
the last 1 to 50,000 numbers, k drawn from the checksum so far, so no
answer carries over; answered by the ★ arm's running products, and
folding each answer plus the round into the checksum. Every
implementation prints `10000000 rounds: checksum 114623747`.

BENCHTAB
