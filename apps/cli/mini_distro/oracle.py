# Runs data/jobs.tsv through distro itself; the output is expected.out.
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import distro  # noqa: E402
from distro import LinuxDistribution  # noqa: E402

ROOTS = "data/roots/"


def field(s):
    if s == "-":
        return None
    return s.replace("∅", "").replace("⏎", "\n").replace("⇥", "\t").replace("␣", " ")


def failure(e):
    return "raised %s: %s" % (type(e).__name__, e)


def show(label, f):
    try:
        v = repr(f())
    except Exception as e:  # noqa: BLE001
        print("   %-22s %s" % (label, failure(e)))
        return
    print("   %-22s %s" % (label, v))


def report(d):
    # The repr comes first, on a fresh instance: it names the distro
    # release file before it has looked for one.
    show("repr", lambda: d)
    show("id", d.id)
    show("name", d.name)
    show("name pretty", lambda: d.name(pretty=True))
    show("version", d.version)
    show("version pretty", lambda: d.version(pretty=True))
    show("version best", lambda: d.version(best=True))
    show("version pretty best", lambda: d.version(pretty=True, best=True))
    show("version_parts", d.version_parts)
    show("version_parts best", lambda: d.version_parts(best=True))
    show("major minor build", lambda: (d.major_version(), d.minor_version(), d.build_number()))
    show("like", d.like)
    show("codename", d.codename)
    show("linux_distribution", d.linux_distribution)
    show("linux_distribution id", lambda: d.linux_distribution(False))
    show("info", d.info)
    show("info pretty best", lambda: d.info(True, True))
    show("os_release_file", lambda: d.os_release_file)
    show("distro_release_file", lambda: d.distro_release_file)
    show("os_release_info", d.os_release_info)
    show("lsb_release_info", d.lsb_release_info)
    show("distro_release_info", d.distro_release_info)
    show("uname_info", d.uname_info)
    show("oslevel_info", d.oslevel_info)
    show("os_release_attr id", lambda: d.os_release_attr("id"))
    show("distro_release_attr", lambda: d.distro_release_attr("name"))


def flag(s):
    return None if s == "-" else s == "T"


def cli(args):
    log = logging.getLogger("distro")
    sys.argv = ["distro"] + args
    try:
        distro.main()
    except SystemExit as e:
        print("   [exit status %s]" % e.code)
    for h in list(log.handlers):
        log.removeHandler(h)


def main():
    with open("data/jobs.tsv", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    for line in lines:
        if line.startswith("#"):
            print(line)
            continue
        print("-- " + line.replace("\t", " | "))
        w = line.split("\t")
        op = w[0]
        if op == "root":
            report(LinuxDistribution(root_dir=ROOTS + w[1]))
        elif op == "files":
            report(LinuxDistribution(root_dir=ROOTS + w[1], os_release_file=field(w[2]) or "",
                                     distro_release_file=field(w[3]) or ""))
        elif op == "inject":
            d = LinuxDistribution(root_dir=ROOTS + w[1])
            # What lsb_release -a, uname -rs and oslevel would have printed.
            if field(w[2]) is not None:
                d.__dict__["_lsb_release_info"] = LinuxDistribution._parse_lsb_release_content(
                    field(w[2]).splitlines())
            if field(w[3]) is not None:
                d.__dict__["_uname_info"] = LinuxDistribution._parse_uname_content(field(w[3]).splitlines())
            if field(w[4]) is not None:
                d.__dict__["_oslevel_info"] = field(w[4]).strip()
            report(d)
        elif op == "ctor":
            try:
                d = LinuxDistribution(include_lsb=flag(w[2]), include_uname=flag(w[3]),
                                      include_oslevel=flag(w[4]), root_dir=w[1])
            except Exception as e:  # noqa: BLE001
                print("   " + failure(e))
                continue
            print("   include_lsb=%r include_uname=%r include_oslevel=%r root_dir=%r etc_dir=%r usr_lib_dir=%r"
                  % (d.include_lsb, d.include_uname, d.include_oslevel, d.root_dir, d.etc_dir, d.usr_lib_dir))
        elif op == "release":
            show("parsed", lambda: LinuxDistribution._parse_distro_release_content(field(w[1])))
        elif op == "osrel":
            show("parsed", lambda: LinuxDistribution._parse_os_release_content(field(w[1])))
        elif op == "lsb":
            show("parsed", lambda: LinuxDistribution._parse_lsb_release_content(field(w[1]).splitlines()))
        elif op == "uname":
            show("parsed", lambda: LinuxDistribution._parse_uname_content(field(w[1]).splitlines()))
        elif op == "cli":
            cli(w[1:])


main()
