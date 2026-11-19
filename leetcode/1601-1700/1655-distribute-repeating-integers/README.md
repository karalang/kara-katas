# 1655. Distribute Repeating Integers

You are given an array of `n` integers, `nums`, where there are at most
`50` unique values in the array. You are also given an array of `m`
customer order quantities, `quantity`, where `quantity[i]` is the amount
of integers the `i`th customer ordered. Determine if it is possible to
distribute `nums` such that:

- The `i`th customer gets **exactly** `quantity[i]` integers,
- The integers the `i`th customer gets are **all equal**, and
- Every customer is satisfied.

Return `true` *if it is possible to distribute* `nums` *according to the
above conditions*.

```
nums = [1,2,3,4], quantity = [2]    ->  false
nums = [1,2,3,3], quantity = [2]    ->  true
nums = [1,1,2,2], quantity = [2,2]  ->  true
```

**Constraints:** `n == nums.length`; `1 <= n <= 10^5`;
`1 <= nums[i] <= 1000`; `m == quantity.length`; `1 <= m <= 10`;
`1 <= quantity[i] <= 10^5`; there are at most `50` unique values in
`nums`.

## Approaches

| file | mechanism |
|---|---|
| `distribute.kara` ★ | only each value's count matters: `can[mask]` says whether the counts taken so far can serve the customers in `mask`, and each new count serves any submask of the customers not yet served whose wants it covers. O(k 3^m) for k values |
| `distribute_backtrack.kara` | backtracking: the customers from the largest want down, each given to a count that still covers it, undone on failure; of two equal counts only the first is tried. Exponential at worst |
| `distribute_memo.kara` | memoised search: whether the values from the v-th on can serve the customers in `mask`, each (v, mask) decided once. O(k 3^m) |
| `distribute_solution.kara` | LeetCode's Rust template: the ★ arm's subset DP over a `HashMap` of counts with `usize` masks. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's three examples, one
customer wanting all of one value (`true`), and three customers served
only by splitting a value (`true`); then how many are served and a
checksum for 3000 random problems of up to 12 numbers and 4 customers,
300 of up to 1000 numbers and 10 customers, and 30 of up to `10^5`
numbers and 10 customers. `distribute.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every way of giving each customer one of the values is tried,
and the problem can be served when, for some way, every value occurs at
least as often as its customers want together. It checks 3000 random
problems of 1 to 10 numbers from 1 to 4 values and 1 to 4 customers
wanting 1 to 4. Every problem is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the customers in reverse order give the same answer |
| P3 | the numbers relabelled and reversed give the same answer |
| P4 | one more customer never makes a problem servable |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 478235297, 60000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Two first tries were replaced. The ★
arm enumerating submasks of all the customers, not only those still
unserved, survived: it is equivalent, since any served customer it adds
only raises the want, and the unserved part of the same submask is
tried too. The template's `dp = next` changed to `dp = dp` stopped the
compiler with an internal move-check error rather than a diagnostic;
that is a compiler bug, B-2026-11-19-90, fixed in kara `bd214fffc0`: `v = v`
dropped the old value before moving it into the store.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a submask served ends at itself, not added to the mask | P1 299, P5 299 |
| M2 | ★: a count must exceed the want, not cover it | P1 463, P5 463 |
| M3 | ★: the submask of the last customer alone never tried | P1 716, P2 42, P4 281, P5 716 |
| M4 | backtrack: a count after an equal or smaller one skipped | P1 1, P5 1 |
| M5 | backtrack: a want not given back on failure | P1 1, P5 1 |
| M6 | memo: a run of equal numbers not restarted | P1 586, P3 120, P5 586 |
| M7 | memo: the next value never left to serve everyone | P1 133, P3 205, P4 31, P5 133 |
| M8 | memo: a mask's want summed over the customers not in it | P1 1744, P5 1744 |
| M9 | template: a mask's want only its lowest customer's | P1 984, P2 500, P5 984 |
| M10 | template: each count starts from nothing served | P1 515, P4 182, P5 515 |

M4 and M5 are killed by one problem each: equal counts after sorting are
rare on 4 values, and an undone want matters only after a failed branch.

## Benchmarks

The bench draws 200 random problems of `10^5` numbers from 50 values and
10 customers wanting 1 to 3000 each, LeetCode's largest shapes, all of
them first, then answers each by the ★ arm in all five languages. The C
mirror keeps the counts in an open-addressing table, as the others keep
them in a hash map. Every implementation prints `200 problems of 100000
numbers and 10 customers: 6 served, checksum 737395111`. The C build also
runs clean under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

TIMINGS

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. PARNOTE

## Verification

All four arms print the same output as `distribute.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `SHA`.

The ★ arm walks its counts in the `Map`'s order, which differs from run
to run; the answer does not depend on it.

## Writing it

The ★, backtracking and memoised arms checked clean as first written.

LeetCode's Rust template takes one `karac fix` of 17 edits: the `use
std::collections::HashMap;` line dropped, `struct Solution;` to
`struct Solution {}`, `Vec<i32>` to `Vec[i32]`, `HashMap<i32, i32>` and
`HashMap::new()` to `Map[i32, i32]` and `Map.new()`, `for &x in &nums`
to `for x in ref nums`, `vec![0i32; 1 << m]` and `vec![false; 1 << m]`
to `Vec.filled`, `for (_, &c)` to `for (_, c)`, and `!` to `not`. The
arm then checks and agrees with no hand edit.
