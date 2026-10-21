# Runs data/jobs.jsonl and the five photo programs through piexif 1.1.3
# itself (the copy in piexif/, unchanged) and prints what
# mini_piexif.kara must print.
import datetime as dt
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(write_through=True)
os.chdir(HERE)

import piexif  # noqa: E402
from piexif import ExifIFD, GPSIFD, ImageIFD  # noqa: E402
from piexif.helper import UserComment  # noqa: E402

assert piexif.__file__.startswith(HERE), piexif.__file__

IFDS = ("0th", "Exif", "GPS", "Interop", "1st")


def err(e):
    return f"{type(e).__name__}: {e}".replace("\n", "\\n")


def hexdump(b):
    for i in range(0, len(b), 32):
        print(f"    {i:04x}: {b[i:i + 32].hex()}")


def show(name, v):
    if isinstance(v, dict):
        print(f"  {name} = {{")
        for ifd, sub in v.items():
            if ifd == "thumbnail":
                print(f"    thumbnail: {sub!r}")
            elif not sub:
                print(f"    {ifd}: {{}}")
            else:
                print(f"    {ifd}:")
                for k, x in sub.items():
                    print(f"      {k!r}: {x!r}")
        print("  }")
    else:
        print(f"  {name} = {v!r}")


def path(p):
    return os.path.join("data", p)


def read(p):
    with open(path(p), "rb") as f:
        return f.read()


def val(s, env):
    if isinstance(s, list):
        return tuple(val(x, env) for x in s)
    if isinstance(s, dict):
        if "b" in s:
            b = s["b"].encode("latin-1")
            if "then" in s:
                b += s["then"].encode("latin-1") * s["times"]
            return b
        if "f" in s:
            return float(s["f"])
        if "file" in s:
            return read(s["file"])
        if "v" in s:
            return env[s["v"]]
    return s


def exif_dict(spec, env):
    d = {}
    for k, sub in spec.items():
        if k == "thumbnail":
            d[k] = val(sub, env)
        else:
            d[k] = {int(t): val(x, env) for t, x in sub.items()}
    return d


def arg(a, env):
    return env[a] if isinstance(a, str) and a in env else val(a, env)


def step(s, env):
    op = s[0]
    if op in ("load", "loadb", "loadn"):
        src = path(s[2]) if op != "loadb" else read(s[2])
        env[s[1]] = piexif.load(src, key_is_name=(op == "loadn"))
        print(f"  {s[1]} loaded")
    elif op == "loadx":
        env[s[1]] = piexif.load(val(s[2], env))
        print(f"  {s[1]} loaded")
    elif op == "bytes":
        env[s[1]] = val(s[2], env)
    elif op == "dict":
        env[s[1]] = exif_dict(s[2], env)
    elif op == "dump":
        env[s[1]] = piexif.dump(env[s[2]])
        print(f"  {s[1]} = dump({s[2]}): {len(env[s[1]])} bytes")
    elif op == "insert":
        piexif.insert(env[s[1]], path(s[2]), path(s[3]))
        print(f"  inserted {s[1]} into {s[2]} as {s[3]}")
    elif op == "remove":
        piexif.remove(path(s[1]), path(s[2]))
        print(f"  removed Exif from {s[1]} as {s[2]}")
    elif op == "transplant":
        piexif.transplant(path(s[1]), path(s[2]), path(s[3]))
        print(f"  transplanted {s[1]} into {s[2]} as {s[3]}")
    elif op == "show":
        show(s[1], env[s[1]])
    elif op == "file":
        b = read(s[1])
        print(f"  {s[1]}: {len(b)} bytes")
        hexdump(b)
    elif op == "set":
        if s[2] == "thumbnail":
            env[s[1]]["thumbnail"] = val(s[4], env)
        else:
            env[s[1]][s[2]][s[3]] = val(s[4], env)
    elif op == "del":
        del env[s[1]][s[2]][s[3]]
    elif op == "ucload":
        print(f"  UserComment.load({val(s[1], env)!r}) = {UserComment.load(val(s[1], env))!r}")
    elif op == "ucdump":
        print(f"  UserComment.dump({s[1]!r}, {s[2]!r}) = {UserComment.dump(s[1], s[2])!r}")
    else:
        raise SystemExit(f"unknown step {op}")


