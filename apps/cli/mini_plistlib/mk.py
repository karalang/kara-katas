#!/usr/bin/env python3
"""Writes data/ for mini_plistlib: real-world property lists in XML and
binary form, hand-made binary files that plistlib's own writer never
produces (shared references, int keys, None, 4-byte reals, UIDs), broken
files, and data/jobs.tsv."""
import datetime
import os
import plistlib
import struct

D = "data"


def put(name, data):
    path = os.path.join(D, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if isinstance(data, str):
        data = data.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)


INFO = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleDevelopmentRegion</key>
	<string>en</string>
	<key>CFBundleDisplayName</key>
	<string>Café Notes</string>
	<key>CFBundleExecutable</key>
	<string>CafeNotes</string>
	<key>CFBundleIdentifier</key>
	<string>com.example.cafenotes</string>
	<key>CFBundleInfoDictionaryVersion</key>
	<string>6.0</string>
	<key>CFBundlePackageType</key>
	<string>APPL</string>
	<key>CFBundleShortVersionString</key>
	<string>2.4.1</string>
	<key>CFBundleVersion</key>
	<string>2041</string>
	<key>CFBundleURLTypes</key>
	<array>
		<dict>
			<key>CFBundleURLName</key>
			<string>com.example.cafenotes.open</string>
			<key>CFBundleURLSchemes</key>
			<array>
				<string>cafenotes</string>
				<string>cafe-notes</string>
			</array>
		</dict>
	</array>
	<key>CFBundleDocumentTypes</key>
	<array>
		<dict>
			<key>CFBundleTypeExtensions</key>
			<array>
				<string>cnote</string>
			</array>
			<key>CFBundleTypeName</key>
			<string>Café Note</string>
			<key>CFBundleTypeRole</key>
			<string>Editor</string>
			<key>LSHandlerRank</key>
			<string>Owner</string>
		</dict>
	</array>
	<key>LSApplicationCategoryType</key>
	<string>public.app-category.productivity</string>
	<key>LSMinimumSystemVersion</key>
	<string>12.0</string>
	<key>NSHighResolutionCapable</key>
	<true/>
	<key>NSSupportsAutomaticTermination</key>
	<false/>
	<key>NSHumanReadableCopyright</key>
	<string>Copyright © 2024 Example &amp; Co. All rights reserved.</string>
	<key>NSAppTransportSecurity</key>
	<dict>
		<key>NSAllowsArbitraryLoads</key>
		<false/>
		<key>NSExceptionDomains</key>
		<dict>
			<key>sync.example.com</key>
			<dict>
				<key>NSExceptionMinimumTLSVersion</key>
				<string>TLSv1.2</string>
				<key>NSIncludesSubdomains</key>
				<true/>
			</dict>
		</dict>
	</dict>
	<key>UIRequiredDeviceCapabilities</key>
	<array/>
</dict>
</plist>
"""

LAUNCHD = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Label</key>
	<string>com.example.backup</string>
	<!-- run the nightly backup as the backup user -->
	<key>UserName</key>
	<string>backup</string>
	<key>ProgramArguments</key>
	<array>
		<string>/usr/local/bin/backup</string>
		<string>--target</string>
		<string>/Volumes/Archive</string>
		<string>--exclude=*.tmp</string>
	</array>
	<key>EnvironmentVariables</key>
	<dict>
		<key>PATH</key>
		<string>/usr/local/bin:/usr/bin:/bin</string>
		<key>BACKUP_LEVEL</key>
		<string>incremental</string>
	</dict>
	<key>StartCalendarInterval</key>
	<array>
		<dict>
			<key>Hour</key>
			<integer>2</integer>
			<key>Minute</key>
			<integer>30</integer>
		</dict>
		<dict>
			<key>Weekday</key>
			<integer>0</integer>
			<key>Hour</key>
			<integer>4</integer>
			<key>Minute</key>
			<integer>0</integer>
		</dict>
	</array>
	<key>KeepAlive</key>
	<dict>
		<key>SuccessfulExit</key>
		<false/>
		<key>NetworkState</key>
		<true/>
	</dict>
	<key>ThrottleInterval</key>
	<integer>300</integer>
	<key>Nice</key>
	<integer>-5</integer>
	<key>SoftResourceLimits</key>
	<dict>
		<key>NumberOfFiles</key>
		<integer>4096</integer>
	</dict>
	<key>StandardOutPath</key>
	<string>/var/log/backup.log</string>
	<key>StandardErrorPath</key>
	<string>/var/log/backup.err</string>
	<key>WorkingDirectory</key>
	<string>/var/empty</string>
</dict>
</plist>
"""

