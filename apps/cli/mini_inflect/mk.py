# Writes data/: inflect's word lists and tables (data/tables.json, taken
# from the module as it is after import, so the lists are inflect's
# own), the jobs mini_inflect runs (data/jobs.jsonl) and the files its
# programs read.
import json
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)

_tg = types.ModuleType("typeguard")
_tg.typechecked = lambda f: f
_mi = types.ModuleType("more_itertools")


def windowed_complete(iterable, n):
    seq = tuple(iterable)
    for i in range(len(seq) - n + 1):
        yield seq[:i], seq[i:i + n], seq[i + n:]


_mi.windowed_complete = windowed_complete
sys.modules["typeguard"] = _tg
sys.modules["more_itertools"] = _mi

import inflect  # noqa: E402

# ------------------------------------------------------------ tables

LISTS = """
pl_sb_z_zes_list pl_sb_ze_zes_list pl_sb_C_is_ides_complete pl_sb_C_is_ides_endings
pl_sb_C_a_ata_list pl_sb_U_a_ae_list pl_sb_C_a_ae_list pl_sb_C_en_ina_list pl_sb_U_um_a_list
pl_sb_C_um_a_list pl_sb_U_us_i_list pl_sb_C_us_i_list pl_sb_C_us_us pl_sb_U_on_a_list
pl_sb_C_on_a_list pl_sb_C_o_i pl_sb_U_o_os_complete pl_sb_U_o_os_endings pl_sb_U_ch_chs_list
pl_sb_U_ex_ices_list pl_sb_U_ix_ices_list pl_sb_C_ex_ices_list pl_sb_C_ix_ices_list
pl_sb_C_i_list pl_sb_C_im_list pl_sb_U_man_mans_list pl_sb_U_man_mans_caps_list
pl_sb_U_louse_lice_list pl_sb_uninflected_s_complete pl_sb_uninflected_s_endings
pl_sb_uninflected_herd pl_sb_uninflected_complete pl_sb_uninflected_caps
pl_sb_uninflected_endings pl_sb_singular_s_complete pl_sb_singular_s_endings
pl_sb_singular_s_es si_sb_ois_oi_case si_sb_uses_use_case si_sb_uses_use si_sb_ies_ie_case
si_sb_ies_ie si_sb_oes_oe_case si_sb_oes_oe si_sb_z_zes si_sb_zzes_zz si_sb_ches_che_case
si_sb_ches_che si_sb_xes_xe si_sb_sses_sse_case si_sb_sses_sse si_sb_ves_ve_case si_sb_ves_ve
si_sb_es_is pl_prep_list singular_pronoun_genders plverb_irregular_non_pres pl_v_oes_oe
pl_v_oes_oe_endings_size4 pl_v_oes_oe_endings_size5 pl_count_zero pl_count_one unit teen ten mill
""".split()
DICTS = """
pl_sb_irregular_s pl_sb_irregular pl_sb_irregular_caps pl_sb_irregular_compound pl_pron_nom
pl_pron_acc plverb_irregular_pres plverb_ambiguous_pres pl_adj_special pl_adj_poss ordinal nth
""".split()

tables = {}
for name in LISTS:
    v = getattr(inflect, name)
    tables[name] = sorted(v) if isinstance(v, set) else list(v)
for name in DICTS:
    tables[name] = [[str(k), v] for k, v in getattr(inflect, name).items()]
with open(os.path.join(DATA, "tables.json"), "w", encoding="utf-8") as f:
    f.write("{\n")
    names = LISTS + DICTS
    for i, name in enumerate(names):
        sep = "," if i + 1 < len(names) else ""
        f.write(f"{json.dumps(name)}: {json.dumps(tables[name], ensure_ascii=False)}{sep}\n")
    f.write("}\n")

# ------------------------------------------------------------ jobs

jobs = []


def job(name, ops):
    jobs.append({"name": name, "ops": ops})


def call(fn, *args, **kw):
    op = {"op": "call", "fn": fn, "args": list(args)}
    if kw:
        op["kw"] = kw
    return op


