#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #1665.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Seq-only kata. Requires: hyperfine, rustc, clang, go, karac.

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

mem_peak() {
    { /usr/bin/time -l "$@" >/dev/null; } 2>&1 \
        | awk '/peak memory footprint/ {print $1}'
}
print_mem() {
    local label="$1" bytes="$2"
    local mib
    mib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1048576}')
    printf '  %-34s %12s bytes (%6s MiB)\n' "$label" "$bytes" "$mib"
}

mkdir -p target

# Equal-safety Rust twin: rustc with overflow checks ON, matching kāra's
# default-checked arithmetic. The runtime-only `rust_ovf` lane overlays this on
# the chart so the safety tax that `rust -O`'s silent wrapping hides is visible.
build_rust_ovf() {
    local src="$1"
    local out="target/$(basename "$src" .rs)_ovf"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling $src (overflow-checks=on, equal-safety) ..." >&2
        rustc -O -C overflow-checks=on "$src" -o "$out"
    fi
}

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
    local out="target/greedy_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust greedy.rs
build_rust_ovf greedy.rs
build_c    greedy.c
build_kara greedy.kara
build_go_seq

expected=$(./target/greedy_kara)
mismatch=""
for pair in \
    'rust:./target/greedy' \
    'rust_ovf:./target/greedy_ovf' \
    'c:./target/greedy_c' \
    'go:./target/greedy_go_seq'; do
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
echo "sink (kara/rust/c/go): $expected"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    py_out=$(python3 greedy.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

# Declare the kata for the JSON feed (no-op when BENCH_JSON=0).
bench_begin id=1665 slug=minimum-initial-energy-to-finish-tasks group=1601-1700 \
    title="Minimum Initial Energy to Finish Tasks" \
    workload="N=50_000 deterministic tasks, K=5 outer iterations" \
    sink="$expected"

echo "=== runtime — short workloads (compiled) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach greedy --lane seq --mode codegen \
    --name 'kara greedy (codegen)' --cmd './target/greedy_kara'
rt_cmd --lang rust --approach greedy --lane seq --mode native \
    --name 'rust greedy' --cmd './target/greedy'
rt_cmd --lang rust_ovf --approach greedy --lane seq --mode native \
    --name 'rust greedy (overflow-checks=on, equal-safety)' --cmd './target/greedy_ovf'
rt_cmd --lang c --approach greedy --lane seq --mode native \
    --name 'c    greedy' --cmd './target/greedy_c'
rt_cmd --lang go --approach greedy --lane seq --mode native \
    --name 'go   greedy' --cmd './target/greedy_go_seq'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 2 --runs 10
rt_cmd --lang python --approach greedy --lane seq --mode interp \
    --name 'py   greedy' --cmd 'python3 greedy.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach greedy --mode codegen \
    --prepare 'rm -f target/greedy_kara greedy' \
    --name 'karac build greedy.kara' \
    --cmd 'sh -c "karac build greedy.kara >/dev/null && mv greedy target/greedy_kara"'
ce_cmd --lang rust --approach greedy --mode native \
    --prepare 'rm -f target/greedy' \
    --name 'rustc -O greedy.rs' --cmd 'rustc -O greedy.rs -o target/greedy'
ce_cmd --lang c --approach greedy --mode native \
    --prepare 'rm -f target/greedy_c' \
    --name 'clang -O3 greedy.c' --cmd 'clang -O3 greedy.c -o target/greedy_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach greedy --lane seq --mode codegen --path target/greedy_kara
size_put --lang rust --approach greedy --lane seq --mode native  --path target/greedy
size_put --lang c    --approach greedy --lane seq --mode native  --path target/greedy_c
size_put --lang go   --approach greedy --lane seq --mode native  --path target/greedy_go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara   --approach greedy --lane seq --mode codegen --bytes "$(mem_peak ./target/greedy_kara)"
mem_put --lang rust   --approach greedy --lane seq --mode native  --bytes "$(mem_peak ./target/greedy)"
mem_put --lang c      --approach greedy --lane seq --mode native  --bytes "$(mem_peak ./target/greedy_c)"
mem_put --lang go     --approach greedy --lane seq --mode native  --bytes "$(mem_peak ./target/greedy_go_seq)"
mem_put --lang python --approach greedy --lane seq --mode interp  --bytes "$(mem_peak python3 greedy.py)"

echo
echo "=== compile memory (cold) ==="
for src in greedy.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in greedy.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in greedy.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit