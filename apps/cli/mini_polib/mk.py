"""Writes data/ for mini_polib: the gettext catalogs of Larkfield, a
library-loans web application (a template, five translations at different
stages, one in ISO-8859-1), three MO files, broken catalogs, and
data/jobs.txt, the commands the run executes.

Run from this directory: python3 -s -P -B mk.py"""
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

POT = r'''# Larkfield translation template.
# Copyright (C) 2026 The Larkfield contributors
# This file is distributed under the same license as the Larkfield project.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: Larkfield 4.2\n"
"Report-Msgid-Bugs-To: translators@larkfield.example\n"
"POT-Creation-Date: 2026-10-20 09:14+0000\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"Language: \n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=CHARSET\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=INTEGER; plural=EXPRESSION;\n"
"Generated-By: Babel 2.16.0\n"

#: larkfield/views/catalog.py:41 templates/catalog/search.html:12
msgid "Search the catalog"
msgstr ""

#: larkfield/views/catalog.py:58
#, python-format
msgid "%(count)d result for \"%(query)s\""
msgid_plural "%(count)d results for \"%(query)s\""
msgstr[0] ""
msgstr[1] ""

#. Button label: places a hold on a book that is out on loan.
#: templates/catalog/detail.html:88
msgctxt "button"
msgid "Hold"
msgstr ""

#. Heading of the list of holds a member has placed.
#: templates/members/account.html:30
msgctxt "heading"
msgid "Holds"
msgstr ""

#: templates/members/account.html:31
msgid "Holds"
msgstr ""

#: larkfield/views/loans.py:102 larkfield/views/loans.py:147
#: larkfield/emails/reminders.py:33 larkfield/emails/reminders.py:71
#: templates/loans/overdue-notice.html:9 templates/loans/overdue-notice.txt:4
#: static/js/loan-calendar.js:210
#, python-format
msgid "Return by %(date)s"
msgstr ""

#: larkfield/views/loans.py:180
#, python-format
msgid "You have %(n)d overdue item"
msgid_plural "You have %(n)d overdue items"
msgstr[0] ""
msgstr[1] ""

#. This is shown on the account page under the loan list, and is the one
#. place where the fine schedule is explained, so keep the amounts and the
#. grace period exactly as written in the source text.
#: templates/members/fines.html:14
msgid ""
"Fines are charged at 25 cents a day after a grace period of three days, up "
"to the replacement cost of the item. Fines under one dollar are waived at "
"checkout."
msgstr ""

#: templates/members/fines.html:20
msgid ""
"Dear member,\n"
"\n"
"Your card expires on %(date)s. Renew it at any branch desk.\n"
msgstr ""

#: larkfield/forms.py:22
msgid "Library card number"
msgstr ""

#: larkfield/forms.py:23
msgid "PIN"
msgstr ""

#: larkfield/forms.py:40
#, python-brace-format
msgid "The PIN must be {min} to {max} digits long."
msgstr ""

#: larkfield/forms.py:58
msgid "Signed in as \"{name}\"\t(change)"
msgstr ""

#: templates/base.html:5
msgid "Larkfield - your library, online"
msgstr ""

#: templates/base.html:17
msgid "Sign out"
msgstr ""

#: templates/base.html:18 templates/base.html:44
msgid "My account"
msgstr ""

#: templates/catalog/detail.html:12
msgid "Available"
msgstr ""

#: templates/catalog/detail.html:13
msgid "On loan"
msgstr ""

#: templates/catalog/detail.html:40
msgctxt "verb"
msgid "Open"
msgstr ""

#: templates/branches/hours.html:8
msgctxt "adjective"
msgid "Open"
msgstr ""

#: templates/branches/hours.html:9
msgid "Closed"
msgstr ""

#: larkfield/views/holds.py:66
#, python-format
msgid "%(title)s is ready for pickup at %(branch)s until %(date)s."
msgstr ""

#: larkfield/views/holds.py:90
#, python-format
msgid "%(n)d hold"
msgid_plural "%(n)d holds"
msgstr[0] ""
msgstr[1] ""

#: larkfield/admin/reports.py:12
msgid "Circulation by branch and collection, last twelve months"
msgstr ""

#: larkfield/admin/reports.py:31
msgid "C:\\Exports\\circulation.csv"
msgstr ""

#: larkfield/api/errors.py:8
msgid "Something went wrong. Please try again in a few minutes, or contact the help desk."
msgstr ""

#: static/js/search-box.js:44
msgid "Type at least three letters"
msgstr ""
'''

