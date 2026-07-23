#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #48.
# See ../README.md § Benchmarks for what these numbers mean.
#
# The benched algorithm is the in-place layer four-way cyclic rotation (★): an n×n matrix is rotated
# 90° clockwise IN PLACE by walking concentric rings and cycling four cells at a time via a
# four-target parallel assignment (`top, right, bottom, left = left, top, right, bottom`). Unlike
# kata #46/#47 this kernel ALLOCATES NOTHING per solve — the matrix is its own scratch — so it is a
# pure compute + memory-access workload (index arithmetic + in-place swaps), not a Vec[Vec]
# allocation workload.
# Workload: a fixed n=20 matrix is rotated TOTAL=40000 times in place with the state carrying
# forward; each iteration punches one cell (`m[k%n][(k*7)%n] = k%97`, not reverted) then rotates and
# folds a position-weighted signature of every cell into a rolling checksum. The punched cell varies
# with the loop index (no hoisting of a constant result) and the checksum carries a loop-borne
# dependency, so this is a single-lane (seq) bench by construction.
#
# Requires: hyperfine (`brew install hyperfine`), rustc (rustup), clang, go,
# karac (with --features llvm for the codegen path).

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
require karac     "cargo install --path . --features llvm  (from karac checkout)"

if [ "${BENCH_JSON:-1}" = "1" ]; then
    require jq      "brew install jq"
    require python3 "python3 ships with macOS; or 'brew install python'"
fi
ROOT="$(cd ../../../.. && pwd)"
. "$ROOT/scripts/bench-lib.sh"


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

# Apples-to-apples safety comparator: Rust with overflow checks ON, matching
# Kāra's checked-by-default integer semantics (design.md § Arithmetic Overflow).
# `rustc -O` alone silently WRAPS; this `-C overflow-checks=on` variant traps
# like Kāra. The checksum modulus keeps every value well inside i64, so neither
# variant traps — the safety tax isolates codegen, not arithmetic.
build_rust_checked() {
    local src="$1"
    local out="target/$(basename "$src" .rs)_rschk"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling $src (overflow-checks=on) ..." >&2
        rustc -O -C overflow-checks=on "$src" -o "$out"
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
    local out="target/rotate_image_go_seq"
    local src="go-seq/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

build_rust         rotate_image.rs
build_rust_checked rotate_image.rs
build_c            rotate_image.c
build_kara         rotate_image.kara
build_kara_seq     rotate_image.kara
build_go_seq

# Sink agreement — every mirror's stdout must be byte-identical before timing.
expected="320060006"
mismatch=""
for pair in \
    'kara:./target/rotate_image_kara' \
    'kara_seq:./target/rotate_image_kara_seq' \
    'rust:./target/rotate_image' \
    'rust_chk:./target/rotate_image_rschk' \
    'c:./target/rotate_image_c' \
    'go:./target/rotate_image_go_seq'; do
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
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    py_out=$(python3 rotate_image.py)
    if [ "$py_out" != "$expected" ]; then
        echo "python sink mismatch: py=$py_out" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

bench_begin id=48 slug=rotate-image group=1-100 \
    title="Rotate Image" \
    workload="TOTAL=40000 in-place 90° rotations of a fixed n=20 matrix (one cell punched per iteration m[k%n][(k*7)%n]=k%97, not reverted), layer four-way cyclic swap via a four-target parallel assignment, every cell folded into a position-weighted checksum" \
    sink="$expected"

echo "=== runtime — seq lane (single-threaded in-place ring rotation) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach rotate_image --lane seq --mode codegen \
    --name 'kara rotate_image (seq, KARAC_AUTO_PAR=0)' --cmd './target/rotate_image_kara_seq'
rt_cmd --lang rust --approach rotate_image --lane seq --mode native \
    --name 'rust rotate_image' --cmd './target/rotate_image'
rt_cmd --lang rust --approach rotate_image_rschk --lane seq --mode native \
    --name 'rust rotate_image (overflow-checks=on, =Kara safety)' --cmd './target/rotate_image_rschk'
rt_cmd --lang c --approach rotate_image --lane seq --mode native \
    --name 'c    rotate_image' --cmd './target/rotate_image_c'
rt_cmd --lang go --approach rotate_image --lane seq --mode native \
    --name 'go   rotate_image' --cmd './target/rotate_image_go_seq'
rt_end

echo
echo "=== runtime — long workloads (py) ==="
rt_begin --warmup 1 --runs 3
rt_cmd --lang python --approach rotate_image --lane seq --mode interp \
    --name 'py   rotate_image' --cmd 'python3 rotate_image.py'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach rotate_image --mode codegen \
    --prepare 'rm -f target/rotate_image_kara rotate_image' \
    --name 'karac build rotate_image.kara' \
    --cmd 'sh -c "karac build rotate_image.kara >/dev/null && mv rotate_image target/rotate_image_kara"'
ce_cmd --lang rust --approach rotate_image --mode native \
    --prepare 'rm -f target/rotate_image' \
    --name 'rustc -O rotate_image.rs' --cmd 'rustc -O rotate_image.rs -o target/rotate_image'
ce_cmd --lang c --approach rotate_image --mode native \
    --prepare 'rm -f target/rotate_image_c' \
    --name 'clang -O3 rotate_image.c' --cmd 'clang -O3 rotate_image.c -o target/rotate_image_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach rotate_image --lane seq --mode codegen --path target/rotate_image_kara_seq
size_put --lang rust --approach rotate_image --lane seq --mode native  --path target/rotate_image
size_put --lang c    --approach rotate_image --lane seq --mode native  --path target/rotate_image_c
size_put --lang go   --approach rotate_image --lane seq --mode native  --path target/rotate_image_go_seq

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach rotate_image --lane seq --mode codegen --bytes "$(mem_peak ./target/rotate_image_kara_seq)"
mem_put --lang rust --approach rotate_image --lane seq --mode native  --bytes "$(mem_peak ./target/rotate_image)"
mem_put --lang c    --approach rotate_image --lane seq --mode native  --bytes "$(mem_peak ./target/rotate_image_c)"
mem_put --lang go   --approach rotate_image --lane seq --mode native  --bytes "$(mem_peak ./target/rotate_image_go_seq)"
mem_put --lang python --approach rotate_image --lane seq --mode interp --bytes "$(mem_peak python3 rotate_image.py)"

echo
echo "=== compile memory (cold) ==="
for src in rotate_image.kara; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach "$stem" --mode codegen --bytes "$bytes"
done
for src in rotate_image.rs; do
    stem="$(basename "$src" .rs)"
    out="target/$stem"
    rm -f "$out"
    cmem_put --lang rust --approach "$stem" --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in rotate_image.c; do
    stem="$(basename "$src" .c)"
    out="target/${stem}_c"
    rm -f "$out"
    cmem_put --lang c --approach "$stem" --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
