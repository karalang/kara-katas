# Writes data/jobs.tsv, the operations oracle.py and mini_webcolors.kara
# run, and data/site.css, the stylesheet the audit job reads.
#
# A line of jobs.tsv is an operation and its arguments, separated by tabs,
# with \t, \n and \\ escaped; "== name" starts a job.
import os
import random

rng = random.Random(125)


def esc(s):
    return s.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n")


lines = []


def job(name):
    lines.append("== " + name)


def op(*args):
    lines.append("\t".join(esc(str(a)) for a in args))


SPECS = ["html4", "css2", "css21", "css3"]

# ---------------------------------------------------------------- names
job("names")
for s in SPECS + ["CSS3", "svg"]:
    op("names", s)
for n in ["white", "Navy", "GOLDENROD", "orange", "rebeccapurple", "grey",
          "DarkSlateGrey", "cyan", "magenta", "aqua", "fuchsia", " red",
          "", "transparent", "lightgoldenrodyellow"]:
    for s in ["css3", "css21", "html4"]:
        op("name_to_hex", n, s)
for n in ["teal", "Silver", "orange", "PapayaWhip", "nosuch"]:
    op("name_to_rgb", n, "css3")
    op("name_to_rgb_percent", n, "css3")
op("name_to_hex", "white", "css1")
op("name_to_rgb", "orange", "css2")

# ---------------------------------------------------------------- hex
job("hex")
for h in ["#0099cc", "#0099CC", "#09c", "#09C", "#0099gg", "0099cc", "#",
          "#1234", "#12345", "#1234567", "#FFF", "#ffffff", "#aBcDeF",
          "#00ffff", "#ff00ff", "#808080", "#d3d3d3", "#663399", " #fff",
          "#fff\n", "#ＡＢＣ", "#a9a9a9"]:
    op("normalize_hex", h)
    for s in ["css3", "html4"]:
        op("hex_to_name", h, s)
    op("hex_to_rgb", h)
    op("hex_to_rgb_percent", h)
op("hex_to_name", "#ffa500", "css21")
op("hex_to_name", "#ffa500", "css2")
op("hex_to_name", "#fff", "CSS21")

# ---------------------------------------------------------------- rgb
job("rgb")
for t in [(255, 255, 255), (0, 0, 128), (218, 165, 32), (270, -20, -0),
          (1, 2, 3), (128, 64, 32), (16, 255, 0), (300, 300, 300),
          (-1, -1, -1), (102, 51, 153), (0, 255, 255), (192, 192, 192),
          (127, 129, 254), (250, 235, 215), (1000000, 7, 8)]:
    op("normalize_integer_triplet", *t)
    op("rgb_to_hex", *t)
    op("rgb_to_rgb_percent", *t)
    for s in ["css3", "html4"]:
        op("rgb_to_name", *t, s)
for v in range(0, 256, 3):
    op("html5_serialize_simple_color", v, 255 - v, (v * 7) % 256)

# ---------------------------------------------------------------- percent
job("percent")
pts = [("50%", "50%", "50%"), ("0%", "100%", "0%"), ("-10%", "-0%", "500%"),
       ("85.49%", "64.71%", "12.5%"), ("100%", "100%", "0%"),
       ("12.5%", "6.25%", "25%"), ("33.3%", "66.6%", "99.9%"),
       ("1e2%", "0%", "0%"), ("1.e2%", "0%", "0%"), (" 7 %", "+5%", "007%"),
       ("1_0%", "2_0.5%", "3%"), ("nan.%", "0%", "0%"), ("inf.%", "-inf.%", "0%"),
       ("abc%", "0%", "0%"), ("5", "10", "15"), ("0.5%", "0.25%", "0.125%"),
       ("99.99999%", "100.00001%", "-0.0%"), ("1.%", ".5%", "50.%"),
       ("0.19607843%", "0.2%", "0.21%"), ("%", "0%", "0%"),
       ("20%x", "0%", "0%"), ("1.5e1%", "2.5E1%", "3.5e-1%"),
       ("50.0%", "50.00%", "49.99%"), ("0.1%", "0.2%", "0.3%")]
