# The oracle: the same tool as mini_pip, written with packaging 26.3 (the
# library pip vendors) and Python 3.13's json. Run it from this directory
# after mk.py.
import json, os
from packaging.version import Version, InvalidVersion
from packaging.specifiers import SpecifierSet, InvalidSpecifier
from packaging.markers import Marker, InvalidMarker, UndefinedComparison, UndefinedEnvironmentName
from packaging.requirements import Requirement, InvalidRequirement
from packaging.utils import canonicalize_name


def lines(path):
    return open(path, encoding="utf-8").read().split("\n")[:-1]


def yn(b):
    return "y" if b else "n"


def opt(x):
    return "-" if x is None else str(x)


# ---------------------------------------------------------------- versions

print("== versions")
valid = []
for raw in lines("data/versions.txt"):
    try:
        v = Version(raw)
    except InvalidVersion as e:
        print(f"{raw!r} -> {e}")
        continue
    valid.append(v)
    pre = "-" if v.pre is None else f"{v.pre[0]}{v.pre[1]}"
    flags = []
    if v.is_prerelease:
        flags.append("pre-release")
    if v.is_postrelease:
        flags.append("post-release")
    if v.is_devrelease:
        flags.append("dev-release")
    print(f"{raw!r} -> {v}  [epoch {v.epoch}, release {'.'.join(map(str, v.release))}, pre {pre}, "
          f"post {opt(v.post)}, dev {opt(v.dev)}, local {opt(v.local)}, public {v.public}, base {v.base_version}"
          + ("" if not flags else ", " + ", ".join(flags)) + "]")
print("sorted:")
out = []
prev = None
for v in sorted(valid):
    if prev is not None and v == prev:
        out[-1] += f" = {v}"
    else:
        out.append(str(v))
    prev = v
for o in out:
    print("  " + o)

# ---------------------------------------------------------------- specifiers

print()
print("== specifiers")
for line in lines("data/specifiers.txt"):
    spec, _, items = line.partition("|")
    spec = spec.strip()
    items = items.split()
    try:
        s = SpecifierSet(spec)
    except InvalidSpecifier as e:
        print(f"{spec!r}: {e}")
        continue
    print(f"{spec!r}: {str(s)!r} prereleases={s.prereleases} unsatisfiable={yn(s.is_unsatisfiable())}")
    cells = []
    for it in items:
        cells.append(f"{it}:{yn(s.contains(it))}{yn(s.contains(it, prereleases=True))}{yn(s.contains(it, prereleases=False))}")
    print("  contains " + " ".join(cells))
    print("  filter " + " ".join(s.filter(items)))
    print("  filter pre " + " ".join(s.filter(items, prereleases=True)))
    print("  filter final " + " ".join(s.filter(items, prereleases=False)))

# ---------------------------------------------------------------- environments


