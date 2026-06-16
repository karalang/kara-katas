#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #23
# (Merge k Sorted Lists). See ../README.md § Benchmarks for what these
# numbers mean.
#
# Two-lane kata (BENCH.md § Implicit auto-par): the default `karac
# build` links the par-dispatch runtime surface (the K-loop's
# `total = total + …` fold is reduction-shaped), so we build TWO kara
# binaries:
#
#   divide_and_conquer_kara_seq — KARAC_AUTO_PAR=0, single-threaded.
#                                 Within-lane comparator vs rust / c / go.
#   divide_and_conquer_kara     — default karac build.
#                                 Reported separately per the two-lane
#                                 discipline.
#
# The workload is RC-node allocator churn + pointer-chasing: every
# iteration builds k = 8 stride-interleaved 128-node lists (1024 nodes
# malloc'd), pairwise-merges them down to one over log k = 3 rounds
# (every round fully interleaves), sums the merged list, and frees it.
# No arithmetic kernel, no sort — the k-way generalization of kata #21.
#
# Requires: hyperfine, rustc, clang, go, karac.

set -euo pipefail
cd "$(dirname "$0")"

STEM=divide_and_conquer

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

# Sequential variant — KARAC_AUTO_PAR=0 short-circuits codegen.rs's
# Slice 6 auto-par gate back to plain sequential compile_block. The
# documented mechanism (BENCH.md § Dual-binary bench.sh pattern) for
# side-by-side seq-vs-par benchmarking of the same source. This is the
# row that's directly comparable to rustc -O / clang -O3 / go build on a
# per-core codegen-quality basis.
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
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

# Par-lane comparators — hand-tuned parallelism vs Kāra auto-par. Each
# parallelizes the SAME K=100k outer (build-merge-sum) reduction by hand.
build_rayon() {
    local out="target/${STEM}_rayon"
    local src="rayon/src/main.rs"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "building rayon variant (cargo) ..." >&2
        ( cd rayon && cargo build --release --quiet )
        cp -f "rayon/target/release/${STEM}_rayon" "$out"
    fi
}
build_go_par() {
    local out="target/${STEM}_go_par"
    local src="go-par/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling go-par ..." >&2
        ( cd go-par && go build -o "../$out" . )
    fi
}
# C pthreads — the par-lane bare-metal FLOOR (raw OS threads, no runtime).
build_c_par() {
    local out="target/${STEM}_c_par"
    local src="${STEM}_par.c"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling c-par (pthreads) ..." >&2
        clang -O3 "$src" -o "$out" -lpthread
    fi
}

build_rust     "${STEM}.rs"
build_c        "${STEM}.c"
build_kara     "${STEM}.kara"
build_kara_seq "${STEM}.kara"
build_go_seq
build_rayon
build_go_par
build_c_par

# Sink agreement — every compiled mirror's stdout must be byte-identical
# before timing. K=100k iterations x sum([0..1023]) = 100000 x 523776
# = 52,377,600,000. Python runs a scaled-down K=10k (timed separately,
# not in this cross-check).
expected=$(./target/${STEM}_kara)
mismatch=""
for pair in \
    "kara_seq:./target/${STEM}_kara_seq" \
    "rust:./target/${STEM}" \
    "c:./target/${STEM}_c" \
    "go:./target/${STEM}_go_seq" \
    "rayon:./target/${STEM}_rayon" \
    "go_par:./target/${STEM}_go_par" \
    "c_par:./target/${STEM}_c_par"; do
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
bench_begin id=23 slug=merge-k-sorted-lists group=1-100 \
    title="Merge k Sorted Lists" \
    workload="K=100k x (build 8x128-node stride-interleaved lists, pairwise-merge, sum)" \
    sink="$expected"

echo "=== runtime — seq lane (apples-to-apples, single-threaded) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach divide_and_conquer --lane seq --mode codegen \
    --name "kara ${STEM} (seq, KARAC_AUTO_PAR=0)" --cmd "./target/${STEM}_kara_seq"
rt_cmd --lang rust --approach divide_and_conquer --lane seq --mode native \
    --name "rust ${STEM}" --cmd "./target/${STEM}"
rt_cmd --lang c --approach divide_and_conquer --lane seq --mode native \
    --name "c    ${STEM}" --cmd "./target/${STEM}_c"
rt_cmd --lang go --approach divide_and_conquer --lane seq --mode native \
    --name "go   ${STEM}" --cmd "./target/${STEM}_go_seq"
