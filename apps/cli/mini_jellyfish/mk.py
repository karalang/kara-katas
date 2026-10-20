# Writes data/: jellyfish's own test vectors (testdata/), names to encode
# and pairs to compare, the inputs of four programs built on jellyfish (a
# customer-record deduplicator, a "did you mean" for mistyped commands, a
# surname search for a genealogy index and a fuzzy product lookup), and
# data/jobs.tsv, the jobs mini_jellyfish.kara and oracle.py run.
import os
import random
import shutil
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

# The blocks mini_jellyfish.kara carries NFKD tables for (tables.py
# writes them); every other character must be its own NFKD form.
from tables import table  # noqa: E402

NFKD = dict(table())


def write(rel, text):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def covered(s):
    return "".join(NFKD.get(c, c) for c in s) == unicodedata.normalize("NFKD", s)


NAMES = [
    "Robert", "Rupert", "Rubin", "Ashcraft", "Ashcroft", "Tymczak", "Pfister", "Honeyman", "Lee", "Gutierrez",
    "Jackson", "Washington", "O'Brien", "OBrien", "MacDonald", "McDonald", "Macintosh", "Knight", "Night",
    "Schmidt", "Schmitt", "Smith", "Smyth", "Schneider", "Snyder", "Müller", "Mueller", "Muller", "Möller",
    "José", "Jose", "García", "Garcia", "Núñez", "Nunez", "François", "Francois", "Lefèvre", "Lefebvre",
    "Wójcik", "Wojcik", "Ødegaard", "Øvrebø", "Yılmaz", "Nguyễn", "Nguyen", "Đặng", "Παπαδόπουλος",
    "Иванов", "王", "Smith-Jones", "van der Berg", "Van Der Berg", "D'Angelo", "DAngelo", "ﬁnn", "Ⅻ", "ＪＯＨＮ",
    "Phillips", "Philips", "Pfeiffer", "Kendrick", "Kenrick", "Thompson", "Thomson", "Xavier", "Ximenez",
    "Whitaker", "Wright", "Gnome", "Psmith", "Aeschylus", "Chiang", "Michael", "Mikhail", "Shaughnessy",
    "Schultz", "Schulz", "Evans", "Evens", "Catherine", "Kathryn", "Katherine", "Cathryn", "Haley", "Hayley",
    "Bailey", "Baily", "Dwight", "Hughes", "Hugh", "Zimmerman", "Szymański", "Straße", "Strasse", "Ängström",
    "Æsir", "Œuvre", "Łukasz", "Lukasz", "Ian", "Iain", "Ewan", "Euan", "Sean", "Shawn", "Shaun", "Zoë",
    "Chloé", "Renée", "Rene", "Kristin", "Christine", "Scherbatsky", "Tschaikowsky", "Ritchie", "Richey",
    "Gaston", "Ghislaine", "Sigh", "Dodge", "Judge", "Edge", "Science", "Tiara", "Nation", "Wheat", "Whale",
    "Moore", "Moor", "Matthews", "Mathews", "Kaye", "Kay", "Tchaikovsky", "  padded  ", "",
    "a b c", "x", "AH", "ah",
]

