# Probe — two artifacts, and why this lane cannot rank

This lane was rebuilt once and re-explained once before publishing. Both
corrections are here, because each is a benchmark-methodology fault rather than
a language result, and the second one is the reason the lane's table carries a
caveat instead of a ranking.

## Artifact 1 — the mirrors were not doing the same work

The first version had each leaf build a **string**. Kāra came out at 476.5 ms
against C's 156.0 — 3.05× — which would have read as a language result. It was
not one. The four mirrors were using four different allocation strategies:

| mirror | per leaf |
|---|---|
| C | `char s[64]` on the stack — **no allocation at all** |
| Rust | one `String`, appended in place with `push` |
| Go | one `strings.Builder` |
| **Kāra** | `s = s + f"{…}"` — **a new string per character, 17 per leaf** |

Kāra's `+` is an immutable concatenation, so it allocates and copies on every
character where Rust and Go append in place and C does neither. That is four
programs, not one, and it is the same defect a C stack array introduced in
[#266](../../266-palindrome-permutation/) — the mirror written differently from
the others is the one producing the false number.

The fix is to take the string API out of the comparison entirely: every mirror
now writes its 17 bytes into **one hoisted buffer** it reuses, so nothing
allocates per leaf and the lane measures the search. Kāra went 476.5 → 227 ms on
the identical sink. [#257](../../257-binary-tree-paths/) remains the corpus's
string-building lane; this one is not it.

(Kāra does have `String.push` for in-place append, which would have been the
narrower fix. The buffer was chosen instead because C cannot match a per-leaf
heap allocation without writing unnatural C.)

## Artifact 2 — a 31% "ISA effect" that was code alignment

With the mirrors equalised, the table still had two impossibilities:
`clang -O3 -march=x86-64-v3` beat plain `clang -O3` by 31%, and
`rustc -O -C overflow-checks=on` beat plain `rustc -O` by 24%. Overflow checks
cannot make a program faster, so at least one of those had to be an artifact —
and both were the same size, which is a hint in itself.

The hash loops in the two C builds are the same instruction sequence, register
allocation aside, so it is not the arithmetic. Forcing code alignment settles it:

| build | default | `-falign-loops=32 -falign-functions=32` |
|---|---:|---:|
| `clang -O3` | 397.4 ms | **319.1 ms** |
| `clang -O3 -march=x86-64-v3` | 306.6 ms | **312.0 ms** |

Aligned, the two builds land 2% apart instead of 30%, on the same sink. The
baseline build's 397 ms was a **misaligned hot loop**, not an ISA deficit. The
`-march` flag had shifted the code enough to land the 128-slot scan on a
favourable boundary, which is worth more here than any instruction it unlocked.

## Why the lane still cannot rank, and why that is published rather than fixed

The obvious response — add the alignment flags to every mirror — is the wrong
one. `clang -O3` and `rustc -O` are the corpus's methodology; tuning the flags
for the one lane where they embarrass a build makes that lane incomparable with
the other 250 and starts a search for flags that flatter whoever is losing.

So the table stands as measured with the standard flags, and states what the
measurement supports: **the intra-language twin spread (31% for C, 24% for Rust)
exceeds the inter-language spread, so the per-language ordering is not resolvable
here.** What the lane does support is the top-to-bottom range — every mirror lands
between 309 and 446 ms, a 1.44× band — and the observation that Kāra is inside it
rather than an outlier, which is the claim the first version would have got
badly wrong.

A deep recursion around a small hot loop is simply an alignment-sensitive shape.
Naming that is more useful than picking flags until the numbers behave.

## Reproducing

```bash
clang -O3 pal_gen.c -o /tmp/c_base
clang -O3 -march=x86-64-v3 pal_gen.c -o /tmp/c_v3
clang -O3 -falign-loops=32 -falign-functions=32 pal_gen.c -o /tmp/c_al
clang -O3 -march=x86-64-v3 -falign-loops=32 -falign-functions=32 pal_gen.c -o /tmp/c_al_v3
hyperfine --warmup 3 -N /tmp/c_base /tmp/c_v3 /tmp/c_al /tmp/c_al_v3
```

Measured on the x86-64 container lane (4-core Xeon @ 2.80 GHz, clang 18.1.3,
rustc 1.94.1), the same host as `../results.container-x86.json`.
