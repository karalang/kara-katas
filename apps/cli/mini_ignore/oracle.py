# The oracle: the same report as mini_ignore, made by real git. It copies
# data/repo into a fresh repository, installs data/exclude.txt as
# .git/info/exclude, and asks git. Run it from this directory after mk.py.
import os, shutil, subprocess, tempfile

tmp = tempfile.mkdtemp()
repo = os.path.join(tmp, "repo")
shutil.copytree("data/repo", repo)
subprocess.run(["git", "init", "-q", repo], check=True)
shutil.copy("data/exclude.txt", os.path.join(repo, ".git/info/exclude"))

def git(*args):
    out = subprocess.run(["git", "-c", "core.excludesFile=", "-c", "core.quotePath=false", *args],
                         cwd=repo, capture_output=True, text=True)
    return out.stdout

paths = []
for root, dirs, files in os.walk(repo):
    dirs[:] = [d for d in dirs if not (root == repo and d == ".git")]
    for name in dirs + files:
        paths.append(os.path.relpath(os.path.join(root, name), repo))
paths.sort(key=lambda p: p.encode())

print("== untracked")
print(git("ls-files", "--others", "--exclude-standard"), end="")
print("== ignored")
print(git("ls-files", "--others", "--ignored", "--exclude-standard"), end="")
print("== check-ignore")
print(git("check-ignore", "-v", "--non-matching", "--no-index", "--", *paths), end="")
shutil.rmtree(tmp)
