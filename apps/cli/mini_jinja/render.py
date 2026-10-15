# The oracle: renders the same templates with Jinja2 and prints what
# mini_jinja.kara prints. Run from this directory: python3 render.py
import json, os, jinja2

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader("templates"),
    autoescape=jinja2.select_autoescape(enabled_extensions=("html",), default_for_string=True),
    trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=True)

with open("data/site.json") as f:
    data = json.load(f)
published = [p for p in data["posts"] if not p["draft"]]

def emit(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)
    print(f"== {path} ({len(text.encode())} bytes)")
    print(text, end="")

emit("out/index.html", env.get_template("index.html").render(**data))
for i, p in enumerate(published):
    ctx = dict(data, post=p, posts=published, index=i)
    emit(f"out/{p['slug']}/index.html", env.get_template("post.html").render(**ctx))
emit("out/digest.txt", env.get_template("digest.txt").render(**data))

print("== errors")
cases = [
    "{% for x in xs %}{{ x }}",
    "{{ x|nosuch }}",
    "{{ missing.attr }}",
    "a\n{% endif %}",
    "{{ 1 / zero }}",
    "{% if x %}\n{% for y in x %}\n{% endif %}",
    "{{ x + }}",
    "{% macro m(a) %}{{ a }}{% endmacro %}{{ m(1, 2) }}",
    "<{{ x.y.z }}>",
    "{{ '<b>' ~ x.y }} {{ '<b>'|safe ~ x.y }}",
]
for c in cases:
    try:
        out = env.from_string(c).render(xs=[1], x={"y": 1}, zero=0)
        print(f"ok: {out}")
    except Exception as e:
        msg = getattr(e, "message", None) or str(e)
        line = getattr(e, "lineno", None)
        where = f" (line {line})" if line is not None else ""
        print(f"error: {type(e).__name__}: {msg}{where}")
