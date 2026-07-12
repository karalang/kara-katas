# RC-elision for read-only borrow parameters (`KARAC_RC_ELIDE_REF_PARAMS`)

**Status: SPIKE — NOT landed.** The win is proven and a whole-program call-site
guard makes the *caller* side sound, but Linux LSan surfaced that the ownership
pass's `Ref` classification is an insufficient certificate on the *callee* side
(it permits callee-side consumption — see "Why the `Ref`-gated version is
unsound"). A truly sound version needs a callee-side purity analysis (below).
The code lives as a patch, not on `main`; the flag stays OFF and unshipped until
the callee-side blocker is closed and Linux LSan is clean.

## The gap

The ownership pass classifies a parameter that is only read (never mutated,
consumed, or escaped) as `OwnershipMode::Ref` — a borrow. For a `shared` /
`Option[shared]` such param, codegen nonetheless emits the caller-side retain
(`rc_inc`) at the call site and the callee-side release (`rc_dec`) at scope
exit. The analysis already *says* these are borrows — `karac query ownership`
reports `mode: ref`, and `karac query cost-summary` reports **0 rc_ops** for the
function — but codegen never consumed `OwnershipCheckResult::param_modes`; it
decided retain/release purely from the AST-declared parameter type. So a
bare-owned signature that the pass proved is a borrow still paid full RC
traffic. (The cost-summary/codegen disagreement is tracked separately as a
reporting bug.)

### Measured cost (LeetCode #101, symmetric-tree, Apple M5 Pro)

The read-only crossed tree walk `is_mirror` is a pure pointer-chase. Profiled:

| | wall | vs Rust | instructions | cycles | IPC |
|---|---|---|---|---|---|
| baseline | 273.6 ms | 2.43× | 5.24 B | 1.15 B | 4.57 |
| **rc-elide** | **191.2 ms** | **1.70×** | **3.74 B** (−29%) | **0.77 B** (−33%) | 4.83 |
| rust / c | 112.8 ms | 1.0× | 1.87 B | — | — |

kāra retired **2.81× Rust's instructions** at *higher* IPC — a pure
instruction-count (codegen-density) problem, not a memory/latency one. `is_mirror`
spent ~50 of 77 instructions on refcount inc/dec/free bookkeeping on a walk that
never mutates or stores anything. Eliding it is a **30% wall-time win** and closes
the Rust gap from 2.43× → 1.70×.

## Why it is sound to elide

The caller-side `rc_inc` and callee-side `rc_dec` are a **balanced pair**.
Deleting both changes the net refcount by zero, so the only hazard is the object
reaching refcount 0 *during* the call. That cannot happen when the caller keeps
its own reference alive across the call — which is exactly what a `ref` borrow
guarantees (the argument is not moved/consumed, so the caller still holds it).
kāra's borrow checker already enforces that a `ref` referent outlives the borrow.
So for a genuine borrow the pair is a provable no-op and deleting it is
correctness-preserving.

## The soundness guard (`src/rc_elide.rs`)

A `ref` classification alone is **not** sufficient at the call site: it is only
safe when the *caller* keeps the argument alive. Two shapes break that:

1. **Fresh-rvalue args** — `f(Some(x))`, `f(make_node())`, struct literals. The
   `+1` here comes from the *producer*; the callee's exit `rc_dec` is what
   consumes it, with no caller-kept source. Eliding the dec **leaks** the
   producer's ref. (This is exactly what the unsound prototype did — kata #2's
   adder, called `add_two_numbers(Some(x), Some(y))`, leaked 6 nodes.)
2. **Invisible callers** — a public function (external callers) or a function
   used as a value / called via method dispatch (argument shapes not tracked).

So `safe_elidable_ref_params` computes, whole-program, exactly the `ref` params
that are safe: a `Ref` param of `F` at position `i` is elidable iff

- `F` is seen **directly called** at least once (`Call { callee: Identifier(F) }`) —
  so its argument shapes are fully observed;
- **every** such call passes a **place rooted at a named binding** at `i`
  (`x`, `n.left`, `v[i]`, `t.0`, `self` — the caller owns the root and drops it
  at its own scope exit), never a fresh rvalue;
- `F` is **not** used as a value anywhere (no indirect call could pass an
  untracked arg);
- `F` is **not** `pub` (external callers are invisible).

It is deliberately **conservative** — anything it cannot prove safe it drops, so
the worst case is a missed optimization, never a leak. The traversal is an
**exhaustive** `match` over every `ExprKind` / `StmtKind` (no `_` arm): a call
nested anywhere must be seen, and a future AST variant fails to compile until
handled here — fail-closed, the discipline the leak-safety rests on.

