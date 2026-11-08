# 2011. Final Value of Variable After Performing Operations

There is a programming language with only four operations and one
variable `X`: `++X` and `X++` increment `X` by 1, and `--X` and `X--`
decrement it by 1. `X` starts at 0. Given an array of strings `operations`,
return the final value of `X` after performing all of them.

```
operations = ["--X","X++","X++"]          ->  1
operations = ["++X","++X","X++"]          ->  3
operations = ["X++","++X","--X","X--"]    ->  0
```

**Constraints:** `1 <= operations.length <= 100`; each operation is
`"++X"`, `"X++"`, `"--X"` or `"X--"`.

## Approaches

| file | mechanism |
|---|---|
| `final_value.kara` ★ | a `match` on each operation's `as_str()`, the two increments and the two decrements each an or-pattern. O(n) |
| `final_value_count.kara` | the operations with a `+` in them counted with `filter` and `count`; `X` ends at that count less the rest. O(n) |
| `final_value_middle.kara` | the middle character alone, `chars().nth(1)`, says which way each operation goes. O(n) |
| `final_value_fold.kara` | each operation mapped to +1 when it `starts_with` or `ends_with` a `+`, -1 otherwise, and the steps `sum`med. O(n) |
| `final_value_map.kara` | a `Map` from each of the four operations to its step, built once per call, every operation looked up in it. O(n) |
| `final_value_solution.kara` | LeetCode's Rust template (a unit struct, `impl Solution`, `Vec<String>`, a `fold` with a `match` whose `_` arm decrements, a `&Vec` wrapper), carried by `karac fix` to a clean check |
| `differential.kara` | all six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: the answers for LeetCode's three
examples and three more; then the sum and a checksum of the answers for
3000 lists of 1 to 100 operations, each list leaning up or down by its own
odds. `final_value.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each operation with its `X` taken out leaves its operator, `++`
adding 1 and `--` taking 1. It checks 1500 problems of 1 to 20 operations.
Every random choice of a problem (the operations, a shuffle, an operation
to append) is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the operations shuffled leave the answer |
| P3 | each operation written in its other form (`X++` as `++X`, `--X` as `X--`) leaves the answer |
| P4 | every `+` turned into `-` and every `-` into `+` negates the answer |
| P5 | one more operation appended moves the answer by that operation's step |
| P6 | each arm agrees with at least three of the other five |

The differential prints `1500 problems: checksum 429235345, 54000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Fifteen are kept, two or
three to each arm. All thirty are killed, each fails the same way under
both backends, none by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `X++` taken as a decrement | P1 1078, P3 1048, P4 1411, P5 352, P6 1078 |
| M2 | ★: the last operation skipped | P1 1500, P2 392, P5 766, P6 1500 |
| M3 | ★: `X` starting at 1 | P1 1500, P4 1500, P6 1500 |
| M4 | count: the operations starting with `X` counted | P1 1323, P3 1304, P4 1304, P5 750, P6 1323 |
| M5 | count: every operation subtracted | P1 1239, P4 1500, P5 730, P6 1239 |
| M6 | count: the decrements halved | P1 1254, P4 1500, P5 430, P6 1254 |
| M7 | middle: a decrement taking 2 | P1 1254, P4 1500, P5 770, P6 1254 |
| M8 | middle: the first operation skipped | P1 1500, P2 363, P6 1500 |
| M9 | fold: only a trailing `+` read | P1 1086, P3 1048, P4 1438, P5 378, P6 1086 |
| M10 | fold: an end other than `-` read as `+` | P1 1115, P3 1052, P4 1438, P5 398, P6 1115 |
| M11 | table: the prefix forms' steps swapped | P1 1322, P3 1299, P5 776, P6 1322 |
| M12 | table: only the last step kept | P1 1358, P2 392, P5 1500, P6 1358 |
| M13 | Rust: a decrement resetting `X` | P1 1157, P2 622, P4 1500, P5 634, P6 1157 |
| M14 | Rust: the steps reversed | P1 1426, P5 1500, P6 1426 |
| M15 | Rust: `X--` counted up | P1 1093, P3 1052, P4 1411, P5 372, P6 1093 |