DE = r'''# German translation of Larkfield.
# Copyright (C) 2026 The Larkfield contributors
# This file is distributed under the same license as the Larkfield project.
# Jana Vogt <jana.vogt@example.de>, 2025, 2026.
#
msgid ""
msgstr ""
"Project-Id-Version: Larkfield 4.2\n"
"Report-Msgid-Bugs-To: translators@larkfield.example\n"
"POT-Creation-Date: 2026-10-20 09:14+0000\n"
"PO-Revision-Date: 2026-10-22 18:40+0200\n"
"Last-Translator: Jana Vogt <jana.vogt@example.de>\n"
"Language: de\n"
"Language-Team: German <de@larkfield.example>\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Generated-By: Babel 2.16.0\n"
"X-Generator: Poedit 3.5\n"
"X-Poedit-SearchPath-10: static\n"
"X-Poedit-SearchPath-9: templates\n"
"X-Poedit-SearchPath-0: larkfield\n"
"X-Crowdin-Project: larkfield\n"

#: larkfield/views/catalog.py:41 templates/catalog/search.html:12
msgid "Search the catalog"
msgstr "Katalog durchsuchen"

#: larkfield/views/catalog.py:58
#, python-format
msgid "%(count)d result for \"%(query)s\""
msgid_plural "%(count)d results for \"%(query)s\""
msgstr[0] "%(count)d Treffer für „%(query)s“"
msgstr[1] "%(count)d Treffer für „%(query)s“"

#. Button label: places a hold on a book that is out on loan.
#: templates/catalog/detail.html:88
msgctxt "button"
msgid "Hold"
msgstr "Vormerken"

#. Heading of the list of holds a member has placed.
#: templates/members/account.html:30
msgctxt "heading"
msgid "Holds"
msgstr "Vormerkungen"

#: templates/members/account.html:31
msgid "Holds"
msgstr "Vormerkungen"

#: larkfield/views/loans.py:102 larkfield/views/loans.py:147
#: larkfield/emails/reminders.py:33 larkfield/emails/reminders.py:71
#: templates/loans/overdue-notice.html:9 templates/loans/overdue-notice.txt:4
#: static/js/loan-calendar.js:210
#, python-format
msgid "Return by %(date)s"
msgstr "Rückgabe bis %(date)s"

# Jana: "überfällig" is the word the branches use on their notices.
#: larkfield/views/loans.py:180
#, python-format
msgid "You have %(n)d overdue item"
msgid_plural "You have %(n)d overdue items"
msgstr[0] "Sie haben %(n)d überfälliges Medium"
msgstr[1] "Sie haben %(n)d überfällige Medien"

#. This is shown on the account page under the loan list, and is the one
#. place where the fine schedule is explained, so keep the amounts and the
#. grace period exactly as written in the source text.
#: templates/members/fines.html:14
#, fuzzy
#| msgid ""
#| "Fines are charged at 20 cents a day after a grace period of three days, up "
#| "to the replacement cost of the item."
msgid ""
"Fines are charged at 25 cents a day after a grace period of three days, up "
"to the replacement cost of the item. Fines under one dollar are waived at "
"checkout."
msgstr ""
"Säumnisgebühren betragen nach einer Kulanzfrist von drei Tagen 20 Cent pro "
"Tag, höchstens jedoch den Wiederbeschaffungswert des Mediums."

#: templates/members/fines.html:20
msgid ""
"Dear member,\n"
"\n"
"Your card expires on %(date)s. Renew it at any branch desk.\n"
msgstr ""
"Liebes Mitglied,\n"
"\n"
"Ihr Ausweis läuft am %(date)s ab. Sie können ihn an jeder Theke verlängern.\n"

#: larkfield/forms.py:22
msgid "Library card number"
msgstr "Ausweisnummer"

#: larkfield/forms.py:23
msgid "PIN"
msgstr "PIN"

#: larkfield/forms.py:40
#, python-brace-format
msgid "The PIN must be {min} to {max} digits long."
msgstr "Die PIN muss {min} bis {max} Ziffern lang sein."

#: larkfield/forms.py:58
msgid "Signed in as \"{name}\"\t(change)"
msgstr "Angemeldet als „{name}“\t(ändern)"

#: templates/base.html:5
msgid "Larkfield - your library, online"
msgstr "Larkfield - Ihre Bibliothek, online"

#: templates/base.html:17
msgid "Sign out"
msgstr "Abmelden"

#: templates/base.html:18 templates/base.html:44
msgid "My account"
msgstr "Mein Konto"

#: templates/catalog/detail.html:12
msgid "Available"
msgstr "Verfügbar"

#: templates/catalog/detail.html:13
msgid "On loan"
msgstr "Ausgeliehen"

#: templates/catalog/detail.html:40
msgctxt "verb"
msgid "Open"
msgstr "Öffnen"

#: templates/branches/hours.html:8
msgctxt "adjective"
msgid "Open"
msgstr "Geöffnet"

#: templates/branches/hours.html:9
msgid "Closed"
msgstr "Geschlossen"

#: larkfield/views/holds.py:66
#, fuzzy, python-format
#| msgid "%(title)s is ready for pickup at %(branch)s."
msgid "%(title)s is ready for pickup at %(branch)s until %(date)s."
msgstr "%(title)s liegt in %(branch)s zur Abholung bereit."

#: larkfield/views/holds.py:90
#, python-format
msgid "%(n)d hold"
msgid_plural "%(n)d holds"
msgstr[0] "%(n)d Vormerkung"
msgstr[1] "%(n)d Vormerkungen"

#: larkfield/admin/reports.py:12
msgid "Circulation by branch and collection, last twelve months"
msgstr "Ausleihen nach Zweigstelle und Bestand, letzte zwölf Monate"

#: larkfield/admin/reports.py:31
msgid "C:\\Exports\\circulation.csv"
msgstr "C:\\Export\\Ausleihen.csv"

#: larkfield/api/errors.py:8
msgid ""
"Something went wrong. Please try again in a few minutes, or contact the help "
"desk."
msgstr ""
"Etwas ist schiefgelaufen. Bitte versuchen Sie es in ein paar Minuten noch "
"einmal oder wenden Sie sich an die Auskunft."

#: static/js/search-box.js:44
msgid "Type at least three letters"
msgstr ""

#~ msgid "Renew all"
#~ msgstr "Alle verlängern"

#, python-format
#~| msgid "Due %(date)s"
#~ msgid "Due on %(date)s"
#~ msgstr "Fällig am %(date)s"

# Removed with the old reader-ticket system.
#~ msgctxt "ticket"
#~ msgid ""
#~ "Ask at the desk for a reader's ticket. You will need a proof of address "
#~ "and one photograph."
#~ msgstr ""
#~ "Fragen Sie an der Theke nach einem Leseausweis. Sie brauchen einen "
#~ "Adressnachweis und ein Passbild."
'''

