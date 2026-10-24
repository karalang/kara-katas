#!/usr/bin/env python3
"""Runs data/jobs.txt on the vendored xlrd and prints what it reads; the
expected output of mini_xlrd.kara.

Run from this directory: python3 -I -B oracle.py > expected.out"""
import io
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
import xlrd  # noqa: E402
from xlrd import formatting, xldate  # noqa: E402
from xlrd.biffh import error_text_from_code  # noqa: E402

DATA = os.path.join(HERE, "data")
CTYPE = {0: "empty", 1: "text", 2: "number", 3: "xldate", 4: "bool", 5: "error", 6: "blank"}
FMT_TYPE = {formatting.FGE: "general", formatting.FNU: "number", formatting.FDT: "date",
            formatting.FTX: "text", formatting.FUN: "unknown"}


def fnv(s):
    h = 0x811C9DC5
    for b in s.encode("utf-8"):
        h = ((h ^ b) * 0x01000193) & 0xFFFFFFFF
    return h


def show_text(v):
    if len(v) > 60:
        return "len=%d fnv=%08x %s..." % (len(v), fnv(v), ascii(v[:40]))
    return ascii(v)


def err(e):
    name = "struct.error" if isinstance(e, struct.error) else type(e).__name__
    msg = str(e)
    return "%s: %s" % (name, msg) if msg else name


class Log(io.StringIO):
    def flush_lines(self, indent="  "):
        text = self.getvalue()
        self.seek(0)
        self.truncate(0)
        lines = text.split("\n")
        if lines[-1] == "":
            lines.pop()
        for ln in lines:
            print("%slog: %s" % (indent, ln))


def show_cell(ctype, v, datemode):
    if ctype == 1:
        return "text " + show_text(v)
    if ctype == 2:
        return "number " + repr(v)
    if ctype == 3:
        try:
            t = str(xlrd.xldate_as_tuple(v, datemode))
        except xldate.XLDateError as e:
            t = "%s(%s)" % (type(e).__name__, e)
        return "xldate %r %s" % (v, t)
    if ctype == 4:
        return "bool %d" % v
    if ctype == 5:
        return "error %d %s" % (v, error_text_from_code.get(v, "?"))
    if ctype == 6:
        return "blank"
    return "%s %r" % (CTYPE[ctype], v)


def rle(xs):
    out = []
    for x in xs:
        if out and out[-1][0] == x:
            out[-1][1] += 1
        else:
            out.append([x, 1])
    return " ".join("%d*%d" % (a, b) if b > 1 else str(a) for a, b in out)


def book_line(bk):
    print("  book: biff %d, codepage %s (%s), datemode %d, user %s, countries %r, %d sheet(s)" % (
        bk.biff_version, bk.codepage, bk.encoding, bk.datemode, ascii(bk.user_name), bk.countries, bk.nsheets))


def sheet_lines(bk, sh, fmt, ragged):
    print("  sheet %d %s: %d rows x %d cols, visibility %d" % (sh.number, ascii(sh.name), sh.nrows, sh.ncols, sh.visibility))
    view = "    view: selected %d, active %d, frozen %d, grid %d, zoom %d/%d, first (%d, %d)" % (
        sh.sheet_selected, sh.sheet_visible, sh.panes_are_frozen, sh.show_grid_lines,
        sh.cooked_normal_view_mag_factor, sh.cooked_page_break_preview_mag_factor,
        sh.first_visible_rowx, sh.first_visible_colx)
    if sh.has_pane_record:
        view += ", split (%d, %d) at (%d, %d)" % (sh.horz_split_pos, sh.vert_split_pos,
                                                  sh.horz_split_first_visible, sh.vert_split_first_visible)
    print(view)
    if ragged:
        print("    row lengths: %s" % rle([sh.row_len(r) for r in range(sh.nrows)]))
    for r in range(sh.nrows):
        for c in range(sh.row_len(r)):
            ct = sh.cell_type(r, c)
            if ct == 0:
                continue
            line = "    %s %s" % (xlrd.cellname(r, c), show_cell(ct, sh.cell_value(r, c), bk.datemode))
            if fmt:
                line += "  [xf %d]" % sh.cell_xf_index(r, c)
                runs = sh.rich_text_runlist_map.get((r, c))
                if runs:
                    line += " runs %s" % " ".join("%d:%d" % tuple(x) for x in runs)
            print(line)
    if fmt:
        for rng in sh.merged_cells:
            print("    merged %s" % formula_range(rng))
        for colx in sorted(sh.colinfo_map):
            ci = sh.colinfo_map[colx]
            print("    col %s: width %d, xf %d, hidden %d, outline %d, collapsed %d" % (
                xlrd.colname(colx), ci.width, ci.xf_index, ci.hidden, ci.outline_level, ci.collapsed))
        for rowx in sorted(sh.rowinfo_map):
            ri = sh.rowinfo_map[rowx]
            print("    row %d: height %d, default %d, hidden %d, xf %d, mismatch %d, outline %d" % (
                rowx + 1, ri.height, ri.has_default_height, ri.hidden, ri.xf_index, ri.height_mismatch, ri.outline_level))
        print("    defaults: colwidth %s, standardwidth %s, rowheight %s" % (sh.defcolwidth, sh.standardwidth, sh.default_row_height))


