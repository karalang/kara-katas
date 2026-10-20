# Writes data/ for mini_click: the files the deployctl commands read
# (a config file whose sections become each command's default_map, a
# manifest, release notes and a services directory) and runs.txt, the
# command lines the oracle feeds through click's CliRunner.
import os
import shutil

FILES = {}

FILES["deployctl.ini"] = """[deployctl]
env = staging
verbose = 1

[deployctl.release]
replicas = 4
strategy = canary
tag = blue green

[deployctl.logs]
lines = 25
"""

FILES["manifests/api.yml"] = """service: api
image: registry.local/api
port: 8080
replicas: 3
health: /healthz
"""

FILES["manifests/worker.yml"] = """service: worker
image: registry.local/worker
queue: jobs
"""

FILES["notes/1.4.2.txt"] = """Fix the retry loop in the client.
Raise the default timeout to 30 seconds.
"""

FILES["services/api/VERSION"] = "1.4.1\n"
FILES["services/worker/VERSION"] = "0.9.0\n"
FILES["services/README"] = "One directory per service.\n"

# kind of each line: tool, then env (K=V;K=V or -), then input lines
# joined with | (or -), then the arguments, each separated by a tab.
RUNS = []


def run(tool, *args, env="-", inp="-"):
    RUNS.append("\t".join([tool, env, inp, *args]))


# --- deployctl: help and usage
run("deployctl")
run("deployctl", "--help")
run("deployctl", "-h")
run("deployctl", "--version")
run("deployctl", "release", "--help")
run("deployctl", "logs", "--help")
run("deployctl", "config", "--help")
run("deployctl", "config", "set", "--help")
run("deployctl", "scale", "--help")
run("deployctl", "user", "--help")
run("deployctl", "sync", "--help")
run("deployctl", "promote", "--help")
run("deployctl", "rollback", "--help")
run("deployctl", "status", "--help")

# --- deployctl release
run("deployctl", "release", "api", "1.4.2")
run("deployctl", "-v", "-v", "--env", "prod", "release", "api", "1.4.2", "--replicas", "6")
run("deployctl", "-vvv", "release", "api", "1.4.2", "-r3", "--tag", "a", "--tag", "b", "-t", "c")
run("deployctl", "release", "api", "1.4.2", "--replicas=21")
run("deployctl", "release", "api", "1.4.2", "--replicas", "0")
run("deployctl", "release", "api", "1.4.2", "--replicas", "three")
run("deployctl", "release", "api", "1.4.2", "--replicas", " 7 ")
run("deployctl", "release", "api", "1.4.2", "--replicas", "1_0")
run("deployctl", "release", "api", "1.4.2", "--timeout", "2.5")
run("deployctl", "release", "api", "1.4.2", "--timeout", "0")
run("deployctl", "release", "api", "1.4.2", "--timeout", "600.5")
run("deployctl", "release", "api", "1.4.2", "--timeout", "1e2")
run("deployctl", "release", "api", "1.4.2", "--timeout", "abc")
run("deployctl", "release", "api", "1.4.2", "--strategy", "BLUE-GREEN")
run("deployctl", "release", "api", "1.4.2", "--strategy", "yolo")
run("deployctl", "release", "api", "1.4.2", "--strategy")
run("deployctl", "release", "api", "1.4.2", "--at", "2026-03-01")
run("deployctl", "release", "api", "1.4.2", "--at", "2026-03-01T09:30:00")
run("deployctl", "release", "api", "1.4.2", "--at", "2026-03-01 9:05:07")
run("deployctl", "release", "api", "1.4.2", "--at", "2026-02-30")
run("deployctl", "release", "api", "1.4.2", "--at", "tomorrow")
run("deployctl", "release", "api", "1.4.2", "--id", "{12345678-1234-5678-1234-567812345678}")
run("deployctl", "release", "api", "1.4.2", "--id", "urn:uuid:ABCDEF00-1234-5678-9ABC-DEF012345678")
run("deployctl", "release", "api", "1.4.2", "--id", "1234")
run("deployctl", "release", "api", "1.4.2", "--notes", "data/notes/1.4.2.txt")
run("deployctl", "release", "api", "1.4.2", "--notes", "data/notes/9.9.9.txt")
run("deployctl", "release", "api", "1.4.2", "--manifest", "data/manifests/api.yml")
run("deployctl", "release", "api", "1.4.2", "--manifest", "data/manifests")
run("deployctl", "release", "api", "1.4.2", "--manifest", "data/manifests/db.yml")
run("deployctl", "release", "api", "1.4.2", "--dry-run")
run("deployctl", "release", "api", "1.4.2", "--no-dry-run")
run("deployctl", "release", "api")
run("deployctl", "release")
run("deployctl", "release", "api", "1.4.2", "extra")
run("deployctl", "release", "api", "1.4.2", "more", "extras")
run("deployctl", "release", "api", "1.4.2", "--replica", "2")
run("deployctl", "release", "api", "1.4.2", "--stratgy", "canary")
run("deployctl", "release", "api", "1.4.2", "--zzz")
run("deployctl", "release", "api", "1.4.2", "-x")
run("deployctl", "release", "api", "1.4.2", "--dry-run=yes")
run("deployctl", "release", "--", "-api", "1.4.2")
run("deployctl", "release", "api", "--replicas", "2", "1.4.2")
run("deployctl", "release", "api", "1.4.2", "--replicas")
run("deployctl", "relase", "api")
run("deployctl", "rel", "api")
run("deployctl", "--env", "qa", "release", "api", "1.4.2")
run("deployctl", "--env", "PROD", "release", "api", "1.4.2")
run("deployctl", "--bogus", "release")
run("deployctl", "release", "api", "1.4.2", env="DEPLOYCTL_ENV=prod")
run("deployctl", "release", "api", "1.4.2", env="DEPLOYCTL_RELEASE_REPLICAS=9;DEPLOYCTL_RELEASE_TAG=x y  z")
run("deployctl", "--env", "dev", "release", "api", "1.4.2", env="DEPLOYCTL_ENV=prod")
run("deployctl", "release", "api", "1.4.2", env="DEPLOYCTL_RELEASE_DRY_RUN=no")
run("deployctl", "release", "api", "1.4.2", env="DEPLOYCTL_RELEASE_DRY_RUN=maybe")

