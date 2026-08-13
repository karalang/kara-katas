# Probe — a 23% "ISA effect" that was a 64-byte stack shift

The first run of this lane produced a row that should not exist:

```
c      447.8 ms ± 8.9      c (-march=x86-64-v3)   551.2 ms ± 18.1
```

The *higher* ISA baseline, 23% slower, at σ of 2.0% and 3.3%. On a histogram
loop with nothing to vectorise, from a compiler flag that only ever adds
instructions to choose from.

## The two kernels are the same instruction stream

`clang -O3` and `clang -O3 -march=x86-64-v3` emit an identical scalar histogram
loop. Not similar — identical, one displacement apart:

```asm
; clang -O3                      ; clang -O3 -march=x86-64-v3
mov  (%rbx,%rax,8),%rdx          mov  (%rbx,%rax,8),%rdx
incq (%rsp,%rdx,8)               incq 0x40(%rsp,%rdx,8)
inc  %rax                        inc  %rax
cmp  %rcx,%rax                   cmp  %rcx,%rax
jb   .loop                       jb   .loop
```

Neither vectorises the increment (`vpgather`/`vpscatter` count: zero). The AVX2
that `-march=v3` unlocks is spent entirely on the 256-slot parity sweep — 1.02M
elements against the histogram's 796M, 0.13% of the work. It cannot be worth
23%.

What differs is `0x40`. Requiring 32-byte alignment for AVX2 spills moved the
whole stack frame, and with it the counter table's position relative to the
`data[]` array. On a loop whose entire cost is store-to-load forwarding on a
2 KB table, that is enough.

## The fix is parity, not a workaround

C was the only mirror holding its counters in a **stack array**. Kāra uses a
`Vec`, Rust a `Vec`, Go a slice — all three heap-allocated, none of them moving
with the frame. Making C `malloc` its table matches the other three and takes
the layout out of the measurement:

| C build | stack array (before) | heap (after) |
|---|---:|---:|
| `clang -O3` | 459.8 ms | **449.2 ms** |
| `clang -O3 -march=x86-64-v3` | 537.5 ms | **451.1 ms** |
| gap | **17%** | **0.4%** |

Same sink (`777290116`) throughout. The 17% was the stack offset and nothing
else; both builds land on the faster figure once the table stops moving.

This is the cross-language-parity rule doing real work rather than ceremony: the
mirror that was written differently from the other three was the one producing
the false result, and the difference was a `long counts[256]` that looked
completely innocuous.

## What the lane actually measures, and what it does not explain

With the layout artifact gone, the histogram loops line up with their costs:

| binary | inner loop | checks | mean |
|---|---|---|---:|
| C | 4 instructions | none | 448.4 ms |
| Kāra | 9 instructions | 2 bounds + 1 overflow | 473.4 ms |
| Rust | 7 instructions | 1 bounds | 533.6 ms |

Kāra is 5.6% behind C while carrying three safety checks per element that C does
not, and 12.7% **ahead** of unchecked `rustc -O`, which carries one. It also has
more instructions than Rust in the loop and is faster anyway, so instruction
count does not order this lane.

**Why Rust trails is not established here.** Rust's `incq (%rbx,%rcx,8)` is a
single read-modify-write where Kāra emits a separate load, increment and store,
and a split RMW can schedule better under repeated same-index collisions — but
this probe did not test that, so it stays a hypothesis and is not written up as
a cause. `rustc -O -C overflow-checks=on` is only 4% behind plain `rustc -O`
(553.9 vs 533.6), so whatever costs Rust its 19% against C is not the checking.

## Reproducing

```bash
# the two C kernels, one displacement apart
for m in "" "-march=x86-64-v3"; do
    clang -O3 $m pal_perm.c -o /tmp/pp && objdump -d --no-show-raw-insn /tmp/pp |
        awk '/<main>:/{p=1} p&&/^$/{exit} p' | grep -A1 'mov.*%rbx.*%rdx'
done
```

Measured on the x86-64 container lane (4-core Xeon @ 2.80 GHz, clang 18.1.3,
rustc 1.94.1), the same host as `../results.container-x86.json`.
