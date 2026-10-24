# Writes data/corpus.txt (the documentation text a dictionary is built
# from) and data/jobs.txt (the commands oracle.py and mini_spellchecker.kara
# run). Everything comes from a fixed linear congruential generator, so the
# files are the same on every run. Run as: python3 -s -P -B mk.py
import re

STATE = [20261024]


def rnd(n):
    STATE[0] = (STATE[0] * 1103515245 + 12345) % 2147483648
    return (STATE[0] >> 8) % n


def pick(xs):
    return xs[rnd(len(xs))]


SLOTS = {
    "N": "service server cluster node worker queue job task release build image "
    "volume secret token config file log metric alert backup snapshot replica "
    "database table index cache request response route endpoint certificate "
    "domain proxy gateway container deployment rollout schedule window "
    "dashboard report package dependency version branch commit pipeline stage "
    "artifact registry mirror region zone network firewall policy account "
    "project team owner operator user client session timeout retry limit "
    "quota budget threshold".split(),
    "V": "restarts drains scales pauses resumes rotates expires retries fails "
    "starts stops reloads syncs copies moves deletes creates updates checks "
    "reports writes reads sends receives caches compresses encrypts signs "
    "verifies publishes promotes rolls waits blocks".split(),
    "A": "new old stale healthy degraded primary secondary local remote "
    "public private default custom shared dedicated temporary permanent "
    "read-only empty full slow fast large small nightly weekly manual "
    "automatic pending active idle broken missing current previous".split(),
    "NUM": "1 2 3 5 8 10 30 60 90 443 8080 2024 3600".split(),
    "W": "seconds minutes hours days".split(),
}

TEMPLATES = [
    "The {N} {V} when the {N} {V}.",
    "A {A} {N} {V} every {NUM} {W}.",
    "If the {N} is {A}, the {N} {V} and the {N} {V}.",
    "Each {N} has a {A} {N} and a {A} {N}.",
    "You can set the {N} {N} to {NUM} {W} in the {N} file.",
    "Don't delete the {A} {N} until the {N} {V}.",
    "It's safe to move a {A} {N} to another {N}.",
    "The {N}'s {N} {V} after {NUM} {W}.",
    "When a {N} {V}, the operator's {N} shows a {A} {N}.",
    "Use max_retries and log_level to tune how the {N} {V}.",
    "There isn't a {A} {N} for this {N}; create one first.",
    "We'll keep the {A} {N} for {NUM} {W} before the {N} {V}.",
    "Your {N} can't reach the {N} while the {N} is {A}.",
    "Check that the {N} and the {N} use the same {N} version.",
    "Most teams run one {N} per {N} and one {N} per {N}.",
    "The 'dry run' mode shows what the {N} would do without changing the {N}.",
    "Every {N} writes its {N} to a {A} {N} on port {NUM}.",
    "After the {N} {V}, the {N} {V} and the {A} {N} is removed.",
    "Users' {N} and owners' {N} are kept in separate {N} tables.",
    "A {N} that {V} too often is marked {A} and the {N} {V}.",
]


def fill(t):
    def rep(m):
        return pick(SLOTS[m.group(1)])

    return re.sub(r"\{(\w+)\}", rep, t)


def corpus():
    paras = []
    for _ in range(90):
        sents = [fill(pick(TEMPLATES)) for _ in range(4 + rnd(5))]
        paras.append(" ".join(sents))
    return "\n\n".join(paras) + "\n"


TEXT = corpus()
WORDS = sorted(set(w.lower() for w in re.findall(r"(\w[\w']*\w|\w)", TEXT)))
ALPHA = [w for w in WORDS if w.isalpha() and len(w) >= 4]
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def edit(w):
    k = rnd(4)
    i = rnd(len(w))
    if k == 0:
        return w[:i] + w[i + 1 :]
    if k == 1 and i + 1 < len(w):
        return w[:i] + w[i + 1] + w[i] + w[i + 2 :]
    if k == 2:
        return w[:i] + pick(LETTERS) + w[i + 1 :]
    return w[:i] + pick(LETTERS) + w[i:]


def typo(w, twice):
    for _ in range(20):
        t = edit(w)
        if twice:
            t = edit(t)
        if t != w and t not in WORDS:
            return t
    return w


def doc(n_typos, n_double):
    sents = [fill(pick(TEMPLATES)) for _ in range(2)]
    toks = " ".join(sents).split(" ")
    spots = [i for i, t in enumerate(toks) if t.strip(".,;'").lower() in ALPHA and t.strip(".,;'") == t.rstrip(".,;")]
    for j in range(n_typos):
        if not spots:
            break
        i = spots.pop(rnd(len(spots)))
        tail = toks[i][len(toks[i].rstrip(".,;")) :]
        core = toks[i].rstrip(".,;")
        bad = typo(core.lower(), j < n_double)
        if core[0].isupper():
            bad = bad[0].upper() + bad[1:]
        toks[i] = bad + tail
    return " ".join(toks)


