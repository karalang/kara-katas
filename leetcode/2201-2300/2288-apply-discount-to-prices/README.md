# 2288. Apply Discount to Prices

A **sentence** is a string of single-space separated words where each
word can contain digits, lowercase letters, and the dollar sign `'$'`.
A word represents a **price** if it is a sequence of digits preceded by
a dollar sign.

- For example, `"$100"`, `"$23"`, and `"$6"` represent prices while
  `"100"`, `"$"`, and `"$1e5"` do not.

You are given a string `sentence` representing a sentence and an
integer `discount`. For each word representing a price, apply a
discount of `discount%` on the price and **update** the word in the
sentence. All updated prices should be represented with **exactly two**
decimal places.

Return *a string representing the modified sentence*.

```
sentence = "there are $1 $2 and 5$ candies in the shop", discount = 50
    ->  "there are $0.50 $1.00 and 5$ candies in the shop"
sentence = "1 2 $3 4 $5 $6 7 8$ $9 $10$", discount = 100
    ->  "1 2 $0.00 4 $0.00 $0.00 7 8$ $0.00 $10$"
```

**Constraints:** `1 <= sentence.length <= 10^5`; `sentence` consists of
lowercase English letters, digits, `' '`, and `'$'`; `sentence` does not
have leading or trailing spaces; all words in `sentence` are separated
by a single space; all prices are **positive** numbers without leading
zeros; all prices have **at most** `10` digits; `0 <= discount <= 100`.

Split on spaces. A word of `$` and then one or more digits is a price,
and its discounted value in cents is exactly `price * (100 - discount)`,
at most about 10^12, so it fits an `i64`; write it back as the cents
divided by 100, a point, and the remainder padded to two digits. No
floating point. O(n).

## Approaches

| file | mechanism |
|---|---|
| `discount.kara` ★ | `split(" ")`; `is_price` by `starts_with("$")` and `bytes().iter().skip(1).all(is_ascii_digit)`; the cents as an `i64`, written with `{:02}`; `join(" ")` |
| `discount_naive.kara` | a walk over `bytes()` to each space, the word judged and its value read digit by digit in one pass; the answer pushed onto one `String` |
| `discount_float.kara` | the price parsed as an `f64`, multiplied by `(100 - discount) / 100.0`, and written with `{:.2}`, as most submitted answers do |
| `discount_struct.kara` | `enum Token` of `Price(Cents)` or `Text(String)`, read by `Token.read`; `struct Cents` discounts itself and implements `Display` as dollars and cents |
| `discount_iter.kara` | `split`, a `map` closure that takes the tail after a `$` and parses it when it is all digits, `collect` into a `Vec[String]`, `join` |
| `discount_solution.kara` | LeetCode's Rust template: `String` and `i32` in, `String` out; `split_whitespace`, an `f64` factor and `format!("${:.2}", ..)`, `collect::<Vec<String>>()` and `join`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; prices of
`$0`, `$00` and `$007` (zeros the constraints rule out, which every arm
reads as a number all the same); two ten-digit prices at 1% and at 99%;
the words that are nearly prices, `$`, `$$5`, `$5$`, `$5e3` and `a$1`;
a ten-digit price at no discount; then 2000 random sentences of 1 to 12
words, each a price, a `$` alone, `$` before letters or before digits
ending in `e`, a word of letters or a number with no `$`, with the
discount 0 to 100, folded into a checksum and a byte count.
`discount.py` mirrors the ★ arm and its output is byte-identical.

The float arms agree with the integer arms on every case. A price of at
most ten digits times a factor of hundredths is a value below 10^10
whose error in an `f64` is far below half a cent, so `{:.2}` rounds to
the exact cents.

`karac fix` carries the template in one call, reporting 7 edits: `&&`
to `and` twice, the `'$'` pattern to `"$"`, `w[1..].parse()` with the
`f64` annotation to `f64.parse(w[1..])`, `format!` to an f-string, and
the turbofish `collect::<Vec<String>>()`, whose result is the receiver
of `join`, to `Vec[String].from_iter(..)` around the iterator. The
struct arm was written first with Rust's `fn fmt(&self, f)` and
`write!`, which `karac fix` turns into `fn to_string(self) -> String`
returning an f-string, and a `!` turned to `not`: 4 edits. The naive
arm's `as i64` on a `u8` digit was dropped: 1 edit.

