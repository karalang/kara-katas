# Writes data/: the jobs (data/jobs.jsonl), the files the programs read,
# and data/wcwidth.txt, the width tables of the copy of wcwidth in
# wcwidth/ (Unicode 15.1.0, the version it uses by default).
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
DATA = os.path.join(HERE, "data")

from wcwidth.table_vs16 import VS16_NARROW_TO_WIDE  # noqa: E402
from wcwidth.table_wide import WIDE_EASTASIAN  # noqa: E402
from wcwidth.table_zero import ZERO_WIDTH  # noqa: E402


def put(name, text, newline="\n"):
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, name), "w", encoding="utf-8", newline=newline) as f:
        f.write(text)


def ranges(table):
    return " ".join(f"{a:x}-{b:x}" for a, b in table)


put(
    "wcwidth.txt",
    ranges(ZERO_WIDTH["15.1.0"]) + "\n"
    + ranges(WIDE_EASTASIAN["15.1.0"]) + "\n"
    + ranges(VS16_NARROW_TO_WIDE["9.0.0"]) + "\n",
)

JOBS = []


def job(name, ops):
    JOBS.append({"name": name, "ops": ops})


def show(say, fmt="str", t="t", **kw):
    op = {"op": "show", "t": t, "say": say, "fmt": fmt}
    if kw:
        op["kw"] = kw
    return op


def text(say, t="t", **kw):
    return show(say, "text", t, **kw)


CITIES = ["City name", "Area", "Population", "Annual Rainfall"]
CITY_ROWS = [
    ["Adelaide", 1295, 1158259, 600.5],
    ["Brisbane", 5905, 1857594, 1146.4],
    ["Darwin", 112, 120900, 1714.7],
    ["Hobart", 1357, 205556, 619.5],
    ["Melbourne", 1566, 3806092, 646.9],
    ["Perth", 5386, 1554769, 869.4],
    ["Sydney", 2058, 4336374, 1214.8],
]


def cities(t="t", divider=False, **kw):
    ops = [{"op": "new", "t": t, "field_names": CITIES}]
    if kw:
        ops[0]["kw"] = kw
    for row in CITY_ROWS:
        op = {"op": "add_row", "t": t, "row": row}
        if divider and row[0] == "Hobart":
            op["divider"] = True
        ops.append(op)
    return ops


# ------------------------------------------------------------ basics

job("basics", cities() + [
    show("print(table)"),
    {"op": "get", "attr": "rowcount"},
    {"op": "get", "attr": "colcount"},
    {"op": "get", "attr": "field_names"},
    text("sortby=Population, reversesort", sortby="Population", reversesort=True),
    text("fields=[City name, Population]", fields=["City name", "Population"]),
    text("start=2, end=5", start=2, end=5),
    text("title", title="Australian capital cities"),
    text("header=False", header=False),
    text("border=False", border=False),
    text("border=False, preserve_internal_border", border=False, preserve_internal_border=True),
    text("hrules=ALL", hrules="ALL"),
    text("hrules=NONE", hrules="NONE"),
    text("hrules=HEADER", hrules="HEADER"),
    text("vrules=FRAME", vrules="FRAME"),
    text("vrules=NONE", vrules="NONE"),
    text("vrules=NONE, hrules=ALL", vrules="NONE", hrules="ALL"),
    text("padding_width=3", padding_width=3),
    text("left 0, right 4", left_padding_width=0, right_padding_width=4),
    text("junction and edge chars", vertical_char=":", horizontal_char="=", junction_char="#",
         top_left_junction_char="/", top_right_junction_char="\\",
         bottom_left_junction_char="\\", bottom_right_junction_char="/"),
    {"op": "set", "attr": "align", "value": "l"},
    {"op": "set_key", "attr": "align", "key": "Population", "value": "r"},
    {"op": "set_key", "attr": "align", "key": "Annual Rainfall", "value": "r"},
    show("align l, numbers r"),
    {"op": "get", "attr": "align"},
    {"op": "set", "attr": "header_style", "value": "upper"},
    show("header_style=upper"),
    {"op": "set", "attr": "header_style", "value": "title"},
    {"op": "set", "attr": "field_names", "value": ["city NAME", "area km2", "population", "annual rainfall mm"]},
    show("renamed fields, header_style=title"),
    {"op": "get", "attr": "align"},
    {"op": "set", "attr": "header_style", "value": "cap"},
    show("header_style=cap"),
    {"op": "set", "attr": "header_style", "value": "lower"},
    show("header_style=lower"),
    {"op": "set", "attr": "header_style", "value": None},
    {"op": "del_row", "i": 0},
    {"op": "del_column", "name": "area km2"},
    show("without Adelaide and area"),
    {"op": "add_column", "name": "State", "column": ["QLD", "NT", "TAS", "VIC", "WA", "NSW"], "align": "l"},
    {"op": "add_autoindex"},
    show("with State and Index"),
    {"op": "add_autoindex", "name": "#"},
    show("a second index"),
    {"op": "get", "attr": "rows"},
    {"op": "add_divider"},
    {"op": "get", "attr": "dividers"},
    {"op": "clear_rows"},
    show("cleared rows"),
    text("cleared rows, print_empty=False", print_empty=False),
    text("cleared rows, border=False", border=False),
    {"op": "clear"},
    show("cleared"),
    {"op": "get", "attr": "colcount"},
    {"op": "add_row", "row": ["no", "names", 3]},
    show("rows without field names"),
    {"op": "get", "attr": "field_names"},
    {"op": "new", "t": "e"},
    show("a new empty table", t="e"),
    {"op": "get", "t": "e", "attr": "colcount"},
    {"op": "add_column", "t": "e", "name": "Fruit", "column": ["apple", "pear"]},
    {"op": "add_column", "t": "e", "name": "Count", "column": [3, 12], "align": "r", "valign": "b"},
    show("built from columns", t="e"),
])

