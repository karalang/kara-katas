# 895. Maximum Frequency Stack

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Hash Table, Stack, Design &nbsp;·&nbsp; **Source:** [leetcode.com/problems/maximum-frequency-stack](https://leetcode.com/problems/maximum-frequency-stack/)

`push(x)` adds an element; `pop()` removes and returns the **most frequent**
element, breaking ties toward the one pushed **most recently**.

```
push 5, 7, 5, 7, 4, 5     →  freq: 5→3, 7→2, 4→1
pop → 5    (only element with frequency 3)
pop → 7    (7 and 5 both at 2; 7 was pushed later)
pop → 5
pop → 4
```

**Constraints:** `0 ≤ x ≤ 10⁹`; at most `2·10⁴` calls; `pop` is only called on
a non-empty stack.

## Why this kata — a container nested in a container

The textbook solution keeps two maps and a running maximum:

| | |
|---|---|
| `freq: Map[i64, i64]` | live count per value |
| `buckets: Map[i64, Vec[i64]]` | for each frequency `f`, the values that reached `f`, in push order |
| `maxfreq` | largest `f` with a non-empty bucket |

`push` bumps `freq[x]` to `f` and appends `x` to `buckets[f]`; `pop` takes the
**last** element of `buckets[maxfreq]` — exactly the most-recent among the
most-frequent. Both are O(1).

That makes `Map[K, Vec[V]]` the point of the exercise: a container nested
inside a container, living on a struct, mutated through a `mut ref self`
method. It is the shape where a stale bucket handle or an over-eager temp drop
shows up as a **wrong sum** rather than a crash, which is why the stress driver
prints a checksum rather than just "ok".

## What it found

The idiomatic one-liner does not run:

```kara
self.buckets.entry(f).or_insert(Vec.new()).push(x);   // check passes, every backend fails
```

`karac check` accepts it; the interpreter then says *"method 'push' not found
on type 'unknown'"* and codegen says *"no handler for method 'push' on
non-identifier receiver"*. The same chain over a **local** map works
everywhere — the variable is the receiver's root being a struct **field**.
Filed as `B-2026-08-18-34`; `entry_chain_gap.kara` is the standing minimal
probe, with the working local and the failing field spelling side by side.

So `freq_stack.kara` uses the get/modify/insert round-trip instead. That is a
real canonical spelling, not a contortion to dodge the bug — but it copies the
bucket out and back, turning this problem's signature O(1) append into O(n).

## Files

| File | |
|---|---|
| `freq_stack.kara` | the kata, plus a 600-step deterministic stress |
| `freq_stack_explicit.kara` | the same algorithm with the bucket updated via an explicit `match` on `get` — the other canonical spelling, and a distinct lowering |
| `entry_chain_gap.kara` | standing probe for `B-2026-08-18-34` |
| `freq_stack.py` | the oracle mirror, same algorithm step for step |

Verified identical across `karac run --interp`, `karac run` (JIT), `karac
build`, and `KARAC_AUTO_PAR=0 karac build`, against the Python oracle —
including the stress checksum `5913`.
