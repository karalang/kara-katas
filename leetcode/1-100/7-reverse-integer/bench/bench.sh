#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #7.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Two-lane kata. The K=50M outer loop reduces via
# `sum += reverse(inputs[k % N]) as i64` — karac's auto-par-on-reduction
# recognizes the shape and emits a karac_par_reduce dispatch (binary grows
# from ~49 KiB to ~296 KiB, wall drops ~10× via multi-core dispatch). For
# the BENCH.md seq lane this masks the per-core codegen-vs-rustc comparison
# the kata corpus is built around, so we ship a second kara binary built
# with KARAC_AUTO_PAR=0 (codegen.rs Slice 6 gate — short-circuits all
# auto-par dispatch back to plain sequential compile_block; the documented
# mechanism for side-by-side seq-vs-par benchmarking of the same workload).
# The default binary still gets built so the auto-par number stays reported
# as the production regime — NOT headlined cross-lane against the
# single-threaded comparators (see ../README.md).
#
# Requires: hyperfine (`brew install hyperfine`), rustc (rustup), clang,
# go, karac (with --features llvm for the codegen path).

set -euo pipefail
cd "$(dirname "$0")"

STEM=reverse

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
        echo "compiling $src (auto-par default) ..." >&2
        karac build "$src" >/dev/null
        mv "$stem" "$out"
    fi
}

build_kara_seq() {
    local src="$1"
    local stem="$(basename "$src" .kara)"
    local out="target/${stem}_kara_seq"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling $src (KARAC_AUTO_PAR=0, seq lane) ..." >&2
        KARAC_AUTO_PAR=0 karac build "$src" >/dev/null
        mv "$stem" "$out"
    fi
}

build_go_seq() {
    local out="target/${STEM}_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust     "${STEM}.rs"
build_c        "${STEM}.c"
build_kara     "${STEM}.kara"
build_kara_seq "${STEM}.kara"
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before
# timing. Python is excluded from the sink check + the JSON feed: at K=50M a
# full python run is ~86 s, so it's sampled at K=1M and quoted as a
# projection in the console + README only (charts exclude python anyway).
expected="-292465958482676"
mismatch=""
for pair in \
    "kara:./target/${STEM}_kara" \
    "kara_seq:./target/${STEM}_kara_seq" \
    "rust:./target/${STEM}" \
    "c:./target/${STEM}_c" \
    "go:./target/${STEM}_go_seq"; do
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
echo "sink (kara/kara_seq/rust/c/go): $expected"
echo

# Declare the kata for the JSON feed (no-op when BENCH_JSON=0).
bench_begin id=7 slug=reverse-integer group=1-100 \
    title="Reverse Integer" workload="K=50M reverse reduction (py K=1M scaled-down)" \
    sink="$expected"

echo "=== runtime — seq lane (apples-to-apples, single-threaded) ==="
# All four comparators here run single-threaded. The kara binary built with
# KARAC_AUTO_PAR=0 short-circuits auto-par dispatch back to plain sequential
# codegen — this is the row directly comparable to rustc -O / clang -O3 /
# go build on a per-core codegen-quality basis.
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach reverse --lane seq --mode codegen \
    --name "kara ${STEM} (seq, KARAC_AUTO_PAR=0)" --cmd "./target/${STEM}_kara_seq"
rt_cmd --lang rust --approach reverse --lane seq --mode native \
    --name "rust ${STEM}" --cmd "./target/${STEM}"
rt_cmd --lang c --approach reverse --lane seq --mode native \
    --name "c    ${STEM}" --cmd "./target/${STEM}_c"
rt_cmd --lang go --approach reverse --lane seq --mode native \
    --name "go   ${STEM}" --cmd "./target/${STEM}_go_seq"
rt_end

echo
echo "=== runtime — auto-par regime (kara default, multi-core) ==="
# Default `karac build` output: karac's auto-par-on-reduction recognizes the
# `sum +=` reduction in main's K=50M loop and emits a karac_par_reduce
# dispatch. Multi-core wall-time win on top of the seq lane. NOT directly
# comparable to the single-thread rows above per BENCH.md's two-lane
# discipline — reported separately so the production-default Kara behavior
# stays visible. Heavier warmup (10/50) absorbs worker-pool init noise that
# otherwise inflates σ on short auto-par runs.
rt_begin --warmup 10 --runs 50
rt_cmd --lang kara --approach reverse --lane par --mode codegen \
    --name "kara ${STEM} (auto-par default)" --cmd "./target/${STEM}_kara"
rt_end

echo
echo "=== runtime — long workloads (py, K=1M scaled-down) ==="
# Python at K=50M takes ~86 s per sample; sample 50× smaller K and quote the
# ratio in the README. Console-only (no JSON row — different K than the
# compiled mirrors, and charts exclude python regardless).
python3 -c '
import sys
sys.path.insert(0, ".")
import reverse as r
inputs = [r.to_i32(i * 2_654_435_769 + 305_419_896) for i in range(1024)]
total = 0
for k in range(1_000_000):
    total += r.reverse(inputs[k % 1024])
print(f"  py reverse (K=1M) sink={total}")
print(f"  -> projected K=50M scale=50×")
'

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach reverse --mode codegen \
    --prepare "rm -f target/${STEM}_kara ${STEM}" \
    --name "karac build ${STEM}.kara" \
    --cmd "sh -c \"karac build ${STEM}.kara >/dev/null && mv ${STEM} target/${STEM}_kara\""
ce_cmd --lang rust --approach reverse --mode native \
    --prepare "rm -f target/${STEM}" \
    --name "rustc -O ${STEM}.rs" --cmd "rustc -O ${STEM}.rs -o target/${STEM}"
ce_cmd --lang c --approach reverse --mode native \
    --prepare "rm -f target/${STEM}_c" \
    --name "clang -O3 ${STEM}.c" --cmd "clang -O3 ${STEM}.c -o target/${STEM}_c"
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach reverse --lane seq --mode codegen --path "target/${STEM}_kara_seq"
size_put --lang kara --approach reverse --lane par --mode codegen --path "target/${STEM}_kara"
size_put --lang rust --approach reverse --lane seq --mode native  --path "target/${STEM}"
size_put --lang c    --approach reverse --lane seq --mode native  --path "target/${STEM}_c"
size_put --lang go   --approach reverse --lane seq --mode native  --path "target/${STEM}_go_seq"

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach reverse --lane seq --mode codegen --bytes "$(mem_peak ./target/${STEM}_kara_seq)"
mem_put --lang kara --approach reverse --lane par --mode codegen --bytes "$(mem_peak ./target/${STEM}_kara)"
mem_put --lang rust --approach reverse --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM})"
mem_put --lang c    --approach reverse --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM}_c)"
mem_put --lang go   --approach reverse --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM}_go_seq)"

echo
echo "=== compile memory (cold) ==="
for src in "${STEM}.kara"; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach reverse --mode codegen --bytes "$bytes"
done
for src in "${STEM}.rs"; do
    out="target/$(basename "$src" .rs)"
    rm -f "$out"
    cmem_put --lang rust --approach reverse --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in "${STEM}.c"; do
    out="target/$(basename "$src" .c)_c"
    rm -f "$out"
    cmem_put --lang c --approach reverse --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
