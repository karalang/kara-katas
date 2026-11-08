"""Writes data/ for mini_lancaster: a few small documents a search index
takes in (release notes, a bug report, a recipe, a contract clause, and
French, Greek, Turkish and Russian text), custom rule sets for the
stemmer, and the script that drives it.

Run from this directory: python3 -s -P -B mk.py"""
import os

DOCS = {
    "release_notes": (
        "Release notes for version 4.2 of the scheduler.\n"
        "\n"
        "Fixed: connecting to a replica no longer hangs when the connection\n"
        "is refused; reconnects are retried, and every connected client is\n"
        "told. The installer now provisions the cache before installing\n"
        "plugins, and installation logs say which provision failed.\n"
        "Configuration is configurable per tenant: configured limits are\n"
        "multiplied by the tenant's weight, presumably the maximum anyone\n"
        "needs. Readiness probes report hopefulness no more; they report\n"
        "readiness. Microservices ship 30 megabytes lighter, and the\n"
        "pseudocode in the docs is gone.\n"
    ),
    "bug_report": (
        "Title: the scheduler doesn't retry 404s after a re-run\n"
        "\n"
        "Steps: start the state-of-the-art scheduler (v2.3), queue 12 jobs,\n"
        "kill the worker. The worker's queue shows 'running' for jobs that\n"
        "aren't. Retrying by hand works; retries by the scheduler don't.\n"
        "Expected: retried jobs are \"queued\" again (see #4411).\n"
        "Actual: nothing; the jobs stay running... forever?\n"
        "Notes: mp3s and x86_64 builds both show it. Twelve kilometers of\n"
        "logs, no errors.\n"
    ),
    "recipe": (
        "Slice the onions and boil them while the oven heats. Boiling\n"
        "softens them; boiled onions slice cleanly. Stir the sauce, keep\n"
        "stirring, and when it has stirred for ten minutes add the sliced\n"
        "onions. Bake for forty minutes. Baking longer dries the bakery\n"
        "loaf; baked bread keeps for days. Serves four hungry bakers.\n"
    ),
    "contract": (
        "Provisions. Notwithstanding the provisions above, the Supplier is\n"
        "liable for the liabilities it assumes, provided that the Customer,\n"
        "providing notice, accepts the assignment. Assignments of this\n"
        "Agreement are agreeable to both parties; no agreement binds a\n"
        "party who has not agreed in writing. Disagreements are resolved\n"
        "by arbitration, and the arbitrator's resolution is final.\n"
    ),
    "french": (
        "Le café crème du matin, une élégance naïve: "
        "le résumé des résumés.\n"
        "Les élèves étaient étonnés; la "
        "naïveté étonne toujours.\n"
        "Élégances, CAFÉS et crèmes »sans fin«.\n"
    ),
    "mixed": (
        "ΟΔΟΣ and ΣΑΣ are Greek; "
        "İstanbul and İzmir are Turkish cities.\n"
        "Москва is Russian. "
        "Straße and STRASSE are German streets.\n"
        "ＡＢＣ are fullwidth letters; 東京 is Tokyo.\n"
    ),
}

RULES = {
    # The rule set in NLTK's docstring: "ness" becomes "nest".
    "nest": "ssen4>\ns1t.\n",
    # Comment lines and blank lines are the port's file format, not rules.
    "plurals": (
        "# A tiny English plural stripper.\n"
        "\n"
        "sei3y.\n"
        "sess2.\n"
        "ss0.\n"
        "s1>\n"
        "gni3.\n"
        "de2.\n"
    ),
    # An upper-case letter is not a rule.
    "shouting": "sei3y.\nS1>\n",
    # A trailing space is not part of a rule either, so the rule fails.
    "spaced": "s1. \n",
    # A digit that is two digits long: the pattern takes exactly one.
    "greedy": "gni10>\n",
    # No rules at all: the stemmer falls back to its default rule tuple.
    "empty": "# nothing here\n",
    # A rule may append letters and carry on (`>`), and a rule ending in
    # neither `>` nor `.` carries on too: only `.` stops.
    "chain": "gni3e\nezi2>\nz1s.\n",
    # Intact rules (`*`) fire only on a word no rule has touched yet.
    "intact": "s*1>\ne1.\nsei*3y.\n",
}

SCRIPT = """\
# The default stemmer: NLTK's own doctest words first.
stem maximum presumably multiply provision owed ear saying crying string meant cement
stem Running RUNS runner runners ran
stem connection connections connected connecting connects
stem hopefulness readiness kilometer microservices
stem don't x86_64 404s mp3s state-of-the-art 'quoted'
stem café ÉLÉGANCE naïveté résumés
stem ΟΔΟΣ İstanbul Straße ＡＢＣ
stem a i y is us as
stem ia ai ha aia
stem

# The prefix flag strips one of a fixed list of prefixes first.
use default prefix
stem kilometer kilo kilos microservices millimeter megabytes pseudocode ultrasonic intranet nanoseconds picojoules
stem-repeat kilo 1
stem-repeat ness 250
stem-repeat ness 251
use default
stem-repeat ness 250
stem-repeat ness 251
stem-repeat éness 200
stem-repeat éness 201
stem-repeat abc 0

# Custom rule sets.
use nest
stem ness business ness's nests
use plurals
stem ponies classes glass dogs dog running ended needed is
use shouting
use spaced
use greedy
stem running
use empty
stem running connections
use chain
stem running organizing amazing
use intact
stem cats cases ponies ties tie
use missing
use

# An index over the documents, with the default stemmer.
use default
index release_notes
index bug_report
index recipe
index contract
index french
index mixed
index nowhere
classes
classes 3
top 12
query connect
query connections retried
query bake
query baking slicing
query provisions agreement
query ÉLÉGANCE
query οδος
query nothing-here
query

# Re-indexing a document replaces it; switching stemmers empties the index.
index recipe
top 3
use default prefix
top 3
index bug_report
index release_notes
query meters
query kilometers
classes 2

stemm word
top many
classes -1
stem-repeat ness many
"""

os.makedirs("data/docs", exist_ok=True)
os.makedirs("data/rules", exist_ok=True)
for name, text in DOCS.items():
    with open(f"data/docs/{name}.txt", "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
for name, text in RULES.items():
    with open(f"data/rules/{name}.rules", "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
with open("data/script.txt", "w", encoding="utf-8", newline="") as fh:
    fh.write(SCRIPT)
