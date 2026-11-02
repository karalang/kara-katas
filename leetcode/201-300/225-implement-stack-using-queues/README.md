# 225. Implement Stack using Queues

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Stack · Queue · Design &nbsp;·&nbsp; **Source:** [leetcode.com/problems/implement-stack-using-queues](https://leetcode.com/problems/implement-stack-using-queues/)

Implement a LIFO **stack** (`push`, `pop`, `top`, `empty`) using only **FIFO queue** operations — enqueue at the back, dequeue from the front, peek the front, size, empty.

```
push(1); push(2);
top()   -> 2
pop()   -> 2
empty() -> false
```

**Constraints:** `1 ≤ value ≤ 9`, at most 100 calls; `pop`/`top` are only called on a non-empty stack.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **single queue, costly push** ★ | [`stack_using_queues.kara`](stack_using_queues.kara) | [`stack_using_queues.py`](stack_using_queues.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

A queue hands back its **oldest** element first; a stack needs its **newest**. The gap is closed at push time. After enqueuing a new value at the back, **rotate** the queue — dequeue and re-enqueue every other element — so the value just pushed circles around to the **front**. Now the queue's front always holds the most-recently pushed value, which is exactly stack order, so `pop` and `top` are just the queue's front operations. `push` is O(n); `pop`, `top`, and `empty` are O(1).

The underlying queue is an index-pool FIFO: a `Vec[i64]` with a `head` cursor — dequeue advances `head`, enqueue pushes at the back.

## Kāra features exercised

- **Layered structs + free functions** — a `Queue` struct (`Vec[i64]` + `mut head`) with `q_enqueue` / `q_dequeue` / `q_front` / `q_size` / `q_empty`, and the stack ops built on top, the corpus's impl-block-free design.
- **`mut ref` mutation discipline** — `stack_push` / `stack_pop` take `mut ref Queue` (they mutate) and are called with the `mut` marker on the owned binding (`stack_pop(mut s)`); `stack_top` / `stack_empty` take `ref Queue` (read-only) and need no marker. The compiler enforces exactly this split.
- **Mutable struct field** — `head` is `mut` (reassigned on dequeue); `data` is mutated only through `push` (no `mut` needed for a method-call mutation of a field).

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`451784582`). Workload: PRNG-driven push/pop/top sequence on the queue-backed stack (O(n) costly-push rotations).

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-11-02, karac g6697158fa (0.9.0-dev.14057, the v2/MIR backend) (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 97.2 ms | 0.59× |
| Rust `-O` | 133.4 ms | 0.81× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 150.1 ms | 0.91× |
| **Kāra (codegen)** | 165.6 ms | 1.00× |
| Go | 1128.8 ms | 6.81× |

Against the 2026-07-28 legacy-backend run, Kāra regressed about 1.55× against Rust and C: Kāra/Rust `-O` 0.80× → 1.24×, Kāra/equal-safety Rust 0.70× → 1.10×, Kāra/C 1.09× → 1.70×, Kāra/Go 0.12× → 0.15×. In that run Kāra was ahead of both Rust rows (1.25× faster than `rustc -O`); that was true of the legacy backend on 2026-07-28 and is no longer the result — Kāra now trails both Rust rows and C, and stays well ahead of Go only. Every comparator also ran slower this session, so compare the ratios, not the milliseconds. On the v2/MIR backend the kernel executes 1.43× legacy dd86e3955's instructions and 1.61× its cycles in the queue-rotation loop, tracked as [`B-2026-11-02-2`](../../../../kara/docs/bugs-v2.md) (see [Bug ledger](#bug-ledger)).

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`, karac g6697158fa); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   stack_using_queues.kara
karac build stack_using_queues.kara && ./stack_using_queues
python3 stack_using_queues.py
diff <(karac run stack_using_queues.kara) <(python3 stack_using_queues.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Benchmarked: see § Benchmarks.

## Bug ledger

**Surfaced [`B-2026-11-02-2`](../../../../kara/docs/bugs-v2.md)** (perf, medium, open). On the v2/MIR backend the `bench/` Kāra program executes 1.43× legacy dd86e3955's instructions and 1.61× its cycles (`KARAC_AUTO_PAR=0`): the seq lane went from 0.80× to 1.24× `rustc -O`, 1.09× to 1.70× C and 0.12× to 0.15× Go. The hot loop is `stack_push`'s queue rotation — each iteration a `q_dequeue` (index read plus `head` field update) and a `q_enqueue` (`Vec` push) through a `mut ref Queue`. Measured 2026-11-02 with karac g6697158fa.
