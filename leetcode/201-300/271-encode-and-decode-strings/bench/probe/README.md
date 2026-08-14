# Probe — where C's 2.8× comes from

The lane's headline gap (C 255.8 ms vs Kāra 729.7 ms) is far too large for the
same algorithm, so it was measured before it was published.

The inner payload copy is written identically in all five mirrors:

```
enc[w + p] = src[base + p]
```

`clang -O3` is the only compiler that recognizes it. Its `main` contains exactly
one call to glibc's `memcpy` and zero vector registers; `rustc -O`'s `main`
contains neither, and Go's contains one vector register.

Disabling the promotion changes only the codegen — not the workload, not the
source, not the sink, which stays `446190680`:

| build | mean | `memcpy` calls in `main` |
|---|---:|---:|
| `clang -O3` (the lane) | 255.8 ± 7.2 ms | 1 |
| `clang -O3 -mllvm -disable-loop-idiom-all` | 339.0 ± 3.1 ms | 0 |
| `clang -O3 -fno-builtin` | 525.3 ± 12.6 ms | 0 |

So roughly **2× of C's 2.8× advantage is one loop-idiom recognition**. Against a
C that copies bytes the way the other four do, Kāra is 1.38× behind rather than
2.8×; the remainder is the bounds check, which C alone does not pay and which is
most expensive exactly here, in a byte-at-a-time copy.

The lane keeps C at its true 255.8 ms — that is what `clang -O3` genuinely does
with this source — with the mechanism named rather than tuned away.

## Reproducing

```bash
clang -O3 -mllvm -disable-loop-idiom-all codec.c -o probe/codec_c_noidiom
clang -O3 -fno-builtin                   codec.c -o probe/codec_c_nobuiltin
hyperfine -w 5 -r 30 ./target/codec_c ./probe/codec_c_noidiom ./probe/codec_c_nobuiltin

# the counts in the table
objdump -d target/codec_c | awk '/<main>:/,/^$/' | grep -c 'call.*memcpy'
objdump -d target/codec   | awk '/<main>:/,/^$/' | grep -c '%xmm\|%ymm'
```
