# 553. Optimal Division

You are given an integer array `nums`. The adjacent integers in `nums`
will perform the float division. For example, for `nums = [2,3,4]`, we
will evaluate the expression `"2/3/4"`. However, you can add any number
of parenthesis at any position to change the priority of operations. You
want to add these parentheses such the value of the expression after the
evaluation is maximum. Return the corresponding expression that has the
maximum value in string format. Note: your expression should not contain
redundant parenthesis.

```
nums = [1000, 100, 10, 2]  ->  "1000/(100/10/2)"
nums = [2, 3, 4]           ->  "2/(3/4)"
```

**Constraints:** `1 <= nums.length <= 10`, `2 <= nums[i] <= 1000`, and
there is only one optimal division for the given input.

## Approaches

Every arm is `fn optimal_division(nums: Vec[i64]) -> String`. The answer
always has one shape: the first number over the second divided by all
the rest in turn, a/(b/c/.../z), which is a c ... z / b. Every number is
at least 2, so putting each of c to z on top makes the value larger, and
b must stay below. The ★ and join arms write that shape down; the table
and memo arms search every bracketing and find it.

| file | mechanism |
|---|---|
| `optimal_division.kara` ★ | the shape built in one `String`, a number at a time with `push` and `push_str`, the brackets opened before the second number and closed at the end when there are more than two; O(n) |
| `optimal_division_join.kara` | every number formatted, then `parts[1..].join("/")` for the rest, bracketed when there are more than two; O(n) |
| `optimal_division_table.kara` | bottom-up over spans: for each span the largest and the smallest value as `f64` and the text that gives each, the last division split at every k; O(n^3) |
| `optimal_division_memo.kara` | the same recursion top-down, a `Map` keyed (i, j, largest or smallest) holding the value and its text; O(n^3) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 9 lines: the two examples, six arrays at the
edges (one number, two numbers, ten numbers rising and ten falling), and
a checksum over 300 random arrays. `optimal_division.py` mirrors the ★
arm and its output is byte-identical.

The join arm stops at type checking on every backend, legacy and
v2: `join` is not found on the `Slice[String]` that `parts[1..]` is
(kara B-2026-10-14-4). The arm keeps that spelling. A copy with
`parts[1..].to_vec().join("/")` prints the same output as the ★ arm
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every value the numbers can take under some full bracketing, worked out
exactly as fractions, and the largest of them. Each answer is read back
as an expression by a small parser and its value worked out the same
way. Each arm is held to the properties below on 1,000 random arrays of
distinct numbers: 1 to 5 from 2 to 6, 1 to 7 from 2 to 20, or 1 to
3 from 2 to 1000 in turn, sizes small enough that no product of the
fractions leaves `i64`.

| | property |
|---|---|
| P1 | the answer's value is the definition's |
| P2 | no brackets are redundant: dropping any one pair changes the value |
| P3 | the numbers in the answer are the input's, in order |
| P4 | there are n - 1 slashes |
| P5 | the value is at least that of the divisions left to right with no brackets |

Its copy of the join arm keeps `parts[1..].join("/")`, so it stops at
type checking on B-2026-10-14-4 as the arm does. A copy with `.to_vec()`
before the `join` prints `1000 cases, 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Thirteen edits to that copy of the differential, two to each arm that
change its answers, one that changes the work but not the answer, and
four that change nothing, each run under `karac __mir-run`. All eight
that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the bracket opened for two numbers as well | P1 224, P5 224 |
| M2 | ★: the bracket left open for three numbers | P1 211, P5 211 |
| M3 | join: three numbers taken as two | P1 211, P2 224, P3 211, P4 211 |
| M4 | join: no brackets around the rest | P1 534 |
| M5 | table: the right part bracketed even when it is one number | P2 758 |
| M6 | table: a span's smallest taken from the left part's largest | P1 193 |
| M7 | memo: the largest and the smallest swapped | P1 534 |
| M8 | memo: the left part searched for the other extreme | P1 197 |
| X1 | memo: the memo looked up as if the largest were wanted | 0 |
| E1 | ★: the closing bracket written `n >= 3` | 0 |
| E2 | join: two numbers or fewer, after one has returned | 0 |
| E3 | table: a later split taken on a tie for the largest | 0 |
| E4 | memo: the right part bracketed when j - k > 1 | 0 |

There are 224 cases of two numbers, 211 of three and 534 of three or
more. M1 and M2 leave a bracket unclosed, so the answer does not read
and fails P1 and P5 together. M3 brackets a lone second number when
there are two (P2) and drops the third number when there are three.
M5 is seen only by P2: its brackets are around one number, so the value
is right and the text is not. P3 and P4 see only M3, the one mutant that
loses a number.

X1 is a real change that no test can see. A lookup under the wrong key
hands back the largest value where the smallest was wanted, which only
makes a candidate worse; the best candidate is never one of those, so
the answer stands. E3 is safe because the problem promises one optimal
division, so there are no ties.

## Verification

The ★, table and memo arms print the same output as
`optimal_division.py` under `karac __mir-run` (the v2 MIR interpreter)
and `karac __mir-llvm-run`, and run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. `karac check` passes on those arms and the bench program. The join
arm and the differential stop at type checking on B-2026-10-14-4; their
`.to_vec()` copies pass all of the above.

The frozen legacy backends: the ★ and table arms print the same output
under `karac run --interp`, `karac run` and `karac build`, and under
`KARAC_AUTO_PAR=1 karac build`. The memo arm prints it under `karac run
--interp`; under `karac run` the JIT's module verification fails
("Function return type does not match operand type of return inst"), and
`karac build` exits 1 after an ownership warning that `nums` is moved
and used again. The differential also stops on `*b` over the bytes of a
`Vec[u8]` ("unary '*' requires 'ref T' ... found 'u8'"). Legacy is
frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 2,000 random arrays of 1 to
10 numbers from 2 to 1000 once, then answers every array 500 times over,
and folds the length of each answer and its middle byte into a checksum.
Every implementation prints `2000 arrays, 500 rounds each:
22281000 characters, checksum 290848146`, the Kāra program under `karac
__mir-run` included (10.3 s).

Each implementation builds the answer in one growing string as the Kāra
arm does: a `String` in Rust, a `strings.Builder` in Go, a list joined
at the end in Python, and in C a fresh `malloc`'d buffer that doubles as
it fills. Spot timings on a shared 4-core container, three runs each
(two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.28 to 0.29 s |
| Rust (`rustc -O`) | 0.26 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.27 to 0.34 s |
| Go | 0.21 s |
| Python | 0.91 to 0.94 s |
| Kāra (`karac build --mir`) | 0.40 to 0.44 s |

The legacy `karac build` refuses this program: it moves `all[(round *
7 + g) % count]` out of the index (E_INDEX_MOVE_NON_COPY) where
v2 borrows it. So `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`dc40f07098`. Under `karac __mir-llvm-run` the program prints the same
line in 3.9 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark. The Kāra row is about
1.6 times Rust's.

## Compiler findings

| id | status | what |
|---|---|---|
| B-2026-10-14-4 | open | `join` and `concat` on a `Slice[String]` (`parts[1..].join("/")`) fail type checking: the method is looked up only on a `Vec` or `VecDeque` receiver. The join arm and the differential keep the natural spelling; `.to_vec()` first passes. Recheck both once it is fixed. |
