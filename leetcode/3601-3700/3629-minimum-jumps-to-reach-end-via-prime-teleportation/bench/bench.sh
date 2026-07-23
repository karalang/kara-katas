#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #3629.
# See ../README.md § Benchmarks for what these numbers mean.
#
# One approach (bfs_sieve): BFS over an index graph whose prime-teleport edges
# come from an O(cap log log cap) factor sieve. The K=50 outer loop is a batch
# of independent, read-only min_jumps calls reduced into a sum sink, so Kāra's
# cost model auto-parallelizes it (post trip-count fix). It therefore carries
# BOTH lanes: a seq twin (KARAC_AUTO_PAR=0) in the seq lane and the auto-par
# binary in the par lane, compared against rayon / pthreads-C / goroutine-Go
# hand-tuned-parallel mirrors. The seq lane also carries the rust/c/go
# single-threaded baselines; python is benched seq-only (tree-walk over the
# sieve is impractical to parallelize and slow enough to keep on its own block).
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
    local out="target/bfs_sieve_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

# --- par-lane builders (hand-tuned-parallel comparators for auto-par) --------
# kara seq twin: same source, KARAC_AUTO_PAR=0 forces the single-threaded
# lowering so the seq lane is a true single-thread baseline (the default build
# auto-parallelizes bfs_sieve after the cost-model trip-count fix).
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

# rayon cargo project (bench/rayon/, package bfs_sieve_rayon). cargo's own
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

# goroutine-Go par mirror (bench/go-par/, module bfs_sieve_go_par).
build_go_par() {
    local bin="$1"
    local out="target/$bin"
    local src="go-par/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-par/$bin ..." >&2
        ( cd go-par && go build -o "../$out" . )
    fi
}

build_rust bfs_sieve.rs
build_c    bfs_sieve.c
build_kara bfs_sieve.kara          # auto-par (par lane)
build_kara_seq bfs_sieve.kara      # seq twin (seq lane)
build_go_seq
# par-lane comparators for bfs_sieve
build_rust_rayon bfs_sieve_rayon
build_c_par      bfs_sieve_par.c
build_go_par     bfs_sieve_go_par