rt_end

echo
echo "=== runtime — auto-par regime (kara default, multi-core) ==="
# Default `karac build` output: karac's auto-par-on-reduction recognizes
# the K=100k outer (build-merge-sum) reduction in `main` and emits a
# `karac_par_reduce` dispatch. NOT directly comparable to the single-
# thread rows above per BENCH.md's two-lane discipline — reported
# separately so the production-default Kara behavior stays visible. The
# c/rust/go par comparators parallelize the SAME K-loop by hand.
# Heavier warmup (10/50) absorbs worker-pool init noise.
rt_begin --warmup 10 --runs 50
rt_cmd --lang kara --approach divide_and_conquer --lane par --mode codegen \
    --name "kara ${STEM} (auto-par default)" --cmd "./target/${STEM}_kara"
rt_cmd --lang c --approach divide_and_conquer --lane par --mode native \
    --name "c    ${STEM} (pthreads — metal floor)" --cmd "./target/${STEM}_c_par"
rt_cmd --lang rust --approach divide_and_conquer --lane par --mode native \
    --name "rust ${STEM} (rayon par_iter)" --cmd "./target/${STEM}_rayon"
rt_cmd --lang go --approach divide_and_conquer --lane par --mode native \
    --name "go   ${STEM} (goroutines + WaitGroup)" --cmd "./target/${STEM}_go_par"
rt_end

echo
echo "=== runtime — Python (scaled K=10k) ==="
# Allocation/pointer-chasing-bound workload: CPython allocates nodes in
# C, so the interpreter gap stays narrow (kata-21 precedent). Timed at
# K=10k; project x10 to compare against the compiled mirrors' K=100k.
rt_begin --warmup 2 --runs 10
rt_cmd --lang python --approach divide_and_conquer --lane seq --mode interp \
    --name "py   ${STEM} (K=10k)" --cmd "python3 ${STEM}.py"
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach divide_and_conquer --mode codegen \
    --prepare "rm -f target/${STEM}_kara ${STEM}" \
    --name "karac build ${STEM}.kara" \
    --cmd "sh -c \"karac build ${STEM}.kara >/dev/null && mv ${STEM} target/${STEM}_kara\""
ce_cmd --lang rust --approach divide_and_conquer --mode native \
    --prepare "rm -f target/${STEM}" \
    --name "rustc -O ${STEM}.rs" --cmd "rustc -O ${STEM}.rs -o target/${STEM}"
ce_cmd --lang c --approach divide_and_conquer --mode native \
    --prepare "rm -f target/${STEM}_c" \
    --name "clang -O3 ${STEM}.c" --cmd "clang -O3 ${STEM}.c -o target/${STEM}_c"
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach divide_and_conquer --lane seq --mode codegen --path "target/${STEM}_kara_seq"
size_put --lang kara --approach divide_and_conquer --lane par --mode codegen --path "target/${STEM}_kara"
size_put --lang c    --approach divide_and_conquer --lane par --mode native  --path "target/${STEM}_c_par"
size_put --lang rust --approach divide_and_conquer --lane par --mode native  --path "target/${STEM}_rayon"
size_put --lang go   --approach divide_and_conquer --lane par --mode native  --path "target/${STEM}_go_par"
size_put --lang rust --approach divide_and_conquer --lane seq --mode native  --path "target/${STEM}"
size_put --lang c    --approach divide_and_conquer --lane seq --mode native  --path "target/${STEM}_c"
size_put --lang go   --approach divide_and_conquer --lane seq --mode native  --path "target/${STEM}_go_seq"

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach divide_and_conquer --lane seq --mode codegen --bytes "$(mem_peak ./target/${STEM}_kara_seq)"
mem_put --lang kara --approach divide_and_conquer --lane par --mode codegen --bytes "$(mem_peak ./target/${STEM}_kara)"
mem_put --lang c    --approach divide_and_conquer --lane par --mode native  --bytes "$(mem_peak ./target/${STEM}_c_par)"
mem_put --lang rust --approach divide_and_conquer --lane par --mode native  --bytes "$(mem_peak ./target/${STEM}_rayon)"
mem_put --lang go   --approach divide_and_conquer --lane par --mode native  --bytes "$(mem_peak ./target/${STEM}_go_par)"
mem_put --lang rust --approach divide_and_conquer --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM})"
mem_put --lang c    --approach divide_and_conquer --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM}_c)"
mem_put --lang go   --approach divide_and_conquer --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM}_go_seq)"

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
