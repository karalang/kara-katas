# 241. Different Ways to Add Parentheses

Given an arithmetic expression of non-negative integers and the operators `+`,
`-`, `*`, return every value obtainable by parenthesizing the expression in a
different way.

## Approach

Divide and conquer on each operator. Treating operator `k` as the **last** one
evaluated splits the expression into an independent left and right part; recurse
to enumerate *all* values each part can take, then combine every left value with
every right value under operator `k`. A run of digits with no operator is a
single leaf value.

The expression is tokenized (a byte scan) into an interleaved `Vec[i64]` —
numbers at even positions, operator codes at odd — so the recursion works over
token indices. Results are sorted (`Vec[i64].sort()`) for a deterministic,
oracle-comparable line.

## Files

- [`diff_ways.kara`](diff_ways.kara) — Kāra implementation.
- [`diff_ways.py`](diff_ways.py) — Python mirror (oracle).

Expected output (both):

```
0 2
-34 -14 -10 -10 10
11
7 9
24 24
```
