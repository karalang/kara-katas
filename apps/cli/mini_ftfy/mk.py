#!/usr/bin/env python3
"""Writes data/jobs.tsv: a cleanup pass over the text a support desk
collects from its inboxes, web forms and old exports (customer messages,
product reviews, names and addresses in a dozen languages), as calls on
ftfy.

Each line is one op, tab-separated: "job<TAB>name" starts a job; any other
line is a call, "<function><TAB><arg>...". A positional argument is
"s:<hex>" (a str, UTF-8 in hex), "y:<hex>" (bytes), "p:<plan>" (a list of
(step, parameter) tuples, written "step,param;step,param"), "b:0"/"b:1",
"i:<int>" or "n" (None). A keyword argument is "<name>=<value>" with the
value written the same way.

The mojibake is made here the way it happens in the wild: UTF-8 bytes
decoded with the wrong single-byte codec, sometimes twice, sometimes with
the bytes the codec has no character for replaced by U+FFFD, or with
U+00A0 turned into a plain space by an editor along the way.

Run: python3 -s -P -B mk.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LINES = []


def s(text):
    return "s:" + text.encode("utf-8").hex()


def y(data):
    return "y:" + data.hex()


def p(plan):
    return "p:" + ";".join(a + "," + b for a, b in plan)


def b(v):
    return "b:1" if v else "b:0"


def job(name):
    LINES.append("job\t" + name)


def call(fn, *args, **kwargs):
    fields = [fn] + list(args) + ["%s=%s" % kv for kv in kwargs.items()]
    LINES.append("\t".join(fields))


def sloppy(data, codec):
    """Decode bytes the way a "sloppy" Windows codec does: a byte the
    codec has no character for becomes the Latin-1 character instead."""
    out = []
    for byte in data:
        try:
            out.append(bytes([byte]).decode(codec))
        except UnicodeDecodeError:
            out.append(chr(byte))
    return "".join(out)


def lossy(data, codec):
    return data.decode(codec, errors="replace")


def mojibake(text, codec):
    data = text.encode("utf-8")
    if codec.startswith("cp125"):
        return sloppy(data, codec)
    return data.decode(codec)


# ---------------------------------------------------------------- texts

MESSAGES = [
    "Café crème, s'il vous plaît.",
    "Le colis est arrivé à Montréal — merci !",
    "¿Dónde está mi pedido? Lo pagué el miércoles.",
    "Die Lieferung für Herrn Müller kam nicht an. Grüße aus Köln",
    "Não consegui acessar a conta. Obrigado pela atenção",
    "Zamówienie nr 4411 nie dotarło do Łodzi.",
    "Dobrý den, objednávka přišla poškozená.",
    "Здравствуйте! Заказ не пришёл.",
    "Ευχαριστώ για τη γρήγορη απάντηση",
    "Siparişim hâlâ gelmedi, lütfen yardım edin.",
    "Ačiū, prekės gautos laiku.",
    "Paldies par ātro piegādi!",
    "注文がまだ届いていません。",
    "我的订单什么时候发货？",
    "Great product \u2014 5 stars \u2b50\u2b50\u2b50\u2b50\u2b50",
    "It\u2019s \u201cperfect\u201d \u2026 really \U0001f44d",
    "Price: 25 \u20ac (was 30 \u20ac) \u2022 free shipping",
    "Temperature range: \u221240\u00b0C to +85\u00b0C, \u00b10.5\u00b0",
    "\u00bfQu\u00e9? \u00a1Incre\u00edble!",
    "na\u00efve r\u00e9sum\u00e9 co\u00f6perate",
    "\u00e0 la mode, \u00e0 bient\u00f4t",
    "Size: 10\u00bd \u00d7 4\u00bc in",
    "Tsch\u00fc\u00df",
    "\u00c5ngstr\u00f6m",
    "\u0160koda \u017dilina",
]

ENCODINGS = ["latin-1", "cp1252", "cp1251", "cp1250", "cp1253", "cp1254",
             "cp1257", "iso-8859-2", "mac-roman", "cp437"]

# ---------------------------------------------------------------- jobs

job("support inbox")
for text in [
    "âœ” No problems",
    "&macr;\\_(ã\x83\x84)_/&macr;",
    "Broken text&hellip; it&#x2019;s ﬂubberiﬁc!",
    "ＬＯＵＤ　ＮＯＩＳＥＳ",
    "sÃ³",
    "voilÃ le travail",
    "schÃ¶n",
    "Ã la mode",
    "Ã  la mode",
    "fÃ cil",
    "Ã s vezes, Ã quele dia",
    "â€œquotedâ€\x9d",
    "â€œ like this â€�",
    "The Mona Lisa doesnÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢t have eyebrows.",
    "Ã¨Ã©Ã®Ã¯",
    "Ã¨ Ã© Ã® Ã¯",
    "This â€” should be an em dash",
    "Ð¿Ñ€Ð¸Ð²ÐµÑ‚",
    "Ð\xa0Ð¾ÑÑÐ¸Ñ",
    "ÐŸÑ€Ð¸Ð²ÐµÑ‚ Ð¼Ð¸Ñ€",
    "ã“ã‚“ã«ã¡ã¯",
    "Ã°Å¸Ëœâ€š",
    "Ã°Å¸â€˜Â",
    "IÃ±tÃ«rnÃ¢tiÃ´nÃ\xa0lizÃ¦tiÃ¸n",
    "Ã¢â‚¬Å“hello Ã¢â‚¬Â",
    "\x84Handwerk bringt dich \xfcberall hin\x93: Von der YOU bis nach Monaco",
    "Lo\x92s Angeles",
    "kÃ¶nnen Ã¼ber",
    "CÃ´te dâ€™Ivoire",
    "PÃ©rez &EACUTE;TÃ‰",
    "P&EACUTE;REZ",
    "BUNDESSTRA&SZLIG;E",
    "&ntilde; &Ntilde; &NTILDE; &nTILDE;",
    "&lt;b&gt;bold&lt;/b&gt;",
    "<p>AT&amp;T &lt;rocks&gt;</p>",
    "\x1b[36;44mI'm blue, da ba dee\x1b[0m",
    "\ufeffWhere do you want to go today?",
    "Line one\r\nLine two\rLine three\u2028Line four\u2029Line five\x85end",
    "ﬂuﬃeﬆ ﬁnancial oﬃce",
    "Ｕﾀｰﾝ ｶﾀｶﾅ ﾊﾟﾋﾟ",
    "\u201chere\u2019s a test\u201d \u2018single\u201b",
    "tab\there\x00nul\x07bell\x7fdel\u200bzwsp\u206aold\ufffcobj",
    "e\u0301te\u0301 cafe\u0301 n\u0303",
    "\u1100\u1161\u11a8 \u1112\u1161\u11ab\u1100\u1173\u11af",
    "ＡＢＣ　１２３　！？",
    "",
    "plain ascii text",
    "already fine: café, naïve, 東京",
    "\u0130stanbul ve \u00e7ok g\u00fczel",
]:
    call("fix_text", s(text))
    call("fix_and_explain", s(text))

job("wrong codec")
for text in MESSAGES:
    for codec in ENCODINGS:
        try:
            bad = mojibake(text, codec)
        except UnicodeDecodeError:
            continue
        call("fix_and_explain", s(bad))

job("twice wrong")
for text in MESSAGES[:12]:
    once = mojibake(text, "cp1252")
    twice = sloppy(once.encode("utf-8"), "cp1252")
    call("fix_and_explain", s(twice))
    call("fix_text", s(twice))
    once = mojibake(text, "latin-1")
    call("fix_and_explain", s(sloppy(once.encode("utf-8"), "cp1252")))

job("lost bytes")
for text in MESSAGES:
    data = text.encode("utf-8")
    bad = lossy(data, "cp1252")
    call("fix_and_explain", s(bad))
    call("fix_text", s(bad.replace("\ufffd", "?")))
    nbsp = sloppy(data, "cp1252").replace("\xa0", " ")
    call("fix_and_explain", s(nbsp))

job("mixed lines")
for i in range(0, len(MESSAGES) - 2, 3):
    good = MESSAGES[i]
    bad = mojibake(MESSAGES[i + 1], "cp1252")
    bad2 = mojibake(MESSAGES[i + 2], "cp1251")
    call("fix_text", s(good + "\n" + bad + "\n" + bad2 + "\n"))
    call("fix_and_explain", s(good + " | " + bad))
    call("fixes.decode_inconsistent_utf8", s(good + " | " + bad))
call("fix_text", s("&lt;b&gt;\n<i>x</i> &amp;\n&lt;c&gt;"))
call("fix_text", s("&lt;b&gt;\n&amp;\n<i>x</i> &amp;"))
call("fix_text", s("Ã©Ã©Ã©Ã©Ã©Ã©Ã©Ã©"), max_decode_length="i:4")
call("fix_text", s("Ã©Ã©\nÃ©Ã©\r\nÃ©Ã©"), max_decode_length="i:3")

job("options")
SAMPLES = [
    "&lt;Ã©&gt; \u201cquote\u201d ﬁ ＡＢ\r\n",
    "\x1b[1mbold\x1b[0m and caf\u00e9 \u2014 e\u0301",
    "Ã¡\x9d \u2019 \ufb01 \uff21 \u3000 \u2028 \x00",
    "\u00c5 \u212b A\u030a \u1e9b\u0323 \u2460 \u00bd \uac00 \u3131",
]
for text in SAMPLES:
    for name, val in [
        ("unescape_html", b(False)), ("unescape_html", b(True)),
        ("unescape_html", s("auto")), ("remove_terminal_escapes", b(False)),
        ("fix_encoding", b(False)), ("restore_byte_a0", b(False)),
        ("replace_lossy_sequences", b(False)),
        ("decode_inconsistent_utf8", b(False)), ("fix_c1_controls", b(False)),
        ("fix_latin_ligatures", b(False)), ("fix_character_width", b(False)),
        ("uncurl_quotes", b(False)), ("fix_line_breaks", b(False)),
        ("fix_surrogates", b(False)), ("remove_control_chars", b(False)),
        ("normalization", s("NFD")), ("normalization", s("NFKC")),
        ("normalization", s("NFKD")), ("normalization", "n"),
        ("explain", b(False)),
    ]:
        call("fix_and_explain", s(text), **{name: val})
    call("fix_text", s(text), uncurl_quotes=b(False), normalization=s("NFKC"))
    call("fix_text_segment", s(text))
call("fix_text", s("x"), normalization=s("NFX"))
call("fix_text", s("x"), colour=b(True))
call("fix_text", y(b"caf\xc3\xa9"))
call("fix_and_explain", y(b"caf\xc3\xa9"))

job("normalization")
for text in [
    "\u00c5 \u212b A\u030a \u1e9b\u0323 \u0071\u0307\u0323",
    "\u1e0b\u0323 \u1e0d\u0307 d\u0323\u0307 d\u0307\u0323",
    "\uac00\u11a8 \u1100\u1161\u11a8 \uac01 \u1100\u1161 \ud7a3",
    "\u0958 \u2126 \u00c7\u0301 \u0344 \u0f73 \u0f75",
    "\ufb03 \u2460 \u00bd \u33c2 \u2075 \u1d2c \u2122 \u2163",
    "\ufdfa \u3300 \uff76\uff9e \u2dee \u0385",
    "a\u0328\u0301\u0331 \u05d0\u05b8\u05b7 \u0e40\u0e01\u0e48\u0e32",
    "\u1f80\u0345 \u03b1\u0313\u0300\u0345 \u0390",
    "\U0001d15e \U0001d160 \U0001f1ef\U0001f1f5 \U0002f800",
]:
    for form in ["NFC", "NFD", "NFKC", "NFKD"]:
        call("fix_text", s(text), normalization=s(form))

job("html entities")
for text in [
    "&lt;tag&gt;", "&Jscr;ohn &HilbertSpace;ancock", "&checkmark;",
    "P&eacute;rez", "&AMP; &amp &amp; &AmP;", "this&not that",
    "&#65;&#x42;&#X43;&#0;&#1;&#128;&#150;&#x80;&#xD800;&#1114112;",
    "&#99999999999999999999; &#x110000; &#65abc; &#x41g; &#abc;",
    "&#13; &#x0D; &#127; &#xFDD0; &#xFFFE; &#x1F600; &#x10FFFF;",
    "&EURO; &euro; &COPY; &Copy; &copy; &AElig; &AELIG; &aelig;",
    "&SZLIG; &szlig; &IEXCL; &NBSP; &nbsp; &SHY;",
    "&abcdefghijklmnopqrstuvwxyz; &a; &;",
    "&NotNestedGreaterGreater; &nGt; &ngE;",
    "&ACIRC;&ATILDE;&SUP3;",
]:
    call("fixes.unescape_html", s(text))

job("fixers")
for fn, texts in [
    ("fixes.remove_terminal_escapes", [
        "\x1b[36;44mblue\x1b[0m", "\x1b[1;31;4mred\x1b[m \x1b[2J",
        "\x1b[\u0661\u0662mdigits\x1b[0m", "\x1b(B kept", "\x1b[3;x"]),
    ("fixes.uncurl_quotes", [
        "\u201chere\u2019s a test\u201d", "\u02bcokina \u201b\u201f",
        "\u00abguillemets\u00bb \u201e\u201a"]),
    ("fixes.fix_latin_ligatures", [
        "ﬂuﬃeﬆ", "\u0132SSEL \u0133s \u01c4 \u01c5 \u01c6 \u01c9 \u01cc \u0149",
        "\u00e6 \u0153 \ufb05"]),
    ("fixes.fix_character_width", [
        "ＬＯＵＤ　ＮＯＩＳＥＳ", "Ｕﾀｰﾝ", "\uffe0\uffe1\uffe5\uffe6 \uffe8\uffee",
        "\uff9e\uff9f \uffa0\uffa1\uffdc"]),
    ("fixes.fix_line_breaks", [
        "a\r\nb\rc\u2028d\u2029e\x85f", "\r\r\n\n\r", "no breaks"]),
    ("fixes.remove_control_chars", [
        "a\x00b\x08c\td\ne\x0bf\x0cg\rh\x0ei\x1fj\x7fk",
        "\u206a\u206f\ufeff\ufff9\ufffb\ufffc\ufffd\u200d\u202e",
        "\x80\x9f\u2028"]),
    ("fixes.remove_bom", [
        "\ufeff\ufeffstart\ufeff", "none"]),
    ("fixes.decode_escapes", [
        "\\u20a1 is the currency symbol for the col\u00f3n.",
        "\\x41\\x42 \\101\\7\\777 \\U0001F600 \\n\\t\\\\ \\' \\\" \\a\\b\\f\\v\\r",
        "\\q \\x4 \\u12 caf\\xe9", "\\x4z", "\\xzz", "\\u12zz",
        "\\U0000004g", "\\U00110000", "\\x\u00e9z", "\\u1\u20acz9"]),
    ("fixes.fix_c1_controls", [
        "\x80\x81\x8d\x8f\x90\x93\x94\x9d\x9f", "Lo\x92s \x96 dash"]),
    ("fixes.fix_surrogates", ["no surrogates here \U0001f600"]),
]:
    for text in texts:
        call(fn, s(text))
for data in [b"\xc3 la", b"\xc3 quele", b"\xc3 s ", b"\xc3  x",
             b"\xc2 \xe2 \x80\xe2\x80 \xf0 \x9f\x98", b"\xf0\x9f \x98 \xce ",
             b"\xe0\x80 \xe1\x85 "]:
    call("fixes.restore_byte_a0", y(data))
for data in [b"\xe2\x80\x1a", b"\xe2\x1a\x9c", b"\xc3?", b"\xc4?",
             b"\xed\xa0\x1a\xed\xb0\x80", b"\xf0\x9f\x1a\x80", b"a\x1ab",
             b"\xe2\x1a\x1a", b"\xf4?\x80\x80"]:
    call("fixes.replace_lossy_sequences", y(data))

job("badness")
for text in MESSAGES + [
    "âœ” No problems", "Ã©", "Ã©t\u00e9", "\u00c3\u00a9", "Â£5",
    "\u00e0\u00b2", "\u221a\u00b1", "\u00d7\u00b2", "\u0432\u0402",
    "\u0413\u045e\u0412\u0402\u0412\u00a6x", "Ã\xa0", "a Ã ", "Ã ", "x.Â ",
    "\u03b2\u20ac\u2122", "\u0101\u20ac", "\u0152x \u0153A",
    "\u2500\u2502\u250c box \u2510\u2518", "(\u256f\u00b0\u25a1\u00b0)\u256f\ufe35 \u253b\u2501\u253b",
    "\u00c9\u00b0", "\u00d8\u00a8\u00d9\u0160",
]:
    call("badness.badness", s(text))
    call("badness.is_bad", s(text))

job("plans")
for text in ["schÃ¶n", "voilÃ le travail", "â€œ like this â€�",
             "Ð¿Ñ€Ð¸Ð²ÐµÑ‚", "\u00c3\u00a9 \u00c3\xa0"]:
    call("fix_encoding_and_explain", s(text))
    call("fix_encoding", s(text))
for text, plan in [
    ("schÃ¶n", [("encode", "latin-1"), ("decode", "utf-8")]),
    ("voilÃ le travail", [("encode", "latin-1"), ("transcode", "restore_byte_a0"), ("decode", "utf-8")]),
    ("â€œ like this â€�", [("encode", "sloppy-windows-1252"), ("transcode", "replace_lossy_sequences"), ("decode", "utf-8")]),
    ("Ð¿Ñ€Ð¸Ð²ÐµÑ‚", [("encode", "sloppy-windows-1252"), ("decode", "utf-8")]),
    ("&lt;Ã¶&gt;", [("apply", "unescape_html"), ("encode", "latin-1"), ("decode", "utf-8"), ("apply", "uncurl_quotes")]),
    ("\u00c3\u00a9", [("encode", "macroman")]),
    ("\u00c3\u00a9", [("encode", "cp437"), ("decode", "iso-8859-2")]),
    ("\u00c3\u00a9", [("encode", "iso-8859-2")]),
    ("\u00c3\x81", [("encode", "latin-1"), ("decode", "windows-1252")]),
    ("\u00c3\u00a9\u0100", [("encode", "latin-1")]),
    ("x\u0100", [("encode", "sloppy-windows-1252")]),
    ("\u00ff", [("encode", "latin-1"), ("decode", "utf-8")]),
    ("\u00ed\u00a0\u0080", [("encode", "latin-1"), ("decode", "utf-8-variants")]),
    ("ab\u00ed\u00a0\u00bd\u00ed\u00b8\u0080\u00c0\u0080", [("encode", "latin-1"), ("decode", "utf-8-variants")]),
    ("ok", [("encode", "utf-8"), ("decode", "sloppy-windows-1251")]),
    ("ok", [("encode", "klingon")]),
    ("ok", [("decode", "utf-8")]),
    ("ok", [("encode", "utf-8"), ("encode", "utf-8")]),
    ("ok", [("frobnicate", "utf-8")]),
    ("ok", [("apply", "fix_everything")]),
    ("ok", []),
]:
    call("apply_plan", s(text), p(plan))

job("guess bytes")
for data in [
    "caf\u00e9".encode("utf-8"), "caf\u00e9".encode("cp1252"),
    "caf\u00e9\r".encode("mac-roman"), "caf\u00e9\r\n".encode("cp1252"),
    "h\u00e9".encode("utf-16"), "h\u00e9".encode("utf-16-be"),
    b"\xfe\xff\x00h\x00\xe9", b"\xff\xfeh\x00\x3d\xd8\x00\xde",
    b"\xff\xfeh", b"\xff\xfe\x00\xd8", b"\xff\xfe\x00\xdca\x00",
    b"null \xc0\x80 here", b"\xed\xa0\xbd\xed\xb8\x80 cesu",
    b"\xed\xa0\x80 lone", b"\xc0", b"\x81\x8d\x8f\x90\x9d plain",
    b"", b"ascii",
]:
    call("guess_bytes", y(data))

job("tables")
LINES.append("table\tWIDTH_MAP")
LINES.append("table\tHTML_ENTITIES")

os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
with open(os.path.join(HERE, "data", "jobs.tsv"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(LINES) + "\n")
