# Ablations for B-2026-07-25-1

Each file removes exactly one ingredient from [`../repro.kara`](../repro.kara).
Run each under both surfaces — `karac run --interp` (always correct) and
`karac build` — and compare.

| File | Ingredient removed | Build result |
|---|---|---|
| `a1-local-binding-STILL-FAILS.kara` | element bound to a local before the call | ❌ **still corrupts** → rules out the call-site argument path |
| `a2-no-map-PASSES.kara` | the `Map` (plain factory-returned `Vec[String]`) | ✅ passes → the Map is required |
| `a3-map-no-recursion-PASSES.kara` | the recursion | ✅ passes → recursion is required |
| `a4-plain-map-derived-drop-PASSES.kara` | recursion + deferred use (just create/drop a `Map.get` result) | ✅ passes → not a plain `Map.get` value-ownership double-free |

**Net:** the trigger needs **map-derived values AND recursion together**. Neither
the element-read path nor `Map.get`'s value ownership is wrong in isolation.

⚠️ A passing ablation is **non-manifestation, not proof of correctness** — some
of these share the same latent aliasing but have no allocation between the free
and the read, so the freed bytes survive intact.
