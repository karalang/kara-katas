# Writes data/: unidiff's own sample diffs (samples/, from its test
# suite), malformed and corner-case diffs, a generated project with three
# changes to it (its files before and after, and git diffs of each
# change at three context widths), the inputs of four programs built on
# unidiff (a diffstat, a patch applier, a code-review comment mapper and
# a scanner of added lines), and data/jobs.tsv, the jobs
# mini_unidiff.kara and oracle.py run.
import difflib
import os
import random
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def write(rel, text):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


# ------------------------------------------------- corners and mistakes

EXTRA = {
    "too_long.diff": "--- a/x\n+++ b/x\n@@ -1,2 +1,2 @@\n one\n-two\n+zwei\n three\n",
    "too_short.diff": "--- a/x\n+++ b/x\n@@ -1,3 +1,3 @@\n one\n-two\n+zwei\n",
    "target_without_source.diff": "diff --git a/x b/x\nindex 1..2 100644\n+++ b/y\n@@ -1 +1 @@\n-a\n+b\n",
    "unexpected_hunk.diff": "some notes\n@@ -1 +1 @@\n-a\n+b\n",
    "orphan_new_file.diff": "new file mode 100644\n--- /dev/null\n+++ b/n\n@@ -0,0 +1 @@\n+n\n",
    "orphan_deleted_file.diff": "deleted file mode 100644\n",
    "orphan_marker.diff": "\\ No newline at end of file\n",
    "blank_before_hunk.diff": "diff --git a/x b/x\nindex 1..2 100644\n\n--- a/x\n+++ b/x\n",
    "bad_body_line.diff": "--- a/x\n+++ b/x\n@@ -1,2 +1,2 @@\n one\n*two\n",
    "no_lengths.diff": "--- a/one\n+++ b/one\n@@ -1 +1 @@\n-before\n+after\n",
    "section_headers.diff": (
        "diff --git a/lib.c b/lib.c\nindex 3f1..9a0 100644\n--- a/lib.c\n+++ b/lib.c\n"
        "@@ -10,4 +10,5 @@ int parse(const char *s)\n {\n-    return 0;\n+    if (!s)\n+        return -1;\n     return 1;\n }\n"
        "@@ -40,3 +41,3 @@\n x\n-y\n+Y\n z\n"
        "@@ -60,2 +61,2 @@static void done(void)\n-a\n+b\n c\n"
    ),
    "blank_context.diff": "--- a/t.txt\n+++ b/t.txt\n@@ -1,4 +1,4 @@\n first\n\n-third\n+THIRD\n\n",
    "blank_context_crlf.diff": "--- a/t.txt\r\n+++ b/t.txt\r\n@@ -1,3 +1,3 @@\r\n first\r\n\r\n-third\r\n+THIRD\r\n",
    "marker_mid_hunk.diff": (
        "diff --git a/v b/v\nindex 1..2 100644\n--- a/v\n+++ b/v\n"
        "@@ -1,2 +1,2 @@\n keep\n-old\n\\ No newline at end of file\n+new\n\\ No newline at end of file\n"
    ),
    "empty_hunk.diff": "--- a/e\n+++ b/e\n@@ -3,0 +3,0 @@\n",
    "empty_hunk_then_line.diff": "--- a/e\n+++ b/e\n@@ -3,0 +3,0 @@\n stray\n",
    "source_mismatch.diff": (
        "diff --git a/x b/x\nindex 1..2 100644\n--- a/y\n+++ b/x\n@@ -1 +1 @@\n-p\n+q\n"
    ),
    "binary_odd_names.diff": (
        "Binary files a/x and y.png and b/x and y.png differ\n"
        "Binary files a/s.db\t2024-01-02 10:11:12 +0100 and b/s.db\t2024-01-03 09:00:00 +0100 differ\n"
        "Binary files a/k.bin\t12:00 and b/k.bin differ (twice) differ\n"
    ),
    "binary_no_target.diff": "Binary file build/app.wasm has changed\nBinary files only/a differ\n",
    "uri_like.diff": (
        "diff --git file:///srv/a/conf.ini file:///srv/b/conf.ini\nindex 1..2 100644\n"
        "--- file:///srv/a/conf.ini\n+++ file:///srv/b/conf.ini\n@@ -1 +1 @@\n-port=80\n+port=8080\n"
    ),
    "no_prefix_spaces.diff": (
        "diff --git my notes.txt my notes.txt\nindex 1..2 100644\n--- my notes.txt\n+++ my notes.txt\n"
        "@@ -1,2 +1,2 @@\n-tea\n+coffee\n biscuits\n"
    ),
    "trailing_blank.diff": "--- a/z\n+++ b/z\n@@ -1 +1 @@\n-z\n+Z\n\n\n",
    "unicode.diff": (
        "diff --git a/README.fr.md b/README.fr.md\nindex 1..2 100644\n--- a/README.fr.md\n+++ b/README.fr.md\n"
        "@@ -1,3 +1,3 @@ # Démarrage\n-Installez le paquet avec « pip ».\n+Installez le paquet avec « pipx ».\n"
        " Voir aussi : la FAQ, l'été dernier.\n Ça marche — normalement.\n"
    ),
    "email_patch.diff": (
        "From 1a2b3c Mon Sep 17 00:00:00 2001\nFrom: Dev <dev@example.org>\nSubject: [PATCH 1/2] fix off by one\n\n"
        "---\n src/count.py | 2 +-\n 1 file changed, 1 insertion(+), 1 deletion(-)\n\n"
        "diff --git a/src/count.py b/src/count.py\nindex 11..22 100644\n--- a/src/count.py\n+++ b/src/count.py\n"
        "@@ -1,3 +1,3 @@ def count(xs):\n def count(xs):\n-    return len(xs) - 1\n+    return len(xs)\n # end\n"
        "-- \n2.43.0\n\n"
    ),
}

