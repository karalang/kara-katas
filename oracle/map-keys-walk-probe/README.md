# map-keys-walk-probe

**Discriminator probe for `kara` ledger B-2026-07-24-2** (map `keys()` perf gap).

LeetCode #170 runs ~2× the equal-safety Rust mirror. Two candidate causes:
the **key walk** (`for k in m.keys()`) or the **probe** (`m.get(k)` inside the
loop body). This probe isolates the walk: same shape as #170's `find`, ~170-entry
`Map[i64, i64]`, 1.2M outer iterations — but **no `get` in the body**, so the
only per-key work is the iterator step.

The body xors each key with the outer index so the inner walk genuinely depends
on `i` and neither compiler can hoist it out. Both versions pay that identical
extra xor. Both print `1620243187968`.

```bash
KARAC_AUTO_PAR=0 karac build walk.kara
rustc -O -C overflow-checks=on walk.rs -o walk_rs
```

## Result (container x86, idle, 5 runs each)

| | before `bef6bbc` | after `bef6bbc` |
|---|---|---|
| **Kāra** | 1.70–1.73 s (~8.3 ns/key) | **0.32–0.36 s** |
| Rust (`-O -C overflow-checks=on`) | 0.23–0.26 s (~1.13 ns/key) | 0.27–0.30 s |
| **ratio** | **~7.4×** | **~1.19×** |

**The walk was the cost, not the probe** — the gap was far wider here than in
#170 itself (~2×), where ~170 `get`s per call diluted it. That diagnosis drove
the fix: LeetCode #170 went 2.06× → 1.20× on the same change.

This probe stays as the regression gate for the inline walk. Re-run it before
and after any change to map iteration.

## Why

`objdump` of the Kāra binary shows `karac_map_iter_next` as a real `call` per
key — it lives in the runtime archive, so LLVM cannot inline through it. Each
step therefore pays: an opaque call, two `ptr::copy_nonoverlapping` writes
through out-parameters with **runtime-variable** `key_size`/`val_size` loaded
from the map header, and an iterator index living in a heap `Box` rather than a
register. Rust's `keys()` is an inlined typed 8-byte load.

(By contrast the mono `karac_map_i64_i64_get` **is** inlined at `-O2` — it is a
`linkonce_odr` function emitted into the module, so LLVM can see through it.
That is the shape the walk needs.)

## Fix (landed — `kara` `bef6bbc`, ledger B-2026-07-24-2)

Codegen now open-codes the scan when both map halves are scalar: for
`slot in 0..capacity`, test `status[slot] == OCCUPIED`, load the halves
straight from `kv[slot*stride]` / `kv[slot*stride + key_size]`. The call, the
out-parameter memcpys and the boxed index go together, and no iterator is
allocated — so `break` and early `return` are leak-free with no cleanup.

Heap halves (`String`/`Vec` key or value) and `SortedMap` deliberately stay on
the runtime iterator: they need the per-element clone/drop it performs.
