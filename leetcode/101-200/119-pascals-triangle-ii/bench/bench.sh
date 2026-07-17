#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #119.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Pascal's Triangle II asks only for the rowIndex-th row in O(rowIndex) space, so this is an
# IN-PLACE INDEX-ASSIGNMENT workload (no nested Vec): each rep computes the row for a DATA-DEPENDENT
# rowIndex (30 + acc%20, so 30..49, seeded by the running hash so get_row() can't be hoisted),
# building one Vec[i64] of length rowIndex+1 and updating it in place right-to-left
# (row[k] = row[k] + row[k-1]), folding every entry. Dominated by the O(k^2) in-place updates — a
# single small Vec per rep. C uses a malloc'd long[], Go a []int64, Rust a Vec<i64>; Kara a Vec[i64].
# NOTE: on this pattern kara keeps a per-iteration bounds check LLVM elides for Rust (kara
# B-2026-07-17-1), so kara trails equal-safety Rust here. Default `karac build` == KARAC_AUTO_PAR=0.
# EQUAL-SAFETY: karac checks integer overflow by default while `rustc -O` wraps, so a
# `rustc -O -C overflow-checks=on` row is the like-for-like (kata #69's discipline).
# Python runs a smaller K (pure-Python is slow) — timed separately, NOT cross-checked.
#
# Requires: hyperfine, rustc, clang, go, karac (with --features llvm).

set -euo pipefail
cd "$(dirname "$0")"

STEM=get_row

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
# timing. Over K=6000000 passes the fold is a fixed constant; Python runs a
# smaller K and is intentionally excluded from this check.
expected="72342709"
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

bench_begin id=119 slug=get_row group=101-200 \
    title="Pascal's Triangle II" \
    workload="each rep computes the rowIndex-th Pascal row for a data-dependent rowIndex (30+acc%20, 30..49) as one Vec[i64] updated in place right-to-left (row[k]=row[k]+row[k-1]), folding every entry; K=440000 reps — the in-place index-assignment regime" \
    sink="$expected"

echo "=== runtime — seq lane (apples-to-apples, single-threaded) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach get_row --lane seq --mode codegen \
    --name "kara ${STEM}" --cmd "./target/${STEM}_kara"
rt_cmd --lang rust --approach get_row --lane seq --mode native \
    --name "rust ${STEM}" --cmd "./target/${STEM}"
rt_cmd --lang rust --approach get_row_ovf --lane seq --mode native \
    --name "rust ${STEM} (overflow-checks=on)" --cmd "./target/${STEM}_ovf"
rt_cmd --lang c --approach get_row --lane seq --mode native \
    --name "c    ${STEM}" --cmd "./target/${STEM}_c"
rt_cmd --lang go --approach get_row --lane seq --mode native \
    --name "go   ${STEM}" --cmd "./target/${STEM}_go_seq"
rt_end

echo
echo "=== runtime — Python (smaller K, timed separately, not cross-checked) ==="
rt_begin --warmup 2 --runs 10
rt_cmd --lang python --approach get_row --lane seq --mode interp \
    --name "py   ${STEM} (K=22000)" --cmd "python3 ${STEM}.py"
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach get_row --mode codegen \
    --prepare "rm -f target/${STEM}_kara ${STEM}" \
    --name "karac build ${STEM}.kara" \
    --cmd "sh -c \"karac build ${STEM}.kara >/dev/null && mv ${STEM} target/${STEM}_kara\""
ce_cmd --lang rust --approach get_row --mode native \
    --prepare "rm -f target/${STEM}" \
    --name "rustc -O ${STEM}.rs" --cmd "rustc -O ${STEM}.rs -o target/${STEM}"
ce_cmd --lang c --approach get_row --mode native \
    --prepare "rm -f target/${STEM}_c" \
    --name "clang -O3 ${STEM}.c" --cmd "clang -O3 ${STEM}.c -o target/${STEM}_c"
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach get_row --lane seq --mode codegen --path "target/${STEM}_kara"
size_put --lang rust --approach get_row --lane seq --mode native  --path "target/${STEM}"
size_put --lang c    --approach get_row --lane seq --mode native  --path "target/${STEM}_c"
size_put --lang go   --approach get_row --lane seq --mode native  --path "target/${STEM}_go_seq"

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach get_row --lane seq --mode codegen --bytes "$(mem_peak ./target/${STEM}_kara)"
mem_put --lang rust --approach get_row --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM})"
mem_put --lang c    --approach get_row --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM}_c)"
mem_put --lang go   --approach get_row --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM}_go_seq)"

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