def formula_range(rng):
    from xlrd.formula import rangename2d
    return rangename2d(*rng)


def fmt_book(bk):
    for f in bk.font_list:
        print("  font %d %s: height %d, weight %d, bold %d, italic %d, underline %d, struck %d, colour %d, escapement %d, family %d, charset %d" % (
            f.font_index, ascii(f.name), f.height, f.weight, f.bold, f.italic, f.underline_type,
            f.struck_out, f.colour_index, f.escapement, f.family, f.character_set))
    for key in sorted(bk.format_map):
        fo = bk.format_map[key]
        if key >= 164 or key in [f.format_key for f in bk.format_list]:
            print("  format %d %s: %s" % (key, ascii(fo.format_str), FMT_TYPE[fo.type]))
    for xf in bk.xf_list:
        a, b, g, p = xf.alignment, xf.border, xf.background, xf.protection
        print("  xf %d: font %d, format %d, style %d, parent %d, align %d/%d wrap %d rot %d indent %d, border %d,%d,%d,%d colours %d,%d,%d,%d, fill %d %d/%d, locked %d" % (
            xf.xf_index, xf.font_index, xf.format_key, xf.is_style, xf.parent_style_index,
            a.hor_align, a.vert_align, a.text_wrapped, a.rotation, a.indent_level,
            b.left_line_style, b.right_line_style, b.top_line_style, b.bottom_line_style,
            b.left_colour_index, b.right_colour_index, b.top_colour_index, b.bottom_colour_index,
            g.fill_pattern, g.pattern_colour_index, g.background_colour_index, p.cell_locked))
    for name in sorted(bk.style_name_map):
        bi, xfx = bk.style_name_map[name]
        print("  style %s: built-in %d, xf %d" % (ascii(name), bi, xfx))
    print("  colours used: %s" % sorted(bk.colour_indexes_used))


def job_dump(path, opts):
    fmt = "fmt" in opts
    ragged = "ragged" in opts
    ondemand = "ondemand" in opts
    log = Log()
    try:
        bk = xlrd.open_workbook(os.path.join(DATA, path), logfile=log, formatting_info=fmt,
                                ragged_rows=ragged, on_demand=ondemand)
    except Exception as e:
        log.flush_lines()
        print("  error: " + err(e))
        return
    log.flush_lines()
    book_line(bk)
    if fmt:
        fmt_book(bk)
    names = bk.sheet_names()
    if ondemand:
        print("  loaded: %s" % " ".join(str(int(bk.sheet_loaded(i))) for i in range(len(names))))
    for i in range(len(names)):
        try:
            sh = bk.sheet_by_index(i)
        except Exception as e:
            log.flush_lines()
            print("  error: " + err(e))
            return
        log.flush_lines()
        sheet_lines(bk, sh, fmt, ragged)
    if ondemand:
        print("  loaded: %s" % " ".join(str(int(bk.sheet_loaded(i))) for i in range(len(names))))
        bk.unload_sheet(names[0])
        print("  after unload: %s" % " ".join(str(int(bk.sheet_loaded(i))) for i in range(len(names))))
        bk.release_resources()
        try:
            bk.sheet_by_index(0)
        except Exception as e:
            print("  error: " + err(e))


def job_inspect(paths):
    for p in paths:
        try:
            r = xlrd.inspect_format(os.path.join(DATA, p))
        except Exception as e:
            r = "<" + err(e) + ">"
        print("  %s: %s" % (p, r))


