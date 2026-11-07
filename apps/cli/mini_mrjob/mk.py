"""Writes data/ for mini_mrjob: two text inputs made from a small invented
vocabulary, an empty one, and a script that defines and runs jobs on them,
with a few mistakes.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)


def put(name, text):
    with open(os.path.join("data", name), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


# A linear congruential generator, so the text is the same everywhere.
state = 20261107


def rand(n):
    global state
    state = (state * 1103515245 + 12345) % 2147483648
    return (state // 65536) % n


NOUNS = ["river", "lamp", "harbor", "orchard", "kettle", "ledger", "meadow",
         "lantern", "quarry", "signal", "bridge", "garden", "engine", "window",
         "market", "tower", "anchor", "valley", "mirror", "basket"]
VERBS = ["carries", "holds", "finds", "mends", "counts", "keeps", "turns",
         "follows", "guards", "lifts", "paints", "opens"]
ADJS = ["old", "quiet", "bright", "narrow", "heavy", "green", "early",
        "small", "far", "warm"]
SMALL = ["the", "a", "and", "of", "by", "to", "in"]


def sentence():
    parts = [SMALL[rand(2)], ADJS[rand(len(ADJS))], NOUNS[rand(len(NOUNS))],
             VERBS[rand(len(VERBS))], SMALL[rand(len(SMALL))],
             NOUNS[rand(len(NOUNS))]]
    if rand(3) == 0:
        parts += [SMALL[2], SMALL[0], ADJS[rand(len(ADJS))], NOUNS[rand(len(NOUNS))]]
    s = " ".join(parts)
    s = s[0].upper() + s[1:]
    end = [".", ".", "!", "?", ";"][rand(5)]
    return s + end


def text(lines):
    out = []
    for _ in range(lines):
        k = 1 + rand(3)
        line = " ".join(sentence() for _ in range(k))
        if rand(7) == 0:
            line = line.replace(" ", "  ", 1) + " -- " + str(rand(1000))
        if rand(9) == 0:
            line = line.upper()
        out.append(line)
    return "\n".join(out) + "\n"


os.makedirs(os.path.join("data", "input"), exist_ok=True)
put("input/harbor.txt", text(160))
put("input/orchard.txt", text(90))
put("input/empty.txt", "")

put("script.txt", """\
# Inputs: a name for one or more files under data/input.
input harbor input/harbor.txt
input orchard input/orchard.txt
input both input/harbor.txt input/orchard.txt
input none input/empty.txt
input lost input/missing.txt
input harbor input/orchard.txt
input Bad input/harbor.txt

# Jobs: steps of mapper|reducer or mapper|combiner|reducer.
job wc words|sum|sum
job wc_plain words|sum
job top words|sum|sum pack|top3
job letters words|sum|sum first_letter|sum
job idx index|collect
job lens lengths|count
job pairs bigrams|sum|sum pack|top3
job widest lengths|sum|sum total|max
job bad_sum index|sum
job bad_pack pack|top3
job bad_first lengths|count first_letter|sum
job typo words|summ
job nocombine words|count|sum
job wc words|sum

# Runs.
run wc harbor
run wc harbor maps=1 reduces=1
run wc_plain harbor maps=7 reduces=5
run top both maps=5 reduces=2
run letters orchard show=26
run idx orchard maps=3 reduces=4 show=2
run lens both maps=2 reduces=3 show=20
run pairs harbor reduces=1
run widest both
run wc none
run top none
run bad_sum harbor
run bad_pack harbor
run bad_first orchard maps=3
run nojob harbor
run wc nowhere
run wc harbor maps=0
run wc harbor reduces=x
run wc harbor speed=9
run wc
jobs
""")