FR = r'''# French translation of Larkfield.
# Copyright (C) 2026 The Larkfield contributors
# Élodie Marchand <elodie@example.fr>, 2026.
#
msgid ""
msgstr ""
"Project-Id-Version: Larkfield 4.2\n"
"Report-Msgid-Bugs-To: translators@larkfield.example\n"
"POT-Creation-Date: 2026-10-20 09:14+0000\n"
"PO-Revision-Date: 2026-10-21 11:02+0200\n"
"Last-Translator: Élodie Marchand <elodie@example.fr>\n"
"Language-Team: French <fr@larkfield.example>\n"
"Language: fr\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=utf8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=2; plural=(n > 1);\n"

#: larkfield/views/catalog.py:41 templates/catalog/search.html:12
msgid "Search the catalog"
msgstr "Rechercher dans le catalogue"

#: larkfield/views/catalog.py:58
#, python-format
msgid "%(count)d result for \"%(query)s\""
msgid_plural "%(count)d results for \"%(query)s\""
msgstr[0] "%(count)d résultat pour « %(query)s »"
msgstr[1] ""

#. Button label: places a hold on a book that is out on loan.
#: templates/catalog/detail.html:88
msgctxt "button"
msgid "Hold"
msgstr "Réserver"

#: templates/members/account.html:31
msgid "Holds"
msgstr "Réservations"

#: larkfield/views/loans.py:102 larkfield/views/loans.py:147
#: larkfield/emails/reminders.py:33 larkfield/emails/reminders.py:71
#: templates/loans/overdue-notice.html:9 templates/loans/overdue-notice.txt:4
#: static/js/loan-calendar.js:210
#, python-format
msgid "Return by %(date)s"
msgstr "À rendre avant le %(date)s"

#. This is shown on the account page under the loan list, and is the one
#. place where the fine schedule is explained, so keep the amounts and the
#. grace period exactly as written in the source text.
#: templates/members/fines.html:14
msgid ""
"Fines are charged at 25 cents a day after a grace period of three days, up "
"to the replacement cost of the item. Fines under one dollar are waived at "
"checkout."
msgstr ""
"Les pénalités sont de 25 centimes par jour après un délai de grâce de trois "
"jours, dans la limite du coût de remplacement du document. Les pénalités "
"inférieures à un dollar sont annulées au moment de l'emprunt."

#: larkfield/forms.py:22
msgid "Library card number"
msgstr "Numéro de carte"

#: larkfield/forms.py:23
msgid "PIN"
msgstr "Code"

#: templates/base.html:5
msgid "Larkfield - your library, online"
msgstr "Larkfield - votre bibliothèque en ligne"

#: templates/base.html:17
msgid "Sign out"
msgstr "Se déconnecter"

#: templates/base.html:18 templates/base.html:44
msgid "My account"
msgstr "Mon compte"

#: templates/catalog/detail.html:12
#, fuzzy
msgid "Available"
msgstr "Libre"

#: templates/catalog/detail.html:13
msgid "On loan"
msgstr "Emprunté"

#: templates/branches/hours.html:8
msgctxt "adjective"
msgid "Open"
msgstr "Ouvert"

#: templates/branches/hours.html:9
msgid "Closed"
msgstr "Fermé"

#: larkfield/views/holds.py:90
#, python-format
msgid "%(n)d hold"
msgid_plural "%(n)d holds"
msgstr[0] "%(n)d réservation"
msgstr[1] "%(n)d réservations"

#: larkfield/api/errors.py:8
msgid ""
"Something went wrong. Please try again in a few minutes, or contact the help "
"desk."
msgstr ""

#: static/js/search-box.js:44
msgid "Type at least three letters"
msgstr "Saisissez au moins trois lettres"
'''

