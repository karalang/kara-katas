# 2. Add Two Numbers

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Linked List, Math, Recursion &nbsp;·&nbsp; **Source:** [leetcode.com/problems/add-two-numbers](https://leetcode.com/problems/add-two-numbers/)

Two non-empty linked lists representing non-negative integers, digits stored in **reverse order** (least-significant first), one digit per node. Return the sum as a linked list in the same form. Lists may differ in length and the final carry can produce one extra leading digit.

**Constraints:** `1 ≤ digits in each list ≤ 100`, `0 ≤ Node.val ≤ 9`, leading digit non-zero unless the number is zero.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Iterative: walk both lists in lockstep, append digit-by-digit | O(max(m, n)) time, O(max(m, n)) space | [`iterative.kara`](iterative.kara) ✓ | [`iterative.py`](iterative.py) ✓ |
| Recursive: thread carry as explicit accumulator | O(max(m, n)) time, O(max(m, n)) space (stack) | [`recursive.kara`](recursive.kara) ✓ | [`recursive.py`](recursive.py) ✓ |

`✓` runs end-to-end today under both `karac run` and `karac build`.

## Why both?

Reverse-order digit storage makes addition local — no normalisation pass is needed. At each position you have at most three inputs (digit-of-a, digit-of-b, carry-from-below) summing into `[0, 27]`; emit `sum % 10`, propagate `sum / 10`. The iterative form expresses this with a dummy-head + `tail` cursor; the recursive form expresses the same recurrence directly as `add(a, b, carry) = cons(s % 10, add(a.next, b.next, s / 10))`. Recursive is tail-call-shaped but Kāra doesn't currently guarantee TCO — at the ≤100-digit constraint, stack depth is bounded and either is safe.

## Kāra features exercised

- **`shared struct ListNode { val: i64, mut next: Option[ListNode] }`** — self-referential RC-backed node with a mutable tail link, enabling left-to-right list construction via a `tail` cursor.
- **`Option[ListNode]` + `if let Some(n) = a`** — flat per-list peek without a four-arm `match (a, b)` (three of those arms would share code).
- **f-string accumulation (`s = f"{s}, {node.val}"`)** — `String + String` doesn't typecheck (registered as arithmetic); f-string is the supported incremental-string idiom.
- **Tail-recursive shape in `recursive.kara`** — recursive call sits in the `next` field; tail-position by source, not by codegen guarantee.

## Running

```bash
# Kāra (interpreter — works today)
karac run iterative.kara
karac run recursive.kara

# Python
python3 iterative.py
python3 recursive.py
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup) and karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust file with `rustc -O` and the Kāra file with `karac build` (both cached in `bench/target/`, gitignored), then runs `hyperfine --warmup 5 --runs 30 --shell=none` across three implementations on N=100-digit lists, K=500_000 iterations:

| File | What it does |
|---|---|
| [`bench/iterative.kara`](bench/iterative.kara) | N=100 nine-digit lists built once; K=500_000 iterations of `add_two_numbers(l1, l2)` with sum-of-first-digit sink so the result participates in I/O. |
| [`bench/iterative.py`](bench/iterative.py) | Algorithmic mirror — same N, K, sink |
| [`bench/iterative.rs`](bench/iterative.rs) | Algorithmic mirror; uses `Rc<RefCell<ListNode>>` to mirror Kāra's `shared struct` reference semantics; compiled with `rustc -O` |

All three print `4000000` (500_000 × 8 — the units digit of 999…9 + 999…9 = 1999…98 is 8, and that's the first digit of the reversed-storage result).

### Codegen vs Rust — **landed**

Snapshot — M5 Pro (6 performance + 12 efficiency = 18 cores), 2026-05-17, hyperfine `--warmup 5 --runs 30 --shell=none`:

| Workload | Kāra (codegen) | Rust (Rc&lt;RefCell&gt;) | Python (CPython) | Kāra : Rust |
|---|---|---|---|---|
| `iterative` (N=100, K=500_000) | **832.7 ± 38.4 ms** | 883.1 ± 6.8 ms | 5.71 ± 0.09 s | **1.06× faster** |

Allocator-bound, RC-discipline-bound shape: a hot inner loop walking and growing a chain of small heap nodes, then recursively dropping the chain when the result goes out of scope. Kāra's `shared struct` does the same per-field recursive drop as Rust's `Rc<RefCell<>>` — both pay one rc-dec per node along the chain — and the ratio narrows to a modest 1.06× edge, driven by Kāra skipping `RefCell`'s runtime borrow check on each `borrow()` / `borrow_mut()`. Python runs the same shape in a tree-walking interpreter ~6.9× slower.

(An earlier snapshot of this kata reported 358 ms / 2.53× faster than Rust; that number measured the kernel correctly but the `karac` runtime was leaking the result chain on every iteration — peak RSS climbed to 2.3 GiB. After closing that leak — recursive drop on shared struct RC=0, plus Option[shared T] cleanup tracking — Kāra now does the same drop walk Rust does. The 1.06× number is the memory-correct apples-to-apples comparison; the 2.53× number was apples-to-leaky-apples.)

### Binary size

| Build | Size |
|---|---|
| `kara iterative (codegen)` | 296 KiB |
| `rust iterative` | 456 KiB |

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara iterative (codegen)` | 1.5 MiB |
| `py   iterative` | 9.5 MiB |
| `rust iterative` | 1.2 MiB |

Peak RSS is bounded and comparable to Rust's. Lowering K does not significantly affect peak (the runtime keeps one 100-node chain live at any time).
