# 474. Ones and Zeroes

You are given an array of binary strings `strs` and two integers `m`
and `n`.

Return the size of the largest subset of `strs` such that there are at
most `m` `0`'s and `n` `1`'s in the subset.

A set `x` is a subset of a set `y` if all elements of `x` are also
elements of `y`.

```
strs = ["10","0001","111001","1","0"], m = 5, n = 3  ->  4   ({"10","0001","1","0"})
strs = ["10","0","1"], m = 1, n = 1                  ->  2   ({"0","1"})
```

**Constraints:** `1 <= strs.length <= 600`; `1 <= strs[i].length <=
100`; `strs[i]` consists only of digits `'0'` and `'1'`; `1 <= m, n <=
100`.

## Approaches

Every arm is `fn find_max_form(strs: Vec[String], m: i64, n: i64) ->
i64`, and borrows the list. Each string costs its zeros from one budget
and its ones from the other, and is worth 1: a knapsack with two
weights.

| file | mechanism |
|---|---|
| `ones_and_zeroes.kara` ★ | one table `best[i][j]`, the most strings that fit in i zeros and j ones so far; each string updates it with the budgets going down, so it is counted at most once. O(strings × m × n) |
| `ones_and_zeroes_table.kara` | the full table, one layer per string: the most of the first k strings for every budget, from layer k - 1. O(strings × m × n) time and space |
| `ones_and_zeroes_memo.kara` | take or leave string k with z zeros and o ones left, each `(k, z, o)` worked out once and kept in a `Map[(i64, i64, i64), i64]` |
| `ones_and_zeroes_groups.kara` | the strings counted per (zeros, ones) pair in a `Map[(i64, i64), i64]`, then each pair taken 0 to its count times (a bounded knapsack); the map's order does not change the answer |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

The arms count zeros three ways: a `for` loop over `chars()`, a
`chars().filter(..).count()`, and a loop over `bytes()`.

Every arm prints the same 9 lines: the two LeetCode examples, the second
with no budget, three zeros against a budget of two, three copies of
`1000` that fill both budgets beside a `111` that would also fit alone,
two strings with more zeros than the budget of one, four strings that
fit exactly, a single 1 with no zeros, and for 300 random cases (1 to 20
strings of 1 to 8 digits, each leaning to zeros, to ones, or neither;
`m` and `n` from 0 to 12) the number of strings, the total of the
answers, and a checksum of them in order. `ones_and_zeroes.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases: 1 to 10 strings of 1 to 6 digits, `m` and `n` from
0 to 8.

| | property |
|---|---|
| P1 | the arm's answer is the most strings of any subset that fits, every one of the 2^k subsets tried |
| P2 | the same strings in another order give the same answer |
| P3 | one more zero (or one more one) in the budget raises the answer by 0 or 1 |
| P4 | one more string raises the answer by 0 or 1 |
| P5 | every digit flipped, with `m` and `n` swapped, gives the same answer |

P3 and P4 hold because taking one string out of the bigger answer
leaves a set that fits the smaller problem.

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, in 8 to 9 s, and a count for each property when
anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the budgets go up, so a string can be taken again | P1 674, P4 95, P5 681 |
| M2 | ★: a string never uses up the last of the ones | P1 413, P3 14, P5 563 |
| M3 | table: a string that uses exactly the zeros left is not taken | P1 404, P3 18, P5 563 |
| M4 | table: the string adds to its own layer, so it can be taken again | P1 921, P4 159 |
| M5 | memo: the remembered answer is looked up with the budgets swapped | P1 29, P2 36, P3 8 |
| M6 | memo: a one is counted as a zero and a zero as a one | P1 645 |
| M7 | groups: one copy fewer than the count may be taken | P1 1254 |
| M8 | groups: the budgets go up, so a group can be taken past its count | P1 674, P4 95, P5 681 |

M1 and M8 turn their arms into the same unbounded knapsack, and fail
the same cases. M2 and M3 are the same edge, one in each budget; P5
catches both, since flipping the digits moves the edge to the other
budget, where the arm is right. M6 and M7 are caught by P1 alone: M6
answers the flipped problem, which P5 cannot tell from the real one,
and M7 is consistent under every change P2 to P5 make. M5 is the
weakest; a lookup under the swapped budgets is wrong only when that
state was worked out first and differs.

## Verification

All four arms print the same output as `ones_and_zeroes.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file, the bench program included. The
differential prints `30000 checks, 0 failures` on both. The four arms
and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

On the frozen legacy backends the differential runs and passes under
`karac run --interp` and legacy `karac build`. The arms do not:
`karac run --interp` has no `String.as_str` (the harness prints with
it), and LLJIT and legacy `karac build` both stop on `as_str` in their
code generator. Legacy also reads a bare parameter as owned and warns
on every second use (`value 'strs' moved here, used again here`), but
only warns. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 600 strings (the problem's
most) of 1 to 100 binary digits once, each leaning to zeros, to ones,
or neither as in the harness, then runs 300 rounds with `m` and `n`
from 50 to 100. Every implementation prints `300 rounds on 600 strings:
10981 chosen, checksum 402717894`, the Kāra program under
`karac __mir-run` included (in 698 s).

Every mirror keeps one table of `(m + 1) × (n + 1)` counts per round
(rows of a `Vec` in Rust and Go, one flat block in C), counts each
string's zeros with a loop over its characters, and runs both budgets
from the top down. Spot timings on a shared 4-core container, three
runs each (two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.30 to 0.31 s |
| Rust (`rustc -O`) | 0.48 to 0.53 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.70 to 0.77 s |
| Go | 0.76 to 0.82 s |
| Python | 23.8 to 24.4 s |
| Kāra (`karac build`) | 0.80 to 0.82 s |
| Kāra (`karac build --mir`) | 1.06 to 1.11 s |

The legacy `karac build` builds this program (it has no `as_str`), so
`bench.sh` is the `scripts/new-bench.sh` output unchanged and times that
build. The `--mir` row is the v2 compiled backend, timed for comparison.
Both Kāra rows are timed at kara `b0b1557b39`. Under `karac
__mir-llvm-run` the program prints the same line in 10 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

## Compiler findings

No new findings. `s.chars().filter(|c| *c == '0').count()` is refused
by `karac check` ("found 'char'") and runs on the MIR backends; per
docs/library/iterators.md a predicate gets its item as a bare
`Self.Item`, a `char` copy here, so `c == '0'` is the spelling the
arms use. Which of the two is right is the open question in
B-2026-10-13-6.
