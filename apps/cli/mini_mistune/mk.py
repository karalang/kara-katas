# Writes data/: a small documentation site (Markdown pages with
# directives, includes, tables, footnotes and the rest), a file of short
# Markdown cases, and data/jobs.txt, the list of runs mini_mistune makes:
# - `config NAME key=value ...` names a Markdown instance: the renderer
#   (html, markdown, rst or ast), escape, hard_wrap, the plugins, and the
#   directive styles with their directive plugins;
# - `cases FILE CONFIG...` renders each case of FILE under each config;
# - `site CONFIG DIR OUT` builds the pages under DIR into OUT;
# - `links CONFIG DIR` checks the links of the pages under DIR;
# - `cli ARG...` runs `python -m mistune` with those arguments (tab
#   separated).
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def write(rel, text):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


CASES = []


def case(title, text):
    CASES.append((title, text))


# ------------------------------------------------------------ blocks

case("atx headings", "# one\n## two ##\n### three #  \n####### seven\n#hash\n#\n### ###\n")
case("atx closing", "# foo#\n## foo \\#\n### b ## ##  \n")
case("setext", "Title\n=====\n\nSub *title*\n---\n\n  Indented\n  ===\n")
case("setext no paragraph", "---\n\n===\n")
case("thematic breaks", "***\n---\n___\n * * *\n- - -\n_ _ _ _\n**\n")
case("indented code", "    a simple\n      indented code block\n\n    chunk2\n\n\n\n    chunk3\n")
case("indented code in paragraph", "Foo\n    bar\n")
case("tab code", "\tfoo\tbaz\t\tbim\n  \tbar\n")
case("fenced code", "```python\ndef f(x):\n    return x * 2\n```\n\n~~~\n<tag> & more\n~~~~\n")
case("fenced info with backtick", "``` aa `\nfoo\n```\n")
case("fenced indented", "   ```\n   aaa\n    aaa\n  aaa\n   ```\n")
case("fenced unclosed", "````\naaa\n```\n")
case("fenced escaped info", "```\\{x\\} attrs\nbody\n```\n")
case("block quote", "> # Foo\n> bar\n> baz\n")
case("block quote lazy", "> bar\nbaz\n> foo\n\nafter\n")
case("block quote nested", "> > > deep\n> > two\n> one\n")
case("block quote code", ">     code\n>\n>     more\n")
case("block quote break", "> a\n---\n> b\n- list\n")
case("lists simple", "- one\n- two\n- three\n")
case("lists loose", "- a\n\n- b\n- c\n")
case("lists ordered", "3. three\n4. four\n\n1) paren\n2) next\n")
case("lists nested", "- a\n  - b\n    - c\n      - d\n- e\n")
case("lists with code", "1. item\n\n       code\n\n2. next\n")
case("lists marker change", "- a\n+ b\n* c\n")
case("lists interrupt", "para\n- item\n\npara\n2. no\n\npara\n1. yes\n")
case("lists empty item", "-\n  foo\n-\n- bar\n")
case("lists blank start", "-\n\n  foo\n")
case("lists continuation", "- first line\ncontinued lazily\n\n  second paragraph\n- next\n")
case("lists with quote", "- > quoted\n  > more\n- plain\n")
case("lists deep", "1. a\n   1. b\n      1. c\n         1. d\n            1. e\n               1. f\n                  1. g\n")
case("html blocks", "<div>\n*not md*\n</div>\n\n<!-- a comment\nstill -->\nafter\n\n<?php echo 1; ?>\n\n<!DOCTYPE html>\n\n<![CDATA[\nx < y\n]]>\n")
case("html pre", "<pre>\n**raw**\n\n</pre>\nafter\n")
case("html rule 7", "<custom-tag a=\"1\">\n*md*\n\n</custom-tag>\n\npara <span>\n<span>\n")
case("html close", "</div>\nok\n\n</section>\n")
case("ref links", "[foo]: /url \"title\"\n[Bar]: <my url> 'other'\n[baz]:\n/next\n\n[foo] [bar][] [Baz][bar] [missing]\n")
case("ref link titles", "[a]: /a\n\"title on next line\"\n[b]: /b \"broken\n\n[a] [b]\n")
case("ref link first wins", "[x]: /first\n[X]: /second\n\n[x]\n")
case("ref link inside paragraph", "para\n[x]: /u\n\n[x]\n")
case("paragraphs", "aaa\n\nbbb\n  ccc\n\n   ddd\n")
case("blank lines", "\n\n  \naaa\n  \n\n# heading\n\n")

# ------------------------------------------------------------ inlines

