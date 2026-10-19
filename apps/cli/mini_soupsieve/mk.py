#!/usr/bin/env python3
"""Writes data/: the HTML pages under data/pages and data/jobs.tsv.

A job is one line of tab-separated fields. In a field, "⏎" stands for a
newline, "⇥" for a tab, "␣" for a space and "∅" for the empty string;
"␀", "␁", "␉" and "␡" stand for U+0000, U+0001, U+0009 and U+007F.
"-" in a scope or element field means the document itself; a number is
the index of a tag in document order.
"""
import os

PAGES = {}

PAGES["shop.html"] = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Trail running shoes | Northpeak Outfitters</title>
  <link rel="stylesheet  preload" href="/css/site.css">
  <link rel="canonical" href="https://shop.example/c/trail-running">
  <link rel="alternate" hreflang="de" href="https://shop.example/de/c/trail-running">
</head>
<body class="catalog  theme-dark">
<header id="top">
  <nav aria-label="Main">
    <ul class="menu">
      <li><a href="/" class="logo">Northpeak</a></li>
      <li class="active"><a href="/c/running">Running</a></li>
      <li><a href="/c/hiking">Hiking</a></li>
      <li><a href="/c/sale" class="sale hot">Sale</a></li>
      <li><a>Stores</a></li>
    </ul>
  </nav>
  <form id="search" action="/search" role="search">
    <input type="search" name="q" placeholder="Search products">
    <button type="submit">Go</button>
  </form>
</header>
<main>
  <h1>Trail running shoes <small>(6 products)</small></h1>
  <ul class="breadcrumb"><li><a href="/">Home</a></li><li><a href="/c/running">Running</a></li><li aria-current="page">Trail</li></ul>
  <section class="grid" data-columns="3">
    <article class="product card" data-sku="NP-1001" data-price="129.95" data-rating="4.6">
      <h2 class="title"><a href="/p/np-1001">Ridgeback 3</a></h2>
      <p class="price"><span class="currency">$</span>129.95</p>
      <ul class="tags"><li>waterproof</li><li>wide fit</li></ul>
      <button class="add" data-action="cart-add">Add to cart</button>
    </article>
    <article class="product card featured" data-sku="NP-1002" data-price="99.00" data-rating="4.1">
      <h2 class="title"><a href="/p/np-1002">Scree Dancer</a></h2>
      <p class="price"><del>$119.00</del> <ins>$99.00</ins></p>
      <ul class="tags"><li>lightweight</li></ul>
      <button class="add" data-action="cart-add">Add to cart</button>
    </article>
    <article class="product card sold-out" data-sku="NP-1003" data-price="149.50">
      <h2 class="title"><a href="/p/np-1003">Moraine GTX</a></h2>
      <p class="price"><span class="currency">$</span>149.50</p>
      <p class="stock">Sold out</p>
      <button class="add" disabled data-action="notify">Notify me</button>
    </article>
    <article class="product card" data-sku="NP-1004" data-price="89.99" data-rating="3.8">
      <h2 class="title"><a href="/p/np-1004">Talus Trainer</a></h2>
      <p class="price"><span class="currency">$</span>89.99</p>
      <ul class="tags"></ul>
      <button class="add" data-action="cart-add">Add to cart</button>
    </article>
    <article class="product card featured" data-sku="NP-1005" data-price="179.00" data-rating="4.9">
      <h2 class="title"><a href="/p/np-1005" title="New for spring">Cirque Pro</a></h2>
      <p class="price"><span class="currency">$</span>179.00</p>
      <ul class="tags"><li>carbon plate</li><li>race</li><li>waterproof</li></ul>
      <button class="add" data-action="cart-add">Add to cart</button>
    </article>
    <article class="product card" data-sku="np-1006" data-price="64.00" data-rating="">
      <h2 class="title"><a href="/p/np-1006">Kids' Scout</a></h2>
      <p class="price"><span class="currency">$</span>64.00</p>
      <button class="add" data-action="cart-add">Add to cart</button>
    </article>
  </section>
  <nav class="pagination" aria-label="Pages">
    <a href="?page=1" rel="prev">&laquo; Prev</a>
    <a href="?page=1">1</a>
    <a href="?page=2" aria-current="page" class="current">2</a>
    <a href="?page=3">3</a>
    <a href="?page=3" rel="next nofollow">Next &raquo;</a>
  </nav>
