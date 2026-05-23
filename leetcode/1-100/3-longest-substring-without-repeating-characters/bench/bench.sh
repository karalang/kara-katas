#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #3.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Seq-only kata: the inner loop is one Map.get + one Map.insert per char
# of the 104_000-char input, K=20 outer iterations. Each iteration of the
# inner walk feeds the next (`left` / `last_idx` carry state), so the
# inner loop can't be parallelized; the outer K=20 loop is too small to
# amortize dispatch. Stays single-threaded so the kata measures pure
# codegen quality per the BENCH.md two-lane protocol.
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

# /usr/bin/time -l (macOS BSD time) prints a "peak memory footprint" line on
# stderr. We capture its stderr through a brace-group redirect, discard the
# wrapped command's own stdout, and parse the bytes column. Memory is much
# more stable run-to-run than wall-time (no scheduling/cache variance), so a
# single sample is honest — no hyperfine-style averaging needed.
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
    local out="target/sliding_window_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust sliding_window.rs
build_c    sliding_window.c
build_kara sliding_window.kara
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before
# timing. Python skipped from sink check by default — at N=104K, K=20
# the py run takes ~110 ms and bench.sh would block on it. Set
# `KARA_BENCH_INCLUDE_PY=1` to opt in.
#
# Plain "name:command" pairs (no associative arrays — macOS bash is 3.2).
expected="520"
mismatch=""
for pair in \
    'kara:./target/sliding_window_kara' \
    'rust:./target/sliding_window' \
    'c:./target/sliding_window_c' \
    'go:./target/sliding_window_go_seq'; do
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
    py_out=$(python3 sliding_window.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

echo "=== runtime — short workloads (compiled) ==="
hyperfine \
    --warmup 5 \
    --runs 30 \
    --shell=none \
    --command-name 'kara sliding_window (codegen)' './target/sliding_window_kara' \
    --command-name 'rust sliding_window'           './target/sliding_window' \
    --command-name 'c    sliding_window'           './target/sliding_window_c' \
    --command-name 'go   sliding_window'           './target/sliding_window_go_seq'

echo
echo "=== runtime — long workloads (py) ==="
hyperfine \
    --warmup 2 \
    --runs 10 \
    --shell=none \
    --command-name 'py   sliding_window'           'python3 sliding_window.py'

echo
echo "=== compile elapsed (cold) ==="
# Per BENCH.md: hyperfine --warmup 1 --runs 10 with --prepare deleting the
# build artifact so every invocation is a true cold compile. karac/rustc/clang
# are the single-file compilers; go is excluded — its first invocation mixes
# module resolution + std-lib link and isn't comparable to single-file.
hyperfine \
    --warmup 1 \
    --runs 10 \
    --shell=none \
    --prepare 'rm -f target/sliding_window_kara sliding_window' \
    --command-name 'karac build sliding_window.kara' 'sh -c "karac build sliding_window.kara >/dev/null && mv sliding_window target/sliding_window_kara"' \
    --prepare 'rm -f target/sliding_window' \
    --command-name 'rustc -O sliding_window.rs'      'rustc -O sliding_window.rs -o target/sliding_window' \
    --prepare 'rm -f target/sliding_window_c' \
    --command-name 'clang -O3 sliding_window.c'      'clang -O3 sliding_window.c -o target/sliding_window_c'

echo
echo "=== binary size ==="
for spec in \
    'kara sliding_window:target/sliding_window_kara' \
    'rust sliding_window:target/sliding_window' \
    'c    sliding_window:target/sliding_window_c' \
    'go   sliding_window:target/sliding_window_go_seq'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-30s %10s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem 'kara sliding_window (codegen)' "$(mem_peak ./target/sliding_window_kara)"
print_mem 'rust sliding_window'           "$(mem_peak ./target/sliding_window)"
print_mem 'c    sliding_window'           "$(mem_peak ./target/sliding_window_c)"
print_mem 'go   sliding_window'           "$(mem_peak ./target/sliding_window_go_seq)"
print_mem 'py   sliding_window'           "$(mem_peak python3 sliding_window.py)"

echo
echo "=== compile memory (cold) ==="
# Artifact deleted before each measurement so the karac/rustc/clang invocation
# is a full cold compile. Go is omitted per BENCH.md — `go build`'s first run
# mixes module resolution + std-lib link and is not comparable to a single-file
# rustc/clang/karac invocation.
for src in sliding_window.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    print_mem "karac build $src" "$bytes"
done
for src in sliding_window.rs; do
    out="target/$(basename "$src" .rs)"
    rm -f "$out"
    print_mem "rustc -O $src" "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in sliding_window.c; do
    out="target/$(basename "$src" .c)_c"
    rm -f "$out"
    print_mem "clang -O3 $src" "$(mem_peak clang -O3 "$src" -o "$out")"
done