def job_xldate(x, mode):
    v = float(x)
    try:
        t = str(xlrd.xldate_as_tuple(v, mode))
    except Exception as e:
        t = err(e)
    try:
        d = str(xlrd.xldate_as_datetime(v, mode))
    except Exception as e:
        d = err(e)
    print("  tuple %s" % t)
    print("  datetime %s" % d)


def job_fromdate(y, m, d, mode):
    try:
        print("  %r" % xldate.xldate_from_date_tuple((y, m, d), mode))
    except Exception as e:
        print("  " + err(e))


def job_fromtime(h, m, s):
    try:
        print("  %r" % xldate.xldate_from_time_tuple((h, m, s)))
    except Exception as e:
        print("  " + err(e))


def job_names(args):
    out = []
    for a in args:
        try:
            out.append("%s=%s" % (a, xlrd.colname(int(a))))
        except Exception as e:
            out.append("%s=<%s>" % (a, err(e)))
    print("  " + " ".join(out))


def job_cells(args):
    from xlrd.formula import cellnameabs
    for a in args:
        r, c = map(int, a.split(","))
        try:
            print("  %s: %s %s" % (a, xlrd.cellname(r, c), cellnameabs(r, c)))
        except Exception as e:
            print("  %s: <%s>" % (a, err(e)))


def job_ranges(args):
    from xlrd.formula import rangename2d
    for a in args:
        try:
            print("  %s: %s" % (a, rangename2d(*map(int, a.split(",")))))
        except Exception as e:
            print("  %s: <%s>" % (a, err(e)))


# ------------------------------------------------------------ programs

def cell_text(ctype, v, datemode):
    if ctype == 1:
        return v
    if ctype == 2:
        if v == int(v) and abs(v) < 1e15:
            return str(int(v))
        return repr(v)
    if ctype == 3:
        try:
            t = xlrd.xldate_as_tuple(v, datemode)
        except xldate.XLDateError:
            return "#DATE?"
        if t[0] == 0:
            return "%02d:%02d:%02d" % t[3:]
        if t[3:] == (0, 0, 0):
            return "%04d-%02d-%02d" % t[:3]
        return "%04d-%02d-%02d %02d:%02d:%02d" % t
    if ctype == 4:
        return "TRUE" if v else "FALSE"
    if ctype == 5:
        return error_text_from_code.get(v, "#ERR?")
    return ""


def csv_field(s):
    if any(ch in s for ch in ',"\n\r'):
        return '"' + s.replace('"', '""') + '"'
    return s


def prog_csv(path, sheet_name):
    try:
        bk = xlrd.open_workbook(os.path.join(DATA, path), logfile=Log())
        sh = bk.sheet_by_name(sheet_name)
    except Exception as e:
        print("  error: " + err(e))
        return
    lines = []
    for r in range(sh.nrows):
        fields = [cell_text(sh.cell_type(r, c), sh.cell_value(r, c), bk.datemode) for c in range(sh.ncols)]
        while fields and fields[-1] == "":
            fields.pop()
        lines.append(",".join(csv_field(f) for f in fields))
    stem = os.path.splitext(os.path.basename(path))[0]
    out = "out/%s_%s.csv" % (stem, sheet_name)
    os.makedirs(os.path.join(DATA, "out"), exist_ok=True)
    body = "".join(ln + "\n" for ln in lines)
    with open(os.path.join(DATA, out), "w", encoding="utf-8", newline="") as f:
        f.write(body)
    print("  wrote %s: %d rows, %d bytes" % (out, len(lines), len(body.encode("utf-8"))))
    for ln in body.split("\n")[:-1]:
        print("  | " + ln)


