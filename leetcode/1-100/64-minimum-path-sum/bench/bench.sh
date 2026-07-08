#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #64.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Seq-only kata: the loop sweeps grid shapes (m = 2 + k%32, n = 2 + (k/32)%32),
# fills a rolling DP array (`dp[c] = cost + min(dp[c], dp[c-1])`, sized to the
# real column count n — costs break #62's axis symmetry, so no swap to the
# smaller side) with an inline cost predicate ((i*7 + c*3 + k) % 13 + 1, in
# [1,13]), and folds each min-path-sum into a rolling polynomial hash 1_000_000×
# per run. The hash
# `acc = (acc*131 + ans) % modulus` is a loop-carried dependency, so the loop is
# NOT a reduction karac's auto-par pass can split — the default `karac build`
# stays single-threaded, directly comparable to rustc -O / clang -O3 / go build
# on a per-core codegen-quality basis. Same discipline as kata #55/#62/#63.
#
# Requires: hyperfine, rustc, clang, go, karac (with --features llvm).

set -euo pipefail
cd "$(dirname "$0")"

STEM=minimum_path_sum

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
    printf '  %-30s %12s bytes (%6s MiB)\n' "$label" "$bytes" "$mib"
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
    local out="target/${STEM}_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust "${STEM}.rs"
build_c    "${STEM}.c"
build_kara "${STEM}.kara"
build_go_seq

# Sink agreement — every compiled mirror's stdout must be byte-identical before
# timing. Each iteration k folds the min-path-sum for the swept m×n grid (cost
# field also threaded on k) into a rolling hash
# `acc = (acc*131 + ans) % 1_000_000_007`. Over K=1_000_000 iters the sink is a
# fixed constant (verified against the Python oracle). Python runs K=100_000
# (sink 961487096) — timed separately, not cross-checked.
expected="355333129"
mismatch=""
for pair in \
    "kara:./target/${STEM}_kara" \
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
echo "sink (kara/rust/c/go): $expected"
echo

# Declare the kata for the JSON feed (no-op when BENCH_JSON=0).
bench_begin id=64 slug=minimum-path-sum group=1-100 \
    title="Minimum Path Sum" \
    workload="K=1_000_000 rolling min-path DP (cost + min RMW scan) over swept m×n grids / polynomial-hash sink" \
    sink="$expected"

echo "=== runtime — seq lane (apples-to-apples, single-threaded) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach minimum_path_sum --lane seq --mode codegen \
    --name "kara ${STEM}" --cmd "./target/${STEM}_kara"
rt_cmd --lang rust --approach minimum_path_sum --lane seq --mode native \
    --name "rust ${STEM}" --cmd "./target/${STEM}"
rt_cmd --lang c --approach minimum_path_sum --lane seq --mode native \
    --name "c    ${STEM}" --cmd "./target/${STEM}_c"
rt_cmd --lang go --approach minimum_path_sum --lane seq --mode native \
    --name "go   ${STEM}" --cmd "./target/${STEM}_go_seq"
rt_end

echo
echo "=== runtime — Python (K=100k scaled-down) ==="
rt_begin --warmup 2 --runs 10
rt_cmd --lang python --approach minimum_path_sum --lane seq --mode interp \
    --name "py   ${STEM} (K=100k)" --cmd "python3 ${STEM}.py"
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach minimum_path_sum --mode codegen \
    --prepare "rm -f target/${STEM}_kara ${STEM}" \
    --name "karac build ${STEM}.kara" \
    --cmd "sh -c \"karac build ${STEM}.kara >/dev/null && mv ${STEM} target/${STEM}_kara\""
ce_cmd --lang rust --approach minimum_path_sum --mode native \
    --prepare "rm -f target/${STEM}" \
    --name "rustc -O ${STEM}.rs" --cmd "rustc -O ${STEM}.rs -o target/${STEM}"
ce_cmd --lang c --approach minimum_path_sum --mode native \
    --prepare "rm -f target/${STEM}_c" \
    --name "clang -O3 ${STEM}.c" --cmd "clang -O3 ${STEM}.c -o target/${STEM}_c"
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach minimum_path_sum --lane seq --mode codegen --path "target/${STEM}_kara"
size_put --lang rust --approach minimum_path_sum --lane seq --mode native  --path "target/${STEM}"
size_put --lang c    --approach minimum_path_sum --lane seq --mode native  --path "target/${STEM}_c"
size_put --lang go   --approach minimum_path_sum --lane seq --mode native  --path "target/${STEM}_go_seq"

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach minimum_path_sum --lane seq --mode codegen --bytes "$(mem_peak ./target/${STEM}_kara)"
mem_put --lang rust --approach minimum_path_sum --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM})"
mem_put --lang c    --approach minimum_path_sum --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM}_c)"
mem_put --lang go   --approach minimum_path_sum --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM}_go_seq)"

echo
echo "=== compile memory (cold) ==="
for src in "${STEM}.kara"; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in "${STEM}.rs"; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in "${STEM}.c"; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
