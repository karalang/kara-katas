# fstring-arg-borrow-divergence

**A call's parameter modes changed depending on whether it sat inside an f-string
interpolation.** A bare (owning) parameter was consumed in statement position and
merely borrowed inside `f"{...}"` — same signature, same call, two semantics.

Surfaced writing kata [#243](../../leetcode/201-300/243-shortest-word-distance/).
Filed as `kara` ledger **B-2026-07-29-28**, **fixed by `c8bce5d3`**.

## The three programs

```bash
karac build moves.kara    && ./moves       # bare param consumes: DROP inside callee
karac check  borrows.kara                  # the bug: WAS accepted, now REJECTED
karac check  rejected.kara                 # same call under plain println(): always REJECTED
```

`consume` declares `t: Tracked` with no `ref`, so it owns its argument. A user
`impl Drop` made the release observable:

| Call position | before `c8bce5d3` | after |
|---|---|---|
| `let n = consume(t);` | accepted; destructor **inside `consume`** | unchanged |
| `println(consume(t));` twice | **rejected** — `value 't' moved here, used again here` | unchanged |
| `let a = f"{consume(t)}";` twice | **accepted** — one drop, at `t`'s last use in the *caller* | **rejected**, same as every other position |

So before the fix, `consume(t)` inside an interpolation never consumed `t`: two
calls on one value were legal, and the value the callee declared ownership of
outlived it.

## Root cause

Simpler than this file's original hypothesis, which guessed the interpolation's
documented borrow was being applied "one level too deep". It was not applying a
borrow at all — **the pass never looked inside the hole.**
`ExprKind::InterpolatedStringLit` was grouped with the leaf literals
(`Integer`/`StringLit`/…) in **two** walkers:

- `src/use_classifier.rs` — classifies uses; the arm body was `{}`, so a hole's
  expression was never walked.
- `src/cfg.rs` — lowers expressions to CFG nodes; same grouping, returned `cur`
  unchanged, so `direct_uam_candidates` had no node at which to find a witness.

Both had to be fixed. Patching either alone changes nothing observable — which
is why the first attempt looked like a complete no-op and sent the search after a
second diagnostic emitter that did not exist.

Holes are now walked in `Mode::Reading`, which preserves design.md § String
Interpolation (L4667): `{expr}` desugars to `expr.to_string()` with
`Display.to_string(ref self)` borrowing the receiver, so a value may still appear
in multiple `{}` slots without being consumed. The `Call`/`MethodCall` arms
derive their own argument modes from the callee's signature independently of the
enclosing mode, and that is what restores the nested move.

## What it was not

Three explanations ruled out by probe, each of which looked likely first:

- **Not the print-borrow rule.** `B-2026-07-02-21` made `println(s); println(s)`
  legal by giving the print family `ref` argument modes. That governs println's
  *own* argument and never reached a nested call's parameter modes —
  `rejected.kara` is the control, and it was rejected before the fix too.
- **Not `Slice` semantics.** Bare `Slice[T]`/`Vec[T]` params consuming their
  argument is deliberate design, settled in `B-2026-07-01-10`. The repro uses a
  plain user struct, so `Slice` is not involved at all.
- **Not memory unsafety.** Exactly one drop, no double-free, and nothing poisoned
  reading the payload under `MallocScribble=1 MallocPreScribble=1`; `--interp`,
  JIT and `karac build` all agreed. It was a *borrow*, not a use-after-free — the
  checker and codegen were self-consistent, both treating it as one. An
  intermediate reading of the drop order as an early consume followed by a
  use-after-destructor was wrong; it was drop-at-last-use.

## What the fix caught

Real code was relying on this. Sweeping all 687 `.kara` files in this repo with
pre- and post-fix binaries, two katas newly failed `karac check`, both genuine
latent use-after-moves that the bug had hidden:

- [#87](../../leetcode/1-100/87-scramble-string/) — `to_vec(s1)` / `to_vec(s2)`
  consume, then `f"{s1} ~ {s2}: {found}"` uses both.
- [#93](../../leetcode/1-100/93-restore-ip-addresses/) — `restore(str)` consumes,
  then `f"\"{str}\": {count}"` uses it.

Both are fixed by declaring the read-only params `ref` — the same lesson #243
started from. Output was never wrong (codegen defensive-copies the reuse, which is
why they passed A/B all along), so this made the source say what it meant. All
four surfaces re-verified against the Python mirrors afterwards.

Six codegen tests in the `kara` repo failed for the same reason and were repaired
the same way. Making these uses visible also exposes them to rc-promotion, so #93
now draws a conservative `perf[rc-fallback]` for `path`: the consume and the use
are on disjoint branches (the `part == 4` arm returns), so the Rc is unnecessary
but safe — `rc_values` fires for dominance-*incomparable* consume/use by design.
Not measured for perf impact.

## ablations/

The narrowing probes, one case per file. `<owner>_<elem>_<ret>.kara` is the
owner × element-type × return-type matrix that established bare `Slice` params
consume (and that `Array` of a `Copy` element escapes because it *is* `Copy`, and
that the return type is irrelevant). `<case>__<callform>.kara` is the call-form
matrix: before the fix `stmt` / `bare` / `arith` rejected and **`fstring` alone
was accepted**, which is what localised the bug. After the fix all four reject
uniformly — so the three `*__fstring.kara` files are now expected failures, and
that they fail is the regression test.

```bash
for f in ablations/*.kara; do
    printf '%-30s %s\n' "$(basename "$f")" \
        "$(karac check "$f" >/dev/null 2>&1 && echo pass || echo FAIL)"
done
```