NOUNS = """
cat dog house mouse louse booklouse goose tooth foot child ox person man woman German Roman
Norman human talisman fish sheep deer moose salmon trout bison series species news measles
mumps scissors trousers glasses box church dish quiz buzz fez waltz topaz quartz bus gas
lens kiss boss class status virus campus genus corpus opus penis testis atlas iris
analysis thesis crisis axis basis ellipsis diagnosis hypothesis parenthesis criterion
phenomenon automaton polyhedron datum medium memorandum bacterium curriculum stadium
millennium aquarium forum alumnus cactus fungus nucleus radius stimulus syllabus octopus
genie index appendix matrix vertex vortex apex codex helix radix calf half knife life wife
leaf loaf wolf shelf thief dwarf roof chief scarf hoof proof belief cliff city lady baby
toy boy day key monkey money soliloquy colloquy guy story Mary Kennedy potato tomato hero
echo veto photo piano solo radio zoo tattoo studio cameo embryo canto tempo libretto
torso ego memo kilo logo tornado volcano buffalo mosquito domino taco die dice ice
mother-in-law father-in-law brother-in-law son-in-law man-of-war attorney-general
Governor-General court-martial poet laureate passer-by hanger-on looker-on
prima donna aide-de-camp bureau chateau tableau plateau beau milieu adieu sphinx larynx
pharynx lynx onyx phalanx trix matrix cherub seraph goy afrit efreet stamen foramen lumen
schema dogma stigma lemma oedema alga larva nebula formula vertebra antenna
Chinese Japanese Portuguese Vietnamese ISO NATO NGO ado CD PhD UFO ATM
I me myself you yourself he she it they him her them herself himself itself themself
mine yours hers his its theirs
""".split()
NOUNS += ["prima donna", "Governor General", "court martial", "attorney general", "major general",
          "son of a gun", "pair of scissors", "piece of cake", "cup of tea", "man of war",
          "mother in law", "degree Celsius", "degree fahrenheit hour", "kilometer per hour",
          "mile a minute", "box of chocolates", "to me", "for them", "with you", "about her",
          "  cat  ", "\tdog", "Cat", "CAT", "cAT", "Person", "PERSON", "Mouse", "MOUSE", "SHEEP",
          "Tooth", "Children", "IT", "Knife", "Wolf", "Lady", "Kennedys", "Monday", "Sunday",
          "a\nb", "big dog", "hot dog stand", "data", "deer hunter", "fish fry", "news anchor",
          "eye of newt", "lord of the rings", "jack-in-the-box", "will-o'-the-wisp"]
NOUNS = list(dict.fromkeys(NOUNS))

VERBS = """
is am are was were has have does do runs run flies fly tries try copies copy watches watch
washes wash buzzes fizzes passes misses fixes boxes goes does echoes vetoes canoes shoes hoes
toes woes says plays obeys reaches fights likes makes looks views sleeps sinks acts blames
can must thought saw bent will might cut did had ate made put spent fought sank gave sought
shall could ought should isn't wasn't hasn't doesn't don't can't won't quizzes
analyses ceps crises
""".split() + ["is going", "has been", "does not", "was here", "runs away", "flies south",
               "thought about", "saw it", "Is", "WAS", "Has", "Runs", "Flies"]
VERBS = list(dict.fromkeys(VERBS))

ADJS = ["a", "an", "this", "that", "my", "your", "its", "her", "his", "their", "This", "THAT",
        "My", "cat's", "dog's", "child's", "mouse's", "James's", "boss'", "boss's", "woman's",
        "red", "big", "sheep's", "ox's", "person's", "Mary's"]

basic = []
for w in NOUNS:
    basic.append(call("plural", w))
job("plural nouns", basic)
job("plural_noun", [call("plural_noun", w) for w in NOUNS[:80]] + [call("plural_noun", w, c) for w, c in [
    ("cat", 1), ("cat", 2), ("cat", 0), ("cat", "one"), ("cat", "a"), ("cat", "an"), ("cat", "each"),
    ("cat", "every"), ("cat", "this"), ("cat", "that"), ("cat", "1"), ("cat", "zero"), ("cat", "no"),
    ("cat", "nil"), ("cat", "two"), ("cat", "One"), ("cat", "ONE"), ("cat", -1), ("cat", "")]])
job("plural verbs", [call("plural_verb", w) for w in VERBS] + [call("plural", w) for w in VERBS]
    + [call("plural_verb", "runs", 1), call("plural_verb", "is", 1), call("plural_verb", "is", "zero")])
job("plural adjectives", [call("plural_adj", w) for w in ADJS] + [call("plural", w) for w in ADJS]
    + [call("plural_adj", "my", 1), call("plural_adj", "this", "one")])