# ------------------------------------------------------------ constructor options and errors

job("options", [
    {"op": "new", "field_names": ["a", "b"], "kw": {"vrules": "FRAME", "left_padding_width": 0, "header": 1}},
    {"op": "add_row", "row": [1, 2]},
    show("vrules=FRAME, left_padding_width=0, header=1 in the constructor"),
    {"op": "get", "attr": "vrules"},
    {"op": "get", "attr": "left_padding_width"},
    {"op": "set", "attr": "vrules", "value": "FRAME"},
    {"op": "set", "attr": "left_padding_width", "value": 0},
    show("the same set as attributes"),
    {"op": "get", "attr": "horizontal_align_char"},
    {"op": "set", "attr": "bottom_left_junction_char", "value": "L"},
    {"op": "get", "attr": "horizontal_align_char"},
    {"op": "get", "attr": "top_junction_char"},
    {"op": "set", "attr": "junction_char", "value": "*"},
    {"op": "get", "attr": "top_junction_char"},
    show("junction * with a bottom-left L"),
    {"op": "new", "t": "x", "field_names": ["a"], "kw": {"start": -1}},
    {"op": "new", "t": "x", "field_names": ["a"], "kw": {"hrules": 7}},
    {"op": "new", "t": "x", "field_names": ["a"], "kw": {"sortby": "b"}},
    {"op": "new", "t": "x", "field_names": ["a"], "kw": {"fields": ["a", "z"]}},
    {"op": "new", "t": "x", "field_names": ["a"], "kw": {"junction_char": "++"}},
    {"op": "new", "t": "x", "field_names": ["a"], "kw": {"int_format": "x"}},
    {"op": "new", "t": "x", "field_names": ["a"], "kw": {"float_format": "a.b"}},
    {"op": "new", "t": "x", "field_names": ["a"], "kw": {"float_format": "5"}},
    {"op": "new", "t": "x", "field_names": ["a"], "kw": {"float_format": "1.2.3"}},
    {"op": "new", "t": "x", "field_names": ["a"], "kw": {"header_style": "shout"}},
    {"op": "new", "t": "x", "field_names": ["a"], "kw": {"border": "yes"}},
    {"op": "new", "t": "x", "field_names": ["a"], "kw": {"none_format": 0}},
    {"op": "new", "t": "x", "field_names": ["a"], "kw": {"attributes": "class=x"}},
    {"op": "new", "t": "x", "field_names": ["a", "a"]},
    {"op": "new", "t": "x", "field_names": ["a", "b"]},
    {"op": "add_row", "t": "x", "row": [1]},
    {"op": "set", "t": "x", "attr": "field_names", "value": ["a", "b", "c"]},
    {"op": "del_row", "t": "x", "i": 0},
    {"op": "del_column", "t": "x", "name": "c"},
    {"op": "add_row", "t": "x", "row": [1, 2]},
    {"op": "add_column", "t": "x", "name": "c", "column": [1, 2]},
    {"op": "add_column", "t": "x", "name": "c", "column": [1], "align": "x"},
    {"op": "add_column", "t": "x", "name": "c", "column": [1], "valign": "x"},
    {"op": "set", "t": "x", "attr": "align", "value": "x"},
    {"op": "set", "t": "x", "attr": "valign", "value": "x"},
    {"op": "set", "t": "x", "attr": "max_width", "value": -2},
    {"op": "set", "t": "x", "attr": "sortby", "value": "zz"},
    {"op": "set", "t": "x", "attr": "padding_width", "value": -1},
    {"op": "set", "t": "x", "attr": "vertical_char", "value": "||"},
    {"op": "set", "t": "x", "attr": "vertical_char", "value": 7},
    show("vertical char 7", t="x"),
    {"op": "set", "t": "x", "attr": "title", "value": 2024},
    {"op": "get", "t": "x", "attr": "title"},
    {"op": "set_key", "t": "x", "attr": "align", "key": "a", "value": "x"},
    show("an alignment set straight into the dict", t="x"),
    show("the same in formatted HTML", "html", "x", format=True),
    {"op": "set_style", "t": "x", "style": 99},
    show("after an invalid style", t="x"),
    text("max_width passed to get_string", "x", max_width=1),
    {"op": "show", "t": "x", "say": "an unknown format", "fmt": "formatted", "out": "yaml"},
    {"op": "new", "t": "k", "kw": {"align": "r", "valign": "b"}},
    {"op": "add_row", "t": "k", "row": ["x", "yy\nyy"]},
    {"op": "add_autoindex", "t": "k"},
    show("align r, valign b in the constructor, then an index", t="k"),
    {"op": "set", "t": "k", "attr": "max_width", "value": 1},
    {"op": "set", "t": "k", "attr": "field_names", "value": ["N", "P", "Q"]},
    show("renaming resets max_width", t="k"),
    {"op": "get", "t": "k", "attr": "max_width"},
    {"op": "get", "t": "k", "attr": "align"},
    {"op": "get", "t": "k", "attr": "valign"},
])

# ------------------------------------------------------------ styles

STYLES = ["DEFAULT", "MSWORD_FRIENDLY", "PLAIN_COLUMNS", "MARKDOWN", "ORGMODE", "DOUBLE_BORDER", "SINGLE_BORDER"]