# ------------------------------------------------- a generated project

WORDS = ["cache", "user", "token", "order", "price", "queue", "event", "batch", "retry", "limit",
         "client", "server", "config", "record", "index", "shard", "lease", "report"]


def code_line(r):
    k = r.randrange(8)
    a, b = r.choice(WORDS), r.choice(WORDS)
    if k == 0:
        return "def %s_%s(%s):\n" % (a, b, a)
    if k == 1:
        return "    return %s.get(%s)\n" % (a, b)
    if k == 2:
        return "    %s = %s + %d\n" % (a, b, r.randrange(100))
    if k == 3:
        return "\n"
    if k == 4:
        return "    # TODO: %s the %s\n" % (a, b)
    if k == 5:
        return "    print(%s)\n" % a
    if k == 6:
        return "    if %s > %d:\n" % (a, r.randrange(50))
    return "    %s.%s(%s)\n" % (a, b, r.choice(WORDS))


def make_file(r, n):
    return [code_line(r) for _ in range(n)]


def edit(r, lines):
    out = list(lines)
    for _ in range(r.randint(1, 5)):
        if not out:
            out = make_file(r, 3)
            continue
        i = r.randrange(len(out))
        k = r.randrange(3)
        if k == 0:
            del out[i:i + r.randint(1, 4)]
        elif k == 1:
            out[i:i] = make_file(r, r.randint(1, 4))
        else:
            out[i] = code_line(r)
    return out


def text(lines, nonl=False):
    s = "".join(lines)
    return s[:-1] if nonl and s.endswith("\n") else s


def udiff(a_text, b_text, a_name, b_name, n):
    a = a_text.splitlines(keepends=True)
    b = b_text.splitlines(keepends=True)
    out = []
    for line in difflib.unified_diff(a, b, a_name, b_name, n=n):
        if line.endswith("\n"):
            out.append(line)
        else:
            out.append(line + "\n\\ No newline at end of file\n")
    return "".join(out)


def git_change(before, after, renames, n):
    out = []
    names = sorted(set(before) | set(after) | set(renames))
    for name in names:
        if name in renames:
            new = renames[name]
            a, b = before[name], after[new]
            sim = 100 - 5 * len(a.splitlines()) % 30
            out.append("diff --git a/%s b/%s\nsimilarity index %d%%\nrename from %s\nrename to %s\n"
                       % (name, new, sim, name, new))
            if a != b:
                out.append("index 4f1e2d3..9a8b7c6 100644\n")
                out.append(udiff(a, b, "a/" + name, "b/" + new, n))
            continue
        if name in set(renames.values()):
            continue
        if name.endswith(".png"):
            if name in before and name in after and before[name] != after[name]:
                out.append("diff --git a/%s b/%s\nindex 0a0a0a0..1b1b1b1 100644\n"
                           "Binary files a/%s and b/%s differ\n" % (name, name, name, name))
            continue
        if name not in before:
            out.append("diff --git a/%s b/%s\nnew file mode 100644\nindex 0000000..e69de29\n" % (name, name))
            out.append(udiff("", after[name], "/dev/null", "b/" + name, n))
        elif name not in after:
            out.append("diff --git a/%s b/%s\ndeleted file mode 100644\nindex e69de29..0000000\n" % (name, name))
            out.append(udiff(before[name], "", "a/" + name, "/dev/null", n))
        elif before[name] != after[name]:
            out.append("diff --git a/%s b/%s\nindex 1234567..89abcde 100644\n" % (name, name))
            out.append(udiff(before[name], after[name], "a/" + name, "b/" + name, n))
    return "".join(out)


