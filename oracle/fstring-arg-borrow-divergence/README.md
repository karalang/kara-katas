# fstring-arg-borrow-divergence

**A call's parameter modes change depending on whether it sits inside an f-string
interpolation.** A bare (owning) parameter is consumed in statement position and
merely borrowed inside `f"{...}"` — same signature, same call, two semantics.

Surfaced writing kata [#243](../../leetcode/201-300/243-shortest-word-distance/),
whose first draft declared `words: Slice[String]` and called a `report` helper
repeatedly on one array.

## The three programs

```bash
karac build moves.kara    && ./moves       # bare param consumes: DROP inside callee
karac build borrows.kara  && ./borrows     # inside f"{}": no consume, DROP at caller's last use
karac check  rejected.kara                 # same call under plain println(): correctly REJECTED
```

`consume` declares `t: Tracked` with no `ref`, so it owns its argument. A user
`impl Drop` makes the release observable:

| Call position | `karac check` | Where the destructor runs |
|---|---|---|
| `let n = consume(t);` | accepted (one call) | **inside `consume`**, before it returns |
| `println(consume(t));` twice | **rejected** — `value 't' moved here, used again here` | — |
| `let a = f"{consume(t)}";` twice | **accepted** | once, at `t`'s **last use in the caller** |

So `consume(t)` inside an interpolation never consumes `t`: two calls on one
value are legal, and the value the callee declared ownership of outlives it.

## What this is not

Three explanations ruled out by probe, because each looked likely first:

- **Not the print-borrow rule.** `B-2026-07-02-21` made `println(s); println(s)`
  legal by giving the print family `ref` argument modes. That is about println's
  *own* argument and does not reach a nested call's parameter modes —
  `rejected.kara` is the control, and it is rejected.
- **Not `Slice` semantics.** Bare `Slice[T]`/`Vec[T]` params consuming their
  argument is deliberate language design, settled in `B-2026-07-01-10`: that
  entry offered "declare the params `ref`" or "give `Slice[T]` borrow mode by
  default" and chose the first, declaring `ref Slice[f64]` across `stats.kara`.
  The repro here uses a plain user struct, so `Slice` is not involved at all.
- **Not memory unsafety.** Exactly one drop, no double-free, and nothing
  poisoned reading the payload under `MallocScribble=1 MallocPreScribble=1`.
  `--interp`, JIT and `karac build` all agree. This is a *borrow*, not a
  use-after-free. An earlier reading of the drop order as an early consume
  followed by a use-after-destructor was wrong — it was drop-at-last-use.

## Root-cause hypothesis

design.md § String Interpolation (L4667) specifies that `{expr}` desugars to
`expr.to_string()` and that `Display.to_string(ref self)` **borrows the
receiver**, "so the same value can appear in multiple `{}` slots without being
consumed". That rule is correct and intended for the interpolated *value* —
`f"{t}"` must not consume `t`.

The behaviour here looks like that borrow being applied one level too deep: the
ownership pass appears to treat the whole interpolated expression as a borrow
context instead of borrowing only its result, so it never descends into a nested
call's arguments to classify them against the callee's declared modes. Codegen
agrees with the checker, which is why the two stay self-consistent and nothing
crashes.

## Why it matters

Not memory safety — **release timing**. For a value whose purpose is
release-on-consume (a lock guard, a file handle, a `Secret`), writing the
consuming call inside an f-string silently defers the release from inside the
callee to the caller's last-use point. `oracle/moves.kara` releases before the
next statement; `oracle/borrows.kara` holds it across two more calls. And
`karac check` accepts reuse that the declared signature forbids, so the
ownership pass is not a reliable gate in that position.

## ablations/

The narrowing probes, one case per file. `<owner>_<elem>_<ret>.kara` is the
owner × element-type × return-type matrix that established bare `Slice` params
consume (and that `Array` of a `Copy` element escapes because it *is* `Copy`, and
that the return type is irrelevant). `<case>__<callform>.kara` is the call-form
matrix — `stmt` / `bare` / `arith` all reject, `fstring` alone is accepted:

```bash
for f in ablations/*.kara; do
    printf '%-30s %s\n' "$(basename "$f")" \
        "$(karac check "$f" >/dev/null 2>&1 && echo pass || echo FAIL)"
done
```
