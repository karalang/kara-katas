#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #12.
# See ../README.md § Benchmarks for what these numbers mean.
#
# Two-lane kata (BENCH.md § Implicit auto-par): karac's auto-par-on-
# reduction recognizes the `sum = sum + score_roman(r)` accumulator in
# main's K=10M loop and emits a `karac_par_reduce` dispatch by default.
# We build TWO kara binaries:
#
#   greedy_kara_seq — KARAC_AUTO_PAR=0, single-threaded.
#                     Within-lane comparator vs rust / c / go.
#   greedy_kara     — default karac build, auto-par on.
#                     Reported separately so the production-default
#                     Kara behavior stays visible.
#
# Per BENCH.md's two-lane discipline, cross-lane wall-time ratios are
# not meaningful — the README headlines the within-lane seq comparison,
# and reports the auto-par regime as a separate sub-section.
#
# Also emits structured JSON (bench/results.json) via scripts/bench-lib.sh;
# the human-readable console output below is unaffected.
#
# Requires: hyperfine, rustc, clang, go, karac.

set -euo pipefail
cd "$(dirname "$0")"

STEM=greedy

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
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ] || [ "$(command -v karac)" -nt "$out" ]; then
        echo "compiling go-seq ..." >&2
        ( cd go-seq && go build -o "../$out" . )
    fi
}

# Par-lane comparators — hand-tuned parallelism vs Kāra auto-par. Each
# parallelizes the SAME K=10M outer reduction by hand.
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
bench_begin id=12 slug=integer-to-roman group=1-100 \
    title="Integer to Roman" \
    workload="kara/rust/c/go K=10^7 reduction over roman scores; py K=10^6 scaled-down" \
    sink="$expected"

echo "=== runtime — seq lane (apples-to-apples, single-threaded) ==="
# All four comparators here run single-threaded. The kara binary built
# with KARAC_AUTO_PAR=0 short-circuits auto-par dispatch back to plain
# sequential codegen — directly comparable to rustc -O / clang -O3 /
# go build on a per-core codegen-quality basis.
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach greedy --lane seq --mode codegen \
    --name "kara ${STEM} (seq, KARAC_AUTO_PAR=0)" --cmd "./target/${STEM}_kara_seq"
rt_cmd --lang rust --approach greedy --lane seq --mode native \
    --name "rust ${STEM}" --cmd "./target/${STEM}"
rt_cmd --lang c --approach greedy --lane seq --mode native \
    --name "c    ${STEM}" --cmd "./target/${STEM}_c"
rt_cmd --lang go --approach greedy --lane seq --mode native \
    --name "go   ${STEM}" --cmd "./target/${STEM}_go_seq"
rt_end

echo
echo "=== runtime — auto-par regime (kara default, multi-core) ==="
# Default `karac build` output: karac's auto-par-on-reduction recognizes
# the K=10M reduction in `main` and emits a `karac_par_reduce` dispatch.
# NOT directly comparable to the single-thread rows above per BENCH.md's
# two-lane discipline — reported separately so the production-default
# Kara behavior stays visible. Heavier warmup (10/50) absorbs worker-pool
# init noise that otherwise inflates σ on short auto-par runs.
rt_begin --warmup 10 --runs 50
rt_cmd --lang kara --approach greedy --lane par --mode codegen \
    --name "kara ${STEM} (auto-par default)" --cmd "./target/${STEM}_kara"
rt_cmd --lang c --approach greedy --lane par --mode native \
    --name "c    ${STEM} (pthreads — metal floor)" --cmd "./target/${STEM}_c_par"
rt_cmd --lang rust --approach greedy --lane par --mode native \
    --name "rust ${STEM} (rayon par_iter)" --cmd "./target/${STEM}_rayon"
rt_cmd --lang go --approach greedy --lane par --mode native \
    --name "go   ${STEM} (goroutines + WaitGroup)" --cmd "./target/${STEM}_go_par"