p = inflect.engine()
plurals = []
for w in NOUNS:
    try:
        plurals.append(p.plural_noun(w))
    except Exception:
        pass
plurals = list(dict.fromkeys(plurals + """
cats dogs boxes churches dishes quizzes buzzes fezzes topazes quartzes buses gases lenses
kisses bosses classes statuses viruses campuses alumni cacti fungi foci nuclei radii stimuli
syllabi octopuses octopodes genera corpora opera penes testes atlases irises analyses theses
crises axes bases ellipses diagnoses hypotheses parentheses criteria phenomena automata data
media memoranda bacteria curricula stadia millennia indices appendices matrices vertices
vortices apices codices helices radices calves halves knives lives wives leaves loaves wolves
shelves thieves dwarves dwarfs roofs chiefs scarves hooves proofs beliefs cliffs cities ladies
babies toys boys days keys monkeys moneys monies soliloquies guys stories Marys Kennedys
potatoes tomatoes heroes echoes vetoes photos pianos solos radios zoos tattoos studios cameos
embryos cantos tempi libretti torsos egos memos kilos logos tornadoes volcanoes buffaloes
mosquitoes dominoes tacos dice mice lice geese teeth feet children oxen people persons men
women Germans Romans Normans humans talismans sheep deer fish fishes moose salmon trout bison
series species news measles mumps scissors trousers glasses houses blouses causes horses
movies cookies pies ties lies hippies zombies goalies calories prairies shoes toes hoes oes
canoes oboes floes woes throes bureaus bureaux chateaus chateaux tableaux beaux milieus milieux
sphinxes sphinges larynges lynxes onyxes phalanges cherubim seraphim goyim afriti efreeti stamina
foramina lumina schemata dogmata stigmata lemmata algae larvae nebulae formulae formulas
vertebrae antennae antennas we us ourselves yourselves they them themselves theirs ours
mothers-in-law fathers-in-law attorneys-general Governors-General courts-martial passers-by
hangers-on lookers-on prima donnas prime donne aides-de-camp men-of-war sons of guns
pairs of scissors cups of tea degrees Celsius kilometers per hour Chinese Japanese CDs PhDs
UFOs ATMs Hesses Matisses Bolshois Hanois Betelgeuses Toulouses ellipses neuroses taxes
annexes pickaxes waltzes fizzes razzes avalanches caches niches moustaches aches headaches
caves waves sleeves eaves knaves olives valves wolves dwarves selves hyenas
""".split()))
job("singular_noun", [call("singular_noun", w) for w in plurals]
    + [call("singular_noun", w) for w in ["cat", "glass", "boss", "status", "sheep", "child",
                                          "news", "Monday", "I", "s", "is", "sss", "  cats  "]])
job("singular_noun with gender and count", [
    call("singular_noun", w, gender=g)
    for w in ["they", "them", "themselves", "theirs", "to them", "with themselves", "we", "us", "ours"]
    for g in ["neuter", "feminine", "masculine", "gender-neutral", "feminine or masculine",
              "masculine or feminine"]
] + [call("singular_noun", "cats", 1), call("singular_noun", "cats", 2), call("singular_noun", "cats", "one"),
     call("singular_noun", "cats", gender="robot"), call("gender", "feminine"), call("singular_noun", "they"),
     call("singular_noun", "them"), call("gender", "plural"), call("gender", "masculine or feminine"),
     call("singular_noun", "theirs"), call("singular_noun", "for them")])

CLASSICAL_WORDS = ["cat", "person", "persons", "matrix", "index", "formula", "cherub", "bureau", "sphinx",
                   "lynx", "stamen", "appendix", "octopus", "cactus", "criterion", "focus", "trix", "Mary",
                   "Kennedy", "bison", "wildebeest", "fish", "zero", "0", "corpus", "genus", "opus",
                   "matrices", "formulae", "cherubim", "octopodes", "people", "prima donna", "major general"]
