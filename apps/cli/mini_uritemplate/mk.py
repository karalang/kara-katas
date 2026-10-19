# Writes data/: jobs.tsv, the operations, and the inputs of the API
# client report, api.json and requests.tsv.
import json
import os
import random

random.seed(127)
os.makedirs("data", exist_ok=True)


def js(v):
    return json.dumps(v, ensure_ascii=False)


def pairs(*kv):
    return {"__pairs__": [list(p) for p in kv]}


jobs = []

# The RFC 6570 test suite, with each case's accepted expansions.
for name in ["spec-examples", "spec-examples-by-section", "extended-tests", "negative-tests"]:
    with open(os.path.join("suite", name + ".json"), encoding="utf-8") as f:
        suite = json.load(f)
    for group, body in suite.items():
        jobs.append("== %s: %s" % (name, group))
        jobs.append("vars\t" + js(body.get("variables", {})))
        for template, expected in body["testcases"]:
            jobs.append("case\t%s\t%s" % (template, js(expected)))

# What the suite does not reach: numbers, booleans, None, defaults,
# prefixes on numbers, negative prefixes, lists of pairs, the reserved
# operators, unmatched braces and non-ASCII text.
edge_vars = {
    "n": 42, "zero": 0, "neg": -7, "f": 2.5, "big": 1e22, "tiny": 0.0001,
    "whole": 3.0, "t": True, "no": False, "nothing": None, "empty": "",
    "word": "drücken", "emoji": "a😀b", "pct": "50%", "path": "/a b/c",
    "list": ["x", "y z", None, 3], "nums": [1, 2.5, True],
    "dict": {"b": "2", "a": "1", "c": None}, "pairs": pairs(("z", 1), ("a", "x y")),
    "empty_list": [], "empty_dict": {}, "q": "a&b=c", "long": "abcdefghij",
}
templates = [
    "{n}", "{zero}", "{neg}", "{f}", "{big}", "{tiny}", "{whole}", "{t}", "{no}",
    "{nothing}", "{empty}", "{?empty}", "{;empty}", "{/empty}", "{.empty}", "{&empty}",
    "{word}", "{+word}", "{emoji}", "{emoji:2}", "{pct}", "{+pct}", "{#pct}",
    "{path}", "{+path}", "{/path}", "{list}", "{list*}", "{/list}", "{/list*}",
    "{?list}", "{?list*}", "{;list}", "{;list*}", "{.list}", "{#list*}", "{nums}",
    "{dict}", "{dict*}", "{/dict}", "{/dict*}", "{?dict}", "{?dict*}", "{;dict}",
    "{;dict*}", "{.dict*}", "{pairs}", "{pairs*}", "{?pairs*}", "{;pairs}", "{/pairs*}",
    "{empty_list}", "{?empty_list}", "{/empty_list}", "{;empty_list}", "{empty_dict}",
    "{?empty_dict*}", "{;empty_dict}", "{.empty_dict}",
    "{long:3}", "{long:0}", "{long:-3}", "{long: 4}", "{long:+2}", "{long:1_0}",
    "{long:30}", "{?long:5}", "{;long:2}", "{/long:2,word:3}", "{long:3*}", "{long*:3}",
    "{n:2}", "{?f:1}", "{t:1}", "{zero:1}", "{list:2}", "{dict:1}",
    "{missing=fallback}", "{missing=a b}", "{zero=dflt}", "{no=dflt}", "{empty=dflt}",
    "{empty_list=dflt}", "{n=dflt}", "{?missing=1,n}", "{/missing=x,y=}",
    "{|list}", "{!n,word}", "{@dict*}", "{|nothing}", "{&q}", "{?q}", "{+q}",
    "{a{b}", "x}y{n}", "{n}{n}{?n}", "{,}", "{,n}", "{missing:x}", "{n:}",
    "{n:3.5}", "{=n}", "{??n}", "/{n}/{word}{?list*,dict*}{#q}",
]
jobs.append("== edge cases")
jobs.append("vars\t" + js(edge_vars))
for t in templates:
    jobs.append("expand\t" + t)
for t in ["{a,b:3,c*}{?d=x,e}{+f}", "{/list*,n}{.x:2}", "{,}{=n}", "{a:1}{b:x}",
          "no templates", "{m*:2}{n:2*}", "{?a}{?a}{&b,a}"]:
    jobs.append("parse\t" + t)
    jobs.append("variables\t" + t)
for t in ["{n}{missing}{/list*}", "{?n,missing}", "{?missing,n}", "{+path}{#missing}",
          "https://x.test{/word,missing}", "{nothing}{empty}{?empty}"]:
    jobs.append("partial\t" + t)

