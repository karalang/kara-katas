# 2232. Minimize Result by Adding Parentheses to Expression

You are given a **0-indexed** string `expression` of the form
`"<num1>+<num2>"` where `<num1>` and `<num2>` represent positive
integers.

Add a pair of parentheses to `expression` such that after the addition
of parentheses, `expression` is a **valid** mathematical expression and
evaluates to the **smallest** possible value. The left parenthesis
**must** be added to the left of `'+'` and the right parenthesis
**must** be added to the right of `'+'`.

Return `expression` *after adding a pair of parentheses such that*
`expression` *evaluates to the **smallest** possible value.* If there
are multiple answers that yield the same result, return any of them.

The input has been generated such that the original value of
`expression`, and the value of `expression` after adding any pair of
parentheses that meets the requirements fits within a signed 32-bit
integer.

```
expression = "247+38"   ->  "2(47+38)"     (2 * (47 + 38) = 170)
expression = "12+34"    ->  "1(2+3)4"      (1 * (2 + 3) * 4 = 20)
expression = "999+999"  ->  "(999+999)"
```

**Constraints:** `3 <= expression.length <= 10`; `expression` consists
of digits from `'1'` to `'9'` and `'+'`; `expression` starts and ends
with digits; `expression` contains exactly one `'+'`.

Every place for the two parentheses is tried: `"("` before digit i of
the left number and `")"` after digit j of the right one, the value `a *
(b + c) * d` with an empty `a` or `d` counting as 1, and the first
smallest kept. O(n^2) placements of O(n) each, for n <= 10.

## Approaches

Every arm keeps the first smallest placement in the same order, `"("`
from left to right and then `")"` from left to right, so they all return
the same string even where placements tie.

| file | mechanism |
|---|---|
| `parentheses.kara` ★ | the two numbers cut out with `substring` and every piece parsed with `i64.parse`, the answer written with an `f`-string |
| `parentheses_digits.kara` | the expression as a `Vec[char]`, each piece's number read off its digits by arithmetic, and only the best placement written out at the end |
| `parentheses_eval.kara` | each candidate written out in full, the parentheses `insert`ed into the expression's characters, and the string evaluated as it reads: a number beside a parenthesis multiplying |
| `parentheses_struct.kara` | a `struct Sides` of the two numbers, from `split("+")`, with `value`, `written` and `best` (`ref self`) |
| `parentheses_iter.kara` | the placements a `flat_map` over the left places of a `map` over the right ones, `min_by_key` keeping the first smallest, the numbers through a closure that reads an empty piece as 1 |
| `parentheses_solution.kara` | LeetCode's Rust template: `split('+')` into a `Vec<&str>`, the pieces cut as slices `l[..i]` and `l[i..]` and parsed with `parse::<i32>()`, the best from `i32::MAX`, and the answer written with `format!` of the slices taken by `&`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more (one digit each side, both sides split, the longest left side, and
the longest right side), each with its answer; then a checksum of 3000
random expressions of 3 to 10 characters; then, over every expression
of two digits on each side, how many answers wrap the whole sum and how
many split a number. `parentheses.py` mirrors the ★ arm and its output
is byte-identical.

`karac fix` carries the template in one round of 16 edits:
`Vec<&str>` to `Vec[Str]`, `split('+')` to `split("+")`, `i32::MAX` and
`String::new()` to `i32.MAX` and `String.new()`, each
`l[..i].parse::<i32>()` to `i32.parse(l[..i])`, `format!("{}({}+{}){}",
&l[..i], ...)` to the `f`-string `f"{l[..i]}({l[i..]}+{r[..j]}){r[j..]}"`,
and `struct Solution;` to `struct Solution {}`. The range slices of a
`Str` are Kāra's too.

