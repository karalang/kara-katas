# Writes data/jobs.tsv, the operations to run through inflection, and
# data/unicode.txt, the case mappings and compatibility decompositions of
# the characters those operations reach (from Python's unicodedata and
# str methods).
#
# jobs.tsv: a line `== name` starts a job; every other line is an
# operation, its fields separated by tabs. In a field, \t, \n and \\
# stand for a tab, a newline and a backslash. A number argument to
# ordinal and ordinalize is written i:<int>, f:<float>, b:<bool> or
# s:<str>.
import os
import random
import unicodedata

random.seed(20261019)

jobs = []


def job(name, ops):
    jobs.append((name, ops))


# Rails' own singular/plural pairs (activesupport's inflector test data
# and inflection's tests), as words a model, a route or a column is
# named with.
PAIRS = [
    ("search", "searches"), ("switch", "switches"), ("fix", "fixes"),
    ("box", "boxes"), ("process", "processes"), ("address", "addresses"),
    ("case", "cases"), ("stack", "stacks"), ("wish", "wishes"),
    ("fish", "fish"), ("jeans", "jeans"), ("funky jeans", "funky jeans"),
    ("my money", "my money"), ("category", "categories"), ("query", "queries"),
    ("ability", "abilities"), ("agency", "agencies"), ("movie", "movies"),
    ("archive", "archives"), ("index", "indices"), ("wife", "wives"),
    ("safe", "saves"), ("half", "halves"), ("move", "moves"),
    ("salesperson", "salespeople"), ("person", "people"), ("spokesman", "spokesmen"),
    ("man", "men"), ("woman", "women"), ("basis", "bases"),
    ("diagnosis", "diagnoses"), ("diagnosis_a", "diagnosis_as"), ("datum", "data"),
    ("medium", "media"), ("stadium", "stadia"), ("analysis", "analyses"),
    ("node_child", "node_children"), ("child", "children"), ("experience", "experiences"),
    ("day", "days"), ("comment", "comments"), ("foobar", "foobars"),
    ("newsletter", "newsletters"), ("old_news", "old_news"), ("news", "news"),
    ("series", "series"), ("species", "species"), ("quiz", "quizzes"),
    ("perspective", "perspectives"), ("ox", "oxen"), ("passerby", "passersby"),
    ("photo", "photos"), ("buffalo", "buffaloes"), ("tomato", "tomatoes"),
    ("potato", "potatoes"), ("dwarf", "dwarves"), ("elf", "elves"),
    ("information", "information"), ("equipment", "equipment"), ("criterion", "criteria"),
    ("foot", "feet"), ("goose", "geese"), ("crisis", "crises"),
    ("testis", "testes"), ("mouse", "mice"), ("louse", "lice"),
    ("house", "houses"), ("octopus", "octopi"), ("virus", "viri"),
    ("alias", "aliases"), ("status", "statuses"), ("bus", "buses"),
    ("axis", "axes"), ("vertex", "vertices"), ("matrix", "matrices"),
    ("shoe", "shoes"), ("horse", "horses"), ("prize", "prizes"),
    ("edge", "edges"), ("cow", "kine"), ("database", "databases"),
    ("human", "humans"), ("zombie", "zombies"), ("hive", "hives"),
    ("thesis", "theses"), ("synopsis", "synopses"), ("prognosis", "prognoses"),
    ("parenthesis", "parentheses"), ("sex", "sexes"), ("tive", "tives"),
]

ops = []
for i, (s, p) in enumerate(PAIRS):
    for w in (s,) + ((s.capitalize(),) if i % 2 == 0 else ()) + ((s.upper(),) if i % 4 == 0 else ()):
        ops.append(["pluralize", w])
    for w in (p,) + ((p.capitalize(),) if i % 2 == 1 else ()) + ((p.upper(),) if i % 4 == 2 else ()):
        ops.append(["singularize", w])
    if i % 2 == 0:
        ops.append(["pluralize", p])
        ops.append(["singularize", s])
job("rails_pairs", ops)

