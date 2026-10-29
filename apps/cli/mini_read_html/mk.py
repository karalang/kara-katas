"""Writes data/: the HTML pages the jobs read, each shaped like a page a
scraper meets (an encyclopedia article with infobox, sortable tables and
footnotes, a league table with a two-row header, a bank's statement
export in windows-1252, a statistics release with a layout table,
hidden tables and missing-value markers, a 1990s page with unclosed
cells, a shop's price list with a header that has no row), the broken
inputs people meet, and data/jobs.txt, one job per line. oracle.py runs
each job on pandas' read_html, mini_read_html.kara on its own port.

Every value is made up; the IBAN is the documentation example with its
check digits broken.

Run: python3 -s -P -B mk.py"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
shutil.rmtree(DATA, ignore_errors=True)
os.makedirs(DATA)


def put(name, data, encoding="utf-8"):
    if isinstance(data, str):
        data = data.encode(encoding)
    with open(os.path.join(DATA, name), "wb") as f:
        f.write(data)


# ------------------------------------------------------------ cities.html
# An encyclopedia article: an infobox, a sortable table with a rowspan
# region, sort keys hidden with display:none, footnote markers, <br> in
# cells, U+2212 minus signs and &nbsp;, a second table with a caption,
# and a navigation box.
CITIES = [
    ("1", "Paris", "/wiki/Paris", "Île-de-France", "2,102,650", "105.4", "19,950", "&minus;1.2%"),
    ("2", "Boulogne-Billancourt", "/wiki/Boulogne-Billancourt", None, "121,583", "6.17", "19,705", "+0.4%"),
    ("3", "Marseille", "/wiki/Marseille", "Provence-Alpes-Côte d'Azur", "873,076", "240.6", "3,629", "+0.9%"),
    ("4", "Nice", "/wiki/Nice", None, "348,085", "71.9", "4,841", "+0.3%"),
    ("5", "Lyon", "/wiki/Lyon", "Auvergne-Rhône-Alpes", "522,250", "47.87", "10,910", "+1.1%"),
    ("6", "Saint-Étienne", "/wiki/Saint-%C3%89tienne", None, "173,089", "79.97", "2,164", "&minus;0.1%"),
    ("7", "Toulouse", "/wiki/Toulouse", "Occitanie", "504,078", "118.3", "4,261", "+1.4%"),
    ("8", "Montpellier", "/wiki/Montpellier", None, "302,454", "56.88", "5,317", "+1.6%"),
]
rows = []
region_span = {"Île-de-France": 2, "Provence-Alpes-Côte d'Azur": 2, "Auvergne-Rhône-Alpes": 2, "Occitanie": 2}
for rank, city, href, region, pop, area, dens, change in CITIES:
    cells = [f"<td>{rank}</td>"]
    name = f'<a href="{href}" title="{city}">{city}</a>'
    if city == "Saint-Étienne":
        name += "<br><small>(Loire)</small>"
    cells.append(f"<td>{name}</td>")
    if region is not None:
        cells.append(f'<td rowspan="{region_span[region]}"><a href="/wiki/{region.replace(" ", "_")}">{region}</a></td>')
    note = '<sup id="cite_ref-insee_1-0" class="reference"><a href="#cite_note-insee-1">[a]</a></sup>' if city == "Paris" else ""
    cells.append(f'<td data-sort-value="{pop.replace(",", "")}">{pop}{note}</td>')
    cells.append(f"<td>{area}</td>")
    cells.append(f'<td><span style="display:none">{dens.replace(",", "").zfill(6)}</span>{dens}</td>')
    cells.append(f"<td>{change}</td>")
    rows.append("<tr>\n" + "\n".join(cells) + "\n</tr>")
put("cities.html", """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>List of communes in France with over 100,000 inhabitants - Example Encyclopedia</title>
<style>.wikitable td { padding: 0.2em }</style>
</head>
<body class="mediawiki">
<h1 id="firstHeading">List of communes in France with over 100,000 inhabitants</h1>
<table class="infobox vcard">
<tbody><tr><th colspan="2" class="infobox-above">Communes of France</th></tr>
<tr><th scope="row">Country</th><td>France</td></tr>
<tr><th scope="row">Communes</th><td>34,945<sup class="reference"><a href="#cite_note-2">[2]</a></sup></td></tr>
<tr><th scope="row">Largest</th><td><a href="/wiki/Paris">Paris</a></td></tr>
<tr><th scope="row">Census</th><td>1&nbsp;January 2021</td></tr>
</tbody></table>
<p>The table lists the communes of metropolitan France by population.</p>
<h2>By population</h2>
<table class="wikitable sortable" id="largest">
<tbody><tr>
<th>Rank</th>
<th>Commune</th>
<th>Region</th>
<th>Population<br>(2021)</th>
<th>Area<br>(km<sup>2</sup>)</th>
<th>Density<br>(/km<sup>2</sup>)</th>
<th>Change<br>2015&ndash;21</th>
</tr>
""" + "\n".join(rows) + """
</tbody></table>
<h2>By region</h2>
<table class="wikitable">
<caption>Communes over 100,000 by region</caption>
<tbody><tr><th>Region</th><th>Communes</th><th>Share</th></tr>
<tr><td>Île-de-France</td><td>5</td><td>11.9%</td></tr>
<tr><td>Auvergne-Rhône-Alpes</td><td>4</td><td>9.5%</td></tr>
<tr><td>Occitanie</td><td>2</td><td>4.8%</td></tr>
<tr><td>Grand Est</td><td>3</td><td>7.1%</td></tr>
<tr><th>Total</th><th>42</th><th>100%</th></tr>
</tbody></table>
<h2>Notes</h2>
<ol class="references"><li id="cite_note-insee-1">Municipal population, INSEE.</li></ol>
<table class="navbox">
<tbody><tr><th scope="row" class="navbox-group">Prefectures</th><td class="navbox-list"><a href="/wiki/Lyon">Lyon</a> &middot; <a href="/wiki/Marseille">Marseille</a> &middot; <a href="/wiki/Toulouse">Toulouse</a></td></tr>
<tr><th scope="row" class="navbox-group">Rivers</th><td class="navbox-list"><a href="/wiki/Rh%C3%B4ne">Rhône</a> &middot; <a href="/wiki/Garonne">Garonne</a></td></tr>
</tbody></table>
</body>
</html>
""")

# ------------------------------------------------------------ standings.html
# A league table: two header rows in <thead> (rowspans and colspans),
# links and badges in the team cell, a <tfoot> note across every column,
# and a second table of fixtures with no <thead>.
TEAMS = [
    ("Lyon Rovers", "/teams/lyon-rovers", "(C)", 9, 2, 1, 6, 3, 1),
    ("Harbour City", "/teams/harbour-city", "", 8, 3, 1, 5, 4, 2),
    ("Northbridge United", "/teams/northbridge", "", 7, 2, 3, 5, 2, 3),
    ("St. Clement's", "/teams/st-clements", "", 6, 4, 2, 3, 5, 4),
    ("Vale Athletic", "/teams/vale", "(R)", 2, 3, 7, 1, 2, 9),
]
body = []
for pos, (team, href, badge, hw, hd, hl, aw, ad, al) in enumerate(TEAMS, 1):
    pts = 3 * (hw + aw) + hd + ad
    b = f' <span class="badge">{badge}</span>' if badge else ""
    body.append(f'    <tr class="pos-{pos}"><td>{pos}</td><td><a href="{href}">{team}</a>{b}</td>'
                f"<td>{hw}</td><td>{hd}</td><td>{hl}</td><td>{aw}</td><td>{ad}</td><td>{al}</td><td><b>{pts}</b></td></tr>")
put("standings.html", """<!doctype html>
<html><head><meta charset="utf-8"><title>Regional League 2025-26</title></head>
<body>
<table id="standings" class="league">
  <thead>
    <tr><th rowspan="2">Pos</th><th rowspan="2">Team</th><th colspan="3">Home</th><th colspan="3">Away</th><th rowspan="2"><abbr title="Points">Pts</abbr></th></tr>
    <tr><th>W</th><th>D</th><th>L</th><th>W</th><th>D</th><th>L</th></tr>
  </thead>
  <tbody>
