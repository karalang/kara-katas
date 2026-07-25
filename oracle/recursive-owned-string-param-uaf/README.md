# recursive-owned-string-param-uaf

**Compiler-behavior demonstration — an open, high-severity codegen bug.**

[`repro.kara`](repro.kara) walks an Eulerian path over a
`Map[String, Vec[String]]` adjacency map (the Hierholzer shape used by LeetCode
#332 Reconstruct Itinerary). The tree-walk interpreter is **correct**; codegen
is **not**:

| Surface | Result |
|---|---|
| `karac run --interp` | ✅ `SFO ATL SFO JFK ATL JFK` |
| `karac run` (LLJIT) | 💥 aborts in `karac_string_clone` — `ptr::copy_nonoverlapping` precondition violated |
| `karac build` | ❌ garbage bytes at indices 1–4 (freed `String` buffers) |
| `karac build` + `KARAC_AUTO_PAR=0` | ❌ same garbage |

## The triggering shape

All four ingredients are required — each was ablated individually and the
program passes without it:

1. a **recursive** function,
2. taking an **owned `String`** parameter,
3. whose argument is an **element of a `Vec[String]` obtained from a
   `Map[String, Vec[String]]`**,
4. with the parameter **used after** the recursive descent.

The owned `String` parameter appears to be passed as a borrow into the
map-derived `Vec`, which is dropped when the recursive frame's local goes out of
scope — so the value pushed after the descent dangles.

Tracked in the sibling `kara` repo as ledger **B-2026-07-25-1**. LeetCode #332 is
held out of the corpus until this is fixed (its output would violate the
repo's *A/B run == build* invariant).