# Edge cases of the XML reader: entities, CDATA, number spellings, partial
# dates, whitespace in base64, \r line ends, duplicate keys, no header.
EDGES = (
    "<plist version=\"1.0\">\r\n"
    "<dict>\r\n"
    "  <key>entities</key><string>a &lt;b&gt; &amp; &quot;c&quot; &apos;d&apos; &#65;&#x42;&#169;&#x1F600;</string>\r\n"
    "  <key>cdata</key><string><![CDATA[x < y && y > z]]></string>\r\n"
    "  <key>mixed</key><string>one\r\ntwo\rthree\nfour\ttab</string>\r\n"
    "  <key>empty</key><string></string>\r\n"
    "  <key>empty2</key><string/>\r\n"
    "  <key>ints</key>\r\n"
    "  <array>\r\n"
    "    <integer>0</integer><integer>+5</integer><integer> 7 </integer><integer>1_000</integer>\r\n"
    "    <integer>-42</integer><integer>0x1F</integer><integer>0X_ff</integer>\r\n"
    "    <integer>9223372036854775807</integer><integer>-9223372036854775808</integer>\r\n"
    "    <integer>18446744073709551615</integer><integer>9223372036854775808</integer>\r\n"
    "  </array>\r\n"
    "  <key>reals</key>\r\n"
    "  <array>\r\n"
    "    <real>1.5</real><real>1e3</real><real>-0.0</real><real>0.0</real><real>inf</real><real>-Infinity</real>\r\n"
    "    <real> .5</real><real>5.</real><real>1_0.25</real><real>0.1</real><real>1e-7</real><real>123456789012345678</real>\r\n"
    "    <real>2.5e-308</real><real>1.7976931348623157e308</real><real>3.0</real><real>100</real>\r\n"
    "  </array>\r\n"
    "  <key>dates</key>\r\n"
    "  <array>\r\n"
    "    <date>2024-02-29T23:59:59Z</date><date>1999-12-31T00:00:00Z</date><date>2001-01-01Z</date>\r\n"
    "    <date>2024-06-15T09Z</date><date>2024-06-15T09:45Z</date><date>0001-01-01T00:00:00Z</date>\r\n"
    "  </array>\r\n"
    "  <key>blob</key>\r\n"
    "  <data>\r\n"
    "    SGVs bG8s\r\n"
    "    IHBs aXN0\r\n"
    "    IQ==\r\n"
    "  </data>\r\n"
    "  <key>nodata</key><data></data>\r\n"
    "  <key>nested</key><array><array><array><dict/></array><array/></array></array>\r\n"
    "  <key>dup</key><string>first</string>\r\n"
    "  <key>z-last</key><true/>\r\n"
    "  <key>dup</key><string>second</string>\r\n"
    "  <key>&lt;angle&gt;</key><integer>1</integer>\r\n"
    "  <key>Ünïcode</key><string>日本語テキスト</string>\r\n"
    "  <key>emoji</key><string>🚀 launch</string>\r\n"
    "  <key>unknown</key><string>a<b>ignored-reset</b>tail</string>\r\n"
    "</dict>\r\n"
    "</plist>\r\n"
)

BOM = b"\xef\xbb\xbf" + b"""<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<array>
	<string>byte order mark</string>
	<integer>1</integer>
</array>
</plist>
"""

