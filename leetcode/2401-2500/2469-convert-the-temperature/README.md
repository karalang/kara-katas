# 2469. Convert the Temperature

You are given a non-negative floating point number rounded to two
decimal places `celsius`, that denotes the **temperature in Celsius**.

You should convert Celsius into **Kelvin** and **Fahrenheit** and
return it as an array `ans = [kelvin, fahrenheit]`.

Return *the array `ans`*. Answers within `10^-5` of the actual answer
will be accepted.

**Note that:**

- `Kelvin = Celsius + 273.15`
- `Fahrenheit = Celsius * 1.80 + 32.00`

```
celsius = 36.50   ->  [309.65000, 97.70000]
celsius = 122.11  ->  [395.26000, 251.79800]
```

**Constraints:** `0 <= celsius <= 1000`.

The work is two floating-point formulas; what a kata can find here is
how the arms' different but equal formulas round, and how Kāra formats
an `f64` to a fixed number of decimals. Every exact answer has at most
four decimals, since the input has two and the factor one, so printed
to five each arm's answer reads the same.

## Approaches

| file | mechanism |
|---|---|
| `convert.kara` ★ | the two formulas as given, `celsius + 273.15` and `celsius * 1.80 + 32.00`. O(1) |
| `convert_ratio.kara` | the textbook ratio: `celsius * 9 / 5 + 32`, the multiplication before the division. O(1) |
| `convert_kelvin.kara` | through kelvin: kelvin first, then Rankine as kelvin times 1.8, and Fahrenheit as Rankine less 459.67. O(1) |
| `convert_exact.kara` | in exact integers: the input as a whole number of hundredths, kelvin that plus 27315 hundredths, Fahrenheit `hundredths * 18 + 32000` thousandths, each turned into an `f64` by one division, so only the last step rounds. O(1) |
| `convert_iter.kara` | iterators: each scale a pair of factor and offset, `(1, 273.15)` and `(1.8, 32)`, mapped over by `map`. O(1) |
| `convert_solution.kara` | LeetCode's Rust template: the ★ arm's formulas in a `vec![..]`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples; then five
more, the range's two ends, a hundredth above the first, 40, and a
hundredth below the last, each printed with `{:.5}`; then every
hundredth from 0 to 1000, the constraints' whole range, as the sums of
the answers' two values in hundred-thousandths; and 3000 random
temperatures with two decimals, as a checksum. `convert.py` mirrors
the ★ arm and its output is byte-identical, and the mirror was checked
on every hundredth from 0 to 1000 against the formulas in exact
fractions: no value is more than `3 * 10^-13` off.

`check` first reports 1 error on the template, the brackets of
`Vec<f64>`, and `karac fix` carries it in one call, reporting 4 edits:
those brackets, two edits; `vec![..]` written as a list; and `struct
Solution {}` added. The two formulas stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally, in exact integers: with `celsius` a whole number of
hundredths `h`, `Kelvin = Celsius + 273.15` is `100 * h + 2731500` and
`Fahrenheit = Celsius * 1.80 + 32.00` is `180 * h + 320000`, both in
ten-thousandths, which the statement's own decimals need. No float
stands in for the reading. It checks 360 random temperatures from 0 to
1000 with two decimals, all drawn before any arm answers.

| | property |
|---|---|
| P1 | each value within `10^-5` of the literal reading's, the statement's own tolerance |
| P2 | kelvin less celsius is 273.15, within `10^-9` |
| P3 | five degrees Celsius more: nine degrees Fahrenheit more, within `10^-9` |
| P4 | a hundredth more: both values larger |
| P5 | kelvin times 1.8 less 459.67 is the Fahrenheit value, within `10^-9` |
| P6 | each arm agrees with at least three of the other five, within `10^-9` |

P2 is the first formula. P3 holds because the second is linear with
slope 1.8. P4 holds because both formulas rise with the temperature.
P5 holds because `(c + 273.15) * 1.8 - 459.67 = c * 1.8 + 32`, the two
formulas tied through the Rankine scale. Near 1000 the five degrees and
the hundredth are taken downward, so every temperature stays in range.

