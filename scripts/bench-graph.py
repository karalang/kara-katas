#!/usr/bin/env python3
"""bench-graph.py — render the consolidated bench feed as committable SVG dot charts.

Reads bench-results.json (the single feed produced by consolidate-bench.sh) and
emits one SVG per metric into graphs/. Each chart is a *relative-performance
distribution* across every benchmarked program:

  - x-axis : one dot per program = (kata id x approach). NOT sorted, NOT a time
             series -- x-order carries no meaning, which is exactly why the dots
             are NOT connected by a line (a line would imply a trend that isn't
             there). This form scales: at hundreds/thousands of programs the dots
             overplot into a density band per language; dot radius/opacity and the
             x-labels auto-shrink with the program count.
  - y-axis : value / baseline-language value. Baseline lang draws as a flat
             reference at 1.0 (no dot cloud). Lower = faster/smaller/leaner.
  - dots   : one cloud per language (kara, rust, c, go), with a small per-language
             horizontal dodge so coincident dots (e.g. kāra == C at binary parity)
             don't occlude each other. Python and interpreted modes are excluded --
             this chart compares compiled output.

The default form is dots; --style line|bars|bars-overlap exist for comparison but
dots is the form that stays readable from 7 programs to 2000.

Pure stdlib: no matplotlib / cairo / network. Static SVG renders on GitHub.

Usage:
  python3 scripts/bench-graph.py [--baseline rust|c] [--feed bench-results.json]
"""
import argparse
import json
import math
import os
import sys

# Language presentation order + colors. kara first (highlighted), then the
# mainstream comparators. Python is intentionally absent.
LANGS = ["kara", "rust", "c", "go"]

# Dark theme. A soft charcoal-gray canvas (not near-black), with text dimmed
# below pure white so nothing glares. Reads as a clean dark card in light mode.
BG = "#282c34"      # soft charcoal-gray canvas
FG = "#c9d1d9"      # primary text (titles, legend) -- off-white, not glaring
MUTED = "#8b949e"   # secondary text (subtitles, labels, captions)
GRID = "#3b414b"    # faint gridlines / tick marks (just above the canvas)
DIM = "#a7b0bc"     # baseline line -- light enough to read clearly on the dark canvas
DIM2 = "#aeb6c0"    # baseline label (brightest gray, for emphasis)
RED = "#ff7b72"     # ceiling reference line

# Line colors, tuned to pop on the dark canvas.
COLOR = {
    "kara": "#ff922b",  # bright orange -- the subject
    "rust": "#8b949e",  # gray -- usually the baseline (flat), intentionally recessive
    "c": "#3fb950",     # green
    "go": "#bc8cff",    # violet
}
LABEL = {"kara": "Kāra", "rust": "Rust", "c": "C", "go": "Go"}

# Metric specs: (filename, title, unit-note, lane-or-None, extractor).
# extractor(measurement-or-compile-row) -> float|None
def _rt(m):
    rt = m.get("runtime")
    return rt.get("mean_ms") if rt else None

def _bin(m):
    return m.get("binary_bytes")

def _rss(m):
    return m.get("runtime_peak_rss_bytes")

def _cel(c):
    el = c.get("elapsed")
    return el.get("mean_ms") if el else None

def _crss(c):
    return c.get("compile_peak_rss_bytes")

# Per-metric spec. langs: which languages participate (compile metrics exclude
# Go -- `go build` bundles module resolution + multi-package compile + link,
# so its compile time/memory isn't comparable to single-file compilers; the
# finished artifact still is, so Go stays in runtime/binary/rss). yscale: how
# the relative axis is drawn ("linear" | "log") -- size spans orders of
# magnitude, the rest are well-behaved linear.
# (fname, title, unitnote, section, lane, langs, yscale, extractor)
ALL4 = ["kara", "rust", "c", "go"]
PAR4 = ["kara", "rust", "c", "go"]   # par lane = Kāra auto-par vs Rust rayon vs Go goroutines vs C pthreads (metal floor)
COMPILE3 = ["kara", "rust", "c"]  # Go excluded: `go build` bundles module resolution, not a single-file compile
METRICS = [
    ("runtime-seq", "Runtime — sequential lane", "lower = faster", "measurements", "seq", ALL4, "linear", _rt),
    ("runtime-par", "Runtime — auto-parallel lane", "lower = faster", "measurements", "par", PAR4, "linear", _rt),
    ("binary-seq", "Binary size — sequential lane", "lower = smaller", "measurements", "seq", ALL4, "log", _bin),
    ("binary-par", "Binary size — auto-parallel lane", "lower = smaller", "measurements", "par", PAR4, "log", _bin),
    ("rss-seq", "Runtime peak memory — sequential lane", "lower = leaner", "measurements", "seq", ALL4, "linear", _rss),
    ("rss-par", "Runtime peak memory — auto-parallel lane", "lower = leaner", "measurements", "par", PAR4, "linear", _rss),
    ("compile-elapsed", "Compile time (cold)", "lower = faster", "compile", None, COMPILE3, "linear", _cel),
    ("compile-rss", "Compile peak memory (cold)", "lower = leaner", "compile", None, COMPILE3, "linear", _crss),
]


