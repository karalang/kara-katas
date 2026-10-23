"""Write data/: the rapidfuzz jobs (one JSON array per line) and the inputs
of the three programs.

Run: python3 -s -P -B mk.py
"""
import json
import os
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
os.makedirs(D, exist_ok=True)

JOBS = []
TEXT = []


def section(title):
    JOBS.append("# " + title)


def job(*parts):
    for p in parts:
        if isinstance(p, str):
            TEXT.append(p)
    JOBS.append(json.dumps(list(parts), ensure_ascii=False))


def prog(line):
    JOBS.append("!" + line)


P = {"processor": "default"}

section("fuzz: the ten scorers on the pairs their documentation uses")
for a, b in [
    ("this is a test", "this is a test!"),
    ("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear"),
    ("fuzzy was a bear", "fuzzy fuzzy was a bear"),
    ("this is a test", "this is a test"),
    ("New York Mets", "New York Meats"),
    ("New York Mets vs Atlanta Braves", "Atlanta Braves vs New York Mets"),
    ("YANKEES", "NEW YORK YANKEES"),
    ("NEW YORK METS", "NEW YORK MEATS"),
    ("new york mets - atlanta braves", "atlanta braves new york mets"),
    ("purple elephant", "elephant"),
    ("Dallas Cowboys", "cowboys"),
    ("apple inc", "apple incorporated"),
    ("Microsoft Corporation", "Microsoft Corp."),
    ("Pfizer Inc.", "Pfizer"),
    ("the quick brown fox", "the fast brown dog"),
    ("Main Street", "Main St"),
    ("123 Main Street, Springfield", "123 Main St Springfield"),
    ("Café Rouge", "Cafe Rouge"),
    ("Zürich Hauptbahnhof", "Zurich HB"),
    ("João Silva", "Joao da Silva"),
    ("ab", "ba"),
    ("abc", "abcabc"),
    ("aaaa", "aa"),
    ("a b c d", "d c b a"),
    ("hello world", "world hello world"),
    ("algorithm", "logarithm"),
]:
    job("fuzz", "all", a, b)

section("fuzz: default_process strips punctuation and case first")
for a, b in [
    ("New York Mets!", "new york mets"),
    ("HELLO, WORLD", "hello world"),
    ("O'Reilly Media", "OReilly media"),
    ("e-mail", "email"),
    ("(555) 123-4567", "555.123.4567"),
    ("Ünïcödé Strasse", "ünïcödé strasse"),
    ("  padded  ", "padded"),
    ("snake_case_name", "snake case name"),
    ("Straße", "STRASSE"),
]:
    job("fuzz", "all", a, b)
    job("fuzz", "all", a, b, P)

section("fuzz: score_cutoff turns a lower score into 0")
for cut in [0, 50, 85, 90, 95.5, 99.99, 100, 101]:
    job("fuzz", "all", "fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear", {"score_cutoff": cut})
for cut in [60, 80.5, 100]:
    job("fuzz", "all", "Dallas Cowboys", "cowboys", {"score_cutoff": cut, "processor": "default"})
    job("fuzz", "all", "purple elephant", "elephant", {"score_cutoff": cut})

