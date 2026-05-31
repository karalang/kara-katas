#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #56 (Merge
# Intervals).
# See ../README.md § Benchmarks for what these numbers mean.
#
# Two-lane kata (BENCH.md § Implicit auto-par): karac's auto-par-on-
# reduction recognizes the `sum = sum + r.len()` accumulator in main's
# K=1M loop and may emit a `karac_par_reduce` dispatch by default. We
# build TWO kara binaries:
#
#   merge_intervals_kara_seq — KARAC_AUTO_PAR=0, single-threaded.
#                              Within-lane comparator vs rust / c / go.
#   merge_intervals_kara     — default karac build, auto-par on (if it
#                              fires). Reported separately so the
#                              production-default Kara behavior stays
#                              visible.
#
# Sort dispatch shape note: this kata sorts `Vec[(i64, i64)]` by
# `|a, b| a.0.cmp(b.0)` — TUPLE element type, so Slice 6.1's mono fast
# path (gated on i64 elem type only) DOES NOT FIRE. Both kara binaries
# route through `karac_vec_sort_by`'s runtime callback. This kata is the
# natural-pull trigger evidence for Slice 6.4 (tuple/struct elem mono
# sort) — see karac's docs/implementation_checklist/phase-7-codegen.md.
#
# Per BENCH.md's two-lane discipline, cross-lane wall-time ratios are
# not meaningful — the README headlines the within-lane seq comparison,
# and reports the auto-par regime as a separate sub-section.
#
# Requires: hyperfine, rustc, clang, go, karac.

set -euo pipefail
cd "$(dirname "$0")"

STEM=merge_intervals

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
require karac     "cargo install --path . --features llvm  (from kara checkout)"

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
    printf '  %-40s %12s bytes (%6s MiB)\n' "$label" "$bytes" "$mib"
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

expected=$(./target/${STEM}_kara)
mismatch=""
for pair in \
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
bench_begin id=56 slug=merge-intervals group=1-100 \
    title="Merge Intervals" workload="K=1M merge passes (py K=100k scaled-down)" \
    sink="$expected"

echo "=== runtime — seq lane (apples-to-apples, single-threaded) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach merge_intervals --lane seq --mode codegen \
    --name "kara ${STEM} (seq, KARAC_AUTO_PAR=0)" --cmd "./target/${STEM}_kara_seq"
rt_cmd --lang rust --approach merge_intervals --lane seq --mode native \
    --name "rust ${STEM}" --cmd "./target/${STEM}"
rt_cmd --lang c --approach merge_intervals --lane seq --mode native \
    --name "c    ${STEM}" --cmd "./target/${STEM}_c"
rt_cmd --lang go --approach merge_intervals --lane seq --mode native \
    --name "go   ${STEM}" --cmd "./target/${STEM}_go_seq"
rt_end

echo
echo "=== runtime — auto-par regime (kara default, multi-core) ==="
rt_begin --warmup 10 --runs 50
rt_cmd --lang kara --approach merge_intervals --lane par --mode codegen \
    --name "kara ${STEM} (auto-par default)" --cmd "./target/${STEM}_kara"
rt_end

echo
echo "=== runtime — long workloads (py, K=100k scaled-down) ==="
rt_begin --warmup 2 --runs 10
rt_cmd --lang python --approach merge_intervals --lane seq --mode interp \
    --name "py   ${STEM} (K=100k)" --cmd "python3 ${STEM}.py"
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach merge_intervals --mode codegen \
    --prepare "rm -f target/${STEM}_kara ${STEM}" \
    --name "karac build ${STEM}.kara" \
    --cmd "sh -c \"karac build ${STEM}.kara >/dev/null && mv ${STEM} target/${STEM}_kara\""
ce_cmd --lang rust --approach merge_intervals --mode native \
    --prepare "rm -f target/${STEM}" \
    --name "rustc -O ${STEM}.rs" --cmd "rustc -O ${STEM}.rs -o target/${STEM}"
ce_cmd --lang c --approach merge_intervals --mode native \
    --prepare "rm -f target/${STEM}_c" \
    --name "clang -O3 ${STEM}.c" --cmd "clang -O3 ${STEM}.c -o target/${STEM}_c"
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach merge_intervals --lane seq --mode codegen --path "target/${STEM}_kara_seq"
size_put --lang kara --approach merge_intervals --lane par --mode codegen --path "target/${STEM}_kara"
size_put --lang rust --approach merge_intervals --lane seq --mode native  --path "target/${STEM}"
size_put --lang c    --approach merge_intervals --lane seq --mode native  --path "target/${STEM}_c"
size_put --lang go   --approach merge_intervals --lane seq --mode native  --path "target/${STEM}_go_seq"

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach merge_intervals --lane seq --mode codegen --bytes "$(mem_peak ./target/${STEM}_kara_seq)"
mem_put --lang kara --approach merge_intervals --lane par --mode codegen --bytes "$(mem_peak ./target/${STEM}_kara)"
mem_put --lang rust --approach merge_intervals --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM})"
mem_put --lang c    --approach merge_intervals --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM}_c)"
mem_put --lang go   --approach merge_intervals --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM}_go_seq)"

echo
echo "=== compile memory (cold) ==="
for src in "${STEM}.kara"; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach merge_intervals --mode codegen --bytes "$bytes"
done
for src in "${STEM}.rs"; do
    out="target/$(basename "$src" .rs)"
    rm -f "$out"
    cmem_put --lang rust --approach merge_intervals --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in "${STEM}.c"; do
    out="target/$(basename "$src" .c)_c"
    rm -f "$out"
    cmem_put --lang c --approach merge_intervals --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