def pick_row(rows, lang):
    """Among a lang's rows for one program, choose the compiled one.

    Excludes interp mode (this chart is about compiled output). kara -> codegen,
    others -> native. Returns the first non-interp row or None.
    """
    cands = [r for r in rows if r.get("lang") == lang and r.get("mode") != "interp"]
    return cands[0] if cands else None


def collect(feed, section, lane, langs, extract):
    """Return list of programs: {key, label, vals:{lang:value}} that have a value
    for every language in `langs` (so the relative lines have no gaps)."""
    progs = []
    for kata in feed["katas"]:
        kid = kata["kata"]["id"]
        rows = kata.get(section, [])
        if section == "measurements" and lane is not None:
            rows = [r for r in rows if r.get("lane") == lane]
        # group by approach
        approaches = []
        for r in rows:
            a = r.get("approach")
            if a not in approaches:
                approaches.append(a)
        for ap in approaches:
            arows = [r for r in rows if r.get("approach") == ap]
            vals = {}
            for lang in langs:
                row = pick_row(arows, lang)
                v = extract(row) if row else None
                if v is not None:
                    vals[lang] = float(v)
            # require every participating language, else the profile has gaps
            if all(lang in vals for lang in langs):
                short_ap = ap if len(ap) <= 14 else ap[:13] + "…"
                progs.append({"key": f"{kid}:{ap}", "label": f"#{kid}\n{short_ap}", "vals": vals})
    return progs


def nice_ceil(v):
    """Round a y-max up to a friendly tick (0.5 steps below 5, else 1.0)."""
    if v <= 2.0:
        return (int(v / 0.5) + 1) * 0.5
    if v <= 5.0:
        return float(int(v) + 1)
    step = 1.0
    while v / step > 8:
        step *= 2
    return (int(v / step) + 1) * step


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def log_ticks(lo, hi):
    """Nice multiplicative ticks (…0.1,0.2,0.5,1,2,5,10…) within [lo,hi]."""
    base = [1.0, 2.0, 5.0]
    ticks = []
    e = -3
    while e <= 4:
        for b in base:
            v = b * (10 ** e)
            if lo <= v <= hi:
                ticks.append(v)
        e += 1
    return ticks


