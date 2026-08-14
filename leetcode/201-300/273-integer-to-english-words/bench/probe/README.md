# Probe — where Kāra's string append actually goes

The lane puts Kāra second of five at 1.048 s, ahead of both Rust builds. That is
a real result on this workload, and it is also a narrow one — so the string
append was measured directly rather than inferred from the lane.

## The lane's algorithm prepends, and prepending is the case nobody can optimize

`out = piece + " " + out` cannot reuse the left buffer in any language. Building
a 3,200-byte string 2,000 times over, appending versus prepending:

| | append `s = s + lit` | prepend `s = lit + s` |
|---|---:|---:|
| Kāra | 52.4 ms | 53.2 ms |
| `rustc -O` | **3.0 ms** | 93.2 ms |

Rust's 93.2 ms is what the work costs when it must be done; its 3.0 ms is what it
costs when the left buffer is extended in place instead. **Kāra pays the prepend
price for both** — the two numbers being equal is the measurement, not the
absolute time. So on this lane's prepending algorithm Kāra is competitive
precisely because the optimization it is missing would not have applied.

## The fast path exists; `+` does not reach it

Same 20,000 appends, three spellings, same 160,000-byte result:

| spelling | time | peak RSS |
|---|---:|---:|
| `s.push_str(x)` | **2.5 ms** | 2,476 KB |
| `s = s + x` | 53.4 ms | 2,804 KB |
| `s += x` | 6.1 s | **1,565,032 KB** |

`push_str` matches Rust, so the amortized in-place growth is implemented — `+`
just never reaches it ([`B-2026-08-14-23`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.md)).

And `+=` is worse than slow. 1.5 GB of RSS for a 160 KB string is exactly
`sum(8i, i=1..20000)` — every intermediate buffer, never freed
([`B-2026-08-14-22`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.md)).
Through a `mut ref String` parameter the same operator silently drops the append
altogether and the caller sees an empty string
([`B-2026-08-14-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.md)).

## Scope for optimization

One change closes all three: lower `s += x`, and `s = s + x` where the target is
the left operand, to the in-place append `push_str` already performs. That is a
21× constant factor on the most common way to build a string in a loop, and it is
the likely explanation for the corpus's long-standing observation
(`SWEEP_TRACKER_v2`, `B-2026-07-18-8`) that the `kara`/`rust_ovf` ≥ 1.15 cluster
is dominated by String-concat and char-append katas.

It would not move this lane, which prepends.

## Reproducing

```bash
# append vs prepend, Kāra and Rust
cat > app.kara <<'K'
fn main() {
    let mut sink = 0i64; let mut r = 0i64;
    while r < 2000i64 {
        let mut s = ""; let mut i = 0i64;
        while i < 400i64 { s = s + "abcdefgh"; i = i + 1i64; }
        sink = (sink + s.len()) % 1000000007i64; r = r + 1i64;
    }
    println(sink);
}
K
# ... and the same with `s = "abcdefgh" + s`, `s.push_str(...)`, `s += ...`
karac build app.kara && hyperfine -w 2 -r 10 ./app

# the leak
/usr/bin/time -v ./pluseq 2>&1 | grep "Maximum resident"
```