</main>
<footer>
  <p>&copy; 2024 Northpeak Outfitters &middot; <a href="/privacy">Privacy</a> &middot; <a href="/terms" lang="en-GB">Terms</a></p>
  <!-- footer links rendered by cms -->
</footer>
</body>
</html>
"""

PAGES["signup.html"] = """<!DOCTYPE html>
<html lang="en">
<head><title>Create your account</title></head>
<body>
<form id="signup" action="/signup" method="post">
  <fieldset id="who">
    <legend>About you</legend>
    <label>Name <input type="text" name="name" required placeholder="Ada Lovelace"></label>
    <label>Email <input type="email" name="email" required placeholder="you@example.com" value="ada@example.com"></label>
    <label>Password <input type="password" name="password" required minlength="12" placeholder=""></label>
    <label>Phone <input type="tel" name="phone" placeholder="+1 555 0100"></label>
    <label>Website <input type="url" name="site"></label>
    <label>Bio <textarea name="bio" placeholder="A line or two"></textarea></label>
    <label>Notes <textarea name="notes" placeholder="Anything else">
</textarea></label>
    <label>Signature <textarea name="sig" placeholder="Shown under posts">Ada</textarea></label>
    <input type="hidden" name="csrf" value="tok-7f3a" disabled>
  </fieldset>
  <fieldset id="prefs">
    <legend>Preferences</legend>
    <label><input type="checkbox" name="news" checked> Newsletter</label>
    <label><input type="checkbox" name="offers"> Offers</label>
    <label><input type="checkbox" name="beta" indeterminate> Beta features</label>
    <p>Plan:
      <label><input type="radio" name="plan" value="free" checked> Free</label>
      <label><input type="radio" name="plan" value="pro"> Pro</label>
    </p>
    <p>Theme:
      <label><input type="radio" name="theme" value="light"> Light</label>
      <label><input type="radio" name="theme" value="dark"> Dark</label>
    </p>
    <label><input type="radio" name=""> Unnamed</label>
    <label><input type="radio"> No name</label>
    <select name="country">
      <optgroup label="Europe">
        <option value="de">Germany</option>
        <option value="fr" selected>France</option>
      </optgroup>
      <optgroup label="Elsewhere" disabled>
        <option value="jp">Japan</option>
      </optgroup>
    </select>
    <progress></progress>
    <progress value="40" max="100"></progress>
  </fieldset>
  <fieldset id="billing" disabled>
    <legend>Billing <input type="checkbox" name="same-as-shipping"></legend>
    <label>Card <input type="text" name="card" inputmode="numeric"></label>
    <div><label>Expires <input type="month" name="exp" min="2024-01" max="2030-12" value="2023-11"></label></div>
    <button type="button">Check card</button>
  </fieldset>
  <fieldset id="schedule">
    <legend>Delivery</legend>
    <input type="date" name="day" min="2024-03-01" max="2024-03-31" value="2024-03-15">
    <input type="date" name="late" min="2024-03-01" max="2024-03-31" value="2024-04-02">
    <input type="date" name="bad" min="2024-03-01" max="2024-03-31" value="2024-02-30">
    <input type="date" name="leap" min="2024-02-01" max="2024-02-29" value="2024-02-29">
    <input type="time" name="slot" min="09:00" max="17:30" value="18:15">
    <input type="time" name="night" min="22:00" max="06:00" value="23:30">
    <input type="time" name="noon" min="22:00" max="06:00" value="12:00">
    <input type="week" name="wk" min="2020-W01" max="2020-W53" value="2020-W53">
    <input type="week" name="wk2" min="2021-W01" max="2021-W53" value="2021-W10">
    <input type="datetime-local" name="at" min="2024-03-01T08:00" max="2024-03-01T20:00" value="2024-03-01T07:59">
    <input type="number" name="qty" min="1" max="10" value="12">
    <input type="number" name="tip" min="0" max=".5" value="0.25">
    <input type="number" name="free" value="7">
    <input type="range" name="vol" min="-10" max="10" value="-11">
    <input type="number" name="neg" min="-3.5" value="-4">
    <input type="number" name="junk" min="abc" max="" value="5">
  </fieldset>
  <p contenteditable>Click to add a note.</p>
  <p contenteditable="TRUE">Also editable.</p>
  <p contenteditable="false">Not editable.</p>
  <input type="text" name="code" readonly value="ABC-123">
  <details open><summary>Terms</summary><p>By signing up you agree.</p></details>
  <details><summary>Privacy</summary><p>We keep your email.</p></details>
  <button type="reset">Clear</button>
  <button type="submit" name="go">Create account</button>
  <input type="submit" value="Create and verify">