def render(progs, baseline, title, unitnote, langs, yscale):
    """Render one SVG string. progs already sorted; baseline lang = 1.0.

    yscale: "linear" (axis 0..nice_ceil) | "log" (decade ticks) | "clamp"
    (linear axis capped, over-cap points drawn as an arrow + value label)."""
    W, H = 980, 560
    ml, mr, mt, mb = 70, 168, 78, 104
    pw, ph = W - ml - mr, H - mt - mb
    n = len(progs)

    series = {lang: [] for lang in langs}
    ymax_data, ymin_data = 0.0, 1e18
    for p in progs:
        base = p["vals"][baseline]
        for lang in langs:
            r = p["vals"][lang] / base
            series[lang].append(r)
            ymax_data = max(ymax_data, r)
            ymin_data = min(ymin_data, r)

    def X(i):
        if n == 1:
            return ml + pw / 2
        pad = pw * 0.06
        return ml + pad + i * (pw - 2 * pad) / (n - 1)

    # --- axis setup per scale -------------------------------------------
    overflow = []  # (x, lang, value) for clamp points above cap
    if yscale == "log":
        lo = 10 ** math.floor(math.log10(ymin_data))
        hi = 10 ** math.ceil(math.log10(ymax_data))
        llo, lhi = math.log10(lo), math.log10(hi)

        def Y(v):
            return mt + ph - (math.log10(v) - llo) / (lhi - llo) * ph
        gridvals = log_ticks(lo, hi)
        fmt = lambda t: (f"{t:g}×")
        cap = None
    elif yscale == "clamp":
        cap = 2.0
        ystep = 0.5

        def Y(v):
            vv = min(v, cap)
            return mt + ph - (vv / cap) * ph
        gridvals = [i * ystep for i in range(int(cap / ystep) + 1)]
        fmt = lambda t: f"{t:.1f}×"
    else:  # linear
        ymax = nice_ceil(ymax_data)
        ystep = 0.5 if ymax <= 2.0 else (1.0 if ymax <= 5.0 else ymax / 5)

        def Y(v):
            return mt + ph - (v / ymax) * ph
        gridvals = []
        t = 0.0
        while t <= ymax + 1e-9:
            gridvals.append(t)
            t += ystep
        fmt = lambda t: f"{t:.1f}×"
        cap = None

    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif">')
    s.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    if yscale == "log":
        scale_note = " · log scale"
    elif yscale == "clamp":
        scale_note = f" · axis capped at {cap:.0f}×"
    else:
        scale_note = ""
    s.append(f'<text x="{ml}" y="34" font-size="21" font-weight="700" fill="{FG}">{esc(title)}</text>')
    s.append(f'<text x="{ml}" y="56" font-size="13" fill="{MUTED}">'
             f'relative to {LABEL[baseline]} = 1.0 · {esc(unitnote)} · {n} programs{scale_note}</text>')

    # y gridlines + labels
    for t in gridvals:
        y = Y(t)
        is_base = abs(t - 1.0) < 1e-9
        dash = ' stroke-dasharray="5 4"' if is_base else ""
        s.append(f'<line x1="{ml}" y1="{y:.1f}" x2="{ml+pw}" y2="{y:.1f}" '
                 f'stroke="{DIM if is_base else GRID}" stroke-width="{2 if is_base else 1}"{dash}/>')
        wt = ' font-weight="700"' if is_base else ""
        s.append(f'<text x="{ml-10}" y="{y+4:.1f}" font-size="12" text-anchor="end" '
                 f'fill="{DIM2 if is_base else MUTED}"{wt}>{fmt(t)}</text>')
    s.append(f'<text x="{ml+pw}" y="{Y(1.0)-6:.1f}" font-size="11" text-anchor="end" '
             f'fill="{DIM2}">{LABEL[baseline]} baseline</text>')

    # x ticks (program labels), rotated
    for i, p in enumerate(progs):
        x = X(i)
        s.append(f'<line x1="{x:.1f}" y1="{mt+ph}" x2="{x:.1f}" y2="{mt+ph+5}" stroke="{GRID}"/>')
        ty = mt + ph + 18
        s.append(f'<g transform="translate({x:.1f},{ty}) rotate(35)">')
        for li, ln in enumerate(p["label"].split("\n")):
            s.append(f'<text x="0" y="{li*12}" font-size="10.5" fill="{MUTED}">{esc(ln)}</text>')
        s.append('</g>')

    # lines: kara drawn last (on top)
    draw_order = [l for l in langs if l != "kara"] + (["kara"] if "kara" in langs else [])
    for lang in draw_order:
        is_kara = lang == "kara"
        pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(series[lang]))
        s.append(f'<polyline points="{pts}" fill="none" stroke="{COLOR[lang]}" '
                 f'stroke-width="{3 if is_kara else 2}" stroke-linejoin="round" '
                 f'opacity="{1.0 if is_kara else 0.85}"/>')
        for i, v in enumerate(series[lang]):
            s.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="{4 if is_kara else 3}" fill="{COLOR[lang]}"/>')
            if yscale == "clamp" and v > cap:
                overflow.append((X(i), lang, v))

    # clamp overflow markers (arrow + value, drawn above the cap line)
    for x, lang, v in overflow:
        yt = Y(cap)
        s.append(f'<text x="{x:.1f}" y="{yt-6:.1f}" font-size="10.5" text-anchor="middle" '
                 f'fill="{COLOR[lang]}" font-weight="700">{v:.1f}× ↑</text>')

    # legend
    lx, ly = ml + pw + 24, mt + 6
    for j, lang in enumerate(langs):
        yy = ly + j * 24
        s.append(f'<line x1="{lx}" y1="{yy}" x2="{lx+22}" y2="{yy}" stroke="{COLOR[lang]}" '
                 f'stroke-width="{3 if lang=="kara" else 2}"/>')
        s.append(f'<circle cx="{lx+11}" cy="{yy}" r="3.5" fill="{COLOR[lang]}"/>')
        s.append(f'<text x="{lx+30}" y="{yy+4}" font-size="13" '
                 f'fill="{FG}" font-weight="{700 if lang=="kara" else 400}">{LABEL[lang]}</text>')

    cap_txt = ("Each point is one benchmarked program (kata × approach); left-to-right order is not "
               "meaningful — this is not a time series. Raw absolute numbers: bench-results.json")
    s.append(f'<text x="{ml}" y="{H-22}" font-size="11.5" fill="{MUTED}">{esc(cap_txt)}</text>')
    s.append('</svg>')
    return "\n".join(s)


