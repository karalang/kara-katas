# 342. Power of Four

Given a 32-bit integer `n`, return `true` if `n == 4^x` for some integer
`x >= 0`. Follow-up: can you do it without loops or recursion?

```
n = 16  ->  true     (4^2)
n = 5   ->  false
n = 1   ->  true     (4^0)
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `power_of_four.kara` ★ | `n > 0`, one bit set (`n & (n - 1) == 0`), and that bit inside `0x55555555` | `O(1)` time and space |
| `power_of_four_divide.kara` | divide out every factor of 4, then check the rest is 1 | `O(log n)` time, `O(1)` space |
| `power_of_four_mod3.kara` | a positive power of two with `n % 3 == 1` | `O(1)` time and space |
| `power_of_four_bits.kara` | `count_ones() == 1` and an even `trailing_zeros()` | `O(1)` time and space |
| `power_of_four_unsigned.kara` | as `u32`: `is_power_of_two()` and an odd `leading_zeros()`, with no sign test | `O(1)` time and space |
| `differential.kara` | the five arms on 220,289 inputs, seven properties | — |
| `bench/power_of_four.kara` | 100 re-classifications of 500,000 values by the ★ arm | — |

Every arm prints the same 19 lines: the three examples, eight more single
values, the largest 32-bit power `4^15 = 2^30` with its two neighbours, the
largest power of two that is not one (`2^29`), both ends of the 32-bit range,
a pass over every power of two `2^0 .. 2^30`, and a sweep over
`[-1000, 1000000]` (10 powers, sum 349525). The five arms' output is
byte-identical, and `power_of_four.py` mirrors both the ★ arm and, with
`--divide`, the divide arm.

## Why each test works

`4^x = 2^(2x)`, so a power of four is a power of two whose one set bit sits
at an even position. Each bit arm finds the power of two the same way and
then tells the even positions from the odd ones differently:

- **The mask.** `0x55555555` is `0101...0101`, the even positions only.
- **Mod 3.** `4 % 3 == 1`, so `4^x % 3 == 1`. The odd powers `2 * 4^x`
  leave 2. No power of two leaves 0, since 3 is not a factor of one.
- **Trailing zeros.** The bit's position is the number of zeros below it.
- **Leading zeros, unsigned.** In 32 bits the position is `31 - lz`, so an
  even position is an odd `lz`.

The ★ arm puts `n > 0` first for two reasons. It rejects 0 and every
negative value, including `-2^31`, whose only set bit is the sign bit. And
`and` stops there, so `n - 1` is never computed at `-2^31`, where it would
overflow, which Kāra traps. Mutant M3 below deletes the test and panics with
`integer overflow` on exactly that input.

The unsigned arm needs no sign test at all. Read as a `u32`, a negative
`n` has its top bit set, so it is either not a power of two or exactly
`2^31`, which has no leading zeros, an even count, so it is rejected. And
0 fails `is_power_of_two` on its own. Kāra offers `is_power_of_two` on
unsigned types only, which is what pushes this arm into the cast.

The divide arm is the one to write when the base is not a power of two. It
must reject `n <= 0` up front: `0 % 4 == 0`, so on 0 it would loop forever
(M4).

## Differential

`differential.kara` runs all five arms on every `n` in `[-100, 200000]`,
every `2^k + d` for `k` in `0..30` and `d` in `-2..2`, every `-2^31 + 2^k`,
both 32-bit extremes, and 20,000 pseudo-random 32-bit values.

| | property |
|---|---|
| P1 | all five arms agree |
| P2 | nothing at or below 0 is accepted |
| P3 | for `0 < n < 2^29`, `n` is accepted exactly when `4n` is |
| P4 | an accepted `n` leaves 1 mod 3, and is 1 or divisible by 4 |
| P5 | the exhaustive range holds exactly the powers a multiplication loop finds in it, by count and by sum |
| P6 | `2^k` is accepted exactly when `k` is even, and `2^k + d` with `d != 0` and `2^k > 4` never is |
| P7 | for `n > 0`, `n` is accepted exactly when it is the square of a power of two |

P7 is the only property that does not lean on bits or division: it takes a
float square root as a guess, checks the guess and its neighbours exactly,
and asks whether the root is a power of two.

`checked 220289, accepted 27, failures 0`, and all properties hold, on every
surface.

## Mutation testing

Twelve edits to the copies inside `differential.kara`, each run under
`--interp`.

| # | mutation | outcome | how |
|---|---|---|---|
| M1 | mask arm: mask `0x55555554`, dropping bit 0 | **killed** | P1 at `n = 1`, 12 failures |
| M2 | mask arm: `n >= 0` instead of `n > 0` | silent (equivalent) | — |
| M3 | mask arm: no `n > 0` test | **killed** | panics, `integer overflow` at `-2^31` |
| M4 | divide arm: `n < 0` instead of `n <= 0` | **killed** | hangs at `n = 0` |
| M5 | mod-3 arm: `n % 3 != 2` instead of `== 1` | silent (equivalent) | — |
| M6 | bits arm: odd `trailing_zeros` instead of even | **killed** | P1 at `n = 1`, 53 failures |
| M7 | unsigned arm: even `leading_zeros` instead of odd | **killed** | P1 at `n = 1`, 54 failures |
| M8 | unsigned arm: `count_ones() == 1` instead of `is_power_of_two()` | silent (equivalent) | — |
| M9 | mod-3 arm: no power-of-two test | **killed** | P1 at `n = 7`, 66,687 failures |
| M10 | divide arm: `m <= 1` instead of `m == 1` | silent (equivalent) | — |
| M11 | mask arm: mask `0x15555555`, dropping bit 30 | **killed** | P1, P6, P7 at `4^15` only |
| M12 | unsigned arm: clear the sign bit before the cast | **killed** | P1 at `-2^31 + 4^k`, 16 failures |

The four silent mutants are equivalent. M2 adds only `n = 0`, which the
mask rejects anyway. M5: no power of two leaves 0 mod 3, so `!= 2` and
`== 1` agree on every input that reaches it. M8: a `u32` with one bit set
is exactly a power of two. M10: dividing a positive `n` by 4 never reaches
0, so `m <= 1` means `m == 1`.

M12 survived the first version of the differential. Clearing the sign bit
turns `-2^31 + 4^k` into `4^k`, and none of the inputs had that shape: the
exhaustive range stops at -100, and 20,000 random 32-bit values include one
of those 16 with odds of about 1 in 13,000. The `-2^31 + 2^k` inputs were
added for it. M11 is the boundary case: it differs from the other arms on
one value, `2^30`, which only the power-of-two pass reaches, and that one
input fails P1, P6 and P7.

## Verification

All five arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build`. All six programs are
valgrind-clean at `-O0` (`0 errors from 0 contexts`). The five arms' output
is byte-identical to `power_of_four.py` and `power_of_four.py --divide`.

