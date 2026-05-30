# shellcheck shell=bash
# bench-lib.sh — shared structured-JSON emission for kata bench.sh scripts.
#
# Source this near the top of a kata's bench/bench.sh:
#
#     ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"   # repo root
#     . "$ROOT/scripts/bench-lib.sh"
#
# Then declare the kata and wrap each measurement so its structure
# (lang, approach, lane, mode) is recorded once, at the measurement:
#
#     bench_begin id=204 slug=count-primes group=201-300 \
#         title="Count Primes" workload="N=10^7 list primes" \
#         sink="(664579, 3203324994356)"
#
#     rt_begin --warmup 3 --runs 10
#     rt_cmd --lang kara --approach count --lane par --mode codegen \
#         --name 'kara count (codegen, #[par_unordered])' --cmd ./target/count_kara
#     rt_cmd --lang rust --approach count --lane seq --mode native \
#         --name 'rust count (single-threaded)' --cmd ./target/count
#     rt_end
#
# --cmd takes the command as a single string exactly as hyperfine wants it
# (hyperfine parses quotes itself even under --shell=none), so a compile
# command like  --cmd 'sh -c "karac build x.kara && mv x target/x"'  round-trips
# its inner quoting intact.
#
#     size_put --lang kara --approach count --lane par --mode codegen \
#         --path target/count_kara
#     mem_put  --lang kara --approach count --lane par --mode codegen \
#         --bytes "$(mem_peak ./target/count_kara)"
#     cmem_put --lang kara --approach count --mode codegen \
#         --bytes "$(mem_peak karac build count.kara)"
#
#     bench_emit          # writes bench/results.json
#
# Set BENCH_JSON=0 to disable all emission (the bench runs exactly as before,
# every bench_* call is a no-op). This keeps the library safe to source from a
# bench.sh that is run in an environment without python3.
#
# The lane/mode vocabulary the dashboard expects (see BENCH_JSON.md):
#   lane:  seq | par
#   mode:  codegen | interp | native        (native = rustc/clang/go output)
#   lang:  kara | rust | c | go | python

# Resolve the directory this library lives in so bench-emit.py is locatable
# regardless of the caller's cwd.
_BENCH_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

BENCH_JSON="${BENCH_JSON:-1}"

_bench_on() { [ "$BENCH_JSON" = "1" ]; }

# --- metadata + env capture -------------------------------------------------

bench_begin() {
    _bench_on || return 0
    BENCH_TMP="$(mktemp -d "${TMPDIR:-/tmp}/benchjson.XXXXXX")"
    : >"$BENCH_TMP/rt_map.tsv"
    : >"$BENCH_TMP/ce_map.tsv"
    : >"$BENCH_TMP/size.tsv"
    : >"$BENCH_TMP/mem.tsv"
    : >"$BENCH_TMP/cmem.tsv"

    local id="" slug="" group="" title="" workload="" sink=""
    local kv key val
    for kv in "$@"; do
        key="${kv%%=*}"
        val="${kv#*=}"
        case "$key" in
            id) id="$val" ;;
            slug) slug="$val" ;;
            group) group="$val" ;;
            title) title="$val" ;;
            workload) workload="$val" ;;
            sink) sink="$val" ;;
            *) echo "bench_begin: unknown key '$key'" >&2 ;;
        esac
    done

    local karac_v rustc_v clang_v go_v hf_v host p0 p1 cores os now
    karac_v="$(karac --version 2>/dev/null || echo unknown)"
    rustc_v="$(rustc --version 2>/dev/null || echo unknown)"
    clang_v="$(clang --version 2>/dev/null | head -1 || echo unknown)"
    go_v="$(go version 2>/dev/null || echo unknown)"
    hf_v="$(hyperfine --version 2>/dev/null || echo unknown)"
    host="$(sysctl -n machdep.cpu.brand_string 2>/dev/null || uname -m)"
    p0="$(sysctl -n hw.perflevel0.logicalcpu 2>/dev/null || echo '')"
    p1="$(sysctl -n hw.perflevel1.logicalcpu 2>/dev/null || echo '')"
    if [ -n "$p0" ] && [ -n "$p1" ]; then
        cores="${p0}P+${p1}E"
    else
        cores="$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo unknown)"
    fi
    os="$(uname -sr)"
    now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

    jq -n \
        --arg id "$id" --arg slug "$slug" --arg group "$group" \
        --arg title "$title" --arg workload "$workload" --arg sink "$sink" \
        --arg karac "$karac_v" --arg rustc "$rustc_v" --arg clang "$clang_v" \
        --arg go "$go_v" --arg hf "$hf_v" --arg host "$host" \
        --arg cores "$cores" --arg os "$os" --arg now "$now" \
        '{
            kata: {id: $id, slug: $slug, group: $group, title: $title,
                   workload: $workload, sink: $sink},
            env: {host: $host, cores: $cores, os: $os, karac: $karac,
                  rustc: $rustc, clang: $clang, go: $go, hyperfine: $hf,
                  measured_at: $now}
         }' >"$BENCH_TMP/meta.json"
}

