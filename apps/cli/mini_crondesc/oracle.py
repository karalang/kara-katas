# Runs data/jobs.jsonl through the real cron_descriptor 2.2.1 (vendored next
# to this file) and prints what mini_crondesc.kara must print.
import contextlib
import io
import json
import locale
import os
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import cron_descriptor  # noqa: E402
from cron_descriptor import CasingTypeEnum, DescriptionTypeEnum, ExpressionDescriptor, Options  # noqa: E402
from cron_descriptor.ExpressionValidator import ExpressionValidator  # noqa: E402
import cron_descriptor.__main__ as cli  # noqa: E402

SYSTEM = ["en_US"]
locale.getlocale = lambda *a: (SYSTEM[0], "UTF-8" if SYSTEM[0] else None)

out = sys.stdout


def emit(s):
    out.write(s + "\n")


def exc_line(e):
    t = type(e)
    name = t.__qualname__ if t.__module__ == "builtins" else f"{t.__module__}.{t.__qualname__}"
    msg = str(e)
    return f"{name}: {msg}" if msg else name


def opts_text(o):
    return json.dumps(o, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def make_options(o):
    SYSTEM[0] = o.get("system", "en_US")
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        if o.get("auto"):
            opts = Options()
        else:
            kw = {"locale_code": o.get("locale", "en_US")}
            if "casing" in o:
                kw["casing_type"] = CasingTypeEnum[o["casing"]]
            if "verbose" in o:
                kw["verbose"] = o["verbose"]
            if "dow0" in o:
                kw["day_of_week_start_index_zero"] = o["dow0"]
            if "h24" in o:
                kw["use_24hour_time_format"] = o["h24"]
            if "location" in o:
                kw["locale_location"] = o["location"]
            opts = Options(**kw)
    for x in w:
        emit(f"  warning: {x.message}")
    return opts


def job_desc(expr, o):
    emit(f"desc {json.dumps(expr, ensure_ascii=False)} {opts_text(o)}")
    try:
        opts = make_options(o)
        kwargs = dict(o.get("kwargs", {}))
        if "casing_type" in kwargs:
            kwargs["casing_type"] = CasingTypeEnum[kwargs["casing_type"]]
        d = ExpressionDescriptor(expr, opts, **kwargs)
        part = DescriptionTypeEnum[o.get("part", "FULL")]
        emit("  = " + d.get_description(part))
    except Exception as e:
        emit("  ! " + exc_line(e))


def job_validate(expr):
    try:
        ExpressionValidator().validate(expr)
        emit(f"valid {json.dumps(expr)}: ok")
    except Exception as e:
        emit(f"valid {json.dumps(expr)}: {exc_line(e)}")


def job_cli(argv, sysloc):
    emit(f"$ cron_descriptor {json.dumps(argv)} LANG={sysloc}")
    SYSTEM[0] = sysloc
    so, se = io.StringIO(), io.StringIO()
    code = 0
    old = sys.argv
    sys.argv = ["cron_descriptor"] + argv
    try:
        with contextlib.redirect_stdout(so), contextlib.redirect_stderr(se), warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                cli.main()
            except SystemExit as e:
                code = e.code if isinstance(e.code, int) else 1
            except Exception as e:
                se.write("Traceback (most recent call last):\n" + exc_line(e) + "\n")
                code = 1
    finally:
        sys.argv = old
    for line in so.getvalue().splitlines():
        emit(line)
    for line in se.getvalue().splitlines():
        emit("stderr: " + line)
    emit(f"exit {code}")


MACROS = {
    "@yearly": "0 0 1 1 *", "@annually": "0 0 1 1 *", "@monthly": "0 0 1 * *",
    "@weekly": "0 0 * * 0", "@daily": "0 0 * * *", "@midnight": "0 0 * * *", "@hourly": "0 * * * *",
}


def describe(expr, opts):
    try:
        return ExpressionDescriptor(expr, opts).get_description()
    except Exception as e:
        return "error: " + exc_line(e)


def job_crontab(path, loc):
    emit(f"crontab {path} {loc}")
    try:
        with open(os.path.join(HERE, path), encoding="utf-8") as f:
            lines = f.read().split("\n")
    except OSError as e:
        emit(f"  cannot read {path}: {e.strerror}")
        return
    opts = Options(locale_code=loc)
    n = 0
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if path.endswith(".crontab"):
            first = line.split()[0]
            if first.startswith("@"):
                cmd = line[len(first):].strip()
                if first == "@reboot":
                    emit(f"  {cmd} :: at startup")
                elif first in MACROS:
                    emit(f"  {cmd} :: {describe(MACROS[first], opts)} ({first})")
                else:
                    emit(f"  {cmd} :: unknown macro {first}")
                n += 1
                continue
            if "=" in first:
                emit(f"  env {first}")
                continue
            fields = line.split()
            emit(f"  {' '.join(fields[5:])} :: {describe(' '.join(fields[:5]), opts)}")
        elif path.endswith(".txt"):
            name, _, sched = line.partition("\t")
            emit(f"  {name} :: {describe(sched, opts)}")
        else:
            key, _, val = line.partition("=")
            emit(f"  {key.strip()} :: {describe(val.strip(), opts)}")
        n += 1
    emit(f"  {n} schedules")


def main():
    os.chdir(HERE)
    with open(os.path.join(HERE, "data", "jobs.jsonl"), encoding="utf-8") as f:
        for line in f:
            j = json.loads(line)
            if j[0] == "desc":
                job_desc(j[1], j[2])
            elif j[0] == "validate":
                job_validate(j[1])
            elif j[0] == "cli":
                job_cli(j[1], j[2])
            elif j[0] == "crontab":
                job_crontab(j[1], j[2])


if __name__ == "__main__":
    main()
