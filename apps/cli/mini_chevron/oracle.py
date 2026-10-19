# Runs data/cases.txt and the site jobs through chevron 0.14.0 (the copy
# in chevron/, unchanged) and wrote expected.out. A case calls
# chevron.render with its template, its JSON data, its partials and
# warn=True; a job calls chevron.main.main, the function behind the
# `chevron` command, on files under data/. Each prints the warnings
# chevron writes to stderr, then the output or the error.
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.modules["yaml"] = None  # chevron.main loads data with PyYAML when it can; the port reads JSON

import chevron  # noqa: E402
cli = sys.modules["chevron.main"]  # the package exports the function main under the module's name

# (name, template, data, partials path, partials extension, left and right delimiter, warn)
JOBS = [
    ("nginx", "site/nginx/nginx.conf.mustache", "site/nginx/sites.json", "site/nginx/partials", "mustache", "{{", "}}", True),
    ("nginx without data", "site/nginx/nginx.conf.mustache", None, "site/nowhere", "mustache", "{{", "}}", False),
    ("email", "site/email/order.html.mustache", "site/email/order.json", "site/email", "html", "{{", "}}", True),
    ("k8s", "site/k8s/deployment.yaml.mustache", "site/k8s/values.json", "site/k8s", "tpl", "{{", "}}", True),
    ("ci", "site/ci/workflow.yml.tmpl", "site/ci/ci.json", "site/ci", "", "<%", "%>", True),
    ("broken", "site/broken/page.mustache", "site/broken/page.json", ".", "mustache", "{{", "}}", True),
]


def parse_cases(text):
    cases = []
    cur = None
    block = None
    for line in text.split("\n"):
        if line.startswith("=== "):
            cur = {"name": line[4:], "template": "", "data": "{}", "partials": {}, "delims": None}
            cases.append(cur)
            block = None
        elif cur is None:
            continue
        elif line.startswith("~~~ "):
            block = [line[4:], []]
            cur.setdefault("blocks", []).append(block)
        elif block is not None:
            block[1].append(line)
    for c in cases:
        for kind, lines in c.pop("blocks", []):
            body = "\n".join(lines)
            if kind == "template":
                c["template"] = body
            elif kind == "data":
                c["data"] = body
            elif kind == "delimiters":
                c["delims"] = body.split(" ")
            elif kind.startswith("partial "):
                c["partials"][kind[8:]] = body
    return cases


def show(out, err, exc):
    for line in err.getvalue().split("\n")[:-1]:
        print(f"  ? {line}")
    if exc is not None:
        lines = str(exc).split("\n")
        print(f"  ! {type(exc).__name__}: {lines[0]}")
        for line in lines[1:]:
            print(f"  !   {line}")
    else:
        for line in out.split("\n"):
            print("  |" + line.replace("\r", "\\r"))


def run(fn):
    err = io.StringIO()
    old = sys.stderr
    sys.stderr = err
    out, exc = None, None
    try:
        out = fn()
    except (SyntaxError, IndexError, TypeError) as e:
        exc = e
    finally:
        sys.stderr = old
    show(out, err, exc)


def main():
    os.chdir(os.path.join(HERE, "data"))
    with open("cases.txt", encoding="utf-8", newline="") as f:
        cases = parse_cases(f.read())
    for c in cases:
        print(f"== {c['name']}")
        data = json.loads(c["data"])
        ldel, rdel = c["delims"] or ("{{", "}}")
        run(lambda: chevron.render(template=c["template"], data=data, partials_path=None,
                                   partials_dict=c["partials"], warn=True, def_ldel=ldel, def_rdel=rdel))
    for name, template, data, ppath, pext, ldel, rdel, warn in JOBS:
        print(f"== job: {name}")
        run(lambda: cli.main(template, data, partials_path=ppath, partials_ext=pext,
                             def_ldel=ldel, def_rdel=rdel, warn=warn))


main()
