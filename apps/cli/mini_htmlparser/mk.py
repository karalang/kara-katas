#!/usr/bin/env python3
"""Writes data/ for mini_htmlparser: six HTML pages and the jobs."""
import os

os.makedirs("data/pages", exist_ok=True)

PAGES = {}

PAGES["blog.html"] = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Caf&eacute; notes &mdash; Week 12 &amp; more</title>
  <meta name="description" content="What we roasted, brewed &amp; broke this week.">
  <link rel="stylesheet" href="/css/site.css?v=3&amp;theme=dark">
  <link rel="alternate" type="application/rss+xml" href="/feed.xml">
  <style>
    body > p { margin: 0 }  /* a > in CSS is not a tag */
  </style>
  <script>
    if (a < b && c > d) { document.write("</div>"); }
    var s = '<p>not a tag</p>';
  </script>
</head>
<body>
<nav><a href="/">Home</a> | <a href="/archive/" title="All posts">Archive</a> | <a href=/about>About</a></nav>
<!-- main article starts here -->
<article>
<h1 id="week-12">Week 12: the new grinder</h1>
<p>We finally replaced the old burr grinder&#8230; and the espresso is <em>much</em> better.
Prices went up 5&nbsp;% (sorry). See <a href="https://example.com/grind?size=fine&amp;unit=um">the
grind chart</a>.</p>
<h2 id="beans">Beans</h2>
<ul>
  <li>Ethiopia Guji &ndash; 18&nbsp;g in, 36&nbsp;g out</li>
  <li>Colombia Huila &lt;sold out&gt;</li>
</ul>
<img src="/img/grinder.jpg" alt="The new grinder &quot;Mk II&quot;" width=640 height=480>
<h2 id="recipes">Recipes</h2>
<h3 id="v60">V60</h3>
<pre><code>15 g coffee
250 g water at 94&deg;C</code></pre>
<p>Questions? <a href="mailto:hello@example.com">Write to us</a>.<br/>
Or ring the bell.</p>
</article>
<footer><p>&copy; 2026 Caf&eacute; Example &middot; <a href="/privacy">Privacy</a></p></footer>
</body>
</html>
"""

PAGES["edge.html"] = """\
<!doctype html>
<p class=a id='b' hidden data-x = "1 > 0" DATA-Y=Two>Mixed &amp attrs</p>
<!---->
<!-->abrupt
<!--->abrupt too
<!-- ends with bang --!>
<!-- has -- inside -->
<!not a doctype>
<![CDATA[x < y]]>
<?php echo "hi"; ?>
</ >
</>
</3>
<br/><br /><img src="a.png"/>
<a href=x/>bare slash</a>
<DIV CLASS="Up">Upper</DIV>
<i>&ampx &notit; &notin; &#128; &#0; &#x110000; &#xD800; &#65&#x42; &bogus;</i>
<b title="&ampx &notit; &copy=3 &lt;&#62;">attr refs</b>
<script>if (x </scriptx> y) {}</script >
<textarea name=t>a <b>bold</b> &amp; </textarea>
< not a tag
&# and &#x and & alone
<span>last
<a b='unclosed>text here
"""

PAGES["form.html"] = """\
<form action="/search" method=get>
<label for=q>Search</label>
<input type="text" name="q" value="&quot;exact phrase&quot;" autofocus>
<select name="sort"><option value=new selected>Newest<option value=old>Oldest</select>
<input type=checkbox name=safe checked disabled>
<button type="submit" onclick="go('/search?q=1&amp;page=2')">Go</button>
</form>
<title>Search &amp; find</title>
"""

PAGES["plain.html"] = """\
<p>Before</p>
<plaintext>
<b>after plaintext everything is text</b> &amp; </plaintext>
"""

PAGES["comment.html"] = """\
<p>Thanks for the <b>great</b> post!</p>
<script>alert('xss')</script>
<p onclick="steal()">Check <a href="javascript:alert(1)">this</a> and
<a href="https://good.example/page?a=1&amp;b=2" title="Good &quot;site&quot;" target=_blank>that</a>.</p>
<img src=x onerror=alert(2)>
<style>body{display:none}</style>
<ul><li>one<li>two</ul>
<i>caf&eacute; &lt;3</i> <code>a < b</code>
<iframe src="https://evil.example/"></iframe>
<p>Bye</p>
"""

PAGES["unicode.html"] = """\
<h1 id="intro">Grüße aus Köln 🍺</h1>
<p>Zwei Zeilen:
ä ö ü — und <b>ß</b>.</p>
<h2 id="mehr">Mehr &rarr; Info</h2>
<p>日本語のテキスト &amp; <a href="/ja/">リンク</a></p>
"""

for name, text in PAGES.items():
    with open(os.path.join("data/pages", name), "w", encoding="utf-8") as f:
        f.write(text)

JOBS = []
# The event stream, whole and in chunks, with and without convert_charrefs.
for page in ["edge.html", "form.html", "plain.html", "unicode.html"]:
    JOBS.append("events\t@%s\t1\t0" % page)
JOBS.append("events\t@edge.html\t0\t0")
JOBS.append("events\t@edge.html\t1\t7")
JOBS.append("events\t@edge.html\t0\t1")
JOBS.append("events\t@unicode.html\t1\t5")
JOBS.append("events\t@blog.html\t1\t64")
# Small inline documents; \\n stands for a newline.
for src in [
    "<a href=\"x\">link</a>",
    "a &amp b &amp; c &#x26; d",
    "&amp",
    "&am",
    "x &#38",
    "x &#",
    "<b",
    "<b class='x",
    "</b",
    "<!-- open",
    "<!-- open --",
    "<!doctype html",
    "<?pi",
    "<![CDATA[open",
    "<!bogus",
    "</ bogus",
    "<",
    "a<",
    "<script>x</script",
    "<title>t &amp; u",
    "<p>line1\\nline2<br>\\n<i>three</i>",
]:
    JOBS.append("events\t%s\t1\t0" % src)
    JOBS.append("events\t%s\t0\t0" % src)
# html.unescape and html.escape.
for s in [
    "fish &amp; chips", "&lt;tag&gt;", "&ampx &amp;x", "&notit; &notin; &not",
    "&#65;&#x42;&#X43;", "&#0; &#13; &#128; &#150; &#159;", "&#x110000; &#xD800; &#xFFFE; &#1;",
    "&#99999999999999999999;", "&bogus; & &; &#; &#x;", "&AMP; &Amp; &QUOT;",
    "&centerdot; &cent &centx", "&ThickSpace; &NotEqualTilde; &fjlig;",
    "&eacutex &Eacute;", "no refs at all", "&&amp;&&",
]:
    JOBS.append("unescape\t%s" % s)
for s, q in [("<a href=\"x\">'hi' & bye</a>", "1"), ("<a href=\"x\">'hi' & bye</a>", "0"),
             ("&amp; already", "1"), ("plain", "1")]:
    JOBS.append("escape\t%s\t%s" % (s, q))
# Programs over the pages.
for page in ["blog.html", "edge.html", "form.html", "comment.html"]:
    JOBS.append("links\t@%s" % page)
for page in ["blog.html", "comment.html", "unicode.html", "plain.html"]:
    JOBS.append("text\t@%s" % page)
for page in ["blog.html", "unicode.html", "edge.html"]:
    JOBS.append("toc\t@%s" % page)
for page in ["comment.html", "blog.html", "edge.html"]:
    JOBS.append("sanitize\t@%s" % page)

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    for j in JOBS:
        f.write(j + "\n")
