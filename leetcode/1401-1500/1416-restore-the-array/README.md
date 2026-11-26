# 1416. Restore The Array

A program was supposed to print an array of integers. The program forgot
to print whitespaces and the array is printed as a string of digits `s`,
and all we know is that all integers in the array were in the range `[1,
k]` and there are no leading zeros in the array. Given the string `s`
and the integer `k`, return the number of the possible arrays that can
be printed as `s` using the mentioned program. Since the answer may be
very large, return it modulo `10^9 + 7`.

```
s = "1000", k = 10000        ->  1    [1000]
s = "1000", k = 10           ->  0
s = "1317", k = 2000         ->  8    [1317], [131,7], [13,17], [1,317], [13,1,7], [1,31,7], [1,3,17], [1,3,1,7]
s = "2020", k = 30           ->  1    [20,20]
s = "1234567890", k = 90     ->  34
```

**Constraints:** `1 <= s.length <= 10^5`, `s` consists of only digits
and does not contain leading zeros, `1 <= k <= 10^9`.

Each arm is `fn number_of_arrays(s: String, k: i32) -> i32`. A number of
the array is at most 10 digits long, since k is.

## Approaches

| file | mechanism |
|---|---|
| `number_of_arrays.kara` ★ | ways[i] counts the arrays the digits from i on can be read as, from the end back: each number starting at i with no leading 0, read over `s.bytes()` until it passes k, followed by any array of the rest. O(10 n) |
| `number_of_arrays_forward.kara` | the same count pushed forward over `to_digit` digits: from every i some array reaches, each number that starts there and fits carries ways[i] on to where it ends. O(10 n) |
| `number_of_arrays_memo.kara` | a recursion on the first number, each answer kept once found in a memo; at the constraints' most it recurses 10^5 calls deep. O(10 n) |
| `number_of_arrays_window.kara` | the backward count kept in a ring of the last 11 entries, indexed modulo 11. O(10 n), O(1) space |
| `number_of_arrays_solution.kara` | a Rust solution as LeetCode's Rust users write it (`const MOD`, `s.as_bytes()`, `vec![0i64; n + 1]`, the digit as `(s[j] - b'0') as i64`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's five examples and three
more (`1 0 8 1 34 1 0 1`); the constraints' most, 10^5 ones and 10^5
drawn digits, each with k at 10^9 and at 1000 (`10^5 digits: 98806521
111787461 175733372 0`); and 2000 random cases of 1 to 40 digits with k
up to 10, 10^4 or 10^9 (`2000 random cases: 828 with no array, checksum
379180156`). `number_of_arrays.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: every arm checks with warnings only as first written, and
`karac fix` clears them. The harness passed `ones.clone()` and
`big.clone()` to a parameter that only borrows them, 2 fixes in every
arm; the ★, memo and window arms widened a `u8` digit with `as i64`, and
the forward and memo arms `k` with `k as i64`, casts the widening makes
unneeded. The Rust solution takes one round of 13 fixes by `karac fix`'s
count: `struct Solution;` to `struct Solution {}`, `s.as_bytes()` to
`s.bytes()`, `vec![0i64; n + 1]` to `Vec.filled(n + 1, 0)`, the digit's
cast dropped, the harness's clones, and `Solution::` to `Solution.`. Its
`const MOD: i64 = 1_000_000_007;` and `let k = k as i64;` are taken as
written. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way to cut the digits into pieces, a cut or none after
each digit but the last, counted when every piece is a number from 1 to
k written with no leading 0, while the digits are at most 14. LeetCode's
examples, six edge cases (one digit, k exactly 10^9 and a number of 11
digits, k exactly the whole of s, a 0 that must join the digit before
it) and the constraints' most, 10^5 ones and 10^5 drawn digits, and 1990
random cases, 1 to 14 digits two times in three and up to 200 otherwise,
k up to 10, 1000 or 10^9.

The literal reading first parsed each piece with Rust's
`piece.parse::<i64>()`, written `parse::[i64]`; Kāra has no call-site
type arguments, and `karac fix` writes `i64.parse(piece)`, 2 fixes by
its count.

| | property |
|---|---|
| P1 | the statement read literally, while the digits are at most 14 |
| P2 | a count taken modulo 10^9 + 7 |
| P3 | ten 0s more at the end need a number of eleven digits, past any k, so no array is left |
| P4 | while no count wraps, a larger k, ten times or 10^9, allows every array it did |
| P5 | below 10 every number is one digit, so there is one array when every digit is from 1 to k and none otherwise |
| P6 | the ★ arm's answer |

All 46,895 checks pass on every arm: `2003 cases: checksum 348813474,
46895 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by `int()` of
each piece in a forward count, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a number allowed to start with 0 | P1 580, P3 1567, P5 93, P6 4788 |
| M2 | ★: the arrays after a number counted from its own last digit, not the one after it | P1 724, P5 73, P6 4704 |
| M3 | forward: a number of 10 digits never tried | P1 1, P6 1 |
| M4 | forward: a number allowed to start with 0 | P1 580, P3 1567, P5 93, P6 1197 |
| M5 | memo: nothing left counted as no array, where it is one | P1 724, P5 73, P6 1176 |
| M6 | memo: a number equal to k refused | P1 39, P5 27, P6 41 |
| M7 | window: nothing left counted as two arrays | P1 724, P5 73, P6 1176 |
| M8 | window: the leading 0 test made against `9` | P1 655, P3 1325, P5 80, P6 1253 |
| M9 | solution: no number allowed to run to the last digit | P1 724, P5 73, P6 1176 |
| M10 | solution: the numbers that start with 1 skipped, where those with 0 are | P1 628, P3 1285, P5 74, P6 1224 |

M8 first filled the ring with 1s in place of 0s. No slot past the end of
the digits is ever read, so that edit changes nothing, and it was
replaced.

## Benchmarks

The bench draws a pool of 2 * 10^5 digits, a 0 one time in 10 and never
two in a row, and runs the ★ arm on 100 windows of 10^5 of them, each
window's start and k drawn. Every implementation prints `100 windows of
10^5 digits: checksum 115245272`.

BENCHTAB

Kāra is level with Rust, C and Go here, measured by hand at 0.49 s each,
with Rust's overflow checks on or off.