def render_dots(progs, baseline, title, unitnote, langs, yscale):
    """Dot-chart (scatter/strip). Each program = one dot per language at its
    ratio-to-baseline; NO connecting line (x-order is meaningless, so a line would
    imply a trend that doesn't exist). Designed to scale: at hundreds/thousands of
    programs the dots overplot into a density band per language. baseline draws as
    the flat 1.0 reference. kāra is larger + on top."""
    W, H = 980, 560
    ml, mr, mt, mb = 70, 168, 78, 104
    pw, ph = W - ml - mr, H - mt - mb
    n = len(progs)

    series = {lang: [] for lang in langs}
    ymax_data, ymin_data = 0.0, 1e18
    for p in progs:
        base = p["vals"][baseline]
        for lang in langs:
            r = p["vals"][lang] / base
            series[lang].append(r)
            ymax_data = max(ymax_data, r)
            ymin_data = min(ymin_data, r)

    def X(i):
        if n == 1:
            return ml + pw / 2
        pad = pw * 0.04
        return ml + pad + i * (pw - 2 * pad) / (n - 1)

    if yscale == "log":
        lo = 10 ** math.floor(math.log10(ymin_data))
        hi = 10 ** math.ceil(math.log10(ymax_data))
        llo, lhi = math.log10(lo), math.log10(hi)
        def Y(v):
            return mt + ph - (math.log10(v) - llo) / (lhi - llo) * ph
        gridvals = log_ticks(lo, hi)
        fmt = lambda t: f"{t:g}×"
    else:
        ymax = nice_ceil(ymax_data)
        ystep = 0.5 if ymax <= 2.0 else (1.0 if ymax <= 5.0 else ymax / 5)
        def Y(v):
            return mt + ph - (v / ymax) * ph
        gridvals = []
        t = 0.0
        while t <= ymax + 1e-9:
            gridvals.append(t)
            t += ystep
        fmt = lambda t: f"{t:.1f}×"

    # Always pin 1.0 as a gridline. On a tall linear axis the regular step
    # (ymax/5, e.g. 1.6) can skip 1.0 entirely, which silently drops the
    # Rust=1.0 baseline line. Inject it so the reference is always drawn.
    if not any(abs(t - 1.0) < 1e-9 for t in gridvals):
        gridvals = sorted(gridvals + [1.0])

    # dot radius + alpha shrink as the suite grows so dense clouds stay readable
    if n <= 30:
        r_other, r_kara, op = 4.0, 5.0, 0.95
    elif n <= 200:
        r_other, r_kara, op = 2.6, 3.2, 0.7
    else:
        r_other, r_kara, op = 1.7, 2.1, 0.5

    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif">')
    s.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    scale_note = " · log scale" if yscale == "log" else ""
    s.append(f'<text x="{ml}" y="34" font-size="21" font-weight="700" fill="{FG}">{esc(title)}</text>')
    s.append(f'<text x="{ml}" y="56" font-size="13" fill="{MUTED}">'
             f'relative to {LABEL[baseline]} = 1.0 · {esc(unitnote)} · {n} programs{scale_note}</text>')

    for t in gridvals:
        y = Y(t)
        is_base = abs(t - 1.0) < 1e-9
        dash = ' stroke-dasharray="5 4"' if is_base else ""
        s.append(f'<line x1="{ml}" y1="{y:.1f}" x2="{ml+pw}" y2="{y:.1f}" '
                 f'stroke="{DIM if is_base else GRID}" stroke-width="{2 if is_base else 1}"{dash}/>')
        wt = ' font-weight="700"' if is_base else ""
        s.append(f'<text x="{ml-10}" y="{y+4:.1f}" font-size="12" text-anchor="end" '
                 f'fill="{DIM2 if is_base else MUTED}"{wt}>{fmt(t)}</text>')
    s.append(f'<text x="{ml+pw}" y="{Y(1.0)-6:.1f}" font-size="11" text-anchor="end" '
             f'fill="{DIM2}">{LABEL[baseline]} baseline</text>')

    # x ticks only when sparse enough to label; otherwise just an axis line
    if n <= 30:
        for i, p in enumerate(progs):
            x = X(i)
            s.append(f'<line x1="{x:.1f}" y1="{mt+ph}" x2="{x:.1f}" y2="{mt+ph+5}" stroke="{GRID}"/>')
            ty = mt + ph + 18
            s.append(f'<g transform="translate({x:.1f},{ty}) rotate(35)">')
            for li, ln in enumerate(p["label"].split("\n")):
                s.append(f'<text x="0" y="{li*12}" font-size="10.5" fill="{MUTED}">{esc(ln)}</text>')
            s.append('</g>')
    else:
        s.append(f'<line x1="{ml}" y1="{mt+ph}" x2="{ml+pw}" y2="{mt+ph}" stroke="{GRID}"/>')
        s.append(f'<text x="{ml+pw/2:.1f}" y="{mt+ph+22}" font-size="11" text-anchor="middle" '
                 f'fill="{MUTED}">{n} programs (kata × approach) — x-order carries no meaning</text>')

    # per-language horizontal dodge so coincident dots (e.g. kāra == C at binary
    # parity) sit shoulder-to-shoulder instead of one occluding the other. Scaled
    # to inter-program spacing so it shrinks gracefully as the suite grows.
    plotlangs = [l for l in langs if l != baseline]
    spacing = (pw / max(n - 1, 1))
    ddx = min(spacing * 0.5, (r_kara * 2 + 1.5)) / max(len(plotlangs), 1)
    dodge = {l: (j - (len(plotlangs) - 1) / 2) * ddx for j, l in enumerate(plotlangs)}

    # dots: kara drawn last (on top)
    draw_order = [l for l in plotlangs if l != "kara"] + (["kara"] if "kara" in plotlangs else [])
    for lang in draw_order:
        is_kara = lang == "kara"
        r = r_kara if is_kara else r_other
        o = min(1.0, op + 0.15) if is_kara else op
        dx = dodge[lang]
        for i, v in enumerate(series[lang]):
            s.append(f'<circle cx="{X(i)+dx:.1f}" cy="{Y(v):.1f}" r="{r}" '
                     f'fill="{COLOR[lang]}" opacity="{o}"/>')

    # legend
    lx, ly = ml + pw + 24, mt + 6
    for j, lang in enumerate(langs):
        yy = ly + j * 24
        if lang == baseline:
            s.append(f'<line x1="{lx}" y1="{yy}" x2="{lx+22}" y2="{yy}" stroke="{DIM}" '
                     f'stroke-width="2" stroke-dasharray="5 4"/>')
            disp = f"{LABEL[lang]} = 1.0×"
        else:
            s.append(f'<circle cx="{lx+11}" cy="{yy}" r="{5 if lang=="kara" else 4}" fill="{COLOR[lang]}"/>')
            disp = LABEL[lang]
        s.append(f'<text x="{lx+30}" y="{yy+4}" font-size="13" '
                 f'fill="{FG}" font-weight="{700 if lang=="kara" else 400}">{esc(disp)}</text>')

    cap_txt = ("Each dot is one benchmarked program (kata × approach); there is no connecting line "
               "because left-to-right order is not meaningful. Raw numbers: bench-results.json")
    s.append(f'<text x="{ml}" y="{H-22}" font-size="11.5" fill="{MUTED}">{esc(cap_txt)}</text>')
    s.append('</svg>')
    return "\n".join(s)


