# 2197. Replace Non-Coprime Numbers in Array

You are given an array of integers `nums`. Perform the following steps:

1. Find **any** two **adjacent** numbers in `nums` that are
   **non-coprime**.
2. If no such numbers are found, **stop** the process.
3. Otherwise, delete the two numbers and **replace** them with their
   **LCM (Least Common Multiple)**.
4. **Repeat** this process as long as you keep finding two adjacent
   non-coprime numbers.

Return *the **final** modified array.* It can be shown that replacing
adjacent non-coprime numbers in **any** arbitrary order will lead to the
same result.

The test cases are generated such that the values in the final array are
**less than or equal** to `10^8`.

Two values `x` and `y` are **non-coprime** if `GCD(x, y) > 1` where
`GCD(x, y)` is the **Greatest Common Divisor** of `x` and `y`.

```
nums = [6,4,3,2,7,6,2]  ->  [12,7,6]
nums = [2,2,1,1,3,3,3]  ->  [2,1,1,3]
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^5`;
the test cases are generated such that the values in the final array
are less than or equal to `10^8`.

A stack of the numbers settled so far: each number, before it is
pushed, merges with the top while the two share a factor, the pair
replaced by its LCM, so the stack never holds two adjacent non-coprime
numbers. O(n log m).

## Approaches

| file | mechanism |
|---|---|
| `replace.kara` ★ | a `Vec` as the stack; each number merged with the top by `while let Some(top) = stack.last()` while their `gcd` is above 1, the LCM written `top / g * cur` |
| `replace_linked.kara` | a doubly linked list over the array's own slots, `prev` and `next` indices: walking forward, each slot merges with the live slot before it, which is unlinked, and the LCM written into the later one; the answer read along `next` from the first live slot |
| `replace_fold.kara` | one `fold` with the stack as the accumulator, each number merged in by a recursive `settle` (`mut ref` the stack) that `match`es `stack.last().cloned()` with a guard, pops and recurses on the LCM; `gcd` recursive too |
| `replace_struct.kara` | a `struct Settled` of the merged run, with `push` (`mut ref self`) merging from the end and `into_vec` (`own self`) handing the run back, each pair's LCM built by a `struct Pair` with `gcd` and `lcm` methods |
| `replace_inplace.kara` | in place: the array taken by `own`, its first `w` slots the settled run, each next number merged backward into the run's last slot, then written at `w`; the array `truncate`d to the run |
| `replace_solution.kara` | LeetCode's Rust template: `Vec<i32>` in and out, a recursive `gcd` nested in the method, the stack a `Vec<i64>` walked by `while let Some(&top) = st.last()`, the answer narrowed back by `into_iter().map(..).collect()`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one number, all coprime, a merge that runs back to the start, and one
that takes them all), each with its answer; then the count kept and a
checksum for 3000 random arrays of 1 to 40 numbers; then the
constraints' longest, 10^5 numbers from the first pool and from the
third. The numbers are drawn in turn from three pools: the divisors up
to 10^5 of 2^4 3^3 5^2 7 11 13 (10810800), those of 2^6 3^4 17 19
(1674432), and 1 with six primes near 10^5. Every LCM of a pool's
numbers divides its product, or is one of its primes, so each answer
keeps the constraints' bound of 10^8. `replace.py` mirrors the ★ arm and
its output is byte-identical.

`karac fix` carries the template in one round of 18 edits: Rust's
spellings (`Vec<..>` to brackets, `Vec::new()` to `Vec.new()`, `for &x
in nums.iter()` to `for x in ..`, `|&x|` to `|x|`, `struct Solution;` to
`struct Solution {}`, `Solution::` to `.`), the `gcd` nested in the
method moved out to the top level, and `while let Some(&top) =
st.last()` to `while let Some(top) = st.last().cloned()`.

The fold arm was first written `match stack.last() { Some(top) if ..
=> { stack.pop(); settle(mut stack, top / g * x); } .. }`, which `karac
check` refuses as Rust does: `top` still borrows the stack when it is
popped. The message names `.cloned()` among the ways out, though with
no fix; the template's `Some(&top)` gets one.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: find the first two adjacent numbers that share a factor,
replace them by their LCM, and start again from the front until no such
pair is left; no stack. It checks 300 random arrays of 1 to 40 numbers
from the three pools in turn; then 30 of one number repeated; then 30
runs of consecutive numbers up to 10^5, no two adjacent ones sharing a
factor. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | no two adjacent numbers of it share a factor, and it is the array cut into runs, in order, each replaced by its LCM |
| P3 | the array reversed: the answer reversed |
| P4 | the answer replaced again: itself |
| P5 | the array followed by itself reversed: the same as the two answers so joined, replaced again |
| P6 | each arm agrees with at least three of the other five |