The iterator arm was written first with `.collect[Vec[String]]()`,
Kāra's bracket spelling of a turbofish. That is not a call with a type
argument but the field `collect` indexed by `Vec[String]`, and `karac
check` said `no field 'collect' on struct 'IterMap'`. Worse, `karac fix`
applied the fix-it of the deprecated `Vec[..]` prefix literal to the
index and produced `.collect[[String]]()`, which reads `String` as a
function. The compiler now answers that spelling as it answers the
turbofish, with no fix that rewrites the index (B-2026-11-18-86). The arm names
the collection on its `let` instead, as the language means it to.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a word is a price when it is `$` and then one or more
digits, tested character by character; its digits, as written, are
multiplied by `100 - discount` on paper, from the right, each digit
times the factor plus the carry, and the point is set two places from
the right, with zeros to make three digits and the whole part's leading
zeros dropped. No integer wider than a digit times 100 plus a carry, no
division of the price, no floats. It checks 300 random sentences drawn
as the arms' harness draws them; then 30 of ten-digit prices; then 30
of words that are nearly prices, `$$5`, `5$`, `$5x`, `$5.5`, `$005` and
`$-5`. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer has as many words, and every word that is not a price is unchanged |
| P3 | each word on its own gives the same word as in the sentence |
| P4 | a discount of 100: every price reads `$0.00` |
| P5 | a discount of 0: every price reads as its own value and `.00` |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 381275497, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading by
`re.fullmatch(r"\$[0-9]+")` and `int`. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the cents unpadded | P1 117, P4 326, P5 326, P6 117 |
| M3 | ★: the discount added | P1 324, P4 325, P6 324 |
| M4 | ★: the `$` itself checked a digit | P1 326, P4 326, P5 326, P6 326 |
| M8 | naive: a lone `$` a price | P1 152, P2 152, P6 152 |
| M9 | naive: a `9` not a digit | P1 244, P4 244, P5 244, P6 244 |
| M10 | naive: the value's digits summed | P1 316, P5 319, P6 316 |
| M13 | float: the factor the discount | P1 322, P4 325, P5 325, P6 322 |
| M16 | float: a one-digit price not a price | P1 83, P4 83, P5 83, P6 83 |
| M17 | float: the price truncated | P1 320, P6 320 |
| M18 | struct: the discount applied twice | P1 321, P6 321 |
| M19 | struct: the cents as dollars | P1 322, P5 325, P6 322 |
| M20 | struct: a text emptied | P1 303, P2 303, P6 303 |
| M23 | iter: a bare number a price | P1 159, P2 159, P6 159 |
| M24 | iter: the words joined with nothing | P1 to P6 327 each |
| M27 | iter: the tail from the second digit | P1 318, P2 23, P5 298, P6 318 |
| M28 | solution: the discount at 1% | P1 325, P4 326, P5 325, P6 325 |
| M29 | solution: a space after the `$` | P1 to P6 326 each |

P1 and P6 kill all seventeen, P5 eleven, P4 nine, P2 six and P3 two.
P4 and P5 hold the discount at its ends, where every price's answer is
known without the arm: they catch the edits that misread the factor or
miswrite the cents. P2 catches the edits that touch a word that is not
a price. P3, each word alone, fails only where the words run together
or split apart: joined with nothing, or a space written inside a price.
Three edits that miswrite the value only somewhere in the middle of the
discount range, the price truncated to dollars, the discount applied
twice, and the struct arm's cents as dollars, are caught by P1 and P6
and by the ends only where an end is affected.

Of the thirty-one, fourteen were not kept. Two crash under both
backends: the ★ arm's lone `$` a price and any digit enough (M1, M6)
both send a word that is not all digits to `i64.parse(..).unwrap()`.
Eleven fail as a kept one does: the ★ arm's price kept whole and the
template's price undiscounted (M5, M31) as the ★ arm's discount added
(M3); the float arm's one decimal and `$` dropped and the iter arm's
three places of cents (M14, M15, M26) as the ★ arm's `$` checked a
digit (M4); the naive arm's no space between words and next word from
the space (M7, M11) as the iter arm's words joined with nothing (M24);
the naive arm's dollars rounded up and the template's rounded to
dollars (M12, M30) as the float arm's price truncated (M17); the struct
arm's price in dollars (M21) as its cents as dollars (M19); the iter
arm's discount as the price (M25) as the float arm's factor the
discount (M13). The struct arm's cents' digits swapped (M22) fails in a
way of its own and is left out because its arm keeps enough.

Four edits of the first draft were replaced. The float arm's lone `$` a
price, the iter arm's `$` alone a price and the template's any digit
enough each crashed on the same `unwrap`; the iter arm's words reversed
was written with a turbofish `collect` and did not compile. They are now
M16, M23, M29 and M26.

## Verification

Every arm prints the same output as `discount.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.4 to 0.6 s. The differential
takes 2 s.

## Benchmarks

The bench builds 4000 sentences of 12 words once, each word a price of
1 to 8 digits, a `$` before letters, a word of letters or a number with
no `$`, then makes 50 passes over all of them at discounts of 0, 2, 4
and so on to 98, folding each answer's length and its next-to-last byte
into a checksum, with the ★ arm in all five languages. Every
implementation prints `50 passes over 4000 sentences: checksum
317233264`. C walks each sentence once and writes the answer into one
buffer with `sprintf`, where the others build each word as a string and
join them.

BENCHTAB
