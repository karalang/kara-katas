# Prints the Kara font_text() and jobs_text() functions, appended to
# mini_pyfiglet.kara. font_text() carries figfont.tsv (the standard FIGlet
# font dumped from the vendored pyfiglet: one line per code, the code then a
# tab then the six glyph rows separated by \x1f); jobs_text() carries
# data/jobs.tsv. Both are parsed at run time so the embedding stays a flat
# string literal rather than a large constructor.
def lit(s):
    out = []
    for ch in s:
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\t":
            out.append("\\t")
        elif ord(ch) < 0x20:
            out.append("\\x%02x" % ord(ch))
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


def emit(fnname, path):
    print("fn %s() -> String {" % fnname)
    print("    let mut s = String.new();")
    for line in open(path, encoding="utf-8").read().splitlines():
        print("    s.push_str(%s);" % lit(line + "\n"))
    print("    s")
    print("}")


print("// figfont.tsv (standard FIGlet font dumped from pyfiglet): per line a")
print("// code, a tab, then the six glyph rows separated by \\x1f.")
emit("font_text", "figfont.tsv")
print("")
print("// data/jobs.tsv, as mk.py writes it.")
emit("jobs_text", "data/jobs.tsv")
