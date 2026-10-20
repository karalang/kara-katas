# Writes data/: documents that two people edit at the same time (a deploy
# runbook, a service config, a short story, a contract with typographic
# quotes and an emoji, a server log), saved patch files (one hand-edited,
# one broken), and jobs.txt, the list of jobs the run performs.
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

DEPLOY = """# Deploying the billing service

1. Announce the deploy in #ops and wait five minutes.
2. Check that the build on main is green.
3. Pull the release branch:

       git fetch origin
       git checkout release/2.4

4. Run the database migrations:

       ./manage.py migrate --plan
       ./manage.py migrate

5. Restart the workers one at a time:

       systemctl restart billing-worker@1
       systemctl restart billing-worker@2

6. Watch the error rate on the dashboard for ten minutes.
7. If it goes above 2%, roll back with `./deploy.sh rollback`.
"""

DEPLOY_ALICE = DEPLOY.replace(
    "2. Check that the build on main is green.",
    "2. Check that the build on main is green and that the canary passed.",
).replace(
    "       ./manage.py migrate --plan\n",
    "       ./manage.py migrate --plan\n       ./manage.py check --deploy\n",
).replace("ten minutes", "fifteen minutes")

DEPLOY_BOB = DEPLOY.replace("five minutes", "5 minutes").replace(
    "7. If it goes above 2%, roll back with `./deploy.sh rollback`.\n",
    "7. If it goes above 2%, roll back with `./deploy.sh rollback`.\n8. Post the release notes in #billing.\n",
).replace("release/2.4", "release/2.5")

CONFIG = """service:
  name: checkout
  port: 8080
  replicas: 3
database:
  host: db.internal
  pool: 10
  timeout_ms: 2500
cache:
  host: redis.internal
  ttl_s: 300
features:
  new_cart: false
  express_pay: true
"""

CONFIG_OPS = CONFIG.replace("replicas: 3", "replicas: 5").replace("pool: 10", "pool: 20")
CONFIG_DEV = CONFIG.replace("new_cart: false", "new_cart: true").replace("replicas: 3", "replicas: 4")
CONFIG_REWRITE = """# rewritten by the platform team
checkout:
  listen: 0.0.0.0:9090
  instances: 2
"""

STORY = """The lighthouse keeper climbed the stairs every evening at dusk. There were
one hundred and twelve of them, and he counted each one out loud, because the
counting kept his mind off the wind. At the top he trimmed the wick, wiped the
glass, and lit the lamp. Then he sat by the window with his tea and watched the
light sweep across the water, once every eight seconds, all night long.
"""

STORY_V2 = """The lighthouse keeper climbed the stairs each evening at dusk. There were
one hundred and twelve of them, and she counted every one out loud, because the
counting kept her mind off the wind. At the top she trimmed the wick, polished the
glass, and lit the lamp. Then she sat by the window with her coffee and watched the
beam sweep across the dark water, once every eight seconds, all night long.
"""

CONTRACT = """This Agreement (the “Agreement”) is made between Acme Café Ltd. — the
“Supplier” — and the Customer. Payment is due within 30 days of the invoice
date; late payments accrue interest at 1.5% per month. 🙂
"""

CONTRACT_V2 = """This Agreement (the “Agreement”) is made between Acme Café GmbH — the
“Supplier” — and the Customer named below. Payment is due within 45 days of the
invoice date; late payments accrue interest at 1% per month. 🙂👍
"""


