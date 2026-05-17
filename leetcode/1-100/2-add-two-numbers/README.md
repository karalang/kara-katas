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

All three print `4000000` (500_000 × 8 — the units digit of 999…9 + 999…9 = 1999…98 is 8, and that's the first digit of the reversed-storage result).

### Codegen vs Rust — **landed**

Snapshot — M5 Pro (6 performance + 12 efficiency = 18 cores), 2026-05-17, hyperfine `--warmup 5 --runs 30 --shell=none`:

| Workload | Kāra (codegen) | Rust (Rc&lt;RefCell&gt;) | Python (CPython) | Kāra : Rust |
|---|---|---|---|---|
| `iterative` (N=100, K=500_000) | **832.7 ± 38.4 ms** | 883.1 ± 6.8 ms | 5.71 ± 0.09 s | **1.06× faster** |

Allocator-bound, RC-discipline-bound shape: a hot inner loop walking and growing a chain of small heap nodes, then recursively dropping the chain when the result goes out of scope. Kāra's `shared struct` does the same per-field recursive drop as Rust's `Rc<RefCell<>>` — both pay one rc-dec per node along the chain — and the ratio narrows to a modest 1.06× edge, driven by Kāra skipping `RefCell`'s runtime borrow check on each `borrow()` / `borrow_mut()`. Python runs the same shape in a tree-walking interpreter ~6.9× slower.

(An earlier snapshot of this kata reported 358 ms / 2.53× faster than Rust; that number measured the kernel correctly but the `karac` runtime was leaking the result chain on every iteration — peak RSS climbed to 2.3 GiB. After closing that leak in the Caveats Cluster 3 commits below — recursive drop on shared struct RC=0, plus Option[shared T] cleanup tracking — Kāra now does the same drop walk Rust does. The 1.06× number is the memory-correct apples-to-apples comparison; the 2.53× number was apples-to-leaky-apples.)

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

## Caveats surfaced while writing this kata

Six codegen bugs found and fixed in `karac` while writing this kata, across three sibling karac-rust commit clusters. The kata is the test case that surfaced and verifies each. All landed; none remain open.

### Cluster 1 — f-string cleanup discipline (`a345e15`)

1. **`s = f"{...{s}...}"` (or `let t: String = f"…"`) double-frees the heap buffer at scope exit.** The f-string accumulator's queued `FreeVecBuffer` fires on the same `data` pointer the LHS binding's cleanup also fires on, hanging in macOS `malloc_printf`. Fix: stage the acc alloca from the `InterpolatedStringLit` codegen and zero its `cap` in the consumer (Let / Assign for tracked Vec/String LHS), so its scope-exit free no-ops. The LHS slot becomes the unique owner. (Surfaced via the kata's `to_string` loop body `s = f"{s}{node.val}"`.)

2. **Function returning `f"…"` returned a struct with a dangling `data` pointer.** The acc's `FreeVecBuffer` fired during the function's scope-exit cleanup walk — which runs between the return-value load and the `ret` instruction — so the caller received `{data: freed, len, cap}`. Fix: the function-tail-return path also zeros the acc's `cap` (mirror of the Identifier-tail-return shape already handled by `suppress_cleanup_for_tail_return`). (Surfaced via the kata's `to_string` final expression `f"{s}]"`.)

### Cluster 2 — body-local shared-struct cleanup (`2bd2dba`)

3. **Body-local shared-struct lets corrupted the heap on the second call to any function that defined them in a control-flow sub-block.** Every `let node = ListNode { … }` inside a `for` / `loop` / `while` body queued an `RcDec` cleanup on the function-tail frame; when the enclosing block didn't execute (degenerate loop range, conditional branch not taken), the alloca held undef bytes at cleanup time and the dec deref'd into live malloc bookkeeping pages, hanging on the *next* allocation. Fix: nested-block shared-struct lets null-init their slot in the function entry block (so a never-executed `bind_pattern` leaves a known sentinel), and the cleanup walker's `RcDec` arm null-guards the dec. Additionally, `compile_for_range_with_step`, `compile_loop`, and `compile_while` now push a per-iteration scope frame around their body's `compile_block` and drain it before the back-edge / increment branch — so the body-local cleanups fire once per iteration instead of accumulating to function-tail. The two pieces work together: null-init covers the zero-iteration case; per-iter frame covers the iterate-and-clean case. (Surfaced via the kata's six-`report()` `main` aborting after the first output; minimal repro is `fn f() -> Option[Node] { for i in 1..1 { let x = Node { v: 99 }; } Some(...) }` from a caller that match-destructures.)

### Cluster 3 — Option[shared T] cleanup surface (`79a7db8` + `9cc1a74` + `53a6c4e` + `f541131`)

4. **`Option[shared T]` let-bindings didn't track for scope-exit cleanup, and `shared struct` RC=0 didn't recursively drop heap-bearing fields.** Two intertwined gaps that together caused the kata's bench to peak at 2.3 GiB at K=500_000 even though the runtime kernel was correct. A let-binding of `Option[ListNode]` didn't populate `shared_info` (so no `RcDec` queued), and even if it had, `emit_rc_dec`'s base case was a bare `free(ptr)` with no field walk — so dropping the chain head wouldn't propagate dec through the 99 transitive `next` nodes. Fix lands in `79a7db8`:
   - New `CleanupAction::RcDecOption` variant with discriminant-guarded inner-pointer dec (load tag, branch on Some, dec inner).
   - New `__karac_rc_drop_<Name>` per-shared-struct synth fn that walks heap-bearing fields (recursively, for `Option[shared T]` fields via the same discriminant guard) before `free`.
   - `Option[shared T]` Assign-arm refcount management (dec old inner, inc new inner unless fresh) — without this, `next_a = n.next;` in the recursive kata strands the old ref and use-after-frees on the next deref.
   - Tail-return defuse for `var.option_field` returns (`dummy.next`-style patterns) — recursive drop would otherwise walk the field and free the chain before the caller received it.

5. **`Option[shared T]` parameters didn't track at the callee, and call-site arg-passing didn't share the inner ref.** Follow-up in `9cc1a74`: parameter-binding loop registers `track_rc_option_var` for `Option[shared T]` params; call site emits a discriminant- and null-guarded `rc_inc` on the inner pointer for each `Option[shared T]` arg (mirror of `suppress_source_vec_cleanup_for_arg`'s shared-T branch). Caller's slot is unchanged across calls — multi-call patterns like the bench's K-loop preserve `l1` / `l2` identity. (An earlier shape used move semantics that zeroed caller args to None after each call; correctness regression caught by the bench's output dropping from `4000000` to `8` after one call.)

6. **`var.opt_field = X` field-store didn't dec the old Option-field ref or inc the new one.** Follow-up in `53a6c4e`: `compile_field_store` for an `Option[shared T]` field emits the 3-step dec-old / store-new / inc-new (if `!rhs_is_fresh`) IR. (Surfaced as a latent leak on `tail.next = Some(node); tail = node;`-style tail-chain construction inside loops.)

7. **Chained `call().opt_field` access on a function returning a struct with an `Option[shared T]` field didn't preserve ref discipline.** Follow-up in `f541131`: `compile_field_access`'s call-chain branch emits the same discriminant-guarded inc on the inner ptr BEFORE dec'ing the outer call temp, so the recursive drop's field dec is balanced. New case in `shared_option_info` detection for `FieldAccess` RHS whose object is a call-like or Identifier-bound shared struct.

### Validation

`cargo test --features llvm` passes (4500+ tests across codegen, parser, typechecker, effect, ownership, interpreter — no regressions across all three cluster slices); fmt and `clippy --all-targets --features llvm -- -D warnings` clean. The kata's six-test `main` runs end-to-end under both `karac run` and `karac build`; the bench at N=100, K=500_000 produces `4000000` with a bounded 1.5 MiB peak RSS.

**Typechecker warnings remain** (same shape as 133):

- `arithmetic operator requires numeric type, found 'String'` when concatenating `String`s with `+`. Worked around in this kata with `f"{s}{x}"` rather than `s + x`. The underlying gap is that the `+` operator isn't registered for `String`; either it should be (with explicit semantics — allocate a new String) or the diagnostic should be `String + String not supported, use f-string` instead of the generic arithmetic message.
- `no method 'to_string' on type 'String'` when calling `"literal".to_string()`. Worked around by just writing `"literal"` (String literals are already `String`). The original `to_string()` call was a defensive habit from Rust; in Kāra it's redundant.