case("escapes", "\\*not emph\\* \\_x\\_ \\` \\# \\\\ \\a \\[link\\]\n")
case("code spans", "`code` `` a`b `` ` x ` `  ` ``unterminated\nmulti\nline` `a\nb`\n")
case("emphasis", "*a* _b_ **c** __d__ ***e*** ___f___ *nested **strong** inside*\n")
case("emphasis edge", "a * b * c\nsnake_case_word\n*foo*bar\n**unclosed\n_a_b_\n")
case("emphasis escaped", "*a\\*b* **c\\*\\*d**\n")
case("links", "[text](/url \"title\") [empty]() [angle](<a b>) ![img](/i.png 'T') [esc](/a\\)b)\n")
case("links nested", "[outer [inner] text](/u) [a [b](/x) c](/y) ![img [x](/l)](/i)\n")
case("links titles", "[a](/u \"t \\\"q\\\"\") [b](/u 'single') [c](/u (paren))\n")
case("links precedence", "[not a `link](/u)` here] *a `*` b* [x <http://a.b/>](/c)\n")
case("autolinks", "<https://example.com/path?q=1&r=2> <mailto:me@x.org> <me@example.com> <not auto> <a+b:c>\n")
case("inline html", "a <span class=\"x\">b</span> <!-- c --> <?pi?> <![CDATA[d]]> <a href=\"/q\">[in](/link)</a>\n")
case("entities", "&amp; &copy; &#35; &#x22; &nbsp;x &bogus; &ampxyz; &#0; &#xD800; &#1114112; &Auml\n")
case("line breaks", "hard  \nbreak\nsoft\nback\\\nslash\n")
case("urls in text", "visit https://example.com/a_b. or http://x.y/(z) now\n")
case("unicode", "*ünïcödé* — “quotes” [ссылка](/путь) `код`\n")

# ------------------------------------------------------------ plugins

case("strikethrough", "~~gone~~ ~~not closed ~ ~~a\\~~b~~\n")
case("mark insert", "==marked== ^^inserted^^ ==a\\==b==\n")
case("sup sub", "2^10^ is 1024, H~2~O, a^b\\ c^\n")
case("table", "| a | b | c |\n|:--|:-:|--:|\n| 1 | 2 | 3 |\n| x \\| y | `z` | **w** |\n")
case("table mismatch", "| a | b |\n|---|\n| 1 | 2 |\n")
case("nptable", "a | b\n--|--\n1 | 2\n3 | 4\n")
case("footnotes", "Text[^1] and more[^note] and [^1] again, [^missing].\n\n[^1]: First note.\n[^note]: A longer note\n    with a second line.\n\n    And a paragraph.\n")
case("task lists", "- [ ] todo\n- [x] done\n- [X] also\n- [y] not a task\n\n1. [ ] ordered\n")
case("def list", "Apple\n:   A fruit.\n\nOrange\n:   Citrus.\n:   Second definition\n    continued.\n\nTerm\n\n: loose\n")
case("abbr", "The HTML spec is by the W3C.\n\n*[HTML]: Hyper Text Markup Language\n*[W3C]:  World Wide Web Consortium\n")
case("math", "Inline $a^2 + b^2$ and $ not$.\n\n$$\n\\int_0^1 x\\,dx\n$$\n")
case("ruby", "[漢字(かんじ)] [東(ひがし)京(きょう)](/tokyo) [語(ご)][ref]\n\n[ref]: /ref\n")
case("spoiler", ">! hidden\n>! more\n\ninline >! secret !< text\n\n> normal\n")
case("url plugin", "see https://example.com/x, or <https://a.b> and [https://in.link](/u)\n")

# ------------------------------------------------------------ directives

case("admonitions", ".. note:: Read this\n   :class: wide\n\n   Body **text**.\n\n.. warning::\n\n   No title.\n\n.. unknown:: thing\n")
case("fenced directives", "```{tip} A tip\n:class: small\n\nInside the tip.\n```\n\n~~~{danger}\nCareful.\n~~~\n\n```{nope}\nx\n```\n")
case("image directive", ".. image:: /img/a.png\n   :alt: An image\n   :width: 100\n   :height: 50%\n   :align: center\n   :target: /big.png\n\n.. image:: /b.png\n   :align: sideways\n   :width: wide\n")
case("figure directive", ".. figure:: /fig.png\n   :figwidth: 80%\n   :figclass: framed\n   :align: left\n\n   The caption.\n\n   A legend paragraph.\n")
case("toc errors", ".. toc::\n   :min-level: 0\n\n.. toc::\n   :max-level: x\n\n.. toc::\n   :min-level: 3\n   :max-level: 2\n\n# heading\n")
case("toc", "# Intro\n\n.. toc:: Contents\n   :max-level: 2\n\n## Part *one*\n### Deep\n## Part two\n# End\n")

write("cases.md", "".join("%%% " + t + "\n" + s for t, s in CASES))

# ------------------------------------------------------------ the site

