# 131. Palindrome Partitioning

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Backtracking · DP · String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/palindrome-partitioning](https://leetcode.com/problems/palindrome-partitioning/)

Return **all** ways to cut `s` into contiguous pieces such that every piece is a palindrome.

```
"aab"  ->  [["a","a","b"], ["aa","b"]]          (2 partitionings)
"aaaa" ->  8 partitionings
```

**Constraints:** `1 ≤ s.length ≤ 16`, lowercase.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Backtracking over palindromic prefixes** ★ | [`palindrome_partitioning.kara`](palindrome_partitioning.kara) ✓ | [`palindrome_partitioning.py`](palindrome_partitioning.py) ✓ |

`✓` runs end-to-end today: interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`) all agree with the Python mirror. Answers are validated against the known counts (aab 2, aaaa 8, single 1). Zero diagnostics, valgrind-clean.

## The mechanism

Backtrack from index `start`: for each `end ≥ start`, if `s[start..=end]` is a palindrome, push that piece onto the running `path`, recurse from `end + 1`, then pop (undo the choice). A complete cut is reached when `start` walks off the end. To keep the oracle deterministic without pinning a partition order, each complete cut contributes to a `count` and an **order-independent digest** (sum of per-partition hashes). The palindrome test is a two-pointer byte scan on the inclusive range; each piece is materialized as a fresh substring.

## Kāra features exercised

- **Backtracking with a `mut ref Vec[String]` path** — `push` a palindromic piece / recurse / `pop`; `count` and `digest` ride alongside as `mut ref` out-params (the same shape as [#126](../126-word-ladder-ii/)/[#124](../124-binary-tree-maximum-path-sum/), forwarded through recursion without a call-site marker).
- **Substring materialization** — `s[start..=end]` built char-by-char from `s.chars()`; each piece is an owned `String` pushed onto the path and freed on `pop`/scope exit (leak-clean on the `Vec[String]` path — the class `B-2026-07-18-52` closed).
- **Two-pointer palindrome test** over `s.bytes()` on an inclusive index range.

## Running

```bash
karac run   palindrome_partitioning.kara
karac build palindrome_partitioning.kara && ./palindrome_partitioning
python3 palindrome_partitioning.py
diff <(karac run palindrome_partitioning.kara) <(python3 palindrome_partitioning.py) && echo OK
```

## Notes

Dogfood-first backtracking kata (LeetCode caps `s.length` at 16, so the partition count is bounded), exercising `Vec[String]` backtracking snapshots + per-piece substring allocation across every surface.