for t in pts:
    op("normalize_percent_triplet", *t)
    op("rgb_percent_to_rgb", *t)
    op("rgb_percent_to_hex", *t)
    op("rgb_percent_to_name", *t, "css3")
for k in range(40):
    t = tuple(f"{rng.uniform(-5, 105):.{rng.randrange(0, 5)}f}%" for _ in range(3))
    op("rgb_percent_to_rgb", *t)

# ---------------------------------------------------------------- roundtrip
job("roundtrip")
op("percent_roundtrip")
for s in SPECS:
    op("name_roundtrip", s)

# ---------------------------------------------------------------- html5
job("html5")
for v in ["#ffffff", "#fff", "ffffff7", "#fffffg", "#FfEeDd", "#000000",
          "#ＡＢＣＤＥＦ", "", "#1234567"]:
    op("html5_parse_simple_color", v)
legacy = ["black", "chucknorris", "Window", "transparent", " Transparent ",
          "", "   ", "#fff", "#FFF", "#ffff", "#abcdef", "#1", "#12", "#123",
          "red", "  LightGoldenrodYellow\n", "#0099cc", "0099cc", "crap",
          "ninjaturtle", "sick", "grass", "#ff0000ff", "#12345678",
          "#123456789abcdef0", "rgb(10, 20, 30)", "hsl(0, 100%, 50%)",
          "😀😀😀", "a😀b", "#😀", "zzzzzz", "00000000000000000001",
          "0000ff000000ff000000ff", "#" + "a" * 200, "x" * 129 + "fff",
          "\u3000blue\u3000", "\u00a0white", "\x1cred\x1f", "cyan\u0085",
          "1", "12", "1234", "12345", "123456", "#abc ", "#a b c"]
for v in legacy:
    op("html5_parse_legacy_color", v)
alphabet = "0123456789abcdefABCDEF#xyz ghij-+.%😀é\u00a0"
for k in range(60):
    n = rng.randrange(1, 40)
    op("html5_parse_legacy_color", "".join(rng.choice(alphabet) for _ in range(n)))

# ---------------------------------------------------------------- audit
job("audit")
op("audit", "site.css")

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

CSS = """/* Main stylesheet for the shop front. */
:root {
  --brand: #3366CC;
  --accent: rgb(255, 102, 0);
}

body {
  color: #333;
  background-color: White;
  font-family: Georgia, serif;
}

header, .masthead {
  color: rgb(255, 255, 255);
  background-color: var(--brand);
  background: #3366cc url(header.png) no-repeat;
  border-bottom: 3px solid #224488;
}

nav a {
  color: navy;
  background-color: #f0f0f0;
}

nav a:hover {
  color: rgb(100%, 40%, 0%);
  background-color: #FFFFF0;
  text-decoration: underline;
}

.button-primary {
  color: #fff;
  background-color: rgb(51, 102, 204);
  border: 1px solid DarkSlateGrey;
}

.button-muted {
  color: silver;
  background-color: whitesmoke;
}

.alert-warning {
  color: #8a6d3b;
  background-color: #FCF8E3;
  border-color: #faebcc;
}

.alert-danger {
  color: rgb(169,68,66);
  background-color: rgb(242, 222, 222);
  outline: 2px dashed crimson;
}

.price {
  color: rgb(85.49%, 64.71%, 12.5%);
  background-color: black;
}

.sale-banner {
  color: yellow;
  background-color: #ff0;
}

footer {
  color: GRAY;
  background-color: #222;
  border-top: 1px solid rgb(300, -20, 128);
}

.legal {
  color: #777777;
  background-color: #333333;
  font-size: 0.75em;
}

.badge {
  color: Teal;
  background-color: #e0f2f1;
  border: thin dotted #0099cc;
}

.code {
  color: rebeccapurple;
  background-color: oldlace;
  fill: #ABCDEF;
  stroke: rgb(18, 52, 86);
}

.oops {
  color: #ggg;
  background-color: notacolor;
  border-color: #12345;
}
"""
with open("data/site.css", "w", encoding="utf-8") as f:
    f.write(CSS)
