"""Runs data/jobs.txt through the copy of pynmea2 1.19.0 in pynmea2/.

`parse` and `strict` call pynmea2.parse on each line of a file (split on
"\\n", so a CRLF line keeps its "\\r") and print the sentence's repr, its
renderings and the properties its class has. `attrs` reads attributes by
name. `stream` feeds a file to NMEAStreamReader in fixed-size chunks and
`streamfile` hands it the open file; `file`, `fileread`, `filelines` and
`filenext` go through NMEAFile. `edit` sets attributes and `build`,
`buildp` and `query` make sentences from their parts. `report`, `gpx`,
`mux` and `alarms` are small programs a boat's logger might run."""
import math
import os
import sys
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
os.chdir(HERE)

import pynmea2  # noqa: E402
from pynmea2 import nmea_utils  # noqa: E402
from pynmea2.seatalk_utils import SeaTalk  # noqa: E402
import warnings  # noqa: E402

warnings.simplefilter("ignore")


def path(name):
    return os.path.join("data", name)


def raw_text(name):
    with open(path(name), encoding="utf-8", newline="") as f:
        return f.read()


def lines_of(name):
    ls = raw_text(name).split("\n")
    if ls and ls[-1] == "":
        ls.pop()
    return ls


def err(e):
    return "%s: %s" % (type(e).__name__, e)


def prop(name, fn, show=repr):
    try:
        v = fn()
    except Exception as e:
        print("  %s ! %s" % (name, err(e)))
        return
    print("  %s %s" % (name, show(v)))


VALID = (nmea_utils.ValidStatusFix, nmea_utils.ValidGSAFix, nmea_utils.ValidGGAFix,
         nmea_utils.ValidVBWFix)


def show_props(m):
    print("  str %s" % m)
    print("  plain %s" % m.render(checksum=False, dollar=False))
    if isinstance(m, nmea_utils.LatLonFix):
        for n in ("latitude", "longitude", "latitude_minutes", "longitude_minutes",
                  "latitude_seconds", "longitude_seconds"):
            prop(n, lambda n=n: getattr(m, n))
    if isinstance(m, pynmea2.ZDA):
        prop("datestamp", lambda: m.datestamp)
        prop("localdatetime", lambda: m.localdatetime, str)
    if isinstance(m, nmea_utils.DatetimeFix):
        prop("datetime", lambda: m.datetime)
    if isinstance(m, VALID):
        prop("is_valid", lambda: m.is_valid)
    if isinstance(m, (pynmea2.RTE, pynmea2.R00)):
        prop("waypoint_list", lambda: m.waypoint_list)
    if isinstance(m, pynmea2.XDR):
        prop("num_transducers", lambda: m.num_transducers)
        for i in range(m.num_transducers):
            prop("transducer", lambda i=i: m.get_transducer(i))
    if isinstance(m, SeaTalk):
        prop("command_name", lambda: m.command_name)
    if isinstance(m, pynmea2.types.proprietary.ubx.UBX03):
        prop("satellite_list", lambda: m.satellite_list)


def job_parse(name, check):
    for n, line in enumerate(lines_of(name), 1):
        try:
            m = pynmea2.parse(line, check=check)
        except Exception as e:
            print("%d ! %s" % (n, err(e)))
            continue
        print("%d %r" % (n, m))
        if not check:
            show_props(m)


def job_attrs(name, names):
    for n, line in enumerate(lines_of(name), 1):
        try:
            m = pynmea2.parse(line)
        except Exception as e:
            print("%d ! %s" % (n, err(e)))
            continue
        parts = []
        for a in names:
            try:
                parts.append("%s=%r" % (a, getattr(m, a)))
            except Exception as e:
                parts.append("%s!%s" % (a, err(e)))
        print("%d %s" % (n, " ".join(parts)))


def show_item(x):
    if isinstance(x, pynmea2.ParseError):
        print("  error %s" % err(x))
    else:
        print("  %r" % x)


