# Probe — a 1.5× Kāra deficit, filed and fixed the same day

This lane's **first** run put Kāra last among the compiled mirrors and by a wide
margin — 1.58× behind the equal-safety Rust build and 1.49× behind C. That was a
real codegen gap. It is now fixed, and this file is the record of finding it,
the record of getting its cause half wrong, and the correction.

## What the first run showed

```
rust      260.8 ms      c      305.7 ms
rust_ovf  288.3 ms      kara   457.1 ms
```

σ was 2.4–4.4%, so not noise, and the build Kāra trailed checks arithmetic too,
so checked arithmetic was not the explanation.

Conditional moves inside `main`: `rustc -O` 133, `rustc -O -C overflow-checks=on`
127, `clang -O3` 129, **Kāra 17**.

The hot loop is the reduction over the previous row for `(min, its index,
second-min)`. `rustc` fully unrolled it — `k` is 32, so the loop became 32
straight-line blocks, every `j` a literal, each element six branchless
instructions. Kāra unrolled by 4 and kept a data-dependent `jl` per element.

## Controls run before filing

| control | finding |
|---|---|
| all costs set to `1`, making the branch predictable | Kāra 457.1 → 263.2 ms, C 305.7 → 201.5, checked Rust 288.3 → 300.7 (unchanged, as branchless predicts). Kāra's deficit vs C narrowed 1.49× → 1.31×: **mispredictions were about a third**, instruction count the rest. |
| Kāra source rewritten to Rust's `else if` over a bound local | **byte-identical kernel** — same 403 lines, same 17 `cmov`, 452.9 vs 451.5 ms. Not a spelling artifact in the kata. |
| one `2k` buffer indexed by parity instead of swapping two | 445.8 vs 477.5 ms, same sink. `prev = cur` is a move, not a copy. |
| bounds checks | Kāra's unrolled reduction loads with a bare `mov`; the *faster* `rust_ovf` map loop carries a bounds check and still wins. Not it. |

## Filed as B-2026-08-13-10 — and the hypothesis was wrong

The row guessed the lever was "raising the unroll threshold, or checking that the
loop metadata `karac` attaches does not cap it", flagged as unverified. **It was
the wrong half.** `karac` attached *no* metadata to that loop at all; the 4× was
LLVM's own default. The actual cause was upstream of that: `karac`'s
`while_loop_wants_full_unroll` predicate reads the bound off the **source guard**
and accepted only a literal — and the kernel writes

```kara
let k = 32i64;
…
while j < k { … }
```

so a bound spelled as a name never qualified, however obviously constant.

The disassembly had actually contained the disproof the whole time: the loop ends
on `cmp $0x20`, so LLVM had already constant-propagated 32 and knew the trip
count. It was not being *prevented* from unrolling — it simply was never asked.
Reading "LLVM knows the trip count, so the trip count is not the problem" as
"therefore the problem is downstream in the pass pipeline" was the error; the
missing request was upstream, in the frontend predicate.

## Fixed by 3ea8310

`while_loop_wants_full_unroll` now accepts a bound written as a name bound to an
immutable integer literal. On this host, the same kernel source and the same sink
`991930357`:

| | `cmov` in `main` |
|---|---:|
| before the fix | 17 |
| after the fix | **191** |

The fixing session's own interleaved A/B on its host recorded 620 → 257 ms, a
2.4× speedup at identical sink.

## A note on the two runs

The container was **restarted between the pre-fix and post-fix measurements**, so
the two tables in this file were produced on different hardware and the absolute
numbers across them are not a same-host A/B. A stable reference confirms the
drift is real but small — [#261](../../261-graph-valid-tree/)'s unchanged C
mirror moved 425.5 → 460.6 ms (+8%) across the same boundary, while this lane's
byte-identical C binary moved 305.7 → 434.3 ms.

What *is* sound is each table on its own: every row within a run comes from one
interleaved hyperfine invocation on one host. The claim "Kāra is now fastest"
rests on the post-fix run alone, and the claim "the fix worked" rests on the
`cmov` count and the fixing session's same-host A/B — not on subtracting one
table from the other.

## Reproducing

```bash
# cmov counts
for b in target/paint_ii_kara target/paint_ii target/paint_ii_ovf target/paint_ii_c; do
    echo -n "$b: "
    objdump -d --no-show-raw-insn "$b" |
        awk '/<main>:|paint_ii4main/{p=1} p&&/^$/{exit} p' | grep -c cmov
done

# predictable-branch variants
sed 's|% 40i64 + 1i64|% 1i64 + 1i64|' paint_ii.kara > flat.kara
sed 's|% 40 + 1|% 1 + 1|'             paint_ii.c    > flat.c
```

Measured on the x86-64 container lane (4-core Xeon @ 2.80 GHz, rustc 1.94.1,
clang 18.1.3), the same host as `../results.container-x86.json` for the post-fix
table.
