# Writes data/: a downloads folder of .torrent files (Linux images, an
# album, an office suite, a private tracker's upload, an old client's
# Shift-JIS names, broken and truncated files), the data of two partly
# downloaded torrents with the .torrent files a client checks them
# against, folders to make new torrents from, and jobs.tsv, the jobs
# oracle.py and mini_torrentool.kara run. The .torrent files are made
# with torrentool's own Bencode (vendor/torrentool) or written byte by
# byte where a real tool wrote them differently.
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
sys.path.insert(0, os.path.join(HERE, "vendor"))
sys.dont_write_bytecode = True

from torrentool.bencode import Bencode  # noqa: E402


def write(rel, body):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if isinstance(body, str):
        body = body.encode("utf-8")
    with open(path, "wb") as f:
        f.write(body)


def fake_pieces(seed, count):
    return b"".join(hashlib.sha1(("%s/%d" % (seed, i)).encode()).digest() for i in range(count))


def pieces_of(blob, plen):
    return b"".join(hashlib.sha1(blob[i:i + plen]).digest() for i in range(0, len(blob), plen))


def raw(v):
    # Bencode as some tools write it: dict keys in the order given.
    if isinstance(v, str):
        v = v.encode("utf-8")
    if isinstance(v, bytes):
        return b"%d:" % len(v) + v
    if isinstance(v, int):
        return b"i%de" % v
    if isinstance(v, list):
        return b"l" + b"".join(raw(x) for x in v) + b"e"
    return b"d" + b"".join(raw(k) + raw(x) for k, x in v.items()) + b"e"


class Lcg:
    def __init__(self, seed):
        self.x = seed

    def next(self, n):
        self.x = (self.x * 1103515245 + 12345) % 2147483648
        return self.x % n


# ------------------------------------------------------------ the library

