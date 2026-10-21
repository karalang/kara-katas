# Runs data/jobs.jsonl through prettytable itself (the copy in
# prettytable/, unchanged, with the copy of wcwidth in wcwidth/) and
# prints what mini_prettytable prints.
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from prettytable import (  # noqa: E402
    HRuleStyle,
    PrettyTable,
    TableStyle,
    VRuleStyle,
    from_csv,
    from_html,
    from_html_one,
    from_json,
    from_mediawiki,
)
from prettytable.colortable import ColorTable, Theme, Themes  # noqa: E402

DATA = os.path.join(HERE, "data")


# The functions a job names for sort_key, row_filter and custom_format.
SORT_KEYS = {
    "lower": lambda x: str(x[0]).lower(),
    "length": lambda x: len(str(x[0])),
    "last": lambda x: x[-1],
    "number": lambda x: float(x[0]),
    "rest": lambda x: x[1:],
}

FORMATTERS = {
    "upper": lambda f, v: str(v).upper(),
    "money": lambda f, v: f"${v:,.2f}" if v != "" else "",
    "percent": lambda f, v: f"{v:.1%}",
    "label": lambda f, v: f"{f}={v}",
    "yesno": lambda f, v: "yes" if v else "no",
    "kib": lambda f, v: f"{v / 1024:.1f} KiB",
    "lines": lambda f, v: str(v).replace(", ", "\n"),
    "red": lambda f, v: f"\x1b[31m{v}\x1b[0m",
    "link": lambda f, v: f"\x1b]8;;https://pypi.org/project/{v}/\x1b\\{v}\x1b]8;;\x1b\\",
}


def row_filter(spec):
    kind = spec[0]
    if kind == "gt":
        i, v = spec[1], spec[2]
        return lambda r: r[i] > v
    if kind == "eq":
        i, v = spec[1], spec[2]
        return lambda r: r[i] == v
    if kind == "has":
        i, v = spec[1], spec[2]
        return lambda r: v in str(r[i])
    if kind == "truthy":
        i = spec[1]
        return lambda r: bool(r[i])
    raise SystemExit(f"unknown filter {spec}")


ENUMS = {"hrules": HRuleStyle, "vrules": VRuleStyle}


def conv(name, v):
    if name in ENUMS and isinstance(v, str):
        return ENUMS[name][v]
    if name == "sort_key":
        return SORT_KEYS[v]
    if name == "row_filter":
        return row_filter(v)
    if name == "custom_format":
        if isinstance(v, dict):
            return {k: FORMATTERS[f] for k, f in v.items()}
        if isinstance(v, str):
            return FORMATTERS[v]
    if name == "attributes" and isinstance(v, list):
        return dict(v)
    return v


def kwargs_of(kw):
    return {k: conv(k, v) for k, v in (kw or {}).items()}


def read(path, newline=None):
    with open(os.path.join(DATA, path), encoding="utf-8", newline=newline) as f:
        return f.read()


def visible(s):
    return s.replace("\r", "\\r").replace("\f", "\\f")


def show(t, op):
    fmt = op["fmt"]
    kw = kwargs_of(op.get("kw"))
    if fmt == "str":
        return str(t)
    if fmt == "text":
        return t.get_string(**kw)
    if fmt == "html":
        return t.get_html_string(**kw)
    if fmt == "csv":
        return t.get_csv_string(**kw)
    if fmt == "json":
        return t.get_json_string(**kw)
    if fmt == "latex":
        return t.get_latex_string(**kw)
    if fmt == "mediawiki":
        return t.get_mediawiki_string(**kw)
    if fmt == "formatted":
        return t.get_formatted_string(op["out"], **kw)
    if fmt == "paginate":
        args = {}
        if "page_length" in op:
            args["page_length"] = op["page_length"]
        if "line_break" in op:
            args["line_break"] = op["line_break"]
        return t.paginate(**args, **kw)
    raise SystemExit(f"unknown format {fmt}")


def run_op(tables, op):
    kind = op["op"]
    name = op.get("t", "t")
    if kind == "new":
        cls = ColorTable if op.get("cls") == "ColorTable" else PrettyTable
        kw = kwargs_of(op.get("kw"))
        if "field_names" in op:
            tables[name] = cls(op["field_names"], **kw)
        else:
            tables[name] = cls(**kw)
        return None
    if kind == "from_csv":
        params = kwargs_of(op.get("kw"))
        with open(os.path.join(DATA, op["file"]), encoding="utf-8") as fp:
            if "field_names" in op:
                tables[name] = from_csv(fp, op["field_names"], **params)
            else:
                tables[name] = from_csv(fp, **params)
        return None
    if kind == "from_json":
        text = op["text"] if "text" in op else read(op["file"])
        tables[name] = from_json(text, **kwargs_of(op.get("kw")))
        return None
    if kind == "from_html":
        found = from_html(read(op["file"]), **kwargs_of(op.get("kw")))
        for i, tab in enumerate(found):
            tables[f"{name}{i}"] = tab
        return f"{len(found)} tables"
    if kind == "from_html_one":
        tables[name] = from_html_one(read(op["file"]), **kwargs_of(op.get("kw")))
        return None
    if kind == "from_mediawiki":
        text = op["text"] if "text" in op else read(op["file"])
        tables[name] = from_mediawiki(text, **kwargs_of(op.get("kw")))
        return None

    t = tables[name]
    if kind == "set":
        setattr(t, op["attr"], conv(op["attr"], op["value"]))
    elif kind == "set_key":
        getattr(t, op["attr"])[op["key"]] = conv(op["attr"], op["value"])
    elif kind == "theme":
        t.theme = getattr(Themes, op["name"])
    elif kind == "custom_theme":
        t.theme = Theme(**op["kw"])
    elif kind == "add_row":
        t.add_row(op["row"], divider=op.get("divider", False))
    elif kind == "add_rows":
        t.add_rows(op["rows"], divider=op.get("divider", False))
    elif kind == "add_column":
        args = {k: op[k] for k in ("align", "valign") if k in op}
        t.add_column(op["name"], op["column"], **args)
    elif kind == "add_autoindex":
        if "name" in op:
            t.add_autoindex(op["name"])
        else:
            t.add_autoindex()
    elif kind == "del_row":
        t.del_row(op["i"])
    elif kind == "del_column":
        t.del_column(op["name"])
    elif kind == "add_divider":
        t.add_divider()
    elif kind == "clear_rows":
        t.clear_rows()
    elif kind == "clear":
        t.clear()
    elif kind == "set_style":
        style = op["style"]
        t.set_style(TableStyle[style] if isinstance(style, str) else style)
    elif kind == "slice":
        tables[op["to"]] = t[op.get("lo"):op.get("hi")]
    elif kind == "index":
        tables[op["to"]] = t[op["i"]]
    elif kind == "copy":
        tables[op["to"]] = t.copy()
    elif kind == "get":
        return f"{op['attr']} = {getattr(t, op['attr'])!r}"
    elif kind == "show":
        return "-- " + op["say"] + "\n" + visible(show(t, op))
    else:
        raise SystemExit(f"unknown op {kind}")
    return None


def main():
    with open(os.path.join(DATA, "jobs.jsonl"), encoding="utf-8") as f:
        jobs = [json.loads(line) for line in f]
    for job in jobs:
        print(f"== {job['name']}")
        tables = {}
        for op in job["ops"]:
            try:
                out = run_op(tables, op)
            except Exception as e:  # noqa: BLE001
                print(f"! {type(e).__name__}: {e}")
                continue
            if out is not None:
                print(out)


main()
