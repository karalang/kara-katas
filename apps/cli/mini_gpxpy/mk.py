# Writes data/: the GPX files the run reads. They are gpxpy's own test
# files (copied from tracks/) and five more written here: a run recorded
# by a sports watch (Garmin's TrackPointExtension with heart rate and
# cadence, local times with milliseconds, a pause and a GPS dropout that
# starts a new segment), a file of awkward timestamps, and four broken
# files. The longest test tracks are cut to their first points (TRIM), so
# the interpreted run stays short.
import math, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def watch_run():
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<gpx creator="Forerunner 265" version="1.1" xmlns="http://www.topografix.com/GPX/1/1" '
           'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
           'xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1" '
           'xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd '
           'http://www.garmin.com/xmlschemas/TrackPointExtension/v1 '
           'http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd">',
           ' <metadata>',
           '  <link href="connect.example.com"><text>Example Connect</text></link>',
           '  <time>2024-10-12T07:58:41.000+02:00</time>',
           ' </metadata>',
           ' <trk>',
           '  <name>Morning Run &amp; Strides</name>',
           '  <type>running</type>',
           '  <trkseg>']
    lat0, lon0 = 46.0512, 14.5060
    t = 8 * 3600 + 0 * 60 + 3  # seconds after midnight, local time
    ms = 250
    seg = 0
    for i in range(150):
        if i == 100:
            out.append('  </trkseg>')
            out.append('  <trkseg>')
            seg = 1
            t += 95  # GPS dropout under a bridge
        a = 2 * math.pi * i / 120
        r = 0.006 + 0.0004 * math.sin(5 * a)
        lat = lat0 + r * math.sin(a)
        lon = lon0 + 1.45 * r * math.cos(a)
        ele = 296 + 9 * math.sin(3 * a) + (0.4 if i % 7 == 0 else 0)
        hr = 128 + int(30 * (1 - math.cos(a)) / 2) + (i % 5)
        cad = 0 if 70 <= i < 78 else 84 + (i % 3)
        if 70 <= i < 78:
            lat = out_lat
            lon = out_lon
        else:
            out_lat, out_lon = lat, lon
        hh, mm, ss = t // 3600, t // 60 % 60, t % 60
        stamp = f'2024-10-12T{hh:02d}:{mm:02d}:{ss:02d}.{ms:03d}+02:00'
        out.append(f'   <trkpt lat="{lat:.7f}" lon="{lon:.7f}">')
        out.append(f'    <ele>{ele:.1f}</ele>')
        out.append(f'    <time>{stamp}</time>')
        out.append('    <extensions>')
        out.append('     <gpxtpx:TrackPointExtension>')
        out.append(f'      <gpxtpx:hr>{hr}</gpxtpx:hr>')
        out.append(f'      <gpxtpx:cad>{cad}</gpxtpx:cad>')
        out.append('     </gpxtpx:TrackPointExtension>')
        out.append('    </extensions>')
        out.append('   </trkpt>')
        step = 7 if seg == 0 else 6
        if 70 <= i < 78:
            step = 9  # waiting at a crossing
        t += step
        ms = (ms + 137) % 1000
    out += ['  </trkseg>', ' </trk>', '</gpx>']
    return "\n".join(out) + "\n"