# --- runtime lane -----------------------------------------------------------
# rt_begin sets warmup/runs; rt_cmd accumulates one comparator; rt_end runs the
# single hyperfine call (all comparators interleaved, per the BENCH.md protocol)
# and exports JSON for bench-emit to join.

rt_begin() {
    _bench_on || return 0
    _RT_WARMUP=3
    _RT_RUNS=10
    while [ $# -gt 0 ]; do
        case "$1" in
            --warmup) _RT_WARMUP="$2"; shift 2 ;;
            --runs) _RT_RUNS="$2"; shift 2 ;;
            *) echo "rt_begin: unknown arg '$1'" >&2; shift ;;
        esac
    done
    _RT_ARGS=()
}

# rt_cmd --lang L --approach A --lane LANE --mode MODE --name NAME --cmd 'CMD'
rt_cmd() {
    _bench_on || return 0
    local lang="" approach="" lane="" mode="" name="" cmd=""
    while [ $# -gt 0 ]; do
        case "$1" in
            --lang) lang="$2"; shift 2 ;;
            --approach) approach="$2"; shift 2 ;;
            --lane) lane="$2"; shift 2 ;;
            --mode) mode="$2"; shift 2 ;;
            --name) name="$2"; shift 2 ;;
            --cmd) cmd="$2"; shift 2 ;;
            *) echo "rt_cmd: unknown arg '$1'" >&2; shift ;;
        esac
    done
    printf '%s\t%s\t%s\t%s\t%s\n' "$name" "$lang" "$approach" "$lane" "$mode" \
        >>"$BENCH_TMP/rt_map.tsv"
    _RT_ARGS+=(--command-name "$name" "$cmd")
}

rt_end() {
    _bench_on || return 0
    hyperfine --warmup "$_RT_WARMUP" --runs "$_RT_RUNS" --shell=none \
        --export-json "$BENCH_TMP/runtime.json" \
        "${_RT_ARGS[@]}"
}

# --- compile-elapsed lane ---------------------------------------------------
# Same shape as runtime but each command carries a --prepare (the cold-compile
# artifact deletion). No lane (compile is lane-agnostic); mode distinguishes
# codegen vs native.

ce_begin() {
    _bench_on || return 0
    _CE_WARMUP=1
    _CE_RUNS=10
    while [ $# -gt 0 ]; do
        case "$1" in
            --warmup) _CE_WARMUP="$2"; shift 2 ;;
            --runs) _CE_RUNS="$2"; shift 2 ;;
            *) echo "ce_begin: unknown arg '$1'" >&2; shift ;;
        esac
    done
    _CE_ARGS=()
}

# ce_cmd --lang L --approach A --mode MODE --name NAME --prepare 'rm -f ...' --cmd 'CMD'
ce_cmd() {
    _bench_on || return 0
    local lang="" approach="" mode="" name="" prepare="" cmd=""
    while [ $# -gt 0 ]; do
        case "$1" in
            --lang) lang="$2"; shift 2 ;;
            --approach) approach="$2"; shift 2 ;;
            --mode) mode="$2"; shift 2 ;;
            --name) name="$2"; shift 2 ;;
            --prepare) prepare="$2"; shift 2 ;;
            --cmd) cmd="$2"; shift 2 ;;
            *) echo "ce_cmd: unknown arg '$1'" >&2; shift ;;
        esac
    done
    printf '%s\t%s\t%s\t%s\n' "$name" "$lang" "$approach" "$mode" \
        >>"$BENCH_TMP/ce_map.tsv"
    if [ -n "$prepare" ]; then
        _CE_ARGS+=(--prepare "$prepare")
    fi
    _CE_ARGS+=(--command-name "$name" "$cmd")
}

