#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #1.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Seq-only kata: brute_force's per-call work (~12.5M comparisons) is
# small enough that a par lane would mostly measure dispatch overhead;
# hash_map's per-call work (~5K inserts) is even smaller. Both stay
# single-threaded so the kata measures pure codegen quality per the
# BENCH.md two-lane protocol.
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
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling $src ..." >&2
        karac build "$src" >/dev/null
        mv "$stem" "$out"
    fi
}

# Two-sum has two algorithmic approaches, so we keep a single go module
# (bench/go-seq/) with two main packages (./brute_force, ./hash_map).
# Each builds into target/<approach>_go_seq.
build_go_seq() {
    local pkg="$1"           # subpackage name (e.g. brute_force)
    local out="target/${pkg}_go_seq"
    local src="go-seq/${pkg}/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-seq/${pkg} ..." >&2
        ( cd go-seq && go build -o "../$out" "./${pkg}" )
    fi
}

build_rust brute_force.rs
build_rust hash_map.rs
build_c    brute_force.c
build_c    hash_map.c
build_kara brute_force.kara
build_kara hash_map.kara
build_go_seq brute_force
build_go_seq hash_map

# Sink agreement — every mirror's stdout must be byte-identical before
# timing. Python skipped from sink check by default — at N=5000 the
# brute-force py run takes ~1.5s and bench.sh would block on it.
# Set `KARA_BENCH_INCLUDE_PY=1` to opt in.
#
# Plain "name:command" pairs (no associative arrays — macOS bash is 3.2).
expected="-20"
mismatch=""
for pair in \
    'bf_kara:./target/brute_force_kara' \
    'bf_rust:./target/brute_force' \
    'bf_c:./target/brute_force_c' \
    'bf_go:./target/brute_force_go_seq' \
    'hm_kara:./target/hash_map_kara' \
    'hm_rust:./target/hash_map' \
    'hm_c:./target/hash_map_c' \
    'hm_go:./target/hash_map_go_seq'; do
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
echo "sink (all eight: kara/rust/c/go × brute_force/hash_map): $expected"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    py_bf=$(python3 brute_force.py)
    py_hm=$(python3 hash_map.py)
    if [ "$py_bf" != "$expected" ] || [ "$py_hm" != "$expected" ]; then
        echo "python sink mismatch: py_bf=$py_bf py_hm=$py_hm" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

# Two runtime batches because the workloads span ~5 orders of magnitude:
#   - short workloads (<50ms): hash_map across all langs, brute_force in
#     compiled languages. Need 30 runs to drown startup jitter.
#   - long workloads (>1s): kara interp on both approaches, py brute_force.
#     Already <2% RSD at 10 runs; bumping runs adds wall without info.
echo "=== runtime — short workloads ==="
hyperfine \
    --warmup 5 \
    --runs 30 \
    --shell=none \
    --command-name 'kara brute_force (codegen)' './target/brute_force_kara' \
    --command-name 'rust brute_force'           './target/brute_force' \
    --command-name 'c    brute_force'           './target/brute_force_c' \
    --command-name 'go   brute_force'           './target/brute_force_go_seq' \
    --command-name 'kara hash_map (codegen)'    './target/hash_map_kara' \
    --command-name 'rust hash_map'              './target/hash_map' \
    --command-name 'c    hash_map'              './target/hash_map_c' \
    --command-name 'go   hash_map'              './target/hash_map_go_seq' \
    --command-name 'py   hash_map'              'python3 hash_map.py'

echo
echo "=== runtime — long workloads (interp + py brute_force) ==="
hyperfine \
    --warmup 2 \
    --runs 10 \
    --shell=none \
    --command-name 'kara hash_map (interp)'     'karac run hash_map.kara' \
    --command-name 'py   brute_force'           'python3 brute_force.py'