The eval arm was first written inserting the parentheses with
`String.insert`, which Kāra's `String` does not have: `karac check`
said to collect the characters into a `Vec[char]`, whose `insert` does
it, and collect them back, and that was done by hand, as there is no
machine fix for it. The struct and iter arms were first written
collecting `split("+")` straight into a `Vec[String]`, and the iter arm
with Rust's `move` before a closure; `karac fix` added `.map(|p|
p.to_string())` and deleted the `move`. The struct arm's search first
started from the whole sum wrapped rather than from the first placement,
which broke ties differently from the other arms; it was set to start
from the first.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: `"("` tried at every place in the string and `")"` at every
place at or after it, each string kept when it is a well-formed
expression with `"("` left of `"+"` and `")"` right of it, read by a
general evaluator in which a number beside a parenthesis multiplies, and
the smallest value; no splitting into `a * (b + c) * d`. Since any
smallest answer is accepted, the arms are judged by the value of the
string they return. It checks 300 random expressions of 3 to 10
characters; then 30 with one side a single digit; then 30 of 1s only,
where many placements tie. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer's value is the smallest, read literally |
| P2 | the answer is the expression with one `"("` and one `")"` added, well-formed, `"("` left of `"+"` and `")"` right of it |
| P3 | its value is at most both the sum itself and the sum of the two digits beside `"+"` in parentheses |
| P4 | the first digit of the left number raised: no smaller value |
| P5 | the last digit of the right number raised: no smaller value |
| P6 | each arm's value agrees with at least three of the other five |

The differential prints `360 cases: checksum 372514681, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal values was checked against a Python reading that takes
the smallest `a * (b + c) * d` over every split of each side. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to each
of the others, each run under `karac __mir-llvm-run`, and the kept ones
under `karac __mir-run` too. Seventeen are kept, three to each Kāra arm
and two to the Rust-template arm. Each kept one is killed, fails the
same way under both backends and not by a crash, and no two kept ones
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `"("` never before the first digit | P1 122, P2 65, P3 112, P6 122 |
| M2 | ★: an empty right end counted as 0 | P1 313, P3 112, P6 313 |
| M6 | ★: an empty left end counted as 0 | P1 336, P3 271, P6 336 |
| M8 | digits: every digit read one less | P1 108, P3 67, P4 36, P5 39, P6 108 |
| M9 | digits: `")"` also right after `"+"` | P1 24, P2 24, P3 24, P6 24 |
| M10 | digits: the best `"("` never recorded | P1 238, P3 81, P4 2, P5 2, P6 238 |
| M13 | eval: the sum only its right part | P1 295, P3 233, P6 295 |
| M15 | eval: `"("` inserted first, moving `")"` one place left | P1 247, P2 121, P3 218, P6 247 |
| M16 | eval: the left part of the sum counted twice | P1 24, P3 11, P4 1, P5 5, P6 24 |
| M17 | struct: the number before `"("` taken as 1 | P1 272, P3 203, P6 272 |
| M20 | struct: a one-digit right part inside never tried | P1 126, P3 69, P6 126 |
| M21 | struct: the two sides swapped | P1 306, P2 357, P3 4, P6 306 |
| M23 | iter: the largest kept | P1 350, P3 350, P6 350 |
| M25 | iter: the sum a product | P1 203, P3 136, P6 203 |
| M26 | iter: the number after `")"` dropped | P1 210, P3 165, P6 210 |
| M27 | solution: the best starting at 1000 | P1 273, P2 273, P3 273, P4 3, P6 273 |
| M28 | solution: one digit inside on the left | P1 276, P3 188, P4 11, P5 10, P6 276 |

P1, P3 and P6 kill all seventeen, P2 and P4 five each, and P5 four.
P3's bound is tight, since wrapping the two digits beside `"+"` is
often the best or close to it, so almost every wrong value passes it.
P2 catches the edits that write a wrong string rather than a wrong
value: no placement at all (M1, M27), a `")"` with nothing before it
(M9), one moved off its digit (M15), and the sides swapped (M21). P4 and
P5 raise one digit and expect the answer not to fall; most edits are
wrong by the same rule either way, and only those whose error depends
on the digits' size break it.

Of the thirty-one, fourteen were not kept. Two survive and are
equivalent within the differential, which accepts any smallest answer:
the ★ arm keeping the last smallest placement (M4), and the iter arm
trying the left places from the right (M24); both change only which of
two equal answers is written. None crashes, and none differs between
the backends. Nine fail as a kept one does: the ★ arm's sum without
parentheses (M3) as the iter arm's product (M25); the ★ arm's `")"`
never at the end (M5) as the eval arm's (M15); the digits and iter arms'
empty number as 0 (M7, M22) as the ★ arm's (M6); the eval arm's number
before `"("` dropped (M12) as the struct arm's (M17); the eval and
struct arms' number after `")"` dropped (M14, M18) as the iter arm's
(M26); the struct arm's largest (M19) as the iter arm's (M23); and the
template's answer always written whole (M30) as the ★ arm's empty right
end (M2). Three fail their own way and are left out for the count of
three (two for the template): the digits arm's `"("` never at the start
(M11), and the template's number after `")"` added and at most two right
digits inside (M29, M31).

## Verification

Every arm prints the same output as `parentheses.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.4 s to 1.3 s, and the
differential 1.3 s.

## Benchmarks

The bench draws 20000 expressions of 3 to 10 characters once, then makes
20 passes over all of them, one expression drawn again before each pass,
with the ★ arm in all five languages; the answer is folded to its length
and the places of its parentheses. C parses each piece with `strtoll`
and writes the answer with `snprintf`. Every implementation prints `20
passes over 20000 expressions: checksum 392550337`.

BENCHTAB