cl_ops = []
for setting in [{}, {"all": True}, {"all": False}, {"zero": True}, {"herd": True}, {"names": False},
                {"persons": True}, {"ancient": True}, {"all": False, "names": True, "ancient": True}]:
    cl_ops.append(call("classical", **setting))
    for w in CLASSICAL_WORDS:
        cl_ops.append(call("plural", w))
    for w in ["matrices", "formulae", "cherubim", "octopodes", "persons", "Kennedys", "bison",
              "bureaux", "stamina", "sphinges"]:
        cl_ops.append(call("singular_noun", w))
    cl_ops.append(call("plural", "cat", 0))
    cl_ops.append(call("no", "cat", "zero"))
    cl_ops.append(call("plural_verb", "is", "nil"))
cl_ops.append(call("classical", bogus=True))
cl_ops.append(call("classical", all=True, bogus=True))
cl_ops.append(call("plural", "formula"))
job("classical modes", cl_ops)

job("compare", [call(fn, a, b) for fn in ["compare", "compare_nouns", "compare_verbs", "compare_adjs"]
                for a, b in [("egg", "eggs"), ("eggs", "egg"), ("egg", "egg"), ("cat", "dog"),
                             ("index", "indices"), ("indexes", "indices"), ("indices", "indexes"),
                             ("formulas", "formulae"), ("runs", "run"), ("run", "runs"),
                             ("my", "our"), ("cat's", "cats'"), ("child's", "children's"),
                             ("indexes's", "indices's"), ("person", "people"), ("people", "persons"),
                             ("mouse", "mice"), ("fish", "fish"), ("is", "are"), ("this", "these")]]
    + [call("plural", "formula"), call("classical", names=False), call("compare", "Mary", "Marys"),
       call("plural", "Mary")])

ARTICLE_WORDS = """
cat apple hour honest heir honor honour euler mpeg unicorn union unanimous unabomber university
uniform European ewe once onetime one-off unit uber ubiquitous ukulele Ukraine UN UK UNESCO UNICEF
US USA FBI NBA NASA SQL HTML XML LED MRI RSVP FAQ SUV NPC X-ray x-ray y-axis yttrium yclept ygg
yblent ypsilanti a e i o u y A E I O U Y h H s S b B f F 8th 1st 11th 18 80 8 11 FJORD MNEMONIC
LZW SPC NHS RHESUS SQUID X XYL sth fth bth ath -th hth uth ether ewer eucalyptus oyster urn
""".split() + ["  cat  ", "an apple", "a hour", "an cat", "A cat", "honest man", "user", "usual",
               "Uber driver", "one", "1", "a", "an", "\tx"]
job("indefinite article", [call("a", w) for w in ARTICLE_WORDS]
    + [call("an", "cat"), call("a", "cat", 2), call("a", "cat", "some"), call("a", "cat", 0),
       call("a", "cat", "one"), call("a", "cat", "1")])

DEF_OPS = [
    call("defnoun", "VAX", "VAXen"), call("plural", "VAX"), call("plural", "vax"), call("plural", "VAXes"),
    call("defnoun", "(.*)ox", "$1oxen"), call("plural", "box"), call("plural", "Fox"),
    call("defnoun", "(.*)ix", "$2ices"), call("plural", "matrix"),
    call("defnoun", "cow", "kine|cows"), call("plural", "cow"), call("classical", all=True), call("plural", "cow"),
    call("classical", all=False),
    call("defnoun", "sky", None), call("plural", "sky"), call("singular_noun", "VAXen"),
    call("defnoun", "ox", "$1en"), call("plural", "ox"),
    call("defnoun", "(x", "y"), call("defnoun", "x[", "y"),
    call("defverb", "will", "shall", "will", "will", "will", "will"), call("plural_verb", "will"),
    call("defverb", "runs", "sprint", None, None, "jogs", "jog"), call("plural_verb", "runs"), call("plural_verb", "jogs"),
    call("defadj", "hir", "their"), call("plural_adj", "hir"), call("plural", "hir"),
    call("defa", "ego"), call("a", "ego"), call("a", "egotist"),
    call("defan", "horrendous.*"), call("a", "horrendous"), call("a", "horrendously bad"), call("a", "horror"),
    call("defa", "(?:h|H)orr.*"), call("a", "horrendous"), call("a", "Horror"),
    call("defan", "(a"),
]
job("user definitions", DEF_OPS)

