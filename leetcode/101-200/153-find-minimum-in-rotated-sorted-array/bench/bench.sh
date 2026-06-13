#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #153.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Multi-approach kata: linear_scan (K=10) and binary_search (K=2_000_000)
# share one bench.sh with separate runtime hyperfine batches per approach.
#
# binary_search runs a K=2_000_000 outer loop of independent read-only
# find_min calls, so Kāra's cost model auto-parallelizes it (post trip-count
# fix). It therefore carries BOTH lanes: a seq twin (KARAC_AUTO_PAR=0) in the
# seq lane and the auto-par binary in the par lane, compared against rayon /
# pthreads-C / goroutine-Go hand-tuned-parallel mirrors. linear_scan stays
# seq-only (it carries the small-K approach contrast, not a par surface).
#
# find_min is loop-invariant + pure, so -O3 would hoist the K-loop to a
# single call; the seq lane and ALL par comparators (rayon / C / Go) use
# black_box to defeat that, so the sink reflects K real iterations (K × min
# value 1 = 2000000), not a collapsed single call.
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

# --- par-lane builders (hand-tuned-parallel comparators for auto-par) --------
# kara seq twin: same source, KARAC_AUTO_PAR=0 forces the single-threaded
# lowering so the seq lane is a true single-thread baseline (the default build
# auto-parallelizes binary_search after the cost-model trip-count fix).
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

# rayon cargo project (bench/rayon/, package findmin_rayon). cargo's own
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

# goroutine-Go par mirror (bench/go-par/, module findmin_go_par).
build_go_par() {
    local bin="$1"
    local out="target/$bin"
    local src="go-par/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-par/$bin ..." >&2
        ( cd go-par && go build -o "../$out" . )
    fi
}

build_rust linear_scan.rs
build_rust binary_search.rs
build_c    linear_scan.c
build_c    binary_search.c
build_kara linear_scan.kara
build_kara binary_search.kara          # auto-par (par lane)
build_kara_seq binary_search.kara      # seq twin (seq lane)
build_go_seq linear_scan
build_go_seq binary_search
# par-lane comparators for binary_search
build_rust_rayon findmin_rayon
build_c_par      binary_search_par.c
build_go_par     findmin_go_par

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

# binary_search sink — K × min value 1 = 2000000. black_box keeps the
# loop-invariant find_min from being hoisted to a single call on every lane,
# so this value confirms K real iterations ran (seq twin + auto-par + the
# three hand-tuned-parallel mirrors must all agree).
expected_bs="2000000"
mismatch_bs=""
for pair in \
    'bs_kara_seq:./target/binary_search_kara_seq' \
    'bs_kara_par:./target/binary_search_kara' \
    'bs_rust:./target/binary_search' \
    'bs_c:./target/binary_search_c' \
    'bs_go:./target/binary_search_go_seq' \
    'bs_rayon:./target/findmin_rayon' \
    'bs_c_par:./target/binary_search_par_c' \
    'bs_go_par:./target/findmin_go_par'; do
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
echo "sink binary_search (kara seq+par/rust/c/go + rayon/c-par/go-par): $expected_bs"
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

# Declare the kata for the JSON feed (no-op when BENCH_JSON=0).
bench_begin id=153 slug=find-minimum-in-rotated-sorted-array group=101-200 \
    title="Find Minimum in Rotated Sorted Array" \
    workload="linear_scan K=10 / binary_search K=2_000_000" \
    sink="linear_scan=$expected_ls binary_search=$expected_bs"

echo "=== runtime — linear_scan (compiled, K=10) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach linear_scan --lane seq --mode codegen \
    --name 'kara linear_scan (codegen)' --cmd './target/linear_scan_kara'
rt_cmd --lang rust --approach linear_scan --lane seq --mode native \
    --name 'rust linear_scan' --cmd './target/linear_scan'
rt_cmd --lang c --approach linear_scan --lane seq --mode native \
    --name 'c    linear_scan' --cmd './target/linear_scan_c'
rt_cmd --lang go --approach linear_scan --lane seq --mode native \
    --name 'go   linear_scan' --cmd './target/linear_scan_go_seq'
rt_end

echo
echo "=== runtime — binary_search seq lane (compiled, K=2_000_000) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach binary_search --lane seq --mode codegen \
    --name 'kara binary_search (seq twin)' --cmd './target/binary_search_kara_seq'
rt_cmd --lang rust --approach binary_search --lane seq --mode native \
    --name 'rust binary_search' --cmd './target/binary_search'
rt_cmd --lang c --approach binary_search --lane seq --mode native \
    --name 'c    binary_search' --cmd './target/binary_search_c'
rt_cmd --lang go --approach binary_search --lane seq --mode native \
    --name 'go   binary_search' --cmd './target/binary_search_go_seq'
rt_end

echo
echo "=== runtime — binary_search par lane (K=2_000_000 auto-par vs hand-tuned) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach binary_search --lane par --mode codegen \
    --name 'kara binary_search (auto-par)' --cmd './target/binary_search_kara'
rt_cmd --lang rust --approach binary_search --lane par --mode native \
    --name 'rust binary_search (rayon)' --cmd './target/findmin_rayon'
rt_cmd --lang c --approach binary_search --lane par --mode native \
    --name 'c    binary_search (pthreads)' --cmd './target/binary_search_par_c'
