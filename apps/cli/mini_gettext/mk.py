# Writes data/: the .po catalogs of a small shop's UI in nine languages,
# the UI calls to render, plural expressions to compile, and .mo files
# that are broken in each way the loader reports.
import os, shutil, struct
shutil.rmtree("data", ignore_errors=True)
os.makedirs("data/po")
os.makedirs("data/broken")

def header(lang, plural, charset="UTF-8", extra=""):
    return f'''# Translations of the shop UI.
# Copyright (C) 2026 The Shop Authors
#
msgid ""
msgstr ""
"Project-Id-Version: shop 2.4\\n"
"Report-Msgid-Bugs-To: i18n@shop.example\\n"
"POT-Creation-Date: 2026-09-01 12:00+0000\\n"
"PO-Revision-Date: 2026-10-01 09:30+0200\\n"
"Language-Team: {lang} <{lang}@li.example>\\n"
"Language: {lang}\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset={charset}\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: {plural}\\n"
{extra}
'''

def entry(msgid, msgstr, ctx=None, plural=None, comments="", fuzzy=False):
    out = comments
    if fuzzy:
        out += "#, fuzzy\n"
    if ctx is not None:
        out += f'msgctxt "{ctx}"\n'
    out += f'msgid "{msgid}"\n'
    if plural is None:
        out += f'msgstr "{msgstr}"\n'
    else:
        out += f'msgid_plural "{plural}"\n'
        for i, s in enumerate(msgstr):
            out += f'msgstr[{i}] "{s}"\n'
    return out + "\n"

ITEM = ("{n} item in your cart", "{n} items in your cart")
DAY = ("{n} day left", "{n} days left")
MSG = ("{n} new message", "{n} new messages")

