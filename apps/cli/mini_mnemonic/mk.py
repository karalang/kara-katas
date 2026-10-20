# Writes data/: the twelve wordlists the package ships, BIP-39's test
# vectors (vendor/vectors.json) as a table, recovery backups as people
# write them (a two-column recovery sheet, a stamped steel plate of
# four-letter abbreviations, a Japanese card, a Korean phone note in
# NFC, Spanish typed without accents, a Russian phrase), phrases typed
# with a word missing, misspelt or swapped, a custom wordlist, and
# jobs.tsv, the jobs oracle.py and mini_mnemonic.kara run. The phrases
# are made with the package itself (vendor/mnemonic).
import hashlib
import json
import os
import shutil
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
sys.path.insert(0, os.path.join(HERE, "vendor"))
sys.dont_write_bytecode = True

from mnemonic import Mnemonic  # noqa: E402
from tables import nfkd  # noqa: E402

WORDLISTS = os.path.join(HERE, "vendor", "mnemonic", "wordlist")


def covered(s):
    return nfkd(s) == unicodedata.normalize("NFKD", s)


def write(rel, text):
    for line in text.splitlines():
        assert covered(line), "no NFKD table for %r" % line
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def entropy(seed, n):
    return hashlib.sha256(seed.encode()).digest()[:n]


EN = Mnemonic("english")


def phrase(lang, seed, n=16):
    return Mnemonic(lang).to_mnemonic(entropy(seed, n))


LANGS = [Mnemonic(lang) for lang in Mnemonic.list_languages()]


def settled(text):
    # detect_language walks the words as a set and names the first word
    # that leaves no language, so which word it names can change from run
    # to run. It cannot when the words leave some language between them,
    # or when exactly one word fits no language and the rest leave one.
    code = Mnemonic.normalize_string(text)
    fits = {w: set(m.language for m in LANGS if any(c.startswith(w) for c in m.wordlist)) for w in set(code.split())}
    if not fits or set.intersection(*fits.values()):
        return True
    none = [w for w, v in fits.items() if not v]
    rest = [v for w, v in fits.items() if v]
    return len(none) == 1 and (not rest or bool(set.intersection(*rest)))


def one_changed(lang, seed):
    # The first phrase with exactly one word that NFKD changes: the
    # package's NFC wordlist does not hold that word once it is
    # normalized, so detect_language names it.
    for k in range(100):
        p = phrase(lang, "%s%d" % (seed, k))
        if [unicodedata.normalize("NFKD", w) != w for w in p.split(" ")].count(True) == 1 and settled(p):
            return p
    raise AssertionError(lang)


def recovery_sheet():
    words = phrase("english", "sheet", 32).split(" ")
    lines = ["RECOVERY SEED - keep it secret, keep it safe", ""]
    for i in range(12):
        lines.append("%2d. %-12s %2d. %s" % (i + 1, words[i], i + 13, words[i + 12]))
    return "\n".join(lines) + "\n"


def steel_plate():
    words = phrase("english", "steel", 24).split(" ")
    return "".join("%02d %s\n" % (i + 1, w[:4].upper()) for i, w in enumerate(words))


def numbered(words, sep="\n"):
    return "".join("%d. %s%s" % (i + 1, w, sep) for i, w in enumerate(words))


def backups():
    out = {}
    out["recovery-sheet.txt"] = recovery_sheet()
    out["steel-plate.txt"] = steel_plate()
    out["japanese-card.txt"] = numbered(phrase("japanese", "card").split("　"))
    ko = [unicodedata.normalize("NFC", w) for w in phrase("korean", "phone").split(" ")]
    out["korean-phone-note.txt"] = "지갑 복구 단어\n" + numbered(ko)
    es = [unicodedata.normalize("NFKD", w).encode("ascii", "ignore").decode() for w in phrase("spanish", "accents").split(" ")]
    out["spanish-no-accents.txt"] = numbered(es)
    out["spanish.txt"] = numbered(phrase("spanish", "accents").split(" "))
    out["russian.txt"] = numbered(one_changed("russian", "ru").split(" "))
    fr = [unicodedata.normalize("NFC", w) for w in phrase("french", "nfc").split(" ")]
    out["french-nfc.txt"] = numbered(fr)
    out["abbreviated-mix.txt"] = "# typed on a phone, partly abbreviated\n" + " ".join(
        w if i % 3 else w[:4] for i, w in enumerate(phrase("english", "mix").split(" "))) + "\n"
    out["too-short.txt"] = numbered(phrase("english", "short").split(" ")[:11])
    return out


