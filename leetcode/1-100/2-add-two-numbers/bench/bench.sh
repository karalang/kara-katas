#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #2.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Seq-only kata: the loop runs `add_two_numbers` 500_000× over a single
# 100-digit-pair input. Each call is independent, but per-call work is
# small enough (linear walk + ~100 small heap allocs) that a par lane
# would mostly measure dispatch overhead. Stays single-threaded so the
# kata measures pure codegen quality per the BENCH.md two-lane protocol.
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
    local out="target/iterative_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust iterative.rs
build_c    iterative.c
build_kara iterative.kara
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before
# timing. Python skipped from sink check by default — at N=100, K=500_000
# the py run takes ~6s and bench.sh would block on it. Set
# `KARA_BENCH_INCLUDE_PY=1` to opt in.
#
# Plain "name:command" pairs (no associative arrays — macOS bash is 3.2).
expected="4000000"
mismatch=""
for pair in \
    'kara:./target/iterative_kara' \
    'rust:./target/iterative' \
    'c:./target/iterative_c' \
    'go:./target/iterative_go_seq'; do
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
    py_out=$(python3 iterative.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

# Declare the kata for the JSON feed (no-op when BENCH_JSON=0).
bench_begin id=2 slug=add-two-numbers group=1-100 \
    title="Add Two Numbers" \
    workload="K=500_000 add_two_numbers over a single 100-digit-pair input" \
    sink="$expected"

echo "=== runtime — short workloads (compiled) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach iterative --lane seq --mode codegen \
    --name 'kara iterative (codegen)' --cmd './target/iterative_kara'
rt_cmd --lang rust --approach iterative --lane seq --mode native \
    --name 'rust iterative' --cmd './target/iterative'
rt_cmd --lang c --approach iterative --lane seq --mode native \
    --name 'c    iterative' --cmd './target/iterative_c'
rt_cmd --lang go --approach iterative --lane seq --mode native \
    --name 'go   iterative' --cmd './target/iterative_go_seq'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 2 --runs 10
rt_cmd --lang python --approach iterative --lane seq --mode interp \
    --name 'py   iterative' --cmd 'python3 iterative.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
# Per BENCH.md: hyperfine --warmup 1 --runs 10 with --prepare deleting the
# build artifact so every invocation is a true cold compile. karac/rustc/clang
# are the single-file compilers; go is excluded — its first invocation mixes
# module resolution + std-lib link and isn't comparable to single-file.
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach iterative --mode codegen \
    --prepare 'rm -f target/iterative_kara iterative' \
    --name 'karac build iterative.kara' \
    --cmd 'sh -c "karac build iterative.kara >/dev/null && mv iterative target/iterative_kara"'
ce_cmd --lang rust --approach iterative --mode native \
    --prepare 'rm -f target/iterative' \
    --name 'rustc -O iterative.rs' --cmd 'rustc -O iterative.rs -o target/iterative'
ce_cmd --lang c --approach iterative --mode native \
    --prepare 'rm -f target/iterative_c' \
    --name 'clang -O3 iterative.c' --cmd 'clang -O3 iterative.c -o target/iterative_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach iterative --lane seq --mode codegen --path target/iterative_kara
size_put --lang rust --approach iterative --lane seq --mode native  --path target/iterative
size_put --lang c    --approach iterative --lane seq --mode native  --path target/iterative_c
size_put --lang go   --approach iterative --lane seq --mode native  --path target/iterative_go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach iterative --lane seq --mode codegen --bytes "$(mem_peak ./target/iterative_kara)"
mem_put --lang rust --approach iterative --lane seq --mode native  --bytes "$(mem_peak ./target/iterative)"
mem_put --lang c    --approach iterative --lane seq --mode native  --bytes "$(mem_peak ./target/iterative_c)"
mem_put --lang go   --approach iterative --lane seq --mode native  --bytes "$(mem_peak ./target/iterative_go_seq)"
mem_put --lang python --approach iterative --lane seq --mode interp --bytes "$(mem_peak python3 iterative.py)"

echo
echo "=== compile memory (cold) ==="
# Artifact deleted before each measurement so the karac/rustc/clang invocation
# is a full cold compile. Go is omitted per BENCH.md — `go build`'s first run
# mixes module resolution + std-lib link and is not comparable to a single-file
# rustc/clang/karac invocation.
for src in iterative.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in iterative.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in iterative.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