""" + "\n".join(body) + """
  </tbody>
  <tfoot>
    <tr><td colspan="9">Source: league office, 2026-04-30. (C) champion, (R) relegated.</td></tr>
  </tfoot>
</table>
<h3>Last round</h3>
<table id="fixtures">
  <tr><th>Date</th><th>Home</th><th>Score</th><th>Away</th><th>Attendance</th></tr>
  <tr><td>2026-04-25</td><td><a href="/teams/lyon-rovers">Lyon Rovers</a></td><td>2&ndash;1</td><td><a href="/teams/vale">Vale Athletic</a></td><td>18,204</td></tr>
  <tr><td>2026-04-25</td><td><a href="/teams/harbour-city">Harbour City</a></td><td>0&ndash;0</td><td><a href="/teams/st-clements">St. Clement's</a></td><td>9,870</td></tr>
  <tr><td>2026-04-26</td><td><a href="/teams/northbridge">Northbridge United</a></td><td>3&ndash;2</td><td><a href="https://example.org/clubs/visitors">Visitors XI</a></td><td></td></tr>
</table>
</body></html>
""")

# ------------------------------------------------------------ statement.html
# A bank's statement export in windows-1252, declared with http-equiv:
# upper-case tags, unquoted attributes, a <thead> and a <tfoot>, amounts
# in the German style (1.234,56), the euro sign as the raw byte 0x80 and
# as &euro;, and &nbsp; padding.
TX = [
    ("01.10.2026", "01.10.2026", "Gehalt Oktober / Arbeitgeber GmbH", "", "3.250,00"),
    ("02.10.2026", "02.10.2026", "Miete Oktober", "1.150,00", ""),
    ("03.10.2026", "05.10.2026", "REWE Markt Köln – Kartenzahlung", "84,37", ""),
    ("07.10.2026", "07.10.2026", "Stadtwerke Abschlag", "96,00", ""),
    ("09.10.2026", "09.10.2026", "Erstattung »Bürobedarf«", "", "45,90"),
    ("12.10.2026", "12.10.2026", "Bargeldauszahlung Geldautomat", "200,00", ""),
    ("15.10.2026", "16.10.2026", "Überweisung an M. Müller", "1.020,50", ""),
]
tr = []
for booked, value, text, debit, credit in TX:
    tr.append(f"<TR><TD>{booked}<TD>{value}<TD>{text}<TD ALIGN=right>{debit or '&nbsp;'}<TD ALIGN=right>{credit}")
put("statement.html", ("""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=windows-1252">
<TITLE>Kontoauszug 10/2026</TITLE>
</HEAD>
<BODY>
<H2>Kontoauszug Nr. 10/2026</H2>
<TABLE BORDER=0 CLASS=meta>
<TR><TH ALIGN=left>IBAN<TD>DE00 1234 5678 9012 3456 78
<TR><TH ALIGN=left>Währung<TD>€ (EUR)
<TR><TH ALIGN=left>Eröffnungssaldo<TD>1.512,04 &euro;
</TABLE>
<TABLE BORDER=1 CELLPADDING=3 CLASS=umsaetze ID=tx>
<THEAD>
<TR><TH>Buchungstag<TH>Valuta<TH>Verwendungszweck<TH>Soll (€)<TH>Haben (€)
</THEAD>
<TBODY>
""" + "\n".join(tr) + """
</TBODY>
<TFOOT>
<TR><TH COLSPAN=3 ALIGN=right>Summe<TD ALIGN=right>2.550,87<TD ALIGN=right>3.295,90
<TR><TH COLSPAN=3 ALIGN=right>Schlusssaldo<TD COLSPAN=2 ALIGN=right>2.257,07
</TFOOT>
</TABLE>
</BODY>
</HTML>
"""), "cp1252")

# ------------------------------------------------------------ release.html
# A statistics release: a layout table that holds the data table, a
# hidden table, a column hidden by style, a <style> inside a table, an
# empty table, a table of only whitespace, and the markers a statistics
# office uses for missing values (.., x, -, and an en dash).
put("release.html", """<!DOCTYPE html>
<html lang="en-GB">
<head><meta charset="utf-8"><title>Labour market overview, UK: October 2026</title></head>
<body>
<table class="layout" width="100%"><tr><td class="nav"><a href="/">Home</a> &gt; <a href="/releases">Releases</a></td>
<td class="main">
<h1>Labour market overview</h1>
<table class="data" id="t1" summary="Employment rate by region">
<caption>Table 1: Employment rate (%), people aged 16 to 64, seasonally adjusted</caption>
<thead><tr><th scope="col">Region</th><th scope="col">Jul-Sep 2026</th><th scope="col">Change on quarter</th><th scope="col" style="display: none">Code</th><th scope="col">Change on year</th></tr></thead>
<tbody>
<tr><th scope="row">North East</th><td>71.4</td><td>0.3</td><td style="display: none">E12000001</td><td>-0.2</td></tr>
<tr><th scope="row">North West</th><td>73.9</td><td>-0.1</td><td style="display: none">E12000002</td><td>0.6</td></tr>
<tr><th scope="row">Wales</th><td>72.0</td><td>..</td><td style="display: none">W92000004</td><td>x</td></tr>
<tr><th scope="row">Scotland</th><td>74.6</td><td>&ndash;</td><td style="display: none">S92000003</td><td>1.1</td></tr>
<tr><th scope="row">Northern Ireland</th><td>-</td><td>-</td><td style="display: none">N92000002</td><td>-</td></tr>
</tbody>
<tfoot><tr><td colspan="5">.. not available; x suppressed; &ndash; no change. Source: Labour Force Survey.</td></tr></tfoot>
</table>
<table class="data" id="t2">
<style>#t2 td.n { text-align: right }</style>
<tr><th>Industry</th><th>Vacancies (thousands)</th><th>Rate</th></tr>
<tr><td>Health and social work</td><td class="n">162</td><td class="n">3.9</td></tr>
<tr><td>Accommodation &amp; food</td><td class="n">104</td><td class="n">4.8</td></tr>
<tr><td>Information &amp; communication</td><td class="n">39</td><td class="n">2.6</td></tr>
<tr><td>All industries</td><td class="n">1,014</td><td class="n">3.0</td></tr>
</table>
<table style="display:none" id="draft"><tr><th>Draft</th></tr><tr><td>Do not publish</td></tr></table>
<table id="empty"></table>
<table id="blank"><tr><td> </td><td>
</td></tr></table>
</td></tr></table>
</body>
</html>
""")

# ------------------------------------------------------------ legacy.html
# A page from 1998: no doctype, upper-case tags, unclosed <TD> and <TR>,
# <P> and <FONT> in cells, a comment, a script that writes a <table>
# string, &amp; and a bare &, numeric references, and no </TABLE>.
put("legacy.html", """<HTML>
<HEAD><TITLE>Our Price List!!</TITLE>
<SCRIPT LANGUAGE="JavaScript">
<!--
document.write("<table><tr><td>not a table</td></tr></table>");
// -->
</SCRIPT>
</HEAD>
<BODY BGCOLOR=#FFFFFF>
<CENTER><FONT FACE="Arial" SIZE=4>Welcome to AT&T Hobby Supplies</FONT></CENTER>
<P>Prices updated 10/29/98
<TABLE BORDER=1 WIDTH=600>
<TR BGCOLOR=#CCCCFF><TD><B>Item #</B><TD><B>Description</B><TD><B>Price</B><TD><B>In stock?</B>
<!-- row 1 -->
<TR><TD>1001<TD>Model train set<P>HO scale<TD>$129.99<TD>Yes
<TR><TD>1002<TD><FONT COLOR=red>NEW!</FONT> Caf&#233; diorama<TD>$45.00<TD>No
<TR><TD>1003<TD>Paint &amp; brushes<TD>$12.50<TD>Yes
<TR><TD>1004<TD>Glue &#x2014; 2 oz.<TD>$3.25<TD>
<TR><TD>1005<TD>Track (per foot)<TD>$1.10
</TABLE>
<P>Call us at 555-0199!
<TABLE><TR><TD>Hours<TD>Mon-Fri 9-5<TR><TD>Sat<TD>10-2
</BODY>
</HTML>
""")

# ------------------------------------------------------------ prices.html
# A shop's price list with a UTF-8 BOM and no charset: a <thead> whose
# cells have no <tr>, a duplicate column name, ragged rows, an empty
# row, th cells down the first column, and prices with a space as the
# thousands separator.
put("prices.html", "﻿" + """<html><body>
<table class="prices">
<thead><th>SKU</th><th>Product</th><th>Price</th><th>Price</th><th>Stock</th></thead>
<tbody>
<tr><th>A-100</th><td>Espresso machine</td><td>1 299,00</td><td>1 199,00</td><td>4</td></tr>
<tr><th>A-101</th><td>Milk frother</td><td>89,90</td><td>79,90</td><td>12</td></tr>
<tr><th>A-102</th><td>Grinder</td><td>249,00</td></tr>
<tr><td></td><td></td><td></td><td></td><td></td></tr>
<tr><th>B-200</th><td>Beans, 1 kg</td><td>18,50</td><td>16,90</td><td>140</td></tr>
<tr><th>B-201</th><td>Descaler</td><td>9,99</td><td></td><td>0</td></tr>
</tbody>
</table>
<table class="prices" id="bundles">
<tr><th>Bundle</th><th>Items</th><th>Save</th></tr>
<tr><td>Starter</td><td>A-101, B-200</td><td>10%</td></tr>
<tr><td>Barista</td><td>A-100, A-102, B-200</td><td>15%</td></tr>
</table>
</body></html>
""")

# ------------------------------------------------------------ the broken inputs
put("no_tables.html", "<!DOCTYPE html><html><body><h1>Nothing here</h1><p>No data today.</p></body></html>\n")
put("empty.html", b"")
put("fragment.html", "<tr><td>orphan</td><td>row</td></tr>\n<td>lone cell</td>\n")
put("latin1.html", "<html><head><title>Résultats</title></head><body><table>"
    "<tr><th>Équipe</th><th>Points</th></tr><tr><td>Montélimar</td><td>12</td></tr>"
    "<tr><td>Béziers</td><td>9</td></tr></table></body></html>\n", "latin-1")

JOBS = """
read cities.html
read cities.html match=Population
read cities.html match=Prefectures
read cities.html attrs=id:largest
read cities.html attrs=class:wikitable
read cities.html attrs=class:wikitable\\ssortable
read cities.html match=Share index_col=0
read cities.html match=Population displayed_only=False
read cities.html match=Population thousands=None
read cities.html match=Population extract_links=body head=3
read cities.html match=Population extract_links=all head=2
read cities.html match=Population extract_links=header head=1
read cities.html match=Prefectures extract_links=all
read cities.html match=Population skiprows=2
read cities.html match=Population skiprows=1,3
read cities.html match=Population header=1
read cities.html match=Population index_col=1 head=4
read cities.html match=Population na_values=+0.4%
read cities.html match=Population dtype_backend=numpy_nullable
read cities.html match=communes\\sof\\smetropolitan
read cities.html match=(?i)DENSITY
read cities.html match=^Rank$
read cities.html match=[0-9]{3},[0-9]{3}
read cities.html match=nowhere
read cities.html match=(unclosed
read cities.html attrs=id:missing
read standings.html
read standings.html attrs=id:standings
read standings.html attrs=id:standings header=0
read standings.html attrs=id:standings header=1
read standings.html attrs=id:standings index_col=0
read standings.html attrs=id:standings index_col=0,1
read standings.html attrs=id:standings extract_links=body
read standings.html attrs=id:standings extract_links=header
read standings.html attrs=id:standings extract_links=footer
read standings.html attrs=id:standings extract_links=all head=2
read standings.html attrs=id:fixtures
read standings.html attrs=id:fixtures extract_links=body
read standings.html attrs=id:fixtures thousands=None
read standings.html attrs=id:fixtures keep_default_na=False
read standings.html attrs=id:fixtures index_col=0
read standings.html attrs=id:fixtures dtype_backend=numpy_nullable
read standings.html match=Visitors
read standings.html extract_links=bogus
read statement.html
read statement.html attrs=id:tx
read statement.html attrs=id:tx thousands=. decimal=,
read statement.html attrs=class:meta header=None
read statement.html attrs=class:meta header=None index_col=0
read statement.html attrs=id:tx thousands=. decimal=, dtype_backend=numpy_nullable
read statement.html match=Schlusssaldo thousands=. decimal=,
read statement.html encoding=latin-1 attrs=class:meta header=None
read statement.html encoding=utf-8 attrs=class:meta header=None
read release.html
read release.html attrs=id:t1
read release.html attrs=id:t1 displayed_only=False
read release.html attrs=id:t1 na_values=..,x
read release.html attrs=id:t1 na_values=..,x,– index_col=0
read release.html attrs=id:t1 keep_default_na=False
read release.html attrs=id:t1 keep_default_na=False na_values=..
read release.html attrs=id:t2
read release.html attrs=id:t2 thousands=None
read release.html attrs=id:t2 displayed_only=False
read release.html attrs=id:draft
read release.html attrs=id:draft displayed_only=False
read release.html attrs=id:empty
read release.html attrs=id:blank
read release.html attrs=class:layout
read release.html attrs=class:layout displayed_only=False
read release.html match=Vacancies
read release.html match=Labour\\sForce
read legacy.html
read legacy.html match=Item
read legacy.html match=Item header=0
read legacy.html match=Item index_col=0
read legacy.html match=Hours header=None
read legacy.html match=not\\sa\\stable
read legacy.html match=Hours
read prices.html
read prices.html attrs=class:prices
read prices.html attrs=class:prices thousands=\\s decimal=,
read prices.html attrs=class:prices thousands=\\s decimal=, index_col=0
read prices.html attrs=class:prices header=None
read prices.html attrs=id:bundles
read prices.html attrs=id:bundles index_col=0 na_values=10%
read prices.html attrs=id:bundles skiprows=1
read prices.html attrs=id:bundles skiprows=0:3:2
read prices.html attrs=id:bundles header=None skiprows=5
read latin1.html
read latin1.html encoding=latin-1
read latin1.html encoding=cp1252
read fragment.html
read no_tables.html
read no_tables.html match=Nothing
read empty.html
read missing.html
read cities.html flavor=lxml match=Share
read cities.html match=Share index_col=5
read cities.html match=Share header=7
"""
with open(os.path.join(DATA, "jobs.txt"), "w", encoding="utf-8") as f:
    for line in JOBS.strip("\n").split("\n"):
        f.write(line + "\n")