def run_jobs():
    shutil.rmtree(path("out"), ignore_errors=True)
    os.makedirs(path("out"), exist_ok=True)
    with open(path("jobs.jsonl")) as f:
        for line in f:
            j = json.loads(line)
            print(f"== {j['name']}")
            env = {}
            for s in j["steps"]:
                try:
                    step(s, env)
                except Exception as e:
                    print(f"  {s[0]}: error {err(e)}")
                    break


# --- the photo programs ------------------------------------------------

def photos():
    return sorted(os.listdir(path("photos")))


def text(b):
    return b.decode("latin-1").strip()


def tenths(n, d):
    t = (n * 10 + d // 2) // d
    return f"{t // 10}.{t % 10}"


def decimal_deg(v, ref):
    """Degrees, minutes and seconds as micro-degrees, rounded half up."""
    (dn, dd), (mn, md), (sn, sd) = v
    den = dd * md * sd * 3600
    num = dn * md * sd * 3600 + mn * dd * sd * 60 + sn * dd * md
    micro = (num * 2000000 + den) // (2 * den)
    if ref in (b"S", b"W"):
        micro = -micro
    return micro


def micro_text(m):
    sign = "-" if m < 0 else ""
    m = abs(m)
    return f"{sign}{m // 1000000}.{m % 1000000:06d}"


ORIENTATION = {1: "normal", 2: "mirrored", 3: "rotated 180", 4: "flipped", 5: "mirrored, rotated 90 CCW",
               6: "rotated 90 CW", 7: "mirrored, rotated 90 CW", 8: "rotated 90 CCW"}


def taken(d):
    e = d["Exif"]
    if ExifIFD.DateTimeOriginal in e:
        return text(e[ExifIFD.DateTimeOriginal])
    if ImageIFD.DateTime in d["0th"]:
        return text(d["0th"][ImageIFD.DateTime])
    return None


def camera(d):
    z = d["0th"]
    make = text(z.get(ImageIFD.Make, b""))
    model = text(z.get(ImageIFD.Model, b""))
    if model.startswith(make):
        return model or "unknown"
    return f"{make} {model}".strip() or "unknown"


def report():
    print("== program: photo report")
    cams = {}
    for name in photos():
        try:
            d = piexif.load(path(f"photos/{name}"))
        except Exception as e:
            print(f"{name}: cannot read: {err(e)}")
            continue
        z, e, g = d["0th"], d["Exif"], d["GPS"]
        print(name)
        cam = camera(d)
        cams[cam] = cams.get(cam, 0) + 1
        print(f"  camera: {cam}")
        t = taken(d)
        off = e.get(ExifIFD.OffsetTimeOriginal)
        print(f"  taken: {t or '-'}{' ' + text(off) if off else ''}")
        if ExifIFD.ExposureTime in e:
            n, dd = e[ExifIFD.ExposureTime]
            print(f"  exposure: {n // dd if n >= dd and n % dd == 0 else f'{n}/{dd}'} s")
        if ExifIFD.FNumber in e:
            print(f"  aperture: f/{tenths(*e[ExifIFD.FNumber])}")
        if ExifIFD.ISOSpeedRatings in e:
            print(f"  iso: {e[ExifIFD.ISOSpeedRatings]}")
        if ExifIFD.FocalLength in e:
            n, dd = e[ExifIFD.FocalLength]
            print(f"  focal length: {n // dd if n % dd == 0 else tenths(n, dd)} mm")
        if ExifIFD.LensModel in e:
            print(f"  lens: {text(e[ExifIFD.LensModel])}")
        if ImageIFD.Orientation in z:
            print(f"  orientation: {ORIENTATION.get(z[ImageIFD.Orientation], 'unknown')}")
        if GPSIFD.GPSLatitude in g and GPSIFD.GPSLongitude in g:
            lat = decimal_deg(g[GPSIFD.GPSLatitude], g.get(GPSIFD.GPSLatitudeRef, b"N"))
            lon = decimal_deg(g[GPSIFD.GPSLongitude], g.get(GPSIFD.GPSLongitudeRef, b"E"))
            alt = ""
            if GPSIFD.GPSAltitude in g:
                n, dd = g[GPSIFD.GPSAltitude]
                below = g.get(GPSIFD.GPSAltitudeRef, 0) == 1
                alt = f", {'-' if below else ''}{tenths(n, dd)} m"
            print(f"  gps: {micro_text(lat)}, {micro_text(lon)}{alt}")
        if ExifIFD.UserComment in e:
            try:
                print(f"  comment: {UserComment.load(e[ExifIFD.UserComment])}")
            except ValueError as x:
                print(f"  comment: unreadable ({x})")
        private = [n for t, n in ((ImageIFD.Artist, "artist"), (ExifIFD.CameraOwnerName, "owner"),
                                  (ExifIFD.BodySerialNumber, "serial number"), (ExifIFD.MakerNote, "maker note"))
                   if t in z or t in e]
        if g:
            private.insert(0, "location")
        if private:
            print(f"  private: {', '.join(private)}")
        th = d["thumbnail"]
        print(f"  thumbnail: {len(th)} bytes" if th else "  thumbnail: none")
    print("cameras:")
    for cam in sorted(cams):
        print(f"  {cam}: {cams[cam]}")


def slug(s):
    out = []
    for c in s.lower():
        if c.isascii() and c.isalnum():
            out.append(c)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")


def organize():
    print("== program: organize")
    root = path("out/library")
    lines = []
    used = set()
    for name in photos():
        src = path(f"photos/{name}")
        try:
            d = piexif.load(src)
        except Exception as e:
            lines.append(f"{name} skipped ({type(e).__name__})")
            continue
        ext = os.path.splitext(name)[1].lower()
        t = taken(d)
        if t is None:
            rel = f"undated/{name}"
        else:
            date, time = t.split(" ")
            y, m, dd = date.split(":")
            rel = f"{y}/{m}-{dd}/{time.replace(':', '')}_{slug(camera(d))}"
            base = rel
            n = 1
            while rel + ext in used:
                n += 1
                rel = f"{base}-{n}"
            rel += ext
        used.add(rel)
        os.makedirs(os.path.dirname(os.path.join(root, rel)), exist_ok=True)
        shutil.copyfile(src, os.path.join(root, rel))
        lines.append(f"{name} -> {rel}")
    with open(os.path.join(root, "index.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    with open(os.path.join(root, "index.txt")) as f:
        print(f.read(), end="")
    for dirpath, dirs, files in sorted(os.walk(root)):
        dirs.sort()
        for fn in sorted(files):
            p = os.path.join(dirpath, fn)
            print(f"  {os.path.relpath(p, root)} {os.path.getsize(p)}")


def parse_micro(s):
    neg = s.startswith("-")
    s = s.lstrip("-")
    whole, _, frac = s.partition(".")
    frac = (frac + "000000")[:6]
    v = int(whole) * 1000000 + int(frac)
    return -v if neg else v


def parse_tenths(s):
    whole, _, frac = s.partition(".")
    return int(whole) * 10 + int((frac + "0")[:1])


def dms(micro):
    total = abs(micro)
    d = total // 1000000
    m_full = (total % 1000000) * 60
    m = m_full // 1000000
    s100 = ((m_full % 1000000) * 6000 + 500000) // 1000000
    return ((d, 1), (m, 1), (s100, 100))


def offset_seconds(off):
    sign = -1 if off[0] == "-" else 1
    return sign * (int(off[1:3]) * 3600 + int(off[4:6]) * 60)


def geotag():
    print("== program: clock fix and geotag")
    track = []
    with open(path("track.csv")) as f:
        next(f)
        for line in f:
            t, lat, lon, ele = line.strip().split(",")
            when = dt.datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
            track.append((int(when.timestamp()), parse_micro(lat), parse_micro(lon), parse_tenths(ele)))
    fixes = {}
    with open(path("clock.txt")) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.split()
            fixes[" ".join(parts[:-2])] = (int(parts[-2]), parts[-1])
    os.makedirs(path("out/tagged"), exist_ok=True)
    for name in photos():
        src = path(f"photos/{name}")
        try:
            d = piexif.load(src)
        except Exception as e:
            print(f"{name}: skipped ({type(e).__name__})")
            continue
        t = d["Exif"].get(ExifIFD.DateTimeOriginal)
        if t is None:
            print(f"{name}: no capture time")
            continue
        cam = camera(d)
        shift, off = fixes.get(cam, (0, None))
        if ExifIFD.OffsetTimeOriginal in d["Exif"]:
            off = text(d["Exif"][ExifIFD.OffsetTimeOriginal])
        if off is None:
            print(f"{name}: no time zone for {cam}")
            continue
        local = dt.datetime.strptime(text(t), "%Y:%m:%d %H:%M:%S") + dt.timedelta(seconds=shift)
        utc = int(local.replace(tzinfo=dt.timezone.utc).timestamp()) - offset_seconds(off)
        new_t = local.strftime("%Y:%m:%d %H:%M:%S")
        msg = f"{name}: {text(t)} -> {new_t} {off}"
        d["Exif"][ExifIFD.DateTimeOriginal] = new_t.encode()
        d["Exif"][ExifIFD.OffsetTimeOriginal] = off.encode()
        best = None
        for p in track:
            if best is None or abs(p[0] - utc) < abs(best[0] - utc):
                best = p
        if d["GPS"]:
            msg += ", has a location"
        elif best is None or abs(best[0] - utc) > 900:
            msg += ", no track point within 15 min"
        else:
            _, lat, lon, ele = best
            d["GPS"] = {GPSIFD.GPSVersionID: (2, 3, 0, 0),
                        GPSIFD.GPSLatitudeRef: b"S" if lat < 0 else b"N", GPSIFD.GPSLatitude: dms(lat),
                        GPSIFD.GPSLongitudeRef: b"W" if lon < 0 else b"E", GPSIFD.GPSLongitude: dms(lon),
                        GPSIFD.GPSAltitudeRef: 1 if ele < 0 else 0, GPSIFD.GPSAltitude: (abs(ele), 10)}
            msg += f", at {micro_text(lat)}, {micro_text(lon)} ({abs(best[0] - utc)} s from the track)"
        print(msg)
        out = path(f"out/tagged/{name}")
        piexif.insert(piexif.dump(d), src, out)
        again = piexif.load(out)
        g = again["GPS"]
        print(f"  written: {os.path.getsize(out)} bytes, time {text(again['Exif'][ExifIFD.DateTimeOriginal])}"
              f"{', gps ' + repr(g[GPSIFD.GPSLatitude]) + ' ' + repr(g[GPSIFD.GPSLongitude]) if g else ''}")


PRIVATE = [("0th", ImageIFD.Artist), ("Exif", ExifIFD.CameraOwnerName), ("Exif", ExifIFD.BodySerialNumber),
           ("Exif", ExifIFD.MakerNote), ("Exif", ExifIFD.UserComment)]


def share():
    print("== program: strip for sharing")
    os.makedirs(path("out/share"), exist_ok=True)
    for name in photos():
        src = path(f"photos/{name}")
        out = path(f"out/share/{name}")
        try:
            d = piexif.load(src)
        except Exception as e:
            print(f"{name}: not shared ({err(e)})")
            continue
        gone = []
        if d["GPS"]:
            gone.append(f"GPS ({len(d['GPS'])} tags)")
            d["GPS"] = {}
        for ifd, tag in PRIVATE:
            if tag in d[ifd]:
                gone.append(piexif.TAGS[ifd][tag]["name"])
                del d[ifd][tag]
        if d["thumbnail"] is not None:
            gone.append("thumbnail")
            d["thumbnail"] = None
            d["1st"] = {}
        if not any(d[i] for i in IFDS):
            piexif.remove(src, out)
            how = "no Exif"
        else:
            piexif.insert(piexif.dump(d), src, out)
            how = "rewritten"
        check = piexif.load(out)
        left = sum(len(check[i]) for i in IFDS)
        print(f"{name}: {how}, {os.path.getsize(src)} -> {os.path.getsize(out)} bytes, {left} tags kept")
        if gone:
            print(f"  removed: {', '.join(gone)}")
        assert not check["GPS"]


def thumbs():
    print("== program: thumbnails")
    os.makedirs(path("out/thumbs"), exist_ok=True)
    for name in photos():
        try:
            d = piexif.load(path(f"photos/{name}"))
        except Exception:
            continue
        th = d["thumbnail"]
        if not th:
            continue
        stem = os.path.splitext(name)[0]
        with open(path(f"out/thumbs/{stem}.jpg"), "wb") as f:
            f.write(th)
        first = d["1st"]
        print(f"{stem}.jpg: {len(th)} bytes, starts {th[:4].hex()}, ends {th[-2:].hex()}, "
              f"compression {first.get(ImageIFD.Compression, '-')}")


run_jobs()
report()
organize()
geotag()
share()
thumbs()
