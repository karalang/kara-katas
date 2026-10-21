# Runs data/jobs.jsonl and the three programs through dictdiffer 0.9.0
# itself (the copy in dictdiffer/, unchanged) and prints what
# mini_dictdiffer.kara must print.
import json
import math
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(write_through=True)
os.chdir(HERE)

import dictdiffer  # noqa: E402
from dictdiffer import diff, dot_lookup, patch, revert, swap  # noqa: E402
from dictdiffer.merge import Merger  # noqa: E402
from dictdiffer.resolve import NoFurtherResolutionException, UnresolvedConflictsException  # noqa: E402
from dictdiffer.utils import WildcardDict  # noqa: E402

assert dictdiffer.__file__.startswith(HERE), dictdiffer.__file__


def fmt(v):
    """repr(), except that a set's items are sorted so the output is stable."""
    if isinstance(v, bool) or v is None or isinstance(v, int):
        return repr(v)
    if isinstance(v, float):
        return repr(v)
    if isinstance(v, str):
        return repr(v)
    if isinstance(v, list):
        return "[" + ", ".join(fmt(x) for x in v) + "]"
    if isinstance(v, tuple):
        if len(v) == 1:
            return "(" + fmt(v[0]) + ",)"
        return "(" + ", ".join(fmt(x) for x in v) + ")"
    if isinstance(v, dict):
        return "{" + ", ".join(f"{fmt(k)}: {fmt(x)}" for k, x in v.items()) + "}"
    if isinstance(v, set):
        if not v:
            return "set()"
        return "{" + ", ".join(sorted(fmt(x) for x in v)) + "}"
    raise TypeError(type(v))


def err(e):
    return f"{type(e).__name__}: {e}".replace("\n", "\\n")


def hook(o):
    if list(o) == ["$set"]:
        return set(o["$set"])
    return o


def spec(s):
    return json.loads(json.dumps(s), object_hook=hook)


def diff_opts(o):
    kw = {}
    shown = []
    for k in ("ignore", "path_limit", "expand", "tolerance", "absolute_tolerance", "dot_notation", "node"):
        if k in o:
            v = spec(o[k])
            kw[k] = v
            shown.append(f"{k}={fmt(v)}")
    return kw, shown


def policy(what):
    def act(conflict, first_patches, second_patches, info):
        if what == "decline":
            return False
        if what == "stop":
            raise NoFurtherResolutionException()
        conflict.take = what
        return True
    return act


def run_merge(env, s):
    o = s[4]
    actions = WildcardDict() if o["wildcard"] else {}
    for path, what in o["actions"]:
        actions[tuple(path)] = policy(what)
    mg = Merger(env[s[1]], env[s[2]], env[s[3]], actions, [tuple(p) for p in o["path_limits"]])
    try:
        mg.run()
    except UnresolvedConflictsException as e:
        print(f"  unresolved: {len(e.content)}")
        for c in e.content:
            print(f"    {fmt(c.first_patch)} vs {fmt(c.second_patch)}")
        if o["picks"] is None:
            print("  merge stops")
            return
        print(f"  picks: {' '.join(o['picks'])}")
        mg.continue_run(o["picks"])
    print(f"  first patches: {fmt(mg.first_patches)}")
    print(f"  second patches: {fmt(mg.second_patches)}")
    for c in mg.conflicts:
        print(f"  conflict: {fmt(c.first_patch)} vs {fmt(c.second_patch)}, took {c.take}")
    print(f"  unified: {fmt(mg.unified_patches)}")
    print(f"  merged: {fmt(patch(mg.unified_patches, env[s[1]]))}")


def step(s, env):
    op = s[0]
    if op == "val":
        env[s[1]] = spec(s[2])
        print(f"  {s[1]} = {fmt(env[s[1]])}")
    elif op == "diff":
        kw, shown = diff_opts(s[4])
        env[s[1]] = list(diff(env[s[2]], env[s[3]], **kw))
        print(f"  {s[1]} = diff({', '.join([s[2], s[3]] + shown)}):")
        for p in env[s[1]]:
            print(f"    {fmt(p)}")
    elif op == "patch":
        env[s[1]] = patch(env[s[2]], env[s[3]])
        print(f"  {s[1]} = patch({s[2]}, {s[3]}) = {fmt(env[s[1]])}")
    elif op == "swap":
        env[s[1]] = list(swap(env[s[2]]))
        print(f"  {s[1]} = swap({s[2]}) = {fmt(env[s[1]])}")
    elif op == "revert":
        env[s[1]] = revert(env[s[2]], env[s[3]])
        print(f"  {s[1]} = revert({s[2]}, {s[3]}) = {fmt(env[s[1]])}")
    elif op == "eq":
        print(f"  {s[1]} == {s[2]}: {env[s[1]] == env[s[2]]}")
    elif op == "show":
        print(f"  {s[1]} = {fmt(env[s[1]])}")
    elif op == "lookup":
        r = dot_lookup(env[s[1]], env[s[2]], parent=s[3])
        print(f"  dot_lookup({s[1]}, {s[2]}{', parent=True' if s[3] else ''}) = {fmt(r)}")
    elif op == "merge":
        run_merge(env, s)
    else:
        raise SystemExit(f"unknown step {op}")


