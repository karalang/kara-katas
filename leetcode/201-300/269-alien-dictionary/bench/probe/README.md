# Probe — half of Go's 2.6× is one unrecognised clear loop

This lane behaved, which is worth saying after the previous two. The twins track
their bases (`c_v3` 343.6 against `c` 345.4; `rust_ovf` 386.3 against `rust`
358.3, the checked build slower as it should be), σ is 2.3–3.4%, and nothing in
the table is impossible. So this one ranks.

The one figure that wanted explaining is **Go at 885.4 ms — 2.56× behind C**, the
largest Go gap in this corpus.

## The clear loop

Every call clears a 676-slot adjacency array. All five mirrors spell it the same
way, as an indexed loop, because that is what the kāra kernel does:

```go
for e := 0; e < 676; e++ {
    adj[e] = false
}
```

Go's compiler recognises a **range-clear** and lowers it to `memclr`. It does not
recognise the indexed form. Swapping only that loop:

```go
for e := range adj {
    adj[e] = false
}
```

| build | mean |
|---|---:|
| Go, indexed clear (the lane) | 880.9 ms ± 19.8 |
| Go, range clear | **604.3 ms ± 9.9** |
| C | 340.0 ms ± 7.4 |

Same sink (`208478711`). The idiom closes **277 ms of the 541 ms gap — about
51%**.

## What that does and does not settle

The remaining 264 ms — Go still 1.78× behind C — is **not identified**. This
probe does not say where it goes, and neither does the lane's README.

It also does not make the lane's Go number unfair. All five mirrors run the same
algorithm, and an indexed clear loop is the same algorithm in every one of them;
C's `memset` and LLVM's recognition of the C loop are the *compilers* doing work
Go's does not. That is a language result, not a parity defect — which is the
distinction this corpus turns on, and the reason the range-clear variant stays a
**probe** rather than replacing the mirror. Rewriting the Go mirror to suit Go's
optimiser, while the other four keep the plain form, is precisely the parity
break that produced a 3× phantom in [#267](../../267-palindrome-permutation-ii/).

## Reproducing

```bash
sed 's|for e := 0; e < 676; e++ {|for e := range adj {|' go-seq/main.go > /tmp/m.go
# (then drop the now-unused bound in the loop header)
hyperfine --warmup 3 -N ./target/alien_go_seq /tmp/go_range_build ./target/alien_c
```

Measured on the x86-64 container lane (4-core Xeon @ 2.80 GHz, go1.24.7,
clang 18.1.3), the same host as `../results.container-x86.json`.
