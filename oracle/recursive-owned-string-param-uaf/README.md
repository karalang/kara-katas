# recursive-owned-string-param-uaf

**Compiler-behavior demonstration — a FIXED, high-severity codegen bug.**
Kept as a live regression probe.

[`repro.kara`](repro.kara) walks an Eulerian path over a
`Map[String, Vec[String]]` adjacency map (the Hierholzer shape used by LeetCode
#332 Reconstruct Itinerary). It now prints `SFO ATL SFO JFK ATL JFK` on all four
surfaces — `karac run --interp`, `karac run` (LLJIT), `karac build`, and
`karac build` under `KARAC_AUTO_PAR=0`.

Before the fix, the tree-walk interpreter was correct and codegen was not:

| Surface | Result before the fix |
|---|---|
| `karac run --interp` | ✅ `SFO ATL SFO JFK ATL JFK` |
| `karac run` (LLJIT) | 💥 aborted in `karac_string_clone` — `ptr::copy_nonoverlapping` precondition violated |
| `karac build` | ❌ garbage bytes at indices 1–4 (freed `String` buffers) |
| `karac build` + `KARAC_AUTO_PAR=0` | ❌ same garbage |

## The triggering shape

The narrow trigger turned out to be an **owned `String` parameter consumed twice
in one function** — here `cursor.insert(airport, …)` inside the loop, then
`route.push(airport)` after the recursive descent.

Owned `Vec`/`String` parameters are *caller-retains*: the callee never registers
a buffer free for them, and each retaining consume site deep-copies. But the
first consume also ran the move-out suppression, which zeroed the parameter
header's `cap`. With `cap == 0` the **second** consume took the parameter for a
borrowed view, skipped its own defensive copy, and stored a raw alias into the
caller's map-derived `Vec[String]` element — freed the moment the recursive call
returned. So `route` finished holding dangling pointers.

The other ingredients in the original ablation (recursion, a map-derived source
`Vec`, use-after-descent) are what make the aliased buffer actually die before
it is read; they set the stage rather than cause the bug. The `Map` mattered
only because `cursor.insert(airport, …)` supplied the *first* of the two
consumes.

Fixed in the sibling `kara` repo as ledger **B-2026-07-25-1**, with a permanent
ASan regression test (`asan_owned_string_param_consumed_twice_no_uaf` in
`tests/memory_sanitizer.rs`). See [`ablations/`](ablations/) for the
one-ingredient-removed variants used during the hunt.
