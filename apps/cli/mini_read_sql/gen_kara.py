# Rewrites the data section at the end of mini_read_sql.kara, after the
# MARK line: one function per file under data/ (as mk.py writes it) that
# returns the file's bytes as hex, and write_data, which writes them back,
# so the program carries its own inputs. No function gets more than about
# 200 lines.
#
# Run from this directory: python3 -I -B gen_kara.py

import os

MARK = "\n// ============================================================ data\n"
WIDTH = 96


def read(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return fh.read()


src = read("mini_read_sql.kara")
src = src[:src.index(MARK)]

names = sorted(os.listdir("data"))

d = ["", "// The files under data/, in name order.", "fn write_data() -> Result[(), String] {"]
for k, n in enumerate(names):
    d.append(f'    put_bytes("data/{n}", unhex(file_{k}()))?;')
d += ["    Ok(())", "}"]
for k, n in enumerate(names):
    with open(os.path.join("data", n), "rb") as fh:
        h = fh.read().hex()
    lines = [h[i:i + WIDTH] for i in range(0, len(h), WIDTH)] or [""]
    d += ["", f"// data/{n}", f"fn file_{k}() -> String {{", '    """']
    d += lines
    d += ['"""', "}"]
with open("mini_read_sql.kara", "w", encoding="utf-8", newline="") as fh:
    fh.write(src + MARK + "\n".join(d) + "\n")