style_ops = cities(divider=True)
for s in STYLES:
    style_ops.append({"op": "set_style", "style": s})
    style_ops.append(show(f"style {s}"))
style_ops += [
    {"op": "set_style", "style": "MARKDOWN"},
    {"op": "set_key", "attr": "align", "key": "City name", "value": "l"},
    {"op": "set_key", "attr": "align", "key": "Population", "value": "r"},
    show("markdown with l, c and r columns"),
    {"op": "get", "attr": "horizontal_align_char"},
    text("markdown, title", title="Rain"),
    {"op": "new", "t": "m", "field_names": ["k", "v"]},
    {"op": "add_row", "t": "m", "row": ["a", ""]},
    {"op": "set_style", "t": "m", "style": "MARKDOWN"},
    {"op": "set_key", "t": "m", "attr": "align", "key": "k", "value": "l"},
    show("markdown, narrow columns", t="m"),
    {"op": "set_style", "style": "ORGMODE"},
    text("orgmode, title", title="Rain"),
    text("orgmode, no header", header=False),
    {"op": "set_style", "style": "DOUBLE_BORDER"},
    text("double border, title", title="Rain"),
    text("double border, no header, title", header=False, title="Rain"),
    text("double border, hrules ALL", hrules="ALL", end=3),
    text("double border, vrules FRAME", vrules="FRAME", end=3),
    text("double border, vrules NONE", vrules="NONE", end=3),
    {"op": "set_style", "style": "SINGLE_BORDER"},
    text("single border, title, fields", title="Rain", fields=["City name", "Annual Rainfall"]),
    text("single border, preserve_internal_border", border=False, preserve_internal_border=True, end=3),
    {"op": "set_style", "style": "PLAIN_COLUMNS"},
    text("plain columns, title", title="Rain"),
    {"op": "set_style", "style": "DEFAULT"},
    show("back to default"),
    {"op": "set_style", "style": "MSWORD_FRIENDLY"},
    text("msword, title", title="Rain"),
]
job("styles", style_ops)

# ------------------------------------------------------------ number and value formats

job("formats", [
    {"op": "new", "field_names": ["name", "count", "ratio", "flag", "note"]},
    {"op": "add_rows", "rows": [
        ["alpha", 3, 0.5, True, None],
        ["beta", 42, 2.0, False, "ok"],
        ["gamma", -7, 1234.5678, True, None],
        ["delta", 0, -0.125, None, "None"],
        ["eps", 1000000, 1e-07, 1, 3.0],
        ["zeta", 12, 1e16, 0, 0.1],
    ]},
    show("str() of each value"),
    {"op": "set", "attr": "int_format", "value": "03"},
    show("int_format=03"),
    {"op": "set", "attr": "int_format", "value": "8"},
    {"op": "set", "attr": "float_format", "value": "5.2"},
    show("int_format=8, float_format=5.2"),
    {"op": "set", "attr": "float_format", "value": ".1"},
    show("float_format=.1"),
    {"op": "set", "attr": "float_format", "value": "4."},
    show("float_format=4."),
    {"op": "set", "attr": "float_format", "value": "6.2f"},
    show("float_format=6.2f"),
    {"op": "set", "attr": "float_format", "value": "09.3"},
    show("float_format=09.3"),
    {"op": "set", "attr": "float_format", "value": ""},
    show("float_format empty"),
    {"op": "set", "attr": "float_format", "value": {}},
    {"op": "set", "attr": "int_format", "value": {}},
    show("formats cleared"),
    {"op": "set_key", "attr": "int_format", "key": "count", "value": "+5"},
    show("int_format +5 on count, set straight into the dict"),
    {"op": "set_key", "attr": "int_format", "key": "count", "value": "05"},
    {"op": "set_key", "attr": "float_format", "key": "ratio", "value": ".3e"},
    show("float_format .3e on ratio, set straight into the dict"),
    {"op": "set", "attr": "float_format", "value": {}},
    {"op": "set", "attr": "int_format", "value": {}},
    {"op": "set", "attr": "none_format", "value": "-"},
    show("none_format=-"),
    {"op": "set_key", "attr": "none_format", "key": "note", "value": "(none)"},
    show("none_format (none) on note"),
    {"op": "get", "attr": "none_format"},
    {"op": "set", "attr": "none_format", "value": {}},
    {"op": "set", "attr": "custom_format", "value": {"ratio": "percent", "flag": "yesno", "name": "upper"}},
    show("custom formats"),
    text("custom formats, sorted by ratio", sortby="ratio"),
    {"op": "set", "attr": "custom_format", "value": "label"},
    show("one custom format for every field"),
    {"op": "set", "attr": "custom_format", "value": None},
    show("custom format cleared"),
    {"op": "set", "attr": "custom_format", "value": 5},
    {"op": "new", "t": "p", "field_names": ["item", "price", "qty"], "kw": {"custom_format": {"price": "money"}, "int_format": "4"}},
    {"op": "add_row", "t": "p", "row": ["Widget", 1234.5, 3]},
    {"op": "add_row", "t": "p", "row": ["Gadget", 0.015, 12]},
    {"op": "add_row", "t": "p", "row": ["Gizmo", 1000000.004999, 1]},
    show("money and int_format=4 from the constructor", t="p"),
    {"op": "set", "t": "p", "attr": "field_names", "value": ["Item", "Price", "Qty"]},
    show("renamed: the formats come back from the constructor", t="p"),
])

