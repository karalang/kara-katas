# Prints expected.out: runs data/jobs.txt through mistune itself (the
# copy in mistune/, unchanged), the way mini_mistune.kara runs it through
# its port.
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
os.chdir(HERE)

import mistune  # noqa: E402
import mistune.__main__ as cli_main  # noqa: E402
from mistune.directives import (  # noqa: E402
    Admonition, FencedDirective, Figure, Image, Include, RSTDirective,
    TableOfContents,
)
from mistune.renderers.markdown import MarkdownRenderer  # noqa: E402
from mistune.renderers.rst import RSTRenderer  # noqa: E402
from mistune.toc import add_toc_hook, render_toc_ul  # noqa: E402
from mistune.util import striptags  # noqa: E402

out = sys.stdout

DIRECTIVES = {
    "admonition": Admonition,
    "toc": TableOfContents,
    "include": Include,
    "image": Image,
    "figure": Figure,
}


def make(cfg):
    renderer = cfg.get("renderer", "html")
    if renderer == "markdown":
        renderer = MarkdownRenderer()
    elif renderer == "rst":
        renderer = RSTRenderer()
    plugins = [p for p in cfg.get("plugins", "").split(",") if p]
    md = mistune.create_markdown(
        escape=cfg.get("escape", "1") == "1",
        hard_wrap=cfg.get("hard_wrap", "0") == "1",
        renderer=renderer,
        plugins=plugins,
    )
    for style, cls in (("rst", RSTDirective), ("fenced", FencedDirective)):
        names = [n for n in cfg.get(style, "").split(",") if n]
        if names:
            md.use(cls([DIRECTIVES[n]() for n in names]))
    return md


def show(result):
    if isinstance(result, list):
        out.write(json.dumps(result) + "\n")
        return
    out.write(result)
    if not result.endswith("\n"):
        out.write("\\ no newline\n")


def failure(e):
    return "error: " + type(e).__name__ + ": " + str(e) + "\n"


def read_cases(path):
    cases = []
    with open(path, encoding="utf-8", newline="") as f:
        for line in f.read().split("\n")[:-1]:
            if line.startswith("%%% "):
                cases.append([line[4:], ""])
            else:
                cases[-1][1] += line + "\n"
    return cases


def run_cases(configs, args):
    cases = read_cases(os.path.join("data", args[0]))
    for name in args[1:]:
        md = make(configs[name])
        for title, text in cases:
            out.write("== " + title + " [" + name + "]\n")
            try:
                show(md(text))
            except Exception as e:
                out.write(failure(e))


def pages(top):
    found = []
    for root, dirs, files in os.walk(top):
        for f in files:
            if f.endswith(".md"):
                found.append(os.path.join(root, f))
    return sorted(found)


def walk_links(tokens, found):
    for tok in tokens:
        if tok["type"] in ("link", "image"):
            found.append((tok["type"], tok["attrs"]["url"]))
        if "children" in tok:
            walk_links(tok["children"], found)


def run_site(configs, args):
    cfg, top, dest = configs[args[0]], os.path.join("data", args[1]), os.path.join("data", args[2])
    for path in pages(top):
        md = make(cfg)
        add_toc_hook(md, 1, 2)
        html, state = md.read(path)
        heads = [t for t in state.tokens if t["type"] == "heading"]
        if heads:
            title = striptags(md.renderer.render_tokens(heads[0]["children"], state))
        else:
            title = os.path.basename(path)
        rel = os.path.relpath(path, top)
        target = os.path.join(dest, rel[:-3] + ".html")
        os.makedirs(os.path.dirname(target), exist_ok=True)
        page = ("<!doctype html>\n<title>" + title + "</title>\n<nav>\n"
                + render_toc_ul(state.env["toc_items"]) + "</nav>\n<main>\n"
                + html + "</main>\n")
        with open(target, "w", encoding="utf-8") as f:
            f.write(page)
        with open(target, encoding="utf-8") as f:
            back = f.read()
        out.write("== page " + rel + " -> " + target + " (" + str(len(back.encode("utf-8"))) + " bytes, "
                  + str(len(heads)) + " headings)\n")
        show(back)


def run_links(configs, args):
    cfg, top = configs[args[0]], os.path.join("data", args[1])
    for path in pages(top):
        md = make(cfg)
        html, state = md.read(path)
        found = []
        walk_links(state.tokens, found)
        out.write("== links " + os.path.relpath(path, top) + ": " + str(len(found)) + "\n")
        for kind, url in found:
            if "://" in url or url.startswith(("/", "#", "mailto:")):
                verdict = "external"
            else:
                target = os.path.normpath(os.path.join(os.path.dirname(path), url))
                verdict = "ok" if os.path.isfile(target) else "MISSING " + target
            out.write("  " + kind + " " + url + " " + verdict + "\n")


def run_cli(argv):
    out.write("== cli " + " ".join(argv) + "\n")
    out.flush()
    sys.argv = ["mistune"] + argv
    cli_main.read_stdin = lambda: None
    code = 0
    try:
        cli_main.cli()
    except SystemExit as e:
        code = e.code
    except Exception as e:
        out.write(failure(e))
        code = 1
    out.write("[exit " + str(code) + "]\n")
    if "-o" in argv:
        path = argv[argv.index("-o") + 1]
        with open(path, encoding="utf-8") as f:
            text = f.read()
        out.write("-- " + path + "\n")
        show(text)


def main():
    configs = {}
    with open("data/jobs.txt", encoding="utf-8") as f:
        lines = f.read().split("\n")
    for line in lines:
        if not line or line.startswith("#"):
            continue
        kind, _, rest = line.partition(" ")
        if kind == "config":
            words = rest.split(" ")
            configs[words[0]] = dict(w.split("=", 1) for w in words[1:])
        elif kind == "cases":
            run_cases(configs, rest.split(" "))
        elif kind == "site":
            run_site(configs, rest.split(" "))
        elif kind == "links":
            run_links(configs, rest.split(" "))
        elif kind == "cli":
            run_cli([a.replace("\\n", "\n") for a in rest.split("\t")])


main()
