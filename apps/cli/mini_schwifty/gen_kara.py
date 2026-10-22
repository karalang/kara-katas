# Prints the Kara registry_text() and jobs_text() functions, appended to
# mini_schwifty.kara. registry_text() carries iban_registry.tsv (the effective
# ISO 13616 IBAN registry dumped from the vendored schwifty); jobs_text()
# carries data/jobs.tsv. Both are parsed at run time so the embedding stays a
# flat string literal rather than a large constructor.
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


print("// iban_registry.tsv (effective ISO 13616 registry dumped from schwifty).")
emit("registry_text", "iban_registry.tsv")
print("")
print("// data/jobs.tsv, as mk.py writes it.")
emit("jobs_text", "data/jobs.tsv")