# ------------------------------------------------------------ widths and wrapping

LONG = ("A small library for printing tables in ASCII form, used by command line tools, "
        "test runners and well-known database shells.")

job("widths", [
    {"op": "new", "field_names": ["package", "summary"]},
    {"op": "add_row", "row": ["prettytable", LONG]},
    {"op": "add_row", "row": ["tabulate", "Pretty-print tabular data in Python, a library and a command-line utility."]},
    {"op": "add_row", "row": ["rich", "Rich text and beautiful formatting in the terminal."]},
    show("no limits"),
    {"op": "set", "attr": "max_width", "value": 30},
    show("max_width=30"),
    {"op": "set", "attr": "break_on_hyphens", "value": False},
    show("max_width=30, break_on_hyphens=False"),
    {"op": "set", "attr": "break_on_hyphens", "value": True},
    {"op": "set", "attr": "max_width", "value": 6},
    show("max_width=6"),
    {"op": "set", "attr": "max_width", "value": {}},
    {"op": "set_key", "attr": "max_width", "key": "summary", "value": 24},
    {"op": "set_key", "attr": "min_width", "key": "package", "value": 16},
    {"op": "set", "attr": "valign", "value": "m"},
    {"op": "set", "attr": "hrules", "value": "ALL"},
    show("summary wrapped at 24, package at least 16, valign m"),
    {"op": "set", "attr": "valign", "value": "b"},
    show("valign b"),
    {"op": "set", "attr": "max_width", "value": {}},
    {"op": "set", "attr": "min_width", "value": {}},
    {"op": "set", "attr": "max_table_width", "value": 50},
    show("max_table_width=50"),
    text("max_table_width=50, vrules FRAME", vrules="FRAME"),
    {"op": "set", "attr": "max_table_width", "value": None},
    {"op": "set", "attr": "max_table_width", "value": 0},
    {"op": "set", "attr": "max_width", "value": 0},
    show("max_width=0"),
    {"op": "set", "attr": "max_width", "value": {}},
    {"op": "new", "t": "s", "field_names": ["k", "v"]},
    {"op": "add_row", "t": "s", "row": ["a", 1]},
    {"op": "set", "t": "s", "attr": "min_table_width", "value": 31},
    show("min_table_width=31", t="s"),
    text("min_table_width=31, border=False", "s", border=False),
    {"op": "set", "t": "s", "attr": "min_table_width", "value": 0},
    text("a title wider than the table", "s", title="Configuration values"),
    text("a title, vrules NONE", "s", title="Configuration values", vrules="NONE"),
    text("a title, header off", "s", title="Configuration values", header=False),
    text("use_header_width=False", "s", use_header_width=False),
    {"op": "set", "t": "s", "attr": "field_names", "value": ["a very long key", "v"]},
    {"op": "set_key", "t": "s", "attr": "max_width", "key": "a very long key", "value": 4},
    show("a header longer than max_width", t="s"),
    {"op": "new", "t": "u", "field_names": ["text", "kind"]},
    {"op": "add_rows", "t": "u", "rows": [
        ["日本語", "CJK"],
        ["café", "precomposed"],
        ["café", "combining"],
        ["👍", "emoji"],
        ["❤️", "VS16"],
        ["👩‍💻", "ZWJ"],
        ["tab\there", "tab"],
        ["\x1b[1mbold\x1b[0m", "ANSI"],
        ["\x1b]8;;https://example.com\x1b\\link\x1b]8;;\x1b\\", "OSC 8"],
        ["two\nlines", "newline"],
    ]},
    show("widths of wide, combining, emoji, control and escape text", t="u"),
    {"op": "set", "t": "u", "attr": "align", "value": "r"},
    show("right aligned", t="u"),
    {"op": "set", "t": "u", "attr": "max_width", "value": 3},
    show("max_width=3", t="u"),
])

# ------------------------------------------------------------ sorting and filtering