def prog_report(path):
    try:
        bk = xlrd.open_workbook(os.path.join(DATA, path), logfile=Log())
    except Exception as e:
        print("  error: " + err(e))
        return
    aliases = {}
    for sh in bk.sheets():
        if sh.visibility and sh.ncols >= 2:
            for r in range(sh.nrows):
                if sh.cell_type(r, 0) == 1 and sh.cell_type(r, 1) == 1:
                    aliases[sh.cell_value(r, 0)] = sh.cell_value(r, 1)
            print("  %s (hidden): %d alias(es)" % (sh.name, len(aliases)))
    regions, months, products = {}, {}, {}
    total = 0.0
    used = 0
    for sh in bk.sheets():
        if sh.visibility:
            continue
        head = [sh.cell_value(0, c) if sh.cell_type(0, c) == 1 else "" for c in range(sh.ncols)] if sh.nrows else []
        need = ["Date", "Region", "Product", "Units", "Unit price"]
        if any(h not in head for h in need):
            print("  %s: no sales table" % sh.name)
            continue
        col = {h: head.index(h) for h in need}
        rows = 0
        for r in range(1, sh.nrows):
            def get(h):
                return sh.cell_type(r, col[h]), sh.cell_value(r, col[h])
            dt, dv = get("Date")
            rt, rv = get("Region")
            pt, pv = get("Product")
            ut, uv = get("Units")
            qt, qv = get("Unit price")
            where = "%s!%s" % (sh.name, xlrd.cellname(r, col["Units"]))
            if ut == 0:
                print("  %s: units missing, row skipped" % where)
                continue
            if ut == 1:
                print("  %s: units %s is text, row skipped" % (where, ascii(uv)))
                continue
            if ut == 5:
                print("  %s: units %s, row skipped" % (where, error_text_from_code.get(uv, "?")))
                continue
            if dt != 3 or qt != 2 or rt != 1 or pt != 1:
                print("  %s!row %d: unexpected cell types, row skipped" % (sh.name, r + 1))
                continue
            y, m = xlrd.xldate_as_tuple(dv, bk.datemode)[:2]
            region = aliases.get(rv, rv)
            if region != rv:
                print("  %s!%s: region %s read as %s" % (sh.name, xlrd.cellname(r, col["Region"]), ascii(rv), ascii(region)))
            amount = uv * qv
            regions.setdefault(region, [0.0, 0.0])
            regions[region][0] += uv
            regions[region][1] += amount
            key = "%04d-%02d" % (y, m)
            months[key] = months.get(key, 0.0) + amount
            products[pv] = products.get(pv, 0.0) + amount
            total += amount
            rows += 1
        used += rows
        print("  %s: %d sale(s)" % (sh.name, rows))
    if not used:
        print("  nothing to report")
        return
    for k in sorted(regions):
        print("  region %-6s units %5d  revenue %9.2f" % (k, regions[k][0], regions[k][1]))
    for k in sorted(months):
        print("  month %s revenue %9.2f" % (k, months[k]))
    best = sorted(products.items(), key=lambda kv: (-kv[1], kv[0]))
    for k, v in best:
        print("  product %-7s revenue %9.2f  share %5.1f%%" % (k, v, 100.0 * v / total))
    print("  total revenue %.2f over %d sale(s)" % (total, used))


def prog_find(path, needle):
    try:
        bk = xlrd.open_workbook(os.path.join(DATA, path), logfile=Log())
    except Exception as e:
        print("  error: " + err(e))
        return
    n = 0
    low = needle.lower()
    for sh in bk.sheets():
        for r in range(sh.nrows):
            for c in range(sh.ncols):
                if sh.cell_type(r, c) == 1 and low in sh.cell_value(r, c).lower():
                    n += 1
                    if n <= 12:
                        print("  %s!%s %s" % (ascii(sh.name), xlrd.cellname(r, c), show_text(sh.cell_value(r, c))))
    print("  %d match(es)" % n)


def main():
    with open(os.path.join(DATA, "jobs.txt"), encoding="utf-8") as f:
        lines = [ln for ln in f.read().split("\n") if ln]
    for line in lines:
        if line.startswith("#"):
            print(line)
            continue
        print("> " + line)
        parts = line.split(" ")
        cmd, args = parts[0], parts[1:]
        if cmd == "dump":
            job_dump(args[0], args[1:])
        elif cmd == "fmt":
            job_dump(args[0], ["fmt"] + args[1:])
        elif cmd == "xldate":
            job_xldate(args[0], int(args[1]))
        elif cmd == "fromdate":
            job_fromdate(*map(int, args))
        elif cmd == "fromtime":
            job_fromtime(*map(int, args))
        elif cmd == "names":
            job_names(args)
        elif cmd == "cells":
            job_cells(args)
        elif cmd == "ranges":
            job_ranges(args)
        elif cmd == "!inspect":
            job_inspect(args)
        elif cmd == "!csv":
            prog_csv(args[0], args[1])
        elif cmd == "!report":
            prog_report(args[0])
        elif cmd == "!find":
            prog_find(args[0], args[1])
        else:
            print("unknown job " + line)


main()
