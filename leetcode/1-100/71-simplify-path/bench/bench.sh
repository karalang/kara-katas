#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #71.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Two-lane kata. The K=1M outer loop reduces via
# `sum = sum + simplify(inputs[k % N]).len()` — karac's auto-par-on-
# reduction recognizes the shape and emits a karac_par_reduce dispatch
# (binary grows ~49 KiB → ~312 KiB, wall drops ~3× via multi-core
# dispatch). Per-iter work is allocation-heavy (Vec[char] snapshot +
# two parallel Vec[i64] stacks + f-string append per output char), so
# the parallel speedup is bounded by the system allocator's per-thread
# contention — a real production characteristic that bears reporting.
# For the BENCH.md seq lane the auto-par regime would mask the per-core
# codegen-vs-rustc comparison the kata corpus is built around, so we
# ship a second kara binary built with KARAC_AUTO_PAR=0 (codegen.rs
# Slice 6 gate — short-circuits all auto-par dispatch back to plain
# sequential compile_block; the documented mechanism for side-by-side
# seq-vs-par benchmarking of the same workload). The default binary
# still gets built so the auto-par number stays reported as the
# production regime.
#
# Requires: hyperfine (`brew install hyperfine`), rustc (rustup), clang,
# go, karac (with --features llvm for the codegen path).

set -euo pipefail
cd "$(dirname "$0")"

require() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "$1 not found — install with: $2" >&2
        exit 1
    fi
}

require hyperfine "brew install hyperfine"
require rustc     "rustup (https://rustup.rs) or 'brew install rustup-init'"
require clang     "xcode-select --install (macOS) or your distro's clang package"
require go        "brew install go  or your distro's golang package"
require karac     "cargo install --path . --features llvm  (from karac-rust checkout)"

# Structured-JSON emission (writes bench/results.json). Set BENCH_JSON=0 to
# skip — the human-readable console output below is unaffected either way.
if [ "${BENCH_JSON:-1}" = "1" ]; then
    require jq      "brew install jq"
    require python3 "python3 ships with macOS; or 'brew install python'"
fi
ROOT="$(cd ../../../.. && pwd)"
. "$ROOT/scripts/bench-lib.sh"

print_mem() {
    local label="$1" bytes="$2"
    local mib
    mib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1048576}')
    printf '  %-40s %12s bytes (%6s MiB)\n' "$label" "$bytes" "$mib"
}

mkdir -p target

build_rust() {
    local src="$1"
    local out="target/$(basename "$src" .rs)"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling $src ..." >&2
        rustc -O "$src" -o "$out"
    fi
}

build_c() {
    local src="$1"
    local out="target/$(basename "$src" .c)_c"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling $src ..." >&2
        clang -O3 "$src" -o "$out"
    fi
}

build_kara() {
    local src="$1"
    local stem="$(basename "$src" .kara)"
    local out="target/${stem}_kara"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling $src (auto-par default) ..." >&2
        karac build "$src" >/dev/null
        mv "$stem" "$out"
    fi
}

build_kara_seq() {
    local src="$1"
    local stem="$(basename "$src" .kara)"
    local out="target/${stem}_kara_seq"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling $src (KARAC_AUTO_PAR=0, seq lane) ..." >&2
        KARAC_AUTO_PAR=0 karac build "$src" >/dev/null
        mv "$stem" "$out"
    fi
}