job("sorting", [
    {"op": "new", "field_names": ["name", "team", "score", "joined"]},
    {"op": "add_rows", "rows": [
        ["bob", "red", 12, "2021-03-04"],
        ["Alice", "blue", 15, "2020-11-30"],
        ["carol", "red", 12, "2022-01-15"],
        ["dave", "green", 9, "2021-07-22"],
        ["Eve", "blue", 15, "2019-05-01"],
        ["frank", "green", 12, "2023-02-14"],
    ], "divider": True},
    {"op": "add_divider"},
    show("as added, with a divider at the end"),
    text("sortby=name", sortby="name"),
    text("sortby=score (ties keep their order)", sortby="score"),
    text("sortby=score, reversesort", sortby="score", reversesort=True),
    text("sortby=name, sort_key=lower", sortby="name", sort_key="lower"),
    text("sortby=team, sort_key=length", sortby="team", sort_key="length"),
    text("sortby=team, sort_key=last", sortby="team", sort_key="last"),
    text("sortby=score, sort_key=rest", sortby="score", sort_key="rest"),
    text("sortby=joined, reversesort, start=1, end=4", sortby="joined", reversesort=True, start=1, end=4),
    text("same with oldsortslice", sortby="joined", reversesort=True, start=1, end=4, oldsortslice=True),
    text("start=1, end=4 without sorting", start=1, end=4),
    text("start=1, end=4, oldsortslice, no sort", start=1, end=4, oldsortslice=True),
    text("row_filter score > 10", row_filter=["gt", 2, 10]),
    text("row_filter team == red", row_filter=["eq", 1, "red"]),
    text("row_filter joined has 2021", row_filter=["has", 3, "2021"]),
    text("row_filter score > 'x'", row_filter=["gt", 2, "x"]),
    text("sortby=name, sort_key=number", sortby="name", sort_key="number"),
    text("sortby=score, sort_key=number", sortby="score", sort_key="number"),
    {"op": "set", "attr": "sortby", "value": "score"},
    {"op": "set", "attr": "reversesort", "value": True},
    show("sortby set on the table"),
    {"op": "set", "attr": "sortby", "value": None},
    {"op": "set", "attr": "reversesort", "value": False},
    {"op": "add_row", "row": ["gina", "blue", None, "2024-06-01"]},
    text("a None score", sortby="score"),
    text("a None score, reversed", sortby="score", reversesort=True),
    {"op": "del_row", "i": 6},
    {"op": "add_row", "row": ["hal", "red", "n/a", "2024-06-02"]},
    text("a string score", sortby="score"),
    {"op": "add_row", "row": ["ivy", "red", 12.0, "2024-06-03"]},
    {"op": "del_row", "i": 6},
    text("a float score among ints", sortby="score"),
    text("row_filter truthy score", row_filter=["truthy", 2]),
    {"op": "new", "t": "w", "field_names": ["word"]},
    {"op": "add_rows", "t": "w", "rows": [["b"], ["B"], ["a"], ["é"], ["Z"], [""], ["ab"]]},
    text("code point order", "w", sortby="word"),
    text("code point order, reversed", "w", sortby="word", reversesort=True),
    {"op": "new", "t": "m", "field_names": ["v", "w"]},
    {"op": "add_rows", "t": "m", "rows": [[3, "x"], [1, "y"], [True, "z"], [2.5, "q"], [1.0, "r"], [False, "s"]]},
    text("ints, floats and bools together", "m", sortby="v"),
    {"op": "add_row", "t": "m", "row": ["9", "t"]},
    text("and a string", "m", sortby="v"),
    text("and a string, reversed", "m", sortby="v", reversesort=True),
])

# ------------------------------------------------------------ HTML

job("html", cities(divider=True, end=4) + [
    {"op": "set_key", "attr": "align", "key": "City name", "value": "l"},
    {"op": "set_key", "attr": "valign", "key": "Area", "value": "b"},
    {"op": "add_row", "row": ["<Canberra & co>", 814, 467194, "616.4\n(est.)"]},
    show("simple HTML", "html"),
    show("simple HTML, xhtml, attributes", "html", attributes=[["class", "cities"], ["data-x", "a\"b<c>"]], xhtml=True),
    show("simple HTML, no escaping, fields, title", "html", escape_data=False, escape_header=False,
         fields=["City name", "Annual Rainfall"], title="Rain & sun"),
    show("formatted HTML", "html", format=True),
    show("formatted HTML, hrules ALL", "html", format=True, hrules="ALL"),
    show("formatted HTML, vrules FRAME", "html", format=True, vrules="FRAME", padding_width=2),
    show("formatted HTML, hrules ALL, vrules FRAME", "html", format=True, hrules="ALL", vrules="FRAME"),
    show("formatted HTML, hrules ALL, vrules NONE", "html", format=True, hrules="ALL", vrules="NONE"),
    show("formatted HTML, hrules NONE", "html", format=True, hrules="NONE"),
    show("formatted HTML, hrules NONE, vrules FRAME", "html", format=True, hrules="NONE", vrules="FRAME"),
    show("formatted HTML, hrules NONE, vrules NONE", "html", format=True, hrules="NONE", vrules="NONE"),
    show("formatted HTML, no border, internal border", "html", format=True, border=False, preserve_internal_border=True),
    show("formatted HTML, header off, sorted, sliced", "html", format=True, header=False, sortby="Area", start=1, end=3),
])

# ------------------------------------------------------------ CSV, JSON, LaTeX, MediaWiki

export_ops = cities(end=4) + [
    {"op": "add_row", "row": ["Port \"Lincoln\"", 30, None, True]},
    show("CSV", "csv"),
    show("CSV, semicolons, no header", "csv", delimiter=";", header=False),
    show("CSV, fields, QUOTE_ALL", "csv", fields=["City name", "Area"], quoting=1),
    show("CSV, QUOTE_NONNUMERIC, LF line ends", "csv", quoting=2, lineterminator="\n"),
    show("CSV, sorted by area", "csv", sortby="Area"),
    show("JSON", "json"),
    show("JSON, fields, no header, indent 2", "json", fields=["Area", "City name"], header=False, indent=2),
    show("JSON, compact, keys unsorted", "json", indent=None, separators=[",", ":"], sort_keys=False),
    show("LaTeX", "latex"),
    show("LaTeX, fields, no header", "latex", fields=["Population", "City name"], header=False),
    show("formatted LaTeX", "latex", format=True),
    show("formatted LaTeX, hrules ALL", "latex", format=True, hrules="ALL"),
    show("formatted LaTeX, hrules HEADER, vrules FRAME", "latex", format=True, hrules="HEADER", vrules="FRAME"),
    show("formatted LaTeX, no border", "latex", format=True, border=False),
    show("formatted LaTeX, no border, internal border", "latex", format=True, border=False, preserve_internal_border=True),
    show("formatted LaTeX, vrules NONE, hrules NONE", "latex", format=True, vrules="NONE", hrules="NONE"),
    show("MediaWiki", "mediawiki"),
    show("MediaWiki, title, attributes, fields", "mediawiki", title="Cities",
         attributes=[["class", "wikitable sortable"], ["style", "width: 50%"]], fields=["City name"]),
    show("MediaWiki, no header", "mediawiki", header=False),
    show("MediaWiki, fields matching nothing", "mediawiki", fields=[]),
]
for out in ["text", "html", "json", "csv", "latex", "mediawiki"]:
    export_ops.append({"op": "show", "say": f"get_formatted_string {out}", "fmt": "formatted", "out": out,
                       "kw": {"end": 2}})
