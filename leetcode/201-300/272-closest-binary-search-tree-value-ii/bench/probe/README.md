# Probe — why the field is this tight, and a hypothesis that did not survive

The lane's whole spread is **1.17×**, from C at 431.9 ms to Kāra at 504.3 ms,
with all three Rust builds inside 2.5% of each other. That is unusually
compressed for this corpus, so it was probed rather than narrated.

## The hypothesis: the tree is too big, so everyone waits on memory

A 30,000-node tree is ~703 KiB across three `i64` arrays, and each query is a
chain of ~15 dependent random loads. If the lane were latency-bound, codegen
differences would wash out and the languages would converge — and shrinking the
tree until it fits L1 should pull them apart again.

**It does not.** Holding everything else fixed and moving only `node_count`
across a 150× range:

| tree | working set | C | Rust | Kāra | Kāra / C |
|---|---|---:|---:|---:|---:|
| 2,000 nodes | ~46 KiB | 280.1 ± 5.1 ms | 320.7 ± 3.2 | 339.0 ± 4.5 | 1.21× |
| 30,000 nodes | ~703 KiB | 444.4 ± 14.6 ms | 477.5 ± 12.9 | 499.5 ± 5.3 | **1.12×** |
| 300,000 nodes | ~7 MiB | 1023 ± 32 ms | 1135 ± 46 | 1255 ± 91 | 1.23× |

The ratio is roughly flat — 1.21, 1.12, 1.23 — not monotone in working-set size.
So the compression is not a cache effect, and the 30,000-node point is simply
where the three happen to sit closest; the middle row's 1.12× should be read as
the noisiest of the three, not the most informative.

**What the sweep does confirm is [#261](../../261-graph-valid-tree/)'s lesson
about measurement stability.** Kāra's σ goes 1.3% → 1.1% → **7.2%** across those
three sizes. At 7 MiB the run-to-run variance is larger than the entire gap
between the languages, which would make any ranking at that size meaningless.
That — not the ranking — is why the lane is sized at 703 KiB.

The remaining ~1.1–1.2× is the ordinary bounds-check gap: C indexes unchecked
and Kāra, Rust and Go all check, on every one of the ~15 tree loads and every
stack push and pop.

## Reproducing

```bash
for N in 2000 30000 300000; do
  sed "s/let node_count = 30000i64;/let node_count = ${N}i64;/"      ../k_closest.kara > /tmp/pk.kara
  sed "s/const int64_t node_count = 30000;/const int64_t node_count = ${N};/" ../k_closest.c > /tmp/pc.c
  sed "s/let node_count: i64 = 30000;/let node_count: i64 = ${N};/"  ../k_closest.rs  > /tmp/pr.rs
  karac build /tmp/pk.kara -o /tmp/pk && clang -O3 /tmp/pc.c -o /tmp/pc -lm && rustc -O /tmp/pr.rs -o /tmp/pr
  hyperfine -w 3 -r 12 /tmp/pc /tmp/pr /tmp/pk
done
```