build_go_seq() {
    local out="target/simplify_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

# Par-lane comparators — hand-tuned parallelism vs Kāra auto-par. Each
# parallelizes the SAME K=1M outer reduction by hand.
build_rayon() {
    local out="target/simplify_rayon"
    local src="rayon/src/main.rs"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "building rayon variant (cargo) ..." >&2
        ( cd rayon && cargo build --release --quiet )
        cp -f "rayon/target/release/simplify_rayon" "$out"
    fi
}
build_go_par() {
    local out="target/simplify_go_par"
    local src="go-par/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-par ..." >&2
        ( cd go-par && go build -o "../$out" . )
    fi
}
# C pthreads — the par-lane bare-metal FLOOR (raw OS threads, no runtime).
build_c_par() {
    local out="target/simplify_c_par"
    local src="simplify_par.c"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling c-par (pthreads) ..." >&2
        clang -O3 "$src" -o "$out" -lpthread
    fi
}

build_rust     simplify.rs
build_c        simplify.c
build_kara     simplify.kara
build_kara_seq simplify.kara
build_go_seq
build_rayon
build_go_par
build_c_par

# Sink agreement — every mirror's stdout must be byte-identical before
# timing. Python skipped from sink check by default — at K=1M the py
# run takes ~0.8s and bench.sh would block on it. Set
# `KARA_BENCH_INCLUDE_PY=1` to opt in.
expected="7500000"
mismatch=""
for pair in \
    'kara:./target/simplify_kara' \
    'kara_seq:./target/simplify_kara_seq' \
    'rust:./target/simplify' \
    'c:./target/simplify_c' \
    'go:./target/simplify_go_seq' \
    'rayon:./target/simplify_rayon' \
    'go_par:./target/simplify_go_par' \
    'c_par:./target/simplify_c_par'; do
    name="${pair%%:*}"
    cmd="${pair#*:}"
    out=$("$cmd")
    if [ "$out" != "$expected" ]; then
        mismatch="$mismatch ${name}=${out}"
    fi
done
if [ -n "$mismatch" ]; then
    echo "sink mismatch (expected=$expected):$mismatch" >&2
    exit 1
fi
echo "sink (kara/kara_seq/rust/c/go): $expected"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    py_out=$(python3 simplify.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

# Declare the kata for the JSON feed (no-op when BENCH_JSON=0).
bench_begin id=71 slug=simplify-path group=1-100 \
    title="Simplify Path" workload="K=1M simplify reduction" \
    sink="$expected"

echo "=== runtime — seq lane (apples-to-apples, single-threaded) ==="
# All four comparators here run single-threaded. The kara binary built
# with KARAC_AUTO_PAR=0 short-circuits auto-par dispatch back to plain
# sequential codegen — this is the row directly comparable to rustc -O /
# clang -O3 / go build on a per-core codegen-quality basis.
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach simplify --lane seq --mode codegen \
    --name 'kara simplify (seq, KARAC_AUTO_PAR=0)' --cmd './target/simplify_kara_seq'
rt_cmd --lang rust --approach simplify --lane seq --mode native \
    --name 'rust simplify' --cmd './target/simplify'
rt_cmd --lang c --approach simplify --lane seq --mode native \
    --name 'c    simplify' --cmd './target/simplify_c'
rt_cmd --lang go --approach simplify --lane seq --mode native \
    --name 'go   simplify' --cmd './target/simplify_go_seq'
rt_end

echo
echo "=== runtime — auto-par regime (kara default, multi-core) ==="
# Default `karac build` output: karac's auto-par-on-reduction recognizes
# the `sum +=` reduction in main's K=1M loop and emits a karac_par_reduce
# dispatch. Multi-core wall-time win on top of the seq lane. NOT directly
# comparable to the single-thread rows above per BENCH.md's two-lane
# discipline — reported separately so the production-default Kara
# behavior stays visible. Heavier warmup (10/50) absorbs worker-pool
# init noise that otherwise inflates σ on short auto-par runs.
rt_begin --warmup 10 --runs 50
rt_cmd --lang kara --approach simplify --lane par --mode codegen \
    --name 'kara simplify (auto-par default)' --cmd './target/simplify_kara'
rt_cmd --lang c --approach simplify --lane par --mode native \
    --name 'c    simplify (pthreads — metal floor)' --cmd './target/simplify_c_par'
rt_cmd --lang rust --approach simplify --lane par --mode native \
    --name 'rust simplify (rayon par_iter)' --cmd './target/simplify_rayon'
rt_cmd --lang go --approach simplify --lane par --mode native \
    --name 'go   simplify (goroutines + WaitGroup)' --cmd './target/simplify_go_par'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 2 --runs 10
rt_cmd --lang python --approach simplify --lane seq --mode interp \
    --name 'py   simplify' --cmd 'python3 simplify.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach simplify --mode codegen \
    --prepare 'rm -f target/simplify_kara simplify' \
    --name 'karac build simplify.kara' \
    --cmd 'sh -c "karac build simplify.kara >/dev/null && mv simplify target/simplify_kara"'
ce_cmd --lang rust --approach simplify --mode native \
    --prepare 'rm -f target/simplify' \
    --name 'rustc -O simplify.rs' --cmd 'rustc -O simplify.rs -o target/simplify'
ce_cmd --lang c --approach simplify --mode native \
    --prepare 'rm -f target/simplify_c' \
    --name 'clang -O3 simplify.c' --cmd 'clang -O3 simplify.c -o target/simplify_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach simplify --lane seq --mode codegen --path target/simplify_kara_seq
size_put --lang kara --approach simplify --lane par --mode codegen --path target/simplify_kara
size_put --lang c    --approach simplify --lane par --mode native  --path target/simplify_c_par
size_put --lang rust --approach simplify --lane par --mode native  --path target/simplify_rayon
size_put --lang go   --approach simplify --lane par --mode native  --path target/simplify_go_par
size_put --lang rust --approach simplify --lane seq --mode native  --path target/simplify
size_put --lang c    --approach simplify --lane seq --mode native  --path target/simplify_c
size_put --lang go   --approach simplify --lane seq --mode native  --path target/simplify_go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach simplify --lane seq --mode codegen --bytes "$(mem_peak ./target/simplify_kara_seq)"
mem_put --lang kara --approach simplify --lane par --mode codegen --bytes "$(mem_peak ./target/simplify_kara)"
mem_put --lang c    --approach simplify --lane par --mode native  --bytes "$(mem_peak ./target/simplify_c_par)"
mem_put --lang rust --approach simplify --lane par --mode native  --bytes "$(mem_peak ./target/simplify_rayon)"
mem_put --lang go   --approach simplify --lane par --mode native  --bytes "$(mem_peak ./target/simplify_go_par)"
mem_put --lang rust --approach simplify --lane seq --mode native  --bytes "$(mem_peak ./target/simplify)"
mem_put --lang c    --approach simplify --lane seq --mode native  --bytes "$(mem_peak ./target/simplify_c)"
mem_put --lang go   --approach simplify --lane seq --mode native  --bytes "$(mem_peak ./target/simplify_go_seq)"
mem_put --lang python --approach simplify --lane seq --mode interp --bytes "$(mem_peak python3 simplify.py)"

echo
echo "=== compile memory (cold) ==="
for src in simplify.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in simplify.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in simplify.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
