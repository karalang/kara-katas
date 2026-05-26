#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #153.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Multi-approach kata: linear_scan (K=10) and binary_search (K=2_000_000)
# share one bench.sh with separate runtime hyperfine batches per approach.
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
    local pkg="$1"
    local out="target/${pkg}_go_seq"
    local src="go-seq/${pkg}/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-seq/${pkg} ..." >&2
        ( cd go-seq && go build -o "../$out" "./${pkg}" )
    fi
}

build_rust linear_scan.rs
build_rust binary_search.rs
build_c    linear_scan.c
build_c    binary_search.c
build_kara linear_scan.kara
build_kara binary_search.kara
build_go_seq linear_scan
build_go_seq binary_search

expected_ls="10"
mismatch_ls=""
for pair in \
    'ls_kara:./target/linear_scan_kara' \
    'ls_rust:./target/linear_scan' \
    'ls_c:./target/linear_scan_c' \
    'ls_go:./target/linear_scan_go_seq'; do
    name="${pair%%:*}"
    cmd="${pair#*:}"
    out=$("$cmd")
    if [ "$out" != "$expected_ls" ]; then
        mismatch_ls="$mismatch_ls ${name}=${out}"
    fi
done
if [ -n "$mismatch_ls" ]; then
    echo "linear_scan sink mismatch (expected=$expected_ls):$mismatch_ls" >&2
    exit 1
fi
echo "sink linear_scan (kara/rust/c/go): $expected_ls"

expected_bs="2000000"
mismatch_bs=""
for pair in \
    'bs_kara:./target/binary_search_kara' \
    'bs_rust:./target/binary_search' \
    'bs_c:./target/binary_search_c' \
    'bs_go:./target/binary_search_go_seq'; do
    name="${pair%%:*}"
    cmd="${pair#*:}"
    out=$("$cmd")
    if [ "$out" != "$expected_bs" ]; then
        mismatch_bs="$mismatch_bs ${name}=${out}"
    fi
done
if [ -n "$mismatch_bs" ]; then
    echo "binary_search sink mismatch (expected=$expected_bs):$mismatch_bs" >&2
    exit 1
fi
echo "sink binary_search (kara/rust/c/go): $expected_bs"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    py_ls=$(python3 linear_scan.py)
    py_bs=$(python3 binary_search.py)
    if [ "$py_ls" != "$expected_ls" ] || [ "$py_bs" != "$expected_bs" ]; then
        echo "python sink mismatch: py_ls=$py_ls py_bs=$py_bs" >&2
        exit 1
    fi
    echo "python: matches both approaches"
fi
echo

echo "=== runtime — linear_scan (compiled, K=10) ==="
hyperfine \
    --warmup 5 \
    --runs 30 \
    --shell=none \
    --command-name 'kara linear_scan (codegen)' './target/linear_scan_kara' \
    --command-name 'rust linear_scan'           './target/linear_scan' \
    --command-name 'c    linear_scan'           './target/linear_scan_c' \
    --command-name 'go   linear_scan'           './target/linear_scan_go_seq'

echo
echo "=== runtime — binary_search (compiled, K=2_000_000) ==="
hyperfine \
    --warmup 5 \
    --runs 30 \
    --shell=none \
    --command-name 'kara binary_search (codegen)' './target/binary_search_kara' \
    --command-name 'rust binary_search'           './target/binary_search' \
    --command-name 'c    binary_search'           './target/binary_search_c' \
    --command-name 'go   binary_search'           './target/binary_search_go_seq'

if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    echo
    echo "=== runtime — python ==="
    hyperfine \
        --warmup 5 \
        --runs 30 \
        --shell=none \
        --command-name 'py   linear_scan'   'python3 linear_scan.py' \
        --command-name 'py   binary_search' 'python3 binary_search.py'
fi

echo
echo "=== compile elapsed (cold) ==="
hyperfine \
    --warmup 1 \
    --runs 10 \
    --shell=none \
    --prepare 'rm -f target/linear_scan_kara linear_scan' \
    --command-name 'karac build linear_scan.kara'   'sh -c "karac build linear_scan.kara >/dev/null && mv linear_scan target/linear_scan_kara"' \
    --prepare 'rm -f target/binary_search_kara binary_search' \
    --command-name 'karac build binary_search.kara' 'sh -c "karac build binary_search.kara >/dev/null && mv binary_search target/binary_search_kara"' \
    --prepare 'rm -f target/linear_scan' \
    --command-name 'rustc -O linear_scan.rs'        'rustc -O linear_scan.rs -o target/linear_scan' \
    --prepare 'rm -f target/binary_search' \
    --command-name 'rustc -O binary_search.rs'      'rustc -O binary_search.rs -o target/binary_search' \
    --prepare 'rm -f target/linear_scan_c' \
    --command-name 'clang -O3 linear_scan.c'      'clang -O3 linear_scan.c -o target/linear_scan_c' \
    --prepare 'rm -f target/binary_search_c' \
    --command-name 'clang -O3 binary_search.c'    'clang -O3 binary_search.c -o target/binary_search_c'

echo
echo "=== binary size ==="
for spec in \
    'kara linear_scan:target/linear_scan_kara' \
    'kara binary_search:target/binary_search_kara' \
    'rust linear_scan:target/linear_scan' \
    'rust binary_search:target/binary_search' \
    'c    linear_scan:target/linear_scan_c' \
    'c    binary_search:target/binary_search_c' \
    'go   linear_scan:target/linear_scan_go_seq' \
    'go   binary_search:target/binary_search_go_seq'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-30s %10s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem 'kara linear_scan (codegen)'   "$(mem_peak ./target/linear_scan_kara)"
print_mem 'rust linear_scan'             "$(mem_peak ./target/linear_scan)"
print_mem 'c    linear_scan'             "$(mem_peak ./target/linear_scan_c)"
print_mem 'go   linear_scan'             "$(mem_peak ./target/linear_scan_go_seq)"
print_mem 'kara binary_search (codegen)' "$(mem_peak ./target/binary_search_kara)"
print_mem 'rust binary_search'           "$(mem_peak ./target/binary_search)"
print_mem 'c    binary_search'           "$(mem_peak ./target/binary_search_c)"
print_mem 'go   binary_search'           "$(mem_peak ./target/binary_search_go_seq)"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    print_mem 'py   linear_scan'   "$(mem_peak python3 linear_scan.py)"
    print_mem 'py   binary_search' "$(mem_peak python3 binary_search.py)"
fi

echo
echo "=== compile memory (cold) ==="
for src in linear_scan.kara binary_search.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    print_mem "karac build $src" "$bytes"
done
for src in linear_scan.rs binary_search.rs; do
    out="target/$(basename "$src" .rs)"
    rm -f "$out"
    print_mem "rustc -O $src" "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in linear_scan.c binary_search.c; do
    out="target/$(basename "$src" .c)_c"
    rm -f "$out"
    print_mem "clang -O3 $src" "$(mem_peak clang -O3 "$src" -o "$out")"
done