</form>
<form id="lone"><input type="radio" name="solo"><button>Plain</button></form>
<dialog open><p>Saved.</p></dialog>
<video src="/intro.mp4" muted></video>
<audio src="/ping.mp3"></audio>
</body>
</html>
"""

PAGES["article.html"] = """<!DOCTYPE html>
<html lang="en-US">
<head>
  <meta http-equiv="content-language" content="en-US">
  <title>Bridging three scripts</title>
</head>
<body>
<article id="main" dir="auto">
  <h1>Bridging three scripts</h1>
  <p class="lead">Interfaces that mix left-to-right and right-to-left text need care.</p>
  <p lang="de-CH" id="ch">Grüezi mitenand, das ist Schweizerdeutsch.</p>
  <p lang="de-DE-1996" id="de96">Alte Rechtschreibung.</p>
  <p lang="de-Latn-DE" id="latn">Mit Schrift-Subtag.</p>
  <p lang="fr" id="fr">Bonjour <span lang="">tout</span> le monde.</p>
  <p lang="zh-Hant-TW" id="tw">繁體中文</p>
  <p lang="i-klingon" id="tlh">nuqneH</p>
  <p lang="x-private-use" id="priv">Private.</p>
  <blockquote dir="rtl" id="quote">
    <p id="ar">مرحبا بالعالم</p>
    <p id="mixed"><bdi>abc</bdi> שלום</p>
  </blockquote>
  <div dir="auto" id="auto-he">  שלום עולם</div>
  <div dir="auto" id="auto-en"><!-- note --> 42 Hello</div>
  <div dir="auto" id="auto-none">12345 !!!</div>
  <div dir="ltr" id="ltr-box"><span id="inner">inherit me</span><div dir="RTL" id="upper-rtl">שלום</div></div>
  <p><input type="text" dir="auto" id="in-he" value="שלום"><input type="text" dir="auto" id="in-en" value="hi"><input type="text" dir="auto" id="in-empty" value=""><input type="tel" id="phone"></p>
  <textarea dir="auto" id="ta">مرحبا</textarea>
  <bdi id="bdi-ar">عربي</bdi><bdi id="bdi-en">english</bdi>
  <section>
    <h2>Embedded</h2>
    <iframe src="/widget"><html><body><p id="in-frame" lang="ja">埋め込み</p></body></html></iframe>
    <p>After the frame.</p>
  </section>
  <ul id="steps">
    <li>one</li>
    <li class="x">two</li>
    <li>three</li>
    <li class="x">four</li>
    <li>five</li>
    <li class="x">six</li>
    <li>seven</li>
  </ul>
  <p>Contains <b>bold <i>nested</i></b> text and <code>code</code>.</p>
  <p>Comment <!-- hidden words --> here.</p>
  <p class="empty"></p>
  <p class="empty"> <!-- c --> </p>
  <p class="empty">
  </p>
  <p class="empty"><span></span></p>
</article>
</body>
</html>
"""

PAGES["report.html"] = """<html>
<head><title>Q3 latency report</title></head>
<body>
<table id="latency">
  <caption>p99 latency by service (ms)</caption>
  <thead>
    <tr><th>Service</th><th>Region</th><th>Jul</th><th>Aug</th><th>Sep</th></tr>
  </thead>
  <tbody>
    <tr class="ok"><td>auth</td><td>eu-west</td><td>41</td><td>39</td><td>44</td></tr>
    <tr class="warn"><td>search</td><td>eu-west</td><td>180</td><td>210</td><td>205</td></tr>
    <tr class="ok"><td>cart</td><td>us-east</td><td>52</td><td>55</td><td>51</td></tr>
    <tr class="bad"><td>payments</td><td>us-east</td><td>390</td><td>420</td><td>515</td></tr>
    <tr class="ok"><td>images</td><td>ap-south</td><td>66</td><td>70</td><td>73</td></tr>
    <tr class="warn"><td>feeds</td><td>ap-south</td><td>150</td><td>149</td><td>160</td></tr>
  </tbody>
  <tfoot><tr><td colspan="2">median</td><td>59</td><td>62.5</td><td>62</td></tr></tfoot>
