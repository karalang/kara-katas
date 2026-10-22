# Prints the Kara jobs_text() function, appended to mini_cobs.kara. It carries
# data/jobs.tsv verbatim (one `<op>\t<hex>` line per job), parsed at run time.
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


print("")
print("// data/jobs.tsv, as mk.py writes it.")
emit("jobs_text", "data/jobs.tsv")
