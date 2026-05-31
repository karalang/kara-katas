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

# Declare the kata for the JSON feed (no-op when BENCH_JSON=0).
bench_begin id=133 slug=clone-graph group=101-200 \
    title="Clone Graph" workload="N=2000 ring, K=500 clones (clone_bfs)" \
    sink="$expected"

echo "=== runtime — seq lane (clone_bfs, N=2000 ring, K=500) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach clone_bfs --lane seq --mode codegen \
    --name 'kara clone_bfs (codegen)' --cmd './target/clone_bfs_kara'
rt_cmd --lang rust --approach clone_bfs --lane seq --mode native \
    --name 'rust clone_bfs' --cmd './target/clone_bfs'
rt_cmd --lang c --approach clone_bfs --lane seq --mode native \
    --name 'c    clone_bfs' --cmd './target/clone_bfs_c'
rt_cmd --lang go --approach clone_bfs --lane seq --mode native \
    --name 'go   clone_bfs' --cmd './target/clone_bfs_go_seq'
rt_end

echo
echo "=== runtime — par lane (kara clone_bfs par 18-way only) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach clone_bfs --lane par --mode codegen \
    --name 'kara clone_bfs (par 18-way)' --cmd './target/clone_bfs_par_kara'
rt_end

if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    echo
    echo "=== runtime — python ==="
    rt_begin --warmup 5 --runs 30
    rt_cmd --lang python --approach clone_bfs --lane seq --mode interp \
        --name 'py   clone_bfs' --cmd 'python3 clone_bfs.py'
    rt_end
fi

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach clone_bfs --mode codegen \
    --prepare 'rm -f target/clone_bfs_kara clone_bfs' \
    --name 'karac build clone_bfs.kara' \
    --cmd 'sh -c "karac build clone_bfs.kara >/dev/null && mv clone_bfs target/clone_bfs_kara"'
ce_cmd --lang kara --approach clone_bfs_par --mode codegen \
    --prepare 'rm -f target/clone_bfs_par_kara clone_bfs_par' \
    --name 'karac build clone_bfs_par.kara' \
    --cmd 'sh -c "karac build clone_bfs_par.kara >/dev/null && mv clone_bfs_par target/clone_bfs_par_kara"'
ce_cmd --lang rust --approach clone_bfs --mode native \
    --prepare 'rm -f target/clone_bfs' \
    --name 'rustc -O clone_bfs.rs' --cmd 'rustc -O clone_bfs.rs -o target/clone_bfs'
ce_cmd --lang c --approach clone_bfs --mode native \
    --prepare 'rm -f target/clone_bfs_c' \
    --name 'clang -O3 clone_bfs.c' --cmd 'clang -O3 clone_bfs.c -o target/clone_bfs_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach clone_bfs     --lane seq --mode codegen --path target/clone_bfs_kara
size_put --lang kara --approach clone_bfs     --lane par --mode codegen --path target/clone_bfs_par_kara
size_put --lang rust --approach clone_bfs     --lane seq --mode native  --path target/clone_bfs
size_put --lang c    --approach clone_bfs     --lane seq --mode native  --path target/clone_bfs_c
size_put --lang go   --approach clone_bfs     --lane seq --mode native  --path target/clone_bfs_go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach clone_bfs --lane seq --mode codegen --bytes "$(mem_peak ./target/clone_bfs_kara)"
mem_put --lang kara --approach clone_bfs --lane par --mode codegen --bytes "$(mem_peak ./target/clone_bfs_par_kara)"
mem_put --lang rust --approach clone_bfs --lane seq --mode native  --bytes "$(mem_peak ./target/clone_bfs)"
mem_put --lang c    --approach clone_bfs --lane seq --mode native  --bytes "$(mem_peak ./target/clone_bfs_c)"
mem_put --lang go   --approach clone_bfs --lane seq --mode native  --bytes "$(mem_peak ./target/clone_bfs_go_seq)"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    mem_put --lang python --approach clone_bfs --lane seq --mode interp --bytes "$(mem_peak python3 clone_bfs.py)"
fi

echo
echo "=== compile memory (cold) ==="
for src in clone_bfs.kara clone_bfs_par.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
rm -f target/clone_bfs
cmem_put --lang rust --approach clone_bfs --mode native --bytes "$(mem_peak rustc -O clone_bfs.rs -o target/clone_bfs)"
rm -f target/clone_bfs_c
cmem_put --lang c --approach clone_bfs --mode native --bytes "$(mem_peak clang -O3 clone_bfs.c -o target/clone_bfs_c)"

echo
bench_emit