</table>
<h2>Incidents</h2>
<ol start="7">
  <li><time datetime="2024-07-04">Jul 4</time> <span class="sev sev-2">SEV-2</span> search reindex stalled</li>
  <li><time datetime="2024-08-19">Aug 19</time> <span class="sev sev-1">SEV-1</span> payments provider timeout</li>
  <li><time datetime="2024-09-02">Sep 2</time> <span class="sev">SEV-3</span> image CDN purge</li>
</ol>
<dl class="owners">
  <dt>auth</dt><dd>identity team</dd>
  <dt>search</dt><dt>feeds</dt><dd>discovery team</dd>
  <dt>payments</dt><dd>checkout team</dd><dd>on call: <a href="mailto:pay-oncall@example.com">pay-oncall</a></dd>
</dl>
<p>Generated <time>2024-10-01</time> by <a href="https://ci.example/job/481">job 481</a>.</p>
</body>
</html>
"""

PAGES["edge.html"] = """<!DOCTYPE html>
<?xml-stylesheet href="x.css"?>
<!-- top comment -->
<html>
<body>
<my-widget id="w1" data-state="ready"><slot-item>a</slot-item></my-widget>
<svg:rect id="r1" width="10"></svg:rect>
<x-y:z id="xyz"></x-y:z>
<div ID="Upper" Class="MiXed case" TITLE="Shout">Upper-case attribute names</div>
<div class=" pad  ded " id="pad">padded classes</div>
<div class="" id="noclass">empty class</div>
<div id="dup" class="a" class="b">duplicate class</div>
<div id="1st">id starts with a digit</div>
<div id="a.b" class="c:d">dots and colons</div>
<div id="uni" class="café naïve">accented</div>
<div id="emoji" data-mood="😀 happy">emoji</div>
<div id="nl" title="line one
line two">newline in a value</div>
<p id="ws">   </p>
<p id="cdata"><![CDATA[raw]]></p>
<p id="pi"><?php echo 1; ?></p>
<p id="decl"><!ELEMENT p ANY></p>
<span id="lonely"></span>
<div id="nest"><div><div><span class="deep">deep</span></div></div></div>
<a id="anchor-only" name="here"></a><a id="real-link" href="#here">link</a><area id="map-area" href="/x"><area id="dead-area">
<ul id="mixed"><li>1</li>text<li>2</li><!-- c --><li>3</li></ul>
<table id="t"><tr><td>x</td></tr></table>
<p lang="EN-us" id="caps-lang">Upper lang</p>
<div id="scope-root"><p class="s">one</p><div><p class="s">two</p></div></div>
</body>
</html>
"""

PAGES["fragment.html"] = """<p id="f1">First paragraph.</p>
<p id="f2" class="note">Second <em>paragraph</em>.</p>
<ul id="f3"><li>a</li><li>b</li></ul>
"""

PAGES["lonely.html"] = """<!-- a document with one element -->
<main id="only"><p id="kid">kid</p></main>
"""

CUSTOM_HEADINGS = ":--heading=h1, h2, h3, h4, h5, h6¦:--body-text=p:not(.lead)"
CUSTOM_NESTED = ":--a=:--b .x¦:--b=ul"
CUSTOM_LOOP = ":--a=:--b¦:--b=:--a"
CUSTOM_BADNAME = ":bad=div"
CUSTOM_DUP = ":--Head=h1¦:--head=h2"
CUSTOM_UNDEF = ":--a=:--nope"

NS_HTML = "html=http://www.w3.org/1999/xhtml"
NS_DEFAULT = "∅=http://www.w3.org/1999/xhtml¦svg=http://www.w3.org/2000/svg"
NS_OTHER = "∅=urn:other"

PARSE = [
    "div",
    "DIV.Product#Main",
    "*",
    "*|*",
    "|p",
    "ns|p",
    "a[href]",
    "a[href='/x']",
    'a[ href = "/x" i ]',
    "a[href^=https]",
    "a[href$='.pdf' s]",
    "a[href*=example]",
    "a[rel~=next]",
    "a[rel~='a b']",
    "[lang|=en]",
    "[data-x!=y]",
    "[title^='']",
    "[type=TEXT]",
    "[TYPE=text i]",
    "p:first-child:last-of-type",
    "li:nth-child(2n+1)",
    "li:nth-child(-n+3)",
    "li:nth-last-child(odd)",
    "li:NTH-OF-TYPE(  3  )",
    "li:nth-child(-2n - 4)",
    "li:nth-child(n)",
    "li:nth-child(+5)",
    "li:nth-child(2n+1 of .x, p)",
    "li:nth-last-of-type(even)",
    "div > p + ul ~ span",
    "div    p",
    "div /* c */ > /* d */ p",
    "a, b ,c",
    ":is(h1, h2) > a",
    ":is()",
    ":where(, .x)",
    ":not(.a, .b)",
    ":has(> img)",
    ":has(+ p, ~ ul)",
    "div:has(p span)",
    ":root",
    ":scope > p",
    "& > p",
    ":empty",
    ":defined",
    ":-soup-contains('a b', \"c\")",
    ":-soup-contains-own(x)",
    ":lang(de, '*-CH')",
    ":dir(rtl)",
    ":dir(LTR)",
    ":hover",
    ":host(div)",
    ":link",
    ":checked",
    ":disabled",
    "#\\31 23",
    ".a\\.b",
    "\\@foo",
    "#\\0 x",
    "[x='a\\⏎b']",
    "[x='\\41 BC']",
    "d\\69 v",
    "--custom-el",
    "my-widget[data-state]",
    "p⏎ ⇥> span",
    "  p  ",
    "/* only */ p /* tail */",
    "div:not(:not(p))",
]

BAD = [
    "",
    "div,",
    ",div",
    "div >",
    "> div",
    "div > > p",
    "div[",
    "div[x=]",
    "div[x='a]",
    "div.",
    "#",
    "div#",
    "::before",
    "p::first-line",
    "@page",
    ":unknown",
    ":nth-child(x)",
    ":nth-child",
    ":first-child(2)",
    ":not()",
    ":not(div",
    ":is(div))",
    ")",
    "div p)",
    ":has()",
    ":has(> )",
    "div span:has(",
    ":lang()",
    ":dir(up)",
    "div$",
    "a ! b",
    "p⏎> ⏎",
    "div⏎  p >⏎⏎  > span",
    "div\\",
    "p[a=b c]",
    "div span|",
    ":-soup-contains()",
    ":contains(x",
    "#\\110000",
    ":read-only" * 113,
]


def jobs():
    out = []

    def add(*fields):
        out.append("\t".join(fields))

    out.append("# parse")
    for s in PARSE:
        add("parse", s)
    out.append("# errors")
    for s in BAD:
        add("parse", s if s else "∅")
    out.append("# escape")
    for s in ["abc", "-", "-1x", "1x", "a b", "a.b#c", "∅", "␁z", "␡", "é", "--x", "_y", "a␀b", "1", "-a", "a1-_", "a␉b"]:
        add("escape", s)

    shop = [
        ".product",
        "article.product.featured",
        ".card:not(.sold-out)",
        "[data-sku^=NP]",
        "[data-sku^=np i]",
        "[data-sku$=6]",
        "[data-rating]",
        "[data-rating='']",
        "[data-rating^='']",
        "[data-price*='.9']",
        ".product:has(ins)",
        ".product:has(> ul.tags > li)",
        ".product:not(:has(.tags li))",
        ".tags:empty",
        ".tags > li:only-child",
        ".tags > li:first-child",
        ".tags > li:last-child:not(:first-child)",
        "article:nth-child(2n)",
        "article:nth-of-type(3n+1)",
        "article:nth-last-child(-n+2)",
        ".grid > :nth-child(2 of .featured)",
        ".grid > :nth-child(1 of :not(.featured))",
        "h2 > a[title]",
        "a[href^='/c/']",
        "a:not([href])",
        "a[rel~=next]",
        "a[rel~=nofollow]",
        "link[rel~=preload]",
        "link[rel='stylesheet preload']",
        "[class='catalog theme-dark']",
        "body.catalog",
        "a[aria-current=page], li[aria-current=page]",
        ".pagination a.current ~ a",
        ".pagination a.current + a",
        ".pagination a ~ a[rel]",
        "li.active + li",
        "header nav li a.sale.hot",
        ":is(.sale, .logo)",
        ":where(header, footer) a",
        "button:disabled",
        "button:enabled",
        "button[data-action=cart-add]:not(:disabled)",
        "input:placeholder-shown",
        ":link",
        ":any-link:not(.logo)",
        ":root",
        "html",
        ":root > body",
        "main h1 small",
        "del + ins",
        ".price:-soup-contains('149')",
        ".product:-soup-contains(waterproof)",
        "li:-soup-contains-own(wide)",
        "li:-soup-contains(Sale)",
        "h1:-soup-contains-own('6 products')",
        "h1:-soup-contains('6 products')",
        ":lang(en)",
        ":lang(en-GB)",
        "a:lang('*-GB')",
        "head > *",
        "*:not(li) > a",
        "footer a:last-of-type",
        "p:has(+ ul.tags), p:has(~ p.stock)",
        ".grid > article:first-of-type .title",
        "section[data-columns='3'] > *",
        ":is(h1, h2):has(a)",
        "h2:not(:has(a[title]))",
        "article > :is(p, ul):nth-child(3)",
        "html|a",
        "svg|a",
        "ns|a",
        "|a",
        "* > html",
        ":not(body) > :root",
        "* > * > * > body",
    ]
    out.append("# shop.html")
    for s in shop:
        add("select", "shop.html", "-", "0", s, "-", "-")
    add("select", "shop.html", "-", "3", ".product", "-", "-")
    add("select", "shop.html", "-", "1", ".featured .title a", "-", "-")
    add("select", "shop.html", "-", "0", "html|a.sale", NS_HTML, "-")
    add("select", "shop.html", "-", "0", "a.logo", NS_DEFAULT, "-")
    add("select", "shop.html", "-", "0", "svg|*", NS_DEFAULT, "-")
    add("select", "shop.html", "-", "0", "a.logo", NS_OTHER, "-")
    add("select", "shop.html", "-", "0", "*|a.logo", NS_OTHER, "-")
    add("select", "shop.html", "-", "0", ":--heading", "-", CUSTOM_HEADINGS)
    add("select", "shop.html", "-", "0", "article :--body-text", "-", CUSTOM_HEADINGS)
    add("select", "shop.html", "-", "0", ":--b > li", "-", CUSTOM_NESTED)
    add("helper", "shop.html", "-", ":--heading", CUSTOM_HEADINGS)
    add("one", "shop.html", "-", ".product.featured")
    add("one", "shop.html", "-", ".nothing-here")
    add("one", "shop.html", "-", "a[rel]")
    add("attr", "shop.html", ".product:not(.sold-out)", "data-sku")
    add("attr", "shop.html", ".product[data-rating]:not([data-rating=''])", "data-rating")
    add("attr", "shop.html", ".title a", "href")
    add("attr", "shop.html", "link", "rel")
    add("attr", "shop.html", "a[rel]", "rel")

    out.append("# signup.html")
    signup = [
        ":checked",
        ":default",
        ":indeterminate",
        ":disabled",
        ":enabled",
        ":required",
        ":optional",
        ":placeholder-shown",
        ":read-write",
        ":read-only",
        "input:read-only",
        "p:read-write",
        ":in-range",
        ":out-of-range",
        ":open",
        ":muted",
        "input:not([type])",
        "input[type=CHECKBOX]",
        "input[type='Radio' s]",
        "[name='']",
        "[name]:not([name=''])",
        "fieldset:disabled legend input",
        "fieldset[disabled] > legend:first-of-type input",
        "optgroup:disabled option",
        "option:checked",
        "label:has(> input:checked)",
        "label:has(:required)",
        "textarea:placeholder-shown",
        "fieldset > legend:-soup-contains-own(Pref)",
        "form > button:last-of-type",
        "form#lone :default",
        "form#lone :indeterminate",
        ":is(input, button)[type=submit]",
        "input[type=hidden]",
        "progress:indeterminate",
        "#schedule > :nth-child(odd of :out-of-range)",
        "[contenteditable]",
        "details[open] > summary",
        ":root:has(dialog[open])",
        ":target, :hover, :focus, :visited",
        ":is(:hover, .x)",
        ":is(:hover, input):first-child",
        ":not(:hover)",
    ]
    for s in signup:
        add("select", "signup.html", "-", "0", s, "-", "-")
    add("match", "signup.html", "75", ":out-of-range")
    add("match", "signup.html", "75", ":in-range")
    add("closest", "signup.html", "75", "fieldset")
    add("closest", "signup.html", "75", "form > *")
    add("closest", "signup.html", "75", "body > *")
    add("closest", "signup.html", "75", "input")
    add("closest", "signup.html", "75", "table")
    add("filter", "signup.html", "-", "*")
    add("filter", "signup.html", "5", ":not(legend)")
    add("filter", "signup.html", "5", "label:has(input[required])")
    add("attr", "signup.html", ":out-of-range", "name")
    add("attr", "signup.html", ":in-range", "name")
    add("attr", "signup.html", "input:checked", "name")

    out.append("# article.html")
    article = [
        ":lang(en)",
        ":lang(en-US)",
        ":lang(de)",
        ":lang(de-CH)",
        ":lang(de-DE)",
        ":lang('*-DE')",
        ":lang('*-Latn')",
        ":lang(de-*-DE)",
        ":lang(\"de-*\")",
        ":lang(fr, zh)",
        ":lang(zh-TW)",
        ":lang(zh-Hant)",
        ":lang(i-klingon)",
        ":lang(x)",
        ":lang('')",
        ":lang(ja)",
        "p:lang('*')",
        ":dir(ltr)",
        ":dir(rtl)",
        "p:dir(rtl)",
        "div:dir(rtl)",
        "input:dir(rtl)",
        "input:dir(ltr)",
        "textarea:dir(rtl)",
        "bdi:dir(rtl)",
        "span:dir(ltr)",
        ":root",
        "iframe :root",
        "iframe p",
        "iframe > *",
        "section > p",
        "#steps > li:nth-child(3n)",
        "#steps > li:nth-child(n+3):nth-child(-n+5)",
        "#steps > li:nth-last-child(2n+1)",
        "#steps > li:nth-child(2 of .x)",
        "#steps > li:nth-last-child(1 of .x)",
        "#steps > li:nth-child(-n+3 of :not(.x))",
        "#steps > li:nth-child(0n+2)",
        "#steps > li:nth-child(-n)",
        "#steps > li:nth-child(n-2)",
        "#steps > li:nth-child(-3n+7)",
        "#steps > li:nth-of-type(-2n+5)",
        "#steps > li:nth-child(10)",
        "#steps > .x:nth-last-of-type(2)",
        "p:-soup-contains(nested)",
        "p:-soup-contains-own(nested)",
        "b:-soup-contains-own(bold)",
        "p:-soup-contains('hidden words')",
        "p:-soup-contains-own(here)",
        "p:-soup-contains(nested):-soup-contains-own(xt)",
        "p:-soup-contains(nested):-soup-contains-own(x)",
        "p:-soup-contains-own('Contains '):-soup-contains('Contains ')",
        "p:-soup-contains-own('Contains '):-soup-contains(Contains)",
        ":contains(Grüezi)",
        "p.empty:empty",
        "p:empty",
        ":empty:not(input, meta, p)",
        "blockquote > p:only-of-type",
        "blockquote > p:first-child:not(:last-child)",
        "article > p:has(> b > i)",
        "p:has(code):has(b)",
        "h1 ~ p[lang]:not([lang|=de])",
        "[lang|=de]",
        "[lang|='']",
        "[dir=auto]",
        "[dir=RTL]",
        "[dir=RTL i]",
        "[id*=auto-]",
        "[id$=-en]",
    ]
    for s in article:
        add("select", "article.html", "-", "0", s, "-", "-")
    add("select", "article.html", "16", "0", "p", "-", "-")
    add("select", "article.html", "16", "0", ":scope > p", "-", "-")
    add("select", "article.html", "16", "0", ":root", "-", "-")
    add("match", "article.html", "16", ":dir(ltr)")
    add("closest", "article.html", "42", "[lang]")
    add("closest", "article.html", "42", ":dir(ltr)")

    out.append("# report.html")
    report = [
        "tbody > tr:nth-child(odd) > td:first-child",
        "tr:not(.ok) > td:nth-child(5)",
        "tr.bad td:nth-last-child(-n+3)",
        "thead th:nth-of-type(n+3)",
        "td[colspan]",
        "tfoot td:not([colspan])",
        "table > *",
        "caption + thead",
        "tbody tr:has(> td:-soup-contains-own(eu-west))",
        "tr:has(td:-soup-contains(ap)) + tr",
        "li:has(.sev-1) time",
        ".sev:not([class~=sev-1]):not([class~=sev-2])",
        "[class|=sev]",
        "time[datetime^='2024-0']",
        "time:not([datetime])",
        "dl.owners > dt + dd",
        "dl.owners > dt ~ dt",
        "dl.owners > dd + dd",
        "dt:-soup-contains(search) ~ dd",
        "ol[start] > li:nth-child(2)",
        "a[href^=mailto]",
        ":root body > p > a",
        "td:nth-child(3):-soup-contains-own('5')",
        ":is(th, td):nth-child(1):not(:has(*))",
    ]
    for s in report:
        add("select", "report.html", "-", "0", s, "-", "-")
    add("attr", "report.html", "tr.warn > td:first-child, tr.bad > td:first-child", "class")
    add("filter", "report.html", "13", "tr.ok")

    out.append("# edge.html")
    edge = [
        ":root",
        ":defined",
        ":not(:defined)",
        "my-widget",
        "MY-WIDGET",
        "slot-item",
        "svg\\:rect",
        "[id=r1]",
        "x-y\\:z",
        "#Upper",
        "[id=upper]",
        "[ID=Upper]",
        "div[class~=mixed]",
        "div[class~=MiXed]",
        "div[class~=mixed i]",
        ".MiXed.case",
        "[title=shout i]",
        ".pad.ded",
        "[class='pad ded']",
        "[class=' pad  ded ']",
        "[class]",
        "[class='']",
        "#dup",
        "#dup.b",
        "#dup.a",
        "#\\31 st",
        "[id='1st']",
        "#a\\.b",
        ".c\\:d",
        ".café",
        ".naïve",
        "[data-mood~=happy]",
        "[data-mood*='😀']",
        "[title*='one\\a line']",
        "[title$='two']",
        "[title~=one]",
        "#ws:empty",
        "#cdata:empty",
        "#pi:empty",
        "#decl:empty",
        "#lonely:empty",
        "#mixed > li:nth-child(2)",
        "#mixed > li:nth-of-type(3)",
        "#mixed > li:last-child",
        "#mixed > :not(li)",
        "#nest div",
        "#nest > div > div > span.deep",
        "#nest span:only-child",
        ":link",
        ":any-link",
        "a:not(:link)",
        "area:not(:any-link)",
        "td",
        "tbody",
        "table > tr",
        ":lang(en-US)",
        ":lang(EN)",
        "#scope-root .s",
        "body > :last-child .s",
    ]
    for s in edge:
        add("select", "edge.html", "-", "0", s, "-", "-")
    add("select", "edge.html", "-", "0", ":--a", "-", CUSTOM_LOOP)
    add("select", "edge.html", "-", "0", "p", "-", CUSTOM_BADNAME)
    add("select", "edge.html", "-", "0", "p", "-", CUSTOM_DUP)
    add("select", "edge.html", "-", "0", ":--a", "-", CUSTOM_UNDEF)
    add("select", "edge.html", "-", "0", ":--zzz", "-", "-")
    add("select", "edge.html", "36", "0", ":scope .s", "-", "-")
    add("select", "edge.html", "36", "0", ":scope > .s", "-", "-")
    add("select", "edge.html", "36", "0", "& > div > .s", "-", "-")
    add("select", "edge.html", "36", "0", ":root .s", "-", "-")
    add("one", "edge.html", "36", "p:nth-child(1)")
    add("match", "edge.html", "36", ":scope")
    add("match", "edge.html", "0", "html")
    add("match", "edge.html", "-", "*")
    add("closest", "edge.html", "37", ":scope")
    add("closest", "edge.html", "37", "#scope-root")
    add("closest", "edge.html", "37", "div:has(> p)")
    add("filter", "edge.html", "28", "li")
    add("filter", "edge.html", "28", ":nth-child(2)")

    out.append("# fragment.html")
    for s in [":root", "p", "p:first-child", "p:nth-child(2)", "p:last-of-type", "ul > li:last-child", "p:only-of-type", "body", "* + ul"]:
        add("select", "fragment.html", "-", "0", s, "-", "-")
    add("match", "fragment.html", "0", ":first-child")
    out.append("# lonely.html")
    for s in [":root", ":root > p", "main:only-child", "p:only-child", "main:first-of-type:last-of-type"]:
        add("select", "lonely.html", "-", "0", s, "-", "-")
    add("match", "lonely.html", "1", ":root")
    add("closest", "lonely.html", "1", ":root")
    return out


JOBS = "\n".join(jobs()) + "\n"


def main():
    os.makedirs("data/pages", exist_ok=True)
    for name, text in PAGES.items():
        with open("data/pages/" + name, "w", encoding="utf-8") as f:
            f.write(text)
    with open("data/jobs.tsv", "w", encoding="utf-8") as f:
        f.write(JOBS)


if __name__ == "__main__":
    main()