def render_bars(progs, baseline, title, unitnote, langs, yscale, overlap):
    """Bar-chart prototype. Each program is a group of bars (one per non-baseline
    language; the baseline draws as the flat 1.0 reference line). overlap=True
    stacks the bars at a shared x-origin with alpha (tallest-behind); overlap=False
    draws them side-by-side within the group slot. For comparison against the
    line form -- see render()."""
    W, H = 980, 560
    ml, mr, mt, mb = 70, 168, 78, 104
    pw, ph = W - ml - mr, H - mt - mb
    n = len(progs)

    series = {lang: [] for lang in langs}
    ymax_data, ymin_data = 0.0, 1e18
    for p in progs:
        base = p["vals"][baseline]
        for lang in langs:
            r = p["vals"][lang] / base
            series[lang].append(r)
            ymax_data = max(ymax_data, r)
            ymin_data = min(ymin_data, r)

    barlangs = [l for l in langs if l != baseline]  # baseline is the reference line

    if yscale == "log":
        lo = 10 ** math.floor(math.log10(ymin_data))
        hi = 10 ** math.ceil(math.log10(ymax_data))
        llo, lhi = math.log10(lo), math.log10(hi)
        def Y(v):
            return mt + ph - (math.log10(max(v, lo)) - llo) / (lhi - llo) * ph
        y0 = mt + ph  # bars rise from axis floor
        gridvals = log_ticks(lo, hi)
        fmt = lambda t: f"{t:g}×"
    else:
        ymax = nice_ceil(ymax_data)
        ystep = 0.5 if ymax <= 2.0 else (1.0 if ymax <= 5.0 else ymax / 5)
        def Y(v):
            return mt + ph - (v / ymax) * ph
        y0 = mt + ph
        gridvals = []
        t = 0.0
        while t <= ymax + 1e-9:
            gridvals.append(t)
            t += ystep
        fmt = lambda t: f"{t:.1f}×"

    # group geometry
    slot = pw / n
    if overlap:
        bw = slot * 0.34
    else:
        bw = (slot * 0.62) / len(barlangs)

    def gx(i):
        return ml + slot * (i + 0.5)  # group center

    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif">')
    s.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    scale_note = " · log scale" if yscale == "log" else ""
    style_note = "overlapped bars" if overlap else "grouped bars"
    s.append(f'<text x="{ml}" y="34" font-size="21" font-weight="700" fill="{FG}">{esc(title)}</text>')
    s.append(f'<text x="{ml}" y="56" font-size="13" fill="{MUTED}">'
             f'relative to {LABEL[baseline]} = 1.0 · {esc(unitnote)} · {n} programs · {style_note}{scale_note}</text>')

    # y gridlines
    for t in gridvals:
        y = Y(t)
        is_base = abs(t - 1.0) < 1e-9
        dash = ' stroke-dasharray="5 4"' if is_base else ""
        s.append(f'<line x1="{ml}" y1="{y:.1f}" x2="{ml+pw}" y2="{y:.1f}" '
                 f'stroke="{DIM if is_base else GRID}" stroke-width="{2 if is_base else 1}"{dash}/>')
        wt = ' font-weight="700"' if is_base else ""
        s.append(f'<text x="{ml-10}" y="{y+4:.1f}" font-size="12" text-anchor="end" '
                 f'fill="{DIM2 if is_base else MUTED}"{wt}>{fmt(t)}</text>')
    s.append(f'<text x="{ml+pw}" y="{Y(1.0)-6:.1f}" font-size="11" text-anchor="end" '
             f'fill="{DIM2}">{LABEL[baseline]} baseline</text>')

    # x ticks
    for i, p in enumerate(progs):
        x = gx(i)
        s.append(f'<line x1="{x:.1f}" y1="{mt+ph}" x2="{x:.1f}" y2="{mt+ph+5}" stroke="{GRID}"/>')
        ty = mt + ph + 18
        s.append(f'<g transform="translate({x:.1f},{ty}) rotate(35)">')
        for li, ln in enumerate(p["label"].split("\n")):
            s.append(f'<text x="0" y="{li*12}" font-size="10.5" fill="{MUTED}">{esc(ln)}</text>')
        s.append('</g>')

    # bars
    for i in range(n):
        cx = gx(i)
        if overlap:
            # draw tallest first so shorter bars stay visible in front; alpha blend
            order = sorted(barlangs, key=lambda l: series[l][i], reverse=True)
            for lang in order:
                v = series[lang][i]
                y = Y(v)
                s.append(f'<rect x="{cx-bw/2:.1f}" y="{y:.1f}" width="{bw:.1f}" '
                         f'height="{y0-y:.1f}" fill="{COLOR[lang]}" opacity="0.55"/>')
        else:
            total = bw * len(barlangs)
            for j, lang in enumerate(barlangs):
                v = series[lang][i]
                y = Y(v)
                x = cx - total / 2 + j * bw
                s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw-1:.1f}" '
                         f'height="{y0-y:.1f}" fill="{COLOR[lang]}" opacity="0.92"/>')

    # legend (baseline shown as a line, others as swatches)
    lx, ly = ml + pw + 24, mt + 6
    for j, lang in enumerate(langs):
        yy = ly + j * 24
        if lang == baseline:
            s.append(f'<line x1="{lx}" y1="{yy}" x2="{lx+22}" y2="{yy}" stroke="{DIM}" '
                     f'stroke-width="1.6" stroke-dasharray="5 4"/>')
        else:
            s.append(f'<rect x="{lx}" y="{yy-7}" width="22" height="14" fill="{COLOR[lang]}" '
                     f'opacity="{0.55 if overlap else 0.92}"/>')
        s.append(f'<text x="{lx+30}" y="{yy+4}" font-size="13" '
                 f'fill="{FG}" font-weight="{700 if lang=="kara" else 400}">{LABEL[lang]}</text>')

    cap_txt = ("Each group is one benchmarked program (kata × approach); left-to-right order is not "
               "meaningful — this is not a time series. Raw absolute numbers: bench-results.json")
    s.append(f'<text x="{ml}" y="{H-22}" font-size="11.5" fill="{MUTED}">{esc(cap_txt)}</text>')
    s.append('</svg>')
    return "\n".join(s)


