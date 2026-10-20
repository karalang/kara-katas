# Runs data/jobs.tsv through Python 3.13's own filecmp module and prints
# what expected.out holds. Run it from the app directory, after mk.py.
import os
import shutil
import filecmp
import getopt

WORK = "work"


def unesc(s):
    out = []
    i = 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            out.append({"n": "\n", "t": "\t", "\\": "\\"}.get(s[i + 1], s[i + 1]))
            i += 2
            continue
        out.append(s[i])
        i += 1
    return "".join(out)


def write_file(path, body, mtime):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(body)
    os.utime(path, (mtime, mtime))


def build(name):
    root = os.path.join(WORK, name)
    os.makedirs(root, exist_ok=True)
    with open(f"data/trees/{name}.tsv", encoding="utf-8") as f:
        lines = f.read().split("\n")[:-1]
    for line in lines:
        if not line:
            continue
        kind, path, mtime, body = line.split("\t")
        p = os.path.join(root, path)
        if kind == "d":
            os.makedirs(p, exist_ok=True)
        elif kind == "f":
            write_file(p, unesc(body), int(mtime))
        else:
            os.symlink(body, p)


def names(field):
    # "-" means the default (None), "" an empty list
    if field == "-":
        return None
    if field == "":
        return []
    return field.split(",")


def err(e):
    return f"{type(e).__name__}: {e}"


def attrs(d):
    for a in ["left_list", "right_list", "common", "left_only", "right_only",
              "common_dirs", "common_files", "common_funny", "same_files",
              "diff_files", "funny_files"]:
        print(f"  {a}: {getattr(d, a)}")
    print(f"  subdirs: {list(d.subdirs)}")


def run_job(name, lines):
    print(f"== {name}")
    for line in lines:
        f = line.split("\t")
        op = f[0]
        try:
            if op == "cmp":
                r = filecmp.cmp(f[1], f[2], shallow=f[3] == "shallow")
                print(f"cmp({f[1]!r}, {f[2]!r}, shallow={f[3] == 'shallow'}) = {r}")
            elif op == "write":
                write_file(f[1], unesc(f[2]), int(f[3]))
                print(f"wrote {f[1]} (mtime {f[3]})")
            elif op == "clear_cache":
                filecmp.clear_cache()
                print("clear_cache()")
            elif op == "cmpfiles":
                common = f[3].split(",") if f[3] else []
                r = filecmp.cmpfiles(f[1], f[2], common, shallow=f[4] == "shallow")
                print(f"cmpfiles({f[1]!r}, {f[2]!r}, {common}, shallow={f[4] == 'shallow'}) = {r}")
            elif op in ("attrs", "report", "partial", "full"):
                print(f"{op} {f[1]} {f[2]} ignore={names(f[3])} hide={names(f[4])} {f[5]}:")
                d = filecmp.dircmp(f[1], f[2], names(f[3]), names(f[4]), shallow=f[5] == "shallow")
                if op == "attrs":
                    attrs(d)
                elif op == "report":
                    d.report()
                elif op == "partial":
                    d.report_partial_closure()
                else:
                    d.report_full_closure()
            elif op == "demo":
                argv = f[1].split(" ")
                print(f"$ python -m filecmp {f[1]}")
                options, args = getopt.getopt(argv, "r")
                if len(args) != 2:
                    raise getopt.GetoptError("need exactly two args", None)
                dd = filecmp.dircmp(args[0], args[1])
                if ("-r", "") in options:
                    dd.report_full_closure()
                else:
                    dd.report()
            else:
                raise SystemExit("bad op " + op)
        except Exception as e:
            print(f" -> {err(e)}")


# ------------------------------------------------------------ programs

def walk(d, prefix, out):
    for x in d.left_only:
        kind = "dir" if os.path.isdir(os.path.join(d.left, x)) else "file"
        out.append(("+", prefix + x, kind))
    for x in d.right_only:
        kind = "dir" if os.path.isdir(os.path.join(d.right, x)) else "file"
        out.append(("-", prefix + x, kind))
    for x in d.diff_files:
        out.append(("~", prefix + x, "file"))
    for x in d.common_funny + d.funny_files:
        out.append(("!", prefix + x, "?"))
    for x, sd in d.subdirs.items():
        walk(sd, prefix + x + "/", out)


