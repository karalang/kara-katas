#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #226.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Multi-approach kata: recursive and iterative share one bench.sh with
# compiled runtime batch (warmup 5 / runs 30) and python in a separate batch.
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

build_rust recursive.rs
build_rust iterative.rs
build_c    recursive.c
build_c    iterative.c
build_kara recursive.kara
build_kara iterative.kara
build_go_seq recursive
build_go_seq iterative

expected="2666665501"
mismatch=""
for pair in \
    'rec_kara:./target/recursive_kara' \
    'rec_rust:./target/recursive' \
    'rec_c:./target/recursive_c' \
    'rec_go:./target/recursive_go_seq' \
    'iter_kara:./target/iterative_kara' \
    'iter_rust:./target/iterative' \
    'iter_c:./target/iterative_c' \
    'iter_go:./target/iterative_go_seq'; do
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
echo "sink (all eight: kara/rust/c/go × recursive/iterative): $expected"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    py_rec=$(python3 recursive.py)
    py_iter=$(python3 iterative.py)
    if [ "$py_rec" != "$expected" ] || [ "$py_iter" != "$expected" ]; then
        echo "python sink mismatch: py_rec=$py_rec py_iter=$py_iter" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

# Declare the kata for the JSON feed (no-op when BENCH_JSON=0).
bench_begin id=226 slug=invert-binary-tree group=201-300 \
    title="Invert Binary Tree" \
    workload="N=2000-node balanced tree, K=10 outer iterations / recursive + iterative" \
    sink="$expected"

echo "=== runtime — compiled (warmup 5 / runs 30) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach recursive --lane seq --mode codegen \
    --name 'kara recursive (codegen)' --cmd './target/recursive_kara'
rt_cmd --lang kara --approach iterative --lane seq --mode codegen \
    --name 'kara iterative (codegen)' --cmd './target/iterative_kara'
rt_cmd --lang rust --approach recursive --lane seq --mode native \
    --name 'rust recursive' --cmd './target/recursive'
rt_cmd --lang rust --approach iterative --lane seq --mode native \
    --name 'rust iterative' --cmd './target/iterative'
rt_cmd --lang c --approach recursive --lane seq --mode native \
    --name 'c    recursive' --cmd './target/recursive_c'
rt_cmd --lang c --approach iterative --lane seq --mode native \
    --name 'c    iterative' --cmd './target/iterative_c'
rt_cmd --lang go --approach recursive --lane seq --mode native \
    --name 'go   recursive' --cmd './target/recursive_go_seq'
rt_cmd --lang go --approach iterative --lane seq --mode native \
    --name 'go   iterative' --cmd './target/iterative_go_seq'
rt_end

if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    echo
    echo "=== runtime — python ==="
    rt_begin --warmup 5 --runs 30
    rt_cmd --lang python --approach recursive --lane seq --mode interp \
        --name 'py   recursive' --cmd 'python3 recursive.py'
    rt_cmd --lang python --approach iterative --lane seq --mode interp \
        --name 'py   iterative' --cmd 'python3 iterative.py'
    rt_end
fi

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach recursive --mode codegen \
    --prepare 'rm -f target/recursive_kara recursive' \
    --name 'karac build recursive.kara' \
    --cmd 'sh -c "karac build recursive.kara >/dev/null && mv recursive target/recursive_kara"'
ce_cmd --lang kara --approach iterative --mode codegen \
    --prepare 'rm -f target/iterative_kara iterative' \
    --name 'karac build iterative.kara' \
    --cmd 'sh -c "karac build iterative.kara >/dev/null && mv iterative target/iterative_kara"'
ce_cmd --lang rust --approach recursive --mode native \
    --prepare 'rm -f target/recursive' \
    --name 'rustc -O recursive.rs' --cmd 'rustc -O recursive.rs -o target/recursive'
ce_cmd --lang rust --approach iterative --mode native \
    --prepare 'rm -f target/iterative' \
    --name 'rustc -O iterative.rs' --cmd 'rustc -O iterative.rs -o target/iterative'
ce_cmd --lang c --approach recursive --mode native \
    --prepare 'rm -f target/recursive_c' \
    --name 'clang -O3 recursive.c' --cmd 'clang -O3 recursive.c -o target/recursive_c'
ce_cmd --lang c --approach iterative --mode native \
    --prepare 'rm -f target/iterative_c' \
    --name 'clang -O3 iterative.c' --cmd 'clang -O3 iterative.c -o target/iterative_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach recursive --lane seq --mode codegen --path target/recursive_kara
size_put --lang kara --approach iterative --lane seq --mode codegen --path target/iterative_kara
size_put --lang rust --approach recursive --lane seq --mode native  --path target/recursive
size_put --lang rust --approach iterative --lane seq --mode native  --path target/iterative
size_put --lang c    --approach recursive --lane seq --mode native  --path target/recursive_c
size_put --lang c    --approach iterative --lane seq --mode native  --path target/iterative_c
size_put --lang go   --approach recursive --lane seq --mode native  --path target/recursive_go_seq
size_put --lang go   --approach iterative --lane seq --mode native  --path target/iterative_go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach recursive --lane seq --mode codegen --bytes "$(mem_peak ./target/recursive_kara)"
mem_put --lang kara --approach iterative --lane seq --mode codegen --bytes "$(mem_peak ./target/iterative_kara)"
mem_put --lang rust --approach recursive --lane seq --mode native  --bytes "$(mem_peak ./target/recursive)"
mem_put --lang rust --approach iterative --lane seq --mode native  --bytes "$(mem_peak ./target/iterative)"
mem_put --lang c    --approach recursive --lane seq --mode native  --bytes "$(mem_peak ./target/recursive_c)"
mem_put --lang c    --approach iterative --lane seq --mode native  --bytes "$(mem_peak ./target/iterative_c)"
mem_put --lang go   --approach recursive --lane seq --mode native  --bytes "$(mem_peak ./target/recursive_go_seq)"
mem_put --lang go   --approach iterative --lane seq --mode native  --bytes "$(mem_peak ./target/iterative_go_seq)"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    mem_put --lang python --approach recursive --lane seq --mode interp --bytes "$(mem_peak python3 recursive.py)"
    mem_put --lang python --approach iterative --lane seq --mode interp --bytes "$(mem_peak python3 iterative.py)"
fi

echo
echo "=== compile memory (cold) ==="
for src in recursive.kara iterative.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in recursive.rs iterative.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in recursive.c iterative.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
