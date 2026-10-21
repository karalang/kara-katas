# Prints mini_uaparser.kara's generated section: every parser of
# ua_parser's _regexes.py (the copy in ua_parser/) with its pattern, the
# flags re.compile gave it and its replacements, and the files under
# data/ (as mk.py writes them). No function gets more than about 200
# lines.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True

from ua_parser import user_agent_parser as uap  # noqa: E402


def lit(s):
    out = []
    for ch in s:
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


def opt(s):
    if s is None:
        return "None"
    # after a $ every replacement has an ASCII character, so
    # MultiReplace's \$(\d) only meets ASCII digits, and none is $0
    assert all(c.isascii() for c in s.split("$")[1:] for c in c[:1]) and "$0" not in s, s
    return "Some(%s.to_string())" % lit(s)


FUNCS = []


def chunked(name, ret, lines, per=180):
    names = []
    for k in range(0, max(len(lines), 1), per):
        fn = "%s_%d" % (name, k // per)
        names.append(fn)
        body = ["fn %s(v: mut ref Vec[%s]) {" % (fn, ret)]
        body.extend("    " + line for line in lines[k:k + per])
        body.append("}")
        FUNCS.append("\n".join(body))
    return names


def groups(p):
    return p.user_agent_re.groups


ua_lines = []
for p in uap.USER_AGENT_PARSERS:
    # Parse reads group 1 when there is no family replacement
    assert p.family_replacement or groups(p) >= 1, p.pattern
    ua_lines.append("v.push(UaDef { pat: %s.to_string(), flags: %d, family: %s, v1: %s, v2: %s });"
                    % (lit(p.pattern), p.user_agent_re.flags, opt(p.family_replacement),
                       opt(p.v1_replacement), opt(p.v2_replacement)))
os_lines = []
for p in uap.OS_PARSERS:
    os_lines.append("v.push(OsDef { pat: %s.to_string(), flags: %d, os: %s, v1: %s, v2: %s, v3: %s, v4: %s });"
                    % (lit(p.pattern), p.user_agent_re.flags, opt(p.os_replacement),
                       opt(p.os_v1_replacement), opt(p.os_v2_replacement),
                       opt(p.os_v3_replacement), opt(p.os_v4_replacement)))
dev_lines = []
for p in uap.DEVICE_PARSERS:
    assert p.device_replacement or groups(p) >= 1, p.pattern
    dev_lines.append("v.push(DevDef { pat: %s.to_string(), flags: %d, device: %s, brand: %s, model: %s });"
                     % (lit(p.pattern), p.user_agent_re.flags, opt(p.device_replacement),
                        opt(p.brand_replacement), opt(p.model_replacement)))

out = []
out.append("// ------------------------------------------------------------ generated")
out.append("")
out.append("// USER_AGENT_PARSERS, OS_PARSERS and DEVICE_PARSERS, in order.")
for name, ret, lines in (("ua_defs", "UaDef", ua_lines), ("os_defs", "OsDef", os_lines),
                         ("dev_defs", "DevDef", dev_lines)):
    fns = chunked(name + "_part", ret, lines)
    out.append("fn %s() -> Vec[%s] {" % (name, ret))
    out.append("    let mut v: Vec[%s] = Vec.new();" % ret)
    for fn in fns:
        out.append("    %s(mut v);" % fn)
    out.append("    v")
    out.append("}")
    out.append("")

out.append("// The files under data/.")
for fname in ("agents.txt", "access.log", "jobs.tsv"):
    with open(os.path.join(HERE, "data", fname), encoding="utf-8", newline="") as f:
        text = f.read()
    stem = "file_" + "".join(c if c.isalnum() else "_" for c in fname)
    lines = ["v.push(%s.to_string());" % lit(line) for line in text.splitlines(keepends=True)]
    fns = chunked(stem + "_part", "String", lines)
    out.append("fn %s() -> String {" % stem)
    out.append("    let mut v: Vec[String] = Vec.new();")
    for fn in fns:
        out.append("    %s(mut v);" % fn)
    out.append("    let mut t = String.new();")
    out.append("    for line in v.iter() {")
    out.append("        t.push_str(line.as_str());")
    out.append("    }")
    out.append("    t")
    out.append("}")
    out.append("")

print("\n".join(out))
print("\n\n".join(FUNCS))
