# 158. Read N Characters Given Read4 II - Call multiple times

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** String · Simulation · Design &nbsp;·&nbsp; **Source:** [leetcode.com/problems/read-n-characters-given-read4-ii-call-multiple-times](https://leetcode.com/problems/read-n-characters-given-read4-ii-call-multiple-times/) &nbsp;·&nbsp; 🔒 **LeetCode Premium**

Like [#157](../157-read-n-characters-given-read4/), a `read4` primitive returns up to **4** characters at a time from a source. But now `read(n)` is called **multiple times** on the same source — so any characters `read4` pulled beyond what one call needed must **persist** for the next call.

```
src="HelloWorld":  read(2)=He  read(3)=llo  read(10)=World  read(1)=""
src="abcdefghij":  read(1)=a   read(5)=bcdef  read(100)=ghij
```

**Constraints:** `1 ≤ n`; `read` is called repeatedly until the source is exhausted.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **persistent leftover buffer** ★ | [`read_n2.kara`](read_n2.kara) ✓ | [`read_n2.py`](read_n2.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

The twist over #157 is **state that survives across calls**. The `Reader` carries a leftover buffer (`buf` + `buf_pos`) in addition to the source cursor (`pos`). Each `read(n)` consumes from `buf` first; only when the buffer drains (`buf_pos >= buf.len()`) does it refill via `read4`, resetting `buf_pos` to 0. A `read4` that returns empty signals EOF and the read stops short. Any surplus characters left in `buf` after `n` are collected simply stay there for the following call.

## Kāra features exercised

- **Cross-call `mut ref Reader` state** — `buf` (a `String` chunk) is reassigned via `rd.buf = read4(rd)` when it drains, and across calls the field already holds the previous chunk. This is exactly the shape that surfaced **[B-2026-07-22-8](https://github.com/karalang/kara/blob/main/docs/bug-ledger.md)**: reassigning a heap-owning `String` struct field through a `mut ref` param leaked the displaced buffer when the field's current value was set by a *prior* call. Fixed in the compiler (not routed around); this kata is its regression surface.
- **String slicing** for the one-char append (`rd.buf[buf_pos..buf_pos+1]`) and chunk build.
- **Free functions + `mut ref` receiver** — no impl blocks; `read` / `read4` / `new_reader` take the `Reader` by `mut ref`.

## Running

```bash
karac run   read_n2.kara
karac build read_n2.kara && ./read_n2
python3 read_n2.py
diff <(karac run read_n2.kara) <(python3 read_n2.py) && echo OK
```

## Notes

A 🔒 **LeetCode-Premium** problem (locked; spec reconstructed from its widely-known description). Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only. This kata found and now guards compiler bug B-2026-07-22-8.
