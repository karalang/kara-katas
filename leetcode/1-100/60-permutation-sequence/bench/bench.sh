#!/usr/bin/env bash
# Wall-clock comparison across implementations of LeetCode #60 (Permutation
# Sequence). See ../README.md § Benchmarks for what these numbers mean.
#
# TWO solvers are benchmarked (the "run the bench for both" of this kata):
#
#   factorial — O(n²) factorial-number-system closed form (jumps to the k-th).
#   nextperm  — O(k·n) iterate next_permutation k-1 times (kata #31's step).
#
# Because the per-query cost differs by ~1000×, the two use DIFFERENT K so each
# lands in the same ~80 ms window (factorial K=500k, nextperm K=333). They are
# NOT directly wall-time comparable at equal K; the README normalizes to
# permutations-resolved-per-second (K·1000/mean_ms) over identical (n,k) inputs.
#
# Both are two-lane (BENCH.md § Implicit auto-par): the `total = total +
# <checksum>` reduction makes karac's default build emit a karac_par_reduce
# dispatch. Each solver builds a seq binary (KARAC_AUTO_PAR=0) and an auto-par
# binary (default); the seq lane is the apples-to-apples cross-language
# comparison, the auto-par lane is reported against rust+rayon.
#
# Workload: M=9 rotated (n,k) cases (rotating (n,k) defeats loop-invariant code
# motion). The sink folds a position-weighted checksum over every output digit,
# so no mirror can dead-code the digit picks. Per-solver sinks:
#   factorial → 69777768   nextperm → 46472
# bench.sh fails loudly on any mismatch within a solver's mirror group.
#
# Requires: hyperfine, rustc, clang, go, karac (+ jq, python3 for BENCH_JSON).

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

mkdir -p target

newer() { [ ! -x "$2" ] || [ "$1" -nt "$2" ] || [ "$(command -v karac)" -nt "$2" ]; }

build_kara() {      # src out   (auto-par default)
    local src="$1" out="$2" stem
    stem="$(basename "$src" .kara)"
    if newer "$src" "$out"; then
        echo "compiling $src (auto-par default) ..." >&2
        karac build "$src" >/dev/null
        mv "$stem" "$out"
    fi
}
build_kara_seq() {  # src out   (KARAC_AUTO_PAR=0)
    local src="$1" out="$2" stem
    stem="$(basename "$src" .kara)"
    if newer "$src" "$out"; then
        echo "compiling $src (KARAC_AUTO_PAR=0, seq lane) ..." >&2
        KARAC_AUTO_PAR=0 karac build "$src" >/dev/null
        mv "$stem" "$out"
    fi
}
build_rust() {      # src out
    local src="$1" out="$2"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling $src ..." >&2
        rustc -O "$src" -o "$out"
    fi
}
build_c() {         # src out
    local src="$1" out="$2"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling $src ..." >&2
        clang -O3 "$src" -o "$out"
    fi
}
build_go() {        # dir out
    local dir="$1" out="$2" src="$1/main.go"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling $dir ..." >&2
        ( cd "$dir" && go build -o "../$out" . )
    fi
}
build_rayon() {     # dir binname out
    local dir="$1" binname="$2" out="$3" src="$1/src/main.rs"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "building $dir (cargo) ..." >&2
        ( cd "$dir" && cargo build --release --quiet --offline )
        cp -f "$dir/target/release/$binname" "$out"
    fi
}

# ── build: factorial group ──────────────────────────────────────────────────
build_kara     permutation_sequence.kara         target/ps_fact_kara
build_kara_seq permutation_sequence.kara         target/ps_fact_kara_seq
build_rust     permutation_sequence.rs           target/ps_fact_rust
build_c        permutation_sequence.c            target/ps_fact_c
build_go       go-seq                            target/ps_fact_go_seq
build_rayon    rayon permutation_sequence_rayon  target/ps_fact_rayon

# ── build: next-perm group ──────────────────────────────────────────────────
build_kara     permutation_sequence_nextperm.kara            target/ps_next_kara
build_kara_seq permutation_sequence_nextperm.kara            target/ps_next_kara_seq
build_rust     permutation_sequence_nextperm.rs             target/ps_next_rust
build_c        permutation_sequence_nextperm.c              target/ps_next_c
build_go       go-seq-np                                    target/ps_next_go_seq
build_rayon    rayon-np permutation_sequence_nextperm_rayon target/ps_next_rayon