cat = {
"fr": (header("fr", "nplurals=2; plural=(n > 1);"), [
    entry("Welcome to {shop}!", "Bienvenue chez {shop} !", comments="#: shop/views.py:12\n"),
    entry("Your cart", "Votre panier"),
    entry(ITEM[0], ["{n} article dans votre panier", "{n} articles dans votre panier"], plural=ITEM[1]),
    entry(DAY[0], ["Il reste {n} jour", "Il reste {n} jours"], plural=DAY[1]),
    entry("Open", "Ouvrir", ctx="verb"),
    entry("Open", "Ouvert", ctx="store hours"),
    entry(MSG[0], ["{n} nouveau message", "{n} nouveaux messages"], ctx="inbox", plural=MSG[1]),
    entry("Order #{id} shipped", "Commande n°{id} expédiée"),
    entry("Checkout", "Paiement", fuzzy=True, comments="#. The page title\n"),
    entry("Sign out", "Se déconnecter"),
    entry('Say "hello"', "Dites « bonjour »"),
    entry("Line one\\nLine two", "Ligne un\\nLigne deux"),
]),
"de": (header("de", "nplurals=2; plural=(n != 1);"), [
    entry("Welcome to {shop}!", "Willkommen bei {shop}!"),
    entry("Your cart", "Ihr Warenkorb"),
    entry(ITEM[0], ["{n} Artikel im Warenkorb", "{n} Artikel im Warenkorb"], plural=ITEM[1]),
    entry(DAY[0], ["Noch {n} Tag", "Noch {n} Tage"], plural=DAY[1]),
    entry("Open", "Öffnen", ctx="verb"),
    entry("Open", "Geöffnet", ctx="store hours"),
    entry("Order #{id} shipped", "Bestellung Nr. {id} versandt"),
    entry("Checkout", "Zur Kasse"),
    entry("Sign out", ""),
]),
"pl": (header("pl", "nplurals=3; plural=(n==1 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);"), [
    entry("Welcome to {shop}!", "Witamy w {shop}!"),
    entry("Your cart", "Twój koszyk"),
    entry(ITEM[0], ["{n} produkt w koszyku", "{n} produkty w koszyku", "{n} produktów w koszyku"], plural=ITEM[1]),
    entry(DAY[0], ["Został {n} dzień", "Zostały {n} dni", "Zostało {n} dni"], plural=DAY[1]),
    entry(MSG[0], ["{n} nowa wiadomość", "{n} nowe wiadomości", "{n} nowych wiadomości"], ctx="inbox", plural=MSG[1]),
    entry("Sign out", "Wyloguj się"),
]),
"ru": (header("ru", "nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);"), [
    entry("Welcome to {shop}!", "Добро пожаловать в {shop}!"),
    entry(ITEM[0], ["{n} товар в корзине", "{n} товара в корзине", "{n} товаров в корзине"], plural=ITEM[1]),
    entry(DAY[0], ["Остался {n} день", "Осталось {n} дня", "Осталось {n} дней"], plural=DAY[1]),
    entry("Open", "Открыть", ctx="verb"),
]),
"ar": (header("ar", "nplurals=6; plural=n==0 ? 0 : n==1 ? 1 : n==2 ? 2 : n%100>=3 && n%100<=10 ? 3 : n%100>=11 ? 4 : 5;"), [
    entry(ITEM[0], ["لا منتجات", "منتج واحد", "منتجان", "{n} منتجات", "{n} منتجًا", "{n} منتج"], plural=ITEM[1]),
    entry("Your cart", "سلة التسوق"),
]),
"ja": (header("ja", "nplurals=1; plural=0;"), [
    entry("Welcome to {shop}!", "{shop}へようこそ！"),
    entry(ITEM[0], ["カートに{n}点"], plural=ITEM[1]),
    entry(DAY[0], ["残り{n}日"], plural=DAY[1]),
    entry("Sign out", "ログアウト"),
]),
"ga": (header("ga", "nplurals=5; plural=n==1 ? 0 : n==2 ? 1 : (n>2 && n<7) ? 2 :(n>6 && n<11) ? 3 : 4;"), [
    entry(DAY[0], ["{n} lá fágtha", "{n} lá fágtha", "{n} lá fágtha", "{n} lá fágtha", "{n} lá fágtha"], plural=DAY[1]),
    entry(ITEM[0], ["{n} earra amháin", "{n} earra", "{n} earra", "{n} n-earra", "{n} earra"], plural=ITEM[1]),
]),
"pt": (header("pt", "nplurals=2; plural=(n != 1);"), [
    entry("Your cart", "O seu carrinho"),
    entry("Sign out", "Terminar sessão"),
    entry(DAY[0], ["Falta {n} dia", "Faltam {n} dias"], plural=DAY[1]),
]),
"pt_BR": (header("pt_BR", "nplurals=2; plural=(n > 1);", charset="ISO-8859-1",
                 extra='"X-Generator: Poedit 3.4\\n"\n"X-Poedit-Basepath: ..\\n"'), [
    entry("Welcome to {shop}!", "Bem-vindo à {shop}!"),
    entry("Your cart", "Seu carrinho"),
    entry(ITEM[0], ["{n} item no carrinho", "{n} itens no carrinho"], plural=ITEM[1]),
    entry("Order #{id} shipped", "Pedido nº {id} enviado"),
]),
# nplurals=2 but the expression reaches 2: n=2, 5, 8... find no form
"xx": (header("xx", "nplurals=2; plural=n%3;"), [
    entry(ITEM[0], ["{n} xitem", "{n} xitems"], plural=ITEM[1]),
]),
}
for lang, (head, entries) in cat.items():
    enc = "latin-1" if lang == "pt_BR" else "utf-8"
    with open(f"data/po/{lang}.po", "wb") as f:
        f.write((head + "\n" + "".join(entries)).encode(enc))

