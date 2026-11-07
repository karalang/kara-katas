# Rewrites the data section at the end of mini_dask.kara, after the
# MARK line: one function per file under data/ (as mk.py writes it, so
# data/out is left out) that returns the file's bytes as hex, and
# write_data, which decodes and writes them, so the program carries its own
# inputs.
#
# Run from this directory: python3 -I -B gen_kara.py

import os

MARK = "\n// ============================================================ data\n"
WIDTH = 96


def read(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return fh.read()


src = read("mini_dask.kara")
src = src[:src.index(MARK)]

names = []
for root, dirs, files in os.walk("data"):
    dirs[:] = [d for d in dirs if not (root == "data" and d == "out")]
    for n in files:
        names.append(os.path.relpath(os.path.join(root, n), "data").replace(os.sep, "/"))
names.sort()

d = ["", "// The files under data/, in name order.", "fn write_data() -> Result[(), String] {"]
for k, n in enumerate(names):
    d.append(f'    put_bytes("data/{n}", file_{k}())?;')
d += ["    Ok(())", "}"]
for k, n in enumerate(names):
    with open(os.path.join("data", n), "rb") as fh:
        h = fh.read().hex()
    lines = [h[i:i + WIDTH] for i in range(0, len(h), WIDTH)] or [""]
    d += ["", f"// data/{n}", f"fn file_{k}() -> String {{", '    """']
    d += lines
    d += ['"""', "}"]
with open("mini_dask.kara", "w", encoding="utf-8", newline="") as fh:
    fh.write(src + MARK + "\n".join(d) + "\n")