def prog_drift():
    print("== program: deploy drift")
    d = filecmp.dircmp("release", "deployed", shallow=False)
    out = []
    walk(d, "", out)
    what = {"+": "missing on the server", "-": "only on the server",
            "~": "differs", "!": "cannot be compared"}
    for sign, path, kind in out:
        print(f"  {sign} {path} ({kind}, {what[sign]})")
    counts = {s: sum(1 for o in out if o[0] == s) for s in "+-~!"}
    print(f"  {counts['+']} missing, {counts['-']} extra, {counts['~']} changed, "
          f"{counts['!']} problems; deploy needed: {'yes' if out else 'no'}")
    shallow = filecmp.dircmp("release", "deployed")
    s_out = []
    walk(shallow, "", s_out)
    missed = [o[1] for o in out if o not in s_out]
    print(f"  a shallow check would miss: {missed}")


def prog_backups():
    print("== program: nightly backup check")
    days = ["backup-mon", "backup-tue", "backup-wed"]
    for i in range(len(days) - 1):
        a, b = days[i], days[i + 1]
        names_ = sorted(set(os.listdir(a)) | set(os.listdir(b)))
        sh = filecmp.cmpfiles(a, b, names_, shallow=True)
        dp = filecmp.cmpfiles(a, b, names_, shallow=False)
        print(f"  {a} -> {b}: {len(names_)} names")
        print(f"    shallow: same {sh[0]}, changed {sh[1]}, missing {sh[2]}")
        print(f"    deep:    same {dp[0]}, changed {dp[1]}, missing {dp[2]}")
        missed = [x for x in sh[0] if x in dp[1]]
        print(f"    changed but missed by the shallow check: {missed}")


def plan(d, prefix, steps):
    for x in d.left_only:
        src = os.path.join(d.left, x)
        steps.append(("copytree" if os.path.isdir(src) else "copy", prefix + x))
    for x in d.diff_files:
        steps.append(("update", prefix + x))
    for x in d.right_only:
        dst = os.path.join(d.right, x)
        steps.append(("rmtree" if os.path.isdir(dst) else "remove", prefix + x))
    for x, sd in d.subdirs.items():
        plan(sd, prefix + x + "/", steps)


def same_tree(d):
    if d.left_only or d.right_only or d.diff_files or d.funny_files or d.common_funny:
        return False
    return all(same_tree(sd) for sd in d.subdirs.values())


def prog_sync():
    print("== program: mirror sync")
    steps = []
    plan(filecmp.dircmp("src", "mirror", shallow=False), "", steps)
    for op, path in steps:
        print(f"  {op} {path}")
        s = os.path.join("src", path)
        m = os.path.join("mirror", path)
        if op == "copytree":
            shutil.copytree(s, m, copy_function=shutil.copy2)
        elif op in ("copy", "update"):
            shutil.copy2(s, m)
        elif op == "rmtree":
            shutil.rmtree(m)
        else:
            os.remove(m)
    print(f"  {len(steps)} steps")
    filecmp.clear_cache()
    filecmp.dircmp("src", "mirror").report_full_closure()
    print(f"  in sync: {same_tree(filecmp.dircmp('src', 'mirror', shallow=False))}")


PROGRAMS = {"drift": prog_drift, "backups": prog_backups, "sync": prog_sync}


def main():
    if os.path.exists(WORK):
        shutil.rmtree(WORK)
    jobs = open("data/jobs.tsv", encoding="utf-8").read().split("\n")[:-1]
    i = 0
    while i < len(jobs) and jobs[i].startswith("build\t"):
        build(jobs[i].split("\t")[1])
        i += 1
    jobs = jobs[i:]
    os.chdir(WORK)
    i = 0
    while i < len(jobs):
        f = jobs[i].split("\t")
        if f[0] == "job":
            body = []
            i += 1
            while i < len(jobs) and jobs[i].split("\t")[0] not in ("job", "program"):
                body.append(jobs[i])
                i += 1
            run_job(f[1], body)
            continue
        if f[0] == "program":
            PROGRAMS[f[1]]()
        i += 1


main()
