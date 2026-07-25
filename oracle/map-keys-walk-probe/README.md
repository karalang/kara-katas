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

| | time | per key |
|---|---|---|
| **Kāra** | 1.70–1.73 s | ~8.3 ns |
| Rust (`-O -C overflow-checks=on`) | 0.23–0.26 s | ~1.13 ns |
| **ratio** | **~7.4×** | |

**The walk is the cost, not the probe.** The gap is far wider here than in #170
itself (~2×), where ~170 `get`s per call dilute it.

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

## Fix direction

Emit a **mono inline bucket walk** in codegen instead of calling the runtime
iterator — statically-known key/val sizes become plain typed loads, the index
stays in a register, and the call disappears. Same trick `get`/`insert` already
use (`get_or_emit_map_mono_methods`, `src/codegen/maps.rs`).