# Nouns a schema or an API names things with.
NOUNS = """account address agenda alert alumnus amount answer appendix
apple archive article attachment audit author avatar badge balance batch
battery belief bench bill bird blob blog body bonus book branch brush
budget bug buzz cache cactus calf calendar campus candy cargo catalog
cell chapter charge chassis cherry church city class client clock cloud
coach code column company contact copy country coupon course crash
credit cross curriculum customer cycle dash deal deer delivery deploy
desk device diary dish domain draft dress echo email employee entry
envelope estimate event exam family fax fee ferry field file filter
fly focus folder fox fungus gallery gas genus glass glitch goal grief
group guess hash hero hoax hobby holiday host hypothesis inbox index
inquiry invoice issue item job journey key kiss knife lady lash leaf
lens library life line loaf lobby log loss lunch match mattress memo
menu mess metric minute monkey mosquito mouse nucleus oasis order
outbox owner pass patch payment penny phenomenon piano policy portfolio
potato preference proxy puppy radius ray reply report roof sandwich
scarf schema scratch self session shelf sky spy story studio stimulus
studio subscription survey syllabus tax taxi tax_rate thief tooth
torpedo toy tray trophy turkey valley veto video volcano waltz watch
webhook wharf wolf worry yes zero""".split()
ops = []
for i, w in enumerate(NOUNS):
    if i % 2 == 1:
        continue
    ops.append(["pluralize", w])
    if i % 4 == 0:
        ops.append(["singularize", w])
    if i % 6 == 0:
        ops.append(["roundtrip", w])
job("nouns", ops)

# Class and column names, the way code converts between them.
IDENTS = [
    "DeviceType", "device_type", "IOError", "HTTPServerError", "html5Parser",
    "SSLError", "Area51Controller", "api_v2_key", "special-guest", "Product",
    "SpecialGuest", "ApplicationController", "Area51Controller", "AWSS3Bucket",
    "getHTTPResponseCode", "XMLHttpRequest", "already_snake", "__dunder__",
    "_private_thing", "trailing_", "a", "A", "", "ABC", "aB", "Ab", "a1B2c3",
    "camelCase_with_snake", "Kebab-Case-Name", "with spaces here", "ÉcoleNormale",
    "ÜberCool", "straße_name", "όνομα_χρήστη", "ﬁle_name", "ǆungla_veliki",
    "名前_type", "x_y_z", "user\tname", "line\nbreak_here", "OK2Go", "v2API",
]
ops = []
for w in IDENTS:
    ops.append(["camelize", w])
    ops.append(["camelize", w, "lower"])
    ops.append(["underscore", w])
    ops.append(["dasherize", w])
    ops.append(["tableize", w])
    ops.append(["camelize", w, "under"])
job("identifiers", ops)

# Column names to labels, and titles.
LABELS = [
    "employee_salary", "author_id", "_id", "id", "first_name_id_id",
    "x-men: the last stand", "TheManWithoutAPast", "raiders_of_the_lost_ark",
    "man from the boondocks", "o'brien's dog", "it's 'quoted' text",
    "ΟΔΥΣΣΕΥΣ ΚΑΙ ΚΑΛΥΨΩ", "ΣΑΣ", "Σ", "ΌΣΟΣ_ΣΟΦΟΣ", "straße_café",
    "élan vital", "ǆungla veliki", "ﬁnal ﬂow", "1st_place_winner",
    "hello\tworld", "  leading_space", "UPPER_CASE_COLUMN", "mixedCase_column",
    "html_body_html", "user_ids", "x_id", "ID", "the_ünïcödé_title",
    "çà et là", "ǈudevit", "ﬀ_ligature", "ÿ_end", "ŉ_apostrophe", "a.b_c",
    "über-straße", "name:with:colons", "ΣΑΣ:ΣΑΣ", "ΑΣ.Σ",
]
ops = []
for w in LABELS:
    ops.append(["humanize", w])
    ops.append(["titleize", w])
    ops.append(["capitalize", w])
job("labels", ops)