PREFS = {
    "NSWindow Frame Main": "120 340 980 640 0 0 1680 1025 ",
    "RecentFiles": [
        "/Users/ana/Notes/Groceries.cnote",
        "/Users/ana/Notes/Trip – Lisbon.cnote",
        "/Users/ana/Notes/🚀 Launch plan.cnote",
    ],
    "FontName": "Menlo-Regular",
    "FontSize": 13.0,
    "Zoom": 1.25,
    "LineSpacing": 0.1,
    "AutosaveDelay": 30,
    "LastLaunch": datetime.datetime(2024, 3, 9, 17, 42, 5),
    "FirstLaunch": datetime.datetime(1998, 7, 4, 8, 0, 0),
    "TrialEnds": datetime.datetime(2024, 4, 1, 0, 0, 0, 500000),
    "WindowState": bytes(range(0, 48)) + b"\xff\xfe\x00\x01",
    "Big": 2 ** 63 + 5,
    "Small": -2 ** 63,
    "Negative": -1,
    "Medium": 70000,
    "Huge32": 4000000000,
    "Flags": [True, False, True, True],
    "Ratios": [0.5, 0.5, 1.0, 1, True],
    "Zeros": [0.0, -0.0, 0, False],
    "Empty": {},
    "EmptyList": [],
    "Theme": {"Dark": {"Accent": "orange", "Contrast": 2}, "Light": {"Accent": "blue", "Contrast": 1}},
    "SameTwice": ["repeat", "repeat", "repeat"],
}

ARCHIVE = {
    "$archiver": "NSKeyedArchiver",
    "$version": 100000,
    "$top": {"root": plistlib.UID(1)},
    "$objects": [
        "$null",
        {"$class": plistlib.UID(4), "title": plistlib.UID(2), "count": plistlib.UID(3), "tags": plistlib.UID(5)},
        "Weekly report",
        42,
        {"$classname": "Report", "$classes": ["Report", "NSObject"]},
        {"$class": plistlib.UID(6), "NS.objects": [plistlib.UID(2), plistlib.UID(300), plistlib.UID(70000)]},
        {"$classname": "NSArray", "$classes": ["NSArray", "NSObject"]},
    ],
}


def bplist(objects, top, ref_size=1, offset_size=1):
    """A binary plist from already-encoded objects."""
    out = bytearray(b"bplist00")
    offsets = []
    for o in objects:
        offsets.append(len(out))
        out += o
    table = len(out)
    fmt = {1: "B", 2: "H", 4: "L", 8: "Q"}[offset_size]
    for off in offsets:
        out += struct.pack(">" + fmt, off)
    out += struct.pack(">6xBBQQQ", offset_size, ref_size, len(objects), top, table)
    return bytes(out)


def ascii_obj(s):
    b = s.encode("ascii")
    assert len(b) < 15
    return bytes([0x50 | len(b)]) + b