The differential prints `360 cases: checksum 524886050, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases in exact fractions. On a failure it prints the first ten
and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: the two values swapped | P1 360, P2 360, P3 360, P5 360, P6 360 |
| M5 | ★: the Celsius degrees floored for Fahrenheit | P1 357, P4 357, P5 357, P6 357 |
| M6 | ★: kelvin cut to tenths | P1 330, P2 330, P4 325, P5 330, P6 330 |
| M7 | ratio: the ratio inverted | P1 360, P3 360, P5 360, P6 360 |
| M9 | ratio: the scaled degrees rounded | P1 360, P4 348, P5 360, P6 360 |
| M10 | ratio: kelvin a millionth high | P2 360, P5 360, P6 360 |
| M12 | kelvin: the absolute offset misread | P1 360, P5 360, P6 360 |
| M14 | kelvin: kelvin from 273 | P1 360, P2 360, P6 360 |
| M16 | kelvin: Rankine rounded to tenths | P1 356, P4 293, P5 356, P6 356 |
| M17 | exact: the hundredths truncated | P1 16, P2 16, P3 10, P4 12, P6 16 |
| M18 | exact: the kelvin offset transposed | P1 360, P2 360, P5 360, P6 360 |
| M21 | exact: kelvin cut to tenths | P1 328, P2 328, P4 319, P5 328, P6 328 |
| M23 | iter: the scaled degrees cut to tenths | P1 355, P2 330, P4 354, P5 308, P6 355 |
| M25 | iter: the degrees rounded first | P1 357, P2 357, P4 357, P6 357 |
| M26 | iter: the scaled degrees capped at 1000 | P1 144, P3 147, P4 144, P5 144, P6 144 |
| M28 | solution: the hundredths floored for Fahrenheit | P1 16, P3 10, P4 12, P5 16, P6 16 |
| M31 | solution: kelvin from the whole degrees | P1 357, P2 357, P4 357, P5 357, P6 357 |

P6 kills all seventeen, P1 sixteen, P5 fourteen, P4 eleven, P2 ten,
and P3 five. The ratio arm's kelvin a millionth high (M10) is inside
the statement's tolerance, so P1 passes it, and P2, P5 and P6, held to
`10^-9`, kill it.

Fourteen are not kept, and each fails exactly as a kept one. A constant
off by the same amount at every temperature fails every case alike, so
the edits fall into four kinds: kelvin offset, the ★ arm's kelvin a
hundredth high, the iter arm's offset transposed and the template's
kelvin below zero (M1, M22, M27), as the exact arm's offset transposed
(M18); a wrong factor, the ★ arm's 1.81, the kelvin arm's and the
template's 1.08 and the iter arm's 1.6 (M2, M13, M30, M24), as the
ratio arm's ratio inverted (M7); a wrong Fahrenheit offset, the ★ arm's
32.10, the ratio arm's offset taken away and added before scaling, the
kelvin arm's Rankine for Fahrenheit, and the exact arm's offset a tenth
and Fahrenheit read in hundredths (M4, M8, M11, M15, M19, M20), as the
kelvin arm's absolute offset misread (M12); and the template's kelvin a
ten-millionth high (M29) as the ratio arm's a millionth (M10).

Six edits of the first run were replaced by edits that fail on only
some temperatures, since every constant edit of those arms failed as a
kept one: the kelvin arm's Rankine a hundredth high, the iter arm's
Fahrenheit offset transposed, offset added before scaling and offset
scaled too, and the template's offset 0.32 and Fahrenheit from the
kelvin value. Every edit is killed by some check.

## Verification

Every arm prints the same output as `convert.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.4 to 0.5 s, the iter arm 1.5 s, and the differential 0.3 s; under `karac __mir-llvm-asan` every file takes 0.3 to 0.6 s.

## Benchmarks

The bench makes 230 passes over every temperature from 0 to 1000 in
hundredths, each pass starting at a hundredth chosen from the checksum
so far, so no pass repeats the last; each answer's kelvin in hundredths
and Fahrenheit in thousandths, rounded, is folded into the checksum
with the pass. The bench uses the ★ arm in all five languages, each
answer a fresh two-value list in Kāra, Rust, Go and Python; C writes
into a caller's array of two. The work per answer is a handful of
floating-point steps, so the bench measures the call, the list and the
rounding as much as the formulas. Every implementation prints `230
passes over every hundredth from 0 to 1000: checksum 421855759`.

BENCHTAB