# The API client: a hypermedia root of link templates, and calls made
# through clients that bind some variables up front with partial().
api = {
    "service": "forge.example.org",
    "links": {
        "user": "https://api.forge.example.org/users/{user}",
        "repo": "https://api.forge.example.org/repos/{owner}/{repo}",
        "issues": "https://api.forge.example.org/repos/{owner}/{repo}/issues{/number}{?state,labels,page,per_page}",
        "contents": "https://api.forge.example.org/repos/{owner}/{repo}/contents/{+path}{?ref}",
        "compare": "https://api.forge.example.org/repos/{owner}/{repo}/compare/{base}...{head}",
        "archive": "https://api.forge.example.org/repos/{owner}/{repo}/{archive_format}{/ref}",
        "search": "https://api.forge.example.org/search/code{?q}{&sort,order,page}",
        "tiles": "https://tiles.forge.example.org/{z}/{x}/{y}.png{?style}",
        "matrix": "https://api.forge.example.org/builds{;os,arch*}{?env*}",
        "docs": "https://docs.forge.example.org{/section*}{#anchor}",
        "events": "https://events.forge.example.org/{org}{.format}{?since,types}",
    },
}
with open("data/api.json", "w", encoding="utf-8") as f:
    json.dump(api, f, ensure_ascii=False, indent=1)
    f.write("\n")

owners = [("acme", "rocket"), ("dev-tools", "lint"), ("ünïcode", "naïve repo"), ("ops", "infra")]
paths = ["README.md", "src/main.rs", "docs/a b/guide.md", "data/50%.csv", "x/y?z#w"]
reqs = []
for k in range(44):
    owner, repo = random.choice(owners)
    link = random.choice(sorted(api["links"]))
    ctx = {"owner": owner, "repo": repo}
    call = {}
    if link == "user":
        ctx = {}
        call = {"user": random.choice(["octo", "hubot", "jane.doe", "ünï"])}
    elif link == "issues":
        if random.random() < 0.4:
            call["number"] = random.randint(1, 900)
        else:
            if random.random() < 0.6:
                call["state"] = random.choice(["open", "closed", "all"])
            if random.random() < 0.5:
                call["labels"] = random.sample(["bug", "good first issue", "p1", "ux"], random.randint(0, 3))
            call["page"] = random.randint(1, 5)
            if random.random() < 0.5:
                ctx["per_page"] = random.choice([30, 100])
    elif link == "contents":
        call["path"] = random.choice(paths)
        if random.random() < 0.5:
            call["ref"] = random.choice(["main", "v1.2.0", "feature/x"])
    elif link == "compare":
        call = {"base": random.choice(["main", "v1.0"]), "head": random.choice(["dev", "fix/#12", "user:branch"])}
    elif link == "archive":
        ctx["archive_format"] = random.choice(["tarball", "zipball"])
        if random.random() < 0.7:
            call["ref"] = random.choice(["main", "v2.0.1"])
    elif link == "search":
        ctx = {"sort": "indexed"}
        call = {"q": random.choice(["fn main", "TODO in:file", "size:>1000", "a+b=c"])}
        if random.random() < 0.5:
            call["page"] = random.randint(2, 4)
        if random.random() < 0.4:
            call["order"] = random.choice(["asc", "desc"])
    elif link == "tiles":
        ctx = {"z": random.randint(1, 18)}
        call = {"x": random.randint(0, 5000), "y": random.randint(0, 5000)}
        if random.random() < 0.3:
            call["style"] = random.choice(["dark", "satellite"])
    elif link == "matrix":
        ctx = {"os": random.choice(["linux", "macos"])}
        call = {"arch": random.sample(["x86_64", "arm64", "riscv64"], random.randint(1, 3))}
        if random.random() < 0.6:
            call["env"] = pairs(*random.sample([("CI", "true"), ("RUST_LOG", "debug"), ("OPT", "-O2 -g")], 2))
    elif link == "docs":
        ctx = {}
        call = {"section": random.choice([["api"], ["guide", "install"], ["ref", "templates", "rfc 6570"]])}
        if random.random() < 0.5:
            call["anchor"] = random.choice(["usage", "level-4", "§3.2"])
    elif link == "events":
        ctx = {"org": random.choice(["acme", "ops"]), "format": random.choice(["json", "ndjson", ""])}
        if random.random() < 0.5:
            call["since"] = random.choice(["2024-01-01T00:00:00Z", "1700000000"])
        if random.random() < 0.5:
            call["types"] = random.sample(["push", "pr", "release"], 2)
    client = random.choice(["web", "cli", "bot"])
    reqs.append("%s\t%s\t%s\t%s" % (client, link, js(ctx), js(call)))
with open("data/requests.tsv", "w", encoding="utf-8") as f:
    f.write("# client\tlink\tbound by the client\tper call\n")
    f.write("\n".join(reqs) + "\n")

jobs.append("== api client")
jobs.append("api\tapi.json\trequests.tsv")

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(jobs) + "\n")
