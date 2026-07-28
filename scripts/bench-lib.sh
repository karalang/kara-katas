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

# mem_peak CMD... -> peak RSS bytes. Portable across GNU time (Linux, -v,
# kbytes) and BSD time (macOS, -l, bytes). Python is the authoring parity
# oracle, not a timed lane, so it is skipped unless KARA_BENCH_INCLUDE_PY=1.
mem_peak() {
    if [ "${KARA_BENCH_INCLUDE_PY:-0}" != "1" ] && [ "${1:-}" = "python3" ]; then echo 0; return 0; fi
    if /usr/bin/time -v true >/dev/null 2>&1; then
        { /usr/bin/time -v "$@" >/dev/null; } 2>&1 \
            | awk '/Maximum resident set size/ {print $NF * 1024}'
    else
        { /usr/bin/time -l "$@" >/dev/null; } 2>&1 \
            | awk '/peak memory footprint/ {print $1}'
    fi
}

# --- metadata + env capture -------------------------------------------------

bench_begin() {
    _bench_on || return 0
    BENCH_TMP="$(mktemp -d "${TMPDIR:-/tmp}/benchjson.XXXXXX")"
    : >"$BENCH_TMP/rt_map.tsv"
    : >"$BENCH_TMP/ce_map.tsv"
    : >"$BENCH_TMP/size.tsv"
    : >"$BENCH_TMP/mem.tsv"
    : >"$BENCH_TMP/cmem.tsv"
    # Cumulative hyperfine exports — a kata may run several runtime or
    # compile-elapsed batches (e.g. short- vs long-workload splits); each
    # rt_end/ce_end merges its batch in rather than overwriting.
    echo '{"results":[]}' >"$BENCH_TMP/runtime.json"
    echo '{"results":[]}' >"$BENCH_TMP/compile.json"

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

    local karac_v karac_id rustc_v clang_v go_v hf_v host p0 p1 cores os now
    karac_v="$(karac --version 2>/dev/null || echo unknown)"
    # `karac --version` reads "karac 0.1.0" on every build ever made, so it
    # carries no provenance: a feed spanning three compiler generations looks
    # uniform. Fingerprint the actual binary instead (content hash + mtime), so
    # "which karac produced this row" is answerable from the JSON alone.
    karac_id="$(
        kb="$(command -v karac 2>/dev/null)" || kb=""
        if [ -n "$kb" ]; then
            h="$(shasum -a 256 "$kb" 2>/dev/null | cut -c1-12)"
            t="$(date -u -r "$kb" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null \
                 || stat -c %y "$kb" 2>/dev/null | cut -c1-19)"
            printf '%s %s' "${h:-unknown}" "${t:-unknown}"
        else
            printf 'unknown'
        fi
    )"
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
        --arg karac "$karac_v" --arg karac_id "$karac_id" \
        --arg rustc "$rustc_v" --arg clang "$clang_v" \
        --arg go "$go_v" --arg hf "$hf_v" --arg host "$host" \
        --arg cores "$cores" --arg os "$os" --arg now "$now" \
        '{
            kata: {id: $id, slug: $slug, group: $group, title: $title,
                   workload: $workload, sink: $sink},
            env: {host: $host, cores: $cores, os: $os, karac: $karac,
                  karac_build: $karac_id,
                  rustc: $rustc, clang: $clang, go: $go, hyperfine: $hf,
                  measured_at: $now}
         }' >"$BENCH_TMP/meta.json"
}

# --- equal-safety lane ------------------------------------------------------
# kāra checks integer overflow by default; `rustc -O` silently wraps. Timing
# them against each other is an unequal-safety comparison that flatters Rust by
# whatever the check costs on the workload — see BENCHMARKS.md. This lane builds
# the `-C overflow-checks=on` twin so the honest baseline is always in the feed.
#
# Unlike the matched-ISA helpers below, these are NOT arch-gated: the safety
# mismatch exists on every host.
#
#     ovf_build_rust "<stem>.rs"              # -> target/<stem>_ovf
#     ovf_rt_cmds    "<stem>" <approach> seq  # registers the row (inside rt_begin/rt_end)

ovf_build_rust() {
    local src="$1"
    local out="target/$(basename "$src" .rs)_ovf"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling $src (overflow-checks=on, equal-safety) ..." >&2
        rustc -O -C overflow-checks=on "$src" -o "$out"
    fi
}

