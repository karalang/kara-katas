#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #93.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Seq-only kata: the segment enumeration + validation (which three cut points give four
# valid 0..255 segments) is run as an ENUMERATE-and-fold — the three-dot triple loop
# with the leading-zero / <=255 validity test folds every valid quadruple's segment
# values into a threaded polynomial-hash accumulator (no address strings built), K=6.5M
# iterations seeded by the loop index so nothing hoists. CRUCIALLY the input length
# varies per iteration (`n = 4 + iter%9`, i.e. 4..12 — the real range for a restorable
# string): a FIXED n=12 lets clang/rustc statically unroll and vectorize the fixed-shape
# enumeration, erasing the checked scalar work and distorting the bench (CLAUDE.md
# "vectorizable loop" pitfall — the fixed version put unchecked C/rust 4-5x ahead purely
# on SIMD, an artifact). Data-dependent length keeps every engine doing honest scalar
# work. The compute measured is the enumerate + validate inner loops. The loop-carried
# hash is NOT a reduction karac's auto-par pass can split, so the default `karac build`
# stays single-threaded (verified equal to KARAC_AUTO_PAR=0). EQUAL-SAFETY: karac checks
# integer overflow by default while `rustc -O` wraps, so a `rustc -O -C overflow-checks=on`
# row is included as the faithful like-for-like (kata #69's discipline). Python runs a
# smaller K (a pure-Python loop is slow) — timed separately, NOT cross-checked.
#
# Requires: hyperfine, rustc, clang, go, karac (with --features llvm).

set -euo pipefail
cd "$(dirname "$0")"

STEM=restore_ip

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

build_rust_ovf() {
    local src="$1"
    local out="target/$(basename "$src" .rs)_ovf"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling $src (overflow-checks=on) ..." >&2
        rustc -O -C overflow-checks=on "$src" -o "$out"
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

build_rust     "${STEM}.rs"
build_rust_ovf "${STEM}.rs"
build_c        "${STEM}.c"
build_kara     "${STEM}.kara"
build_go_seq

# Sink agreement — every compiled mirror's stdout must be byte-identical before
# timing. Over K=6.5M passes the fold is a fixed constant; Python runs a
# smaller K and is intentionally excluded from this check.
expected="467547481"
mismatch=""
for pair in \
    "kara:./target/${STEM}_kara" \
    "rust:./target/${STEM}" \
    "rust_ovf:./target/${STEM}_ovf" \
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
echo "sink (kara/rust/rust_ovf/c/go): $expected"
echo

bench_begin id=93 slug=restore_ip group=1-100 \
    title="Restore IP Addresses" \
    workload="K=6.5M enumerate-and-fold passes over the three-dot segment enumeration + validity test, input length data-dependent per iteration (n=4..12) to defeat fixed-shape vectorization, polynomial-hash sink" \
    sink="$expected"

echo "=== runtime — seq lane (apples-to-apples, single-threaded) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach restore_ip --lane seq --mode codegen \
    --name "kara ${STEM}" --cmd "./target/${STEM}_kara"
rt_cmd --lang rust --approach restore_ip --lane seq --mode native \
    --name "rust ${STEM}" --cmd "./target/${STEM}"
rt_cmd --lang rust --approach restore_ip_ovf --lane seq --mode native \
    --name "rust ${STEM} (overflow-checks=on)" --cmd "./target/${STEM}_ovf"
rt_cmd --lang c --approach restore_ip --lane seq --mode native \
    --name "c    ${STEM}" --cmd "./target/${STEM}_c"
rt_cmd --lang go --approach restore_ip --lane seq --mode native \
    --name "go   ${STEM}" --cmd "./target/${STEM}_go_seq"
rt_end

echo
echo "=== runtime — Python (smaller K, timed separately, not cross-checked) ==="
rt_begin --warmup 2 --runs 10
rt_cmd --lang python --approach restore_ip --lane seq --mode interp \
    --name "py   ${STEM} (K=200000)" --cmd "python3 ${STEM}.py"
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach restore_ip --mode codegen \
    --prepare "rm -f target/${STEM}_kara ${STEM}" \
    --name "karac build ${STEM}.kara" \
    --cmd "sh -c \"karac build ${STEM}.kara >/dev/null && mv ${STEM} target/${STEM}_kara\""
ce_cmd --lang rust --approach restore_ip --mode native \
    --prepare "rm -f target/${STEM}" \
    --name "rustc -O ${STEM}.rs" --cmd "rustc -O ${STEM}.rs -o target/${STEM}"
ce_cmd --lang c --approach restore_ip --mode native \
    --prepare "rm -f target/${STEM}_c" \
    --name "clang -O3 ${STEM}.c" --cmd "clang -O3 ${STEM}.c -o target/${STEM}_c"
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach restore_ip --lane seq --mode codegen --path "target/${STEM}_kara"
size_put --lang rust --approach restore_ip --lane seq --mode native  --path "target/${STEM}"
size_put --lang c    --approach restore_ip --lane seq --mode native  --path "target/${STEM}_c"
size_put --lang go   --approach restore_ip --lane seq --mode native  --path "target/${STEM}_go_seq"

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach restore_ip --lane seq --mode codegen --bytes "$(mem_peak ./target/${STEM}_kara)"
mem_put --lang rust --approach restore_ip --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM})"
mem_put --lang c    --approach restore_ip --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM}_c)"
mem_put --lang go   --approach restore_ip --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM}_go_seq)"

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
