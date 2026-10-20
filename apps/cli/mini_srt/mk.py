# Writes data/: subtitle files with the quirks real SRT files have, and
# jobs.tsv, the jobs oracle.py and mini_srt.kara run.
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def put(rel, text, encoding="utf-8", newline="\n"):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(text.replace("\n", newline).encode(encoding))


BASIC = """\
1
00:00:01,000 --> 00:00:03,500
It is a capital mistake to theorise
before one has data.

2
00:00:04,000 --> 00:00:06,250
<i>Insensibly one begins to twist facts</i>
to suit theories.

4
00:00:10,000 --> 00:00:12,000
{\\an8}You see, but you do not observe.

3
00:00:07,000 --> 00:00:09,900
The game is afoot, Watson!

5
00:01:02,003 --> 01:02:03,004
- Holmes?
- Yes?

"""

MESSY = """\
﻿1
00:00:01.500 --> 00:00:02.750
Dots instead of commas.

2
00:00:03,000  -->  00:00:04,000
Extra spaces around the arrow.

00:00:05,000 --> 00:00:06,000
No index at all.

12.5
00:00:07,000 - > 00:00:08,000 X1:100 X2:200 Y1:10 Y2:20
A fractional index and a position.

6
00:00:09：000 --> 00:00:10，500
全角の区切り。

7
00:00:11,000 --> 00:00:12
A missing millisecond field.

8
00:00:13,000 --> 00:00:14,000
A blank line

inside the content.

9
00:00:15,000 --> 00:00:16,000
No blank line at the end."""

GARBAGE = """\
1
00:00:01,000 --> 00:00:02,000
Before the junk.

this line is not a subtitle
neither is this one

2
00:00:03,000 --> 00:00:04,000
After the junk.

3
00:00:05,000 -> 00:00:06,000
A broken arrow.

4
00:00:07,000 --> 00:00:08,000
The last one.

"""

LEADING_JUNK = """\
WEBVTT

1
00:00:01,000 --> 00:00:02,000
A WebVTT header is not SRT.

"""

SKIPS = """\
1
00:00:01,000 --> 00:00:02,000
Kept.

2
00:00:03,000 --> 00:00:03,000
Zero length.

3
00:00:05,000 --> 00:00:04,000
Ends before it starts.

4
00:00:06,000 --> 00:00:07,000


5
00:00:08,000 --> 00:00:09,000

6
00:00:10,000 --> 00:00:11,000
Kept too.

"""

ENG = """\
1
00:00:01,000 --> 00:00:03,000
Where are you going?

2
00:00:04,000 --> 00:00:06,000
To Baker Street.

3
00:00:08,000 --> 00:00:09,500
Come at once if convenient.

4
00:00:12,000 --> 00:00:14,000
If inconvenient, come all the same.

"""

CHS = """\
1
00:00:01,200 --> 00:00:03,300
你要去哪里？

2
00:00:04,500 --> 00:00:06,100
去贝克街。

3
00:00:08,700 --> 00:00:09,400
方便的话请马上来。

4
00:00:13,000 --> 00:00:14,400
不方便也请来。

"""

MIXED = """\
1
00:00:01,000 --> 00:00:03,000
你好
Hello

2
00:00:04,000 --> 00:00:06,000
2023
Only a year.

3
00:00:07,000 --> 00:00:08,000
- 走吧
- Let's go.

4
00:00:09,000 --> 00:00:10,000
１２３
Holmes again.

5
00:00:11,000 --> 00:00:12,000
Nothing to see here.

"""

DUPES = """\
1
00:00:01,000 --> 00:00:02,000
Ring ring.

2
00:00:02,500 --> 00:00:03,500
Ring ring.

3
00:00:04,000 --> 00:00:05,000
Hello?

4
00:00:09,000 --> 00:00:10,000
Ring ring.

5
00:00:20,000 --> 00:00:21,000
Hello?

6
00:00:21,400 --> 00:00:22,000
Hello?

"""

LATIN = """\
1
00:00:01,000 --> 00:00:02,000
Un café, s'il vous plaît.

2
00:00:03,000 --> 00:00:04,000
Ça coûte trois euros… non, deux.

"""