# Hardware ceiling for the auto-par speedup chart's reference line.
CORES_CEILING = 18      # M5 Pro: 6 performance + 12 efficiency cores
CORES_NOTE = "M5 Pro · 6P + 12E"


def collect_speedup(feed):
    """Per (kata, approach) where kāra has BOTH a seq and a par codegen runtime,
    return {label, seq, par, speedup}. speedup = seq_ms / par_ms (higher=better).
    This is an intra-Kāra measurement (auto-par regime vs sequential regime of the
    same source) -- NOT a cross-language comparison."""
    out = []
    for kata in feed["katas"]:
        kid = kata["kata"]["id"]
        krows = [m for m in kata.get("measurements", [])
                 if m.get("lang") == "kara" and m.get("mode") == "codegen"]
        approaches = []
        for r in krows:
            if r.get("approach") not in approaches:
                approaches.append(r.get("approach"))
        for ap in approaches:
            def rt(lane):
                for r in krows:
                    if r.get("approach") == ap and r.get("lane") == lane:
                        x = r.get("runtime")
                        if x and x.get("mean_ms"):
                            return x["mean_ms"]
                return None
            seq, par = rt("seq"), rt("par")
            if seq and par and par > 0:
                short = ap if len(ap) <= 16 else ap[:15] + "…"
                out.append({"label": f"#{kid}\n{short}", "seq": seq, "par": par, "speedup": seq / par})
    return out


