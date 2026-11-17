# 2235. Add Two Integers

Given two integers `num1` and `num2`, return *the **sum** of the two
integers*.

```
num1 = 12,  num2 = 5  ->  17
num1 = -10, num2 = 4  ->  -6
```

**Constraints:** `-100 <= num1, num2 <= 100`.

The two added with `+`. O(1).

## Approaches

| file | mechanism |
|---|---|
| `add.kara` ★ | `num1 + num2` |
| `add_bits.kara` | no `+`: the bits that differ by `^`, the carries by `&` shifted up one with `<<`, added again until no carry is left |
| `add_digits.kara` | by hand on decimal digits, as on paper: the same signs add their magnitudes digit by digit with a carry, different signs take the smaller magnitude from the larger with a borrow, the result taking the larger's sign |
| `add_struct.kara` | a `struct Pair` of the two numbers with `total` (`ref self`) |
| `add_iter.kara` | `[num1, num2].iter().sum()` |
| `add_solution.kara` | LeetCode's Rust template: `pub fn sum(num1: i32, num2: i32) -> i32` in an `impl Solution`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

For a negative number the bits arm's carry climbs through every bit and
out of the top: `-1 + 1` carries 2, 4, 8 and on until the carry is
`2^63`, which is `i64.MIN`, and the next round clears it. That leans on
`<<` dropping the bits shifted past the sign, which is what Kāra
specifies: only a shift amount that is negative or at least the bit
width traps (design.md, *Division, remainder and shifts*).

Every arm prints the same 8 lines: LeetCode's two examples and five more
(both ends, both zero, a sum of zero, and `-1 + 1`, whose carry goes
through every bit), each with its sum; then, over every pair from -100
to 100, a checksum of the sums and how many are negative and how many
zero. `add.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one round of 3 edits:
`struct Solution;` to `struct Solution {}`, the adapter's
`Solution::sum` to `Solution.sum`, and the adapter's `as i64` on the
`i32` result dropped as a lossless cast.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a walk along the number line from `num1`, `num2` unit steps
up, or down for a negative `num2`; no `+` of the two. It checks every
pair from -100 to 100, 40401 of them, all built before any arm answers.

| | property |
|---|---|
| P1 | the answer is where the walk ends |
| P2 | the two numbers swapped: the same answer |
| P3 | `num2` taken back off the answer by the same arm: `num1` |
| P4 | `num1` one higher: the answer one higher |
| P5 | both numbers negated: the answer negated |
| P6 | each arm agrees with at least three of the other five |

The differential prints `40401 cases: checksum 504380948, 1454436
checks over 6 arms: 0 failures` under every lane in Verification; the
checksum of the literal answers was checked against a Python reading
that walks the same unit steps. On a failure it prints the first ten
and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under `karac __mir-llvm-run`, and the kept
ones under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: the sum's magnitude | P1 20100, P3 25150, P4 20100, P5 40200, P6 20100 |
| M5 | ★: `num2`'s magnitude added | P1 20100, P2 30100, P3 40200, P5 40200, P6 20100 |
| M6 | ★: `\|` for `+` | P1 36022, P3 39448, P4 26812, P5 39800, P6 36022 |
| M7 | bits: `\|` for `^` | P1 36022, P3 39448, P4 26812, P5 40000, P6 36022 |
| M8 | bits: the carry shifted up two | P1 36022, P3 40200, P4 26812, P5 36652, P6 36022 |
| M11 | bits: the carry dropped | P1 36022, P3 40200, P4 26812, P5 39800, P6 36022 |
| M12 | digits: no carry | P1 13950, P3 18198, P4 3646, P6 13950 |
| M14 | digits: a difference's sign taken from the smaller | P1 10000, P2 20000, P3 30000, P4 10100, P5 200, P6 10000 |
| M15 | digits: the digits read back in the wrong order | P1 36220, P3 37268, P4 40149, P6 36220 |
| M18 | struct: the first counted twice | P1 40200, P2 40200, P3 40200, P4 40401, P6 40200 |
| M20 | struct: `num2` for both | P1 40200, P2 40200, P3 40300, P4 40401, P6 40200 |
| M21 | struct: the larger for both | P1 40200, P3 40400, P4 40401, P5 40200, P6 40200 |
| M23 | iter: the larger, `max` for `sum` | P1 40200, P3 30200, P4 20100, P5 40200, P6 40200 |
| M25 | iter: the magnitudes summed | P1 30200, P3 40300, P4 20100, P5 40400, P6 30200 |
| M27 | iter: a 1 in the array too | P1 40401, P3 40401, P5 40401, P6 40401 |
| M28 | solution: a difference | P1 40200, P2 40200, P6 40200 |
| M29 | solution: a product | P1 40399, P3 40200, P4 40200, P5 40000, P6 40399 |

P1 and P6 kill all seventeen, P3 sixteen, P4 fourteen, P5 twelve and
P2 five. Over every pair each property sees almost every case, so the
counts tell apart even edits that fail alike: the ★ arm's `|` and the
bits arm's `|` for `^` fail P1 to P4 on exactly the same counts and
part only in P5, the negated pairs. P2, the swap, catches only
the edits that treat the two numbers differently (M5, M14, M18, M20,
M28); the only kept edit P3 misses is the difference (M28), which taken
back with `-num2` returns `num1`.

Of the thirty-one, fourteen were not kept. One survives and is
equivalent within the constraints: the digits arm's borrow never
cleared (M13), since a stale borrow reaches a later digit only when a
digit borrows and the next one does not, which needs three digits
below 100 in the larger magnitude, and none has them. One crashes: the
bits arm stopping at a negative carry (M9), which returns a number near
`i64.MIN`, so that the differential's own `value + 1` overflows. None
differs between the backends. Ten fail as a kept one does: the ★ arm's
difference and the struct arm's second taken away (M1, M19) as the
template's (M28); the ★ arm's `num1` doubled and the iter arm's first
skipped (M2, M24) as the struct arm's first counted twice (M18); the ★
and struct arms' one too many (M3, M22) as the iter arm's 1 in the array
(M27); the bits arm's `num2.abs()` (M10) as the ★ arm's (M5); the iter
arm's product (M26) as the template's (M29); and the template's `num2`
handed in twice and smaller doubled (M30, M31) as the struct arm's
`num2` for both and larger for both (M20, M21). Two fail their own way
and are left out for the count of three: the digits arm's last carry
lost and a negative sum left positive (M16, M17).

## Verification

Every arm prints the same output as `add.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.1 s to 0.4 s, and the
differential 3.3 s.

## Benchmarks

The bench draws 10^7 pairs from -100 to 100 and folds each sum into a
checksum, the ★ arm in all five languages. The addition is one
instruction, so the numbers measure the drawing and the modular fold
around it, not the addition. Every implementation prints `10^7 pairs:
checksum 225376377`.

BENCHTAB