job("exports", export_ops)

# ------------------------------------------------------------ pages, slices, copies

job("pages", cities() + [
    {"op": "show", "say": "paginate by 3", "fmt": "paginate", "page_length": 3},
    {"op": "show", "say": "paginate by 4, blank line between", "fmt": "paginate", "page_length": 4, "line_break": "\n\n"},
    {"op": "show", "say": "paginate by 2 from row 1 to 6", "fmt": "paginate", "page_length": 2, "kw": {"start": 1, "end": 6}},
    {"op": "show", "say": "paginate by 10", "fmt": "paginate", "page_length": 10},
    {"op": "slice", "to": "a", "lo": 1, "hi": 3},
    show("table[1:3]", t="a"),
    {"op": "slice", "to": "b", "lo": -2},
    show("table[-2:]", t="b"),
    {"op": "index", "to": "c", "i": 0},
    show("table[0]", t="c"),
    {"op": "index", "to": "c", "i": -1},
    show("table[-1]", t="c"),
    {"op": "index", "to": "c", "i": 10},
    {"op": "set_style", "style": "MARKDOWN"},
    {"op": "set", "attr": "title", "value": "Capitals"},
    {"op": "slice", "to": "d", "lo": 0, "hi": 2},
    show("a slice of a markdown table", t="d"),
    {"op": "copy", "to": "e"},
    {"op": "add_row", "t": "e", "row": ["Canberra", 814, 467194, 616.4]},
    {"op": "set", "t": "e", "attr": "title", "value": "Capitals and Canberra"},
    show("a copy, with a row added", t="e"),
    show("the original"),
])

# ------------------------------------------------------------ table factories

put("procs.csv", (
    "PID;USER;%CPU;%MEM;COMMAND\n"
    "1;root;0.0;0.1;/sbin/init\n"
    "412;postgres;3.2;4.5;postgres: checkpointer\n"
    "877;www-data;12.5;2.1;nginx: worker process\n"
    "878;www-data;11.9;2.0;nginx: worker process\n"
    "1203;app;48.0;18.3;python3 -m gunicorn app:wsgi\n"
    "1204;app;47.5;18.1;python3 -m gunicorn app:wsgi\n"
    "2210;redis;1.1;0.9;redis-server *:6379\n"
    "3301;root;0.3;0.2;sshd: admin [priv]\n"
    "3302;admin;0.0;0.1;-bash\n"
    "4410;app;5.4;1.2;celery worker --concurrency=4\n"
    "5120;root;0.1;0.0;cron -f\n"
))
put("ports.csv", (
    "service,port,proto\r\n"
    "ssh, 22, tcp\r\n"
    "\"http, alt\", 8080, tcp\r\n"
    "dns, 53, udp\r\n"
))
put("tsv.txt", "name\tsize\tmodified\nREADME.md\t2048\t2024-05-01\nsetup.py\t512\t2024-04-12\n")
put("inventory.html", """<html><body>
<h1>Fleet</h1>
<table class="hosts">
  <tr><th>Host</th><th>Role</th><th>Role</th><th>Zone</th></tr>
  <tr><td> web-1 </td><td>frontend</td><td>nginx</td><td>eu-west-1a</td></tr>
  <tr><td>web-2</td><td>frontend</td><td>nginx</td><td>eu-west-1b</td></tr>
  <tr><td>db-1</td><td colspan="2">postgres primary</td><td>eu-west-1a</td></tr>
  <tr><td>cache-1</td><td>redis</td></tr>
</table>
<p>Volumes</p>
<table>
  <thead><tr><th>Volume</th><th>Size &amp; type</th></tr></thead>
  <tbody>
  <tr><td>vol-01</td><td>100 GiB gp3</td></tr>
  <tr><td>vol-02</td><td>2&nbsp;TiB st1</td></tr>
  </tbody>
</table>
</body></html>
""")
put("fleet.html", open(os.path.join(DATA, "inventory.html"), encoding="utf-8").read().replace(
    "<td>cache-1</td><td>redis</td>", "<td>cache-1</td><td>redis</td><td>redis 7</td><td>eu-west-1c</td>"))
put("one.html", "<table><tr><th>a</th><th>b</th></tr><tr><td>1</td><td>2</td></tr></table>")
put("wiki.txt", """Some text before the table.
{| class="wikitable"
|+ Releases
|-
! Version !! Date !! Notes
|-
| 3.16.0 || 2025-03-24 || Python 3.14 support
|-
| 3.15.1 || 2025-02-24 ||  fixes
|-
|   3.15.0||2025-02-23||new styles
|}
Text after.
""")

