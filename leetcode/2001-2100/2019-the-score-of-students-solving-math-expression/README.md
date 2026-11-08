# 2019. The Score of Students Solving Math Expression

You are given a string `s` holding a valid expression of single digits
`0`-`9` joined by `+` and `*`, such as `3+5*2`. Its right answer is found by
doing every multiplication, left to right, and then every addition, left to
right. `n` students each gave an answer, `answers[i]`. A student whose
answer is the right one gets 5 points; a student whose answer could be had
by applying the operators in a wrong order, with correct arithmetic, gets 2
points; anyone else gets 0. Return the sum of the points.

```
s = "7+3*1*2", answers = [20,13,42]             ->  7
s = "3+5*2",   answers = [13,0,10,13,13,16,16]  ->  19
s = "6+0*1",   answers = [12,9,6,4,8,6]         ->  10
```

**Constraints:** `3 <= s.length <= 31`; `s` holds only digits and `+` and
`*`, alternating, at most 15 operators; every value in a right evaluation
is at most `2^31 - 1`; `1 <= n <= 10^4`; `0 <= answers[i] <= 1000`.

A wrong order is a bracketing of the expression, so the answers it can give
are the values of an interval DP: a run of digits takes every value of its
left part joined by the operator between them to every value of its right
part. Since no answer is above 1000, a value above 1000 can be dropped: it
can only reach an answer by `* 0`, and the shorter runs reach that 0 too.

## Approaches

| file | mechanism |
|---|---|
| `score.kara` ★ | the right answer read left to right, a running product closed into the sum at each `+`; the interval DP with each run's values in a `Set`, values above 1000 dropped. O(n^3 * 1000^2) at worst |
| `score_bits.kara` | the right answer as `s.split("+")` of `split("*")` products, through `i64.parse`; the interval DP over a `Vec[bool]` of 1001 flags per run, the walk of the right part stopped at the first value past 1000 |
| `score_memo.kara` | top-down: a run's values by recursion over the operator applied last, each run's sorted list kept in a `Map` from `(i, j)`; the right answer from a stack, a `*` folding into the top; answers found by `binary_search` |
| `score_brute.kara` | every order by plain recursion with no memo, each run worked out afresh wherever it occurs, values deduplicated by `contains`; the right answer by the same recursion split at the last `+`, else the last `*`. About O(3^n) |
| `score_sorted.kara` | the interval DP with each run's values in a `SortedSet`, the walk of the right part ended at the first value past 1000; the right answer by a `fold` over (sum so far, current term); the score by `filter` and `count` |
| `score_solution.kara` | LeetCode's Rust template (`use std::collections::HashSet`, a unit struct, `impl Solution`, `as_bytes()` and `b'0'`, `vec![vec![HashSet::new(); n]; n]`, `for len in 2..=n`, `for &x in &dp[i][k]`, a `&Vec` wrapper), carried by `karac fix` to a clean check |
| `differential.kara` | all six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: the answers for LeetCode's three
examples and four more; then the total and a checksum of the scores for
1500 expressions of 1 to 6 digits with 1 to 8 answers each, and for 6
expressions of 9 to 11 digits with 10000 answers each. The long ones stop
at 11 digits, not 16, for the brute arm's sake. `score.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the right answer by doing every `*` left to right and then
every `+`, and the wrong orders as every bracketing of the expression, by
recursion over the operator applied last, with values of any size kept. It
checks 700 problems of 1 to 6 digits from 0 to 1-9 and 1 to 8 answers,
each with even odds a value some bracketing gives, up to 1000, or a number
from 0 to 1-30. Every random choice of a problem (the expression, the
answers) is drawn before any arm answers.

| | property |
|---|---|
| P1 | the score is the statement read literally |
| P2 | the answers read in reverse order leave the score |
| P3 | every answer listed twice doubles the score |
| P4 | the expression written backwards leaves the score |
| P5 | `*1` appended to the expression leaves the score |
| P6 | each arm agrees with at least three of the other five |

P4 holds because `+` and `*` both commute: a bracketing of the expression
read backwards is the mirror image of one read forwards, with the same
value, and the right answer is a sum of the same products. P5 holds because
`* 1` changes no value it is applied to.

