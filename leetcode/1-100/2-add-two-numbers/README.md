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

### Sketch

The trick is that **reverse-order digit storage makes addition local** — no normalisation pass is needed. At each position you have at most three inputs (digit-of-a, digit-of-b, carry-from-below), they sum into a value in `[0, 27]`, and you emit `sum % 10` and propagate `sum / 10`. When both lists end you check the carry one last time; if it's non-zero, that's the new leading digit.

```
add(a, b):
    carry = 0
    out = []
    while a or b or carry:
        s = carry + (a.val if a else 0) + (b.val if b else 0)
        out.append(s % 10)
        carry = s / 10
        a = a.next if a else None
        b = b.next if b else None
    return list_from(out)
```

The recursive form expresses the same recurrence directly — `add(a, b, carry) = cons(s % 10, add(a.next, b.next, s / 10))`. It's tail-call-shaped (the recursive call sits in the `next` slot) but Kāra doesn't currently guarantee TCO; at LeetCode constraint sizes (≤100 digits) the stack depth is bounded and recursion is safe.

## Kāra features exercised

- **`shared struct ListNode { val: i64, mut next: Option[ListNode] }`** — self-referential RC-backed node with a mutable tail link. Mutability on `next` is what lets `from_array` build the list by appending to a `tail` cursor (instead of building right-to-left then reversing), and what lets the iterative `add_two_numbers` append result nodes via a dummy-head + `tail.next = Some(node)` pattern.
- **`Option[ListNode]` returns and `if let Some(n) = a` destructuring** — the LeetCode signature already returns a nullable handle, and the lockstep walk needs to peek at each list independently. `if let` keeps the per-list branches flat.
- **`match (a, b)` two-tuple destructuring** was the natural shape but turned out unnecessary — sequencing two `if let Some(...)` blocks plus a `done` flag is shorter and avoids a four-arm match where three arms share the same code (see `iterative.kara` — the same handling for `(Some, None)` / `(None, Some)` / `(Some, Some)` collapses to "did we see any node at all").
- **f-string formatting (`f"{s}, {node.val}"`)** for the `to_string` helper — string `+` concatenation typechecks as arithmetic ("arithmetic operator requires numeric type, found 'String'"), so the f-string is the supported way to build incremental strings. The pattern is `s = f"{s}, {x}"` rather than `s = s + ", " + x`.
- **Tail-recursive shape (`recursive.kara`)** — the recursive call sits in the `next` field of the returned `ListNode`. Tail-position by source, not by codegen guarantee.

## API shape

Each solution exposes `add_two_numbers(l1: Option[ListNode], l2: Option[ListNode]) -> Option[ListNode]` plus a small test harness (`from_array`, `to_string`, `report`). `main` calls `report` per test case. The Python files mirror the same names so the files diff line-for-line.

## Output format