def server_log(edit):
    lines = []
    for i in range(1, 161):
        level = "WARN" if i % 17 == 0 else "INFO"
        msg = "slow request /api/orders took %d ms" % (900 + i) if level == "WARN" else \
            "request /api/items/%d served in %d ms" % (i * 7 % 300, 10 + i % 40)
        if edit and i in (23, 24, 90):
            msg = "request /api/items/%d served from cache" % (i * 7 % 300)
        if edit and i == 120:
            lines.append("2024-05-01T12:%02d:%02dZ ERROR worker 3 restarted" % (i // 60, i % 60))
        lines.append("2024-05-01T12:%02d:%02dZ %s %s" % (i // 60, i % 60, level, msg))
    if edit:
        del lines[60:63]
    return "\n".join(lines) + "\n"


PATCH_HAND = """@@ -1,8 +1,9 @@
 service
+s
 :%0A  na
@@ -40,9 +41,9 @@
 ica
-s: 3
+s: 7
 %0Adat
"""

JOBS = r"""# Each job: a kind and its arguments, separated by " | ". An argument
# that starts with file: names a file in data/; otherwise \n, \t, \\ and \uXXXX
# are escapes. "set" changes a setting for the jobs after it.

# the building blocks, on the examples in the library's tests
prefix | abc | xyz
prefix | 1234abcdef | 1234xyz
prefix | 1234 | 1234xyz
suffix | abcdef1234 | xyz1234
suffix | 1234 | xyz1234
overlap | abc | abcd
overlap | 123456xxx | xxxabcd
overlap | fi | \ufb01i
halfmatch | 1234567890 | a345678z
halfmatch | 121231234123451234123121 | a1234123451234z
halfmatch | qHilloHelloHew | xHelloHeHulloy
halfmatch | 1234567890 | abcdef
lines | alpha\nbeta\nalpha\n | beta\nalpha\nbeta\n
bisect | cat | map
xindex | The cat | The big cat | 5
xindex | The cat | The bat | 4

# diffs
diff | The cat sat on the mat. | The big cat sat on a mat.
diff | Apples are a fruit. | Bananas are also fruit.
diff | ax\t | \u0680x\u00e9
diff | 1ayb2 | abxab
diff | abcy | xaxcxabc
diff | a | b
diff | abc | abc
diff |  | abc
diff semantic | The cat came. | The cat came, so did the dog.
diff semantic | mouse | sofas
diff semantic | abcxxx | xxxdef
diff semantic | The cat sat. | The cat sat on the hat.
diff efficiency | abxyzcd | 12xyz34
diff efficiency | ab12xyz34cd | ab1xyz4cd
diff lossless | AAA\r\n\r\nBBB\r\nDDD | AAA\r\n\r\nBBB\r\n\r\nDDD\r\nBBB
diff lossless | The xxx. The zzz. | The xxx. The yyy. The zzz.
diff semantic | file:docs/story.txt | file:docs/story.v2.txt
diff semantic nolines | file:docs/story.txt | file:docs/story.v2.txt
diff semantic | file:docs/contract.txt | file:docs/contract.v2.txt
diff efficiency | file:docs/config.yaml | file:docs/config.ops.yaml
diff semantic | file:docs/server.log | file:docs/server.edited.log
set | Diff_Timeout | 0
diff | 1234567890 | a345678z
diff semantic | file:docs/story.txt | file:docs/story.v2.txt
set | Diff_Timeout | 1.0
set | Diff_EditCost | 5
diff efficiency | abxyzcd | 12xyz34
set | Diff_EditCost | 4

# deltas
fromdelta | The cat sat. | =4\t-3\t+dog\t=5
fromdelta | The cat sat. | =4\t-3\t+%E2%80%9Ccat%E2%80%9D\t=5
fromdelta | Hello 🙂 | =6\t-2\t+%F0%9F%91%8B
fromdelta | abc | =2
fromdelta | abc | =x3
fromdelta | abc | =1\t-2\t=1
fromdelta | abc | *3
fromdelta | abc | =-1\t=4

# fuzzy matching
match | abcdef | abcdef | 1000
match |  | abcdef | 1
match | abcdef |  | 3
match | abcdef | de | 3
match | abcdefghijk | fgh | 5
match | abcdefghijk | efxhi | 0
match | abcdefghijk | bxy | 1
match | 123456789xx0 | 3456789x0 | 2
match | abcdef | xxabc | 4
match | I am the very model of a modern major general. | majr | 33
match | I am the very model of a modern major general. | modern major general | 3
match | The quick brown fox jumps over the lazy dog. | lazy cat | 30
set | Match_Threshold | 0.4
match | abcdefghijk | efxyhi | 1
set | Match_Threshold | 0.3
match | abcdefghijk | efxyhi | 1
set | Match_Threshold | 0.0
match | abcdefghijk | bcdef | 1
set | Match_Threshold | 0.5
set | Match_Distance | 10
match | abcdefghijklmnopqrstuvwxyz | abcdefg | 24
match | abcdefghijklmnopqrstuvwxyz | abcdxxefg | 1
set | Match_Distance | 0
match | abcdefghijklmnopqrstuvwxyz | defg | 3
set | Match_Distance | 1000
match | abcdefghijklmnopqrstuvwxyz | abcdefg | 24

# patches between two versions, and back from their text
patch | The quick brown fox jumps over the lazy dog. | That quick brown fox jumped over a lazy dog.
patch | file:docs/deploy.md | file:docs/deploy.alice.md
patch | file:docs/contract.txt | file:docs/contract.v2.txt
patch | file:docs/config.yaml | file:docs/config.ops.yaml
patch |  | test
patch | abcdef | abcdef
fromtext | file:patches/hand.patch
fromtext | @@ -1 +1 @@\n-a\n+b\n
fromtext | @@ -0,0 +1,3 @@\n+abc\n
fromtext | Bad\nPatch\n
fromtext | @@ -1,3 +1,3 @@\n*abc\n

# a sync server: patch(base, edited) applied to someone else's copy
sync | file:docs/deploy.md | file:docs/deploy.alice.md | file:docs/deploy.bob.md
sync | file:docs/config.yaml | file:docs/config.ops.yaml | file:docs/config.dev.yaml
sync | file:docs/config.yaml | file:docs/config.ops.yaml | file:docs/config.rewrite.yaml
sync | file:docs/server.log | file:docs/server.edited.log | file:docs/server.log
sync | The quick brown fox jumps over the lazy dog. | That quick brown fox jumped over a lazy dog. | The quick red rabbit jumps over the tired tiger.
sync | The quick brown fox jumps over the lazy dog. | That quick brown fox jumped over a lazy dog. | I am the very model of a modern major general.
sync | x | y | 
sync | y |  | xxyyzz
applytext | file:patches/hand.patch | file:docs/config.dev.yaml
set | Patch_DeleteThreshold | 0.6
sync | abcdefghijklmnopqrstuvwxyz--------------------1234567890 | abcXXXXXXXXXXdefghijklmnopqrstuvwxyz--------------------1234567YYYYYYYYYY890 | ABCDEFGHIJKLMNOPQRSTUVWXYZ--------------------1234567890
set | Patch_DeleteThreshold | 0.5
sync | xabcdefghijklmnopqrstuvwxyz--------------------1234567890123456789012345678901234567890xyz | x1234567890123456789012345678901234567890xyz | xabc12345678901234567890---------------++++++++++---------------12345678901234567890y
set | Patch_Margin | 2
patch | file:docs/config.yaml | file:docs/config.ops.yaml
set | Patch_Margin | 4
"""


def write(rel, text):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def main():
    write("docs/deploy.md", DEPLOY)
    write("docs/deploy.alice.md", DEPLOY_ALICE)
    write("docs/deploy.bob.md", DEPLOY_BOB)
    write("docs/config.yaml", CONFIG)
    write("docs/config.ops.yaml", CONFIG_OPS)
    write("docs/config.dev.yaml", CONFIG_DEV)
    write("docs/config.rewrite.yaml", CONFIG_REWRITE)
    write("docs/story.txt", STORY)
    write("docs/story.v2.txt", STORY_V2)
    write("docs/contract.txt", CONTRACT)
    write("docs/contract.v2.txt", CONTRACT_V2)
    write("docs/server.log", server_log(False))
    write("docs/server.edited.log", server_log(True))
    write("patches/hand.patch", PATCH_HAND)
    write("jobs.txt", JOBS)


if __name__ == "__main__":
    main()