JA = r'''# Japanese translation of Larkfield.
# 佐藤 美咲 <misaki@example.jp>, 2026.
#
msgid ""
msgstr ""
"Project-Id-Version: Larkfield 4.2\n"
"POT-Creation-Date: 2026-10-20 09:14+0000\n"
"PO-Revision-Date: 2026-10-23 08:15+0900\n"
"Last-Translator: 佐藤 美咲 <misaki@example.jp>\n"
"Language-Team: Japanese\n"
"Language: ja\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=1; plural=0;\n"

#: larkfield/views/catalog.py:41 templates/catalog/search.html:12
msgid "Search the catalog"
msgstr "蔵書を検索"

#: larkfield/views/catalog.py:58
#, python-format
msgid "%(count)d result for \"%(query)s\""
msgid_plural "%(count)d results for \"%(query)s\""
msgstr[0] "「%(query)s」の検索結果：%(count)d件"

#: larkfield/views/loans.py:102
#, python-format
msgid "Return by %(date)s"
msgstr "返却期限：%(date)s"

#: larkfield/views/loans.py:180
#, python-format
msgid "You have %(n)d overdue item"
msgid_plural "You have %(n)d overdue items"
msgstr[0] "延滞中の資料が%(n)d点あります"

#: templates/members/fines.html:14
msgid ""
"Fines are charged at 25 cents a day after a grace period of three days, up "
"to the replacement cost of the item. Fines under one dollar are waived at "
"checkout."
msgstr "延滞料は猶予期間の三日を過ぎると一日25セントかかり、資料の弁償額が上限です。一ドル未満の延滞料は貸出時に免除されます。"

#: templates/base.html:17
msgid "Sign out"
msgstr "ログアウト"

#: templates/catalog/detail.html:40
msgctxt "verb"
msgid "Open"
msgstr "開く"

#: templates/branches/hours.html:8
msgctxt "adjective"
msgid "Open"
msgstr "開館中"
'''

