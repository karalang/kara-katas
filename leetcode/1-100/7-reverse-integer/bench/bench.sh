#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #7.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Seq-only kata. Requires: hyperfine, rustc, clang, go, karac.

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

expected=$(./target/${STEM}_kara)
mismatch=""
for pair in \
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

echo "=== runtime — short workloads (compiled) ==="
hyperfine \
    --warmup 5 \
    --runs 30 \
    --shell=none \
    --command-name "kara ${STEM} (codegen)" "./target/${STEM}_kara" \
    --command-name "rust ${STEM}"           "./target/${STEM}" \
    --command-name "c    ${STEM}"           "./target/${STEM}_c" \
    --command-name "go   ${STEM}"           "./target/${STEM}_go_seq"

echo
echo "=== runtime — long workloads (py, K=1M scaled-down) ==="
# Python at K=50M takes multi-minute per sample; sample 50× smaller K
# and quote the ratio in the README.
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
hyperfine \
    --warmup 1 \
    --runs 10 \
    --shell=none \
    --prepare "rm -f target/${STEM}_kara ${STEM}" \
    --command-name "karac build ${STEM}.kara" "sh -c \"karac build ${STEM}.kara >/dev/null && mv ${STEM} target/${STEM}_kara\"" \
    --prepare "rm -f target/${STEM}" \
    --command-name "rustc -O ${STEM}.rs"      "rustc -O ${STEM}.rs -o target/${STEM}" \
    --prepare "rm -f target/${STEM}_c" \
    --command-name "clang -O3 ${STEM}.c"      "clang -O3 ${STEM}.c -o target/${STEM}_c"

echo
echo "=== binary size ==="
for spec in \
    "kara ${STEM}:target/${STEM}_kara" \
    "rust ${STEM}:target/${STEM}" \
    "c    ${STEM}:target/${STEM}_c" \
    "go   ${STEM}:target/${STEM}_go_seq"; do
    label="${spec%%:*}"
    path="${spec##*:}"
    bytes=$(wc -c < "$path" | tr -d ' ')
    kib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1024}')
    printf '  %-30s %10s bytes (%6s KiB)\n' "$label" "$bytes" "$kib"
done

echo
echo "=== runtime memory (peak) ==="
print_mem "kara ${STEM} (codegen)" "$(mem_peak ./target/${STEM}_kara)"
print_mem "rust ${STEM}"           "$(mem_peak ./target/${STEM})"
print_mem "c    ${STEM}"           "$(mem_peak ./target/${STEM}_c)"
print_mem "go   ${STEM}"           "$(mem_peak ./target/${STEM}_go_seq)"

echo
echo "=== compile memory (cold) ==="
for src in "${STEM}.kara"; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    print_mem "karac build $src" "$bytes"
done
for src in "${STEM}.rs"; do
    out="target/$(basename "$src" .rs)"
    rm -f "$out"
    print_mem "rustc -O $src" "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in "${STEM}.c"; do
    out="target/$(basename "$src" .c)_c"
    rm -f "$out"
    print_mem "clang -O3 $src" "$(mem_peak clang -O3 "$src" -o "$out")"
done