## Wiring

- `ownership.rs` computes `OwnershipCheckResult::elidable_ref_params` (only when
  the env flag is set — otherwise empty, zero overhead).
- `codegen.rs` consumes it: `borrowed_arg_skip` / `borrowed_param_dec_skip` (the
  existing, LSan-proven Phase-C2b headerless borrow-skip machinery) also fire for
  these params, so the call-site arg inc, the source transfer/consume, and the
  callee exit dec are all skipped together — a pure balanced borrow. No new
  cleanup-emission code, so no new leak surface; the guard only *prevents*
  elision.

The analysis lives outside codegen and reaches it as a plain-data hint,
preserving the codegen-containment invariant.

## Why the `Ref`-gated version is unsound (the Linux LSan finding)

The caller-side guard above is correct, but it trusts `OwnershipMode::Ref` to
mean "the callee only borrows." It does not. The ownership pass maps
`ParamUsage::Read → Ref`, and it classifies `let mut a = param` (a move-out of a
non-`Copy` `Option[shared]` / `Vec`) as **Read**, not `Consumed`. So a function
that *transfers its param's resource out* is still labelled `Ref`:

```
fn merge_two(l1: Option[ListNode], l2: Option[ListNode]) -> Option[ListNode] {
    let mut a = l1;   // MOVE of l1 — but classified Read → Ref
    ...               // a's nodes are spliced into the returned list
}
fn merge_k(lists: Vec[Option[ListNode]]) -> Option[ListNode] {
    let mut work = lists;  // MOVE of lists → Ref
    ... work[0]            // returns a node the param owned
}
```

Both are *called with place args* (`merge_two(work[i], work[i+interval])`,
`merge_k(v)`), so the caller-side guard admits them — and eliding their exit dec
drops a decrement the transferred nodes genuinely needed. **Linux LSan caught
exactly this**: `owned_vec_param_let_move_interval_merge` leaked 72 bytes in 3
allocations with the flag on. (macOS could not — ASAN does no LeakSanitizer on
Darwin, and the `leaks` spot-checks only covered #101 + the adder.) This is the
whole reason the Linux LSan gate is mandatory for this class.

## Verification (flag ON) — mixed

- macOS `codegen` (2236), `memory_sanitizer` (638, ASAN UAF/double-free),
  `par_codegen` (159): **all 0 failed**. `leaks`/guardmalloc on #101 + adder:
  0 leaks. The #101 win is preserved (5.24 B → 3.74 B instructions).
- **Linux LSan: 1 leak** (`owned_vec_param_let_move_interval_merge`, 72 B / 3
  allocs). ⇒ NOT clean ⇒ not shipped.

## The real remaining work: a callee-side purity certificate

Elision is sound only for a param the callee treats as a *pure borrow* — never
moved out, stored, returned, or passed by value to a consumer. `Ref` is too
weak. What is needed is a dedicated analysis proving every use of the param is a
non-escaping peek:

- allowed: `param.field` / `param[i]` reads, comparisons, and place-args to
  other borrowing calls;
- a `match param { … }` is allowed only if no arm binding escapes (recursive —
  the binding's own uses must be peeks), which is the hard, fixpoint part;
- forbidden: `let x = param`, `x = param`, `return param`, storing it into a
  field/collection, or passing it by value to an owning callee.

`is_mirror` (#101) satisfies this (returns `bool`, only matches/reads/recurses);
`merge_two`/`merge_k` do not (they transfer nodes out). Building that analysis —
correctly, with the same exhaustive/fail-closed discipline — is the next slice.
Until it exists, `Ref` alone cannot gate the elision.

## What is reusable

- `src/rc_elide.rs` — the exhaustive whole-program walker + the caller-side
  guard (place-args-only, non-escaped, private, directly-called). Sound as far as
  it goes; it just needs the callee-side purity filter ANDed in.
- The codegen wiring (`elidable_ref_params` hint → `borrowed_arg_skip` /
  `borrowed_param_dec_skip`) — reuses the LSan-proven C2b borrow-skip machinery,
  no new cleanup emission, so no new leak surface once the input set is correct.

## Also surfaced (separate bug)

`karac query cost-summary` reports 0 rc_ops for `is_mirror` while codegen emits
~40 rc-inc sites — the cost model and codegen disagree. Independent of this
optimization; worth its own ledger entry.
