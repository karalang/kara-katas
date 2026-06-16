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

# Structured-JSON emission (writes bench/results.json). Set BENCH_JSON=0 to
# skip — the human-readable console output below is unaffected either way.
if [ "${BENCH_JSON:-1}" = "1" ]; then
    require jq      "brew install jq"
    require python3 "python3 ships with macOS; or 'brew install python'"
fi
ROOT="$(cd ../../../.. && pwd)"
. "$ROOT/scripts/bench-lib.sh"

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

# NOTE: this kata's `sliding_window` K-loop newly auto-parallelizes under the
# current cost model. Until a par lane is decided (runtime engagement TBD — see
# SWEEP_TRACKER "newly-firing"), the kara binary is built as an honest seq twin
# (KARAC_AUTO_PAR=0) so the seq-codegen row is single-threaded, not the auto-par
# binary. Drop the env override (and add a par lane) once that decision lands.
build_kara() {
    local src="$1"
    local stem="$(basename "$src" .kara)"
    local out="target/${stem}_kara"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling $src (seq twin, KARAC_AUTO_PAR=0) ..." >&2
        KARAC_AUTO_PAR=0 karac build "$src" >/dev/null
        mv "$stem" "$out"
    fi
}

build_go_seq() {
    local out="target/sliding_window_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust sliding_window.rs
build_rust_ovf sliding_window.rs
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
    'rust_ovf:./target/sliding_window_ovf' \
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

# Declare the kata for the JSON feed (no-op when BENCH_JSON=0).
bench_begin id=3 slug=longest-substring-without-repeating-characters group=1-100 \
    title="Longest Substring Without Repeating Characters" \
    workload="sliding_window: 104_000-char input, K=20 outer iters (py timed separately)" \
    sink="$expected"

echo "=== runtime — short workloads (compiled) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach sliding_window --lane seq --mode codegen \
    --name 'kara sliding_window (codegen)' --cmd './target/sliding_window_kara'
rt_cmd --lang rust --approach sliding_window --lane seq --mode native \
    --name 'rust sliding_window' --cmd './target/sliding_window'
rt_cmd --lang rust_ovf --approach sliding_window --lane seq --mode native \
    --name 'rust sliding_window (overflow-checks=on, equal-safety)' --cmd './target/sliding_window_ovf'
rt_cmd --lang c --approach sliding_window --lane seq --mode native \
    --name 'c    sliding_window' --cmd './target/sliding_window_c'
rt_cmd --lang go --approach sliding_window --lane seq --mode native \
    --name 'go   sliding_window' --cmd './target/sliding_window_go_seq'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 2 --runs 10
rt_cmd --lang python --approach sliding_window --lane seq --mode interp \
    --name 'py   sliding_window' --cmd 'python3 sliding_window.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
# Per BENCH.md: hyperfine --warmup 1 --runs 10 with --prepare deleting the
# build artifact so every invocation is a true cold compile. karac/rustc/clang
# are the single-file compilers; go is excluded — its first invocation mixes
# module resolution + std-lib link and isn't comparable to single-file.
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach sliding_window --mode codegen \
    --prepare 'rm -f target/sliding_window_kara sliding_window' \
    --name 'karac build sliding_window.kara' \
    --cmd 'sh -c "KARAC_AUTO_PAR=0 karac build sliding_window.kara >/dev/null && mv sliding_window target/sliding_window_kara"'
ce_cmd --lang rust --approach sliding_window --mode native \
    --prepare 'rm -f target/sliding_window' \
    --name 'rustc -O sliding_window.rs' --cmd 'rustc -O sliding_window.rs -o target/sliding_window'
ce_cmd --lang c --approach sliding_window --mode native \
    --prepare 'rm -f target/sliding_window_c' \
    --name 'clang -O3 sliding_window.c' --cmd 'clang -O3 sliding_window.c -o target/sliding_window_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach sliding_window --lane seq --mode codegen --path target/sliding_window_kara
size_put --lang rust --approach sliding_window --lane seq --mode native  --path target/sliding_window
size_put --lang c    --approach sliding_window --lane seq --mode native  --path target/sliding_window_c
size_put --lang go   --approach sliding_window --lane seq --mode native  --path target/sliding_window_go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach sliding_window --lane seq --mode codegen --bytes "$(mem_peak ./target/sliding_window_kara)"
mem_put --lang rust --approach sliding_window --lane seq --mode native  --bytes "$(mem_peak ./target/sliding_window)"
mem_put --lang c    --approach sliding_window --lane seq --mode native  --bytes "$(mem_peak ./target/sliding_window_c)"
mem_put --lang go   --approach sliding_window --lane seq --mode native  --bytes "$(mem_peak ./target/sliding_window_go_seq)"
mem_put --lang python --approach sliding_window --lane seq --mode interp --bytes "$(mem_peak python3 sliding_window.py)"

echo
echo "=== compile memory (cold) ==="
# Artifact deleted before each measurement so the karac/rustc/clang invocation
# is a full cold compile. Go is omitted per BENCH.md — `go build`'s first run
# mixes module resolution + std-lib link and is not comparable to a single-file
# rustc/clang/karac invocation.
for src in sliding_window.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak env KARAC_AUTO_PAR=0 karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in sliding_window.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in sliding_window.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
