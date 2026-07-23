#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #204.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Kara's `bench/count.kara` carries a `#[par_unordered]` attribute that
# opts the outer loop into the auto-par collect-style codegen path
# (Phase 3 in karac-rust). Rust/C/Python are idiomatic single-threaded
# implementations — the comparison framing is "auto-par Kara vs the code
# a programmer writes when they don't reach for rayon / OpenMP." A
# parallel Rust row (rayon) is a worthwhile follow-up for transparency
# but the per-iter `is_prime()` work is heavy enough that even the
# single-threaded baselines are honest comparators.
#
# Requires: hyperfine (`brew install hyperfine`), rustc (rustup), clang, karac.

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
require cargo     "rustup (https://rustup.rs)  — needed for the rayon-parallel Rust variant"
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

print_mem() {
    local label="$1" bytes="$2"
    local mib
    mib=$(awk -v b="$bytes" 'BEGIN{printf "%.1f", b/1048576}')
    printf '  %-30s %12s bytes (%6s MiB)\n' "$label" "$bytes" "$mib"
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

build_rust count.rs
build_rust_ovf count.rs
build_c    count.c
build_kara count.kara
build_kara count_seq.kara

# Rayon variant lives in its own Cargo project under bench/rayon/ because
# rayon is a third-party crate (no rustc single-file path for that).
# `cargo build --release` is incremental; subsequent invocations are
# near-instant when the source hasn't changed.
echo "building rayon variant (cargo) ..." >&2
( cd rayon && cargo build --release --quiet )
cp -f rayon/target/release/count_rayon target/count_rayon

# Go variants — `go build` requires a module root, so each lives in its
# own subdir with its own go.mod. Go's default build is already release-
# mode (no -O flag exists); the compiler always inlines + optimizes.
build_go() {
    local dir="$1"
    local out="target/$(basename "$dir" | tr '-' '_')"
    if [ ! -x "$out" ] || [ "$dir/main.go" -nt "$out" ]; then
        echo "compiling $dir ..." >&2
        ( cd "$dir" && go build -o "../$out" . )
    fi
}
build_go go-seq
build_go go-par

# C pthreads par mirror (par-lane metal floor) — clang needs -lpthread, so it
# can't go through build_c (which has no link flag).
if [ ! -x target/count_c_par ] || [ count_par.c -nt target/count_c_par ]; then
    echo "compiling count_par.c (pthreads) ..." >&2
    clang -O3 count_par.c -o target/count_c_par -lpthread
fi

# Sanity: all four impls must agree on the (count, sum) sink before we
# time them. Python skipped from sink check by default — at N=10M it
# takes ~30s and bench.sh would block waiting on it. Set
# `KARA_BENCH_INCLUDE_PY=1` to opt in.
kara_sink=$(./target/count_kara)
kara_seq_sink=$(./target/count_seq_kara)
rust_sink=$(./target/count)
rust_ovf_sink=$(./target/count_ovf)
c_sink=$(./target/count_c)
c_par_sink=$(./target/count_c_par)
rayon_sink=$(./target/count_rayon)
go_seq_sink=$(./target/go_seq)
go_par_sink=$(./target/go_par)
mismatch=""
for pair in "kara_seq:$kara_seq_sink" "rust:$rust_sink" "rust_ovf:$rust_ovf_sink" "c:$c_sink" "c_par:$c_par_sink" "rayon:$rayon_sink" "go_seq:$go_seq_sink" "go_par:$go_par_sink"; do
    name="${pair%%:*}"
    sink="${pair#*:}"
    if [ "$sink" != "$kara_sink" ]; then
        mismatch="$mismatch $name=$(echo "$sink" | tr '\n' ',')"
    fi
done
if [ -n "$mismatch" ]; then
    echo "sink mismatch (vs kara=$(echo "$kara_sink" | tr '\n' ',')):$mismatch" >&2
    exit 1
fi
echo "sink (kara == kara-seq == rust == c == rust+rayon == go-seq == go-par): $(echo "$kara_sink" | tr '\n' ' ' | sed 's/ $//')"
if [ "${KARA_BENCH_INCLUDE_PY:-0}" = "1" ]; then
    py_sink=$(python3 count.py)
    if [ "$kara_sink" != "$py_sink" ]; then
        echo "python sink mismatch: kara=$kara_sink py=$py_sink" >&2
        exit 1
    fi
    echo "python: matches"
fi
echo

# Declare the kata for the JSON feed (no-op when BENCH_JSON=0).
bench_begin id=204 slug=count-primes group=201-300 \
    title="Count Primes" workload="N=10^7 list primes" \
    sink="$(echo "$kara_sink" | tr '\n' ' ' | sed 's/ $//')"

echo "=== runtime ==="
rt_begin --warmup 3 --runs 10
rt_cmd --lang kara --approach count --lane par --mode codegen \
    --name 'kara count (codegen, #[par_unordered])' --cmd './target/count_kara'
rt_cmd --lang kara --approach count --lane seq --mode codegen \
    --name 'kara count (codegen, single-threaded)' --cmd './target/count_seq_kara'
rt_cmd --lang rust --approach count --lane seq --mode native \
    --name 'rust count (single-threaded)' --cmd './target/count'
rt_cmd --lang rust_ovf --approach count --lane seq --mode native \
    --name 'rust count (overflow-checks=on, equal-safety)' --cmd './target/count_ovf'
rt_cmd --lang rust --approach count --lane par --mode native \
    --name 'rust count (rayon par_iter)' --cmd './target/count_rayon'
rt_cmd --lang go --approach count --lane seq --mode native \
    --name 'go   count (single-threaded)' --cmd './target/go_seq'
rt_cmd --lang go --approach count --lane par --mode native \
    --name 'go   count (goroutines)' --cmd './target/go_par'
rt_cmd --lang c --approach count --lane seq --mode native \
    --name 'c    count (single-threaded)' --cmd './target/count_c'
rt_cmd --lang c --approach count --lane par --mode native \
    --name 'c    count (pthreads — metal floor)' --cmd './target/count_c_par'
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach count --mode codegen \
    --prepare 'rm -f target/count_kara count' \
    --name 'karac build count.kara' \
    --cmd 'sh -c "karac build count.kara >/dev/null && mv count target/count_kara"'
ce_cmd --lang rust --approach count --mode native \
    --prepare 'rm -f target/count' \
    --name 'rustc -O count.rs' --cmd 'rustc -O count.rs -o target/count'
ce_cmd --lang c --approach count --mode native \
    --prepare 'rm -f target/count_c' \
    --name 'clang -O3 count.c' --cmd 'clang -O3 count.c -o target/count_c'
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach count --lane par --mode codegen --path target/count_kara
size_put --lang kara --approach count --lane seq --mode codegen --path target/count_seq_kara
size_put --lang rust --approach count --lane seq --mode native  --path target/count
size_put --lang rust --approach count --lane par --mode native  --path target/count_rayon
size_put --lang go   --approach count --lane seq --mode native  --path target/go_seq
size_put --lang go   --approach count --lane par --mode native  --path target/go_par
size_put --lang c    --approach count --lane seq --mode native  --path target/count_c
size_put --lang c    --approach count --lane par --mode native  --path target/count_c_par

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach count --lane par --mode codegen --bytes "$(mem_peak ./target/count_kara)"
mem_put --lang kara --approach count --lane seq --mode codegen --bytes "$(mem_peak ./target/count_seq_kara)"
mem_put --lang rust --approach count --lane seq --mode native  --bytes "$(mem_peak ./target/count)"
mem_put --lang rust --approach count --lane par --mode native  --bytes "$(mem_peak ./target/count_rayon)"
mem_put --lang go   --approach count --lane seq --mode native  --bytes "$(mem_peak ./target/go_seq)"
mem_put --lang go   --approach count --lane par --mode native  --bytes "$(mem_peak ./target/go_par)"
mem_put --lang c    --approach count --lane seq --mode native  --bytes "$(mem_peak ./target/count_c)"
mem_put --lang c    --approach count --lane par --mode native  --bytes "$(mem_peak ./target/count_c_par)"

echo
echo "=== compile memory (cold) ==="
rm -f target/count_kara count
cmem_put --lang kara --approach count --mode codegen --bytes "$(mem_peak karac build count.kara)"
mv count target/count_kara 2>/dev/null || true
rm -f target/count
cmem_put --lang rust --approach count --mode native --bytes "$(mem_peak rustc -O count.rs -o target/count)"
rm -f target/count_c
cmem_put --lang c --approach count --mode native --bytes "$(mem_peak clang -O3 count.c -o target/count_c)"

echo
bench_emit
