# 1056. Confusing Number

A **confusing number** is a number that, when rotated 180 degrees, becomes
a different number with each digit valid.

Rotated 180 degrees, `0`, `1`, `6`, `8` and `9` become `0`, `1`, `9`, `8`
and `6`, and `2`, `3`, `4`, `5` and `7` become invalid. Leading zeros of
the rotated number are ignored: `8000` becomes `0008`, which is `8`.

Given an integer `n`, return `true` if it is a confusing number, or
`false` otherwise.

```
n = 6   ->  true    (rotated: 9)
n = 89  ->  true    (rotated: 68)
n = 11  ->  false   (rotated: 11, the same number)
n = 25  ->  false   (2 and 5 do not rotate)
```

**Constraints:** `0 <= n <= 10^9`.

## Approaches

The last digit of `n` becomes the first of the turned number, so the turned
number can be built while `n` is taken apart from its end, or compared
digit by digit with the digit at the mirror place, turned.

| file | mechanism |
|---|---|
| `confusing.kara` ★ | a table of what each digit turns into, `-1` for none; the turned number built up as `n` is divided by 10. O(d) for d digits |
| `confusing_match.kara` | a `match` per digit returning `Option`, and a recursion that gives up through `?` at the first digit that does not turn. O(d) |
| `confusing_string.kara` | the decimal string read from the back, each character turned, collected into an `Option[String]` and parsed back. O(d) |
| `confusing_pairs.kara` | no number built: every digit must turn, and some place must hold a digit other than its mirror's turn. O(d) |
| `confusing_iter.kara` | the digits by `successors(Some(n), ..)` and `% 10`, the turned number by `try_fold` over a table of `Option`s, the answer by `map_or`. O(d) |
| `differential.kara` | the five arms against the statement read literally, seven properties |

Every arm prints the same 19 lines: the answers for LeetCode's examples and
six more; how many numbers from 0 to 100000 are confusing, their total and
a checksum of every answer; the same for 3000 random numbers whose digits
all turn; and seven answers at the limit, among them `1000000000`,
`999999999` and `986101986`, which reads the same upside down.
`confusing.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the decimal string read from the back, each digit drawn as the
one it looks like upside down, the zeros it starts with dropped, and the
text compared with `n`'s. It checks 3000 numbers: 1000 of 1 to 9 digits
that all turn, 1000 that read the same upside down (a number's digits, then
nothing or one of 0, 1 and 8, then its digits turned), and 1000 of any
digits, up to 2000 or up to 10^9.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | a number with a 2, 3, 4, 5 or 7 is never confusing; one above 0 whose digits all turn and that ends in 0 always is; one digit is confusing exactly when it is 6 or 9 |
| P3 | a number whose digits all turn and that does not end in 0 is confusing exactly when the number it turns into is |
| P4 | a number's digits followed by its digits turned, with nothing, 0, 1 or 8 between, read the same upside down: never confusing |
| P5 | every 6 made a 9 and every 9 a 6 leaves the answer |
| P6 | the digits reversed, for a number that does not end in 0, leave the answer |
| P7 | each arm agrees with at least two of the other four |

P3 holds because turning twice gives the number back when it does not end
in 0. P5 holds because the swap maps each pair a number reads the same
through, (6, 9), (0, 0), (1, 1) and (8, 8), to another such pair. P6 holds
because a number reads the same upside down exactly when each digit is the
turn of its mirror's, and reversing keeps that.

The differential prints `3000 numbers: checksum 370285823, 87295 checks
over 5 arms: 0 failures` under `karac __mir-run` (3.1 s), `karac
__mir-llvm-run` and `karac __mir-llvm-asan` with no error, and the same
line under `karac run` and from a `karac build` binary. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Fifteen are kept, three to each arm.
Twenty-nine are killed and one is equivalent, each fails the same way under
both backends, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: 6 and 9 turned into themselves | P1 723, P2 51, P4 1016, P7 723 |
| M2 | ★: a digit that does not turn taken as one | P1 938, P2 938, P5 3, P6 2, P7 938 |
| M3 | ★: the first digit never turned | P1 968, P2 101, P4 1321, P6 93, P7 968 |
| M4 | match: 8 not a digit that turns | P1 649, P2 170, P7 649 |
| M5 | match: the answer the other way round | P1 2061, P2 514, P4 1321, P7 2061 |
| M6 | match: 0 turned into 1 | P1 289, P4 514, P7 289 |
| M7 | string: the string not reversed | P1 757, P2 92, P4 1016, P7 757 |
| M8 | string: 6 turned into itself | P1 671, P2 25, P3 87, P4 1016, P5 87, P7 671 |
| M9 | string: a digit that does not turn makes it confusing when it is even | P1 460, P2 460, P5 152, P6 411, P7 460 |
| M10 | pairs: only the first half of the digits looked at | P1 216, P2 208, P6 264, P7 216 |
| M11 | pairs: a digit that does not turn skipped | P1 861, P2 861, P7 861 |
| M12 | pairs: the first place never looked at | P1 105, P2 105, P6 93, P7 105 |
| M13 | iter: the walk stops before the first digit | P1 919, P2 52, P4 1321, P6 93, P7 919 |
| M14 | iter: each step takes the digit before | P1 1037, P2 170, P4 1321, P6 93, P7 1037 |
| M15 | iter: each turned digit one more | P1 995, P2 128, P4 1321, P7 995 |

P1 and P7 kill all fifteen, P2 fourteen, P4 nine, P6 seven, P5 three and
P3 one. M6 escapes P2: turning 0 into 1 never touches a number with a digit
that does not turn, nor one of a single digit. P3 and P5 see only the edits
that break the pairing of 6 and 9 one way (M8): turning both 6 and 9 into
themselves (M1) keeps a number and its turn, and a 6 and a 9, alike. P6
sees the edits that treat one end of the number in its own way (M3, M10,
M12, M13, M14) and the two that let a bad digit through (M2, M9). P4
sees the edits that misjudge numbers that read the same upside down.

The other fifteen fail as others do or not at all. Four fail exactly as a
kept one: the pairs arm comparing each digit with its own turn, as M7; the
pairs and iter arms turning 6 into itself, as M8; and the iter arm starting
the turned number at 1, as M15. Four fail in pairs with no kept member: the
match arm adding the turned digits up and the pairs arm calling every
number of two digits or more confusing; and the match and iter arms making
a number with a digit that does not turn confusing. Six fail in ways of
their own: the ★ arm not shifting the turned digits along, calling every
number that ends in 0 confusing, and turning 7 into itself; the match arm
losing the turned number; and the string arm with 1 not turning, and with
9 turned into itself. One is equivalent: the string arm comparing the
turned string, zeros and all, with `n`'s. A turned string that starts with
0 comes from an `n` that ends in 0, which is never the turned number.

## Verification

Every arm prints the same output as `confusing.py` under `karac __mir-run`
(the v2 MIR interpreter) and `karac __mir-llvm-run`, and under `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error. `karac
run` and a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any file. The
runs used a release build of kara `41016ef78e`. Under `karac __mir-run` the arms
take 0.3 s (★) to 1.5 s (iter).