def job_stream(name, mode, size):
    text = raw_text(name)
    try:
        r = pynmea2.NMEAStreamReader(errors=mode)
    except ValueError as e:
        print("! %s" % err(e))
        return
    k = 0
    while k < len(text):
        got = []
        raised = None
        try:
            for x in r.next(text[k:k + size]):
                got.append(x)
        except Exception as e:
            raised = e
        print("chunk %d: %d" % (k // size, len(got)))
        for x in got:
            show_item(x)
        if raised is not None:
            print("  raised %s" % err(raised))
        k += size
    print("buffer %r" % r.buffer)


def job_streamfile(name, mode, calls):
    with open(path(name), encoding="utf-8") as f:
        r = pynmea2.NMEAStreamReader(f, errors=mode)
        for i in range(calls):
            got = []
            raised = None
            try:
                for x in r.next():
                    got.append(x)
            except Exception as e:
                raised = e
            print("call %d: %d" % (i, len(got)))
            for x in got:
                show_item(x)
            if raised is not None:
                print("  raised %s" % err(raised))


def job_file(name):
    try:
        with pynmea2.NMEAFile(path(name)) as f:
            for m in f:
                print("%r" % m)
    except Exception as e:
        print("! %s" % err(e))


def job_fileread(name):
    f = pynmea2.NMEAFile(path(name))
    try:
        ms = f.read()
        print("%d sentences" % len(ms))
        for m in ms:
            print("%s" % m)
    except Exception as e:
        print("! %s" % err(e))
    f.close()


def job_filelines(name, n, method):
    f = pynmea2.NMEAFile(path(name))
    for i in range(n):
        try:
            m = f.readline() if method == "readline" else f.next()
            print("%d %r" % (i, m))
        except Exception as e:
            print("%d ! %s" % (i, err(e)))
    f.close()


def value_of(text):
    if text.startswith("i:"):
        return int(text[2:])
    if text.startswith("f:"):
        return float(text[2:])
    if text.startswith("d:"):
        return Decimal(text[2:])
    return text


def job_edit(name, n, assigns):
    line = lines_of(name)[n - 1]
    try:
        m = pynmea2.parse(line)
    except Exception as e:
        print("! %s" % err(e))
        return
    print("before %r" % m)
    names = []
    for a in assigns:
        k, v = a.split("=", 1)
        val = v.split("|") if k == "waypoint_list" else value_of(v)
        names.append(k)
        try:
            setattr(m, k, val)
            print("set %s %r" % (k, val))
        except Exception as e:
            print("set %s ! %s" % (k, err(e)))
    print("after %r" % m)
    for k in names:
        try:
            print("  %s %r" % (k, getattr(m, k)))
        except Exception as e:
            print("  %s ! %s" % (k, err(e)))
    print("  str %s" % m)


def show_built(m):
    print("%r" % m)
    print("  str %s" % m)


def job_build(kind, args):
    try:
        if kind == "build":
            cls = getattr(pynmea2, args[0])
            m = cls(args[1], args[0], args[2].split(","))
        elif kind == "buildp":
            cls = pynmea2.ProprietarySentence.sentence_types.get(args[0], pynmea2.ProprietarySentence)
            m = cls(args[0], args[1].split(","))
        else:
            m = pynmea2.QuerySentence(args[0], args[1], args[2])
    except Exception as e:
        print("! %s" % err(e))
        return
    show_built(m)


def job_render(name, n):
    m = pynmea2.parse(lines_of(name)[n - 1])
    for cs, dollar, nl in ((True, True, False), (False, True, False), (True, False, False),
                           (False, False, False), (True, True, True), (True, True, "\n"),
                           (False, False, ";")):
        print("%r" % m.render(checksum=cs, dollar=dollar, newline=nl))


def parsed(name):
    out = []
    errors = 0
    for line in lines_of(name):
        try:
            out.append(pynmea2.parse(line))
        except Exception:
            errors += 1
    return out, errors


def haversine_nm(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 3440.065 * math.asin(math.sqrt(h))


def job_report(name):
    ms, errors = parsed(name)
    counts = {}
    for m in ms:
        k = type(m).__name__
        counts[k] = counts.get(k, 0) + 1
    print("sentences %d, errors %d" % (len(ms), errors))
    print("types " + " ".join("%s:%d" % (k, counts[k]) for k in sorted(counts)))
    fixes = []
    for m in ms:
        if isinstance(m, pynmea2.RMC) and m.is_valid:
            try:
                fixes.append((m.datetime, m.latitude, m.longitude, m.spd_over_grnd))
            except Exception as e:
                print("rmc skipped: %s" % err(e))
    if fixes:
        print("first fix %s" % fixes[0][0].isoformat())
        print("last fix %s" % fixes[-1][0].isoformat())
        dist = 0.0
        for a, b in zip(fixes, fixes[1:]):
            dist += haversine_nm(a[1:3], b[1:3])
        sogs = [f[3] for f in fixes]
        print("fixes %d, distance %.3f nm, max sog %.2f kn, mean sog %.2f kn" % (
            len(fixes), dist, max(sogs), sum(sogs) / len(sogs)))
        print("from %.5f,%.5f to %.5f,%.5f" % (fixes[0][1], fixes[0][2], fixes[-1][1], fixes[-1][2]))
    quals = {}
    for m in ms:
        if isinstance(m, pynmea2.GGA):
            quals[m.gps_qual] = quals.get(m.gps_qual, 0) + 1
    if quals:
        print("gga quality " + " ".join("%r:%d" % (k, quals[k]) for k in sorted(quals, key=repr)))
    depths = [m.depth for m in ms if isinstance(m, pynmea2.DPT) and isinstance(m.depth, Decimal)]
    if depths:
        print("depth min %s max %s over %d" % (min(depths), max(depths), len(depths)))
    temps = [m.temperature for m in ms if isinstance(m, pynmea2.MTW)]
    if temps:
        print("water %s..%s C" % (min(temps), max(temps)))
    winds = [m.wind_speed for m in ms if isinstance(m, pynmea2.MWV) and m.reference == "T"]
    if winds:
        print("true wind max %s kn, mean %.1f kn" % (max(winds), sum(float(w) for w in winds) / len(winds)))
    for m in ms:
        if isinstance(m, pynmea2.ZDA):
            try:
                print("zda %s" % m.localdatetime)
            except Exception as e:
                print("zda ! %s" % err(e))
        elif isinstance(m, pynmea2.TXT):
            print("text %s" % m.text)
        elif isinstance(m, pynmea2.XDR):
            for i in range(m.num_transducers):
                t = m.get_transducer(i)
                print("sensor %s %s %s" % (t.id, t.value, t.units))
    route = []
    for m in ms:
        if isinstance(m, pynmea2.RTE):
            if m.sen_num == "1":
                route = [m.active_route_id]
            route += m.waypoint_list
    if route:
        print("route %s: %s" % (route[0], " ".join(route[1:])))
    for m in ms:
        if isinstance(m, pynmea2.WPL):
            print("waypoint %s %.5f %.5f" % (m.waypoint_id, nmea_utils.dm_to_sd(m.lat) * (1 if m.lat_dir == "N" else -1),
                                             nmea_utils.dm_to_sd(m.lon) * (1 if m.lon_dir == "E" else -1)))


def job_gpx(name, out):
    ms, _ = parsed(name)
    wpts = {}
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<gpx version="1.1" creator="mini_nmea">']
    for m in ms:
        if isinstance(m, pynmea2.WPL):
            la = nmea_utils.dm_to_sd(m.lat) * (1 if m.lat_dir == "N" else -1)
            lo = nmea_utils.dm_to_sd(m.lon) * (1 if m.lon_dir == "E" else -1)
            wpts[m.waypoint_id] = (la, lo)
            lines.append('  <wpt lat="%.6f" lon="%.6f"><name>%s</name></wpt>' % (la, lo, m.waypoint_id))
    route = []
    for m in ms:
        if isinstance(m, pynmea2.RTE):
            if m.sen_num == "1":
                route = [m.active_route_id]
            route += m.waypoint_list
    if route:
        lines.append("  <rte><name>%s</name>" % route[0])
        for w in route[1:]:
            if w in wpts:
                lines.append('    <rtept lat="%.6f" lon="%.6f"><name>%s</name></rtept>' % (wpts[w][0], wpts[w][1], w))
            else:
                lines.append("    <!-- %s: no position -->" % w)
        lines.append("  </rte>")
    lines.append("  <trk><name>%s</name><trkseg>" % name)
    alt = {}
    for m in ms:
        if isinstance(m, pynmea2.GGA) and m.gps_qual:
            alt[m.timestamp] = m.altitude
    for m in ms:
        if isinstance(m, pynmea2.RMC) and m.is_valid:
            t = m.datetime.isoformat().replace("+00:00", "Z")
            ele = alt.get(m.timestamp)
            ele_s = "<ele>%r</ele>" % ele if ele is not None else ""
            lines.append('    <trkpt lat="%.6f" lon="%.6f">%s<time>%s</time><course>%r</course><speed>%.3f</speed></trkpt>' % (
                m.latitude, m.longitude, ele_s, t, m.true_course, m.spd_over_grnd * 0.514444))
    lines.append("  </trkseg></trk>")
    lines.append("</gpx>")
    text = "\n".join(lines) + "\n"
    with open(path("out/" + out), "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("wrote %s, %d bytes" % (out, len(text.encode("utf-8"))))
    sys.stdout.write(text)


def job_mux(out, talker, types, names):
    keep = types.split(",")
    rendered = []
    kept = dropped = errors = 0
    for name in names:
        for line in lines_of(name):
            try:
                m = pynmea2.parse(line)
            except pynmea2.ParseError:
                errors += 1
                continue
            if isinstance(m, pynmea2.TalkerSentence) and m.sentence_type in keep:
                m.talker = talker
                rendered.append(m.render(newline=True))
                kept += 1
            else:
                dropped += 1
    text = "".join(rendered)
    with open(path("out/" + out), "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("kept %d, dropped %d, errors %d, %d bytes" % (kept, dropped, errors, len(text.encode("utf-8"))))
    with open(path("out/" + out), encoding="utf-8", newline="") as f:
        back = f.read().split("\r\n")
    for i, line in enumerate(back[:-1]):
        m = pynmea2.parse(line, check=True)
        if i % 9 == 0 or i == len(back) - 2:
            print("%d %s %r" % (i, line, getattr(m, "timestamp", None)))


def job_alarms(names):
    clock = "--:--:--"
    no_fix = False
    for name in names:
        for n, line in enumerate(lines_of(name), 1):
            try:
                m = pynmea2.parse(line)
            except Exception as e:
                print("%s %s:%d unreadable (%s)" % (clock, name, n, type(e).__name__))
                continue
            if isinstance(m, pynmea2.RMC) and isinstance(m.timestamp, type(nmea_utils.timestamp("000000"))):
                clock = m.timestamp.strftime("%H:%M:%S")
            if isinstance(m, pynmea2.GGA):
                if m.gps_qual == 0 and not no_fix:
                    no_fix = True
                    print("%s gps fix lost (%s sats)" % (clock, m.num_sats))
                elif m.gps_qual and no_fix:
                    no_fix = False
                    print("%s gps fix back, quality %r" % (clock, m.gps_qual))
            elif isinstance(m, pynmea2.GSA):
                try:
                    if not m.is_valid:
                        print("%s gsa says no 3d fix (mode %r)" % (clock, m.mode_fix_type))
                except ValueError as e:
                    print("%s gsa mode unreadable: %s" % (clock, e))
            elif isinstance(m, pynmea2.DPT):
                if isinstance(m.depth, Decimal) and m.depth < Decimal("6.0"):
                    print("%s shallow water: %s m under the keel" % (clock, m.depth - m.offset))
            elif isinstance(m, pynmea2.MWV):
                if m.reference == "T" and m.wind_speed is not None and m.wind_speed > 18:
                    print("%s true wind %s kn" % (clock, m.wind_speed))
            elif isinstance(m, pynmea2.XTE):
                d = float(m.cross_track_err_dist)
                if d > 0.04:
                    print("%s off track %.2f nm, steer %s" % (clock, d, m.correction_dir))
            elif isinstance(m, pynmea2.AAM):
                if m.arrival_circ_entered == "A":
                    print("%s arrived at %s" % (clock, m.waypoint_id))
            elif isinstance(m, pynmea2.ALK):
                print("%s seatalk %s: %s" % (clock, m.cmd, m.command_name))
            elif isinstance(m, pynmea2.RPM):
                if not m.is_valid:
                    print("%s rpm sensor %s%r not valid" % (clock, m.source, m.engine_no))
            elif isinstance(m, pynmea2.TTM):
                if m.dist_cpa is not None and m.dist_cpa < Decimal("2"):
                    print("%s target %s %r CPA %s nm in %s min" % (clock, m.name, m.target_number, m.dist_cpa, m.time_cpa))
            elif isinstance(m, pynmea2.types.proprietary.grm.GRME):
                if m.hpe > 10:
                    print("%s garmin hpe %s %s" % (clock, m.hpe, m.hpe_unit))


def main():
    with open(path("jobs.txt")) as f:
        jobs = [l.split() for l in f.read().split("\n") if l.strip()]
    for j in jobs:
        print("== " + " ".join(j))
        k = j[0]
        if k == "parse":
            job_parse(j[1], False)
        elif k == "strict":
            job_parse(j[1], True)
        elif k == "attrs":
            job_attrs(j[1], j[2].split(","))
        elif k == "stream":
            job_stream(j[1], j[2], int(j[3]))
        elif k == "streamfile":
            job_streamfile(j[1], j[2], int(j[3]))
        elif k == "file":
            job_file(j[1])
        elif k == "fileread":
            job_fileread(j[1])
        elif k == "filelines":
            job_filelines(j[1], int(j[2]), "readline")
        elif k == "filenext":
            job_filelines(j[1], int(j[2]), "next")
        elif k == "edit":
            job_edit(j[1], int(j[2]), j[3:])
        elif k in ("build", "buildp", "query"):
            job_build(k, j[1:])
        elif k == "render":
            job_render(j[1], int(j[2]))
        elif k == "report":
            job_report(j[1])
        elif k == "gpx":
            job_gpx(j[1], j[2])
        elif k == "mux":
            job_mux(j[1], j[2], j[3], j[4:])
        elif k == "alarms":
            job_alarms(j[1:])


main()
