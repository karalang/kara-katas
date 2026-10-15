# The oracle: makes the patch with Python's difflib and applies it with
# GNU patch (fuzz 0), printing what mini_patch prints.
import difflib, os, shutil, subprocess
def files(t):
    return sorted(os.listdir(t)) if os.path.isdir(t) else []
def read_lines(p):
    return open(p).read().splitlines(keepends=True) if p else []
def udiff(a, b, an, bn):
    out = []
    for line in difflib.unified_diff(a, b, an, bn, n=3):
        if not line.endswith("\n"):
            line += "\n\\ No newline at end of file\n"
        out.append(line)
    return "".join(out)
def tree_diff(old, new, ap, bp):
    names = sorted(set(files(old)) | set(files(new)))
    out = []
    for n in names:
        if n.endswith(".rej"):
            continue
        a = os.path.join(old, n) if n in files(old) else None
        b = os.path.join(new, n) if n in files(new) else None
        la, lb = read_lines(a), read_lines(b)
        if la == lb:
            continue
        out.append(f"diff -u {ap}{n} {bp}{n}\n")
        out.append(udiff(la, lb, f"{ap}{n}" if a else "/dev/null", f"{bp}{n}" if b else "/dev/null"))
    return "".join(out)
def patch(tree, args, pfile):
    r = subprocess.run(["patch", "-p1", "-F0", "--no-backup-if-mismatch", *args, "-i", "../" + pfile], cwd=tree, capture_output=True, text=True)
    print(r.stdout, end=""); print(r.stderr, end="")
    print(f"[exit {r.returncode}]")
def compare(tree, want):
    d = tree_diff(want, tree, "want/", "got/")
    print("identical to " + want if d == "" else d, end="\n" if d == "" else "")
    for n in files(tree):
        if n.endswith(".rej"):
            print(f"-- {n}")
            print(open(os.path.join(tree, n)).read(), end="")
p = tree_diff("before", "after", "a/", "b/")
open("changes.patch", "w").write(p)
print("== mini_patch diff before after > changes.patch")
print(p, end="")
shutil.rmtree("work", ignore_errors=True); shutil.copytree("before", "work")
print("== mini_patch apply -p1 work < changes.patch")
patch("work", [], "changes.patch"); compare("work", "after")
print("== mini_patch apply -R -p1 work < changes.patch")
patch("work", ["-R"], "changes.patch"); compare("work", "before")
shutil.rmtree("work", ignore_errors=True); shutil.copytree("drifted", "work")
print("== mini_patch apply -p1 drifted < changes.patch")
patch("work", [], "changes.patch"); compare("work", "after")
for name in ["bad.patch", "notes.patch"]:
    shutil.rmtree("work", ignore_errors=True); shutil.copytree("before", "work")
    print(f"== mini_patch apply -p1 before < {name}")
    patch("work", [], "patches/" + name); compare("work", "before")