# --- config file defaults
run("deployctl", "--config", "data/deployctl.ini", "release", "api", "1.4.2")
run("deployctl", "--config", "data/deployctl.ini", "release", "api", "1.4.2", "-r", "2", "--strategy", "rolling")
run("deployctl", "--config", "data/deployctl.ini", "logs", "api")
run("deployctl", "--config", "data/missing.ini", "logs", "api")
run("deployctl", "--config", "data/deployctl.ini", "--env", "prod", "status")

# --- logs
run("deployctl", "logs", "api")
run("deployctl", "logs", "api", "worker", "-n", "5", "--follow")
run("deployctl", "logs", "-n5", "-f", "api")
run("deployctl", "logs", "-fn", "5", "api")
run("deployctl", "logs", "--level", "warn", "--level", "error", "api")
run("deployctl", "logs", "--level", "fatal", "api")
run("deployctl", "logs", "--since", "2026-03-01", "api")
run("deployctl", "logs")
run("deployctl", "logs", "-n", "-1", "api")
run("deployctl", "logs", "--grep", "timeout", "--grep=retry", "api")

# --- rollback (confirmation)
run("deployctl", "rollback", "api", "--yes")
run("deployctl", "rollback", "api", inp="y")
run("deployctl", "rollback", "api", inp="n")
run("deployctl", "rollback", "api", inp="maybe|yes")
run("deployctl", "rollback", "api", inp="")
run("deployctl", "rollback", "api")
run("deployctl", "rollback", "api", "--to", "1.3.9", "--yes")

# --- scale (tuple, multiple)
run("deployctl", "scale", "api", "--set", "cpu", "2", "--set", "memory", "512")
run("deployctl", "scale", "api", "--set", "cpu")
run("deployctl", "scale", "api", "--set", "cpu", "lots")
run("deployctl", "scale", "api", "--window", "10", "20")
run("deployctl", "scale", "api", "--window", "10")
run("deployctl", "scale", "api", "--min", "-5")
run("deployctl", "scale", "api", "--min", "50", "--max", "500")
run("deployctl", "scale", "api", "--ratio", "1.5")
run("deployctl", "scale", "api", "--ratio", "0")
run("deployctl", "scale", "api", "--ratio", "1")