The benchmark kernel's sink matches all four language twins and Python
(`sink 207349543`), and `karac run --interp` prints the same sink.

## Benchmarks

`bench/power_of_four.kara` and its four mirrors time the ★ arm as written.
500,000 32-bit values are built once, a third each of: a power of four
`4^0 .. 4^15`, a near miss (a power of two with an odd exponent, or a power
of four plus or minus one), and a random 32-bit value. Each of 100 punches
replaces one value at a random position and classifies the whole array
again. The test has no loop, so the classification pass is the whole cost.
The count and sum of accepted values are folded into a rolling hash, which
is the sink.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each, 5 warmups, on a 4-core x86-64 Linux container, karac
`0.1.0-dev.10448+g76727438c`, measured 2026-10-05. Python is its own lane at
3 runs.

| implementation | mean | vs fastest |
|---|---|---|
| c `-march=x86-64-v3` (matched-ISA) | 47.7 ms ± 2.2 | 1.00× |
| rust `-O` | 331.6 ms ± 11.9 | 6.95× |
| rust `-O -C overflow-checks=on` (equal-safety) | 337.2 ms ± 11.5 | 7.07× |
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 342.9 ms ± 18.4 | 7.19× |
| **kāra `karac build`** | **352.2 ms ± 15.6** | **7.39×** |
| c `clang -O3` | 368.7 ms ± 13.3 | 7.73× |
| go `go build` | 385.0 ms ± 13.4 | 8.07× |
| python 3 | 6056 ms ± 61 | 127× |

**Kāra ties every scalar build; one C build is seven times faster.** Six
rows sit within 16% of each other, and Kāra is 4% behind Rust with overflow
checks. The outlier is clang with AVX2, which vectorises the classification
pass. Plain `clang -O3` targets baseline x86-64 and does not, so the gap is
the instruction set, not the language. Rust with the same instruction set
also does not vectorise, because the overflow check on `count += 1` and
`sum += x` is a branch in every iteration. Kāra checks the same additions,
so it is in the same position. Each scalar run spends about 7 ns per
element, and most of that is the branch on whether a value is accepted,
which the random mix makes unpredictable: the same C build on an array of
nothing but powers of four runs in 0.07 s instead of 0.36 s. The vector loop
has no branch to mispredict.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 108.4 ms ± 5.1 | 15.8 KiB | 3.4 MiB |
| rust | 147.1 ms ± 5.9 | 3864.3 KiB | 4.0 MiB |
| kāra | 347.7 ms ± 24.9 | 341.6 KiB | 4.2 MiB |
| go | — | 2179.3 KiB | 9.5 MiB |
| python | — | — | 24.0 MiB |

`karac build` is 3.2× clang's cold compile and 2.4× rustc's. Its binary is
22× clang's and 11× smaller than rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

**No correctness gaps.** All six programs were byte-identical on every
surface from the first run, and so were eight more spellings probed along
the way: recursion, a `match` with guards, a binary literal mask,
`1 << (2 * k)` in a loop, `<<= 2` on an `i32`, `log2`, `trailing_zeros() & 1`
and a square root.

- **B-2026-10-05-25 (diagnostics, low): `n.is_power_of_two()` on an `i32`
  said only "no method 'is_power_of_two' on type 'i32'".** The method is
  unsigned-only by design, but the message read as if it did not exist.
  Fixed in the kara repo: the error now says the method is defined on
  unsigned integers only and names the cast, with the warning that a
  negative value reinterprets as a large unsigned one.

`karac check` reported one error on the first draft: the sweep
`for n in -1000..1000001` makes `n` an `i64`, as design.md specifies for an
unannotated integer literal, and passing it to `is_power_of_four(n: i32)` is
a narrowing coercion. The message suggests `as i32` at the call, and
`karac fix` has no edit for it. Typing the range, `-1000i32..1000001`, is
the better fix, since the values all fit. The author already knows the
language, so none of this counts toward the machine-fix rate.