PAIRS = [
    ("martha", "marhta"), ("dwayne", "duane"), ("dixon", "dicksonx"), ("jones", "johnson"), ("abcvwxyz", "cabvwxyz"),
    ("jellyfish", "smellyfish"), ("kitten", "sitting"), ("Saturday", "Sunday"), ("José", "Jose"), ("Müller", "Mueller"),
    ("ca", "abc"), ("abcdef", "badcfe"), ("", ""), ("a", ""), ("", "abc"), ("same", "same"), ("Ølsen", "Olsen"),
    ("Straße", "Strasse"), ("123 Main St", "123 Main Street"), ("Apt 4B", "Apartment 4-B"),
    ("Catherine", "Kathryn"), ("Michael", "Mikhail"), ("Smith", "Smyth"), ("Tim", "Timothy"),
    ("Marie Helene", "Maria Rio"), ("Shackleford", "Shackelford"), ("Dunningham", "Cunnigham"),
    ("Nichleson", "Nichulson"), ("Massey", "Massie"), ("Abroms", "Abrams"), ("Hardin", "Martinez"),
    ("Itman", "Smith"), ("Jeraldine", "Geraldine"), ("Marhta", "Martha"), ("Michelle", "Michael"),
    ("Julies", "Julius"), ("Tanya", "Tonya"), ("Dwayne", "Duane"), ("Sean", "Susan"), ("Jon", "John"),
    ("Jon", "Jan"), ("Brookhaven", "Brrokhaven"), ("Brook Hallow", "Brook Hllw"), ("Decatur", "Decatir"),
    ("Fitzrureiter", "Fitzenreiter"), ("Higbee", "Highee"), ("Higbee", "Higvee"), ("Lacura", "Locura"),
    ("Iowa", "Iona"), ("1st", "IST"), ("Nguyễn", "Nguyen"), ("北京", "北京市"), ("👍🏽ok", "👍ok"),
    ("orangutan-kumquat", "orangutan kumquat"), ("aaaa", "aaaaa"), ("pneumonoultramicroscopic", "pneumonoultramicroscopik"),
]

# --------------------------------------------------- customer records

FIRST = ["John", "Jon", "Jonathan", "Catherine", "Katherine", "Kathryn", "Michael", "Mikael", "Sara", "Sarah",
         "Steven", "Stephen", "Zoë", "Zoe", "Luis", "Louis", "Aisha", "Ayesha", "Mohammed", "Muhammad", "Wei",
         "Li", "José", "Jose", "Anne", "Ann", "Bjørn", "Bjorn", "Siobhan", "Shivaun", "Francois", "François"]
LAST = ["Smith", "Smyth", "Schmidt", "Johnson", "Jonson", "Müller", "Mueller", "Garcia", "García", "Nguyen",
        "Nguyễn", "O'Brien", "OBrien", "MacDonald", "McDonald", "Thompson", "Thomson", "Lefèvre", "Lefebvre",
        "Kowalski", "Kowalsky", "Andersson", "Anderson", "Okafor", "Okafur", "Rossi", "Russo", "Haddad", "Hadad"]
CITIES = ["Leeds", "Lyon", "Austin", "Kraków", "Toronto", "Porto", "Osaka", "Nairobi"]


def typo(r, s):
    if len(s) < 3:
        return s
    k = r.randrange(4)
    i = r.randrange(1, len(s) - 1)
    if k == 0:
        return s[:i] + s[i + 1] + s[i] + s[i + 2:]
    if k == 1:
        return s[:i] + s[i + 1:]
    if k == 2:
        return s[:i] + s[i] + s[i:]
    return s[:i] + r.choice("aeiou") + s[i + 1:]


def customers(r):
    rows = []
    people = []
    for _ in range(26):
        f, l = r.choice(FIRST), r.choice(LAST)
        email = "%s.%s%d@%s" % (f.lower()[:4], l.lower()[:5], r.randrange(100), r.choice(["mail.com", "corp.io"]))
        people.append((f, l, email, r.choice(CITIES)))
    n = 1
    for f, l, email, city in people:
        rows.append((n, f, l, email, city))
        n += 1
        for _ in range(r.choice([0, 0, 1, 1, 2])):
            k = r.random()
            f2 = typo(r, f) if k < 0.3 else (f.upper() if k < 0.4 else f)
            l2 = typo(r, l) if 0.3 <= k < 0.7 else l
            e2 = typo(r, email) if r.random() < 0.4 else email
            rows.append((n, f2, l2, e2, city))
            n += 1
    r.shuffle(rows)
    lines = ["id,first,last,email,city"]
    for row in rows:
        lines.append(",".join(str(x) if "," not in str(x) else '"%s"' % x for x in row))
    return "\n".join(lines) + "\n"