rt_cmd --lang go --approach binary_search --lane par --mode native \
    --name 'go   binary_search (goroutines)' --cmd './target/findmin_go_par'
rt_end

if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    echo
    echo "=== runtime — python ==="
    rt_begin --warmup 5 --runs 30
    rt_cmd --lang python --approach linear_scan --lane seq --mode interp \
        --name 'py   linear_scan' --cmd 'python3 linear_scan.py'
    rt_cmd --lang python --approach binary_search --lane seq --mode interp \
        --name 'py   binary_search' --cmd 'python3 binary_search.py'
    rt_end
fi

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach linear_scan --mode codegen \
    --prepare 'rm -f target/linear_scan_kara linear_scan' \
    --name 'karac build linear_scan.kara' \
    --cmd 'sh -c "karac build linear_scan.kara >/dev/null && mv linear_scan target/linear_scan_kara"'
ce_cmd --lang kara --approach binary_search --mode codegen \
    --prepare 'rm -f target/binary_search_kara binary_search' \
    --name 'karac build binary_search.kara' \
    --cmd 'sh -c "karac build binary_search.kara >/dev/null && mv binary_search target/binary_search_kara"'
ce_cmd --lang rust --approach linear_scan --mode native \
    --prepare 'rm -f target/linear_scan' \
    --name 'rustc -O linear_scan.rs' --cmd 'rustc -O linear_scan.rs -o target/linear_scan'
ce_cmd --lang rust --approach binary_search --mode native \
    --prepare 'rm -f target/binary_search' \
    --name 'rustc -O binary_search.rs' --cmd 'rustc -O binary_search.rs -o target/binary_search'
ce_cmd --lang c --approach linear_scan --mode native \
    --prepare 'rm -f target/linear_scan_c' \
    --name 'clang -O3 linear_scan.c' --cmd 'clang -O3 linear_scan.c -o target/linear_scan_c'
ce_cmd --lang c --approach binary_search --mode native \
    --prepare 'rm -f target/binary_search_c' \
    --name 'clang -O3 binary_search.c' --cmd 'clang -O3 binary_search.c -o target/binary_search_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach linear_scan   --lane seq --mode codegen --path target/linear_scan_kara
size_put --lang kara --approach binary_search --lane seq --mode codegen --path target/binary_search_kara_seq
size_put --lang kara --approach binary_search --lane par --mode codegen --path target/binary_search_kara
size_put --lang rust --approach linear_scan   --lane seq --mode native  --path target/linear_scan
size_put --lang rust --approach binary_search --lane seq --mode native  --path target/binary_search
size_put --lang rust --approach binary_search --lane par --mode native  --path target/findmin_rayon
size_put --lang c    --approach linear_scan   --lane seq --mode native  --path target/linear_scan_c
size_put --lang c    --approach binary_search --lane seq --mode native  --path target/binary_search_c
size_put --lang c    --approach binary_search --lane par --mode native  --path target/binary_search_par_c
size_put --lang go   --approach linear_scan   --lane seq --mode native  --path target/linear_scan_go_seq
size_put --lang go   --approach binary_search --lane seq --mode native  --path target/binary_search_go_seq
size_put --lang go   --approach binary_search --lane par --mode native  --path target/findmin_go_par

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach linear_scan   --lane seq --mode codegen --bytes "$(mem_peak ./target/linear_scan_kara)"
mem_put --lang rust --approach linear_scan   --lane seq --mode native  --bytes "$(mem_peak ./target/linear_scan)"
mem_put --lang c    --approach linear_scan   --lane seq --mode native  --bytes "$(mem_peak ./target/linear_scan_c)"
mem_put --lang go   --approach linear_scan   --lane seq --mode native  --bytes "$(mem_peak ./target/linear_scan_go_seq)"
mem_put --lang kara --approach binary_search --lane seq --mode codegen --bytes "$(mem_peak ./target/binary_search_kara_seq)"
mem_put --lang kara --approach binary_search --lane par --mode codegen --bytes "$(mem_peak ./target/binary_search_kara)"
mem_put --lang rust --approach binary_search --lane seq --mode native  --bytes "$(mem_peak ./target/binary_search)"
mem_put --lang rust --approach binary_search --lane par --mode native  --bytes "$(mem_peak ./target/findmin_rayon)"
mem_put --lang c    --approach binary_search --lane seq --mode native  --bytes "$(mem_peak ./target/binary_search_c)"
mem_put --lang c    --approach binary_search --lane par --mode native  --bytes "$(mem_peak ./target/binary_search_par_c)"
mem_put --lang go   --approach binary_search --lane seq --mode native  --bytes "$(mem_peak ./target/binary_search_go_seq)"
mem_put --lang go   --approach binary_search --lane par --mode native  --bytes "$(mem_peak ./target/findmin_go_par)"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    mem_put --lang python --approach linear_scan   --lane seq --mode interp --bytes "$(mem_peak python3 linear_scan.py)"
    mem_put --lang python --approach binary_search --lane seq --mode interp --bytes "$(mem_peak python3 binary_search.py)"
fi

echo
echo "=== compile memory (cold) ==="
for src in linear_scan.kara binary_search.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in linear_scan.rs binary_search.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in linear_scan.c binary_search.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
