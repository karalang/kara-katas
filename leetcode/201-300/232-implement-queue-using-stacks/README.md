# 232. Implement Queue using Stacks

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Stack · Queue · Design &nbsp;·&nbsp; **Source:** [leetcode.com/problems/implement-queue-using-stacks](https://leetcode.com/problems/implement-queue-using-stacks/)

Implement a FIFO **queue** (`push`, `pop`, `peek`, `empty`) using only LIFO **stack** operations — push to the back, pop from the back, peek the back.

```
push(1); push(2);
peek()  -> 1
pop()   -> 1
empty() -> false
```

**Constraints:** `1 ≤ value ≤ 9`, at most 100 calls; `pop`/`peek` only on a non-empty queue.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **two stacks (amortized O(1))** ★ | [`queue_using_stacks.kara`](queue_using_stacks.kara) | [`queue_using_stacks.py`](queue_using_stacks.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

This is the mirror image of [#225](../225-implement-stack-using-queues/), and the cleaner direction: two stacks, an **inbox** and an **outbox**. Pushes always land on the inbox. When the front is needed and the outbox is empty, **pour the entire inbox into the outbox** — popping the inbox reverses its order, so the oldest element ends up on top of the outbox, exactly where LIFO `pop`/`peek` will find it. Refilling only happens when the outbox drains, so each element is moved between the two stacks **at most once** across its lifetime: amortized O(1) per operation even though a single `pop` can occasionally be O(n).

## Kāra features exercised

- **Two-`Vec[i64]` struct** — a `MyQueue` holding an `inbox` and `outbox`, each used as a stack (`push` / `pop` → `Option`, matched); the fields are mutated only through method calls, so no `mut` field marker is needed.
- **`mut ref` vs `ref` split** — `q_push` / `q_pop` / `q_peek` take `mut ref MyQueue` (peek can trigger a refill) and are called with the `mut` marker; `q_empty` takes `ref` and needs none — the ownership checker enforces exactly this.
- **Amortized transfer loop** — the outbox-empty-guarded drain is the whole trick, expressed as a plain `while` over `pop`.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`19660772624544`). Workload: 75M LCG-driven push/pop/peek ops on the two-stack FIFO, size-bounded near 4096 (amortized refill exercised).

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-07-27 (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O` | 72.8 ms | 0.82× |
| C `clang -O3` | 73.4 ms | 0.83× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 74.9 ms | 0.85× |
| **Kāra (codegen)** | 88.4 ms | 1.00× |
| Go | 137.4 ms | 1.55× |

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   queue_using_stacks.kara
karac build queue_using_stacks.kara && ./queue_using_stacks
python3 queue_using_stacks.py
diff <(karac run queue_using_stacks.kara) <(python3 queue_using_stacks.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
