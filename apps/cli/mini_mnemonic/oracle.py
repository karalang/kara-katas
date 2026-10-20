# Runs data/jobs.tsv through python-mnemonic itself (vendor/mnemonic,
# unchanged) and prints what each job gives; expected.out is this output.
# The package reads its wordlists from vendor/mnemonic/wordlist, which
# holds the same files mk.py copies to data/wordlist.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
sys.dont_write_bytecode = True
os.chdir(HERE)

from mnemonic import Mnemonic  # noqa: E402
from mnemonic.mnemonic import b58encode  # noqa: E402

DATA = "data"


def show(text):
    out = []
    for c in text:
        if c == "\r":
            out.append("<CR>")
        elif (c < " " and c not in "\t\n") or "\x7f" <= c <= "\x9f":
            out.append("<x%02x>" % ord(c))
        else:
            out.append(c)
    return "".join(out)


def print(line):
    # Every line goes out through show().
    sys.stdout.write(show(line) + "\n")


def err(e):
    msg = str(e)
    # detect_language names the languages in set order, which changes
    # from run to run; they are sorted here.
    head = "Language ambiguous between "
    if msg.startswith(head):
        msg = head + ", ".join(sorted(msg[len(head):].split(", ")))
    return "error: %s: %s" % (type(e).__name__, msg)


def read(name):
    with open(os.path.join(DATA, name), encoding="utf-8", newline="") as f:
        return f.read()


def lines(name):
    return read(name).split("\n")[:-1]


def short(p):
    words = p.split()
    return "%s ... %s (%d words)" % (words[0], words[-1], len(words))


def vectors_job(args):
    lang = args[0]
    m = Mnemonic(lang)
    for row in lines("vectors.tsv"):
        f = row.split("\t")
        if f[0] != lang:
            continue
        ent, words, seed, xprv = f[1], f[2], f[3], f[4]
        code = m.to_mnemonic(bytes.fromhex(ent))
        notes = []
        notes.append("mnemonic " + ("ok" if code == words else "differs: " + code))
        notes.append("check %s" % m.check(words))
        try:
            back = m.to_entropy(code.split()).hex()
            notes.append("entropy " + ("ok" if back == ent else back))
        except Exception as e:
            notes.append("entropy " + err(e))
        key = Mnemonic.to_hd_master_key(bytes.fromhex(seed))
        notes.append("xprv " + ("ok" if key == xprv else key))
        print("%s %s: %s" % (ent[:8], short(code), ", ".join(notes)))


def seed_job(args):
    s = Mnemonic.to_seed(args[0], args[1])
    print("seed " + s.hex())
    print("xprv " + Mnemonic.to_hd_master_key(s))
    print("tprv " + Mnemonic.to_hd_master_key(s, testnet=True))


def to_mnemonic_job(args):
    try:
        print(Mnemonic(args[0]).to_mnemonic(bytes.fromhex(args[1])))
    except Exception as e:
        print(err(e))


def check_job(args):
    print("check = %s" % Mnemonic(args[0]).check(args[1]))


def to_entropy_job(args, split):
    m = Mnemonic(args[0])
    try:
        e = m.to_entropy(args[1].split() if split else args[1])
        print("to_entropy = " + e.hex())
    except Exception as x:
        print("to_entropy: " + err(x))


def expand_word_job(args):
    print("expand_word(%r) = %r" % (args[1], Mnemonic(args[0]).expand_word(args[1])))


def expand_job(args):
    print("expand = %r" % Mnemonic(args[0]).expand(args[1]))


def detect_job(args):
    try:
        print("detect_language = " + Mnemonic.detect_language(args[0]))
    except Exception as e:
        print(err(e))


def master_job(args):
    try:
        print(Mnemonic.to_hd_master_key(bytes.fromhex(args[0]), testnet=args[1] == "test"))
    except Exception as e:
        print(err(e))


def b58_job(args):
    print("b58encode = %r" % b58encode(bytes.fromhex(args[0])))


def generate_job(args):
    # Only the strength check: the words come from the secrets module.
    n = int(args[0])
    if n in [128, 160, 192, 224, 256]:
        words = Mnemonic("english").generate(n).split(" ")
        print("generate(%d): %d words" % (n, len(words)))
        return
    try:
        Mnemonic("english").generate(n)
    except Exception as e:
        print(err(e))


def new_job(args):
    try:
        m = Mnemonic(args[0])
        print("%s: %d words, first %r, last %r, delimiter %r" % (m.language, len(m.wordlist), m.wordlist[0],
                                                                m.wordlist[-1], m.delimiter))
    except Exception as e:
        print(err(e))


