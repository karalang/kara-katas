#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored packaging.requirements and prints
expected.out. mini_requirements.kara must reproduce this byte-for-byte.

`req` prints the parsed parts; `eval` evaluates the marker against a fixed
Linux / CPython 3.11.5 environment (with the given extra). Both print INVALID
on a requirement the grammar rejects.
"""
import sys

sys.path.insert(0, "vendor")
from packaging.requirements import Requirement, InvalidRequirement  # noqa: E402

# A fixed environment so the result is reproducible on any host. Every marker
# key the jobs use is pinned here; evaluate() overrides the host defaults with
# these.
BASE_ENV = {
    "os_name": "posix",
    "sys_platform": "linux",
    "platform_machine": "x86_64",
    "platform_release": "6.1.0",
    "platform_system": "Linux",
    "platform_version": "#1 SMP",
    "platform_python_implementation": "CPython",
    "python_version": "3.11",
    "python_full_version": "3.11.5",
    "implementation_name": "cpython",
    "implementation_version": "3.11.5",
}


def do_req(s):
    try:
        r = Requirement(s)
    except InvalidRequirement:
        return "INVALID"
    extras = ",".join(sorted(r.extras)) or "-"
    spec = str(r.specifier) or "-"
    url = r.url or "-"
    return "name=" + r.name + " | extras=" + extras + " | spec=" + spec + " | url=" + url


def do_eval(s, extra):
    try:
        r = Requirement(s)
    except InvalidRequirement:
        return "INVALID"
    if r.marker is None:
        return "(no marker)"
    env = dict(BASE_ENV)
    env["extra"] = "" if extra == "-" else extra
    return "True" if r.marker.evaluate(environment=env) else "False"


def run(fields):
    if fields[0] == "req":
        return do_req(fields[1])
    if fields[0] == "eval":
        return do_eval(fields[1], fields[2])
    return "unknown op"


def main():
    chunks = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().splitlines():
        if not line:
            continue
        fields = line.split("\t")
        header = "== " + fields[0] + " | " + " ".join(fields[1:])
        chunks.append(header + "\n  " + run(fields) + "\n")
    sys.stdout.write("".join(chunks))


if __name__ == "__main__":
    main()