P1 and P6 kill all fifteen, P5 thirteen, P4 ten, P3 six and P2 four. With
four operations and one step each, most edits get one form wrong, and which
form is the whole signature: `X++` (M1), `++X` (M9), `--X` (M10), `X--`
(M15), or two at once (M4, M11). P3 swaps every operation's form, so it
sees exactly those six. P4 turns increments into decrements and back, so
it sees every edit that treats the two directions unevenly, and misses the
ones that treat them alike: a dropped first or last operation (M2, M8), the
prefix forms swapped together (M11), only the last step kept (M12), and
the steps reversed, which negates the answer and so commutes with P4 (M14).
P5 misses the two edits that only touch the start of the list (M3, M8):
an appended operation is counted correctly after them. P2 sees the edits
that depend on position: a dropped first or last operation (M2, M8), only
the last step kept (M12), and a decrement resetting `X` to 0 (M13).

The other fifteen fail as a kept one does. Every arm can get a single form
wrong, and each form has one signature: `X++` wrong fails alike in the ★,
count, middle, fold, table and Rust arms (six edits); `++X` wrong in the ★,
middle, fold and table arms; `--X` wrong in the fold and table arms; `X--` wrong in the ★ and Rust arms. Starting at 1 fails alike
in the ★ and Rust arms; a first operation dropped in the middle and fold
arms; the downs never subtracted, a decrement of 2 and a decrement's step of
0 alike (P4 1500, P5 770); and every operation subtracted fails as the
middle character compared with `X`. Two drafts were replaced. The Rust
arm's first operation dropped, `operations.iter().skip(1).fold(0, ..)` in
a function returning `i32`, was refused by the checker: the literal `0`
took `i64` where it was written, though `iter().fold(0, ..)` and a range's
`fold(0, ..)` take `i32` from the return (B-2026-11-08-44, fixed in kara
af14c52dbd; the edit now checks and fails as the middle and fold arms'
first operation dropped). The table arm's `--X`
stepped by 2 duplicated another edit's signature.

## Verification

Every arm prints the same output as `final_value.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any of
them. Under `karac __mir-run` the arms take 0.37 s (table) to 0.62 s
(middle) and the differential 1.4 s.

The five arms were written in Kāra and checked clean, with the examples
written `"--X".to_string()`; `karac fix` drops the `.to_string()` on each
string literal (its `redundant_literal_method` style lint: a string
literal is already a `String`), 19 edits in each arm's examples and four
more in the table arm's `insert`s.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` alone, in two rounds (7 and 21 edits). The first
carries the struct, the `Vec<..>` types, the `&Vec` parameter and the `::`
path; the second drops the wrapper's `as i64`, since an `i32` widens to
`i64` implicitly, and the same twenty `.to_string()`s. The fold's `0` takes
`i32` from the method's return type, so nothing in the arm needs a type
written.

## Benchmarks

The bench builds 20000 lists of 100 operations once in all five languages,
each list leaning up or down by its own odds, and runs the ★ arm on each
for 10 rounds: 200000 calls, 20 million operations matched. Every
implementation prints `200000 calls: sum 29660, checksum 503210695`. Each
operation is its own heap string in every language, as a `String` is; C
compares them with `strcmp`, Rust and Kāra with a `match` on the string,
Go with a `switch`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| Go | 0.296 to 0.335 s | 0.310 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.437 to 0.477 s | 0.438 s |
| Kāra (`karac build`) | 0.434 to 0.487 s | 0.454 s |
| C (`clang -O3`) | 0.455 to 0.507 s | 0.489 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.493 to 0.562 s | 0.508 s |
| Rust (`rustc -O`) | 0.484 to 0.540 s | 0.528 s |
| Python | 2.5 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.403 s) is not above its real time (0.454 s).

The sequential Kāra program is 0.86x Rust under overflow checks and 0.90x
C.