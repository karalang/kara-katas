#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #5.
# See ../README.md § Benchmarks for what these numbers mean.
#
# expand_around_center runs a K=100 outer loop of independent read-only O(n²)
# longest-palindrome scans (n = 5000 'a' chars, the worst-case shape), so
# Kāra's cost model auto-parallelizes it (post trip-count fix). It therefore
# carries BOTH lanes: a seq twin (KARAC_AUTO_PAR=0) in the seq lane and the
# auto-par binary in the par lane, compared against rayon / pthreads-C /
# goroutine-Go hand-tuned-parallel mirrors. The kara auto-par binary writes no
# parallel code — the engagement is the compiler's, vs the hand-tuned mirrors.
#
# python is benched on the same workload but timed separately (tree-walk /
# pure-Python O(n²)·K is far slower; it is a reference point, not a peer).
#
# Requires: hyperfine (`brew install hyperfine`), rustc (rustup), clang,
# go, karac.

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
    printf '  %-34s %12s bytes (%6s MiB)\n' "$label" "$bytes" "$mib"
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
        echo "compiling $src ..." >&2
        karac build "$src" >/dev/null
        mv "$stem" "$out"
    fi
}

build_go_seq() {
    local out="target/expand_around_center_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

# --- par-lane builders (hand-tuned-parallel comparators for auto-par) --------
# kara seq twin: same source, KARAC_AUTO_PAR=0 forces the single-threaded
# lowering so the seq lane is a true single-thread baseline (the default build
# auto-parallelizes expand_around_center after the cost-model trip-count fix).
build_kara_seq() {
    local src="$1"
    local stem="$(basename "$src" .kara)"
    local out="target/${stem}_kara_seq"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling $src (seq twin, KARAC_AUTO_PAR=0) ..." >&2
        KARAC_AUTO_PAR=0 karac build "$src" >/dev/null
        mv "$stem" "$out"
    fi
}

# rayon cargo project (bench/rayon/, package lps_rayon). cargo's own
# incremental check is the freshness gate.
build_rust_rayon() {
    local bin="$1"
    echo "compiling rayon/$bin ..." >&2
    ( cd rayon && cargo build --release --quiet )
    cp "rayon/target/release/$bin" "target/$bin"
}

# pthreads-C par mirror; -lpthread, output target/<stem>_c.
build_c_par() {
    local src="$1"
    local out="target/$(basename "$src" .c)_c"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling $src ..." >&2
        clang -O3 "$src" -o "$out" -lpthread
    fi
}

# goroutine-Go par mirror (bench/go-par/, module lps_go_par).
build_go_par() {
    local bin="$1"
    local out="target/$bin"
    local src="go-par/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-par/$bin ..." >&2
        ( cd go-par && go build -o "../$out" . )
    fi
}

build_rust expand_around_center.rs
build_c    expand_around_center.c
build_kara expand_around_center.kara          # auto-par (par lane)
build_kara_seq expand_around_center.kara      # seq twin (seq lane)
build_go_seq
# par-lane comparators for expand_around_center
build_rust_rayon lps_rayon
build_c_par      expand_around_center_par.c
build_go_par     lps_go_par

# Sink agreement — every compiled mirror's stdout must be byte-identical
# before timing. Sink = K=100 × (best_start 0 + best_len 5000) = 500000.
expected="500000"
mismatch=""
for pair in \
    'kara_seq:./target/expand_around_center_kara_seq' \
    'kara_par:./target/expand_around_center_kara' \
    'rust:./target/expand_around_center' \
    'c:./target/expand_around_center_c' \
    'go:./target/expand_around_center_go_seq' \
    'rayon:./target/lps_rayon' \
    'c_par:./target/expand_around_center_par_c' \
    'go_par:./target/lps_go_par'; do
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
echo "sink (kara seq+par/rust/c/go + rayon/c-par/go-par): $expected"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    py_out=$(python3 expand_around_center.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

# Declare the kata for the JSON feed (no-op when BENCH_JSON=0).
bench_begin id=5 slug=longest-palindromic-substring group=1-100 \
    title="Longest Palindromic Substring" \
    workload="expand_around_center n=5000, K=100; O(n²) (py timed separately)" \
    sink="$expected"

echo "=== runtime — seq lane ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach expand_around_center --lane seq --mode codegen \
    --name 'kara expand_around_center (seq twin)' --cmd './target/expand_around_center_kara_seq'
rt_cmd --lang rust --approach expand_around_center --lane seq --mode native \
    --name 'rust expand_around_center' --cmd './target/expand_around_center'
rt_cmd --lang c --approach expand_around_center --lane seq --mode native \
    --name 'c    expand_around_center' --cmd './target/expand_around_center_c'
rt_cmd --lang go --approach expand_around_center --lane seq --mode native \
    --name 'go   expand_around_center' --cmd './target/expand_around_center_go_seq'
rt_end

echo
echo "=== runtime — par lane (expand_around_center, K=100 auto-par vs hand-tuned) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach expand_around_center --lane par --mode codegen \
    --name 'kara expand_around_center (auto-par)' --cmd './target/expand_around_center_kara'
rt_cmd --lang rust --approach expand_around_center --lane par --mode native \
    --name 'rust expand_around_center (rayon)' --cmd './target/lps_rayon'
rt_cmd --lang c --approach expand_around_center --lane par --mode native \
    --name 'c    expand_around_center (pthreads)' --cmd './target/expand_around_center_par_c'
rt_cmd --lang go --approach expand_around_center --lane par --mode native \
    --name 'go   expand_around_center (goroutines)' --cmd './target/lps_go_par'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 2 --runs 10
rt_cmd --lang python --approach expand_around_center --lane seq --mode interp \
    --name 'py   expand_around_center' --cmd 'python3 expand_around_center.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach expand_around_center --mode codegen \
    --prepare 'rm -f target/expand_around_center_kara expand_around_center' \
    --name 'karac build expand_around_center.kara' \
    --cmd 'sh -c "karac build expand_around_center.kara >/dev/null && mv expand_around_center target/expand_around_center_kara"'
ce_cmd --lang rust --approach expand_around_center --mode native \
    --prepare 'rm -f target/expand_around_center' \
    --name 'rustc -O expand_around_center.rs' --cmd 'rustc -O expand_around_center.rs -o target/expand_around_center'
ce_cmd --lang c --approach expand_around_center --mode native \
    --prepare 'rm -f target/expand_around_center_c' \
    --name 'clang -O3 expand_around_center.c' --cmd 'clang -O3 expand_around_center.c -o target/expand_around_center_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach expand_around_center --lane seq --mode codegen --path target/expand_around_center_kara_seq
size_put --lang kara --approach expand_around_center --lane par --mode codegen --path target/expand_around_center_kara
size_put --lang rust --approach expand_around_center --lane seq --mode native  --path target/expand_around_center
size_put --lang rust --approach expand_around_center --lane par --mode native  --path target/lps_rayon
size_put --lang c    --approach expand_around_center --lane seq --mode native  --path target/expand_around_center_c
size_put --lang c    --approach expand_around_center --lane par --mode native  --path target/expand_around_center_par_c
size_put --lang go   --approach expand_around_center --lane seq --mode native  --path target/expand_around_center_go_seq
size_put --lang go   --approach expand_around_center --lane par --mode native  --path target/lps_go_par

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach expand_around_center --lane seq --mode codegen --bytes "$(mem_peak ./target/expand_around_center_kara_seq)"
mem_put --lang kara --approach expand_around_center --lane par --mode codegen --bytes "$(mem_peak ./target/expand_around_center_kara)"
mem_put --lang rust --approach expand_around_center --lane seq --mode native  --bytes "$(mem_peak ./target/expand_around_center)"
mem_put --lang rust --approach expand_around_center --lane par --mode native  --bytes "$(mem_peak ./target/lps_rayon)"
mem_put --lang c    --approach expand_around_center --lane seq --mode native  --bytes "$(mem_peak ./target/expand_around_center_c)"
mem_put --lang c    --approach expand_around_center --lane par --mode native  --bytes "$(mem_peak ./target/expand_around_center_par_c)"
mem_put --lang go   --approach expand_around_center --lane seq --mode native  --bytes "$(mem_peak ./target/expand_around_center_go_seq)"
mem_put --lang go   --approach expand_around_center --lane par --mode native  --bytes "$(mem_peak ./target/lps_go_par)"
mem_put --lang python --approach expand_around_center --lane seq --mode interp --bytes "$(mem_peak python3 expand_around_center.py)"

echo
echo "=== compile memory (cold) ==="
for src in expand_around_center.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in expand_around_center.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in expand_around_center.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
