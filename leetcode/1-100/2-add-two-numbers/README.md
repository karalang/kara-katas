# 2. Add Two Numbers

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Linked List, Math, Recursion &nbsp;·&nbsp; **Source:** [leetcode.com/problems/add-two-numbers](https://leetcode.com/problems/add-two-numbers/)

Two non-empty linked lists representing non-negative integers, digits stored in **reverse order** (least-significant first), one digit per node. Return the sum as a linked list in the same form. Lists may differ in length and the final carry can produce one extra leading digit.

**Constraints:** `1 ≤ digits in each list ≤ 100`, `0 ≤ Node.val ≤ 9`, leading digit non-zero unless the number is zero.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Iterative: walk both lists in lockstep, append digit-by-digit | O(max(m, n)) time, O(max(m, n)) space | [`iterative.kara`](iterative.kara) ✓ via `karac run` | [`iterative.py`](iterative.py) ✓ |
| Recursive: thread carry as explicit accumulator | O(max(m, n)) time, O(max(m, n)) space (stack) | [`recursive.kara`](recursive.kara) ✓ via `karac run` | [`recursive.py`](recursive.py) ✓ |

`✓ via karac run` means the interpreter path runs all six test cases end-to-end and matches the Python reference output line-for-line. The codegen path (`karac build`) is partially landed — see [Caveats](#caveats-surfaced-while-writing-this-kata) below for what's still blocking the bench.

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

**Status: blocked on the codegen bug noted in [Caveats](#caveats-surfaced-while-writing-this-kata) below.** Codegen runs through one full add-then-print cycle correctly; the second cycle hits a RC-drop / shared-struct scope-exit interaction that aborts the process. The bench harness is already laid out at `bench/` (Rust + Python files compile and run; the Kāra `bench/iterative.kara` would need a single-call-loop shape, which is straightforward once the multi-call scope-exit bug lands). Once that fix is in, the harness mirrors 121's shape — a single `bench.sh` invocation that builds with `karac build` + `rustc -O`, runs `hyperfine --warmup 5 --runs 30 --shell=none`, then prints binary size and peak RSS.

Sketch of the planned workload: `N = 100` digits per list × `K = 50_000` iterations of `add_two_numbers(l1, l2)` with a sum-of-first-digit sink (so the call's return value participates in I/O and can't be elided). The lists are built once outside the K-loop so the bench measures the addition kernel, not list construction.

## Caveats surfaced while writing this kata

Two codegen bugs found and fixed in `karac` while writing the kata:

1. **`s = f"{...{s}...}"` (or `let t: String = f"…"`) double-frees the heap buffer at scope exit.** The f-string accumulator's queued `FreeVecBuffer` fires on the same `data` pointer the LHS binding's cleanup also fires on, hanging in macOS `malloc_printf`. Fix: stage the acc alloca from the `InterpolatedStringLit` codegen and zero its `cap` in the consumer (Let / Assign for tracked Vec/String LHS), so its scope-exit free no-ops. The LHS slot becomes the unique owner.
2. **Function returning `f"…"` returned a struct with a dangling `data` pointer.** The acc's `FreeVecBuffer` fired during the function's scope-exit cleanup walk — which runs between the return-value load and the `ret` instruction — so the caller received `{data: freed, len, cap}`. Fix: the function-tail-return path now also zeros the acc's `cap` (mirror of the Identifier-tail-return shape already handled by `suppress_cleanup_for_tail_return`). Same `karac` slice as bug #1.

(Both surfaced via this kata's `to_string` helper, which uses both shapes: `s = f"{s}{node.val}"` in the loop and `f"{s}]"` as the function's final expression. Fixes live in `src/codegen/exprs.rs`, `src/codegen/stmts.rs`, `src/codegen/runtime.rs`, `src/codegen/functions.rs`. Test coverage: existing `cargo test --features llvm` suite passes; minimal repros captured in the karac-rust commit message.)

**Remaining codegen blocker (pre-existing, not introduced by this kata's fixes):**

3. **Calling a function that constructs + drops shared structs more than once aborts the second call.** Reduced from this kata's multi-`report()` `main` to a minimal: any function whose body builds a few `ListNode`s and lets them go out of scope at end-of-function corrupts the heap such that the *next* call's allocations trip a malloc invariant (SIGABRT) or hang in dyld notification. Single-call workloads (one `report(...)` in `main`) run end-to-end correctly under codegen. The Kāra interpreter path is unaffected — that's why all six test cases pass under `karac run`. Likely candidates from a quick read: per-iteration shared-struct drop walks the `next` chain too eagerly (frees the same node twice when the dummy-head's `next` aliases a node that's also tail-cursor reachable); or the post-cleanup ListNode alloca slot reuse picks up stale RC bytes. Not investigated further in this slice — surface is wider than the f-string scope, and the kata ships its correctness story via the interpreter.

**Typechecker warnings remain** (same shape as 133):

- `arithmetic operator requires numeric type, found 'String'` when concatenating `String`s with `+`. Worked around in this kata with `f"{s}{x}"` rather than `s + x`. The underlying gap is that the `+` operator isn't registered for `String`; either it should be (with explicit semantics — allocate a new String) or the diagnostic should be `String + String not supported, use f-string` instead of the generic arithmetic message.
- `no method 'to_string' on type 'String'` when calling `"literal".to_string()`. Worked around by just writing `"literal"` (String literals are already `String`). The original `to_string()` call was a defensive habit from Rust; in Kāra it's redundant.