COMMANDS = ["add", "am", "archive", "bisect", "blame", "branch", "checkout", "cherry-pick", "clean", "clone",
            "commit", "config", "describe", "diff", "fetch", "format-patch", "gc", "grep", "init", "log", "merge",
            "mv", "notes", "pull", "push", "range-diff", "rebase", "reflog", "remote", "reset", "restore", "revert",
            "rm", "shortlog", "show", "sparse-checkout", "stash", "status", "submodule", "switch", "tag", "worktree"]
TYPOS = ["stauts", "comit", "comitt", "psuh", "pul", "chekcout", "checkotu", "brnach", "rebse", "stsh", "lgo",
         "dif", "merg", "cloen", "fecth", "tga", "sttaus", "statsu", "cherrypick", "cherry_pick", "sparsecheckout",
         "xyzzy", "ad", "rm", "reflg", "blam", "submodlue", "worktee", "swich", "restroe", "resset", "bisec",
         "configure", "describ", "grpe", "initt", "a", "STATUS", "Push"]

PRODUCTS = ["Wireless Mouse", "Wired Mouse", "Mechanical Keyboard", "USB-C Hub", "USB-C Cable 2m", "HDMI Cable",
            "27\" Monitor", "Laptop Stand", "Webcam 1080p", "Noise-Cancelling Headphones", "Bluetooth Speaker",
            "Desk Lamp", "Ergonomic Chair", "Standing Desk", "Monitor Arm", "Café Mug", "Notebook A5"]
QUERIES = ["wireles mouse", "mechanicl keybord", "usb c hub", "hdmi", "cafe mug", "laptop stnd", "web cam",
           "headphone", "speeker", "chair", "desk", "monitr", "note book", "keyboard mechanical", "zzz"]


def main():
    if os.path.isdir(DATA):
        shutil.rmtree(DATA)
    jobs = []
    for name in sorted(os.listdir(os.path.join(HERE, "testdata"))):
        if not name.endswith(".csv"):
            continue
        with open(os.path.join(HERE, "testdata", name), encoding="utf-8") as f:
            write("testdata/" + name, f.read())
        jobs.append(["vectors", "testdata/" + name])
    write("names.txt", "\n".join(NAMES) + "\n")
    jobs.append(["encode", "names.txt"])
    write("pairs.tsv", "".join("%s\t%s\n" % p for p in PAIRS))
    jobs.append(["compare", "pairs.tsv"])
    r = random.Random(151)
    for k in range(3):
        write("customers%d.csv" % k, customers(r))
        jobs.append(["dedupe", "customers%d.csv" % k])
    write("commands.txt", "\n".join(COMMANDS) + "\n")
    write("typos.txt", "\n".join(TYPOS) + "\n")
    jobs.append(["suggest", "commands.txt", "typos.txt"])
    surnames = sorted(set(LAST + NAMES[:60]) - {""})
    write("surnames.txt", "\n".join(surnames) + "\n")
    write("queries.txt", "\n".join(["Smith", "Myller", "Garsia", "Nguyen", "Obrian", "Mcdonald", "Tomson",
                                     "Leferve", "Kovalski", "Ashcroft", "Zzyzx", "Rossi", "Knigt"]) + "\n")
    jobs.append(["search", "surnames.txt", "queries.txt"])
    write("products.txt", "\n".join(PRODUCTS) + "\n")
    write("product_queries.txt", "\n".join(QUERIES) + "\n")
    jobs.append(["lookup", "products.txt", "product_queries.txt"])
    write("jobs.tsv", "".join("\t".join(j) + "\n" for j in jobs))
    for root, _, files in os.walk(DATA):
        for f in files:
            with open(os.path.join(root, f), encoding="utf-8") as fh:
                for line in fh.read().splitlines():
                    assert covered(line) and covered(line.lower()), "no NFKD table for %r" % line


main()