job("factories", [
    {"op": "from_csv", "file": "procs.csv"},
    show("from_csv, dialect sniffed"),
    {"op": "get", "attr": "rows"},
    {"op": "from_csv", "file": "ports.csv"},
    show("from_csv, quotes and spaces sniffed"),
    {"op": "from_csv", "file": "ports.csv", "kw": {"delimiter": ","}},
    show("from_csv, delimiter given, so nothing is sniffed"),
    {"op": "from_csv", "file": "ports.csv", "kw": {"skipinitialspace": True, "title": "Ports"}},
    show("from_csv, skipinitialspace, a title for the table"),
    {"op": "from_csv", "file": "tsv.txt", "field_names": ["File", "Bytes", "Date"]},
    show("from_csv with field names given"),
    {"op": "from_csv", "file": "tsv.txt", "kw": {"delimiter": "\t", "align": "l"}},
    show("from_csv, tabs, align l"),
    {"op": "from_json", "text": "[[\"k\", \"v\"], {\"k\": \"x\", \"v\": 1.50}, {\"v\": [1, 2], \"k\": null}]"},
    show("from_json"),
    {"op": "from_json", "text": "[[\"k\", \"v\"], {\"k\": \"x\"}]"},
    {"op": "from_json", "text": "[]"},
    {"op": "from_html", "t": "h", "file": "inventory.html"},
    {"op": "from_html", "t": "h", "file": "fleet.html"},
    show("the first HTML table", t="h0"),
    show("the second HTML table", t="h1"),
    {"op": "get", "t": "h0", "attr": "field_names"},
    {"op": "from_html_one", "file": "inventory.html"},
    {"op": "from_html_one", "file": "one.html", "kw": {"border": False}},
    show("from_html_one, border off"),
    {"op": "from_mediawiki", "file": "wiki.txt"},
    show("from_mediawiki"),
    {"op": "get", "attr": "rows"},
    {"op": "from_mediawiki", "text": "{|\n|-\n| a || b\n|}"},
    {"op": "from_mediawiki", "text": "{|\n! a !! b\n|-\n| 1 || 2 || 3\n|}"},
    {"op": "from_mediawiki", "text": "{|\n! a !! a\n|}"},
    {"op": "new", "t": "r"},
    {"op": "add_rows", "t": "r", "rows": [["x", 1], ["y", 2.5]]},
    {"op": "show", "t": "r", "say": "round trip through JSON", "fmt": "json"},
])

# ------------------------------------------------------------ ColorTable

color_ops = [{"op": "new", "cls": "ColorTable", "field_names": ["Name", "Score"]},
             {"op": "add_rows", "rows": [["Ada", 98], ["Linus", 87]]}]
for th in ["DEFAULT", "OCEAN", "HIGH_CONTRAST", "EARTH"]:
    color_ops.append({"op": "theme", "name": th})
    color_ops.append(show(f"ColorTable theme {th}"))
color_ops += [
    {"op": "theme", "name": "OCEAN"},
    text("ocean, title", title="Scores"),
    text("ocean, hrules ALL", hrules="ALL"),
    text("ocean, no header", header=False),
    {"op": "custom_theme", "kw": {"default_color": "  ", "vertical_char": "!", "vertical_color": "\x1b[35m",
                                  "horizontal_char": "~", "junction_char": "*", "junction_color": "1;32"}},
    show("a custom theme"),
    {"op": "set_style", "style": "ORGMODE"},
    show("a custom theme in orgmode"),
    {"op": "set_style", "style": "SINGLE_BORDER"},
    show("single border style over a theme"),
    {"op": "show", "say": "ColorTable HTML", "fmt": "html"},
]
job("colortable", color_ops)

# ------------------------------------------------------------ the module's own demo

demo = cities(divider=True)
for s in STYLES:
    demo.append({"op": "set_style", "style": s})
    demo.append(show(f"PrettyTable style: {s}"))
demo += [{"op": "new", "t": "c", "cls": "ColorTable", "field_names": CITIES}]
for row in CITY_ROWS:
    op = {"op": "add_row", "t": "c", "row": row}
    if row[0] == "Hobart":
        op["divider"] = True
    demo.append(op)
for th in ["DEFAULT", "DYSLEXIA_FRIENDLY", "EARTH", "GLARE_REDUCTION", "HIGH_CONTRAST", "LAVENDER",
           "OCEAN", "OCEAN_DEEP", "PASTEL"]:
    demo.append({"op": "theme", "t": "c", "name": th})
    demo.append(show(f"ColorTable theme: {th}", t="c"))
job("demo", demo)

# ------------------------------------------------------------ programs

# A top-like view of a process list exported from ps.
job("top", [
    {"op": "from_csv", "file": "procs.csv", "kw": {"title": "Top processes by CPU"}},
    {"op": "set", "attr": "align", "value": "r"},
    {"op": "set_key", "attr": "align", "key": "USER", "value": "l"},
    {"op": "set_key", "attr": "align", "key": "COMMAND", "value": "l"},
    {"op": "set_key", "attr": "max_width", "key": "COMMAND", "value": 22},
    text("top 5 by %CPU", sortby="%CPU", sort_key="number", reversesort=True, end=5),
    text("app user only", row_filter=["eq", 1, "app"], fields=["PID", "%CPU", "%MEM", "COMMAND"]),
    {"op": "show", "say": "as a CSV report", "fmt": "csv", "kw": {"sortby": "PID", "sort_key": "number", "fields": ["PID", "USER", "%CPU"]}},
])