rt_end

echo
echo "=== runtime — long workloads (py, K=1M scaled-down) ==="
# Python at K=10M takes multi-second per sample; sample 10× smaller K
# and quote the ratio in the README.
rt_begin --warmup 2 --runs 10
rt_cmd --lang python --approach greedy --lane seq --mode interp \
    --name "py   ${STEM} (K=1M)" --cmd "python3 ${STEM}.py"
rt_end

echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach greedy --mode codegen \
    --prepare "rm -f target/${STEM}_kara ${STEM}" \
    --name "karac build ${STEM}.kara" \
    --cmd "sh -c \"karac build ${STEM}.kara >/dev/null && mv ${STEM} target/${STEM}_kara\""
ce_cmd --lang rust --approach greedy --mode native \
    --prepare "rm -f target/${STEM}" \
    --name "rustc -O ${STEM}.rs" --cmd "rustc -O ${STEM}.rs -o target/${STEM}"
ce_cmd --lang c --approach greedy --mode native \
    --prepare "rm -f target/${STEM}_c" \
    --name "clang -O3 ${STEM}.c" --cmd "clang -O3 ${STEM}.c -o target/${STEM}_c"
ce_end

echo
echo "=== binary size ==="
size_put --lang kara --approach greedy --lane seq --mode codegen --path "target/${STEM}_kara_seq"
size_put --lang kara --approach greedy --lane par --mode codegen --path "target/${STEM}_kara"
size_put --lang c    --approach greedy --lane par --mode native  --path "target/${STEM}_c_par"
size_put --lang rust --approach greedy --lane par --mode native  --path "target/${STEM}_rayon"
size_put --lang go   --approach greedy --lane par --mode native  --path "target/${STEM}_go_par"
size_put --lang rust --approach greedy --lane seq --mode native  --path "target/${STEM}"
size_put --lang c    --approach greedy --lane seq --mode native  --path "target/${STEM}_c"
size_put --lang go   --approach greedy --lane seq --mode native  --path "target/${STEM}_go_seq"

echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach greedy --lane seq --mode codegen --bytes "$(mem_peak ./target/${STEM}_kara_seq)"
mem_put --lang kara --approach greedy --lane par --mode codegen --bytes "$(mem_peak ./target/${STEM}_kara)"
mem_put --lang c    --approach greedy --lane par --mode native  --bytes "$(mem_peak ./target/${STEM}_c_par)"
mem_put --lang rust --approach greedy --lane par --mode native  --bytes "$(mem_peak ./target/${STEM}_rayon)"
mem_put --lang go   --approach greedy --lane par --mode native  --bytes "$(mem_peak ./target/${STEM}_go_par)"
mem_put --lang rust --approach greedy --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM})"
mem_put --lang c    --approach greedy --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM}_c)"
mem_put --lang go   --approach greedy --lane seq --mode native  --bytes "$(mem_peak ./target/${STEM}_go_seq)"

echo
echo "=== compile memory (cold) ==="
for src in "${STEM}.kara"; do
    stem="$(basename "$src" .kara)"
    rm -f "target/${stem}_kara" "$stem"
    bytes=$(mem_peak karac build "$src")
    mv "$stem" "target/${stem}_kara" 2>/dev/null || true
    cmem_put --lang kara --approach greedy --mode codegen --bytes "$bytes"
done
for src in "${STEM}.rs"; do
    out="target/$(basename "$src" .rs)"
    rm -f "$out"
    cmem_put --lang rust --approach greedy --mode native --bytes "$(mem_peak rustc -O "$src" -o "$out")"
done
for src in "${STEM}.c"; do
    out="target/$(basename "$src" .c)_c"
    rm -f "$out"
    cmem_put --lang c --approach greedy --mode native --bytes "$(mem_peak clang -O3 "$src" -o "$out")"
done

echo
bench_emit