ODD_TIMES = """<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.0" creator="hand-edited" xmlns="http://www.topografix.com/GPX/1/0">
<time>2021-03-28 01:59:59</time>
<wpt lat="45.0" lon="13.0"><time>2021-3-5T4:05:06</time><name>short fields</name></wpt>
<wpt lat="45.1" lon="13.1"><time>2021-03-05T04:05:06.1234567Z</time><name>seven digits</name></wpt>
<wpt lat="45.2" lon="13.2"><time>2021-03-05T04:05:06−05:30</time><name>unicode minus</name></wpt>
<wpt lat="45.3" lon="13.3"><time>2021-03-05T04:05:06A05:00</time><name>a letter for a sign</name></wpt>
<wpt lat="45.4" lon="13.4"><time>2021-03-05T04:05:06+0530</time><name>no colon</name></wpt>
<wpt lat="45.5" lon="13.5"><time>2021-03-05T04:05:06+05</time><name>hours only</name></wpt>
<wpt lat="45.6" lon="13.6"><time>2021-13-05T04:05:06Z</time><name>month 13</name></wpt>
<wpt lat="45.7" lon="13.7"><time>2021-02-29T04:05:06Z</time><name>not a leap year</name></wpt>
<wpt lat="45.8" lon="13.8"><time>2021-03-05T04:05:06Z
</time><name>newline at the end</name></wpt>
<wpt lat="45.9" lon="13.9"><time> 2021-03-05T04:05:06Z</time><name>space at the start</name></wpt>
<wpt lat=" 46.0 " lon="+14.0"><ele> 1_000 </ele><sat>+07</sat><fix>dgps</fix><name>padded numbers</name></wpt>
<wpt lat="46.1" lon="14.1"><ele>1e-05</ele><magvar>12345678901234567890.5</magvar><name>&lt;exponents&gt; &#x26; &#38;</name></wpt>
<trk><trkseg>
<trkpt lat="46.0" lon="14.0"><time>2021-03-05T04:05:06.5+01:00</time></trkpt>
<trkpt lat="46.001" lon="14.001"><time>2021-03-05T03:05:16Z</time></trkpt>
<trkpt lat="46.002" lon="14.002"><time>2021-03-05T05:05:26+02:00</time></trkpt>
</trkseg></trk>
</gpx>
"""

BROKEN = {
    "broken-mismatched-tag.gpx": '<?xml version="1.0"?>\n<gpx version="1.1">\n <trk><name>x</trk>\n</gpx>\n',
    "broken-latitude.gpx": ('<gpx version="1.1"><wpt lat="46.1x" lon="14.0"><name>typo</name></wpt></gpx>\n'),
    "broken-missing-lon.gpx": ('<gpx version="1.0"><trk><trkseg><trkpt lat="46.1"/></trkseg></trk></gpx>\n'),
    "broken-fix.gpx": ('<gpx version="1.1"><wpt lat="46.1" lon="14.0"><fix>4d</fix></wpt></gpx>\n'),
}


# test file: the number of track points kept
TRIM = {
    "cerknicko-jezero-no-creator.gpx": 90,
    "cerknicko-jezero-with-elevations-zero.gpx": 90,
    "cerknicko-jezero-without-elevations.gpx": 90,
    "cerknicko-jezero.gpx": 90,
    "cerknicko-without-times.gpx": 90,
    "korita-zbevnica.gpx": 180,
}


def trim(text, keep):
    # drops every <trkpt> element after the first `keep`, with the
    # whitespace before it
    seen = 0

    def cut(m):
        nonlocal seen
        seen += 1
        return m.group(0) if seen <= keep else ""
    return re.sub(r"\s*<trkpt\b.*?</trkpt>", cut, text, flags=re.S)


def main():
    os.makedirs(DATA, exist_ok=True)
    for name in sorted(os.listdir(os.path.join(HERE, "tracks"))):
        with open(os.path.join(HERE, "tracks", name), encoding="utf-8", newline="") as f:
            text = f.read()
        if name in TRIM:
            text = trim(text, TRIM[name])
        with open(os.path.join(DATA, name), "w", encoding="utf-8", newline="") as f:
            f.write(text)
    with open(os.path.join(DATA, "watch-run.gpx"), "w", encoding="utf-8") as f:
        f.write(watch_run())
    with open(os.path.join(DATA, "odd-times.gpx"), "w", encoding="utf-8") as f:
        f.write(ODD_TIMES)
    for name, text in BROKEN.items():
        with open(os.path.join(DATA, name), "w", encoding="utf-8") as f:
            f.write(text)


if __name__ == "__main__":
    main()
