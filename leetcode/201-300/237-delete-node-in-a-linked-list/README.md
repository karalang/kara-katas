# 237. Delete Node in a Linked List

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Linked List &nbsp;·&nbsp; **Source:** [leetcode.com/problems/delete-node-in-a-linked-list](https://leetcode.com/problems/delete-node-in-a-linked-list/)

You are given **the node to delete** — not the head. Delete it from the list. The node is guaranteed not to be the last one.

```
[4,5,1,9], node = 5  ->  [4,1,9]
[4,5,1,9], node = 1  ->  [4,5,9]
[1,2],     node = 1  ->  [2]
```

**Constraints:** `2 ≤ nodes ≤ 1000`, `-1000 ≤ Node.val ≤ 1000`, all values distinct on LeetCode, and the given node is not the tail.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **copy successor + splice** ★ | [`delete_node.kara`](delete_node.kara) ✓ | [`delete_node.py`](delete_node.py) ✓ |
| shift values down, drop the tail | [`delete_node_shift.kara`](delete_node_shift.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`) and codegen (`karac build`) produce identical output, under the default auto-parallelising build and `KARAC_AUTO_PAR=0` alike, and both variants agree with the Python mirror on all seven cases.

## The mechanism

Every other linked-list deletion starts with `prev.next = node.next`. Here there is no `prev` and no way to reach one — you were handed a node in the middle of a list you cannot see the start of. The trick is to stop asking "how do I remove this node" and ask **"how do I make the list read as though it were removed"**:

```
node.val  = node.next.val      // become your successor
node.next = node.next.next     // and unlink it
```

The values a traversal sees are now exactly the values it would see if `node` had gone. O(1) time, O(1) space, no allocation.

**The node you were given always survives.** That is not an implementation detail, it is the whole shape of the problem: you can only rewrite memory you can reach, and the one thing you can reach is `node` itself. So the node that physically leaves the list is `node.next` — and any pointer someone else holds to *that* is now dangling at a node outside the list. The "delete" is a lie told to future traversals, which is also why it cannot work on the tail: there is no successor to impersonate.

The second variant pays O(n) to move the lie as far away as possible. It slides every following value back one slot and unlinks the **tail** instead, so the only node that stops being reachable is the last one. Same output, different casualty — worth writing because it makes the trade explicit, and because "which node actually dies" is the question an interviewer asks after the O(1) answer lands.

In the index-pool idiom this corpus uses for pointer structures (`Vec[Node]` with an `i64` `next`, `-1` = null), the casualty is visible as a pool slot: deleting slot 1 of `[4,5,1,9]` leaves slot 2 unreachable and slot 1 holding `1`, while the shift variant leaves slot 3 unreachable and slots 1–2 holding `1, 9`.

## Kāra features exercised

- **Index-pool singly-linked list** — `Vec[Node]` with an `i64` `next`. Both writes of the delete are struct-field assignments through an index (`nodes[node].val = nodes[succ].val`), each carrying a bounds check.
- **Two `mut` fields on one struct** — `mut val` as well as `mut next`; the ★ variant mutates both in the same statement pair, which the read-only-`next` katas ([#203](../203-remove-linked-list-elements/), [#206](../206-reverse-linked-list/)) never do.
- **`mut ref Vec[Node]`** threaded through the mutating `delete_node`, with `ref Vec[Node]` for the read-only `show`.
- **`ref Slice[i64]` forwarded to a bare `Slice[i64]` parameter** — `report` borrows (it is called seven times over six arrays, so `ref` is the only correct mode per `B-2026-07-01-10`) and hands the slice to a `build` that consumes it. This is the shape that found the compiler bug below.
- **`if`-expression** for the `next` link during build, and `Array[i64, N]` coercing into `ref Slice[i64]` with no copy.

## What it found

**One new compiler bug, `B-2026-07-30-18` (fixed, `ccf4053a`) — a silent miscompile with an out-of-bounds read in it.** Forwarding a `ref Slice[T]` or `ref Vec[T]` **parameter** into a callee that takes a **by-value** `Slice[T]` parameter passed `karac check` and then produced a bogus slice on every compiled surface while the interpreter was correct:

| | `--interp` | `karac run` (JIT) | `karac build` |
|---|---|---|---|
| `v.len()` on a 4-element slice | `4` | a stack address, different every run | `1073741824` |
| `v[1]` | `7` | `4` — the slice's own `len` field | spurious `vec index out of bounds` panic |

`coerce_to_slice`'s fast path read the payload straight out of the binding's alloca. That alloca *is* the `{ptr,len}` header for an owned local, but for a `ref` param it holds a **pointer to** the caller's header — so the load produced `{header_ptr, whatever sits next on the stack}`, which is why the length read as an address under the JIT (ASLR) and as a fixed adjacent stack word under AOT. With the data pointer pointing at the header itself, `v[1]` read the length field: an out-of-bounds read the JIT did not trap, and one the AOT bounds check turned into a panic on a perfectly valid index. A `Slice[String]` element printed garbage bytes.

Two things make it worth the entry. First, **the source is irrelevant** — an `Array` local, a `Vec` local and a `ref Vec[T]` forwarding param all reproduce — which is what separates it from the Array-header family (`B-2026-06-19-1`, `B-2026-07-30-3`, `B-2026-07-30-6`, all fixed): the defect was in how the *forwarding binding* is read, not in what it points at. `bare → bare` and `ref → ref` were always correct; it took a `ref` param feeding a by-value `Slice`. Second, **the shape is the plainest thing you can write** — a two-function kata where one function borrows and the other builds — which is exactly why an ordinary kata hit it before any probe did. The fix routes both arms through `get_data_ptr`, the accessor the sibling `ref`-argument path already used.

The kata as written is unchanged by the fix; it was never contorted around the bug.

## Benchmarks
<!-- bench-staleness -->
> **Figures in this section are a 2026-07-30 snapshot; the feed was last measured 2026-07-31.** Where the two disagree, [`bench/results.json`](bench/results.json) and the [charts](../../../BENCHMARKS.md) are current; the numbers below are kept because the analysis around them explains *why* the shape is what it is, and that reasoning outlives the milliseconds.

The kata's inputs are seven tiny lists, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go and Python, all agreeing on the sink (`306510976`). Workload: build an 8,000-node index-pool list once, then 7,000 cycles; each cycle relinks the pool into a single list and then sweeps it repeatedly, deleting every other node by the O(1) rule until one node is left and summing the survivors after every sweep. The sink is a rolling 30-bit polynomial hash of those per-sweep sums — a loop-carried dependency, so no cycle can be reordered or dropped. 168M inner iterations per run.

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-07-30 (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O` | 207.5 ms | 0.99× |
| Go | 209.8 ms | 1.00× |
| C `clang -O3` | 210.2 ms | 1.00× |
| **Kāra (codegen)** | 210.6 ms | 1.00× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 231.3 ms | 1.10× |

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`, karac `329b8e69d021`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

Binary size and peak RSS from the same run: Kāra 33.5 KiB / 1.1 MiB, C 32.7 KiB / 1.1 MiB, Rust 455.4 KiB / 1.2 MiB, Go 2434.1 KiB / 2.7 MiB — Kāra lands within 0.8 KiB of the C binary.

## Running

```bash
# Kāra — interpreter, JIT and codegen produce the same output today.
karac run   delete_node.kara
karac build delete_node.kara && ./delete_node

# The shift-down variant
karac run   delete_node_shift.kara

# Python
python3 delete_node.py

# Verify they agree
diff <(karac run delete_node.kara) <(python3 delete_node.py) && echo OK
diff <(karac run delete_node_shift.kara) <(python3 delete_node.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk) and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — with both Kāra variants agreeing with the Python mirror.

**A four-way dead heat, with Kāra ahead of Rust at equal safety.** Kāra, C, Go and wrapping Rust land inside 1.5% of each other; the only lane that separates is `rustc -O -C overflow-checks=on`, 10% behind the other four. Kāra pays approximately nothing for the checks Rust pays 10% for on this kernel — and the checks are real, not elided: the bench's exact accumulate shape (`pass = pass + nodes[k].val` over a pool of 2⁶² values) panics `integer overflow` under both `karac run` and `karac build`, so this is a codegen result and not skipped work.

Four checks that the measurement is a measurement:

- **The vectorizable loop is not the benchmark.** The per-cycle relink is the one loop an optimizer can vectorize, and an instrumented C build puts it at **3.2%** of runtime; the other 96.8% is the delete-and-traverse pointer chase, which is serial by construction (`cur = nodes[cur].next`).
- **It scales linearly.** Doubling and quadrupling the cycle count doubles and quadruples the time (Kāra 0.21 → 0.43 → 0.85 s), so nothing is being hoisted out.
- **The ratio is stable across those scales.** Kāra/C held at 1.00×, 0.98× and 1.00× over 7,000 / 14,000 / 28,000 cycles, so the dead heat is a property of the code rather than of one lucky run.
- **Auto-par never fires.** The default build and the `KARAC_AUTO_PAR=0` build are the same binary — identical SHA-256 — so the sequential lane is the whole story here and no parallel comparator is owed. The loop-carried sink is what forecloses it.

The Python mirror uses two parallel lists rather than a node object per slot; it is the interpreted scale lane, not a codegen comparator, and the object-per-node form would measure attribute lookup instead of the algorithm. The four compiled mirrors all use the same array-of-structs pool as the Kāra version.

The delete is written inline in all five mirrors rather than as a `delete_node` call. C, Rust and Go would each inline the equivalent function, so factoring it out would have turned the comparison into a question about inlining rather than about the delete.
