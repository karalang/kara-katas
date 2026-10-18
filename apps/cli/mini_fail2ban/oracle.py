# The oracle for mini_fail2ban: the same jails, filters and logs run in
# Python, with `re` for the patterns. expected.out is its output.
import os, re, shutil
import mk

HOST = r"(?P<host>(?:\d{1,3}\.){3}\d{1,3}|[0-9a-fA-F]*:[0-9a-fA-F:]+)"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
SYSLOG_DATE = re.compile(r"^([A-Z][a-z]{2}) +(\d{1,2}) (\d{2}):(\d{2}):(\d{2}) ")
NGINX_DATE = re.compile(r"^(\d{4})/(\d{2})/(\d{2}) (\d{2}):(\d{2}):(\d{2}) ")
YEAR = 2026


def days_from_civil(y, m, d):
    y -= m <= 2
    era = (y if y >= 0 else y - 399) // 400
    yoe = y - era * 400
    doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + d - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    return era * 146097 + doe - 719468


def civil_from_days(z):
    z += 719468
    era = (z if z >= 0 else z - 146096) // 146097
    doe = z - era * 146097
    yoe = (doe - doe // 1460 + doe // 36524 - doe // 146096) // 365
    y = yoe + era * 400
    doy = doe - (365 * yoe + yoe // 4 - yoe // 100)
    mp = (5 * doy + 2) // 153
    d = doy - (153 * mp + 2) // 5 + 1
    m = mp + (3 if mp < 10 else -9)
    return (y + (m <= 2), m, d)


def stamp(t):
    y, m, d = civil_from_days(t // 86400)
    s = t % 86400
    return "%04d-%02d-%02d %02d:%02d:%02d" % (y, m, d, s // 3600, s // 60 % 60, s % 60)


def epoch(y, mo, d, h, mi, s):
    return days_from_civil(y, mo, d) * 86400 + h * 3600 + mi * 60 + s


def detect_date(line):
    """The time of a line and the rest of it, or None."""
    m = SYSLOG_DATE.search(line)
    if m:
        mo = MONTHS.index(m.group(1)) + 1 if m.group(1) in MONTHS else 0
        if mo:
            t = epoch(YEAR, mo, int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)))
            return t, line[m.end():]
    m = NGINX_DATE.search(line)
    if m:
        g = [int(x) for x in m.groups()]
        return epoch(*g), line[m.end():]
    return None


# ------------------------------------------------------------ config files

def read_conf(text):
    """Sections of key -> value, in order. Indented lines continue a value."""
    sections = {}
    order = []
    cur = None
    key = None
    for raw in text.split("\n"):
        stripped = raw.strip()
        if stripped == "" or stripped[0] in "#;":
            key = None
            continue
        if raw[0] in " \t" and key is not None and cur is not None:
            sections[cur][key] += "\n" + stripped
            continue
        if stripped.startswith("[") and stripped.endswith("]"):
            cur = stripped[1:-1].strip()
            if cur not in sections:
                sections[cur] = {}
                order.append(cur)
            key = None
            continue
        i = stripped.find("=")
        if i < 0 or cur is None:
            key = None
            continue
        key = stripped[:i].strip().lower()
        sections[cur][key] = stripped[i + 1:].strip()
    return sections, order


INTERP = re.compile(r"%\((\w+)\)s")


def interpolate(value, defs, depth=0):
    if depth > 10:
        raise ValueError("interpolation too deep")
    out = ""
    pos = 0
    for m in INTERP.finditer(value):
        out += value[pos:m.start()]
        name = m.group(1)
        if name in defs:
            out += interpolate(defs[name], defs, depth + 1)
        else:
            out += m.group(0)
        pos = m.end()
    return out + value[pos:]


def load_filter(name):
    path = "data/filter.d/%s.conf" % name
    if not os.path.exists(path):
        return None
    secs, _ = read_conf(open(path).read())
    defs = {}
    before = secs.get("INCLUDES", {}).get("before", "")
    if before:
        inc, _ = read_conf(open("data/filter.d/" + before).read())
        defs.update(inc.get("DEFAULT", {}))
    defs.update(secs.get("Definition", {}))
    fail = [interpolate(l, defs).replace("<HOST>", HOST) for l in defs.get("failregex", "").split("\n") if l]
    ign = [interpolate(l, defs) for l in defs.get("ignoreregex", "").split("\n") if l]
    return fail, ign


# ------------------------------------------------------------ addresses

def parse_v4(s):
    parts = s.split(".")
    if len(parts) != 4:
        return None
    n = 0
    for p in parts:
        if not p.isdigit() or int(p) > 255:
            return None
        n = n * 256 + int(p)
    return n


def ignored(ip, ignores):
    for item in ignores:
        if "/" in item:
            net, bits = item.split("/")
            a, b = parse_v4(ip), parse_v4(net)
            if a is None or b is None:
                continue
            bits = int(bits)
            mask = ((1 << 32) - 1) ^ ((1 << (32 - bits)) - 1)
            if a & mask == b & mask:
                return True
        elif item == ip:
            return True
    return False


# ------------------------------------------------------------ jails

def log(t, who, jail, msg):
    print("%s %-17s[%s] %s" % (stamp(t), who, jail, msg))


def run_jail(name, cfg, fail, ign):
    maxretry = int(cfg["maxretry"])
    findtime = int(cfg["findtime"])
    bantime = int(cfg["bantime"])
    increment = cfg.get("bantime.increment", "false") == "true"
    maxtime = int(cfg.get("bantime.maxtime", "0"))
    ignores = cfg.get("ignoreip", "").split()
    inc = " (increment, max %ds)" % maxtime if increment else ""
    print("Jail '%s': %d failregex, %d ignoreregex, maxretry %d, findtime %ds, bantime %ds%s"
          % (name, len(fail), len(ign), maxretry, findtime, bantime, inc))
    for r in fail:
        print("  failregex: " + r)
    for r in ign:
        print("  ignoreregex: " + r)
    fres = [re.compile(r) for r in fail]
    ires = [re.compile(r) for r in ign]
    text = open(cfg["logpath"]).read()
    failures = {}
    fail_order = []
    bans = []  # [ip, end]
    bancount = {}
    total_failed = total_banned = lines = nodate = ign_count = 0
    for line in text.split("\n"):
        if line == "":
            continue
        lines += 1
        d = detect_date(line)
        if d is None:
            nodate += 1
            continue
        t, rest = d
        due = sorted([b for b in bans if b[1] <= t], key=lambda b: (b[1], b[0]))
        for b in due:
            log(b[1], "fail2ban.actions", name, "Unban " + b[0])
            bans.remove(b)
        host = None
        for r in fres:
            m = r.search(rest)
            if m:
                host = m.group("host")
                break
        if host is None:
            continue
        if any(r.search(rest) for r in ires):
            ign_count += 1
            continue
        if ignored(host, ignores):
            log(t, "fail2ban.filter", name, "Ignore %s by ip" % host)
            continue
        log(t, "fail2ban.filter", name, "Found " + host)
        total_failed += 1
        if any(b[0] == host for b in bans):
            log(t, "fail2ban.actions", name, "%s already banned" % host)
            continue
        if host not in failures:
            failures[host] = []
            fail_order.append(host)
        failures[host] = [x for x in failures[host] if x > t - findtime] + [t]
        if len(failures[host]) >= maxretry:
            n = bancount.get(host, 0) + 1
            bancount[host] = n
            dur = bantime
            if increment:
                dur = min(bantime * (1 << min(n - 1, 20)), maxtime)
            bans.append([host, t + dur])
            failures[host] = []
            total_banned += 1
            log(t, "fail2ban.actions", name, "Ban %s for %ds (ban %d)" % (host, dur, n))
    failed_now = [h for h in fail_order if failures[h]]
    print("Status for the jail: " + name)
    print("|- Filter")
    print("|  |- Currently failed:\t%d" % len(failed_now))
    print("|  |- Total failed:\t%d" % total_failed)
    print("|  `- File list:\t" + cfg["logpath"])
    print("`- Actions")
    print("   |- Currently banned:\t%d" % len(bans))
    print("   |- Total banned:\t%d" % total_banned)
    print("   `- Banned IP list:\t" + " ".join(b[0] for b in bans))
    print("Lines: %d read, %d without a date, %d ignored by ignoreregex" % (lines, nodate, ign_count))
    return bans


def main():
    shutil.rmtree("data", ignore_errors=True)
    mk.write_all()
    secs, order = read_conf(open("data/jail.local").read())
    defaults = secs.get("DEFAULT", {})
    active = []
    for name in order:
        if name == "DEFAULT":
            continue
        cfg = dict(defaults)
        cfg.update(secs[name])
        if cfg.get("enabled", "false") != "true":
            print("Jail '%s' is disabled" % name)
            continue
        f = load_filter(cfg["filter"])
        if f is None:
            print("ERROR Found no accessible config files for 'filter.d/%s' under data/filter.d" % cfg["filter"])
            continue
        if not os.path.exists(cfg["logpath"]):
            print("ERROR Failed during configuration: Have not found any log file for %s jail" % name)
            continue
        bans = run_jail(name, cfg, f[0], f[1])
        active.append((name, bans))
        print()
    os.makedirs("data/action")
    for name, bans in active:
        out = ""
        for ip, _ in bans:
            tool = "ip6tables" if ":" in ip else "iptables"
            out += "%s -I f2b-%s 1 -s %s -j REJECT --reject-with icmp-port-unreachable\n" % (tool, name, ip)
        path = "data/action/%s.sh" % name
        with open(path, "w") as f:
            f.write(out)
    for name, bans in active:
        path = "data/action/%s.sh" % name
        text = open(path).read()
        print("%s: %d rule(s), %d bytes" % (path, text.count("\n"), len(text.encode())))
        for l in text.split("\n"):
            if l:
                print("  " + l)
    print("Shutdown")
    for name, bans in active:
        for ip, _ in bans:
            print("fail2ban.actions [%s] Unban %s (stop)" % (name, ip))


main()