# Sink agreement — every compiled mirror's stdout must be byte-identical
# before timing. Sink = 24350 (K=50 × per-call result 487).
expected="24350"
mismatch=""
for pair in \
    'kara_seq:./target/bfs_sieve_kara_seq' \
    'kara_par:./target/bfs_sieve_kara' \
    'rust:./target/bfs_sieve' \
    'c:./target/bfs_sieve_c' \
    'go:./target/bfs_sieve_go_seq' \
    'rayon:./target/bfs_sieve_rayon' \
    'c_par:./target/bfs_sieve_par_c' \
    'go_par:./target/bfs_sieve_go_par'; do
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
    py_out=$(python3 bfs_sieve.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

# Declare the kata for the JSON feed (no-op when BENCH_JSON=0).
bench_begin id=3629 slug=minimum-jumps-to-reach-end-via-prime-teleportation group=3601-3700 \
    title="Minimum Jumps to Reach End via Prime Teleportation" \
    workload="N=50,000 nums (values up to 10^6), cap=10^6 sieve, K=50 outer iterations" \
    sink="$expected"

echo "=== runtime — seq lane (compiled) ==="
rt_begin --warmup 2 --runs 10
rt_cmd --lang kara --approach bfs_sieve --lane seq --mode codegen \
    --name 'kara bfs_sieve (seq twin)' --cmd './target/bfs_sieve_kara_seq'
rt_cmd --lang rust --approach bfs_sieve --lane seq --mode native \
    --name 'rust bfs_sieve' --cmd './target/bfs_sieve'
rt_cmd --lang c --approach bfs_sieve --lane seq --mode native \
    --name 'c    bfs_sieve' --cmd './target/bfs_sieve_c'
rt_cmd --lang go --approach bfs_sieve --lane seq --mode native \
    --name 'go   bfs_sieve' --cmd './target/bfs_sieve_go_seq'
rt_end

echo
echo "=== runtime — par lane (bfs_sieve, K=50 auto-par vs hand-tuned) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach bfs_sieve --lane par --mode codegen \
    --name 'kara bfs_sieve (auto-par)' --cmd './target/bfs_sieve_kara'
rt_cmd --lang rust --approach bfs_sieve --lane par --mode native \
    --name 'rust bfs_sieve (rayon)' --cmd './target/bfs_sieve_rayon'
rt_cmd --lang c --approach bfs_sieve --lane par --mode native \
    --name 'c    bfs_sieve (pthreads)' --cmd './target/bfs_sieve_par_c'
rt_cmd --lang go --approach bfs_sieve --lane par --mode native \
    --name 'go   bfs_sieve (goroutines)' --cmd './target/bfs_sieve_go_par'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 2 --runs 10
rt_cmd --lang python --approach bfs_sieve --lane seq --mode interp \
    --name 'py   bfs_sieve' --cmd 'python3 bfs_sieve.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach bfs_sieve --mode codegen \
    --prepare 'rm -f target/bfs_sieve_kara bfs_sieve' \
    --name 'karac build bfs_sieve.kara' \
    --cmd 'sh -c "karac build bfs_sieve.kara >/dev/null && mv bfs_sieve target/bfs_sieve_kara"'
ce_cmd --lang rust --approach bfs_sieve --mode native \
    --prepare 'rm -f target/bfs_sieve' \
    --name 'rustc -O bfs_sieve.rs' --cmd 'rustc -O bfs_sieve.rs -o target/bfs_sieve'
ce_cmd --lang c --approach bfs_sieve --mode native \
    --prepare 'rm -f target/bfs_sieve_c' \
    --name 'clang -O3 bfs_sieve.c' --cmd 'clang -O3 bfs_sieve.c -o target/bfs_sieve_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach bfs_sieve --lane seq --mode codegen --path target/bfs_sieve_kara_seq
size_put --lang kara --approach bfs_sieve --lane par --mode codegen --path target/bfs_sieve_kara
size_put --lang rust --approach bfs_sieve --lane seq --mode native  --path target/bfs_sieve
size_put --lang rust --approach bfs_sieve --lane par --mode native  --path target/bfs_sieve_rayon
size_put --lang c    --approach bfs_sieve --lane seq --mode native  --path target/bfs_sieve_c
size_put --lang c    --approach bfs_sieve --lane par --mode native  --path target/bfs_sieve_par_c
size_put --lang go   --approach bfs_sieve --lane seq --mode native  --path target/bfs_sieve_go_seq
size_put --lang go   --approach bfs_sieve --lane par --mode native  --path target/bfs_sieve_go_par

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara   --approach bfs_sieve --lane seq --mode codegen --bytes "$(mem_peak ./target/bfs_sieve_kara_seq)"
mem_put --lang kara   --approach bfs_sieve --lane par --mode codegen --bytes "$(mem_peak ./target/bfs_sieve_kara)"
mem_put --lang rust   --approach bfs_sieve --lane seq --mode native  --bytes "$(mem_peak ./target/bfs_sieve)"
mem_put --lang rust   --approach bfs_sieve --lane par --mode native  --bytes "$(mem_peak ./target/bfs_sieve_rayon)"
mem_put --lang c      --approach bfs_sieve --lane seq --mode native  --bytes "$(mem_peak ./target/bfs_sieve_c)"
mem_put --lang c      --approach bfs_sieve --lane par --mode native  --bytes "$(mem_peak ./target/bfs_sieve_par_c)"
mem_put --lang go     --approach bfs_sieve --lane seq --mode native  --bytes "$(mem_peak ./target/bfs_sieve_go_seq)"
mem_put --lang go     --approach bfs_sieve --lane par --mode native  --bytes "$(mem_peak ./target/bfs_sieve_go_par)"
mem_put --lang python --approach bfs_sieve --lane seq --mode interp  --bytes "$(mem_peak python3 bfs_sieve.py)"

echo
echo "=== compile memory (cold) ==="
for src in bfs_sieve.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in bfs_sieve.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in bfs_sieve.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
