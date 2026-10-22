# Writes data/: a registry index and two projects, each a package.json
# and the package-lock.json npm wrote for it. The job list,
# data/jobs.txt, is written by hand.
import json, os, shutil

os.makedirs("data/web", exist_ok=True)
os.makedirs("data/cli", exist_ok=True)

def dump(path, obj):
    with open(path, "w") as f:
        f.write(json.dumps(obj, indent=2) + "\n")

registry = {
    "express": {"dist-tags": {"latest": "4.21.2", "next": "5.1.0"},
                "versions": ["4.17.1", "4.18.2", "4.19.2", "4.21.1", "4.21.2", "5.0.0-beta.3", "5.0.0", "5.1.0"]},
    "lodash": {"dist-tags": {"latest": "4.17.21"},
               "versions": ["4.17.15", "4.17.19", "4.17.20", "4.17.21"],
               "deprecated": {"4.17.15": "Prototype pollution: upgrade to 4.17.19 or later"}},
    "react": {"dist-tags": {"latest": "18.3.1", "next": "19.0.0-rc.1", "canary": "19.1.0-canary-3"},
              "versions": ["17.0.2", "18.2.0", "18.3.0", "18.3.1", "19.0.0-rc.0", "19.0.0-rc.1", "19.1.0-canary-3"]},
    "react-dom": {"dist-tags": {"latest": "18.3.1"},
                  "versions": ["17.0.2", "18.2.0", "18.3.1"]},
    "axios": {"dist-tags": {"latest": "1.7.9"},
              "versions": ["0.21.4", "0.27.2", "1.6.8", "1.7.2", "1.7.9", "1.8.0-beta.1"]},
    "left-pad": {"dist-tags": {"latest": "1.3.0"},
                 "versions": ["1.0.0", "1.1.3", "1.2.0", "1.3.0"],
                 "deprecated": {"1.3.0": "use String.prototype.padStart()", "1.2.0": "use String.prototype.padStart()"}},
    "typescript": {"dist-tags": {"latest": "5.7.2", "beta": "5.8.0-beta", "next": "5.8.0-dev.20250101"},
                   "versions": ["4.9.5", "5.4.5", "5.6.3", "5.7.2", "5.8.0-beta", "5.8.0-dev.20250101"]},
    "eslint": {"dist-tags": {"latest": "9.17.0"},
               "versions": ["8.56.0", "8.57.1", "9.0.0", "9.16.0", "9.17.0"]},
    "jest": {"dist-tags": {"latest": "29.7.0"},
             "versions": ["27.5.1", "28.1.3", "29.6.4", "29.7.0", "30.0.0-alpha.6"]},
    "prettier": {"dist-tags": {"latest": "3.4.2"},
                 "versions": ["2.8.8", "3.0.0", "3.3.3", "3.4.2"]},
    "chalk": {"dist-tags": {"latest": "5.4.1"},
              "versions": ["4.1.2", "5.0.0", "5.3.0", "5.4.1"]},
    "commander": {"dist-tags": {"latest": "13.0.0"},
                  "versions": ["9.5.0", "11.1.0", "12.1.0", "13.0.0"]},
    "debug": {"dist-tags": {"latest": "4.4.0"},
              "versions": ["2.6.9", "3.2.7", "4.3.4", "4.3.7", "4.4.0"]},
    "semver": {"dist-tags": {"latest": "7.7.2"},
               "versions": ["5.7.2", "6.3.1", "7.5.4", "7.6.3", "7.7.0", "7.7.1", "7.7.2"]},
    "fsevents": {"dist-tags": {"latest": "2.3.3"},
                 "versions": ["1.2.13", "2.3.2", "2.3.3"]},
    "uuid": {"dist-tags": {"latest": "11.0.3"},
             "versions": ["8.3.2", "9.0.1", "10.0.0", "11.0.3"]},
}
dump("data/registry.json", registry)

def project(name, deps, dev, opt, locked):
    pj = {"name": name, "version": "1.0.0", "private": True}
    if deps:
        pj["dependencies"] = deps
    if dev:
        pj["devDependencies"] = dev
    if opt:
        pj["optionalDependencies"] = opt
    dump(f"data/{name}/package.json", pj)
    packages = {"": {"name": name, "version": "1.0.0"}}
    for k, v in locked.items():
        packages["node_modules/" + k] = {"version": v, "resolved": f"https://registry.npmjs.org/{k}/-/{k}-{v}.tgz"}
    dump(f"data/{name}/package-lock.json", {"name": name, "version": "1.0.0", "lockfileVersion": 3, "requires": True, "packages": packages})

project("web",
        {"express": "^4.18.0", "lodash": "~4.17.15", "react": "^18.2.0", "react-dom": "18.2.0",
         "axios": ">=0.21.0 <1.0.0 || ^1.6", "left-pad": "1.x", "uuid": "next"},
        {"typescript": "~5.6.0", "eslint": "^8.56.0", "jest": "29", "prettier": "latest"},
        None,
        {"express": "4.18.2", "lodash": "4.17.15", "react": "18.3.1", "react-dom": "18.2.0",
         "axios": "0.27.2", "left-pad": "1.3.0", "typescript": "5.6.3", "eslint": "8.57.1", "jest": "29.7.0",
         "prettier": "3.4.2"})

project("cli",
        {"chalk": "^4.1.2", "commander": "9.x || 11.x", "debug": "^4.3.4", "semver": ">=7.5.2",
         "express": "^5.0.0-beta.1", "react": "^19.0.0-rc.0", "is-even": "^1.0.0", "typescript": "github:microsoft/TypeScript"},
        None,
        {"fsevents": "~2.3.2"},
        {"chalk": "4.1.2", "commander": "12.1.0", "debug": "4.4.0", "semver": "7.7.2",
         "express": "5.0.0-beta.3", "react": "19.0.0-rc.0", "fsevents": "2.3.2"})

if os.path.exists("jobs.txt"):
    shutil.copy("jobs.txt", "data/jobs.txt")