P2 is checked without the array's whole LCM, which overflows for a run
of consecutive numbers: a 1 shares a factor with nothing, so it is a run
of its own, and any other number divides the LCM of its run and of no
other, since adjacent answers are coprime. P3 and P5 hold since any
order of replacing gives the same answer, as the statement says.

The differential prints `360 cases: checksum 967919863, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
cases. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Forty edits to the differential, six to the ★ arm, nine to the struct
arm, seven each to the linked and in-place arms, six to the fold arm and
five to the Rust-template arm, each run under `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: the top kept under its merge | P1 307, P2 307, P3 197, P6 307 |
| M4 | ★: the GCD for the LCM | P1 197, P2 197, P3 120, P6 197 |
| M31 | ★: the stack's last number dropped when it is 1 | P1 99, P2 99, P3 26, P6 99 |
| M6 | linked: the head never moved | P1 231, P2 231, P3 218, P5 6, P6 231 |
| M7 | linked: the left link not mended | P1 13, P2 13, P3 11, P5 5, P6 13 |
| M33 | linked: the answer from the second live slot | P1 144, P2 144, P3 143, P4 139, P5 144, P6 144 |
| M11 | fold: the merged number pushed unsettled | P1 16, P2 16, P3 21, P4 16, P5 16, P6 16 |
| M13 | fold: a GCD of 2 taken as coprime | P1 25, P2 25, P6 25 |
| M15 | fold: the first number dropped | P1 152, P2 152, P3 166, P4 352, P5 172, P6 152 |
| M19 | struct: the merged number left out | P1 171, P2 171, P3 156, P5 102, P6 171 |
| M35 | struct: the run's first number never merged | P1 231, P2 231, P3 208, P6 231 |
| M39 | struct: the merge on a GCD of 3 skipped | P1 21, P2 21, P6 21 |
| M22 | inplace: the array not truncated | P1 307, P2 307, P3 280, P4 33, P5 277, P6 307 |
| M25 | inplace: a run of one cut off | P1 216, P2 216, P6 216 |
| M38 | inplace: the first number written over | P1 15, P2 15, P3 25, P4 30, P5 28, P6 15 |
| M26 | solution: the adapter's numbers reversed | P1 138, P2 138, P4 138, P5 138, P6 138 |
| M27 | solution: the merge stopping at an even GCD | P1 264, P2 264, P6 264 |
[('P1', 17), ('P2', 17), ('P3', 12), ('P4', 6), ('P5', 9), ('P6', 17)]

Six survive, and each is equivalent: the GCD's remainder taken the
other way round or from the first remainder (M14, M20) and its base case
put on the other side (M30) still compute the GCD; the in-place arm
stopping its merge at a 1 (M21) stops where it would anyway, since 1
shares a factor with nothing; the template's LCM narrowed to `i32` (M28)
never overflows, because every answer is at most 10^8; and a merged
slot's back link pointed at the slot just before it (M32) walks through
merged slots whose numbers all divide the new one, to the same live
slot. Seven crash under both backends: the product for the LCM (M2), the
struct arm's LCM without the GCD (M16), its pair taken from the second
from last (M17), and the in-place arm writing a slot on (M23) or merging
with the read slot (M24) overflow; a GCD one step short (M5) divides by
zero; and the fold arm leaving the top in place (M12) recurses until the
stack runs out. Three never end: the merged slot's back link left as it
was (M8), and the struct and template arms not popping the top (M18,
M29). Seven fail as a kept one does or are left out to keep three to an
arm: a merge only once in the ★, linked and struct arms (M1, M9, M40) as
M11, the linked walk from the first slot (M10) as M6, the numbers folded
from the back (M34) as M26, and the run handed back without its first
number (M36) as M33; the in-place array truncated one long (M37) is
killed and left out. M39 and M40 were added to the struct arm when its
first seven gave only two kills distinct from the other arms'.

## Verification

Every arm prints the same output as `replace.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.9 s to 1.8 s and the
differential 1.4 s.

## Benchmarks

The bench builds 12 arrays of 10^5 numbers once, four from each pool,
then replaces each 100 times over with the ★ arm in all five languages;
each answer is checked by its length and its middle number. Every
implementation prints `100 passes over 12 arrays: checksum 831065660`.

BENCHTAB