job("no", [call("no", w, c) for w, c in [
    ("cat", None), ("cat", 0), ("cat", 1), ("cat", 2), ("cat", "no"), ("cat", "zero"), ("cat", "nil"),
    ("cat", "0"), ("cat", "one"), ("cat", "a"), ("cat", "some"), ("error", 3), ("  error  ", 3),
    ("mouse", 3), ("sheep", 10), ("person", "many"), ("Box", 5), ("child", -1)]]
    + [call("no", "cat"), call("num", 3), call("no", "cat"), call("plural", "cat"), call("num", 1),
       call("plural", "cat"), call("no", "cat"), call("num", 0, False), call("no", "dog"), call("num"),
       call("no", "dog"), call("num", "x"), call("num", "7"), call("plural", "dog"), call("num")])

PARTICIPLE_VERBS = """
runs run sees see lies dies ties hoes toes shoes canoes goes does is are was were has had
makes writes dances skis taxis eyes dyes hums sits hits stops admits begins prefers visits
offers opens enters shuts plays obeys sues argues glues queues tours sings bakes bes
""".split() + ["lies down", "is here", "Runs"]
job("present participle", [call("present_participle", w) for w in PARTICIPLE_VERBS])

ORD = [0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 21, 22, 23, 101, 102, 103, 111, 112, 113, 1000, 1001,
       -1, -2, -11, 2.5, 3.0, 1.25, 1e16, "1", "2", "3", "11", "12", "21", "3.", "3.5", "12abc",
       "one", "two", "three", "four", "five", "eight", "nine", "twelve", "twenty", "ninety-nine",
       "twenty-one", "one hundred", "first", "eleven", "zero", "a", "Five"]
job("ordinal", [call("ordinal", n) for n in ORD])

NUMS = [0, 1, 2, 9, 10, 11, 12, 15, 19, 20, 21, 42, 99, 100, 101, 110, 111, 119, 120, 199, 200, 999,
        1000, 1001, 1010, 1100, 1234, 9999, 10000, 12345, 100000, 123456, 1000000, 1000001, 1234567,
        10000000, 123456789, 1000000000, 1234567890, 9007199254740993, -1, -42, -1234, 3.14, 0.5,
        2.0, 1e16, -0.25, "0", "00", "007", "1", "12", "1234", "1,234", "1,234,567", "+5", "-5",
        "+1,000", "3.14159", ".5", "5.", "1.2.3", "12th", "1st", "2nd", "3rd", "101st", "th", "st",
        "1e3", "1_000", " 42", "42 ", "1" + "0" * 36, "1" + "0" * 40, "123456789012345678901234567890"]
nw = [call("number_to_words", n) for n in NUMS]
for n in [0, 1, 7, 12, 123, 1234, 12345, 1234567, "1.5", "12.345", "1203", "100", "1000", "305"]:
    for g in [1, 2, 3]:
        nw.append(call("number_to_words", n, group=g))
for n in [1234, 12345678, "1.5"]:
    nw.append(call("number_to_words", n, wantlist=True))
    nw.append(call("number_to_words", n, group=1, wantlist=True))
nw += [
    call("number_to_words", 1234, andword=""), call("number_to_words", 101, andword="plus"),
    call("number_to_words", 0, zero="oh"), call("number_to_words", 1, one="unity"),
    call("number_to_words", 101, group=1, zero="oh", one="unity"), call("number_to_words", "1.0", decimal="dot"),
    call("number_to_words", 1234567, comma=""), call("number_to_words", 1234567, comma=";"),
    call("number_to_words", 1234567, decimal=""), call("number_to_words", "1.5", decimal=None),
    call("number_to_words", "1.5", decimal=""), call("number_to_words", 12, threshold=10),
    call("number_to_words", 9, threshold=10), call("number_to_words", 1234567, threshold=10),
    call("number_to_words", "1234567.891", threshold=10), call("number_to_words", 1234567, threshold=10, comma=""),
    call("number_to_words", 1234567, threshold=10, comma="."), call("number_to_words", "1,000", threshold=10),
    call("number_to_words", 5, group=4), call("number_to_words", 5, group=-1),
    call("number_to_words", "1.2.3", group=0), call("number_to_words", "1.2.3", group=2),
    call("number_to_words", "1.", group=1), call("number_to_words", 12, wantlist=True, group=0),
]
job("number_to_words", nw)

JOIN = [[], ["ant"], ["ant", "bee"], ["ant", "bee", "fly"], ["ant", "bee", "fly", "gnat"],
        ["Paris, France", "Rome", "Berlin"], ["a,b", "c"]]