ce_end() {
    _bench_on || return 0
    hyperfine --warmup "$_CE_WARMUP" --runs "$_CE_RUNS" --shell=none \
        --export-json "$BENCH_TMP/compile.json" \
        "${_CE_ARGS[@]}"
}

# --- scalar metrics (binary size, peak RSS) ---------------------------------
# These both record the value and pretty-print a human line, so they replace
# the bespoke print loops in existing bench scripts.

_fmt_kib() { awk -v b="$1" 'BEGIN{printf "%.1f", b/1024}'; }
_fmt_mib() { awk -v b="$1" 'BEGIN{printf "%.1f", b/1048576}'; }

# size_put --lang L --approach A --lane LANE --mode MODE --path FILE
size_put() {
    local lang="" approach="" lane="" mode="" path=""
    while [ $# -gt 0 ]; do
        case "$1" in
            --lang) lang="$2"; shift 2 ;;
            --approach) approach="$2"; shift 2 ;;
            --lane) lane="$2"; shift 2 ;;
            --mode) mode="$2"; shift 2 ;;
            --path) path="$2"; shift 2 ;;
            *) echo "size_put: unknown arg '$1'" >&2; shift ;;
        esac
    done
    local bytes
    bytes=$(wc -c <"$path" | tr -d ' ')
    printf '  %-8s %-14s %-4s %-8s %10s bytes (%7s KiB)\n' \
        "$lang" "$approach" "$lane" "$mode" "$bytes" "$(_fmt_kib "$bytes")"
    _bench_on || return 0
    printf '%s\t%s\t%s\t%s\t%s\n' "$lang" "$approach" "$lane" "$mode" "$bytes" \
        >>"$BENCH_TMP/size.tsv"
}

# mem_put --lang L --approach A --lane LANE --mode MODE --bytes N
mem_put() {
    local lang="" approach="" lane="" mode="" bytes=""
    while [ $# -gt 0 ]; do
        case "$1" in
            --lang) lang="$2"; shift 2 ;;
            --approach) approach="$2"; shift 2 ;;
            --lane) lane="$2"; shift 2 ;;
            --mode) mode="$2"; shift 2 ;;
            --bytes) bytes="$2"; shift 2 ;;
            *) echo "mem_put: unknown arg '$1'" >&2; shift ;;
        esac
    done
    printf '  %-8s %-14s %-4s %-8s %10s bytes (%7s MiB)\n' \
        "$lang" "$approach" "$lane" "$mode" "$bytes" "$(_fmt_mib "$bytes")"
    _bench_on || return 0
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$lang" "$approach" "$lane" "$mode" "runtime_peak_rss" "$bytes" \
        >>"$BENCH_TMP/mem.tsv"
}

# cmem_put --lang L --approach A --mode MODE --bytes N
cmem_put() {
    local lang="" approach="" mode="" bytes=""
    while [ $# -gt 0 ]; do
        case "$1" in
            --lang) lang="$2"; shift 2 ;;
            --approach) approach="$2"; shift 2 ;;
            --mode) mode="$2"; shift 2 ;;
            --bytes) bytes="$2"; shift 2 ;;
            *) echo "cmem_put: unknown arg '$1'" >&2; shift ;;
        esac
    done
    printf '  %-8s %-14s %-8s %10s bytes (%7s MiB)\n' \
        "$lang" "$approach" "$mode" "$bytes" "$(_fmt_mib "$bytes")"
    _bench_on || return 0
    printf '%s\t%s\t%s\t%s\t%s\n' \
        "$lang" "$approach" "$mode" "compile_peak_rss" "$bytes" \
        >>"$BENCH_TMP/cmem.tsv"
}

# --- emit -------------------------------------------------------------------

bench_emit() {
    _bench_on || return 0
    local out="${BENCH_OUT:-results.json}"
    python3 "$_BENCH_LIB_DIR/bench-emit.py" "$BENCH_TMP" "$out"
    rm -rf "$BENCH_TMP"
}
