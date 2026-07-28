#!/usr/bin/env bash
# isa-sweep.sh — run every kata bench on an x86 host so the matched-ISA
# (c_v3 / rust_v3) lane is recorded corpus-wide.
#
# The ISA lane is a deliberate no-op on aarch64 (see bench-lib.sh
# `_isa_applies`), so the canonical M5 `results.json` files can never carry a v3
# row. This sweep is how those rows come to exist, and they land in the x86
# reference file — never the canonical one.
#
#   ./scripts/isa-sweep.sh                 # sweep all katas
#   ./scripts/isa-sweep.sh 137 260 1       # sweep only these kata ids
#
# Emits one machine-readable line per kata:
#   OK   <id> v3=<n>  langs=<...>      lane recorded
#   NOV3 <id> v3=0    langs=<...>      bench passed but emitted no v3 row
#   FAIL <id> <tail-of-log>            bench.sh exited non-zero
#
# NOV3 is called out separately from FAIL on purpose: _isa_reg DROPS a twin
# whose output disagrees with the kāra binary, and it does so with a warning on
# stderr and exit 0. A dropped lane therefore looks exactly like a passing bench
# unless the emitted rows are checked, which is what makes the silent case worth
# a distinct status rather than folding it into the pass count.
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$ROOT/scripts/bench-logs-isa"
mkdir -p "$LOG_DIR"

export BENCH_OUT="${BENCH_OUT:-results.container-x86.json}"

# Guard rather than silently produce a file full of non-v3 rows: off x86 every
# isa_* helper returns early and the sweep would "succeed" having recorded
# nothing it exists to record.
case "$(uname -m)" in
    x86_64 | amd64) ;;
    *)
        echo "isa-sweep: host is $(uname -m), not x86 — the ISA lane is a no-op here." >&2
        echo "isa-sweep: refusing to run; this sweep would record zero v3 rows." >&2
        exit 2
        ;;
esac

want=("$@")
match() {
    [ ${#want[@]} -eq 0 ] && return 0
    local id="$1" w
    for w in "${want[@]}"; do [ "${id%%-*}" = "$w" ] && return 0; done
    return 1
}

ok=0; nov3=0; fail=0
while IFS= read -r bench; do
    dir="$(dirname "$bench")"
    rel="${dir#"$ROOT"/}"
    id="$(echo "$rel" | sed 's|leetcode/||; s|/bench||; s|.*/||')"
    match "$id" || continue
    log="$LOG_DIR/${id}.log"

    if ( cd "$dir" && ./bench.sh ) >"$log" 2>&1; then
        read -r n langs < <(python3 - "$dir/$BENCH_OUT" <<'PY'
import json, sys
try:
    m = json.load(open(sys.argv[1]))["measurements"]
except Exception:
    print("0 <unreadable>"); raise SystemExit
langs = sorted({x.get("lang") for x in m})
print(sum(l.endswith("_v3") for l in langs), ",".join(langs))
PY
        )
        if [ "${n:-0}" -gt 0 ]; then
            echo "OK   $id v3=$n langs=$langs"; ok=$((ok + 1))
        else
            echo "NOV3 $id v3=0 langs=$langs"; nov3=$((nov3 + 1))
        fi
    else
        echo "FAIL $id $(tail -2 "$log" | tr '\n' ' ')"; fail=$((fail + 1))
    fi
# bespoke/ and backend/ carry katas too — utf8-codepoints was missed by the
# corpus-wide ISA wiring precisely because the earlier tooling only ever walked
# leetcode/. Searching both keeps that class of gap from recurring.
done < <(find "$ROOT/leetcode" "$ROOT/bespoke" "$ROOT/backend" \
    -path '*/bench/bench.sh' 2>/dev/null | sort)

echo "SWEEP-DONE ok=$ok nov3=$nov3 fail=$fail"