def list_job(args):
    print(", ".join(sorted(Mnemonic.list_languages())))


def custom_job(args):
    words = [w.strip() for w in read(args[0]).split("\n")[:-1]]
    try:
        m = Mnemonic("custom", wordlist=words)
        code = m.to_mnemonic(bytes.fromhex(args[1]))
        print(code)
        print("check %s, to_entropy %s" % (m.check(code), m.to_entropy(code).hex()))
    except Exception as e:
        print(err(e))


# --- programs

def backup_job(args):
    # A recovery backup as written down: numbers ("7." or "07") place the
    # word after them; other tokens are words in order. Abbreviations are
    # expanded, in the language the words point to.
    text = read(args[0])
    placed = {}
    loose = []
    pending = None
    for line in text.split("\n"):
        if line.startswith("#"):
            continue
        for tok in line.split():
            t = tok.rstrip(".")
            if t.isdigit() and t.isascii():
                pending = int(t)
                continue
            if pending is not None:
                placed[pending] = tok.lower()
                pending = None
            else:
                loose.append(tok.lower())
    words = [placed[k] for k in sorted(placed)] if placed and len(placed) >= len(loose) else loose
    try:
        lang = Mnemonic.detect_language(" ".join(words))
    except Exception as e:
        print("%d words; %s" % (len(words), err(e)))
        return
    m = Mnemonic(lang)
    expanded = [m.expand_word(Mnemonic.normalize_string(w)) for w in words]
    unknown = [w for w in expanded if w not in m.wordlist]
    print("%d words, %s" % (len(words), lang))
    print("  " + m.delimiter.join(expanded))
    if unknown:
        print("  not in the %s list: %s" % (lang, ", ".join(repr(w) for w in unknown)))
    print("  check %s" % m.check(" ".join(expanded)))
    try:
        print("  entropy " + m.to_entropy(expanded).hex())
    except Exception as e:
        print("  entropy " + err(e))


def distance(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def recover_job(args):
    lang, p = args
    m = Mnemonic(lang)
    words = p.split(" ")
    if m.check(p):
        print("valid as typed")
        return
    norm = [Mnemonic.normalize_string(w) for w in words]
    unknown = [i for i, w in enumerate(norm) if w not in m.wordlist]
    if len(unknown) > 1:
        print("%d words not in the %s list: %s" % (len(unknown), lang, ", ".join(repr(words[i]) for i in unknown)))
        return
    if unknown:
        i = unknown[0]
        pool = m.wordlist if words[i] == "?" else [w for w in m.wordlist if distance(norm[i], w) <= 2]
        found = [w for w in pool if m.check(" ".join(norm[:i] + [w] + norm[i + 1:]))]
        print("word %d (%r): %d candidate%s, %d with a valid checksum" % (i + 1, words[i], len(pool),
                                                                         "" if len(pool) == 1 else "s", len(found)))
        print("  " + ", ".join(found[:8]) + (" ..." if len(found) > 8 else ""))
        if len(found) == 1:
            fixed = norm[:i] + found + norm[i + 1:]
            print("  entropy " + m.to_entropy(fixed).hex())
        return
    swaps = [i for i in range(len(norm) - 1)
             if norm[i] != norm[i + 1] and m.check(" ".join(norm[:i] + [norm[i + 1], norm[i]] + norm[i + 2:]))]
    print("every word is in the list but the checksum fails; %d adjacent swap%s fix%s it" % (
        len(swaps), "" if len(swaps) == 1 else "s", "es" if len(swaps) == 1 else ""))
    for i in swaps:
        print("  words %d and %d (%s, %s)" % (i + 1, i + 2, norm[i], norm[i + 1]))


JOBS = {
    "vectors": vectors_job, "seed": seed_job, "to_mnemonic": to_mnemonic_job, "check": check_job,
    "to_entropy": lambda a: to_entropy_job(a, False), "to_entropy_split": lambda a: to_entropy_job(a, True),
    "expand_word": expand_word_job, "expand": expand_job, "detect": detect_job, "master": master_job,
    "b58": b58_job, "generate": generate_job, "new": new_job, "list_languages": list_job, "custom": custom_job,
    "backup": backup_job, "recover": recover_job,
}


def main():
    for line in lines("jobs.tsv"):
        job = line.split("\t")
        print("== " + " ".join(job))
        JOBS[job[0]](job[1:])


main()