The ★ arm was written in Kāra and checked clean. The other four, written
the way Rust writes them, went through `karac fix` (`Option<..>` to
`Option[..]`, `[T; N]` to `Array[T, N]`, `t.parse::<i64>()` to
`i64.parse(t)`, `as_bytes()` to `bytes()`, `std::iter::successors` to
`successors` and the `&x` pattern dropped) and then met four gaps, fixed in
kara `41016ef78e`:

- `karac fix` took `std::iter::successors(..)` to `successors(..)`, which
  named nothing ("undefined name 'successors'"). The library now has it,
  beside `repeat` and `once` (library/iterators.md, Sources).
- `.try_fold(0, |acc, d| ..)` was "no method 'try_fold' on type
  'IterMap'". It now folds while the function returns `Some` or `Ok`,
  through a prelude trait `Try` that `Option` and `Result` implement.
- `collect()` into `Option[String]` was "`Option[String]` does not
  implement `FromIterator`". `Option[C]` and `Result[C, E]` now gather
  `Option` and `Result` items and stop at the first `None` or `Err`. Items
  whose value the collection inside does not take, such as `Option[ref
  i64]` for an `Option[Vec[i64]]`, are refused with a message that says to
  put a copy in the `Some`; LLVM had run that case as a use after free.
- A method's closure whose result type only the `let` names
  (`let r: Result[i64, String] = (1..5).try_fold(1, |a, x| Ok(a * x))`)
  was "a closure with no function type" in MIR. A method's bare generic
  return now takes the expectation, as a free function's does.

## Benchmarks

The bench builds 500000 numbers once in all five languages, each of 6 to 10
digits that turn, except that about one in eight has a digit that does not,
somewhere after the first. It then runs the ★ arm on every number 20 times.
Every implementation prints `500000 numbers, 20 rounds: 8882760 confusing,
checksum 277439415`. The work is about 80 million digits looked up and
added to the turned number, each a division by 10 and a table read.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `41016ef78e` on LLVM 22. Each time
includes building the numbers.

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.241 to 0.280 s | 0.252 s |
| Rust (`rustc -O`) | 0.247 to 0.278 s | 0.256 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.255 to 0.291 s | 0.265 s |
| Kāra (`karac build`) | 0.255 to 0.290 s | 0.275 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.267 to 0.299 s | 0.281 s |
| Go | 0.335 to 0.391 s | 0.346 s |
| Python | 11.9 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.273 s) is below its real time.

Kāra took 1.06 times Rust's median time under overflow checks and 1.12
times C's; where the difference goes was not broken down. Go took 1.37
times C's.
