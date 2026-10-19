# Writes the three sheets that are not UTF-8 text: run once by hand; the
# results are checked in.
import os
HERE = os.path.dirname(os.path.abspath(__file__))

legacy = '''@charset "ISO-8859-1";
/* Intranet theme, 2009. Saved by Dreamweaver in Latin-1. */
body { font-family: "Trébuchet MS", Verdana; color: #000080; background-color: #c0c0c0; }
.copyright:before { content: "© Société Générale d\\'Électricité"; }
.price:after { content: " €"; }
a:link { color: #0000ff; } a:visited { color: #800080; }
.warn { color: #ff0000; background-color: #ffffcc; }
td.°c { width: 3em; }
'''
open(os.path.join(HERE, "legacy.css"), "wb").write(legacy.encode("cp1252"))

shop = '''/* Магазин: стили каталога */
.цена { color: #b00000; font-weight: bold; }
.скидка::before { content: "Скидка −15%"; color: #ffffff; background-color: #d40000; }
.товар:nth-child(4n) { margin-right: 0; }
'''
open(os.path.join(HERE, "shop-koi8.css"), "wb").write(shop.replace("−", "-").encode("koi8-r"))

utf16 = '''/* exported by ReportBuilder 7 */
.report th { color: #FFFFFF; background-color: #4F81BD; }
.report td.negative { color: #C00000; }
.report td.ünits { color: #404040; background-color: #F2F2F2; }
'''
open(os.path.join(HERE, "report-utf16.css"), "wb").write(b"\xff\xfe" + utf16.encode("utf-16-le"))

menu = '''.menu li:nth-child(+5) { font-style: italic; }
.menu li:nth-child(-2n+7) { color: #000; background-color: #777; }
.menu .żółw { content: "Łódź"; }
'''
open(os.path.join(HERE, "menu-latin2.css"), "wb").write(menu.encode("iso-8859-2"))