# ── verify sinks per solver group ───────────────────────────────────────────
verify_group() {
    local label="$1" expected="$2"; shift 2
    local mismatch="" bin out
    for bin in "$@"; do
        out=$("./target/$bin")
        [ "$out" = "$expected" ] || mismatch="$mismatch ${bin}=${out}"
    done
    if [ -n "$mismatch" ]; then
        echo "[$label] sink mismatch (expected=$expected):$mismatch" >&2
        exit 1
    fi
    echo "[$label] sink OK = $expected"
}
verify_group factorial 69777768 \
    ps_fact_kara ps_fact_kara_seq ps_fact_rust ps_fact_c ps_fact_go_seq ps_fact_rayon
verify_group nextperm 46472 \
    ps_next_kara ps_next_kara_seq ps_next_rust ps_next_c ps_next_go_seq ps_next_rayon
echo

bench_begin id=60 slug=permutation-sequence group=1-100 \
    title="Permutation Sequence" \
    workload="factorial K=500k / next-perm K=333, M=9 rotated (n,k) + digit checksum" \
    sink="factorial=69777768 nextperm=46472"

# ── runtime: factorial ──────────────────────────────────────────────────────
echo "=== runtime — factorial, seq lane (single-threaded) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach factorial --lane seq --mode codegen \
    --name "kara factorial (seq, KARAC_AUTO_PAR=0)" --cmd "./target/ps_fact_kara_seq"
rt_cmd --lang rust --approach factorial --lane seq --mode native \
    --name "rust factorial" --cmd "./target/ps_fact_rust"
rt_cmd --lang c --approach factorial --lane seq --mode native \
    --name "c    factorial" --cmd "./target/ps_fact_c"
rt_cmd --lang go --approach factorial --lane seq --mode native \
    --name "go   factorial" --cmd "./target/ps_fact_go_seq"
rt_end

echo
echo "=== runtime — factorial, auto-par regime (kara default vs rayon) ==="
rt_begin --warmup 10 --runs 50
rt_cmd --lang kara --approach factorial --lane par --mode codegen \
    --name "kara factorial (auto-par default)" --cmd "./target/ps_fact_kara"
rt_cmd --lang rust --approach factorial --lane par --mode native \
    --name "rust factorial (rayon par_iter)" --cmd "./target/ps_fact_rayon"
rt_end

# ── runtime: next-perm ──────────────────────────────────────────────────────
echo
echo "=== runtime — next-perm, seq lane (single-threaded) ==="
rt_begin --warmup 5 --runs 30
rt_cmd --lang kara --approach nextperm --lane seq --mode codegen \
    --name "kara nextperm (seq, KARAC_AUTO_PAR=0)" --cmd "./target/ps_next_kara_seq"
rt_cmd --lang rust --approach nextperm --lane seq --mode native \
    --name "rust nextperm" --cmd "./target/ps_next_rust"
rt_cmd --lang c --approach nextperm --lane seq --mode native \
    --name "c    nextperm" --cmd "./target/ps_next_c"
rt_cmd --lang go --approach nextperm --lane seq --mode native \
    --name "go   nextperm" --cmd "./target/ps_next_go_seq"
rt_end

echo
echo "=== runtime — next-perm, auto-par regime (kara default vs rayon) ==="
rt_begin --warmup 10 --runs 50
rt_cmd --lang kara --approach nextperm --lane par --mode codegen \
    --name "kara nextperm (auto-par default)" --cmd "./target/ps_next_kara"
rt_cmd --lang rust --approach nextperm --lane par --mode native \
    --name "rust nextperm (rayon par_iter)" --cmd "./target/ps_next_rayon"
rt_end

# ── runtime: python (scaled-down K) ─────────────────────────────────────────
echo
echo "=== runtime — python (factorial K=50k, nextperm K=9) ==="
rt_begin --warmup 2 --runs 10
rt_cmd --lang python --approach factorial --lane seq --mode interp \
    --name "py   factorial (K=50k)" --cmd "python3 permutation_sequence.py"
