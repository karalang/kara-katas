# 70. Climbing Stairs

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Math · Dynamic Programming · Memoization &nbsp;·&nbsp; **Source:** [leetcode.com/problems/climbing-stairs](https://leetcode.com/problems/climbing-stairs/)

You climb a staircase of `n` steps, taking **1 or 2** steps at a time. How many distinct ways reach the top?

```
n = 2  →  2      (1+1),  (2)
n = 3  →  3      (1+1+1),  (1+2),  (2+1)
n = 5  →  8
```

**Constraints:** `1 ≤ n ≤ 45`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Two rolling counters** ★ — carry `ways(i-1)`, `ways(i-2)`, roll forward | O(n) time, O(1) space | [`climbing_stairs.kara`](climbing_stairs.kara) ✓ via `karac run` / `karac build` | [`climbing_stairs.py`](climbing_stairs.py) ✓ |
| **Full DP table** — materialise every `ways(i)` in a `Vec[i64]` | O(n) time, O(n) space | [`climbing_stairs_dp.kara`](climbing_stairs_dp.kara) ✓ | — |
| **Matrix exponentiation** — `Mⁿ` by repeated squaring, `(Mⁿ)[0][0] = ways(n)` | O(log n) time, O(1) space | [`climbing_stairs_matrix.kara`](climbing_stairs_matrix.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output across all eleven test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and all three approaches agree with each other and with the Python mirror.

## It's Fibonacci

The last move onto step `n` is either a single step (from `n-1`) or a double step (from `n-2`), and those two families of paths are disjoint — so

```
ways(n) = ways(n-1) + ways(n-2),   ways(1) = 1,  ways(2) = 2
```

which is the Fibonacci recurrence (`ways(n) = fib(n+1)`). It is the same "sum the two ways in" move the grid katas [#62](../62-unique-paths/)–[#63](../63-unique-paths-ii/) make, collapsed to a single dimension.

**Two rolling counters** ([`climbing_stairs.kara`](climbing_stairs.kara)) is the ★. The recurrence only ever looks back two terms, so no array is needed — hold `ways(i-1)` and `ways(i-2)` in a pair of scalars and roll them forward each step. O(1) space, the scalar-accumulator analogue of the grid DP's rolling row (kata [#53](../53-maximum-subarray/)'s Kadane is the same shape).

**Full DP table** ([`climbing_stairs_dp.kara`](climbing_stairs_dp.kara)) keeps every `ways(i)` in a `Vec[i64]` — the textbook 1-D DP, identical to kata [#62](../62-unique-paths/)'s rolling row before it is collapsed to a scalar pair. It carries no information the two scalars don't (each `dp[i]` is dead once `dp[i+2]` is computed), so it is here as the space optimisation shown as a diff.

**Matrix exponentiation** ([`climbing_stairs_matrix.kara`](climbing_stairs_matrix.kara)) is the outlier: it reaches the answer in **O(log n)**. One Fibonacci step is the linear map `M = [[1,1],[1,0]]`, so `(Mⁿ)[0][0] = fib(n+1) = ways(n)`, and `Mⁿ` is computed by exponentiation-by-squaring — square the base each step, fold it into the result on every set bit of `n`. It is the same fast-power as kata [#50](../50-powx-n/)'s `pow`, lifted from scalars to 2×2 matrices (carried as four scalars, no `Vec`). For `n ≤ 45` it is overkill, but it is a genuinely different algorithm that must still land on the same counts — the strongest cross-check of the three.

## Kāra features exercised

- **Scalar rolling recurrence** — the ★'s `next = a + b; a = b; b = next`, an O(1) two-variable state machine, plus the `n <= 2` base-case `return`; the same scalar-accumulator idiom as kata [#53](../53-maximum-subarray/).
- **`Vec[i64]` DP table** — `Vec.new()` + `push` to size the array, then `dp[j] = dp[j-1] + dp[j-2]` read-modify indexing, the 1-D DP shape shared with katas [#62](../62-unique-paths/)–[#64](../64-minimum-path-sum/).
- **2×2 matrix fast-power in scalars** — the matrix solver carries `[[a,b],[c,d]]` as four i64 locals and walks the exponent with `p % 2` (low bit) and `p / 2` (shift); exponentiation-by-squaring over matrices, the same halving loop as kata [#50](../50-powx-n/).
- **Shared `report`/`sums:` harness** — one `climb(n) = ways` per line plus the folded `sums:` checksum, the byte-for-byte diff anchor shared with the numeric katas [#50](../50-powx-n/) and [#69](../69-sqrtx/); all three solvers and the Python mirror print it identically.

**v1 note.** LeetCode caps `n` at 45, so `ways(45) = 1_836_311_903` fits i64 with enormous room (it fits i32). The matrix solver's largest intermediate is about `M⁶⁴`, whose entries are `fib(65) ≈ 1.7·10¹³`, and its biggest product stays far under i64::MAX — so Kāra's default overflow checks never trip on any of the three approaches. All arithmetic is i64 for corpus uniformity.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   climbing_stairs.kara
karac build climbing_stairs.kara && ./climbing_stairs

# The alternative approaches (identical output):
karac run climbing_stairs_dp.kara
karac run climbing_stairs_matrix.kara

# Python
python3 climbing_stairs.py

# Verify they all agree
diff <(karac run climbing_stairs.kara) <(python3 climbing_stairs.py)              && echo OK
diff <(karac run climbing_stairs.kara) <(karac run climbing_stairs_dp.kara)       && echo OK
diff <(karac run climbing_stairs.kara) <(karac run climbing_stairs_matrix.kara)   && echo OK
```