def typed():
    rows = []
    good = phrase("english", "typed").split(" ")
    rows.append(("english", " ".join(good)))
    w = list(good)
    w[11] = "?"
    rows.append(("english", " ".join(w)))
    w = list(good)
    w[2] = w[2][:-1]
    rows.append(("english", " ".join(w)))
    w = list(good)
    w[7] = w[7][:2] + w[7][3] + w[7][2] + w[7][4:]
    rows.append(("english", " ".join(w)))
    w = list(good)
    w[5], w[6] = w[6], w[5]
    rows.append(("english", " ".join(w)))
    w = list(good)
    w[0], w[9] = "satoshi", "nakamoto"
    rows.append(("english", " ".join(w)))
    w = list(good)
    w[3] = w[3].upper()
    rows.append(("english", " ".join(w)))
    long = phrase("english", "long", 32).split(" ")
    w = list(long)
    w[23] = "?"
    rows.append(("english", " ".join(w)))
    fr = phrase("french", "typed").split(" ")
    w = [unicodedata.normalize("NFC", x) for x in fr]
    w[10] = "?"
    rows.append(("french", " ".join(w)))
    it = phrase("italian", "typed").split(" ")
    it[1] = it[1] + "e"
    rows.append(("italian", " ".join(it)))
    return rows


def custom_list(n):
    return "".join("w%04d\n" % i for i in range(n))