def run_jobs():
    shutil.rmtree("data/out", ignore_errors=True)
    os.makedirs("data/out", exist_ok=True)
    with open("data/jobs.jsonl") as f:
        for line in f:
            j = json.loads(line)
            print(f"== {j['name']}")
            env = {}
            for s in j["steps"]:
                try:
                    step(s, env)
                except Exception as e:
                    print(f"  {s[0]}: error {err(e)}")
                    break


# --- the programs ------------------------------------------------------

def load(p):
    with open(p) as f:
        return json.load(f)


def save(p, obj):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(json.dumps(obj, indent=2) + "\n")


def where(node, key=None):
    if isinstance(node, str):
        parts = node.split(".") if node else []
    else:
        parts = list(node)
    if key is not None:
        parts.append(key)
    return "/" + "/".join(str(p) for p in parts)


def describe(p):
    action, node, changes = p
    if action == "change":
        return [f"change {where(node)}: {fmt(changes[0])} -> {fmt(changes[1])}"]
    return [f"{action} {where(node, k)}: {fmt(v)}" for k, v in changes]


VOLATILE = {"metadata.updated_at", "metadata.deployed_by"}


def drift():
    print("== program: drift")
    names = sorted({n[:-5] for n in os.listdir("data/desired") + os.listdir("data/deployed")})
    for name in names:
        want = f"data/desired/{name}.json"
        have = f"data/deployed/{name}.json"
        if not os.path.exists(have):
            print(f"{name}: not deployed")
            continue
        if not os.path.exists(want):
            print(f"{name}: not in the desired state, would be deleted")
            continue
        desired, deployed = load(want), load(have)
        changes = list(diff(deployed, desired, ignore=VOLATILE, absolute_tolerance=0.001))
        if not changes:
            print(f"{name}: in sync")
            continue
        lines = [x for p in changes for x in describe(p)]
        print(f"{name}: {len(lines)} differences")
        for x in lines:
            print(f"  {x}")
        fixed = patch(changes, deployed)
        save(f"data/out/drift/{name}.json", fixed)
        left = list(diff(fixed, desired, ignore=VOLATILE, absolute_tolerance=0.001))
        print(f"  after the patch: {len(left)} differences; reverting gives the deployed file back: "
              f"{revert(changes, fixed) == deployed}")
    for name in sorted(os.listdir("data/out/drift")):
        with open(f"data/out/drift/{name}") as f:
            text = f.read()
        print(f"-- data/out/drift/{name} ({len(text)} bytes)")
        print(text, end="")


def ask(conflict, first_patches, second_patches, info):
    raise NoFurtherResolutionException()


def take(who):
    def act(conflict, first_patches, second_patches, info):
        conflict.take = who
        return True
    return act


def settings_merge():
    print("== program: settings merge")
    base, ours, theirs = load("data/merge/base.json"), load("data/merge/ours.json"), load("data/merge/theirs.json")
    actions = WildcardDict()
    with open("data/merge/policy.txt") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            path, who = line.split()
            actions[tuple(path.split("."))] = ask if who == "ask" else take(who)
    with open("data/merge/picks.txt") as f:
        picks = f.read().split()
    mg = Merger(base, ours, theirs, actions)
    try:
        mg.run()
        print("no conflicts left for picks.txt")
    except UnresolvedConflictsException as e:
        print(f"{len(e.content)} conflicts need a pick:")
        for c, pick in zip(e.content, picks):
            print(f"  ours {fmt(c.first_patch)}")
            print(f"  theirs {fmt(c.second_patch)}")
            print(f"  picked {'ours' if pick == 'f' else 'theirs'}")
        mg.continue_run(picks)
    for c in mg.conflicts:
        print(f"conflict at {where(get_node(c))}: took {'ours' if c.take == 'f' else 'theirs'}")
    print(f"{len(mg.unified_patches)} patches applied:")
    for p in mg.unified_patches:
        for x in describe(p):
            print(f"  {x}")
    merged = patch(mg.unified_patches, base)
    save("data/out/merged.json", merged)
    with open("data/out/merged.json") as f:
        print(f.read(), end="")


def get_node(c):
    from dictdiffer.utils import get_path
    a, b = get_path(c.first_patch), get_path(c.second_patch)
    return list(a if len(a) <= len(b) else b)


def history():
    print("== program: schema history")
    names = sorted(os.listdir("data/history"), key=lambda n: int(n[1:-5]))
    versions = [load(f"data/history/{n}") for n in names]
    os.makedirs("data/out", exist_ok=True)
    with open("data/out/changes.jsonl", "w") as f:
        for i in range(1, len(versions)):
            ps = list(diff(versions[i - 1], versions[i]))
            f.write(json.dumps({"from": names[i - 1][:-5], "to": names[i][:-5], "patches": ps}) + "\n")
    with open("data/out/changes.jsonl") as f:
        log = [json.loads(line) for line in f]
    for entry in log:
        print(json.dumps(entry))
    state = versions[0]
    for i, entry in enumerate(log):
        state = patch(entry["patches"], state)
        print(f"{entry['from']} -> {entry['to']}: {len(entry['patches'])} patches, matches {entry['to']}: "
              f"{state == versions[i + 1]}")
    for i in reversed(range(len(log))):
        entry = log[i]
        state = revert(entry["patches"], state)
        print(f"undo {entry['to']} -> {entry['from']}: matches {entry['from']}: {state == versions[i]}")
    print(f"back at v1: {json.dumps(state, sort_keys=True)}")


run_jobs()
drift()
settings_merge()
history()