# --- config subgroup
run("deployctl", "config")
run("deployctl", "config", "get", "region")
run("deployctl", "config", "set", "region", "eu-west-1")
run("deployctl", "config", "set", "region")
run("deployctl", "config", "unset", "region", "zone", "rack")
run("deployctl", "config", "unset")
run("deployctl", "config", "lst")
run("deployctl", "config", "--json", "get", "region")

# --- user (prompts)
run("deployctl", "user", "create", "ada", inp="s3cret|s3cret")
run("deployctl", "user", "create", "ada", inp="s3cret|other|s3cret|s3cret")
run("deployctl", "user", "create", "ada", "--role", "admin", inp="pw|pw")
run("deployctl", "user", "create", inp="ada|pw|pw")
run("deployctl", "user", "create", inp="|ada|pw|pw")
run("deployctl", "user", "create", "ada", "--role", "root", inp="pw|pw")
run("deployctl", "user", "create", "ada", inp="")
run("deployctl", "user", "invite", inp="grace@example.org|5")
run("deployctl", "user", "invite", inp="grace@example.org|abc|50|3")
run("deployctl", "user", "invite", "--email", "x@example.org", "--days", "2")
run("deployctl", "user", "invite", "--email", inp="y@example.org|")

# --- sync (paths, nargs=-1)
run("deployctl", "sync", "data/services/api", "data/services/worker")
run("deployctl", "sync", "data/services/README")
run("deployctl", "sync", "data/services/db")
run("deployctl", "sync")
run("deployctl", "sync", "--dest", "data/services", "data/services/api")
run("deployctl", "sync", "--dest", "data/services/README", "data/services/api")

# --- hidden, deprecated
run("deployctl", "debug-dump")
run("deployctl", "promote", "api")
run("deployctl", "status", "--format", "json")
run("deployctl", "status", "--wide")
run("deployctl", "status", "--legacy-color")

# --- pipeline (chain)
run("pipeline", "--help")
run("pipeline", "build", "test", "publish")
run("pipeline", "build", "--target", "arm64", "test", "--shard", "2", "publish", "--channel", "beta")
run("pipeline", "--jobs", "4", "build", "build", "--target", "x86")
run("pipeline", "test", "--shard", "9", "build")
run("pipeline", "build", "deploy")
run("pipeline", "build", "test", "--help")
run("pipeline")
run("pipeline", "--jobs", "2")
run("pipeline", "publish", "--channel", "nightly")

# --- greet (one command)
run("greet", "--help")
run("greet", "Ada")
run("greet", "Ada", "Grace", "--shout")
run("greet", "--Shout", "ADA")
run("greet", "--GREETING", "Hi", "Ada")
run("greet", "--upper", "Ada")
run("greet", "--lower", "--upper", "Ada")
run("greet", "--plain", "Ada")
run("greet", "--times", "3", "Ada")
run("greet", "--times", "11", "Ada")
run("greet", "--times", "-3", "Ada")
run("greet", "--pos", "1.5", "-2", "Ada")
run("greet", "--pos", "1.5", "Ada")
run("greet", "--lang", "fr", "Ada")
run("greet", "Ada", env="GREET_LANG=de")
run("greet", "Ada", env="GREET_TIMES=2;GREET_SHOUT=1")
run("greet", "Ada", env="GREET_SHOUT=perhaps")
run("greet", "--version")
run("greet")
run("greet", "--", "--Ada")
run("greet", "--sep", "", "Ada", "Grace")

# --- wrap (formatting)
run("wrap", "--help")
run("wrap", "--size", "M")
run("wrap", "--old-name", "x")
run("wrap", "--size")

os.makedirs("data", exist_ok=True)
for name, body in FILES.items():
    path = os.path.join("data", name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(body)
with open("data/runs.txt", "w") as f:
    for line in RUNS:
        f.write(line + "\n")