# Register the equal-safety comparator, verifying its sink first.
#
# The twin is checked rather than trusted for the same reason the ISA twins are:
# an overflow-checked binary can legitimately TRAP where `rustc -O` wraps. That
# surfaces here as a non-zero exit and drops the lane loudly, instead of feeding
# a wrong or truncated number into the corpus. A trap here is a finding — it
# means the mirror relies on wrapping arithmetic that kāra would reject.
ovf_rt_cmds() {
    local stem="$1" approach="${2:-$1}" lane="${3:-seq}" ref="${4:-}"
    local bin="target/${stem}_ovf" k got
    [ -x "$bin" ] || return 0
    if [ -z "$ref" ]; then
        for k in "target/${stem}_kara_seq" "target/${stem}_kara"; do
            if [ -x "$k" ]; then ref="$("./$k" 2>/dev/null)"; break; fi
        done
    fi
    if [ -n "$ref" ]; then
        got="$("./$bin" 2>/dev/null)" || {
            echo "ovf: $stem overflow-checked twin exited non-zero (trap?) — lane dropped" >&2
            return 0
        }
        if [ "$got" != "$ref" ]; then
            echo "ovf: $stem twin sink mismatch (got=$got want=$ref) — lane dropped" >&2
            return 0
        fi
    fi
    rt_cmd --lang rust_ovf --approach "$approach" --lane "$lane" --mode native \
        --name "rust ${stem} (overflow-checks=on, equal-safety)" --cmd "./$bin"
}

# --- matched-ISA lane -------------------------------------------------------
# karac commits to a v3 deploy baseline (`cpu-baseline = "v3"`), while
# `clang -O3` and `rustc -O` default to the x86-64 v1 baseline (SSE2). On x86
# that makes the default cross-language comparison an AVX2-vs-SSE2 fight rather
# than a codegen comparison — measured on #260, kāra's apparent 1.44x lead over
# C is entirely the baseline and evaporates once C and Rust are rebuilt at v3.
#
# These helpers add the safety-matched *and* ISA-matched twin so the honest
# apples-to-apples number is always in the feed alongside the out-of-the-box
# one. Both are recorded; BENCHMARKS.md states which answers which question.
#
# On aarch64 every helper is a deliberate no-op. Verified 2026-07-27 on the M5:
# `clang -mcpu=apple-m1` (the macOS default) vs `-mcpu=generic` produces
# different binaries but statistically identical times, so there is no ARM
# baseline mismatch to correct.
#
#     isa_build_c    "${STEM}.c"     # -> target/<stem>_c_v3
#     isa_build_rust "${STEM}.rs"    # -> target/<stem>_v3   (also overflow-checked)
#     isa_sinks      "${STEM}"       # echoes the built twins for the sink check
#     isa_rt_cmds    "${STEM}" seq   # registers the rt_cmd rows (inside rt_begin/rt_end)

# True only where the v1-vs-v3 baseline gap actually exists. BENCH_ISA_FORCE=1
# overrides the arch gate — set it together with ISA_LEVEL (e.g. ISA_LEVEL=native)
# to exercise this path on a non-x86 host. That combination is for testing the
# harness only; the numbers it produces are not a corpus lane.
_isa_applies() {
    [ "${BENCH_ISA_FORCE:-0}" = "1" ] && return 0
    case "$(uname -m)" in
        x86_64 | amd64) return 0 ;;
        *) return 1 ;;
    esac
}

ISA_LEVEL="${ISA_LEVEL:-x86-64-v3}"

isa_build_c() {
    _isa_applies || return 0
    local src="$1"
    local out="target/$(basename "$src" .c)_c_v3"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling $src (-march=$ISA_LEVEL, matched-ISA) ..." >&2
        clang -O3 -march="$ISA_LEVEL" "$src" -o "$out"
    fi
}

# The fully-matched Rust twin: equal safety (overflow checks on, as kāra checks
# by default) AND equal ISA. This is the one honest apples-to-apples lane.
isa_build_rust() {
    _isa_applies || return 0
    local src="$1"
    local out="target/$(basename "$src" .rs)_v3"
    if [ ! -x "$out" ] || [ "$src" -nt "$out" ]; then
        echo "compiling $src (target-cpu=$ISA_LEVEL + overflow-checks, matched) ..." >&2
        rustc -O -C overflow-checks=on -C target-cpu="$ISA_LEVEL" "$src" -o "$out"
    fi
}