def read_envs():
    envs = {}
    order = []
    cur = None
    for line in lines("data/envs.txt"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("["):
            cur = line[1:-1]
            envs[cur] = {}
            order.append(cur)
            continue
        k, _, v = line.partition("=")
        envs[cur][k.strip()] = v.strip()
    return envs, order


envs, env_order = read_envs()

print()
print("== markers")
for raw in lines("data/markers.txt"):
    try:
        m = Marker(raw)
    except InvalidMarker as e:
        print(f"{raw!r}: InvalidMarker")
        for l in str(e).split("\n"):
            print("  | " + l)
        continue
    print(f"{raw!r}: {m}")
    for name in env_order:
        env = dict(envs[name])
        try:
            r = "true" if m.evaluate(env) else "false"
        except UndefinedComparison as e:
            r = f"UndefinedComparison: {e}"
        except UndefinedEnvironmentName as e:
            r = f"UndefinedEnvironmentName: {e}"
        print(f"  {name}: {r}")

# ---------------------------------------------------------------- requirements

print()
print("== requirements")
for raw in lines("data/requirement-tests.txt"):
    try:
        r = Requirement(raw)
    except InvalidRequirement as e:
        print(f"{raw!r}: InvalidRequirement")
        for l in str(e).split("\n"):
            print("  | " + l)
        continue
    print(f"{raw!r}: {r}")
    print(f"  name {r.name} ({canonicalize_name(r.name)}), extras {','.join(sorted(r.extras)) or '-'}, "
          f"specifier {str(r.specifier) or '-'}, url {r.url or '-'}, marker {r.marker if r.marker else '-'}")

# ---------------------------------------------------------------- the index

index = {}
for name, rels in json.load(open("data/index.json"))["projects"].items():
    index[canonicalize_name(name)] = rels


class Failed(Exception):
    pass


def read_reqs(path, reqs, cons, as_constraint):
    """Reads a requirements file the way pip does, for the forms it uses:
    comments, line continuations, -r and -c."""
    phys = lines(path)
    i = 0
    while i < len(phys):
        start = i
        text = phys[i]
        while text.endswith("\\") and i + 1 < len(phys):
            i += 1
            text = text[:-1] + phys[i]
        i += 1
        # a comment starts at a '#' at the start or after white space
        cut = -1
        for k, c in enumerate(text):
            if c == "#" and (k == 0 or text[k - 1] in " \t"):
                cut = k
                break
        if cut >= 0:
            text = text[:cut]
        text = text.strip()
        if not text:
            continue
        where = f"{os.path.basename(path)}:{start + 1}"
        if text.startswith("-r ") or text.startswith("-c "):
            other = os.path.join(os.path.dirname(path), text[3:].strip())
            read_reqs(other, reqs, cons, as_constraint or text.startswith("-c "))
            continue
        try:
            r = Requirement(text)
        except InvalidRequirement as e:
            raise Failed(f"{where}: invalid requirement {text!r}\n" + "\n".join("  | " + l for l in str(e).split("\n")))
        (cons if as_constraint else reqs).append(r)


def resolve(file, env_name):
    env = envs[env_name]
    base_env = dict(env, extra="")
    print(f"== resolve {file} ({env_name})")
    roots = []
    cons = []
    try:
        read_reqs("data/reqs/" + file, roots, cons, False)
    except Failed as e:
        print(f"error: {e}")
        return
    reqs = []
    for r in roots:
        if r.marker is not None and not r.marker.evaluate(base_env):
            print(f"skipped {r} (marker is false)")
            continue
        reqs.append((r, "the user"))
    cons = [c for c in cons if c.marker is None or c.marker.evaluate(base_env)]
    pins = {}
    extras = {}
    state = {"backtracks": 0, "conflict": ""}

    def who(name):
        out = []
        for r, parent in reqs:
            if canonicalize_name(r.name) == name and parent not in out:
                out.append(parent)
        return ", ".join(out)

    def candidates(name):
        specs = SpecifierSet()
        for r, _ in reqs:
            if canonicalize_name(r.name) == name:
                specs &= r.specifier
        for c in cons:
            if canonicalize_name(c.name) == name:
                specs &= c.specifier
        if name not in index:
            state["conflict"] = f"no project named {name} in the index (required by {who(name)})"
            return []
        exact = any(s.operator in ("==", "===") and not s.version.endswith(".*") for s in specs)
        vs = []
        for rel in index[name]:
            py = rel.get("requires_python")
            if py is not None and not SpecifierSet(py).contains(env["python_full_version"]):
                continue
            if rel.get("yanked") and not exact:
                continue
            vs.append(rel["version"])
        ok = sorted(specs.filter(vs), key=Version, reverse=True)
        if not ok:
            state["conflict"] = f"no version of {name} matches {str(specs) or '(any)'} (required by {who(name)})"
        return ok

    def deps(name, version, new_extras, base):
        rel = next(r for r in index[name] if r["version"] == version)
        out = []
        parsed = [Requirement(s) for s in rel["requires_dist"]]
        if base:
            for d in parsed:
                if d.marker is None or d.marker.evaluate(base_env):
                    out.append(d)
        for e in new_extras:
            for d in parsed:
                if d.marker is not None and d.marker.evaluate(dict(env, extra=e)) and not d.marker.evaluate(base_env):
                    out.append(d)
        return out

    def solve(k):
        if k == len(reqs):
            return True
        req, parent = reqs[k]
        name = canonicalize_name(req.name)
        want = sorted(set(canonicalize_name(e) for e in req.extras))
        if name in pins:
            v = pins[name]
            if not req.specifier.contains(v, prereleases=True):
                state["conflict"] = f"{name}=={v} does not match {req.specifier} (required by {parent})"
                return False
            new = [e for e in want if e not in extras[name]]
            mark = len(reqs)
            for e in new:
                extras[name].add(e)
            label = f"{name}=={v}"
            for d in deps(name, v, new, False):
                reqs.append((d, label))
            if solve(k + 1):
                return True
            del reqs[mark:]
            for e in new:
                extras[name].discard(e)
            return False
        for v in candidates(name):
            pins[name] = v
            extras[name] = set(want)
            mark = len(reqs)
            label = f"{name}=={v}"
            for d in deps(name, v, want, True):
                reqs.append((d, label))
            if solve(k + 1):
                return True
            state["backtracks"] += 1
            del reqs[mark:]
            del pins[name]
            del extras[name]
        return False

    if not solve(0):
        print(f"error: {state['conflict']}")
        print(f"backtracks: {state['backtracks']}")
        return
    for name in sorted(pins):
        ex = f"[{','.join(sorted(extras[name]))}]" if extras[name] else ""
        print(f"{name}{ex}=={pins[name]}")
    print(f"backtracks: {state['backtracks']}")
    needs = {name: set() for name in pins}
    for r, parent in reqs:
        if parent != "the user":
            needs[parent.split("==")[0]].add(canonicalize_name(r.name))
    order = []
    left = sorted(pins)
    while left:
        pick = next((n for n in left if all(d in order for d in needs[n] if d != n)), left[0])
        order.append(pick)
        left.remove(pick)
    print("install order: " + " ".join(order))


print()
for line in lines("data/jobs.txt"):
    file, env_name = line.split()
    resolve(file, env_name)
