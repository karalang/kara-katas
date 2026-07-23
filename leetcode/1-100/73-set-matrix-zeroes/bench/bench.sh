#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #73.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Seq-only kata: the O(1)-space first-row/col marker algorithm (the kata's ★) is
# run K=100_000 times over a freshly built 20×20 matrix — each iteration builds
# the matrix with all non-zero values, punches THREE zeros at k-dependent
# positions, runs set_zeroes in place, and folds the surviving grid into a
# rolling polynomial hash. FAIRNESS: the kata builds the matrix as a Vec-of-Vec
# with Vec.new()+push (a GROWING dynamic array of GROWING rows), so every mirror
# here builds it the same way (Rust Vec<Vec<i64>>::push, Go [][]int64 append, C a
# realloc-doubling vector of realloc-doubling rows, Python list-of-lists append)
# — NOT a fixed 2-D array, which would be an apples-to-oranges heap-vs-stack
# comparison (the #72 lesson). This makes the run allocation-dominated, so it
# measures growing-dynamic-array throughput. The loop-carried hash is NOT a
# reduction karac's auto-par pass can split — the default `karac build` stays
# single-threaded (verified equal to KARAC_AUTO_PAR=0), comparable to rustc -O /
# clang -O3 / go build per-core. Same discipline as kata #72.
#
# Requires: hyperfine, rustc, clang, go, karac (with --features llvm).

set -euo pipefail
cd "$(dirname "$0")"

STEM=set_matrix_zeroes

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
require karac     "cargo install --path . --features llvm  (from kara checkout)"

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
    printf '  %-30s %12s bytes (%6s MiB)\n' "$label" "$bytes" "$mib"
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
    local out="target/${STEM}_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust "${STEM}.rs"
build_c    "${STEM}.c"
build_kara "${STEM}.kara"
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before timing.
# Each iteration builds a 20×20 matrix, punches three zeros, runs set_zeroes and
# folds the surviving grid into `acc = (acc*131 + v) % 1_000_000_007`. Over
# K=100_000 iters the sink is a fixed constant (verified against the Python
# oracle — which here runs the SAME K=100_000, so it is cross-checked too).
expected="222485272"
mismatch=""
for pair in \
    "kara:./target/${STEM}_kara" \
    "rust:./target/${STEM}" \
    "c:./target/${STEM}_c" \
    "go:./target/${STEM}_go_seq" \
    "python:python3 ${STEM}.py"; do
    name="${pair%%:*}"
    cmd="${pair#*:}"
    out=$($cmd)
    if [ "$out" != "$expected" ]; then
        mismatch="$mismatch ${name}=${out}"
    fi
done
if [ -n "$mismatch" ]; then
    echo "sink mismatch (expected=$expected):$mismatch" >&2
    exit 1
fi
echo "sink (kara/rust/c/go/python): $expected"
echo

# Declare the kata for the JSON feed (no-op when BENCH_JSON=0).
bench_begin id=73 slug=set-matrix-zeroes group=1-100 \
    title="Set Matrix Zeroes" \
    workload="K=100_000 O(1)-marker set-zeroes over a freshly built 20x20 Vec-of-Vec matrix (three punched zeros), all storage as growing dynamic arrays / polynomial-hash sink" \
    sink="$expected"

echo "=== runtime — seq lane (apples-to-apples, single-threaded) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach set_matrix_zeroes --lane seq --mode codegen \
    --name "kara ${STEM}" --cmd "./target/${STEM}_kara"
rt_cmd --lang rust --approach set_matrix_zeroes --lane seq --mode native \
    --name "rust ${STEM}" --cmd "./target/${STEM}"
rt_cmd --lang c --approach set_matrix_zeroes --lane seq --mode native \
    --name "c    ${STEM}" --cmd "./target/${STEM}_c"
rt_cmd --lang go --approach set_matrix_zeroes --lane seq --mode native \
    --name "go   ${STEM}" --cmd "./target/${STEM}_go_seq"
rt_end

echo
echo "=== runtime — Python (same K=100_000, cross-checked) ==="
rt_begin --warmup 2 --runs 10
rt_cmd --lang python --approach set_matrix_zeroes --lane seq --mode interp \
    --name "py   ${STEM}" --cmd "python3 ${STEM}.py"
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach set_matrix_zeroes --mode codegen \
    --prepare "rm -f target/${STEM}_kara ${STEM}" \
    --name "karac build ${STEM}.kara" \
    --cmd "sh -c \"karac build ${STEM}.kara >/dev/null && mv ${STEM} target/${STEM}_kara\""
ce_cmd --lang rust --approach set_matrix_zeroes --mode native \
    --prepare "rm -f target/${STEM}" \
    --name "rustc -O ${STEM}.rs" --cmd "rustc -O ${STEM}.rs -o target/${STEM}"
ce_cmd --lang c --approach set_matrix_zeroes --mode native \
    --prepare "rm -f target/${STEM}_c" \
    --name "clang -O3 ${STEM}.c" --cmd "clang -O3 ${STEM}.c -o target/${STEM}_c"
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach set_matrix_zeroes --lane seq --mode codegen --path "target/${STEM}_kara"
size_put --lang rust --approach set_matrix_zeroes --lane seq --mode native  --path "target/${STEM}"
size_put --lang c    --approach set_matrix_zeroes --lane seq --mode native  --path "target/${STEM}_c"
size_put --lang go   --approach set_matrix_zeroes --lane seq --mode native  --path "target/${STEM}_go_seq"

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach set_matrix_zeroes --lane seq --mode codegen --bytes "$(mem_peak ./target/${STEM}_kara)"
mem_put --lang rust --approach set_matrix_zeroes --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM})"
mem_put --lang c    --approach set_matrix_zeroes --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM}_c)"
mem_put --lang go   --approach set_matrix_zeroes --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM}_go_seq)"

echo
echo "=== compile memory (cold) ==="
for src in "${STEM}.kara"; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in "${STEM}.rs"; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in "${STEM}.c"; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