rt_cmd --lang python --approach nextperm --lane seq --mode interp \
    --name "py   nextperm (K=9)" --cmd "python3 permutation_sequence_nextperm.py"
rt_end

# ── compile elapsed (cold) ──────────────────────────────────────────────────
echo
echo "=== compile elapsed (cold) ==="
ce_begin --warmup 1 --runs 10
ce_cmd --lang kara --approach factorial --mode codegen \
    --prepare "rm -f target/ps_fact_kara permutation_sequence" \
    --name "karac build factorial" \
    --cmd "sh -c \"karac build permutation_sequence.kara >/dev/null && mv permutation_sequence target/ps_fact_kara\""
ce_cmd --lang kara --approach nextperm --mode codegen \
    --prepare "rm -f target/ps_next_kara permutation_sequence_nextperm" \
    --name "karac build nextperm" \
    --cmd "sh -c \"karac build permutation_sequence_nextperm.kara >/dev/null && mv permutation_sequence_nextperm target/ps_next_kara\""
ce_cmd --lang rust --approach factorial --mode native \
    --prepare "rm -f target/ps_fact_rust" \
    --name "rustc -O factorial" --cmd "rustc -O permutation_sequence.rs -o target/ps_fact_rust"
ce_cmd --lang c --approach factorial --mode native \
    --prepare "rm -f target/ps_fact_c" \
    --name "clang -O3 factorial" --cmd "clang -O3 permutation_sequence.c -o target/ps_fact_c"
ce_end

# ── binary size ─────────────────────────────────────────────────────────────
echo
echo "=== binary size ==="
size_put --lang kara --approach factorial --lane seq --mode codegen --path target/ps_fact_kara_seq
size_put --lang kara --approach factorial --lane par --mode codegen --path target/ps_fact_kara
size_put --lang rust --approach factorial --lane seq --mode native  --path target/ps_fact_rust
size_put --lang c    --approach factorial --lane seq --mode native  --path target/ps_fact_c
size_put --lang go   --approach factorial --lane seq --mode native  --path target/ps_fact_go_seq
size_put --lang rust --approach factorial --lane par --mode native  --path target/ps_fact_rayon
size_put --lang kara --approach nextperm  --lane seq --mode codegen --path target/ps_next_kara_seq
size_put --lang kara --approach nextperm  --lane par --mode codegen --path target/ps_next_kara

# ── runtime memory (peak) ───────────────────────────────────────────────────
echo
echo "=== runtime memory (peak) ==="
mem_put --lang kara --approach factorial --lane seq --mode codegen --bytes "$(mem_peak ./target/ps_fact_kara_seq)"
mem_put --lang kara --approach factorial --lane par --mode codegen --bytes "$(mem_peak ./target/ps_fact_kara)"
mem_put --lang rust --approach factorial --lane seq --mode native  --bytes "$(mem_peak ./target/ps_fact_rust)"
mem_put --lang c    --approach factorial --lane seq --mode native  --bytes "$(mem_peak ./target/ps_fact_c)"
mem_put --lang go   --approach factorial --lane seq --mode native  --bytes "$(mem_peak ./target/ps_fact_go_seq)"
mem_put --lang kara --approach nextperm  --lane seq --mode codegen --bytes "$(mem_peak ./target/ps_next_kara_seq)"
mem_put --lang kara --approach nextperm  --lane par --mode codegen --bytes "$(mem_peak ./target/ps_next_kara)"

# ── compile memory (cold) ───────────────────────────────────────────────────
echo
echo "=== compile memory (cold) ==="
rm -f target/ps_fact_kara permutation_sequence
cmem_put --lang kara --approach factorial --mode codegen --bytes "$(mem_peak karac build permutation_sequence.kara)"
mv permutation_sequence target/ps_fact_kara 2>/dev/null || true
rm -f target/ps_fact_rust
cmem_put --lang rust --approach factorial --mode native --bytes "$(mem_peak rustc -O permutation_sequence.rs -o target/ps_fact_rust)"
rm -f target/ps_fact_c
cmem_put --lang c --approach factorial --mode native --bytes "$(mem_peak clang -O3 permutation_sequence.c -o target/ps_fact_c)"

echo
bench_emit