echo
echo "=== compile elapsed (cold) ==="
# Per BENCH.md: hyperfine --warmup 1 --runs 10 with --prepare deleting the
# build artifact so every invocation is a true cold compile. karac/rustc/clang
# are the single-file compilers; rayon (cargo) and go are excluded — their
# first invocation mixes dep resolution + link and isn't comparable to a
# single-file compile.
hyperfine \
    --warmup 1 \
    --runs 10 \
    --shell=none \
    --prepare 'rm -f target/brute_force_kara brute_force' \
    --command-name 'karac build brute_force.kara' 'sh -c "karac build brute_force.kara >/dev/null && mv brute_force target/brute_force_kara"' \
    --prepare 'rm -f target/hash_map_kara hash_map' \
    --command-name 'karac build hash_map.kara'    'sh -c "karac build hash_map.kara >/dev/null && mv hash_map target/hash_map_kara"' \
    --prepare 'rm -f target/brute_force' \
    --command-name 'rustc -O brute_force.rs'      'rustc -O brute_force.rs -o target/brute_force' \
    --prepare 'rm -f target/hash_map' \
    --command-name 'rustc -O hash_map.rs'         'rustc -O hash_map.rs -o target/hash_map' \
    --prepare 'rm -f target/brute_force_c' \
    --command-name 'clang -O3 brute_force.c'      'clang -O3 brute_force.c -o target/brute_force_c' \
    --prepare 'rm -f target/hash_map_c' \
    --command-name 'clang -O3 hash_map.c'         'clang -O3 hash_map.c -o target/hash_map_c'

echo
echo "=== binary size ==="
for spec in \
    'kara brute_force:target/brute_force_kara' \
    'kara hash_map:target/hash_map_kara' \
    'rust brute_force:target/brute_force' \
    'rust hash_map:target/hash_map' \
    'c    brute_force:target/brute_force_c' \
    'c    hash_map:target/hash_map_c' \
    'go   brute_force:target/brute_force_go_seq' \
    'go   hash_map:target/hash_map_go_seq'; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-30s %10s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
# python's number includes ~7 MB CPython runtime baseline regardless of N.
# `interp` rows include the karac binary itself (~7 MB with --features llvm)
# plus the AST/value heap karac walks at runtime — `karac run` re-runs
# lex → … → ownership → tree-walk every invocation, so the number measures
# interpreter overhead + algorithm working set, not algorithm alone.
print_mem 'kara brute_force (codegen)' "$(mem_peak ./target/brute_force_kara)"
print_mem 'kara hash_map (codegen)'    "$(mem_peak ./target/hash_map_kara)"
print_mem 'kara hash_map (interp)'     "$(mem_peak karac run hash_map.kara)"
print_mem 'rust brute_force'           "$(mem_peak ./target/brute_force)"
print_mem 'rust hash_map'              "$(mem_peak ./target/hash_map)"
print_mem 'c    brute_force'           "$(mem_peak ./target/brute_force_c)"
print_mem 'c    hash_map'              "$(mem_peak ./target/hash_map_c)"
print_mem 'go   brute_force'           "$(mem_peak ./target/brute_force_go_seq)"
print_mem 'go   hash_map'              "$(mem_peak ./target/hash_map_go_seq)"
print_mem 'py   brute_force'           "$(mem_peak python3 brute_force.py)"
print_mem 'py   hash_map'              "$(mem_peak python3 hash_map.py)"

echo
echo "=== compile memory (cold) ==="
# Artifact deleted before each measurement so the karac/rustc/clang invocation
# is a full cold compile. karac's number covers lex → … → ownership → codegen IR
# build → LLVM optimization passes. Regression detection: a sudden 10× spike
# on `karac build` here is the signature of an algorithmic blowup in a
# frontend phase. Go is omitted from the compile-memory row per BENCH.md —
# `go build`'s first run mixes module resolution + std-lib link and is not
# comparable to a single-file rustc/clang/karac invocation.
for src in brute_force.kara hash_map.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    print_mem "karac build $src" "$bytes"
done
for src in brute_force.rs hash_map.rs; do
    out="target/$(basename "$src" .rs)"
    rm -f "$out"
    print_mem "rustc -O $src" "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in brute_force.c hash_map.c; do
    out="target/$(basename "$src" .c)_c"
    rm -f "$out"
    print_mem "clang -O3 $src" "$(mem_peak clang -O3 "$src" -o "$out")"
done