jobs = []


def J(s):
    jobs.append(s)


J("# a documentation team's spell checker, built on the docs themselves")
J("new docs distance=2 case=0")
J("load_text_file data/corpus.txt")
J("stats")
J("freq the")
J("freq The")
J("freq THE")
J("freq don't")
J("freq max_retries")
J("freq 8080")
J("freq kubernetes")
J("contains Deploy")
J("contains deployment")
J("contains Operator's")
J("split Don't panic: it's 'quoted' -- a''b x_y 3.14 rock'n'roll users' end' _x_ 'tis")
J("split   leading and trailing   ")
J("known the The service deployment's 8080 2024 nan Infinity inf 1e5 1_000 x")
J("unknown the servise 8080 1__0 _1 1_ 1e 0x10 nan +nan -inf .5 5. ! ? ab")
J("known ! . ' _ - a")
J("unknown ! . ' _ - a q")
J("# candidates and corrections")
for w in ["service", "Service", "servise", "srevice", "servce", "sservice",
          "dpeloyment", "deploymnt", "polcy", "plicy", "8080", "1e9", "nan",
          "token", "tokne", "toekn", "tken", "tokens", "zzzz", "q",
          "qxz", "certificatesandmore", "rools",
          "ro", "teh", "adn", "wiht"]:
    J(f"candidates {w}")
    if w not in ("zzzz", "qxz", "wiht"):
        J(f"correction {w}")
J("ed1 node")
J("ed1 Node")
J("ed1 8080")
J("ed1 a")
J("ed2 job")
J("# documents from the docs' review queue")
for d in range(16):
    J("check " + doc(1 + rnd(3), 1 if d % 8 == 0 else 0))
J("check The nginx proxy reads the config files.")
J("check The service restarts when the config file updates.")
J("check ")
J("# editing the dictionary")
J("add Skiff 40")
J("add skiff 2")
J("add kubectl 5")
J("load_words Helm helm HELM nginx yaml")
J("stats")
J("candidates skif")
J("correction skif")
J("candidates kubctl")
J("check The skiff CLI wraps kubectl and helm; nginx reads yaml.")
J("pop SKIFF")
J("pop skiff")
J("pop skiff")
J("freq skiff")
J("remove nginx")
J("remove nginx")
J("remove_words yaml Helm nothing")
J("stats")
J("export data/docs.json")
J("remove_threshold 3")
J("stats")
J("ed1 node")
J("candidates nod")
J("correction nod")
J("remove_threshold 1000000")
J("stats")
J("candidates hello")
J("ed1 hi")
J("# the exported dictionary, opened again")
J("open saved data/docs.json")
J("stats")
J("freq service")
J("freq skiff")
J("correction servise")
J("# a checker that only looks one edit away")
J("new strict distance=1 case=0")
J("load_text_file data/corpus.txt")
J("candidates srevice")
J("candidates srevcie")
J("correction srevcie")
J("distance 2")
J("candidates srevcie")
J("distance 0")
J("distance 3")
J("distance 1")
J("candidates tken")
J("# an empty checker")
J("new empty distance=2 case=0")
J("stats")
J("candidates hello")
J("candidates hi")
J("known hi")
J("unknown hi hello")
J("ed1 ab")
J("# a case-sensitive checker for product names")
J("new names distance=2 case=1")
J("load_text Skiff runs on Linux and macOS. The Skiff CLI talks to the Skiff API. skiff is the binary. The the THE.")
J("load_words Linux Linux linux API")
J("add The 4")
J("stats")
J("known Skiff skiff SKIFF Linux linux The the")
J("unknown Skiff skiff SKIFF Linux linux The the")
J("candidates Skif")
J("candidates skif")
J("correction Linx")
J("correction linx")
J("candidates THe")
J("ed1 Ab")
J("export data/names.json")
J("open folded data/names.json")
J("stats")
J("freq the")
J("freq skiff")
J("freq linux")
J("freq api")
J("use saved")
J("stats")
J("candidates srvice")

with open("data/corpus.txt", "w", encoding="utf-8", newline="\n") as f:
    f.write(TEXT)
with open("data/jobs.txt", "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(jobs) + "\n")
print(len(TEXT), "bytes of corpus,", len(jobs), "jobs,", len(WORDS), "distinct words")