def main():
    put("Info.plist", INFO)
    put("com.example.backup.plist", LAUNCHD)
    put("edges.plist", EDGES)
    put("bom.plist", BOM)
    put("com.example.cafenotes.plist", plistlib.dumps(PREFS, fmt=plistlib.FMT_BINARY, sort_keys=False))
    put("Info.binary.plist", plistlib.dumps(plistlib.loads(INFO.encode()), fmt=plistlib.FMT_BINARY))
    put("report.archive", plistlib.dumps(ARCHIVE, fmt=plistlib.FMT_BINARY))
    put("prefs.xml.plist", plistlib.dumps(PREFS, sort_keys=False).replace(b"\t", b"    "))

    # Shared references: two keys name the same array object, and the
    # array holds the same string twice by reference.
    objs = [
        bytes([0xD3, 1, 2, 3, 4, 4, 5]),          # 0: dict of 3
        ascii_obj("left"),                         # 1
        ascii_obj("right"),                        # 2
        ascii_obj("both"),                         # 3
        bytes([0xA3, 6, 6, 7]),                    # 4: array of 3
        bytes([0xA0]),                             # 5: empty array
        ascii_obj("shared"),                       # 6
        bytes([0x10, 9]),                          # 7
    ]
    put("shared.bplist", bplist(objs, 0))

    # Things plistlib reads but its own writer would refuse or never make:
    # an int key, None, a 4-byte real, a 16-byte int, UIDs, a 2-byte
    # length, a utf-16 string with a surrogate pair, refs of 2 bytes.
    long = "x" * 20
    objs = [
        bytes([0xD6]) + struct.pack(">12H", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13),  # 0
        ascii_obj("none"),                                      # 1
        ascii_obj("f32"),                                       # 2
        ascii_obj("i128"),                                      # 3
        ascii_obj("uid"),                                       # 4
        ascii_obj("long"),                                      # 5
        ascii_obj("utf16"),                                     # 6
        bytes([0x00]),                                          # 7
        bytes([0x22]) + struct.pack(">f", 0.1),                 # 8
        bytes([0x14]) + (2 ** 64 - 1).to_bytes(16, "big", signed=True),  # 9
        bytes([0xA2, 0, 12, 0, 14]),                            # 10: array refs 12, 14 (2-byte refs)
        bytes([0x5F, 0x10, len(long)]) + long.encode(),        # 11
        bytes([0x80, 7]),                                       # 12: UID(7)
        bytes([0x64]) + "é🚀".encode("utf-16be") + b"",        # 13: 3 utf-16 units? set below
        bytes([0x81, 0x01, 0x2C]),                              # 14: UID(300)
    ]
    objs[13] = bytes([0x63]) + "é🚀".encode("utf-16be")
    put("odd.bplist", bplist(objs, 0, ref_size=2))

    # An int used as a dict key: plistlib loads it, and dumps refuses it.
    objs = [bytes([0xD1, 1, 2]), bytes([0x10, 5]), ascii_obj("five")]
    put("intkey.bplist", bplist(objs, 0))

    # A string with a control character: fine in binary, refused in XML.
    objs = [bytes([0xA1, 1]), bytes([0x53]) + b"a\x01b"]
    put("control.bplist", bplist(objs, 0))

    # A dict whose key is an array: unhashable, so InvalidFileException.
    objs = [bytes([0xD1, 1, 2]), bytes([0xA0]), ascii_obj("v")]
    put("listkey.bplist", bplist(objs, 0))

    # Broken binary files.
    good = plistlib.dumps({"a": [1, 2, 3]}, fmt=plistlib.FMT_BINARY)
    put("truncated.bplist", good[:-5])
    put("badoffset.bplist", good[:-8] + struct.pack(">Q", 4096))
    put("badtoken.bplist", bplist([bytes([0xA1, 1]), bytes([0x70])], 0))
    put("badref.bplist", bplist([bytes([0xA1, 9])], 0))
    put("badascii.bplist", bplist([bytes([0x52]) + b"\xc3\xa9"], 0))
    put("short.bplist", b"bplist00\x00")

    put("notes.json", '{"not": "a plist"}\n')
    put("empty.plist", "")

    put("bad/key-in-array.plist",
        '<?xml version="1.0"?>\n<plist>\n<array>\n\t<string>a</string>\n\t<key>oops</key>\n</array>\n</plist>\n')
    put("bad/missing-value.plist",
        '<plist>\n<dict>\n\t<key>Label</key>\n\t<string>x</string>\n\t<key>Program</key>\n</dict>\n</plist>\n')
    put("bad/value-without-key.plist",
        '<plist>\n<dict>\n\t<key>a</key>\n\t<integer>1</integer>\n\t<string>stray</string>\n</dict>\n</plist>\n')
    put("bad/two-keys.plist",
        '<plist>\n<dict>\n\t<key>a</key>\n\t<key>b</key>\n\t<true/>\n</dict>\n</plist>\n')
    put("bad/entity.plist",
        '<?xml version="1.0"?>\n<!DOCTYPE plist [\n<!ENTITY boom "kaboom">\n]>\n<plist><string>&boom;</string></plist>\n')
    put("bad/int.plist", '<plist><array><integer>12</integer><integer>12a</integer></array></plist>\n')
    put("bad/neg-hex.plist", '<plist><integer>-0x10</integer></plist>\n')
    put("bad/hex.plist", '<plist><integer>0xZZ</integer></plist>\n')
    put("bad/real.plist", '<plist><dict><key>r</key><real>abc</real></dict></plist>\n')
    put("bad/padding.plist", '<plist><data>YWJ</data></plist>\n')
    put("bad/padding5.plist", '<plist><data>YWJjZ</data></plist>\n')
    put("ok/padding-quirks.plist",
        '<plist><array><data>YQ==YQ==</data><data>Y=Q==</data><data>YQ=a=</data><data>!!YWJj</data><data>YWJj====</data></array></plist>\n')
    put("ok/overflow.plist", '<plist><array><integer>-9999999999999999999</integer><integer>18446744073709551616</integer></array></plist>\n')
    put("ok/roots.plist", '<plist><string>first</string><string>second</string></plist>\n')
    put("ok/bare.plist", '<plist version="1.0"><string>just a string</string></plist>\n')

    files = [
        "Info.plist", "com.example.backup.plist", "edges.plist", "bom.plist",
        "com.example.cafenotes.plist", "Info.binary.plist", "report.archive",
        "prefs.xml.plist", "shared.bplist", "odd.bplist", "intkey.bplist",
        "control.bplist", "ok/padding-quirks.plist", "ok/overflow.plist",
        "ok/roots.plist", "ok/bare.plist",
    ]
    bad = [
        "listkey.bplist", "truncated.bplist", "badoffset.bplist", "badtoken.bplist",
        "badref.bplist", "badascii.bplist", "short.bplist", "notes.json", "empty.plist",
        "bad/key-in-array.plist", "bad/missing-value.plist", "bad/value-without-key.plist",
        "bad/two-keys.plist", "bad/entity.plist", "bad/int.plist", "bad/hex.plist",
        "bad/real.plist", "bad/neg-hex.plist", "bad/padding.plist", "bad/padding5.plist",
    ]
    jobs = []
    for f in files:
        jobs.append(["load", f])
        jobs.append(["xml", f])
        jobs.append(["bin", f])
    for f in ["com.example.cafenotes.plist", "edges.plist", "report.archive", "prefs.xml.plist", "shared.bplist"]:
        jobs.append(["xml", f, "sort_keys=0"])
        jobs.append(["bin", f, "sort_keys=0"])
    jobs.append(["xml", "intkey.bplist", "skipkeys=1"])
    jobs.append(["bin", "intkey.bplist", "skipkeys=1"])
    jobs.append(["bin", "intkey.bplist", "sort_keys=0"])
    jobs.append(["bin", "intkey.bplist", "sort_keys=0", "skipkeys=1"])
    for f in ["Info.plist", "edges.plist", "com.example.cafenotes.plist", "odd.bplist", "report.archive"]:
        jobs.append(["roundtrip", f])
    for f in bad:
        jobs.append(["load", f])
    for f in ["com.example.cafenotes.plist", "Info.plist", "report.archive", "edges.plist"]:
        jobs.append(["get", f, "FontSize"])
    jobs.append(["get", "Info.plist", "CFBundleURLTypes", "0", "CFBundleURLSchemes", "1"])
    jobs.append(["get", "Info.plist", "NSAppTransportSecurity", "NSExceptionDomains", "sync.example.com"])
    jobs.append(["get", "com.example.backup.plist", "StartCalendarInterval", "1", "Weekday"])
    jobs.append(["get", "com.example.backup.plist", "ProgramArguments", "9"])
    jobs.append(["get", "com.example.cafenotes.plist", "TrialEnds"])
    jobs.append(["get", "com.example.cafenotes.plist", "Theme", "Dark", "Accent", "x"])
    jobs.append(["get", "report.archive", "$objects", "1", "title"])
    with open(os.path.join(D, "jobs.tsv"), "w", encoding="utf-8") as f:
        for j in jobs:
            f.write("\t".join(j) + "\n")


main()
