#!/usr/bin/env python3
r"""Writes data/jobs.tsv: a sequence of TextFSM jobs, each a (name, template,
input) triple, in a line-delimited block format so the embedded blank lines (a
template's Value/State separator, an input's record-terminating blank line) are
preserved verbatim:

    @JOB <name>
    @TEMPLATE
    <template line>
    ...
    @INPUT
    <input line>
    ...
    @END

No library import — the inputs are literal. `template.splitlines()` and
`input.splitlines()` give the exact line lists both backends consume."""

JOBS = []

JOBS.append(("version", """Value Filldown Hostname (\\S+)
Value Model (\\S+)
Value Version (\\d+\\.\\d+\\S*)

Start
  ^${Hostname}# -> Continue
  ^.*Cisco IOS Software.*Version ${Version} -> Record
  ^cisco ${Model} .*bytes of memory
""", """router1#
Cisco IOS Software, Version 15.2(4)M3, RELEASE
cisco WS-C3750 (PowerPC) processor with 131072K bytes of memory
"""))

JOBS.append(("ifaces", """Value Required Interface (\\S+)
Value Status (up|down)
Value Proto (up|down)

Start
  ^${Interface}\\s+\\S+\\s+\\S+\\s+\\S+\\s+${Status}\\s+${Proto} -> Record
""", """Interface  IP          OK? Method Status Proto
Gi0/0      10.0.0.1    YES NVRAM  up     up
Gi0/1      unassigned  YES unset  down   down
"""))

JOBS.append(("routes", """Value Network (\\d+\\.\\d+\\.\\d+\\.\\d+/\\d+)
Value List NextHop (\\d+\\.\\d+\\.\\d+\\.\\d+)

Start
  ^${Network} -> Continue
  ^${Network}\\s+via\\s+${NextHop} -> Continue
  ^\\s+via\\s+${NextHop}
  ^\\s*$$ -> Record
""", """10.0.0.0/24 via 192.168.1.1
    via 192.168.1.2
    via 192.168.1.3

"""))

JOBS.append(("twostate", """Value User (\\S+)
Value Shell (\\S+)

Start
  ^Users: -> Body

Body
  ^\\s+${User}\\s+${Shell} -> Record
  ^End -> End
""", """Users:
   alice   /bin/bash
   bob     /bin/zsh
End
   ignored line
"""))

JOBS.append(("clearall", """Value A (\\w+)
Value B (\\w+)

Start
  ^a=${A}
  ^b=${B} -> Record
  ^reset -> Clearall
""", """a=1
b=2
reset
a=3
b=4
"""))

JOBS.append(("keyed", """Value Key Port (\\d+)
Value Desc (.+)

Start
  ^${Port}:\\s+${Desc} -> Record
""", """22: ssh
80: http
443: https
"""))

JOBS.append(("errcase", """Value Line (.*)

Start
  ^OK:${Line} -> Record
  ^FATAL -> Error "boom"
""", """OK:first
FATAL here
OK:never
"""))

JOBS.append(("filldown", """Value Filldown Section (\\w+)
Value Item (\\w+)

Start
  ^\\[${Section}\\]
  ^${Item} -> Record
""", """[alpha]
one
two
[beta]
three
"""))

JOBS.append(("eofrec", """# a template with comments
Value Name (\\w+)
Value Age (\\d+)

Start
  # match a person
  ^${Name}\\s+${Age}
""", """Alice 30
"""))

JOBS.append(("fanout", """Value Proto (\\w+)
Value Count (\\d+)

Start
  ^${Proto}:\\s+${Count} -> Record
  ^---
""", """tcp: 5
---
udp: 9
"""))


def main():
    import os
    os.makedirs("data", exist_ok=True)
    out = []
    for (name, tmpl, text) in JOBS:
        out.append("@JOB " + name)
        out.append("@TEMPLATE")
        out.extend(tmpl.splitlines())
        out.append("@INPUT")
        out.extend(text.splitlines())
        out.append("@END")
    with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")


main()