# An older Brazilian Portuguese catalog, from the 4.1 template: some
# messages have changed since and one is gone.
PT_BR = r'''# Brazilian Portuguese translation of Larkfield.
# Rafael Costa <rafael@example.com.br>, 2025.
#
msgid ""
msgstr ""
"Project-Id-Version: Larkfield 4.1\n"
"POT-Creation-Date: 2025-11-02 14:00+0000\n"
"PO-Revision-Date: 2025-11-09 20:31-0300\n"
"Last-Translator: Rafael Costa <rafael@example.com.br>\n"
"Language-Team: Portuguese (Brazil)\n"
"Language: pt_BR\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=2; plural=(n > 1);\n"

# Rafael: "acervo" reads better than "catálogo" here.
#: larkfield/views/catalog.py:39
msgid "Search the catalog"
msgstr "Pesquisar no acervo"

#: larkfield/views/catalog.py:55
#, python-format
msgid "%(count)d result for \"%(query)s\""
msgid_plural "%(count)d results for \"%(query)s\""
msgstr[0] "%(count)d resultado para \"%(query)s\""
msgstr[1] "%(count)d resultados para \"%(query)s\""

#: larkfield/views/loans.py:98
#, python-format
msgid "Return by %(date)s"
msgstr "Devolver até %(date)s"

#: templates/members/fines.html:14
#, fuzzy
msgid ""
"Fines are charged at 20 cents a day after a grace period of three days, up "
"to the replacement cost of the item."
msgstr ""
"As multas são de 20 centavos por dia após um prazo de carência de três "
"dias, até o custo de reposição do item."

#: larkfield/forms.py:21
msgid "Library card number"
msgstr "Número da carteirinha"

#: templates/base.html:16
msgid "Sign out"
msgstr "Sair"

#: templates/base.html:17
msgid "My account"
msgstr "Minha conta"

#: templates/catalog/detail.html:11
msgid "Available"
msgstr "Disponível"

#: templates/catalog/detail.html:12
msgid "On loan"
msgstr "Emprestado"

#: larkfield/views/holds.py:80
#, python-format
msgid "%(n)d hold"
msgid_plural "%(n)d holds"
msgstr[0] "%(n)d reserva"
msgstr[1] "%(n)d reservas"

#: larkfield/views/renewals.py:12
msgid "Renew all"
msgstr "Renovar tudo"

#: larkfield/views/renewals.py:30
#, python-format
msgid "Renewed until %(date)s"
msgstr "Renovado até %(date)s"
'''

# A catalog kept in ISO-8859-1 by an older toolchain.
FR_LEGACY = r'''# Catalogue de la borne de prêt (ancien format).
#
msgid ""
msgstr ""
"Project-Id-Version: Larkfield kiosk 1.9\n"
"Language: fr\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=ISO-8859-1\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=2; plural=(n > 1);\n"

#: kiosk/screens.py:10
msgid "Place your card on the reader"
msgstr "Posez votre carte sur le lecteur"

#: kiosk/screens.py:22
msgid "Item checked out"
msgstr "Document emprunté"

#: kiosk/screens.py:23
#, python-format
msgid "%(n)d item checked out"
msgid_plural "%(n)d items checked out"
msgstr[0] "%(n)d document emprunté"
msgstr[1] "%(n)d documents empruntés"

#: kiosk/screens.py:40
msgid "Receipt"
msgstr "Reçu"

#: kiosk/screens.py:41
msgid "Please take your receipt"
msgstr "Veuillez prendre votre reçu"
'''

# A Spanish catalog compiled on a big-endian machine.
ES_MESSAGES = [
    ("", "Project-Id-Version: Larkfield 4.0\nLanguage: es\nMIME-Version: 1.0\n"
         "Content-Type: text/plain; charset=UTF-8\nContent-Transfer-Encoding: 8bit\n"
         "Plural-Forms: nplurals=2; plural=(n != 1);\nX-Legacy-Build\n"),
    ("Available", "Disponible"),
    ("Closed", "Cerrado"),
    ("My account", "Mi cuenta"),
    ("On loan", "Prestado"),
    ("Return by %(date)s", "Devolver antes del %(date)s"),
    ("Search the catalog", "Buscar en el catálogo"),
    ("Sign out", "Cerrar sesión"),
    ("adjective\x04Open", "Abierto"),
    ("%(n)d hold\x00%(n)d holds", "%(n)d reserva\x00%(n)d reservas"),
]