jo = [call("join", w) for w in JOIN]
jo += [call("join", JOIN[3], conj="or"), call("join", JOIN[3], conj=""), call("join", JOIN[3], conj="", conj_spaced=False),
       call("join", JOIN[3], sep=";"), call("join", JOIN[3], sep="|", sep_spaced=False),
       call("join", JOIN[3], final_sep=""), call("join", JOIN[3], final_sep=" &", conj="", conj_spaced=False),
       call("join", JOIN[2], conj="&", conj_spaced=False), call("join", JOIN[5], sep=","),
       call("join", JOIN[4], conj="and/or"), call("join", None)]
job("join", jo)

INFLECT = [
    "The plural of cat is plural('cat')",
    "plural_noun('mouse') and plural_verb('runs') and plural_adj('my')",
    "I saw a('apple') and an('hour') and a('unicorn')",
    "There num(3) plural_verb('is') no('error')",
    "There num(1) plural_verb('is') no('error')",
    "num(0, False)There are no('error')",
    "She is ordinal(21) and ordinal('nine')",
    "We counted number_to_words(1234)",
    "number_to_words(1234, group=1) and number_to_words(42, andword='')",
    "Running present_participle('runs') and present_participle('sees')",
    "singular_noun('mice') and singular_noun('cats', gender='feminine')",
    "plural('child', 2) vs plural('child', 1) vs plural('child', count=0)",
    "unknown(cat) stays as it is",
    "plural(cat)",
    "x plural(-1) y",
    "singular_noun('cat')",
    "number_to_words(5, wantlist=True)",
    "plural('cat') plural(\"dog\") plural('ox', \"2\")",
    "no('cat', 0) no('cat', 1) no('cat', 5) no('cat', 'no')",
    "plural('sheep') and a(\"FBI agent\") and plural('index')",
    "PLURAL('cat') and Plural('cat')",
    "num(2)plural('cat') num(1)plural('cat') num()plural('cat')",
    "plural('cat',)",
    "a('cat', 3) and an('egg', 'some')",
    "plural('a\\tb')",
    "plural('caf\\u00e9')",
    "plural(['cat'])",
    "ordinal(3.5) ordinal(-11) number_to_words(-0.5)",
]
job("inflect", [call("inflect", t) for t in INFLECT] + [call("num", 2), call("inflect", "plural('cat') num(1)"),
                                                       call("plural", "cat")])

job("programs", [{"op": "digest", "file": "repos.json"}, {"op": "cheques", "file": "payments.csv"},
                 {"op": "leaderboard", "file": "scores.csv"}, {"op": "tables", "file": "models.txt"},
                 {"op": "inventory", "file": "inventory.txt"}, {"op": "notify", "file": "notifications.txt"},
                 {"op": "dryrun", "file": "plan.txt"}])

with open(os.path.join(DATA, "jobs.jsonl"), "w", encoding="utf-8") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")

# ------------------------------------------------------------ programs

REPOS = [
    {"name": "acme/api", "open": [["issue", 3], ["pull request", 1], ["release", 0]], "owners": 2,
     "maintainers": ["ana", "bo"], "stale": 4, "oldest": "hotfix branch"},
    {"name": "acme/web", "open": [["issue", 1], ["pull request", 12], ["security advisory", 2]], "owners": 1,
     "maintainers": ["chen"], "stale": 1, "oldest": "experiment"},
    {"name": "acme/infra", "open": [["issue", 0], ["alert", 11], ["deploy", 1], ["query", 2]], "owners": 3,
     "maintainers": ["dee", "eli", "fay"], "stale": 0, "oldest": "upgrade"},
    {"name": "acme/docs", "open": [["typo", 9], ["analysis", 2], ["index", 2], ["appendix", 1]], "owners": 0,
     "maintainers": [], "stale": 2, "oldest": "hour-long rewrite"},
    {"name": "acme/data", "open": [["datum", 3], ["schema", 2], ["criterion", 4], ["status", 2]], "owners": 4,
     "maintainers": ["gus", "hal", "ida", "jo"], "stale": 0, "oldest": "x"},
]
with open(os.path.join(DATA, "repos.json"), "w", encoding="utf-8") as f:
    json.dump(REPOS, f, indent=1)
    f.write("\n")