# Blog titles to URL slugs.
TITLES = [
    "Donald E. Knuth", "Ærøskøbing", "Crème brûlée — the recipe",
    "Ｆｕｌｌｗｉｄｔｈ ＡＢＣ", "№ 5 ½ price", "東京 Tokyo 2024",
    "---already--sluggy---", "Hello, World!", "  spaces  everywhere  ",
    "C++ & C# in 2024?", "Ünïcödé Strassen in München", "ﬁrst ﬂoor ﬀ",
    "Ⅻ Roman Numerals Ⅳ", "x² + y² = z²", "café_au_lait-recipe",
    "Ångström and Ørsted", "Łódź", "Ǆemal", "trailing.dot.", "a--b__c",
    "", "-", "ÀÁÂÃÄÅ", "ŉ", "Ŀl", "ﬆop", "ẞig",
]
SEPS = [None, "_", "", ".", "--", "+", "*"]
ops = []
for t in TITLES:
    ops.append(["transliterate", t])
    for sep in SEPS:
        if sep is None:
            ops.append(["parameterize", t])
        else:
            ops.append(["parameterize", t, sep])
job("slugs", ops)

nums = ["i:%d" % n for n in [0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 21, 22, 23, 101, 102, 103,
                              111, 112, 113, 1002, 1003, -1, -2, -11, -12, -13, -21, -1021,
                              1000000, 10 ** 18, -(10 ** 18), 9223372036854775807,
                              123456789012345678901234567890]]
nums += ["i:%d" % random.randrange(-10 ** 6, 10 ** 6) for _ in range(30)]
nums += ["s:42", "s: 7 ", "s:-11", "s:+3", "s:1_000_002", "s:١٢", "s:٣", "s:abc", "s:",
         "s:1__0", "s:_1", "s:12.5", "s:0x10", "s:\u20031\u2003", "s:99999999999999999999999993",
         "b:True", "b:False", "f:2.7", "f:-11.0", "f:3.9", "f:0.5", "f:1e+22", "f:-0.0"]
ops = []
for n in nums:
    ops.append(["ordinal", n])
    ops.append(["ordinalize", n])
job("ordinals", ops)

# The inflections an application configures at startup, as Rails apps
# do in config/initializers/inflections.rb.
ops = [
    ["pluralize", "octopus"], ["pluralize", "Octopus"],
    ["irregular", "octopus", "octopodes"],
    ["pluralize", "octopus"], ["pluralize", "Octopus"], ["singularize", "octopodes"],
    ["singularize", "OCTOPODES"], ["pluralize", "CamelOctopus"],
    ["irregular", "goose", "geese"], ["pluralize", "goose"], ["singularize", "geese"],
    ["pluralize", "mongoose"],
    ["irregular", "Person", "Leute"], ["pluralize", "person"], ["pluralize", "Person"],
    ["singularize", "Leute"], ["singularize", "leute"], ["pluralize", "SalesPerson"],
    ["uncountable", "police"], ["pluralize", "police"], ["singularize", "police"],
    ["singularize", "Police"], ["singularize", "the_police"], ["singularize", "nopolice"],
    ["pluralize", "Police"],
    ["plural", "(?i)(ax)is$", "\\1es"], ["pluralize", "taxis"],
    ["plural", "(?i)(quiz)$", "\\1zes_\\g<1>"], ["pluralize", "quiz"],
    ["singular", "(?i)(kn|w|l)ives$", "\\1ife"], ["singularize", "knives"],
    ["singularize", "lives"],
    ["singular", "(?i)(cact|fung)i$", "\\1us"], ["singularize", "cacti"], ["singularize", "fungi"],
    ["plural", "(?i)(cact|fung)us$", "\\1i"], ["pluralize", "cactus"], ["pluralize", "fungus"],
    ["roundtrip", "cactus"],
    ["plural", "(?i)(bad", "\\1"], ["pluralize", "dog"], ["pluralize", ""],
    ["reset"],
    ["plural", "(?i)x$", "\\2"], ["pluralize", "fox"], ["pluralize", "cat"],
    ["reset"],
    ["plural", "^(dat)um$", "\\g<name>"], ["pluralize", "datum"],
    ["reset"],
    ["singular", "(?i)(?P<stem>c)hildren$", "\\g<stem>hild"], ["singularize", "children"],
    ["singularize", "Children"],
    ["singular", "(?i)a{2,}rgh$", "argh"], ["singularize", "aaaargh"], ["singularize", "aargh"],
    ["singular", "(?i)[z-a]$", ""], ["singularize", "dogs"],
    ["reset"],
    ["irregular", "child", "kids"], ["pluralize", "child"], ["singularize", "kids"],
    ["pluralize", "Child"], ["singularize", "Kids"],
    ["reset"],
    ["pluralize", "octopus"], ["pluralize", "goose"],
]
job("configure", ops)