BAD = {
    "bad_quote.po": r'''msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\n"

msgid "Sign out"
msgstr "Click "Sign out" when you are done"
''',
    "bad_prev.po": r'''msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\n"

#, fuzzy
#| msgtxt "Due %(date)s"
msgid "Due on %(date)s"
msgstr "Fällig am %(date)s"
''',
    "bad_cont.po": r'''msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\n"

#, fuzzy
#| msgid
msgid "Renew all"
msgstr "Alle verlängern"
''',
    "bad_order.po": r'''msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\n"

msgstr "Abmelden"
msgid "Sign out"
''',
    "bad_line.po": r'''msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\n"

msgid "Closed"
msgstr "Geschlossen"
translated by hand, check later
''',
    "bad_index.po": r'''msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\n"

msgid "%(n)d hold"
msgid_plural "%(n)d holds"
msgstr[0] "%(n)d Vormerkung"
msgstr[x] "%(n)d Vormerkungen"
''',
    "bad_cont_quote.po": r'''msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\n"

msgid ""
"Line one "
"then "a quote" in line two"
msgstr ""
''',
}


def mo_bytes(messages, big_endian):
    e = ">" if big_endian else "<"
    n = len(messages)
    ids = b""
    strs = b""
    idx = []
    for k, v in messages:
        kb = k.encode("utf-8")
        vb = v.encode("utf-8")
        idx.append((len(kb), len(ids), len(vb), len(strs)))
        ids += kb + b"\0"
        strs += vb + b"\0"
    keystart = 28 + 16 * n
    valuestart = keystart + len(ids)
    out = struct.pack(e + "IIIIIII", 0x950412de, 0, n, 28, 28 + 8 * n, 0, keystart)
    for l1, o1, _, _ in idx:
        out += struct.pack(e + "II", l1, o1 + keystart)
    for _, _, l2, o2 in idx:
        out += struct.pack(e + "II", l2, o2 + valuestart)
    return out + ids + strs