def jobs():
    out = []
    vectors = json.load(open(os.path.join(HERE, "vendor", "vectors.json"), encoding="utf-8"))
    for lang in vectors:
        out.append(["vectors", lang])
    v0 = vectors["english"][0]
    out.append(["seed", v0[1], "TREZOR"])
    out.append(["seed", "Př\xedšerně žluťoučk\xfd kůň \xfapěl ď\xe1belsk\xe9 \xf3dy "
                "z\xe1keřn\xfd učeň běž\xed pod\xe9l z\xf3ny \xfalů",
                "Neuvěřitelně bezpečn\xe9 hesl\xedčko"])
    for lang, hx in [("english", "00" * 16), ("english", "7f" * 16), ("english", "ff" * 32), ("english", "80" * 20),
                     ("english", b"Lorem ipsum dolor sit amet amet.".hex()), ("english", "00" * 15), ("english", "00" * 33),
                     ("english", ""), ("japanese", "00" * 16), ("japanese", "a4" * 24), ("korean", "0f" * 28),
                     ("chinese_simplified", "77c2b00716cec7213839159e404db50d"), ("chinese_traditional", "77c2b00716cec7213839159e404db50d"),
                     ("czech", "18ab19a9f54a9274f03e5209a2ac8a91"), ("russian", "00" * 16), ("turkish", "ff" * 16),
                     ("spanish", "c0ba5a8e914111210f2bd131f3d5e08d"), ("portuguese", "ff" * 24), ("italian", "01" * 32)]:
        out.append(["to_mnemonic", lang, hx])
    for lang, p in [("english", v0[1]), ("english", "abandon " * 11 + "abandon"), ("english", "abandon " * 10 + "about"),
                    ("english", "legal winner thank year wave sausage worth useful legal winner thank yellow"),
                    ("english", "legal winner thank year wave sausage worth useful legal winner thank"),
                    ("english", "legal winner thank year wave sausage worth useful legal winner thank yell0w"),
                    ("english", "Legal winner thank year wave sausage worth useful legal winner thank yellow"),
                    ("english", "legal  winner thank year wave sausage worth useful legal winner thank yellow"),
                    ("english", " ".join(["zoo"] * 23 + ["vote"])),
                    ("french", unicodedata.normalize("NFC", phrase("french", "fr"))),
                    ("japanese", phrase("japanese", "jp")), ("japanese", phrase("japanese", "jp").replace("　", " ")),
                    ("korean", unicodedata.normalize("NFC", phrase("korean", "ko"))),
                    ("russian", phrase("russian", "ru0")), ("turkish", phrase("turkish", "tr2")),
                    ("spanish", phrase("spanish", "es").replace(" ", "　"))]:
        out.append(["check", lang, p])
        out.append(["to_entropy", lang, p])
        out.append(["to_entropy_split", lang, p])
    for lang, p in [("english", ""), ("english", " "), ("english", "access"), ("english", "acce"), ("english", "acb"),
                    ("english", "acc"), ("english", "act"), ("english", "acti"), ("english", "ZOO"), ("english", "zo"),
                    ("spanish", "abaco"), ("spanish", "ába"), ("spanish", "\xe1ba"), ("japanese", "あい"),
                    ("french", "abeil"), ("czech", "zv")]:
        out.append(["expand_word", lang, p])
    for lang, p in [("english", "access acce acb acc act acti"), ("english", "aban abil abl abo abov abs"),
                    ("english", "zoo  zo"), ("french", "aban abeil abor")]:
        out.append(["expand", lang, p])
    for text in ["security", "fruit wave dwarf", "fru wago dw", "fru wago dur enje", "jaguar xxxxxxx", "jaguar jaguar",
                 "jaguar security", "jaguar aboyer", "abandon about", "abandon aboutir", "fav financer", "fav finance",
                 "favor finan", "flanel", "flanela", "flane", phrase("japanese", "jp"), phrase("korean", "ko"),
                 unicodedata.normalize("NFC", phrase("korean", "ko")), phrase("chinese_simplified", "zh"),
                 phrase("chinese_traditional", "zh"), phrase("spanish", "es"), phrase("italian", "it"), phrase("portuguese", "pt"),
                 phrase("czech", "cs"), one_changed("russian", "ru"), one_changed("turkish", "tr"), "", "a", "zz"]:
        assert settled(text), "detect_language's answer for %r depends on set order" % text
        out.append(["detect", text])
    for hx, net in [("00" * 64, "main"), (hashlib.sha512(b"seed").hexdigest(), "main"), (hashlib.sha512(b"seed").hexdigest(), "test"),
                    ("00" * 63, "main"), ("00" * 65, "main"), ("", "main")]:
        out.append(["master", hx, net])
    for hx in ["", "00", "0001", "000001", "61", "626262", "516b6fcd0f", "ff" * 8, "00ff" * 6, "0488ade4" + "00" * 74]:
        out.append(["b58", hx])
    for n in ["128", "256", "100", "512", "0"]:
        out.append(["generate", n])
    for lang in ["english", "klingon", "../vectors", "English", ""]:
        out.append(["new", lang])
    out.append(["list_languages"])
    out.append(["custom", "custom/w.txt", "00" * 16])
    out.append(["custom", "custom/w.txt", "ff" * 32])
    out.append(["custom", "custom/short.txt", "00" * 16])
    for name in sorted(backups()):
        out.append(["backup", "backups/" + name])
    for lang, p in typed():
        out.append(["recover", lang, p])
    return out


def main():
    if os.path.isdir(DATA):
        shutil.rmtree(DATA)
    for name in sorted(os.listdir(WORDLISTS)):
        with open(os.path.join(WORDLISTS, name), encoding="utf-8") as f:
            write("wordlist/" + name, f.read())
    vectors = json.load(open(os.path.join(HERE, "vendor", "vectors.json"), encoding="utf-8"))
    write("vectors.tsv", "".join("%s\t%s\n" % (lang, "\t".join(v)) for lang in vectors for v in vectors[lang]))
    for name, text in backups().items():
        write("backups/" + name, text)
    write("custom/w.txt", custom_list(2048))
    write("custom/short.txt", custom_list(2047))
    write("jobs.tsv", "".join("\t".join(job) + "\n" for job in jobs()))


main()