The differential prints `700 problems: checksum 667929190, 25200 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Fifteen are kept, two or
three to each arm. All thirty are killed, each fails the same way under
both backends, none by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last term never added | P1 367, P4 127, P6 367 |
| M2 | ★: values kept only up to 100 | P1 26, P6 26 |
| M3 | bits: the left part read at its first value only | P1 4, P4 6, P6 4 |
| M4 | bits: the operator read at the run's start | P1 113, P4 114, P5 37, P6 113 |
| M5 | bits: no left value of 0 tried | P1 46, P4 54, P5 9, P6 46 |
| M6 | memo: the memo keyed by the run's start alone | P1 140, P4 130, P5 71, P6 140 |
| M7 | memo: a `*` pushing a new term | P1 420, P5 271, P6 420 |
| M8 | brute: the right answer's left part read as its last digit | P1 246, P4 159, P5 84, P6 246 |
| M9 | brute: the right part one digit long | P1 134, P4 137, P6 134 |
| M10 | brute: a lone 0 giving no value | P1 72, P6 72 |
| M11 | sorted: a right answer counted only once | P1 370, P3 552, P6 370 |
| M12 | sorted: the digit read one place early | P1 480, P4 101, P5 112, P6 480 |
| M13 | Rust: the stack summed without its first term | P1 373, P4 127, P6 373 |
| M14 | Rust: the first digit left out of the table | P1 141, P6 141 |
| M15 | Rust: every answer in the set scoring 2, the right one too | P1 552, P6 552 |

P1 and P6 kill all fifteen, P4 nine, P5 six, P3 one and P2 none. P4 writes
the expression backwards, which sends its first digit to the end and its
last to the start, so it sees every edit that treats the two ends of the
expression or of a run unevenly: the first or last term lost (M1, M13), the
left part of a split read short or at one value (M3, M8, M9), the operator
or digit read at the wrong place (M4, M12), a memo that confuses runs with
the same start (M6), and 0 tried on one side only (M5). It misses the edits
that treat both ends alike: a cap, a lost 0 digit, a lost run of one digit
(M2, M10, M14), a `*` read as `+` in the right answer (M7), and the
scoring edits (M11, M15). P5 appends `*1`, which multiplies a value by 1
and so changes nothing, but it adds a split at the end and a factor to the
last term; it sees the edits that let that split or factor count: the
right answer's terms broken at a `*` (M7, M8), an operator or digit read
from a neighbour (M4, M12), a memo that reads a run by its start (M6), and
0 never tried as a left value (M5). P3 lists every answer twice, which
doubles every score unless an edit counts a right answer only once (M11).
P2 reverses the answers, and no edit reads them in order.

The other fifteen fail as a kept one does, or with counts of their own.
The ★ arm's product reset at a `*` fails as the Rust arm's `*` replacing
the top of its stack (P1 196, P4 162, P5 358); the ★ arm's last split never
tried as M14; the ★ arm scoring a right answer 2 as well as M15; the bits
arm's right answer with `+` bound before `*` as the brute arm splitting the
right answer at its last `*` first (P1 102); the bits arm's operator at the
run's start as the Rust arm's (M4). The bits arm reading the whole
expression's flags from its first digit, the memo arm's left part a digit
short, its `binary_search` off by one and a value of 0 never kept, the
brute arm trying only the first operator as the outermost, and the sorted
arm's last term counted twice when it is the only one, its walk stopped
past 500 and a `+` read as `*` in its fold fail with counts of their own.
Seven drafts were replaced. When the differential drew its answers only
from 0 to 30, five edits around the cap of 1000 never failed, nor did the
brute arm keeping a repeated value, nor the right answer split at its
first `+`, which is the same sum. And the memo arm leaving its values
unsorted failed differently on the two backends: its `binary_search` then
reads a list in the `Set`'s hash order, which is random per process, so
that is the kata's nondeterminism, not a compiler fault. The differential
now draws half its answers from the values some bracketing gives, up to
1000. The cap at 100 then failed and was kept; the bits arm's walk going on
past 1000 instead of stopping still never failed, since it stores nothing
past 1000 either way; and that edit and the other six were replaced.

## Verification

Every arm prints the same output as `score.py` under `karac __mir-run` (the
v2 MIR interpreter), `karac __mir-llvm-run`, and `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer) with no error. `karac run` and a
`karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 0.56 s (Rust) to 9.6 s (bits) and the
differential 30 s.

The five arms were written in Kāra and checked clean, with no fix.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` alone, in four rounds (26, 3, 3 and 3 edits). The
first carries the struct, the `Vec<..>` and `HashSet<..>` types, the `::`
paths, `2..=n`, the `&` patterns and `&dp[i][k]`, and drops the `use`; the
second renames `HashSet` to `Set`, which the resolver reports only once the
`use` is gone; the third turns `as_bytes()` into `bytes()`, the plain
`vec![..]` into a list literal and the inner `vec![Set.new(); n]` into
`Vec.filled(n, Set.new())`; the fourth does the outer one, which held the
inner as its element and so could not be rewritten in the same round, and
drops the wrapper's `ref`s. `let mut ans = 0` returned as the method's
`i32` checks: a return fixes a literal's type (design.md §8).

## Benchmarks

The bench builds 200 expressions of 16 digits, the most the constraints
allow, with 2000 answers up to 1000 each, once in all five languages, and
runs the ★ arm on each for 10 rounds: 2000 calls. Every implementation
prints `2000 calls: 2137150 points, checksum 857862506`. Every language
keeps each run's values in a hash set of its own (C with a small open
addressing table), as the Kāra program does.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 0.753 to 0.789 s | 0.766 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.759 to 0.841 s | 0.773 s |
| C (`clang -O3`) | 0.832 to 0.906 s | 0.851 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.930 to 1.044 s | 0.962 s |
| Kāra (`karac build`) | 0.928 to 1.022 s | 0.970 s |
| Go | 1.861 to 1.985 s | 1.953 s |
| Python | 4.5 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.964 s) is not above its real time (0.970 s).

The sequential Kāra program is 1.25x Rust under overflow checks and 1.13x
C.