ALPINE = "alpine-standard-3.20.3-x86_64.iso"
ALPINE_LEN = 216006656
ALPINE_INFO = {"name": ALPINE, "length": ALPINE_LEN, "piece length": 1048576,
               "pieces": fake_pieces("alpine", (ALPINE_LEN + 1048575) // 1048576)}


def library():
    out = {}
    out["alpine-standard-3.20.3-x86_64.iso.torrent"] = Bencode.encode({
        "announce": "http://torrent.alpinelinux.org:6969/announce",
        "announce-list": [["http://torrent.alpinelinux.org:6969/announce"],
                          ["udp://tracker.opentrackr.org:1337/announce", "udp://open.demonii.com:1337/announce"]],
        "comment": "Alpine Linux 3.20.3 standard image",
        "created by": "mktorrent 1.1",
        "creation date": 1725961200,
        "url-list": "https://dl-cdn.alpinelinux.org/alpine/v3.20/releases/x86_64/",
        "info": ALPINE_INFO,
    })
    # The same image from a mirror's own tracker: the same info hash.
    out["alpine-mirror.torrent"] = Bencode.encode({
        "announce": "https://tracker.mirror.example.net/announce?distro=alpine&arch=x86_64",
        "creation date": 1725964800,
        "info": ALPINE_INFO,
    })
    deb = [("libreoffice24.8-base_24.8.2.1-1_amd64.deb", 2093416), ("libreoffice24.8-calc_24.8.2.1-1_amd64.deb", 10334932),
           ("libreoffice24.8-core_24.8.2.1-1_amd64.deb", 41562320), ("libreoffice24.8-writer_24.8.2.1-1_amd64.deb", 8890664),
           ("libobasis24.8-en-us_24.8.2.1-1_amd64.deb", 1048576)]
    total = sum(n for _, n in deb)
    out["LibreOffice_24.8.2_Linux_x86-64_deb.torrent"] = Bencode.encode({
        "announce": "udp://tracker.documentfoundation.org:6969/announce",
        "created by": "Transmission/4.0.5 (a6fe2a64aa)",
        "creation date": 1728396000,
        "url-list": ["https://download.documentfoundation.org/libreoffice/stable/24.8.2/deb/x86_64/",
                     "https://mirror.example.org/tdf/libreoffice/stable/24.8.2/deb/x86_64/"],
        "info": {"name": "LibreOffice_24.8.2_Linux_x86-64_deb",
                 "files": [{"length": n, "path": ["DEBS", f]} for f, n in deb] + [{"length": 4096, "path": ["readmes", "README_en-US"]}],
                 "piece length": 4194304, "pieces": fake_pieces("lo", (total + 4096 + 4194303) // 4194304)},
    })
    tracks = ["01 - Dawn Chorus.flac", "02 - Harbour Lights.flac", "03 - Night Ferry (feat. Mira).flac", "04 - Últimos días.flac"]
    files = [{"length": 31000000 + 1000003 * i, "path": ["CD1", t]} for i, t in enumerate(tracks)]
    files += [{"length": 184320, "path": ["cover.jpg"]}, {"length": 2048, "path": ["CD1", "album.cue"]},
              {"length": 0, "path": ["CD1", ".hidden", "empty.log"]}]
    out["The Quiet Tides - Harbour (2019) [FLAC].torrent"] = Bencode.encode({
        "announce": "udp://tracker.opentrackr.org:1337/announce",
        "comment": "Released under CC BY-SA 4.0 — share freely",
        "created by": "qBittorrent v4.6.4",
        "creation date": 1555300000,
        "info": {"name": "The Quiet Tides - Harbour (2019) [FLAC]", "files": files, "piece length": 2097152,
                 "pieces": fake_pieces("tides", 64)},
    })
    out["private-upload.torrent"] = Bencode.encode({
        "announce": "https://tracker.example.org/PASSKEY/announce",
        "created by": "mkbrr/1.3.0",
        "creation date": 1729000000,
        "info": {"name": "Field.Recordings.Vol.3.2024.WEB.FLAC", "length": 734003200, "piece length": 4194304,
                 "pieces": fake_pieces("field", 175), "private": 1, "source": "RED"},
    })
    # An old Japanese client: names in Shift-JIS, with name.utf-8 beside.
    out["natsu-sjis.torrent"] = raw({
        "announce": "http://tracker.example.jp:6969/announce", "creation date": 1199145600, "encoding": "SHIFT_JIS",
        "info": {"files": [{"length": 367001856, "path": ["第1話.mkv".encode("shift_jis")]},
                           {"length": 1024, "path": ["readme.txt"]}],
                 "name": "夏のアルバム".encode("shift_jis"), "name.utf-8": "夏のアルバム",
                 "piece length": 1048576, "pieces": fake_pieces("natsu", 351)},
    })
    # Archive.org style: url-list is one string, httpseeds beside it, and
    # the info keys in the order the tool wrote them rather than sorted.
    out["nasa-apollo11-msn_archive.torrent"] = raw({
        "announce": "http://bt1.archive.org:6969/announce",
        "announce-list": [["http://bt1.archive.org:6969/announce"], ["http://bt2.archive.org:6969/announce"]],
        "comment": "This content hosted at the Internet Archive at https://archive.org/details/nasa-apollo11-msn",
        "created by": "ia_make_torrent", "creation date": 1612137600,
        "httpseeds": ["https://ia800300.us.archive.org/1/items/"],
        "info": {"name": "nasa-apollo11-msn", "files": [{"length": 1203400, "path": ["transcript.txt"]},
                                                         {"length": 98000, "path": ["logo.png"]}],
                 "piece length": 524288, "pieces": fake_pieces("ia", 3)},
        "url-list": "https://archive.org/download/",
    })
    # Broken ones.
    whole = out["private-upload.torrent"]
    out["truncated.torrent"] = whole[:180]
    out["empty.torrent"] = b""
    out["error-page.torrent"] = b"<html><head><title>404 Not Found</title></head><body>Not Found</body></html>\n"
    out["no-info.torrent"] = Bencode.encode({"announce": "http://tracker.example.com/announce", "comment": "info dict missing"})
    out["list.torrent"] = b"l4:spam4:eggse"
    out["info-list.torrent"] = Bencode.encode({"announce": "udp://tracker.example.com:80", "info": ["files", "oops"]})
    out["no-length.torrent"] = Bencode.encode({"info": {"name": "half-written", "files": [{"path": ["a.bin"]}],
                                                        "piece length": 16384, "pieces": b""}})
    out["string-date.torrent"] = Bencode.encode({"creation date": "1700000000", "info": {"name": "date-as-text.txt", "length": 10,
                                                                                        "piece length": 16384, "pieces": fake_pieces("d", 1)}})
    out["far-future.torrent"] = Bencode.encode({"creation date": 253402300800, "info": {"name": "y10k.txt", "length": 1,
                                                                                       "piece length": 16384, "pieces": fake_pieces("y", 1)}})
    return out


# ------------------------------------------------------------ downloads

def osm_csv():
    r = Lcg(7)
    rows = ["id,lat,lon,amenity,name"]
    names = ["Café de Paris", "Port Hercule", "Jardin Exotique", "Musée Océanographique", "Casino", "Stade Louis II",
             "Gare de Monaco", "Fontvieille", "Larvotto", "Palais Princier"]
    kinds = ["cafe", "harbour", "park", "museum", "casino", "stadium", "station", "marina", "beach", "palace", "bench", "bus_stop"]
    for i in range(520):
        rows.append("%d,43.7%05d,7.4%05d,%s,%s" % (21000000 + r.next(9000000), r.next(100000), r.next(100000),
                                                  kinds[r.next(len(kinds))], names[r.next(len(names))] if r.next(3) == 0 else ""))
    return "\n".join(rows) + "\n"


def tiles_index():
    r = Lcg(11)
    return "".join("14/%d/%d.png %d\n" % (8530 + r.next(12), 5970 + r.next(12), 1000 + r.next(30000)) for _ in range(300))


def downloads():
    osm = [("README.md", "# OpenStreetMap extract: Monaco\n\nNodes with an amenity tag, as CSV.\nData © OpenStreetMap contributors, ODbL 1.0.\n"),
           ("monaco-amenities.csv", osm_csv()),
           ("tiles/index.txt", tiles_index()),
           ("LICENSE.txt", "Open Data Commons Open Database License (ODbL) v1.0\n" + "See https://opendatacommons.org/licenses/odbl/1-0/\n" * 3)]
    return osm


def check_torrents(osm):
    # The torrent the client has: built over the full data with 4 KiB pieces.
    blob = b"".join(body.encode() for _, body in osm_order(osm))
    info = {"name": "osm-monaco", "piece length": 4096, "pieces": pieces_of(blob, 4096),
            "files": [{"length": len(body.encode()), "path": path.split("/")} for path, body in osm_order(osm)]}
    full = Bencode.encode({"announce": "udp://tracker.opentrackr.org:1337/announce", "info": info})
    notes = "Release notes\n\n" + "".join("- fixed issue #%d in the parser\n" % (100 + i) for i in range(60))
    single = Bencode.encode({"info": {"name": "release-notes.txt", "length": len(notes.encode()), "piece length": 1024,
                                      "pieces": pieces_of(notes.encode(), 1024)}})
    return full, single, notes


def osm_order(osm):
    # The order a torrent lists them in: by path, as torrent makers do.
    return sorted(osm, key=lambda f: f[0])


# ------------------------------------------------------------ jobs

BDECODE = [
    ("-", r"d3:cow3:moo4:spam4:eggse"),
    ("-", r"l4:spam4:eggsi-3ee"),
    ("-", r"d4:spaml1:a1:bee"),
    ("-", r"i42e"),
    ("-", r"i-0e"),
    ("-", r"i 12 e"),
    ("-", r"i1_000_000e"),
    ("-", r"i+7e"),
    ("-", r"ie"),
    ("-", r"i12"),
    ("-", r"i0x10e"),
    ("-", r"i99999999999999999999999999e"),
    ("-", r"0:"),
    ("-", r"4:spa"),
    ("-", r"3 :abc"),
    ("-", r"12"),
    ("-", r"le"),
    ("-", r"de"),
    ("-", r""),
    ("-", r"l"),
    ("-", r"d3:onei1e3:two"),
    ("-", r"ld1:ai1eel"),
    ("-", r"e"),
    ("-", r"i1ee4:rest"),
    ("-", r"x"),
    ("-", r"4:spam4:eggs"),
    ("-", r"d1:bi2e1:ai1e1:ai3ee"),
    ("-", r"d1:ai1e1:be"),
    ("-", r"di2e3:twoi1e3:onee"),
    ("-", r"di1e1:a1:bi2ee"),
    ("-", r"dl1:aei1ee"),
    ("-", r"d1:ai1ei5ee"),
    ("-", r"d1:z1:y1:a1:b1:m1:ne"),
    ("-", r"4:\xff\xfe\x00\x01"),
    ("-", r"5:caf\xc3\xa9"),
    ("-", r"3:caf\xe9"),
    ("pieces", r"d6:pieces4:\x01\x02\xfe\xff4:name3:\xe9t\xe9e"),
    ("pieces", r"d6:pieces5:\xc3\xa9t\xc3\xa94:path2:\xff/e"),
    ("pieces", r"l6:pieces2:\xed\xa0\x80e"),
    ("pieces", r"d4:name4:\xf0\x9f\x98e"),
    ("pieces,name", r"d4:name2:\xc0\xafe"),
    ("-", r"\xb23:abc"),
    ("-", r"i1\xa02e"),
    ("-", r"d3:\xff\xfei1e3:abci2ee"),
    ("-", r"i1e\x80tail"),
]

EDITS = [
    ("alpine-standard-3.20.3-x86_64.iso.torrent", ["announce=udp://tracker.example.com:80/announce"]),
    ("alpine-standard-3.20.3-x86_64.iso.torrent", ["announce=[udp://a.example:1/announce]"]),
    ("alpine-standard-3.20.3-x86_64.iso.torrent", ["announce=[udp://a.example:1/announce,http://b.example/announce]"]),
    ("alpine-standard-3.20.3-x86_64.iso.torrent", ["announce=[[udp://a.example:1/announce,udp://c.example:2/announce],[http://b.example/announce]]"]),
    ("alpine-standard-3.20.3-x86_64.iso.torrent", ["announce=[]"]),
    ("alpine-standard-3.20.3-x86_64.iso.torrent", ["announce=-"]),
    ("alpine-standard-3.20.3-x86_64.iso.torrent", ["webseeds=-", "comment=mirrored"]),
    ("LibreOffice_24.8.2_Linux_x86-64_deb.torrent", ["webseeds=https://cdn.example.com/lo/", "httpseeds=[http://seed.example/a,http://seed.example/b]"]),
    ("LibreOffice_24.8.2_Linux_x86-64_deb.torrent", ["private=1", "source=TDF"]),
    ("private-upload.torrent", ["private=0", "source=OPS", "announce=https://tracker.example.net/KEY/announce"]),
    ("private-upload.torrent", ["name=Field Recordings Vol 3", "date=2024-10-20T08:30:00"]),
    ("no-info.torrent", ["source=x"]),
    ("no-info.torrent", ["name=rescued"]),
    ("empty.torrent", ["name=new", "announce=udp://t.example:1/announce"]),
    ("nasa-apollo11-msn_archive.torrent", ["date=1969-07-20T20:17:40", "comment=Tranquility Base here"]),
    ("natsu-sjis.torrent", ["webseeds=[]"]),
]

CREATES = [
    ("data/downloads/osm-monaco", ["tracker=udp://tracker.opentrackr.org:1337/announce,udp://open.demonii.com:1337/announce", "comment=Monaco amenities, October 2024"]),
    ("data/src/release-notes.txt", []),
    ("data/src/release-notes.txt", ["tracker=http://tracker.example.com/announce"]),
    ("data/src/My Album v1.0", ["comment=demo"]),
    ("data/src/blank.txt", []),
    ("data/src/only-empty", []),
    ("data/src/site", ["tracker=udp://a.example:1/announce,udp://b.example:2/announce,udp://c.example:3/announce"]),
]


def jobs():
    out = []
    for keys, text in BDECODE:
        out.append(["bdecode", keys, text])
    for s in ["d4:name5:Caféi1e3:abce", "l5:日本語e", "3:日本語", "i1e"]:
        out.append(["read_string", s])
    for n in ["0", "1", "1023", "1024", "1536", "10240", "1048575", "1048576", "1073741824", "5368709120",
              "1099511627776", "1125899906842624", "1152921504606846976", "123456789", "999999", "6114656256"]:
        out.append(["humanize", n])
    names = sorted(library())
    for n in names:
        out.append(["torrent", "library/" + n])
    for n in names:
        out.append(["recode", "library/" + n])
    out.append(["info", "library/alpine-standard-3.20.3-x86_64.iso.torrent"])
    out.append(["info", "library/The Quiet Tides - Harbour (2019) [FLAC].torrent"])
    out.append(["info", "library/natsu-sjis.torrent"])
    out.append(["info", "library/no-length.torrent"])
    for f, ops in EDITS:
        out.append(["edit", "library/" + f] + ops)
    for src, opts in CREATES:
        out.append(["create", src] + opts)
    out.append(["library", "library"])
    out.append(["verify", "check/osm-monaco.torrent", "downloads"])
    out.append(["verify", "check/osm-monaco.torrent", "partial"])
    out.append(["verify", "check/release-notes.txt.torrent", "src"])
    out.append(["verify", "check/release-notes.txt.torrent", "partial"])
    return out


def main():
    if os.path.isdir(DATA):
        shutil.rmtree(DATA)
    for name, body in library().items():
        write("library/" + name, body)
    osm = downloads()
    for path, body in osm:
        write("downloads/osm-monaco/" + path, body)
    full, single, notes = check_torrents(osm)
    write("check/osm-monaco.torrent", full)
    write("check/release-notes.txt.torrent", single)
    write("src/release-notes.txt", notes)
    # A partial download: the CSV cut short, one byte of the tiles index
    # changed, and the licence not fetched yet.
    for path, body in osm:
        if path == "LICENSE.txt":
            continue
        b = body.encode()
        if path == "monaco-amenities.csv":
            b = b[:9000]
        if path == "tiles/index.txt":
            b = b[:4500] + b"X" + b[4501:]
        write("partial/osm-monaco/" + path, b)
    write("partial/release-notes.txt", notes.replace("#130", "#131"))
    write("src/My Album v1.0/01 Intro.txt", "intro\n")
    write("src/My Album v1.0/02 Theme.txt", "theme " * 50 + "\n")
    write("src/My Album v1.0/notes/credits.txt", "Written by A. Person\n")
    write("src/blank.txt", "")
    write("src/only-empty/a.txt", "")
    write("src/only-empty/sub/b.txt", "")
    write("src/site/index.html", "<!doctype html><title>Site</title>\n")
    write("src/site/robots.txt", "User-agent: *\nDisallow:\n")
    write("src/site/.keep", "")
    write("src/site/assets/app.css", "body { margin: 0 }\n")
    write("src/site/assets/img/logo.svg", "<svg xmlns='http://www.w3.org/2000/svg'/>\n")
    write("jobs.tsv", "".join("\t".join(job) + "\n" for job in jobs()))


main()