# Rails scaffolding: model names and their columns to the names of the
# table, the routes, the controller, the foreign keys and the labels.
MODELS = [
    "BlogPost title:string body:text author_id:integer published_at:datetime",
    "Person first_name:string last_name:string company_id:integer",
    "Category name:string parent_id:integer position:integer",
    "OrderLineItem order_id:integer product_id:integer unit_price_cents:integer",
    "HTTPRequestLog status:integer remote_ip:string user_agent:string",
    "Address street:string city:string postal_code:string country_code:string",
    "Mouse wheel_count:integer dpi:integer",
    "Analysis dataset_id:integer criteria:json",
    "Child guardian_id:integer birthday:date",
    "Octopus arm_count:integer habitat:string",
    "Datum value:float source_id:integer",
    "Status code:string label:string",
    "AdminUser email:string role_ids:json",
    "Ox name:string yoke_id:integer",
    "Medium kind:string",
]
job("scaffold", [["scaffold", m] for m in MODELS])

# The empty and odd inputs every helper gets eventually.
ops = []
for f in ["pluralize", "singularize", "underscore", "humanize", "titleize",
          "tableize", "parameterize", "dasherize", "transliterate"]:
    for w in ["", " ", "_", "-", "s", "S", "ss", "y", "ies", "_id_", "12345", "!!!"]:
        ops.append([f, w])
ops.append(["camelize", "", "lower"])
ops.append(["camelize", ""])
ops.append(["camelize", "_", "lower"])
ops.append(["camelize", "__x", "lower"])
job("edges", ops)


def esc(s):
    return s.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n")


os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for name, ops in jobs:
        fh.write("== " + name + "\n")
        for op in ops:
            fh.write("\t".join(esc(x) for x in op) + "\n")

for n in nums:
    if n.startswith("f:"):
        assert repr(float(n[2:])) == n[2:], n

# The characters the jobs reach, closed under the mappings.
covered = set()
for name, ops in jobs:
    for op in ops:
        for x in op[1:]:
            covered.update(x)
for w in "octopodes geese Leute kids hild argh ife us i es zes_ ouse".split():
    covered.update(w)
covered.update(chr(c) for c in range(32, 127))
# The final sigma, which lower() makes from context.
covered.add("\u03c2")
todo = list(covered)
while todo:
    c = todo.pop()
    for m in (c.lower(), c.upper(), c.title(), unicodedata.normalize("NFKD", c)):
        for d in m:
            if d not in covered:
                covered.add(d)
                todo.append(d)

WB = {0x27, 0x2E, 0x3A, 0xB7, 0x387, 0x55F, 0x5F4, 0x2018, 0x2019, 0x2024, 0x2027,
      0xFE13, 0xFE52, 0xFE55, 0xFF07, 0xFF0E, 0xFF1A}


def hexs(s):
    return " ".join("%x" % ord(d) for d in s)


with open("data/unicode.txt", "w", encoding="utf-8") as fh:
    fh.write("# cp;lower;upper;title;flags;ccc;nfkd (flags: c cased, i case-ignorable)\n")
    for c in sorted(covered):
        cp = ord(c)
        flags = ""
        if c.islower() or c.isupper() or c.istitle():
            flags += "c"
        if unicodedata.category(c) in ("Mn", "Me", "Cf", "Lm", "Sk") or cp in WB:
            flags += "i"
        fh.write("%x;%s;%s;%s;%s;%d;%s\n" % (cp, hexs(c.lower()), hexs(c.upper()), hexs(c.title()),
                                            flags, unicodedata.combining(c),
                                            hexs(unicodedata.normalize("NFKD", c))))
print(len(jobs), "jobs,", sum(len(o) for _, o in jobs), "operations,", len(covered), "characters")