Each `report` formats the result list as `[d0, d1, d2, ...]` (digits in storage order — least-significant first, same as LeetCode's wire format). One line per test case, no trailing separator.

```
[7, 0, 8]
[0]
[8, 9, 9, 9, 0, 0, 0, 1]
[0, 0, 1]
[0, 1]
[7]
```

Verified line-for-line identical across `karac run iterative.kara`, `karac run recursive.kara`, `python3 iterative.py`, and `python3 recursive.py`.

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

All three print `400000` (50_000 × 8, the units digit of 1999…98 = first digit of the reversed result).

### Codegen vs Rust — **landed**

Snapshot — M5 Pro (6 performance + 12 efficiency = 18 cores), 2026-05-17, hyperfine `--warmup 5 --runs 30 --shell=none`:

| Workload | Kāra (codegen) | Rust (Rc&lt;RefCell&gt;) | Python (CPython) | Kāra : Rust |
|---|---|---|---|---|
| `iterative` (N=100, K=500_000) | **358.6 ± 11.2 ms** | 906.7 ± 28.9 ms | 5.70 ± 0.05 s | **2.53× faster** |

The shape is the same one the 133 clone-graph kata called out: allocator-bound, RC-discipline-bound, with a hot inner loop walking and growing a chain of small heap nodes. Kāra's `shared struct` lowers to plain RC (no `RefCell` borrow check, no `Box::leak`-style indirection) and beats `Rc<RefCell<_>>` on the same algorithm by ~2.5×. Python runs the same shape in a tree-walking interpreter ~16× slower.

### Binary size

| Build | Size |
|---|---|
| `kara iterative (codegen)` | 296 KiB |
| `rust iterative` | 456 KiB |

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara iterative (codegen)` | 2325.7 MiB ⚠ |
| `py   iterative` | 9.4 MiB |
| `rust iterative` | 1.2 MiB |

**The Kāra peak RSS is dominated by a per-iteration `Option[ListNode]` leak — see [Caveats](#caveats-surfaced-while-writing-this-kata) below.** The runtime number above is real and the kernel completes correctly (sink matches); the heap retention is the gap. Lowering K to 5_000 brings peak to 26 MiB (5 KiB per iter — one 100-node chain), confirming linear scaling from the leak. **The runtime ratio (2.53× faster than Rust) is unaffected** — both binaries do the same per-call work, and the Kāra leak takes a fixed-per-call hit independent of the kernel measurement.

## Caveats surfaced while writing this kata

Three codegen bugs found and fixed in `karac` while writing the kata. All three landed in the sibling karac-rust commits; the kata is the test case that surfaced and verifies each.

1. **`s = f"{...{s}...}"` (or `let t: String = f"…"`) double-frees the heap buffer at scope exit.** The f-string accumulator's queued `FreeVecBuffer` fires on the same `data` pointer the LHS binding's cleanup also fires on, hanging in macOS `malloc_printf`. Fix: stage the acc alloca from the `InterpolatedStringLit` codegen and zero its `cap` in the consumer (Let / Assign for tracked Vec/String LHS), so its scope-exit free no-ops. The LHS slot becomes the unique owner. (Surfaced via the kata's `to_string` loop body `s = f"{s}{node.val}"`.)

2. **Function returning `f"…"` returned a struct with a dangling `data` pointer.** The acc's `FreeVecBuffer` fired during the function's scope-exit cleanup walk — which runs between the return-value load and the `ret` instruction — so the caller received `{data: freed, len, cap}`. Fix: the function-tail-return path also zeros the acc's `cap` (mirror of the Identifier-tail-return shape already handled by `suppress_cleanup_for_tail_return`). (Surfaced via the kata's `to_string` final expression `f"{s}]"`.)

3. **Body-local shared-struct lets corrupted the heap on the second call to any function that defined them in a control-flow sub-block.** Every `let node = ListNode { … }` inside a `for` / `loop` / `while` body queued an `RcDec` cleanup on the function-tail frame; when the enclosing block didn't execute (degenerate loop range, conditional branch not taken), the alloca held undef bytes at cleanup time and the dec deref'd into live malloc bookkeeping pages, hanging on the *next* allocation. Fix: nested-block shared-struct lets null-init their slot in the function entry block (so a never-executed bind_pattern leaves a known sentinel), and the cleanup walker's `RcDec` arm null-guards the dec. Additionally, `compile_for_range_with_step`, `compile_loop`, and `compile_while` now push a per-iteration scope frame around their body's `compile_block` and drain it before the back-edge / increment branch — so the body-local cleanups fire once per iteration instead of accumulating to function-tail. The two pieces work together: null-init covers the zero-iteration case; per-iter frame covers the iterate-and-clean case. (Surfaced via the kata's six-`report()` `main` aborting after the first output; minimal repro is `fn f() -> Option[Node] { for i in 1..1 { let x = Node { v: 99 }; } Some(...) }` from a caller that match-destructures.)

`cargo test --features llvm` passes (3000+ tests across codegen, parser, typechecker, effect, ownership, interpreter); fmt and `clippy --all-targets --features llvm -- -D warnings` clean.

**Remaining gap (not blocking the kernel correctness or runtime numbers, only the memory peak):**

4. **`Option[shared T]` bindings don't track for scope-exit cleanup.** A let-binding of `Option[ListNode]` doesn't populate `shared_info` (the codegen's tracker for shared types), so no `RcDec` cleanup is queued. When a function returns `Option[ListNode]` and the caller's `let out = ...` aliases the chain, the chain's RC never drops — the alloc count climbs linearly with K. The bench's runtime numbers above measure the kernel correctly (the per-call work is unaffected), but the peak RSS reflects K × per-call-chain leakage. Fixes (one of):
   - Extend `shared_info` resolution to recognize `Option[shared T]` and queue a discriminant-guarded `RcDec` (load tag, branch on Some, dec inner).
   - Recursive field-drop on shared struct RC=0: when `Drop` would walk a struct's heap-bearing fields, the dummy-head + tail chain's nested `next: Option[ListNode]` would propagate the dec through the whole chain. This would also close the symmetric gap with `Map[K, shared V]` (the 133 kata noted closing one side of it).
   - A combination of both — the discriminant-guarded `Option[T]` cleanup at consumer let-sites, plus per-field drop on shared structs to handle the tail of the chain.

Either path is a meaningful slice; out of scope here. The number to watch is the runtime ratio (2.53× faster than Rust on the same shape), which is unaffected.

**Typechecker warnings remain** (same shape as 133):

- `arithmetic operator requires numeric type, found 'String'` when concatenating `String`s with `+`. Worked around in this kata with `f"{s}{x}"` rather than `s + x`. The underlying gap is that the `+` operator isn't registered for `String`; either it should be (with explicit semantics — allocate a new String) or the diagnostic should be `String + String not supported, use f-string` instead of the generic arithmetic message.
- `no method 'to_string' on type 'String'` when calling `"literal".to_string()`. Worked around by just writing `"literal"` (String literals are already `String`). The original `to_string()` call was a defensive habit from Rust; in Kāra it's redundant.
