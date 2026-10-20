# Runs data/jobs.tsv through dockerfile-parse 2.0.1 (the dockerfile_parse/
# package next to this file, unchanged) and prints what it did.
# mini_dockerfile.kara must print the same bytes.
#
# Each job copies its Dockerfile to data/work/Dockerfile and opens a
# DockerfileParser there. A read-only job prints `structure`, `json`, the
# properties, or `context_structure`. Any other job changes the file
# through the parser's setters or `add_lines`, `add_lines_at` and
# `_delete_instructions`, and prints the file afterwards. A CR in a file
# prints as <CR>.
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
sys.path.insert(0, HERE)

from dockerfile_parse import DockerfileParser  # noqa: E402

OUT = []


def emit(s):
    OUT.append(s + "\n")


def raw(text):
    text = text.replace("\r", "<CR>")
    OUT.append(text)
    if text and not text.endswith("\n"):
        OUT.append("\n\\ no newline at end\n")


def err(e):
    return "error: %s: %s" % (type(e).__name__, e)


def pairs(words):
    d = {}
    for w in words:
        k, v = w.split("=", 1)
        d[k] = v
    return d


def options(words):
    build_args, parent_env, env_replace = {}, {}, True
    i = 0
    while i < len(words):
        if words[i] == "--build-arg":
            build_args.update(pairs([words[i + 1]]))
            i += 2
        elif words[i] == "--parent-env":
            parent_env.update(pairs([words[i + 1]]))
            i += 2
        else:
            env_replace = False
            i += 1
    return build_args, parent_env, env_replace


def open_work(name, words=()):
    work = os.path.join(DATA, "work")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    shutil.copyfile(os.path.join(DATA, name), os.path.join(work, "Dockerfile"))
    build_args, parent_env, env_replace = options(list(words))
    return DockerfileParser(path=work, env_replace=env_replace,
                            parent_env=parent_env, build_args=build_args)


def read_only(op, args):
    p = open_work(args[0], args[1:])
    try:
        if op == "structure":
            for insn in p.structure:
                emit(repr(insn))
        elif op == "json":
            emit(p.json)
        elif op == "info":
            for prop in ["parent_images", "is_multistage", "baseimage", "cmd", "labels", "envs", "args"]:
                try:
                    v = getattr(p, prop)
                    emit("%s: %r" % (prop, dict(v) if isinstance(v, dict) else v))
                except Exception as e:
                    emit("%s: %s" % (prop, err(e)))
        else:
            for c in p.context_structure:
                emit("args=%r envs=%r labels=%r" % (c.args, c.envs, c.labels))
                emit("  line_args=%r line_envs=%r line_labels=%r" % (c.line_args, c.line_envs, c.line_labels))
    except Exception as e:
        emit(err(e))


def split_lines(words):
    k = words.index("--")
    return words[:k], words[k + 1:]


def change(op, args):
    p = open_work(args[0])
    rest = args[1:]
    try:
        if op == "baseimage":
            p.baseimage = rest[0]
        elif op == "parents":
            p.parent_images = rest
        elif op == "cmd":
            p.cmd = rest[0]
        elif op == "labels":
            p.labels = pairs(rest)
        elif op == "envs":
            p.envs = pairs(rest)
        elif op == "args":
            p.args = pairs(rest)
        elif op == "label":
            p.labels[rest[0]] = rest[1]
        elif op == "unlabel":
            del p.labels[rest[0]]
        elif op == "add":
            opts, lines = split_lines(rest)
            p.add_lines(*lines, **{o: True for o in opts})
        elif op == "add-at":
            opts, lines = split_lines(rest)
            kind, where = opts[0], opts[1]
            if kind == "line":
                anchor = int(where)
            elif kind == "insn":
                anchor = p.structure[int(where)]
            else:
                anchor = where + "\n"
            p.add_lines_at(anchor, *lines, **{o: True for o in opts[2:]})
        elif op == "delete":
            p._delete_instructions(*rest)
    except Exception as e:
        emit(err(e))
    raw(p.content)


def main():
    with open(os.path.join(DATA, "jobs.tsv"), encoding="utf-8") as f:
        jobs = [line.rstrip("\n").split("\t") for line in f]
    for job in jobs:
        emit("== " + " ".join(job))
        op, args = job[0], job[1:]
        if op in ("structure", "json", "info", "context"):
            read_only(op, args)
        else:
            change(op, args)
    shutil.rmtree(os.path.join(DATA, "work"), ignore_errors=True)
    sys.stdout.write("".join(OUT))


main()
