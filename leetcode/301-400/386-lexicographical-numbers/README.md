# 386. Lexicographical Numbers

Given an integer `n`, return all the numbers from 1 to `n` sorted in
dictionary order, as their decimal texts would sort. The algorithm must
run in O(n) time and use O(1) extra space besides the answer.

```
n = 13  -> [1, 10, 11, 12, 13, 2, 3, 4, 5, 6, 7, 8, 9]
n = 2   -> [1, 2]
```

**Constraints:** `1 <= n <= 5 * 10^4`.

## Approaches

| file | mechanism | time | extra space |
|---|---|---|---|
| `lexical_order.kara` ★ | step from each number to the next: go one digit deeper (`cur * 10`) while that is at most n, otherwise drop trailing digits while the last is 9 or `cur + 1` passes n, then add one | O(n) | O(1) |
| `lexical_order_dfs.kara` | the numbers form a tree (roots 1 to 9, children `x * 10` to `x * 10 + 9`); dictionary order is its preorder, walked by recursion | O(n) | O(d) stack for d digits |
| `lexical_order_sort.kara` | write every number as text, sort the texts, read them back | O(n log n) string comparisons | O(n) strings |
| `lexical_order_stack.kara` | the same preorder with an explicit stack, children pushed from 9 down to 0 | O(n) | O(9 d) |
| `differential.kara` | the four arms for 412 values of n, five properties | — | — |

Every arm prints the same 16 lines: the full list for the two LeetCode
examples and for n = 1, 9, 10, 21 and 100, then for nine larger n
(99, 101, 199, 999, 1000, 4321, 9999, 10000 and 50000) the length, the
last number, whether the list holds each number once in dictionary
order, and a checksum. That check compares neighbours as decimal
strings with `<`. `lexical_order.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms as
`lexical_order_step`, `lexical_order_dfs`, `lexical_order_sort` and
`lexical_order_stack`, and runs them for every n from 1 to 400 and 12
random n up to 50,000. It checks dictionary order with an arithmetic
comparison that builds no strings: pad the shorter number with zeros to
the other's width; if the padded numbers differ, the smaller comes
first, and if they are equal the shorter does.

| | property |
|---|---|
| P1 | all four arms agree |
| P2 | the list holds every number from 1 to n exactly once |
| P3 | every neighbouring pair is in dictionary order |
| P4 | a number's position is the count of numbers from 1 to n before it in dictionary order, for 20 sampled numbers (5 when n is above 2,000) |
| P5 | the list for n is the list for n + 1 with n + 1 taken out (for every arm up to n = 2,000, and the stepping arm above) |

It prints `412 values of n, 16264 checks, 0 failures` under
`karac __mir-run`.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | how |
|---|---|---|
| M1 | step: does not go deeper to exactly n (`cur * 10 < n`) | P1 to P5, 589 failures |
| M2 | step: does not climb out after a 9 | P1 to P5, 8984 failures |
| M3 | dfs: children start at digit 1 | P1 and P2, 806 failures |
| M4 | dfs: the root equal to n is skipped (`x >= n`) | P1, P2 and P5, 27 failures |
| M5 | sort: leaves out n | P1, P2 and P5, 1224 failures |
| M6 | sort: never sorts | P1 and P3, 806 failures |
| M7 | stack: children ending in 9 are not pushed | P1 and P2, 788 failures |
| M8 | stack: children ending in 0 are not pushed | P1 and P2, 806 failures |

M1 only matters when n ends in 0, since only then is some `cur * 10`
equal to n, and M4 only when n is below 10, which is why the differential
walks every n up to 400 instead of sampling.

## Verification

All four arms print the same output as `lexical_order.py` under every
backend: `karac __mir-run` (the v2 MIR interpreter),
`karac __mir-llvm-run` (the same MIR compiled to LLVM),
`karac run --interp`, LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`. `karac check` passes on every file.
`differential.kara` prints the same line under `karac __mir-run` and
`karac __mir-llvm-run`. The legacy backends refuse it at its `*x` on
the items of `v.iter()` (`unary '*' requires 'ref T' ... found 'i64'`),
the frozen legacy typechecker gap katas 382 and 383 also hit; not filed.

## Benchmarks

The bench program uses the ★ arm for 6,000 values of n from 49,001 to
50,000 (the problem's limit), and folds each list into a checksum
through a position-weighted sum. Every implementation prints
`6000 lists, checksum 414127270`. Spot timings on a shared 4-core
container (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| Kāra, legacy `karac build` | 0.75 s |
| C (`clang -O3`) | 0.78 s |
| Rust (`rustc -O`) | 0.90 s |
| Go | 5.2 s |
| Kāra, `karac __mir-llvm-run` | 12.4 s |
| Python | 44 s |

`karac __mir-llvm-run` JITs the IR without LLVM's optimization passes,
through a debug-built runner, so its times show that the new backend
runs the program, not how fast it will be. Here every `push` is a call
into the runtime's `karac_mir_vec_push`: a loop of 300,000,000 pushes
alone takes 10.2 s that way.

## Compiler findings

None in the current compiler. The legacy typechecker's refusal of `*x`
on `Vec` iterator items is noted under Verification.
