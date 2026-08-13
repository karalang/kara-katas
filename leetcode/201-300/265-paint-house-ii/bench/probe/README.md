# Probe — why Kāra loses this lane by 1.5×

The lane result put Kāra last among the compiled mirrors and by a wide margin:

```
rust      260.8 ms      c      305.7 ms
rust_ovf  288.3 ms      kara   457.1 ms
```

1.58× behind the **equal-safety** Rust build, so checked arithmetic is not the
explanation — that build checks too. σ was 2.4–4.4% throughout, so it is not
noise either. This is where it goes.

## Instruction mix

Counting conditional moves inside each `main`:

| binary | `cmov` | mean |
|---|---:|---:|
| `rustc -O` | 133 | 260.8 ms |
| `rustc -O -C overflow-checks=on` | 127 | 288.3 ms |
| `clang -O3` | 129 | 305.7 ms |
| **Kāra** | **17** | **457.1 ms** |

The hot loop is the reduction that finds `(min, its index, second-min)` over the
previous row. `rustc` **fully unrolls** it — `k` is a compile-time 32, so the
loop becomes 32 straight-line blocks, every `j` is a constant, and each element
costs six instructions with **no branch**:

```asm
mov    0xe0(%r14),%r9
cmp    %r8,%r9
cmovl  %r9,%r8
cmp    %r13,%r9
cmovl  %r13,%r8
mov    $0x1c,%r10d      ; j is a literal here
cmovl  %r10,%rdi
cmovl  %r9,%r13
```

Kāra unrolls it **4×** and keeps a data-dependent branch per element:

```asm
mov    (%r14,%r11,8),%r8
mov    %r8,%r9
cmp    %r10,%r8
jl     90d5             ; <- a branch, not a cmov
mov    %r10,%r9
cmp    %rbp,%r8
cmovl  %rbp,%r9
cmovl  %r11,%r12
cmovl  %r8,%rbp
```

The trip count is not the problem — Kāra's loop ends on `cmp $0x20,%r11`, so
LLVM knows it runs 32 times. It unrolls by 4 and stops, and the partial unroll
leaves `j` in a register rather than a literal.

## Confirming that the branch is part of it

The reduction's branch is data-dependent, so making it predictable isolates its
share. Re-running every build with all costs set to 1 — same instruction stream,
same iteration counts, but within any row every entry is equal, so the branch
outcome becomes constant after the first two elements:

| build | costs `1..40` | costs all `1` | change |
|---|---:|---:|---:|
| Kāra | 457.1 ms | **263.2 ms** | −42% |
| C | 305.7 ms | **201.5 ms** | −34% |
| Rust (checked) | 288.3 ms | 300.7 ms | +4% |

Rust does not move, which is what "branchless" predicts. Kāra and C both drop
sharply, so both are paying for mispredictions — but Kāra's deficit against C
only narrows from **1.49× to 1.31×**. Mispredictions are roughly a third of the
excess; the rest is the instruction count that the partial unroll leaves behind.

## Ruling out the source spelling

The Kāra kernel writes the update as a nested `if` inside an `else`, where the
Rust mirror uses `else if` and binds the loaded value to a local first. Rewriting
the Kāra source to match exactly — `let v = prev[j];` then `else if v < min2` —
produces a **byte-identical kernel**: same 403 lines, same 17 `cmov`, and
452.9 ms against the original's 451.5 ms.

So this is not a spelling artifact in the kata. It is what `karac` hands LLVM, or
what LLVM does with it.

## Ruling out the buffer swap

The kernel swaps two row buffers with `let tmp = prev; prev = cur; cur = tmp;`,
which would be catastrophic if it copied. A variant using one `2k` buffer indexed
by parity — no swap at all — runs at 445.8 ms against 477.5 ms, a 7% difference
and the same sink. The swap is a move, and it is not where the time goes.

## Filed

`B-2026-08-13-10` in the sibling `kara` repo — class `perf`, severity medium.
The kata is unchanged: nothing here is worked around, and the natural spelling
stays in the file.

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
clang 18.1.3), the same host as `../results.container-x86.json`.