write("site/index.md", """\
# Lumen documentation

Lumen is a static site toolkit. This page is the entry point.

```{toc} On this page
:max-level: 2
```

## Getting started

```{include} guide/install.md
```

```{note} Before you begin
:class: tip-box

You need Python 3.8 or later. See [usage](guide/usage.md).
```

## Configuration

| Key | Default | Meaning |
|:----|:-------:|--------:|
| `title` | *none* | Site title |
| `theme` | `plain` | Theme name |
| `out` | `site/` | Output folder |

The defaults are fine for most sites.[^defaults]

[^defaults]: They follow the conventions of other generators.

## Examples

```{include} snippets/example.py
```

```{include} snippets/banner.html
```

```{figure} /images/arch.png
:figwidth: 60%
:align: center

The build pipeline.
```

## Checklist

- [x] write pages
- [ ] add search
- [ ] publish

See the [API reference](api.md), the [changelog](changelog.md) and the
[missing page](guide/missing.md).
""")

write("site/guide/install.md", """\
Install Lumen with pip:

    pip install lumen

Then check the version:

```console
$ lumen --version
lumen 2.1.0
```
""")

write("site/guide/usage.md", """\
# Usage

```{toc}
```

## Build

Run `lumen build`. The output goes to `site/` by default; change it with
`--out`.

```{warning}
Building overwrites the output folder.
```

## Serve

Run `lumen serve` and open <http://localhost:8000/>.
Back to the [index](../index.md).

### Options

Term
:   Meaning of the term.

Port
:   The port to listen on, *8000* by default.

```{include} ../snippets/note.md
```

```{include} usage.md
```
""")

write("site/api.md", """\
API reference
=============

```{toc}
:min-level: 2
:max-level: 3
```

Build
-----

`build(src, out, *, theme=None)` renders every page under `src`.

### Arguments

* **src**: the source folder
* **out**: the output folder

Serve
-----

`serve(out, port=8000)` serves `out` over HTTP.

> **Note**: the server is for previews only.
> Use a real web server in production.

Math: $O(n \\log n)$ for *n* pages, with the bound

$$
T(n) = 2T(n/2) + n
$$

*[HTTP]: Hypertext Transfer Protocol
""")

write("site/changelog.md", """\
# Changelog

## 2.1.0

- Added ~~themes~~ ==theme packs==.
- Fixed H~2~O rendering, 2^10^ pages.
- Faster builds [^speed].

## 2.0.0

1. Rewrote the core.
2. Dropped Python 3.7.

---

Older releases: see <https://example.com/lumen/history>.

[^speed]: About 40% faster on large sites.
""")

write("site/snippets/example.py", """\
from lumen import build

build("docs", "site")
""")

write("site/snippets/banner.html", """\
<div class="banner">Lumen <b>2.1</b></div>
""")

write("site/snippets/note.md", """\
> Included note: *see also* the [api](../api.md).
""")

write("cli/README.md", """\
Project **Kite**
================

A *tiny* tool. Install: `pip install kite`.

| a | b |
|---|---|
| 1 | 2 |

~~old~~ new[^1]

[^1]: A note.
""")

write("cli/notes.txt", "line one  \nline two\n\n- a\n- b\n")

write("jobs.txt", """\
# mini_mistune jobs: configs, then the runs that use them.
config html renderer=html escape=0 plugins=strikethrough,footnotes,table,speedup
config safe renderer=html escape=1
config wrap renderer=html escape=0 hard_wrap=1 plugins=speedup
config full renderer=html escape=0 plugins=strikethrough,mark,insert,superscript,subscript,footnotes,table,url,abbr,def_list,math,ruby,task_lists,spoiler rst=admonition,toc,image,figure fenced=admonition,include
config md renderer=markdown
config rst renderer=rst
config ast renderer=ast plugins=table,footnotes,task_lists
config docs renderer=html escape=0 plugins=strikethrough,mark,superscript,subscript,footnotes,table,url,abbr,def_list,math,task_lists fenced=admonition,toc,include,image,figure
cases cases.md html safe wrap full md rst ast
site docs site out
links docs site
cli -m\tHi **Markdown**
cli -m\t# Title\\n\\nText with <b>html</b>\t--escape
cli -f\tdata/cli/README.md
cli -f\tdata/cli/README.md\t-r\trst
cli -f\tdata/cli/README.md\t-r\tmarkdown\t-p\ttable
cli -f\tdata/cli/notes.txt\t--hardwrap\t-o\tdata/out/notes.html
cli -f\tdata/cli/README.md\t-p\tstrikethrough\tfootnotes\t-p\ttable\t-o\tdata/out/readme.html
cli -m\t- [ ] a\\n- [x] b\t-p\ttask_lists\t-r\tast
cli --version
cli -r\thtml
""")