# A df-like disk report for a status page, in Markdown.
job("disk report", [
    {"op": "new", "field_names": ["Mount", "Size", "Used", "Use%", "Device"],
     "kw": {"custom_format": {"Size": "kib", "Used": "kib"}}},
    {"op": "add_rows", "rows": [
        ["/", 41943040, 20971520, 0.5, "/dev/nvme0n1p2"],
        ["/boot", 1048576, 262144, 0.25, "/dev/nvme0n1p1"],
        ["/var/lib/postgresql", 524288000, 498073600, 0.95, "/dev/nvme1n1"],
        ["/tmp", 8388608, 0, 0.0, "tmpfs"],
    ]},
    {"op": "set_key", "attr": "custom_format", "key": "Use%", "value": "percent"},
    {"op": "set_style", "style": "MARKDOWN"},
    {"op": "set", "attr": "align", "value": "r"},
    {"op": "set_key", "attr": "align", "key": "Mount", "value": "l"},
    {"op": "set_key", "attr": "align", "key": "Device", "value": "l"},
    text("disk usage, fullest first", sortby="Use%", reversesort=True),
    text("over 40%", row_filter=["gt", 3, 0.4], fields=["Mount", "Use%"]),
])

# A test summary: results come in as prettytable's own JSON and are
# shown per suite with dividers.
results = [["suite", "test", "result", "ms"]]
for suite, tests in [("api", [("test_login", "PASS", 41), ("test_logout", "PASS", 12), ("test_refresh", "FAIL", 230)]),
                     ("db", [("test_migrate", "PASS", 1830), ("test_rollback", "SKIP", 0)]),
                     ("ui", [("test_render", "PASS", 95), ("test_a11y", "XFAIL", 64), ("test_dark_mode", "PASS", 77)])]:
    for name, res, ms in tests:
        results.append({"suite": suite, "test": name, "result": res, "ms": ms})
put("results.json", json.dumps(results, indent=2) + "\n")

job("test summary", [
    {"op": "from_json", "file": "results.json", "kw": {"title": "pytest -q summary"}},
    {"op": "set_style", "style": "SINGLE_BORDER"},
    {"op": "set_key", "attr": "align", "key": "test", "value": "l"},
    {"op": "set_key", "attr": "align", "key": "ms", "value": "r"},
    {"op": "set", "attr": "int_format", "value": "5"},
    show("all results"),
    text("failures", row_filter=["eq", 2, "FAIL"]),
    text("slowest first", sortby="ms", reversesort=True, end=3),
    {"op": "show", "say": "two per page", "fmt": "paginate", "page_length": 2, "line_break": "\n-- page --\n",
     "kw": {"fields": ["test", "result"], "end": 5}},
])

# A host inventory scraped from an HTML page and published to a wiki.
job("inventory", [
    {"op": "from_html", "t": "h", "file": "fleet.html"},
    {"op": "set_style", "t": "h0", "style": "DOUBLE_BORDER"},
    show("hosts", t="h0"),
    {"op": "show", "t": "h0", "say": "hosts for the wiki", "fmt": "mediawiki", "kw": {"title": "Fleet", "fields": ["Host", "Zone"]}},
    {"op": "show", "t": "h1", "say": "volumes for the runbook", "fmt": "latex", "kw": {"format": True, "hrules": "ALL"}},
    {"op": "show", "t": "h1", "say": "volumes, formatted HTML", "fmt": "html", "kw": {"format": True, "attributes": [["id", "volumes"]]}},
])

# A dependency audit for a pull request comment: long notes wrapped,
# every row ruled, package names as terminal hyperlinks.
job("dependency audit", [
    {"op": "new", "field_names": ["Package", "From", "To", "Notes"],
     "kw": {"hrules": "ALL", "max_width": 28, "align": "l", "title": "pip-audit and outdated packages"}},
    {"op": "add_rows", "rows": [
        ["requests", "2.31.0", "2.32.3", "Fixes CVE-2024-35195: verify=False persisted across a session's later requests."],
        ["urllib3", "1.26.18", "2.2.2", "Major version: drops OpenSSL < 1.1.1 and the deprecated strict parameter."],
        ["jinja2", "3.1.3", "3.1.4", "Security: xmlattr filter accepted keys with spaces (CVE-2024-34064)."],
        ["idna", "3.6", "3.7", "Denial of service on crafted inputs to encode()."],
    ]},
    show("the audit"),
    {"op": "set_key", "attr": "custom_format", "key": "Package", "value": "link"},
    {"op": "set_key", "attr": "valign", "key": "Package", "value": "m"},
    show("with hyperlinked names"),
    {"op": "set_key", "attr": "custom_format", "key": "Notes", "value": "red"},
    text("security fixes in red", row_filter=["has", 3, "CVE"]),
])

# An invoice in the terminal, with a total row under a divider.
job("invoice", [
    {"op": "new", "field_names": ["Item", "Qty", "Unit", "Amount"],
     "kw": {"custom_format": {"Unit": "money", "Amount": "money"}, "min_table_width": 60,
            "title": "Invoice 2024-0193", "align": "r"}},
    {"op": "set_key", "attr": "align", "key": "Item", "value": "l"},
    {"op": "add_row", "row": ["Hosting, 12 months", 12, 49.0, 588.0]},
    {"op": "add_row", "row": ["Support hours", 7, 95.5, 668.5]},
    {"op": "add_row", "row": ["Domain renewal", 2, 12.99, 25.98], "divider": True},
    {"op": "add_row", "row": ["Total", "", "", 1282.48]},
    show("invoice"),
    {"op": "set", "attr": "custom_format", "value": {"Unit": "money", "Amount": "money", "Item": "lines"}},
    {"op": "set", "attr": "valign", "value": "m"},
    show("items split over lines"),
    show("as HTML for the email", "html", format=True),
])

with open(os.path.join(DATA, "jobs.jsonl"), "w", encoding="utf-8") as f:
    for j in JOBS:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
print(sum(len(j["ops"]) for j in JOBS), "operations in", len(JOBS), "jobs")
