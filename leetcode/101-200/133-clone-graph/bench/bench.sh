#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #133.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Seq lane: clone_bfs across kara/rust/c/go (N=2000 ring, K=500).
# Par lane: kara clone_bfs_par (18-way) only — NOT cross-lane with rust.
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
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling $src ..." >&2
        karac build "$src" >/dev/null
        mv "$stem" "$out"
    fi
}

build_go_seq() {
    local pkg="$1"
    local out="target/${pkg}_go_seq"
    local src="go-seq/${pkg}/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-seq/${pkg} ..." >&2
        ( cd go-seq && go build -o "../$out" "./${pkg}" )
    fi
}

build_rust clone_bfs.rs
build_c    clone_bfs.c
build_kara clone_bfs.kara
build_kara clone_bfs_par.kara
build_go_seq clone_bfs

expected="500"
mismatch=""
for pair in \
    'seq_kara:./target/clone_bfs_kara' \
    'seq_rust:./target/clone_bfs' \
    'seq_c:./target/clone_bfs_c' \
    'seq_go:./target/clone_bfs_go_seq' \
    'par_kara:./target/clone_bfs_par_kara'; do
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
echo "sink seq (kara/rust/c/go): $expected"
echo "sink par (kara clone_bfs_par): $expected"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    py=$(python3 clone_bfs.py)
    if [ "$py" != "$expected" ]; then
        echo "python sink mismatch: py=$py" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

echo "=== runtime — seq lane (clone_bfs, N=2000 ring, K=500) ==="
hyperfine \
    --warmup 5 \
    --runs 30 \
    --shell=none \
    --command-name 'kara clone_bfs (codegen)' './target/clone_bfs_kara' \
    --command-name 'rust clone_bfs'             './target/clone_bfs' \
    --command-name 'c    clone_bfs'             './target/clone_bfs_c' \
    --command-name 'go   clone_bfs'             './target/clone_bfs_go_seq'

echo
echo "=== runtime — par lane (kara clone_bfs par 18-way only) ==="
hyperfine \
    --warmup 5 \
    --runs 30 \
    --shell=none \
    --command-name 'kara clone_bfs (par 18-way)' './target/clone_bfs_par_kara'

if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    echo
    echo "=== runtime — python ==="
    hyperfine \
        --warmup 5 \
        --runs 30 \
        --shell=none \
        --command-name 'py   clone_bfs' 'python3 clone_bfs.py'
fi

echo
echo "=== compile elapsed (cold) ==="
hyperfine \
    --warmup 1 \
    --runs 10 \
    --shell=none \
    --prepare 'rm -f target/clone_bfs_kara clone_bfs' \
    --command-name 'karac build clone_bfs.kara'     'sh -c "karac build clone_bfs.kara >/dev/null && mv clone_bfs target/clone_bfs_kara"' \
    --prepare 'rm -f target/clone_bfs_par_kara clone_bfs_par' \
    --command-name 'karac build clone_bfs_par.kara' 'sh -c "karac build clone_bfs_par.kara >/dev/null && mv clone_bfs_par target/clone_bfs_par_kara"' \
    --prepare 'rm -f target/clone_bfs' \
    --command-name 'rustc -O clone_bfs.rs'          'rustc -O clone_bfs.rs -o target/clone_bfs' \
    --prepare 'rm -f target/clone_bfs_c' \
    --command-name 'clang -O3 clone_bfs.c'          'clang -O3 clone_bfs.c -o target/clone_bfs_c'

echo
echo "=== binary size ==="
for spec in \
    'kara clone_bfs (codegen):target/clone_bfs_kara' \
    'kara clone_bfs (par 18-way):target/clone_bfs_par_kara' \
    'rust clone_bfs:target/clone_bfs' \
    'c    clone_bfs:target/clone_bfs_c' \
    'go   clone_bfs:target/clone_bfs_go_seq'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-30s %10s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem 'kara clone_bfs (codegen)'    "$(mem_peak ./target/clone_bfs_kara)"
print_mem 'kara clone_bfs (par 18-way)' "$(mem_peak ./target/clone_bfs_par_kara)"
print_mem 'rust clone_bfs'              "$(mem_peak ./target/clone_bfs)"
print_mem 'c    clone_bfs'              "$(mem_peak ./target/clone_bfs_c)"
print_mem 'go   clone_bfs'              "$(mem_peak ./target/clone_bfs_go_seq)"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    print_mem 'py   clone_bfs' "$(mem_peak python3 clone_bfs.py)"
fi

echo
echo "=== compile memory (cold) ==="
for src in clone_bfs.kara clone_bfs_par.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    print_mem "karac build $src" "$bytes"
done
rm -f target/clone_bfs
print_mem "rustc -O clone_bfs.rs" "$(mem_peak rustc -O clone_bfs.rs -o target/clone_bfs)"
rm -f target/clone_bfs_c
print_mem "clang -O3 clone_bfs.c" "$(mem_peak clang -O3 clone_bfs.c -o target/clone_bfs_c)"