TAGS = """\
1
00:00:01,000 --> 00:00:02,000
<i>Italic</i> and <b>bold</b>.

2
00:00:03,000 --> 00:00:04,000
<font color="#ffff00">Yellow</font> <<odd>> tags

3
00:00:05,000 --> 00:00:06,000
<i></i>

"""

LONG = """\
1
00:59:58,000 --> 01:00:01,000
Over the hour.

2
23:59:59,000 --> 24:00:01,500
Over the day.

3
100:00:00,000 --> 100:00:02,000
A hundred hours in.

4
00:00:00,000 --> 00:00:00,001
One millisecond.

"""


def srt_blocks(n):
    out = []
    for i in range(n):
        s = 2000 * i + 37 * (i % 7)
        e = s + 1500 + 11 * (i % 5)
        out.append(
            "%d\n%s --> %s\nLine %d of the long file.\n%s\n"
            % (i + 1, ts(s), ts(e), i + 1, "Second line." if i % 3 == 0 else "-")
        )
    return "\n".join(out) + "\n"


def ts(ms):
    return "%02d:%02d:%02d,%03d" % (ms // 3600000, ms // 60000 % 60, ms // 1000 % 60, ms % 1000)


def main():
    shutil.rmtree(DATA, ignore_errors=True)
    put("basic.srt", BASIC)
    put("messy.srt", MESSY, newline="\r\n")
    put("garbage.srt", GARBAGE)
    put("leading.srt", LEADING_JUNK)
    put("spaces.srt", "\n \n\t\n" + BASIC.split("\n\n")[0] + "\n\n")
    put("skips.srt", SKIPS)
    put("eng.srt", ENG)
    put("chs.srt", CHS)
    put("mixed.srt", MIXED)
    put("dupes.srt", DUPES)
    put("latin1.srt", LATIN.replace("…", "..."), encoding="latin-1")
    put("bom.srt", "﻿" + ENG)
    put("tags.srt", TAGS)
    put("long.srt", LONG)
    put("empty.srt", "")
    put("blank.srt", "\n\n  \n")
    put("many.srt", srt_blocks(60))
    put("inplace.srt", MESSY.replace("﻿", ""), newline="\r\n")
    jobs = [
        ["parse", "basic.srt"],
        ["parse", "messy.srt"],
        ["parse", "garbage.srt"],
        ["parse", "garbage.srt", "ignore"],
        ["parse", "leading.srt"],
        ["parse", "leading.srt", "ignore"],
        ["parse", "spaces.srt"],
        ["parse", "skips.srt"],
        ["parse", "long.srt"],
        ["parse", "empty.srt"],
        ["parse", "blank.srt"],
        ["compose", "basic.srt"],
        ["compose", "basic.srt", "reindex=no"],
        ["compose", "basic.srt", "start=100"],
        ["compose", "messy.srt", "strict=no", "reindex=no"],
        ["compose", "messy.srt", "eol=crlf"],
        ["compose", "skips.srt"],
        ["compose", "skips.srt", "reindex=no"],
        ["compose", "long.srt", "shift=-3725.5", "reindex=no"],
        ["compose", "long.srt", "shift=86400", "reindex=no"],
        ["ts", "01:23:04,000"],
        ["ts", "1:2:3"],
        ["ts", "00:00:01.5"],
        ["ts", "00:00:01,0005"],
        ["ts", "12：34：56，789"],
        ["ts", "00:01"],
        ["ts", "aa:bb:cc,ddd"],
        ["ts", "999:59:59,999"],
        ["legal", "foo"],
        ["legal", "\\nfoo\\n\\nbar\\n"],
        ["legal", "a\\n\\n\\n\\nb"],
        ["legal", "\\n"],
        ["legal", ""],
        ["tool", "normalise", "-i", "basic.srt"],
        ["tool", "normalise", "-i", "messy.srt"],
        ["tool", "normalise", "-i", "messy.srt", "--no-strict"],
        ["tool", "normalise", "-i", "garbage.srt"],
        ["tool", "normalise", "-i", "garbage.srt", "-c"],
        ["tool", "normalise", "-i", "skips.srt"],
        ["tool", "normalise", "-i", "bom.srt"],
        ["tool", "normalise", "-i", "bom.srt", "-e", "utf-8"],
        ["tool", "normalise", "-i", "latin1.srt", "-e", "latin-1"],
        ["tool", "normalise", "-i", "empty.srt"],
        ["tool", "normalise", "-i", "many.srt"],
        ["tool", "fixed-timeshift", "-i", "basic.srt", "--seconds", "2.5"],
        ["tool", "fixed-timeshift", "-i", "basic.srt", "--seconds", "-1.75"],
        ["tool", "fixed-timeshift", "-i", "basic.srt", "--seconds", "-5"],
        ["tool", "fixed-timeshift", "-i", "long.srt", "--seconds", "0.0005"],
        ["tool", "fixed-timeshift", "-i", "many.srt", "--seconds", "-30.1"],
        ["tool", "linear-timeshift", "-i", "basic.srt", "--f1", "00:00:01,000", "--t1", "00:00:01,000",
         "--f2", "00:00:02,000", "--t2", "00:00:03,000"],
        ["tool", "linear-timeshift", "-i", "many.srt", "--f1", "00:00:00,000", "--t1", "00:00:00,500",
         "--f2", "00:01:00,000", "--t2", "00:01:02,002"],
        ["tool", "linear-timeshift", "-i", "eng.srt", "--from-start", "00:00:01,000", "--to-start", "00:00:00,000",
         "--from-end", "00:00:12,000", "--to-end", "00:00:12,000"],
        ["tool", "linear-timeshift", "-i", "basic.srt", "--f1", "00:00:01,000", "--t1", "00:00:01,000",
         "--f2", "00:00:01,000", "--t2", "00:00:03,000"],
        ["tool", "deduplicate", "-i", "dupes.srt"],
        ["tool", "deduplicate", "-i", "dupes.srt", "-t", "500"],
        ["tool", "deduplicate", "-i", "dupes.srt", "-t", "0"],
        ["tool", "deduplicate", "-i", "dupes.srt", "--ms", "10000"],
        ["tool", "mux", "-i", "eng.srt", "-i", "chs.srt"],
        ["tool", "mux", "-i", "eng.srt", "-i", "chs.srt", "-t"],
        ["tool", "mux", "-i", "eng.srt", "-i", "chs.srt", "-t", "--no-time-matching"],
        ["tool", "mux", "-i", "eng.srt", "-i", "chs.srt", "--ms", "1000", "-w", "2"],
        ["tool", "mux", "-i", "eng.srt", "-i", "chs.srt", "--no-time-matching"],
        ["tool", "mux", "-i", "eng.srt", "-i", "chs.srt", "-i", "basic.srt", "-t"],
        ["tool", "lines-matching", "-i", "mixed.srt", "-f", "lambda x: x.isdigit()"],
        ["tool", "lines-matching", "-i", "mixed.srt", "-f", "lambda x: x.isdigit()", "-v"],
        ["tool", "lines-matching", "-i", "mixed.srt", "-f", "lambda x: any('一' <= c <= '鿿' for c in x)"],
        ["tool", "lines-matching", "-i", "mixed.srt", "-f", "lambda x: any('一' <= c <= '鿿' for c in x)", "-v"],
        ["tool", "lines-matching", "-i", "mixed.srt", "-f", "lambda x: 'Holmes' in x", "-s"],
        ["tool", "lines-matching", "-i", "basic.srt", "-f", "lambda x: x.startswith('-')", "-s", "-v"],
        ["tool", "lines-matching", "-i", "basic.srt", "-f", "lambda x: x.startswith('-')", "--no-strict"],
        ["tool", "process", "-i", "tags.srt", "-m", "re", "-f", 'lambda sub: re.sub("<[^<]+?>", "", sub)'],
        ["tool", "process", "-i", "basic.srt", "-m", "re", "-f", 'lambda sub: re.sub("<[^<]+?>", "", sub)'],
        ["tool", "process", "-i", "basic.srt", "-f", "lambda sub: sub.upper()"],
        ["tool", "process", "-i", "mixed.srt", "-f", 'lambda sub: sub.replace("\\n", " / ")'],
        ["tool", "process", "-i", "eng.srt", "-f", 'lambda sub: ""'],
        ["tool", "normalise", "-i", "inplace.srt", "-p"],
        ["parse", "inplace.srt"],
    ]
    with open(os.path.join(DATA, "jobs.tsv"), "w", encoding="utf-8") as f:
        for j in jobs:
            f.write("\t".join(j) + "\n")


main()