JOBS = [
    # What the toolchain sees in each file.
    "detect\tdata/messages.pot",
    "detect\tdata/de.po",
    "detect\tdata/fr.po",
    "detect\tdata/ja.po",
    "detect\tdata/fr_legacy.po",
    "detect\tdata/legacy_es.mo",
    "detect\tdata/bad_magic.mo",
    # A translation status page.
    "stats\tdata/messages.pot",
    "stats\tdata/de.po",
    "stats\tdata/fr.po",
    "stats\tdata/ja.po",
    "stats\tdata/pt_BR.po",
    "stats\tdata/fr_legacy.po",
    "metadata\tdata/de.po",
    "metadata\tdata/messages.pot",
    "entries\tdata/de.po",
    "entries\tdata/ja.po",
    "entries\tdata/fr_legacy.po",
    # Lookups the web application makes.
    "find\tdata/de.po\tmsgid\tHolds",
    "find\tdata/de.po\tmsgid\tHolds\theading",
    "find\tdata/de.po\tmsgid\tOpen",
    "find\tdata/de.po\tmsgid\tOpen\tverb",
    "find\tdata/de.po\tmsgid\tOpen\tadverb",
    "find\tdata/de.po\tmsgstr\tVormerkungen",
    "find\tdata/de.po\tmsgid\tRenew all",
    "find-all\tdata/de.po\tmsgid\tRenew all",
    "find\tdata/ja.po\tmsgid\tOpen",
    "find\tdata/fr.po\tmsgid_plural\t%(n)d holds",
    "contains\tdata/fr.po\tHolds",
    "contains\tdata/fr.po\tHold\tbutton",
    "contains\tdata/fr.po\tHold",
    # Writing catalogs back out.
    "roundtrip\tdata/de.po",
    "roundtrip\tdata/fr.po",
    "roundtrip\tdata/ja.po",
    "roundtrip\tdata/messages.pot",
    "roundtrip\tdata/fr_legacy.po",
    "print\tdata/de.po\t78",
    "print\tdata/fr.po\t40",
    "print\tdata/ja.po\t0",
    "print\tdata/messages.pot\t60",
    "print\tdata/pt_BR.po\t120",
    # A reviewer clears and sets fuzzy flags.
    "fuzzy\tdata/de.po\tReturn by %(date)s\ton",
    "fuzzy\tdata/de.po\t%(title)s is ready for pickup at %(branch)s until %(date)s.\toff",
    "fuzzy\tdata/fr.po\tAvailable\toff",
    "fuzzy\tdata/fr.po\tClosed\toff",
    # msgmerge against the new template.
    "merge\tdata/pt_BR.po\tdata/messages.pot\tdata/out/pt_BR.po",
    "merge\tdata/fr.po\tdata/messages.pot\tdata/out/fr.po",
    "merge\tdata/de.po\tdata/messages.pot\tdata/out/de.po",
    "merge\tdata/messages.pot\tdata/messages.pot\tdata/out/messages.pot",
    # Sorting a catalog the way polib's comparison orders entries.
    "sort\tdata/de.po",
    "sort\tdata/fr.po",
    # msgfmt.
    "compile\tdata/de.po\tdata/out/de.mo",
    "compile\tdata/fr.po\tdata/out/fr.mo",
    "compile\tdata/ja.po\tdata/out/ja.mo",
    "compile\tdata/fr_legacy.po\tdata/out/fr_legacy.mo",
    "compile\tdata/messages.pot\tdata/out/messages.mo",
    "mo\tdata/out/de.mo",
    "mo\tdata/out/fr_legacy.mo",
    "mo\tdata/legacy_es.mo",
    "mo\tdata/bad_magic.mo",
    "mo\tdata/rev2.mo",
    "mo\tdata/rev1.mo",
    "mo-to-po\tdata/legacy_es.mo\tdata/out/es.po",
    "mo-save\tdata/legacy_es.mo\tdata/out/es.mo",
    "po\tdata/out/es.po",
    # Broken catalogs.
    "po\tdata/bad_quote.po",
    "po\tdata/bad_prev.po",
    "po\tdata/bad_cont.po",
    "po\tdata/bad_order.po",
    "po\tdata/bad_line.po",
    "po\tdata/bad_index.po",
    "po\tdata/bad_cont_quote.po",
    "po\tdata/missing.po",
    # The helpers.
    "escape\tTab⇥and newline⏎and \"quotes\" and back\\slash",
    "unescape\tTab\\tand newline\\nand \\\"quotes\\\" and \\\\n and \\q",
    "natural-sort\tX-Poedit-SearchPath-10 X-Poedit-SearchPath-9 x-alpha X-Beta item2 item10 Item1 item1b",
]


def main():
    os.makedirs(os.path.join(DATA, "out"), exist_ok=True)
    texts = {
        "messages.pot": POT,
        "de.po": DE,
        "fr.po": FR,
        "ja.po": "\ufeff" + JA,
        "pt_BR.po": PT_BR,
    }
    for name, text in texts.items():
        with open(os.path.join(DATA, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    with open(os.path.join(DATA, "fr_legacy.po"), "w", encoding="latin-1", newline="\n") as f:
        f.write(FR_LEGACY)
    for name, text in BAD.items():
        with open(os.path.join(DATA, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    with open(os.path.join(DATA, "legacy_es.mo"), "wb") as f:
        f.write(mo_bytes(ES_MESSAGES, True))
    small = mo_bytes(ES_MESSAGES[:3], False)
    with open(os.path.join(DATA, "bad_magic.mo"), "wb") as f:
        f.write(b"\x95\x04\x12\xdf" + small[4:])
    with open(os.path.join(DATA, "rev2.mo"), "wb") as f:
        f.write(small[:4] + struct.pack("<I", 0x00020000) + small[8:])
    with open(os.path.join(DATA, "rev1.mo"), "wb") as f:
        f.write(small[:4] + struct.pack("<I", 0x00010001) + small[8:])
    with open(os.path.join(DATA, "jobs.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(JOBS) + "\n")
    # The files the program carries, in the order it writes them.
    names = sorted(n for n in os.listdir(DATA) if os.path.isfile(os.path.join(DATA, n)))
    with open(os.path.join(DATA, "files.txt"), "w", newline="\n") as f:
        f.write("\n".join(n for n in names if n != "files.txt") + "\n")


main()