def project(r):
    files = {}
    for d in ["app", "lib", "tests"]:
        for k in range(r.randint(2, 4)):
            name = "%s/%s_%d.py" % (d, r.choice(WORDS), k)
            files[name] = text(make_file(r, r.randint(6, 40)), nonl=r.random() < 0.2)
    files["assets/logo.png"] = "PNG-v1"
    return files


def change(r, before, step):
    after = {}
    renames = {}
    names = sorted(before)
    for name in names:
        if name.endswith(".png"):
            after[name] = before[name] if step % 2 else "PNG-v%d" % (step + 2)
            continue
        roll = r.random()
        if roll < 0.08:
            continue
        lines = before[name].splitlines(keepends=True)
        nonl = before[name] != "" and not before[name].endswith("\n")
        if nonl and r.random() < 0.5:
            lines[-1] += "\n"
            nonl = False
        elif not nonl and r.random() < 0.15:
            nonl = True
        new = text(edit(r, lines), nonl) if roll < 0.75 else before[name]
        if r.random() < 0.12:
            dst = name.replace(".py", "_v%d.py" % step)
            renames[name] = dst
            after[dst] = new
        else:
            after[name] = new
    for k in range(r.randint(1, 2)):
        after["%s/new_%s_%d.py" % (r.choice(["app", "lib"]), r.choice(WORDS), step * 10 + k)] = \
            text(make_file(r, r.randint(3, 12)), nonl=r.random() < 0.3)
    return after, renames


def put_tree(rel, files):
    for name, body in files.items():
        write("%s/%s" % (rel, name), body)


def main():
    if os.path.isdir(DATA):
        shutil.rmtree(DATA)
    jobs = []
    for name in sorted(os.listdir(os.path.join(HERE, "samples"))):
        with open(os.path.join(HERE, "samples", name), encoding="utf-8", newline="") as f:
            write("samples/" + name, f.read())
        for mode in ["string", "file", "meta"]:
            jobs.append(["parse", "samples/" + name, mode])
    for name in sorted(EXTRA):
        write("extra/" + name, EXTRA[name])
        for mode in ["string", "file", "meta"]:
            jobs.append(["parse", "extra/" + name, mode])

    r = random.Random(150)
    tree = project(r)
    put_tree("project/v0", tree)
    for step in range(1, 4):
        after, renames = change(r, tree, step)
        put_tree("project/v%d" % step, after)
        for n in [3, 1, 0]:
            rel = "project/change%d_U%d.diff" % (step, n)
            write(rel, git_change(tree, after, renames, n))
            jobs.append(["parse", rel, "string"])
            jobs.append(["stat", rel])
            jobs.append(["apply", rel, "project/v%d" % (step - 1), "project/v%d" % step])
            jobs.append(["revert", rel, "project/v%d" % step, "project/v%d" % (step - 1)])
        comments = []
        for name in sorted(after):
            if name.endswith(".png"):
                continue
            nl = len(after[name].splitlines())
            for _ in range(3):
                comments.append("%s\t%d" % (name, r.randint(1, nl + 2)))
        comments.append("nowhere/missing.py\t4")
        write("project/comments%d.tsv" % step, "\n".join(comments) + "\n")
        jobs.append(["position", "project/change%d_U3.diff" % step, "project/comments%d.tsv" % step])
        jobs.append(["position", "project/change%d_U0.diff" % step, "project/comments%d.tsv" % step])
        jobs.append(["scan", "project/change%d_U3.diff" % step, "rules.txt"])
        tree = after
    # a patch made against the wrong base: applying it fails
    jobs.append(["apply", "project/change2_U3.diff", "project/v0", "project/v2"])
    jobs.append(["apply", "project/change3_U0.diff", "project/v1", "project/v3"])
    for name in ["sample0.diff", "sample1.diff", "git.diff", "svn.diff", "hg.diff", "bzr.diff", "binary.diff",
                 "git_rename.diff", "sample8.diff"]:
        jobs.append(["stat", "samples/" + name])
    jobs.append(["stat", "extra/email_patch.diff"])
    jobs.append(["stat", "extra/binary_odd_names.diff"])
    jobs.append(["scan", "extra/email_patch.diff", "rules.txt"])
    jobs.append(["scan", "samples/sample0.diff", "rules.txt"])
    write("rules.txt", "TODO\nprint(\npassword\nlen(\nimportant\nCR\n")
    write("jobs.tsv", "".join("\t".join(j) + "\n" for j in jobs))


main()