def render_speedup(progs):
    """Single-series chart: kāra auto-par speedup per program, with a 1× floor
    and the core-count hardware ceiling as reference lines. Higher = better."""
    W, H = 980, 560
    ml, mr, mt, mb = 70, 168, 88, 104
    pw, ph = W - ml - mr, H - mt - mb
    n = len(progs)
    ymax = nice_ceil(max(CORES_CEILING, max(p["speedup"] for p in progs)) * 1.08)
    if ymax < CORES_CEILING + 2:
        ymax = CORES_CEILING + 2

    def X(i):
        if n == 1:
            return ml + pw / 2
        pad = pw * 0.06
        return ml + pad + i * (pw - 2 * pad) / (n - 1)

    def Y(v):
        return mt + ph - (v / ymax) * ph

    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif">')
    s.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    s.append(f'<text x="{ml}" y="34" font-size="21" font-weight="700" fill="{FG}">'
             f'Kāra auto-parallel speedup</text>')
    s.append(f'<text x="{ml}" y="56" font-size="13" fill="{MUTED}">'
             f'kāra-par ÷ kāra-seq · same source, zero parallel code · higher = faster · {n} programs</text>')

    # y gridlines
    step = 5.0 if ymax > 12 else 2.0
    t = 0.0
    while t <= ymax + 1e-9:
        y = Y(t)
        s.append(f'<line x1="{ml}" y1="{y:.1f}" x2="{ml+pw}" y2="{y:.1f}" stroke="{GRID}"/>')
        s.append(f'<text x="{ml-10}" y="{y+4:.1f}" font-size="12" text-anchor="end" fill="{MUTED}">{t:.0f}×</text>')
        t += step

    # reference lines: 1x floor and hardware ceiling
    for val, txt, col in [(1.0, "1× — no speedup", DIM),
                          (CORES_CEILING, f"{CORES_CEILING} cores — hardware ceiling ({CORES_NOTE})", RED)]:
        y = Y(val)
        s.append(f'<line x1="{ml}" y1="{y:.1f}" x2="{ml+pw}" y2="{y:.1f}" stroke="{col}" '
                 f'stroke-width="1.4" stroke-dasharray="5 4"/>')
        s.append(f'<text x="{ml+pw}" y="{y-6:.1f}" font-size="11" text-anchor="end" fill="{MUTED}">{esc(txt)}</text>')

    # x ticks (labelled only while sparse; otherwise a single axis note)
    if n <= 30:
        for i, p in enumerate(progs):
            x = X(i)
            s.append(f'<line x1="{x:.1f}" y1="{mt+ph}" x2="{x:.1f}" y2="{mt+ph+5}" stroke="{GRID}"/>')
            ty = mt + ph + 18
            s.append(f'<g transform="translate({x:.1f},{ty}) rotate(35)">')
            for li, ln in enumerate(p["label"].split("\n")):
                s.append(f'<text x="0" y="{li*12}" font-size="10.5" fill="{MUTED}">{esc(ln)}</text>')
            s.append('</g>')
    else:
        s.append(f'<line x1="{ml}" y1="{mt+ph}" x2="{ml+pw}" y2="{mt+ph}" stroke="{GRID}"/>')
        s.append(f'<text x="{ml+pw/2:.1f}" y="{mt+ph+22}" font-size="11" text-anchor="middle" '
                 f'fill="{MUTED}">{n} parallel programs — x-order carries no meaning</text>')

    # the kāra speedup series -- dots, no connecting line (x-order is meaningless).
    # Per-point value labels only while sparse enough to not collide.
    show_labels = n <= 30
    r = 4.5 if n <= 30 else (3.0 if n <= 200 else 2.0)
    for i, p in enumerate(progs):
        x, y = X(i), Y(p["speedup"])
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{COLOR["kara"]}" '
                 f'opacity="{0.95 if n <= 30 else (0.7 if n <= 200 else 0.5)}"/>')
        if show_labels:
            s.append(f'<text x="{x:.1f}" y="{y-10:.1f}" font-size="12" text-anchor="middle" '
                     f'fill="{COLOR["kara"]}" font-weight="700">{p["speedup"]:.1f}×</text>')

    # two-line caption (boundaries — this is the honesty)
    c1 = ("Intra-Kāra: the auto-par binary vs the same source built sequentially. Auto-par targets "
          "dependency-free reductions/maps over large data;")
    c2 = ("the compiler's cost gate skips loops too small to benefit (why #4's tiny kernel gets 3.7× and "
          "#204 gets 13.4×). Raw numbers: bench-results.json")
    s.append(f'<text x="{ml}" y="{H-34}" font-size="11.5" fill="{MUTED}">{esc(c1)}</text>')
    s.append(f'<text x="{ml}" y="{H-18}" font-size="11.5" fill="{MUTED}">{esc(c2)}</text>')
    s.append('</svg>')
    return "\n".join(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", choices=["rust", "c"], default="rust")
    ap.add_argument("--feed", default="bench-results.json")
    ap.add_argument("--outdir", default="graphs")
    ap.add_argument("--only", default=None, help="render only this metric filename stem")
    ap.add_argument("--yscale", choices=["linear", "log", "clamp"], default=None,
                    help="override the per-metric y-axis scale")
    ap.add_argument("--suffix", default="", help="append to output filename stem")
    ap.add_argument("--style", choices=["line", "dots", "bars", "bars-overlap"], default="dots",
                    help="chart form: dot/scatter (default), connected line, grouped bars, or overlapped bars")
    args = ap.parse_args()

    with open(args.feed) as f:
        feed = json.load(f)
    os.makedirs(args.outdir, exist_ok=True)

    wrote = []
    for fname, title, unitnote, section, lane, langs, yscale, extract in METRICS:
        if args.only and fname != args.only:
            continue
        progs = collect(feed, section, lane, langs, extract)
        if len(progs) < 2:
            print(f"skip {fname}: only {len(progs)} program(s) with all of {langs} "
                  f"(need ≥2 for a profile)", file=sys.stderr)
            continue
        # No sorting: order follows the feed (numeric kata id). The dots are not a
        # time series and x-order carries no meaning -- see chart caption.
        ys = args.yscale or yscale
        if args.style == "line":
            svg = render(progs, args.baseline, title, unitnote, langs, ys)
        elif args.style == "dots":
            svg = render_dots(progs, args.baseline, title, unitnote, langs, ys)
        else:
            svg = render_bars(progs, args.baseline, title, unitnote, langs, ys,
                              overlap=(args.style == "bars-overlap"))
        path = os.path.join(args.outdir, fname + args.suffix + ".svg")
        with open(path, "w") as f:
            f.write(svg)
        wrote.append((path, len(progs)))

    # Auto-par speedup chart (intra-Kāra; its own shape, not the baseline model).
    if not args.only or args.only == "autopar-speedup":
        sp = collect_speedup(feed)
        if len(sp) < 2:
            print(f"skip autopar-speedup: only {len(sp)} program(s) with kāra seq+par "
                  f"(need ≥2 for a profile)", file=sys.stderr)
        else:
            path = os.path.join(args.outdir, "autopar-speedup" + args.suffix + ".svg")
            with open(path, "w") as f:
                f.write(render_speedup(sp))
            wrote.append((path, len(sp)))

    for path, k in wrote:
        print(f"wrote {path}  ({k} programs)")


if __name__ == "__main__":
    main()