# Emit "name:cmd" pairs for whichever twins exist, for the caller's sink loop.
# Empty off x86 so the caller's loop simply has nothing extra to check.
isa_sinks() {
    _isa_applies || return 0
    local stem="$1"
    [ -x "target/${stem}_c_v3" ] && printf 'c_v3:./target/%s_c_v3\n' "$stem"
    [ -x "target/${stem}_v3" ] && printf 'rust_v3:./target/%s_v3\n' "$stem"
    return 0
}

# Register the matched-ISA comparators. Call between rt_begin and rt_end.
#
# Each twin is verified against the kāra binary's output before it is registered
# — not every kata's sink loop has a shape isa_sinks can extend, and a twin that
# is measured but never checked is exactly how a wrong number reaches the feed.
# (The overflow-checked twin can legitimately *trap* where `rustc -O` wraps; that
# shows up here as a mismatch and is reported rather than silently timed.)
_isa_reg() {
    local lang="$1" bin="$2" stem="$3" lane="$4" label="$5" ref="$6"
    [ -x "$bin" ] || return 0
    if [ -n "$ref" ]; then
        local got
        got="$("./$bin" 2>/dev/null)" || {
            echo "isa: $lang twin exited non-zero — lane dropped" >&2
            return 0
        }
        if [ "$got" != "$ref" ]; then
            echo "isa: $lang twin sink mismatch (got=$got want=$ref) — lane dropped" >&2
            return 0
        fi
    fi
    rt_cmd --lang "$lang" --approach "$stem" --lane "$lane" --mode native \
        --name "$label" --cmd "./$bin"
}

isa_rt_cmds() {
    _isa_applies || return 0
    local stem="$1" lane="${2:-seq}" ref=""
    [ -x "target/${stem}_kara" ] && ref="$(./target/${stem}_kara 2>/dev/null)"
    _isa_reg c_v3 "target/${stem}_c_v3" "$stem" "$lane" \
        "c    ${stem} (-march=$ISA_LEVEL, matched-ISA)" "$ref"
    _isa_reg rust_v3 "target/${stem}_v3" "$stem" "$lane" \
        "rust ${stem} (overflow-checks + target-cpu=$ISA_LEVEL, matched)" "$ref"
    return 0
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
    if [ "$lang" = "python" ] && [ "${KARA_BENCH_INCLUDE_PY:-0}" != "1" ]; then return 0; fi
    printf '%s\t%s\t%s\t%s\t%s\n' "$name" "$lang" "$approach" "$lane" "$mode" \
        >>"$BENCH_TMP/rt_map.tsv"
    _RT_ARGS+=(--command-name "$name" "$cmd")
}

rt_end() {
    _bench_on || return 0
    # No comparators queued (e.g. a Python-only batch skipped via the gate in
    # rt_cmd when KARA_BENCH_INCLUDE_PY!=1) — nothing to run or merge.
    [ "${#_RT_ARGS[@]}" -eq 0 ] && return 0
    hyperfine --warmup "$_RT_WARMUP" --runs "$_RT_RUNS" --shell=none \
        --export-json "$BENCH_TMP/_rt_batch.json" \
        "${_RT_ARGS[@]}"
    # Merge this batch's results into the cumulative export.
    jq -s '{results: (map(.results) | add)}' \
        "$BENCH_TMP/runtime.json" "$BENCH_TMP/_rt_batch.json" \
        >"$BENCH_TMP/_rt_merged.json"
    mv "$BENCH_TMP/_rt_merged.json" "$BENCH_TMP/runtime.json"
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
        --export-json "$BENCH_TMP/_ce_batch.json" \
        "${_CE_ARGS[@]}"
    jq -s '{results: (map(.results) | add)}' \
        "$BENCH_TMP/compile.json" "$BENCH_TMP/_ce_batch.json" \
        >"$BENCH_TMP/_ce_merged.json"
    mv "$BENCH_TMP/_ce_merged.json" "$BENCH_TMP/compile.json"
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
    if [ "$lang" = "python" ] && [ "${KARA_BENCH_INCLUDE_PY:-0}" != "1" ]; then return 0; fi
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