section("fuzz: empty, blank and one-character strings")
for a, b in [
    ("", ""),
    ("", "a"),
    ("a", ""),
    (" ", " "),
    ("   ", "a"),
    ("a", "a"),
    ("a", "b"),
    ("a", "ab"),
    ("!!!", "???"),
    ("x", "xxxxxxxxxxxxxxxxxxxx"),
    ("ab", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxab"),
    ("the the the", "the"),
    ("one two", "two one two one"),
]:
    job("fuzz", "all", a, b)
job("fuzz", "all", "!!!", "???", P)
job("fuzz", "all", "...", "abc", P)
job("fuzz", "all", "  ", "  ", P)

section("partial_ratio_alignment: where the shorter string sits in the longer")
for a, b in [
    ("a certain string", "cetain"),
    ("cetain", "a certain string"),
    ("purple elephant", "elephant"),
    ("elephant", "purple elephant"),
    ("abcd", "xxabcdxx"),
    ("ab", "ba"),
    ("abc", "cba"),
    ("hello", "world"),
    ("", ""),
    ("", "abc"),
    ("abc", "abc"),
    ("this is a test", "is a"),
    ("ERROR: connection refused", "connection refused by host 10.0.0.1"),
    ("bcd", "abcde"),
    ("xyz", "abc"),
]:
    job("align", a, b)
job("align", "Dallas Cowboys", "cowboys", P)
job("align", "abcd", "xxabcexx", {"score_cutoff": 80})
job("align", "abcd", "xxabcexx", {"score_cutoff": 70})
job("align", "abcd", "xxabcexx", {"score_cutoff": 75})

section("utils.default_process")
for s in [
    "Hello, World!",
    "  Lots   of   spaces  ",
    "C++ / C# / F#",
    "snake_case_stays",
    "Ünïcödé — dashes – and “quotes”",
    "über straße",
    "tab\tand\nnewline",
    "!!!",
    "",
    "MiXeD 123 CaSe",
    "e.g. i.e. etc.",
    "naïve café résumé",
    "Ελληνικά ΚΕΙΜΕΝΟ",
    "Привет, МИР",
    "日本語のテキスト",
    "x²+y³=z½",
    "price: $9.99 (€8.50)",
]:
    job("process", s)

section("distance metrics: distance, similarity and both normalized")
METRICS = ["Levenshtein", "Indel", "LCSseq", "Hamming", "Jaro", "JaroWinkler",
           "OSA", "DamerauLevenshtein", "Prefix", "Postfix"]
PAIRS = [
    ("kitten", "sitting"),
    ("lewenstein", "levenshtein"),
    ("ca", "abc"),
    ("abcdef", "badcfe"),
    ("martha", "marhta"),
    ("dixon", "dicksonx"),
    ("jellyfish", "smellyfish"),
    ("", ""),
    ("", "abc"),
    ("abc", "abc"),
    ("prefix_match", "prefix_other"),
    ("other_suffix", "match_suffix"),
    ("CRATE", "TRACE"),
    ("a", "b"),
    ("ab", "b"),
    ("DwAyNE", "DuANE"),
    ("Straße", "Strasse"),
]
for m in METRICS:
    for a, b in PAIRS:
        job("metric", m, a, b)

section("distance metrics: options")
for w in [[1, 1, 1], [1, 1, 2], [2, 1, 1], [1, 2, 1], [1, 1, 3], [3, 5, 7], [0, 1, 1], None]:
    job("metric", "Levenshtein", "kitten", "sitting", {"weights": w})
    job("metric", "Levenshtein", "sitting", "kitten", {"weights": w})
job("metric", "Levenshtein", "kitten", "sitting", {"weights": [1, 0, 1]})
job("metric", "Levenshtein", "", "abc", {"weights": [2, 3, 4]})
job("metric", "Levenshtein", "abc", "", {"weights": [2, 3, 4]})
for cut in [0, 1, 2, 3, 0.5, 0.6]:
    job("metric", "Levenshtein", "kitten", "sitting", {"score_cutoff": cut})
for cut in [0, 0.5, 0.9, 1]:
    job("metric", "Jaro", "martha", "marhta", {"score_cutoff": cut})
    job("metric", "JaroWinkler", "martha", "marhta", {"score_cutoff": cut})
for pw in [0.0, 0.1, 0.25, 1.0, 1.5, -0.1]:
    job("metric", "JaroWinkler", "prefix_match", "prefix_other", {"prefix_weight": pw})
for pw, cut in [(0.25, 0.95), (0.1, 0.99), (0.3, 0.9)]:
    job("metric", "JaroWinkler", "dwayne", "duane", {"prefix_weight": pw, "score_cutoff": cut})
job("metric", "Hamming", "karolin", "kathrin", {"pad": False})
job("metric", "Hamming", "abc", "abcde", {"pad": False})
job("metric", "Hamming", "abc", "abcde", {"pad": True})
job("metric", "Hamming", "", "", {"pad": False})
for m in ["Indel", "OSA", "DamerauLevenshtein", "Prefix", "Postfix", "LCSseq"]:
    job("metric", m, "Hello World", "hello world", P)
    job("metric", m, "Hello World", "hello world", {"score_cutoff": 2})

section("editops and opcodes")
for m in ["Levenshtein", "Indel", "LCSseq", "Hamming"]:
    for a, b in [
        ("qabxcd", "abycdf"),
        ("kitten", "sitting"),
        ("Levenshtein", "Lenvinsten"),
        ("", "abc"),
        ("abc", ""),
        ("abc", "abc"),
        ("spam", "park"),
        ("aaabbb", "ababab"),
    ]:
        job("ops", m, a, b)
job("ops", "Hamming", "abc", "abcd", {"pad": False})
job("ops", "Levenshtein", "Main Street", "main st", P)

section("process: extract, extractOne and extract_iter")
FRUIT = ["apple", "banana", "cherry", "grape", "pineapple", "apricot", "grapefruit", "blackberry"]
TEAMS = ["Atlanta Falcons", "New York Jets", "New York Giants", "Dallas Cowboys",
         "New England Patriots", "Las Vegas Raiders"]
job("extract", "new york jets", TEAMS, {})
job("extract", "new york jets", TEAMS, {"limit": 2})
job("extract", "new york jets", TEAMS, {"limit": None})
job("extract", "new york jets", TEAMS, {"limit": 1})
job("extract", "new york jets", TEAMS, {"limit": 0})
job("extractOne", "cowboys", TEAMS, {})
job("extractOne", "cowboys", TEAMS, {"processor": "default"})
job("extract", "cowboys", TEAMS, {"processor": "default", "score_cutoff": 50})
job("extract", "aple", FRUIT, {})
job("extract", "aple", FRUIT, {"scorer": "fuzz.ratio", "limit": 3})
job("extract", "aple", FRUIT, {"scorer": "fuzz.partial_ratio", "limit": None})
job("extract", "grape", FRUIT, {"scorer": "fuzz.token_set_ratio", "limit": None, "score_cutoff": 50})
job("extract_iter", "aple", FRUIT, {"scorer": "fuzz.QRatio", "score_cutoff": 60})
job("extract_iter", "apple", FRUIT, {"scorer": "fuzz.ratio"})
job("extractOne", "aple", FRUIT, {"scorer": "Levenshtein.distance"})
job("extract", "aple", FRUIT, {"scorer": "Levenshtein.distance", "limit": 4})
job("extract", "aple", FRUIT, {"scorer": "Levenshtein.distance", "score_cutoff": 3, "limit": None})
job("extract", "aple", FRUIT, {"scorer": "Levenshtein.distance", "limit": 3, "scorer_kwargs": {"weights": [1, 1, 2]}})
job("extract", "aple", FRUIT, {"scorer": "Levenshtein.normalized_distance", "limit": 3})
job("extract", "aple", FRUIT, {"scorer": "Levenshtein.similarity", "limit": 3})
job("extract", "aple", FRUIT, {"scorer": "Levenshtein.normalized_similarity", "limit": 3, "score_cutoff": 0.5})
job("extract", "grap", FRUIT, {"scorer": "JaroWinkler.similarity", "limit": 3})
job("extract", "grap", FRUIT, {"scorer": "JaroWinkler.similarity", "limit": 3, "scorer_kwargs": {"prefix_weight": 0.25}})
job("extractOne", "grap", FRUIT, {"scorer": "Jaro.distance"})
job("extract", "grap", FRUIT, {"scorer": "Prefix.similarity", "limit": 3})
job("extract", "berry", FRUIT, {"scorer": "Postfix.distance", "limit": 3})
job("extract", "chery", FRUIT, {"scorer": "OSA.distance", "limit": 2})
job("extract", "bnaana", FRUIT, {"scorer": "DamerauLevenshtein.distance", "limit": 2})
job("extract", "bnaana", FRUIT, {"scorer": "Indel.normalized_distance", "limit": 2})
job("extract", "bnaana", FRUIT, {"scorer": "LCSseq.similarity", "limit": 2})
job("extract", "aple", FRUIT, {"scorer": "Hamming.distance", "limit": 3})
job("extractOne", "apple", ["Apple", None, "APPLE", "apple"], {})
job("extractOne", "apple", ["Apple", None, "APPLE", "apple"], {"processor": "default"})
job("extract", "apple", ["Apple", None, "APPLE", "apple"], {"processor": "default"})
job("extractOne", "zzz", FRUIT, {"score_cutoff": 50})
job("extractOne", "zzz", FRUIT, {"scorer": "Levenshtein.distance", "score_cutoff": 2})
job("extract", "zzz", FRUIT, {"score_cutoff": 50})
job("extract", "ny jets", {"NYJ": "New York Jets", "NYG": "New York Giants", "DAL": "Dallas Cowboys"}, {})
job("extractOne", "giants", {"NYJ": "New York Jets", "NYG": "New York Giants", "DAL": "Dallas Cowboys"}, P)
job("extract", "anything", [], {})
job("extractOne", "anything", [], {})
job("extract", "", FRUIT, {"limit": 2})
job("extract", "", FRUIT, {"scorer": "fuzz.ratio", "limit": 2})

prog("dedupe data/vendors.txt")
prog("suggest data/commands.txt data/typos.txt")
prog("reconcile data/catalog.tsv data/orders.tsv")

VENDORS = """Acme Corporation
ACME Corp.
Acme Corp
Globex Inc
Globex, Inc.
Initech LLC
Initech
Umbrella Corporation
Umbrella Corp
Soylent Green Ltd
Soylent Green Limited
Stark Industries
Stark Industries Inc.
Wayne Enterprises
Wayne Enterprises, Inc
Wonka Industries
Cyberdyne Systems
Cyberdyne Systems Corp
Hooli
Hooli Inc
Pied Piper
Pied Piper, Inc.
Vandelay Industries
Vandelay Imports
Dunder Mifflin
Dunder-Mifflin Paper Company
Café Müller GmbH
Cafe Muller GmbH
Tyrell Corp
Tyrell Corporation
"""

COMMANDS = """add
bisect
branch
checkout
cherry-pick
clone
commit
diff
fetch
init
log
merge
pull
push
rebase
remote
reset
restore
revert
show
stash
status
switch
tag
"""

TYPOS = """comit
stauts
pul
psuh
chekout
rebse
brnach
statsu
mrege
clne
cherrypick
xyzzy
stsh
lgo
remtoe
"""

CATALOG = """SKU-1001\tApple iPhone 15 Pro 128GB Black Titanium
SKU-1002\tApple iPhone 15 128GB Blue
SKU-1003\tSamsung Galaxy S24 Ultra 256GB
SKU-1004\tGoogle Pixel 8 Pro 128GB Obsidian
SKU-1005\tSony WH-1000XM5 Wireless Headphones
SKU-1006\tBose QuietComfort Ultra Headphones
SKU-1007\tApple AirPods Pro (2nd generation)
SKU-1008\tLogitech MX Master 3S Mouse
SKU-1009\tDell XPS 13 Laptop 16GB RAM
SKU-1010\tLenovo ThinkPad X1 Carbon Gen 11
SKU-1011\tAnker PowerCore 10000 Portable Charger
SKU-1012\tKindle Paperwhite 16GB
"""

ORDERS = """A-501\tiphone 15 pro black 128 gb
A-502\tgalaxy s24 ultra
A-503\tsony wh1000xm5 headphones
A-504\tairpods pro 2
A-505\tmx master 3s
A-506\tthinkpad x1 carbon
A-507\tkindle paperwhite
A-508\tpixel 8 pro
A-509\tbose qc ultra
A-510\tanker power bank 10000mah
A-511\tusb-c cable 2m
A-512\tdell xps 13
"""

for name, text in [("vendors.txt", VENDORS), ("commands.txt", COMMANDS),
                   ("typos.txt", TYPOS), ("catalog.tsv", CATALOG),
                   ("orders.tsv", ORDERS)]:
    TEXT.append(text)
    with open(os.path.join(D, name), "w", encoding="utf-8") as f:
        f.write(text)

# Python's \w and str.isalnum() and the compiled side's char test agree on
# letters, digits and punctuation, but not on combining marks: keep those
# out.
for t in TEXT:
    for c in t:
        if ord(c) > 127:
            assert unicodedata.category(c)[0] in "LNPSZ", (c, t)
        assert not ("\x1c" <= c <= "\x1f"), t

with open(os.path.join(D, "jobs.jsonl"), "w", encoding="utf-8") as f:
    f.write("\n".join(JOBS) + "\n")
with open(os.path.join(D, "files.txt"), "w") as f:
    f.write("vendors.txt\ncommands.txt\ntypos.txt\ncatalog.tsv\norders.tsv\n")
print(len([j for j in JOBS if j[0] == "["]), "jobs")