PAYMENTS = [
    ("payee", "amount", "currency", "one", "many"),
    ("Northwind Traders", "1234.50", "USD", "dollar", "dollars"),
    ("Contoso Ltd", "1.00", "USD", "dollar", "dollars"),
    ("Fabrikam", "1000000.07", "EUR", "euro", "euros"),
    ("Tailspin Toys", "0.99", "GBP", "pound", "pounds"),
    ("Wide World Importers", "2015", "USD", "dollar", "dollars"),
    ("Adventure Works", "100100.1", "CAD", "dollar", "dollars"),
    ("Litware", "999999999.99", "JPY", "yen", "yen"),
    ("Proseware", "40", "INR", "rupee", "rupees"),
    ("Coho Winery", "1.5", "CHF", "franc", "francs"),
    ("Lucerne Publishing", "11", "SEK", "krona", "kronor"),
]
with open(os.path.join(DATA, "payments.csv"), "w", encoding="utf-8", newline="") as f:
    for row in PAYMENTS:
        f.write(",".join(row) + "\r\n")

SCORES = [("player", "points"), ("ana", "1520"), ("bo", "980"), ("chen", "1520"), ("dee", "1"),
          ("eli", "700"), ("fay", "980"), ("gus", "1310"), ("hal", "0"), ("ida", "455"),
          ("jo", "455"), ("kai", "220"), ("lu", "1"), ("max", "2"), ("ned", "19"), ("ola", "101"),
          ("pia", "33"), ("quin", "64"), ("ray", "88"), ("sam", "47"), ("tia", "12"), ("uma", "5"),
          ("vic", "3"), ("wes", "4")]
with open(os.path.join(DATA, "scores.csv"), "w", encoding="utf-8", newline="") as f:
    for row in SCORES:
        f.write(",".join(row) + "\n")

MODELS = """# models and tables of a small shop
model User
model Person
model Category
model OrderItem
model ShippingAddress
model Status
model Analysis
model Index
model Child
model Mouse
model Datum
model Medium
model HTTPRequest
model APIKey
model Box
model Leaf
model Hero
model Photo
model Sheep
model Series
model Wife
model Quiz
model Bus
model Matrix
model Criterion
model Cactus
table users
table people
table categories
table order_items
table shipping_addresses
table statuses
table analyses
table indices
table children
table mice
table data
table media
table http_requests
table api_keys
table boxes
table leaves
table heroes
table photos
table sheep
table series
table wives
table quizzes
table buses
table matrices
table criteria
table cacti
table news
table glass
table status
"""
with open(os.path.join(DATA, "models.txt"), "w", encoding="utf-8") as f:
    f.write(MODELS)

INVENTORY = """3 widget
1 hourglass
1 umbrella
1 unicorn figurine
0 gizmo
12 box of matches
2 pair of scissors
1 European adapter
7 mouse
1 honest broker
4 knife
1 FAQ sheet
5 sheep
1 X-ray film
2 cactus
1 one-way ticket
40 hoof pick
1 USB cable
"""
with open(os.path.join(DATA, "inventory.txt"), "w", encoding="utf-8") as f:
    f.write(INVENTORY)

NOTIFY = """1\tYou have no('new message')
3\tYou have no('new message')
0\tYou have no('new message')
2\tplural('Your order', 2) plural_verb('has') shipped
1\tplural('Your order') plural_verb('has') shipped
5\tno('reviewer') plural_verb('is') waiting for a('approval')
1\tno('reviewer') plural_verb('is') waiting for a('approval')
21\tYou are the ordinal(21) person in line
2\tplural('This') plural('file') plural_verb('was') deleted
1\tplural('This') plural('file') plural_verb('was') deleted
4\tthe plural('child') and plural_adj('their') plural('toy')
1\tthe plural('child') and plural_adj('their') plural('toy')
2\tplural('cat') said hello(world)
3\tplural(dog) barked
"""
with open(os.path.join(DATA, "notifications.txt"), "w", encoding="utf-8") as f:
    f.write(NOTIFY)

PLAN = """creates 3 bucket
deletes 1 snapshot
copies 12 file
ties 2 knot
moves 0 secret
runs 4 migration
stops 1 service
dies 1 replica
queues 5 job
skis 1 slope
admits 7 user
"""
with open(os.path.join(DATA, "plan.txt"), "w", encoding="utf-8") as f:
    f.write(PLAN)

print(sum(len(j["ops"]) for j in jobs), "operations in", len(jobs), "jobs")