with open("data/ui.txt", "w") as f:
    f.write("""# the calls the shop makes, in the order it makes them
_ Welcome to {shop}!
_ Your cart
n {n} item in your cart|{n} items in your cart|0 1 2 3 5 11 12 21 22 25 102 111
n {n} day left|{n} days left|0 1 2 4 7 11 21
p verb|Open
p store hours|Open
p menu|Open
np inbox|{n} new message|{n} new messages|1 2 5 22
_ Order #{id} shipped
_ Checkout
_ Sign out
_ Say "hello"
_ Line one\\nLine two
_ Not in any catalog
""")

with open("data/langs.txt", "w") as f:
    f.write("fr\nde\npl\nru\nar\nja\nga\npt_BR pt\nxx de\nja fr\n")

with open("data/plurals.txt", "w") as f:
    f.write("\n".join([
        "n != 1", "(n > 1)", "0", "n%10==1 && n%100!=11 ? 0 : n != 0 ? 1 : 2",
        "!n", "!!n", "!(n == 1)", "n == 1 || n == 2 ? 0 : 1", "n < 2 < 3", "n == 1 == 0",
        "2 * n - 3 * (n / 2)", "n % 7 - 3", "(n - 5) / 2", "(n - 5) % 3", "n / 0", "n ? n / (n - 3) : 9",
        "n && 2", "n || 7", "n > 1 ? n > 2 ? 2 : 1 : 0", "n ? 1 : 2 + 3",
        "n = 1", "n == 1 &", "n +", "(n", "n)", "2n", "m", "n == 1 ? 0", "~n", "n == 1 ; 2", "",
        "((((((((((((((((((((((n))))))))))))))))))))))", "(((((((((((((((((((n)))))))))))))))))))",
        "n" + " + n" * 340,
    ]) + "\n")

def mo(entries, magic="<", version=0, corrupt=False):
    keys = sorted(entries)
    ids = strs = b""
    offs = []
    for k in keys:
        offs.append((len(ids), len(k), len(strs), len(entries[k])))
        ids += k + b"\0"
        strs += entries[k] + b"\0"
    keystart = 7 * 4 + 16 * len(keys)
    valuestart = keystart + len(ids)
    ko, vo = [], []
    for o1, l1, o2, l2 in offs:
        ko += [l1, o1 + keystart]
        vo += [l2, o2 + valuestart + (10000 if corrupt else 0)]
    out = struct.pack(magic + "Iiiiiii", 0x950412de, version, len(keys), 28, 28 + len(keys) * 8, 0, 0)
    out += struct.pack(magic + f"{len(ko + vo)}i", *(ko + vo))
    return out + ids + strs

base = {b"": b"Content-Type: text/plain; charset=UTF-8\nPlural-Forms: nplurals=2; plural=n>1;\n",
        b"Your cart": "Ta charrette".encode(), b"{n} day left\0{n} days left": b"{n} jour BE\0{n} jours BE"}
with open("data/broken/be.mo", "wb") as f:
    f.write(mo(base, magic=">"))
with open("data/broken/version1.mo", "wb") as f:
    f.write(mo(base, version=0x10003))
with open("data/broken/version2.mo", "wb") as f:
    f.write(mo(base, version=0x20000))
with open("data/broken/magic.mo", "wb") as f:
    f.write(b"\x00\x01\x02\x03" + mo(base)[4:])
with open("data/broken/corrupt.mo", "wb") as f:
    f.write(mo(base, corrupt=True))
with open("data/broken/badplural.mo", "wb") as f:
    f.write(mo({b"": b"Content-Type: text/plain; charset=UTF-8\nPlural-Forms: nplurals=2; plural=n >> 1;\n"}))
with open("data/broken/multiline.mo", "wb") as f:
    f.write(mo({b"": b"Content-Type: text/plain; charset=UTF-8\nX-Note: first part\n  continued here\n#-#-#-#-#  a.po  #-#-#-#-#\nLast-Translator: Ana <ana@x.example>\nplural-forms: nplurals=3; plural=n%3;\n",
                b"a": b"A", b"b\0bs": b"B0\0B1\0B2"}))
