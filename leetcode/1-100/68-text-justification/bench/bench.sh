#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #68.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Seq-only kata: the ★'s greedy-pack + even-spread logic is run over a fixed
# 40-word list 300_000× at a SWEPT width (max_width = 10 + k%40), STREAMING the
# bytes it would emit (word chars + gap spaces) into a rolling polynomial hash
# instead of building line strings. No per-call allocation, so it measures the
# packing/spacing codegen (greedy fit + `total / gaps` + `total % gaps` +
# extra-left placement + word-byte reads), not the allocator. The hash
# `h = (h*131 + byte) % modulus` is a loop-carried dependency, so the loop is
# NOT a reduction karac's auto-par pass can split — the default `karac build`
# stays single-threaded, directly comparable to rustc -O / clang -O3 / go build
# on a per-core codegen-quality basis. Same discipline as kata #55/#62/#63/#64/#66.
#
# Requires: hyperfine, rustc, clang, go, karac (with --features llvm).

set -euo pipefail
cd "$(dirname "$0")"

STEM=text_justification

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
# timing. Each iteration justifies the fixed word list at width 10 + k%40 and
# folds the emitted bytes into a rolling hash `h = (h*131 + byte) % 1_000_000_007`.
# Over K=300_000 iters the sink is a fixed constant (verified against the Python
# oracle). Python runs K=30_000 (1/10th) — timed separately, not cross-checked.
expected="335237798"
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
bench_begin id=68 slug=text-justification group=1-100 \
    title="Text Justification" \
    workload="K=300_000 greedy-pack+even-spread over a fixed 40-word list at swept width / streamed-byte polynomial-hash sink" \
    sink="$expected"

echo "=== runtime — seq lane (apples-to-apples, single-threaded) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach text_justification --lane seq --mode codegen \
    --name "kara ${STEM}" --cmd "./target/${STEM}_kara"
rt_cmd --lang rust --approach text_justification --lane seq --mode native \
    --name "rust ${STEM}" --cmd "./target/${STEM}"
rt_cmd --lang c --approach text_justification --lane seq --mode native \
    --name "c    ${STEM}" --cmd "./target/${STEM}_c"
rt_cmd --lang go --approach text_justification --lane seq --mode native \
    --name "go   ${STEM}" --cmd "./target/${STEM}_go_seq"
rt_end

echo
echo "=== runtime — Python (K=30k scaled-down) ==="
rt_begin --warmup 2 --runs 10
rt_cmd --lang python --approach text_justification --lane seq --mode interp \
    --name "py   ${STEM} (K=30k)" --cmd "python3 ${STEM}.py"
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach text_justification --mode codegen \
    --prepare "rm -f target/${STEM}_kara ${STEM}" \
    --name "karac build ${STEM}.kara" \
    --cmd "sh -c \"karac build ${STEM}.kara >/dev/null && mv ${STEM} target/${STEM}_kara\""
ce_cmd --lang rust --approach text_justification --mode native \
    --prepare "rm -f target/${STEM}" \
    --name "rustc -O ${STEM}.rs" --cmd "rustc -O ${STEM}.rs -o target/${STEM}"
ce_cmd --lang c --approach text_justification --mode native \
    --prepare "rm -f target/${STEM}_c" \
    --name "clang -O3 ${STEM}.c" --cmd "clang -O3 ${STEM}.c -o target/${STEM}_c"
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach text_justification --lane seq --mode codegen --path "target/${STEM}_kara"
size_put --lang rust --approach text_justification --lane seq --mode native  --path "target/${STEM}"
size_put --lang c    --approach text_justification --lane seq --mode native  --path "target/${STEM}_c"
size_put --lang go   --approach text_justification --lane seq --mode native  --path "target/${STEM}_go_seq"

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach text_justification --lane seq --mode codegen --bytes "$(mem_peak ./target/${STEM}_kara)"
mem_put --lang rust --approach text_justification --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM})"
mem_put --lang c    --approach text_justification --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM}_c)"
mem_put --lang go   --approach text_justification --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM}_go_seq)"

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
