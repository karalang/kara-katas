# Writes data/: the selectors of four scraper configs (field = selector,
# the way Scrapy spiders keep them), a site stylesheet, and a list of
# selectors that are broken in some way.
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

BOOKS = r"""# books.toscrape.com: catalogue and detail pages
list.item = article.product_pod
list.title = article.product_pod h3 > a::attr(title)
list.link = h3 a::attr(href)
list.price = .product_price .price_color::text
list.stock = p.instock.availability::text
list.rating = p.star-rating::attr(class)
list.next = li.next > a::attr(href)
detail.title = div.product_main > h1::text
detail.upc = table.table-striped tr:nth-child(1) > td::text
detail.desc = #product_description + p::text
detail.crumbs = ul.breadcrumb li:not(.active) a::text
detail.image = #product_gallery img::attr(src)
detail.all = div.product_main h1, div.product_main p.price_color
"""

QUOTES = r"""# quotes.toscrape.com
quote = div.quote
text = div.quote span.text::text
author = small.author::text
tags = div.tags a.tag::text
about = .quote span a[href*="/author/"]::attr(href)
next = li.next a::attr("href")
login.csrf = form input[name=csrf_token]::attr(value)
login.user = FORM INPUT[Name='username']
top.tags = div.tags-box span.tag-item > a.tag::TEXT
"""

JOBS = r"""# a job board with data attributes
card = li[data-job-id]
remote = li[data-job-id]:has(> span.remote)
title = li[data-job-id] :is(h2, h3) > a::text
salary = [data-testid="salary"]::text
posted = time[datetime]::attr(datetime)
english = div:lang(en) p
french = article:lang("fr-CA")::text
no.ads = li:not([data-sponsored]) a.job-link::attr(href)
odd.rows = tr:nth-child(odd) td:first-of-type::text
last = ul.results > li:last-child
every3 = tbody tr:nth-child(3n+2)
tail = tbody tr:nth-last-child(-n+3)
first3 = ol > li:nth-child(-n + 3)
even = tr:nth-of-type(even)
fixed = tr:nth-child(0n+5)
none = tr:nth-child(-2n-1)
from4 = tr:nth-last-of-type(n+4)
loose = tr:nth-child( 2n - 1 )
step = tr:nth-child(-3n+8)
company = div.company:has(img.logo)
next.job = h2.title:has(+ p)
later = h2:has(~ footer)
"""

SHOP = r"""# a shop with microdata
price = span[itemprop=price]::attr(content)
sku = [itemprop~=sku]
alt.lang = link[hreflang|=en]::attr(href)
pdfs = a[href$=".pdf"]::attr(href)
external = a[href^="http"]:not([href*="example.com"])::attr(href)
empty.cells = td:empty
picked = input:checked::attr(name)
disabled = button:disabled
enabled = input:enabled
links = :link
visited = a:visited
only = ul > li:only-child
only.type = dl dt:only-of-type
siblings = h2 ~ p
apos = q[title='It\'s']
total = td:contains("Total")::text
owner = td:contains("Joe's")
quote = td:contains('say "hi"')
mixed = td:contains('Joe\'s "best"')
svg = svg|rect
svg.any = svg|*
xlink = use[xlink|href]::attr(xlink:href)
any.ns = *|*
no.ns = |div
upper = DIV.Item > A[HREF]
nav = :where(nav, footer) a
scope = :scope > div::text
root = :root > body
not.star = div:not(*)
not.p = div:not(p)
blank = a[title=""]
not.eq = a[rel!=nofollow]
not.empty = a[rel!=""]
hyphen = a[class|=btn]
word.empty = a[class~=""]
word.space = a[class~="a b"]
prefix.empty = a[href^=""]
attr.ns = [*|lang]
escaped = #\31 23 > .\@media
unicode = p.caf\E9 ::text
japanese = 日本語 > span.名前
comment = ul /* the menu */ > li
"""

THEME = r"""/* site theme */
html, body {
  margin: 0;
}
@media (max-width: 600px) {
  .nav > li + li { display: none }
}
a:hover,
a:focus-visible {
  text-decoration: underline;
}
.btn.btn-primary:not(.disabled):active { color: white }
#main .card:nth-of-type(2n) { margin-left: 1em }
input[type="checkbox"]:checked + label::before { content: "x" }
p::first-line { font-weight: bold }
ul li:first-child:after { content: "" }
h1 ~ p:first-of-type { margin-top: 0 }
*:nth-of-type(2) { color: red }
table td:nth-child(even) { background: #eee }
.grid > :is(.col, .cell):where(.wide) { flex: 2 }
div:is(.alert) { padding: 4px }
article:has(+ aside) { width: 70% }
section:has(~ footer) { border: 0 }
nav:has(a.active) { font-weight: bold }
#app #sidebar ul.menu > li.item:hover a { color: blue }
::selection { background: yellow }
form :is(input, select, textarea):disabled { opacity: 0.5 }
*:first-of-type { color: green }
li:first_child { list-style: none }
"""

BROKEN = r"""div >
.
#
a[href
a[href=]
a[="x"]
a[href~x]
a[*]
a[|href]
a[x="y" i]
div::text p
p::text::text
:not(:not(a))
p:not(::before)
:is(p::before)
a:nth-child(foo)
a:nth-child("2")
a:nth-child(1.5)
li:nth-child(2N+1)
"unclosed
a[title="bad\
p:unknown-thing
p:frobnicate(1)
:is(a,b)
:is(a
:has(a b)
li:has(- a)
li:has(#x)
a:contains(1)
p:lang(en, fr)
p:lang(en fr)
div:scope
a, :scope p
div ::attr(1)
a::attr
a::attr(href, title)
::selection
::foo(bar)
,a
a,
a b ,, c
a:not(b c)
a:has()
:nth-child
p::text:hover
"""


def write(rel, text):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def main():
    write("spiders/books.cfg", BOOKS)
    write("spiders/quotes.cfg", QUOTES)
    write("spiders/jobs.cfg", JOBS)
    write("spiders/shop.cfg", SHOP)
    write("theme.css", THEME)
    write("broken.txt", BROKEN)


if __name__ == "__main__":
    main()
