# Writes data/: jobs.tsv, the calls and programs mini_mimetypes runs, and
# the mime.types files and inputs they read. The mime.types files are
# written here by hand, in the format the media-types, Apache and nginx
# packages use.
import os

FILES = {}


def put(path, text):
    FILES[path] = text


# ------------------------------------------------------------ mime.types files

put("system/mime.types", """###############################################################
#
#  Media types and the extensions that stand for them: a type on
#  the left, then zero or more extensions. A '#' that starts a word
#  starts a comment.
#
###############################################################

application/atom+xml\t\t\t\tatom
application/epub+zip\t\t\t\tepub
application/geo+json\t\t\t\tgeojson
application/gzip\t\t\t\tgz
application/javascript\t\t\t\tjs mjs
application/json\t\t\t\tjson map
application/ld+json\t\t\t\tjsonld
application/manifest+json\t\t\twebmanifest
application/msword\t\t\t\tdoc dot
application/octet-stream\t\t\tbin deb dmg iso img msi msp msm
application/pdf\t\t\t\t\tpdf
application/pgp-signature\t\t\tasc sig
application/rss+xml\t\t\t\trss
application/rtf\t\t\t\t\trtf
application/sql\t\t\t\t\tsql
application/toml\t\t\t\ttoml
application/vnd.android.package-archive\tapk
application/vnd.ms-excel\t\t\txls xlb xlt
application/vnd.ms-fontobject\t\t\teot
application/vnd.oasis.opendocument.text\todt
application/vnd.oasis.opendocument.spreadsheet\tods
application/vnd.openxmlformats-officedocument.presentationml.presentation pptx
application/vnd.openxmlformats-officedocument.spreadsheetml.sheet\txlsx
application/vnd.openxmlformats-officedocument.wordprocessingml.document\tdocx
application/wasm\t\t\t\twasm
application/x-7z-compressed\t\t\t7z
application/x-bittorrent\t\t\ttorrent
application/x-debian-package\t\t\tdeb udeb
application/x-httpd-php\t\t\t\tphtml pht php
application/x-ruby\t\t\t\trb
application/x-sh\t\t\t\tsh
application/x-sqlite3\t\t\t\tsqlite sqlite3 db
application/x-tar\t\t\t\ttar
application/x-x509-ca-cert\t\t\tcrt der pem
application/x-xpinstall\t\t\t\txpi
application/xhtml+xml\t\t\t\txhtml xht
application/xml\t\t\t\t\txml xsd
application/yaml\t\t\t\tyaml yml
application/zip\t\t\t\t\tzip
application/zstd\t\t\t\tzst

# audio
audio/flac\t\t\t\t\tflac
audio/midi\t\t\t\t\tmid midi kar
audio/mpeg\t\t\t\t\tmpga mpega mp2 mp3 m4a
audio/ogg\t\t\t\t\toga ogg opus spx
audio/x-wav\t\t\t\t\twav
audio/webm\t\t\t\t\tweba

# fonts
font/otf\t\t\t\t\totf
font/ttf\t\t\t\t\tttf
font/woff\t\t\t\t\twoff
font/woff2\t\t\t\t\twoff2

# images
image/avif\t\t\t\t\tavif
image/gif\t\t\t\t\tgif
image/jpeg\t\t\t\t\tjpeg jpg jpe
image/jxl\t\t\t\t\tjxl
image/png\t\t\t\t\tpng
image/svg+xml\t\t\t\t\tsvg svgz
image/tiff\t\t\t\t\ttiff tif
image/vnd.microsoft.icon\t\t\tico
image/webp\t\t\t\t\twebp

# text
text/calendar\t\t\t\t\tics icz
text/css\t\t\t\t\tcss
text/csv\t\t\t\t\tcsv
text/html\t\t\t\t\thtml htm shtml
text/markdown\t\t\t\t\tmd markdown
text/plain\t\t\t\t\tasc txt text pot brf srt log
text/tab-separated-values\t\t\ttsv
text/vcard\t\t\t\t\tvcf vcard
text/x-c++src\t\t\t\t\tc++ cpp cxx cc
text/x-csrc\t\t\t\t\tc
text/x-csharp\t\t\t\t\tcs c#
text/x-diff\t\t\t\t\tdiff patch
text/x-go\t\t\t\t\tgo
text/x-java\t\t\t\t\tjava
text/x-python\t\t\t\t\tpy
text/x-rust\t\t\t\t\trs

# video
video/mp4\t\t\t\t\tmp4
video/mpeg\t\t\t\t\tmpeg mpg mpe
video/quicktime\t\t\t\t\tqt mov
video/webm\t\t\t\t\twebm
video/x-matroska\t\t\t\tmpv mkv

# types with no extension: read, but they add nothing
application/vnd.kara-test+json
multipart/form-data
message/rfc822\t\t\t\t\teml # mail saved from a client
""")

put("apache/mime.types", """# This file maps Internet media types to unique file extension(s).
# Apache's copy, trimmed. Where it disagrees with the system file,
# it is read later and wins.
#
# MIME type (lowercased)\t\t\tExtensions
# ============================================\t==========
application/ecmascript\t\t\t\tes ecma
application/java-archive\t\t\tjar
application/vnd.apple.installer+xml\t\tmpkg
application/vnd.apple.mpegurl\t\t\tm3u8
application/x-msdownload\t\t\texe dll com bat msi
text/javascript\t\t\t\t\tjs
text/x-asm\t\t\t\t\ts asm
text/x-fortran\t\t\t\t\tf for f77 f90
text/x-pascal\t\t\t\t\tp pas
text/x-vcalendar\t\t\t\tvcs
video/mp2t\t\t\t\t\tts
video/x-flv\t\t\t\t\tflv
Application/X-Shockwave-Flash\t\tswf
application/x-photoshop\t\t\tPSD
""")

put("local/mime.types", """# Site-local types, read with strict=False so they only show up for
# a lenient guess.
application/x-kara-source\tkara
application/x-ndjson\tndjson jsonl
text/x-dotenv\tenv
image/x-portable-graymap\tpgm\t# overrides nothing: strict is separate
  text/x-indented    indented   # leading blanks are fine
\ttext/x-tabbed\ttabbed
#text/x-commented commented
text/x-hash-in-word\thash#word not#comment # but this is
text/x-only-comment # nothing after the type
""")

put("broken/odd.types", """text/x-crlf crlf\r
text/x-formfeed\x0cff
text/x-vtab\x0bvt
text/x-nbsp\xa0nbsp
text/x-dup dupe
text/x-dup2 dupe
text/x-dup dupe dupe2
""")

put("nginx/mime.types", """
types {
    text/html                                        html htm shtml;
    text/css                                         css;
    text/xml                                         xml;
    image/gif                                        gif;
    image/jpeg                                       jpeg jpg;
    application/javascript                           js;
    application/atom+xml                             atom;
    application/rss+xml                              rss;

    text/mathml                                      mml;
    text/plain                                       txt;
    text/vnd.sun.j2me.app-descriptor                 jad;
    text/vnd.wap.wml                                 wml;
    text/x-component                                 htc;

    image/avif                                       avif;
    image/png                                        png;
    image/svg+xml                                    svg svgz;
    image/tiff                                       tif tiff;
    image/vnd.wap.wbmp                               wbmp;
    image/webp                                       webp;
    image/x-icon                                     ico;
    image/x-jng                                      jng;
    image/x-ms-bmp                                   bmp;

    font/woff                                        woff;
    font/woff2                                       woff2;

    application/java-archive                         jar war ear;
    application/json                                 json;
    application/mac-binhex40                         hqx;
    application/msword                               doc;
    application/pdf                                  pdf;
    application/postscript                           ps eps ai;
    application/rtf                                  rtf;
    application/vnd.apple.mpegurl                    m3u8;
    application/vnd.ms-excel                         xls;
    application/vnd.ms-fontobject                    eot;
    application/vnd.ms-powerpoint                    ppt;
    application/wasm                                 wasm;
    application/x-7z-compressed                      7z;
    application/x-perl                               pl pm;
    application/x-x509-ca-cert                       der pem crt;
    application/xhtml+xml                            xhtml;
    application/zip                                  zip;

    application/octet-stream                         bin exe dll;
    application/octet-stream                         deb;
    application/octet-stream                         dmg;
    application/octet-stream                         iso img;

    audio/midi                                       mid midi kar;
    audio/mpeg                                       mp3;
    audio/ogg                                        ogg;
    audio/x-m4a                                      m4a;

    video/mp2t                                       ts;
    video/mp4                                        mp4;
    video/mpeg                                       mpeg mpg;
    video/quicktime                                  mov;
    video/webm                                       webm;
    video/x-flv                                      flv;
    video/x-msvideo                                  avi;
}
""")

# ------------------------------------------------------------ jobs

J = []


def job(name, *lines):
    J.append("job\t" + name)
    for l in lines:
        J.append(l)


# Calls: <op>\t<args...>. A '\\xNN' in an argument is that character.
job("guess_type on paths",
    "type\t1\tindex.html",
    "type\t1\tREADME",
    "type\t1\tREADME.md",
    "type\t1\tphoto.JPG",
    "type\t1\tPHOTO.Jpeg",
    "type\t1\tarchive.tar.gz",
    "type\t1\tarchive.tgz",
    "type\t1\tarchive.TGZ",
    "type\t1\tarchive.tar.GZ",
    "type\t1\tbackup.tar.bz2",
    "type\t1\tbackup.tbz2",
    "type\t1\tlogs.txz",
    "type\t1\tdrawing.svgz",
    "type\t1\tdata.json.br",
    "type\t1\tdata.json.Z",
    "type\t1\tdata.json.z",
    "type\t1\tfile.gz",
    "type\t1\t.gz",
    "type\t1\tx.gz.gz",
    "type\t1\t.bashrc",
    "type\t1\t..html",
    "type\t1\t...",
    "type\t1\tfile.",
    "type\t1\tdir.d/file",
    "type\t1\tdir.d/.html",
    "type\t1\t/var/www/site/app.min.js",
    "type\t1\tC:\\\\Users\\\\me\\\\report.pdf",
    "type\t1\tc:report.pdf",
    "type\t1\tnotes.MD",
    "type\t1\tclip.mid",
    "type\t0\tclip.mid",
    "type\t1\tpicture.jpg",
    "type\t0\tpicture.jpg",
    "type\t0\tpicture.pict",
    "type\t1\tpicture.pict",
    "type\t0\tdoc.rtf",
    "type\t1\tunknown.qqq",
    "type\t0\tunknown.qqq",
    "type\t1\tmodule.wasm",
    "type\t1\tstyle.css.map",
    "type\t1\tarchive.tar.zst",
    "type\t1\tsound.WAV",
    "type\t1\t",
)

job("guess_type on URLs",
    "type\t1\thttps://example.com/img/logo.png",
    "type\t1\thttps://example.com/img/logo.png?v=3",
    "type\t1\thttps://example.com/img/logo.png#top",
    "type\t1\thttps://example.com/download?file=report.pdf",
    "type\t1\thttps://example.com/page.html;jsessionid=abc123",
    "type\t1\thttps://example.com/a;b/page.html",
    "type\t1\tftp://ftp.example.org/pub/linux.tar.gz",
    "type\t1\tfile:///home/me/Music/song.mp3",
    "type\t1\thttps://example.com",
    "type\t1\thttps://example.com/",
    "type\t1\thttps://example.com/archive.tgz",
    "type\t1\thttps://cdn.example.com/fonts/Inter.WOFF2",
    "type\t1\tHTTPS://EXAMPLE.COM/INDEX.HTM",
    "type\t1\ts3://bucket/key/data.csv",
    "type\t1\tmailto:someone@example.com",
    "type\t1\tnews:comp.lang.python",
    "type\t1\turn:isbn:0451450523.pdf",
    "type\t1\thttp://[::1]:8080/status.json",
    "type\t1\thttp://[2001:db8::7]/x.png",
    "type\t1\thttp://[::1/x.png",
    "type\t1\thttp://::1]/x.png",
    "type\t1\thttp://host]/x.png",
    "type\t1\thttp://x[::1]/x.png",
    "type\t1\thttp://[::1]x/x.png",
    "type\t1\thttp://[127.0.0.1]/x.png",
    "type\t1\thttp://[v1.fe]/x.png",
    "type\t1\thttp://[vz.fe]/x.png",
    "type\t1\thttp://[::g]/x.png",
    "type\t1\thttp://user@[::1]:80/x.png",
    "type\t1\t//cdn.example.com/lib.js",
    "type\t1\t\\x01\\x02 https://example.com/a.png",
    "type\t1\thttps://exa\\x09mple.com/a.p\\x0ang",
    "type\t1\t1http://example.com/a.png",
    "type\t1\tht+tp.v-1://example.com/a.png",
    "type\t1\tht_tp://example.com/a.png",
    "type\t1\tx:a.png",
    "type\t1\t:a.png",
    "type\t1\tpath/with:colon/a.png",
    "type\t1\thttps://example.com/a.png?x=1#frag.html",
    "type\t1\thttps://example.com/a#b?c.html",
    "type\t1\tsip:alice@example.com;transport=tcp",
)

job("data URLs",
    "type\t1\tdata:,Hello%2C%20World!",
    "type\t1\tdata:text/plain;base64,SGVsbG8=",
    "type\t1\tdata:image/png;base64,iVBORw0KGgo=",
    "type\t1\tdata:text/html,<b>hi</b>",
    "type\t1\tdata:text/html;charset=utf-8,<b>hi</b>",
    "type\t1\tdata:application/json;x=1;y=2,{}",
    "type\t1\tdata:image/svg+xml,<svg/>",
    "type\t1\tdata:;base64,AAAA",
    "type\t1\tdata:charset=utf-8,x",
    "type\t1\tdata:texthtml,x",
    "type\t1\tdata:a=b/c,x",
    "type\t1\tdata:IMAGE/PNG,x",
    "type\t1\tdata:image/png",
    "type\t1\tDATA:image/gif,x",
    "type\t1\tdata:image/gif;a,b;c,d",
    "type\t1\tdata:image/gif?x=1,d",
    "type\t1\tdata:image/gif#a,b",
    "type\t1\tdata://image/gif,x",
)

job("guess_file_type",
    "ftype\t1\treport.pdf",
    "ftype\t1\thttps://example.com/a.png?x=1",
    "ftype\t1\tdata:image/png,x",
    "ftype\t1\tarchive.tar.gz",
    "ftype\t0\tpicture.jpg",
    "ftype\t1\t/tmp/a.b/c",
    "ftype\t1\tsong.mp3#1",
)

job("guess_extension and guess_all_extensions",
    "ext\t1\ttext/html",
    "ext\t1\tTEXT/HTML",
    "ext\t1\ttext/plain",
    "ext\t1\timage/jpeg",
    "ext\t1\tapplication/octet-stream",
    "ext\t1\taudio/midi",
    "ext\t0\taudio/midi",
    "ext\t1\timage/jpg",
    "ext\t0\timage/jpg",
    "ext\t1\ttext/x-nothing",
    "ext\t1\t",
    "ext\t1\ttext/javascript",
    "ext\t1\tapplication/xml",
    "exts\t1\ttext/plain",
    "exts\t1\timage/jpeg",
    "exts\t0\timage/jpeg",
    "exts\t1\tapplication/rtf",
    "exts\t0\tapplication/rtf",
    "exts\t1\ttext/rtf",
    "exts\t1\tvideo/mpeg",
    "exts\t1\tapplication/vnd.ms-powerpoint",
    "exts\t1\tmessage/rfc822",
    "exts\t1\tapplication/x-troff",
    "exts\t1\tno/such",
)

job("add_type",
    "add\t1\tapplication/x-kara\t.kara",
    "type\t1\tmain.kara",
    "ext\t1\tapplication/x-kara",
    "add\t1\tapplication/x-kara-lib\t.kara",
    "type\t1\tmain.kara",
    "exts\t1\tapplication/x-kara",
    "exts\t1\tapplication/x-kara-lib",
    "add\t1\tapplication/x-kara\t.kara",
    "exts\t1\tapplication/x-kara",
    "add\t1\tapplication/x-kara\t.kr",
    "exts\t1\tapplication/x-kara",
    "add\t0\ttext/x-lenient\t.lnt",
    "type\t1\tx.lnt",
    "type\t0\tx.lnt",
    "add\t1\t\t.nothing",
    "type\t1\tx.nothing",
    "add\t1\ttext/x-upper\t.UPPER",
    "type\t1\tx.UPPER",
    "type\t1\tx.upper",
    "add\t1\ttext/x-nodot\tnodot",
    "type\t1\tx.nodot",
    "type\t1\txnodot",
    "add\t1\tText/X-Mixed\t.mixed",
    "type\t1\tx.mixed",
    "ext\t1\tText/X-Mixed",
    "ext\t1\ttext/x-mixed",
    "add\t1\ttext/x-gzip-ext\t.gz",
    "type\t1\tplain.gz",
    "type\t1\tplain.tar.gz",
    "add\t1\timage/png\t.png",
    "exts\t1\timage/png",
    "add\t1\timage/x-png\t.png",
    "type\t1\tx.png",
    "exts\t1\timage/png",
    "ext\t1\timage/png",
)

job("reading mime.types files",
    "read\t1\tsystem/mime.types",
    "type\t1\tapp.js",
    "ext\t1\ttext/javascript",
    "ext\t1\tapplication/javascript",
    "exts\t1\tapplication/javascript",
    "type\t1\tpkg.deb",
    "exts\t1\tapplication/octet-stream",
    "exts\t1\tapplication/x-debian-package",
    "type\t1\tnotes.log",
    "type\t1\tProgram.cs",
    "type\t1\tProgram.c#",
    "type\t1\tmail.eml",
    "type\t1\tcomment",
    "ext\t1\ttext/plain",
    "exts\t1\ttext/plain",
    "type\t1\tmovie.mkv",
    "type\t1\tsong.m4a",
    "type\t1\tsong.ogg",
    "type\t1\tfont.woff2",
    "type\t1\tkey.pem",
    "type\t1\tdb.sqlite3",
    "type\t1\tconfig.yml",
    "type\t1\tarchive.zst",
    "type\t1\tdump.tar.zst",
    "read\t1\tapache/mime.types",
    "type\t1\tapp.js",
    "exts\t1\ttext/javascript",
    "exts\t1\tapplication/javascript",
    "type\t1\tsetup.exe",
    "type\t1\tinstall.msi",
    "type\t1\tclip.ts",
    "type\t1\tmovie.swf",
    "ext\t1\tapplication/x-shockwave-flash",
    "ext\t1\tApplication/X-Shockwave-Flash",
    "type\t1\tlayers.psd",
    "type\t1\tlayers.PSD",
    "exts\t1\tapplication/x-photoshop",
    "read\t0\tlocal/mime.types",
    "type\t1\tmain.kara",
    "type\t0\tmain.kara",
    "type\t0\tevents.jsonl",
    "type\t0\t.env",
    "type\t0\tprod.env",
    "type\t0\timage.pgm",
    "type\t1\timage.pgm",
    "type\t0\tx.indented",
    "type\t0\tx.tabbed",
    "type\t0\tx.commented",
    "type\t0\tx.hash#word",
    "type\t0\tx.not#comment",
    "type\t0\tx.but",
    "exts\t0\ttext/x-hash-in-word",
    "exts\t0\ttext/x-only-comment",
    "read\t1\tbroken/odd.types",
    "type\t1\tx.crlf",
    "type\t1\tx.ff",
    "type\t1\tx.vt",
    "type\t1\tx.nbsp",
    "type\t1\tx.dupe",
    "type\t1\tx.dupe2",
    "exts\t1\ttext/x-dup",
    "exts\t1\ttext/x-dup2",
    "read\t1\tno/such.types",
    "type\t1\tstill.ok.png",
)

job("read_mime_types",
    "readmt\tlocal/mime.types",
    "readmt\tapache/mime.types",
    "readmt\tbroken/odd.types",
    "readmt\tno/such.types",
    "readmt\tnginx/mime.types",
)

job("the module-level database",
    "init",
    "gtype\t1\tapp.js",
    "gtype\t1\tsetup.exe",
    "gext\t1\ttext/javascript",
    "gadd\t1\ttext/x-added\t.added",
    "gtype\t1\tx.added",
    "init\tlocal/mime.types",
    "gtype\t1\tx.added",
    "gtype\t1\tmain.kara",
    "gtype\t0\tmain.kara",
    "init",
    "gtype\t1\tx.added",
    "gtype\t0\tmain.kara",
    "init\tlocal/mime.types",
    "gtype\t1\tmain.kara",
    "gadd\t0\ttext/x-added\t.added",
    "init\tapache/mime.types\tno/such.types",
    "gtype\t1\tx.added",
    "gtype\t0\tx.added",
    "maps",
)

job("the instance's own files",
    "new\tapache/mime.types",
    "type\t1\tapp.js",
    "type\t1\tsetup.exe",
    "new0\tlocal/mime.types",
    "type\t1\tmain.kara",
    "type\t0\tmain.kara",
    "new\tno/such.types",
)

# python -m mimetypes
for args in [
    ["index.html"],
    ["index.html", "archive.tar.gz", "unknown.qqq", "a.mid"],
    ["-l", "a.mid", "x.jpg"],
    ["--lenient", "a.mid"],
    ["--len", "a.mid"],
    ["-e", "text/html", "image/jpeg", "no/such", "audio/midi"],
    ["-el", "audio/midi", "image/jpg"],
    ["-le", "image/jpg"],
    ["--extension", "--lenient", "image/jpg"],
    ["--ext", "application/javascript"],
    ["-e", "--", "-l", "text/css"],
    ["index.html", "-e", "text/css"],
    ["-", "index.html"],
    ["-x"],
    ["-lx", "a.mid"],
    ["--extensions"],
    ["--e"],
    ["--le", "a.mid"],
    ["--lenient=1", "a.mid"],
    ["--=x"],
    ["-:"],
    ["-h"],
    ["--help", "index.html"],
    ["--he"],
    [],
    ["data:text/csv,a,b", "https://x.org/a.svgz"],
    ["text/javascript"],
    ["-e", "text/javascript", "application/javascript"],
]:
    J.append("cli\t" + "\t".join(args) if args else "cli")

for p in ["server", "nginx", "uploads", "objstore", "mail", "negotiate",
          "cdnlog", "inventory"]:
    J.append("program\t" + p)

put("jobs.tsv", "\n".join(J) + "\n")

# ------------------------------------------------------------ program inputs

put("server/requests.txt", """# what a static file server answers for each request path, as
# http.server's SimpleHTTPRequestHandler picks Content-type
/
/index.html
/about/
/css/site.css
/js/app.min.js
/js/app.min.js.map
/img/hero.webp
/img/LOGO.PNG
/img/icon.svg
/downloads/release-2.4.0.tar.gz
/downloads/release-2.4.0.tar.GZ
/downloads/release-2.4.0.tgz
/downloads/release-2.4.0.tar.bz2
/downloads/release-2.4.0.tar.xz
/downloads/legacy.tar.Z
/downloads/legacy.tar.z
/downloads/checksums.txt
/downloads/checksums.txt.asc
/fonts/Inter.woff2
/data/export.csv
/data/report.xlsx
/data/archive.zst
/feed.rss
/sitemap.xml
/robots.txt
/.well-known/security.txt
/.htaccess
/Makefile
/video/intro.webm
/video/intro.MKV
/app.wasm
/notes.md
""")

put("server/precompressed.txt", """# files on disk; a .br or .gz next to a file is a precompressed copy
index.html
index.html.br
index.html.gz
css/site.css
css/site.css.gz
js/app.min.js
js/app.min.js.br
img/hero.webp
img/icon.svg
img/icon.svgz
data/export.csv
data/export.csv.gz
fonts/Inter.woff2
""")

put("server/accept.txt", """# request path, then the Accept-Encoding header
/index.html\tbr, gzip, deflate
/index.html\tgzip
/index.html\tidentity
/css/site.css\tbr, gzip
/css/site.css\tbr
/js/app.min.js\tgzip, br
/img/icon.svg\tgzip
/img/hero.webp\tbr, gzip
/data/export.csv\t*
/fonts/Inter.woff2\tbr, gzip
""")

put("uploads/uploads.tsv", """# file name, the Content-Type the browser sent, bytes
avatar.png\timage/png\t48211
avatar.jpg\timage/png\t51002
resume.pdf\tapplication/pdf\t220140
resume.PDF\tapplication/pdf\t220140
invoice.pdf.exe\tapplication/pdf\t90112
holiday.HEIC\timage/heic\t2210331
budget.xlsx\tapplication/vnd.openxmlformats-officedocument.spreadsheetml.sheet\t30122
budget.xls\tapplication/vnd.ms-excel\t40960
notes.txt\ttext/plain; charset=utf-8\t1200
notes\ttext/plain\t1200
script.sh\ttext/x-sh\t310
logo.svg\timage/svg+xml\t8122
photo.jpeg\timage/jpeg\t3021133
photo.jpe\timage/jpeg\t3021133
huge.png\timage/png\t31457281
data.json\tapplication/json\t512
archive.tar.gz\tapplication/gzip\t1048576
archive.tgz\tapplication/x-gzip\t1048576
.png\timage/png\t100
clip.mov\tvideo/quicktime\t9000000
""")

put("uploads/policy.conf", """# the types this upload form takes, and the size limit for each
image/png 10485760
image/jpeg 10485760
image/gif 5242880
image/webp 10485760
image/heic 20971520
application/pdf 26214400
text/plain 1048576
text/csv 1048576
application/vnd.openxmlformats-officedocument.spreadsheetml.sheet 26214400
""")

put("objstore/manifest.txt", """# local files to upload to an object store, with the metadata each
# object gets
site/index.html
site/index.html.gz
site/assets/app.js
site/assets/app.js.br
site/assets/app.css
site/assets/fonts/Inter.woff2
site/assets/fonts/Inter.ttf
site/assets/fonts/Inter.eot
site/img/hero.avif
site/img/hero.jpg
site/img/favicon.ico
site/docs/guide.pdf
site/docs/guide.epub
site/docs/handbook.docx
site/data/prices.json
site/data/prices.json.gz
site/data/stations.geojson
site/data/events.ndjson
site/feeds/atom.xml
site/feeds/podcast.rss
site/media/episode-12.mp3
site/media/episode-12.ogg
site/media/trailer.mp4
site/media/subtitles.vtt
site/manifest.webmanifest
site/sw.js
site/LICENSE
site/CHANGELOG
site/backup.tar.gz
""")

put("mail/attachments.txt", """# files attached to an outgoing message
Quarterly report.pdf
team-photo.JPG
budget.xlsx
slides.pptx
logs.tar.gz
notes.txt
diagram.svg
recording.wav
contract.docx
data.csv.gz
README
font.otf
calendar.ics
contact.vcf
patch.diff
thesis.tex
""")

put("negotiate/variants.txt", """# the files a resource has; the server picks one for each Accept header
report\treport.html report.json report.pdf report.csv report.md
logo\tlogo.svg logo.png logo.webp logo.avif
feed\tfeed.rss feed.atom feed.json
""")

put("negotiate/requests.txt", """# resource, then the Accept header
report\ttext/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
report\tapplication/json
report\tapplication/json;q=0.5, text/csv
report\ttext/*;q=0.3, application/pdf;q=0.2
report\ttext/markdown;q=0, text/*;q=0.9
report\timage/png
report\t*/*
report\t
logo\timage/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
logo\timage/webp,*/*
logo\timage/png;q=1.0, image/svg+xml;q=0.9
logo\timage/*;q=0.5, image/svg+xml;q=0.5
feed\tapplication/atom+xml
feed\tapplication/rss+xml;q=0.9, application/atom+xml;q=0.9
feed\tapplication/feed+json, application/json;q=0.4
feed\ttext/plain
""")

put("cdnlog/access.log", """203.0.113.10 - - [20/Oct/2026:10:00:01 +0000] "GET /index.html HTTP/2.0" 200 5120
203.0.113.10 - - [20/Oct/2026:10:00:01 +0000] "GET /css/site.css HTTP/2.0" 200 18210
203.0.113.10 - - [20/Oct/2026:10:00:01 +0000] "GET /js/app.min.js?v=8f3a HTTP/2.0" 200 92012
203.0.113.11 - - [20/Oct/2026:10:00:02 +0000] "GET /img/hero.webp HTTP/2.0" 200 210334
203.0.113.11 - - [20/Oct/2026:10:00:02 +0000] "GET /img/thumbs/1.jpg HTTP/2.0" 200 12001
203.0.113.11 - - [20/Oct/2026:10:00:02 +0000] "GET /img/thumbs/2.JPG HTTP/2.0" 200 12890
203.0.113.12 - - [20/Oct/2026:10:00:03 +0000] "GET /fonts/Inter.woff2 HTTP/2.0" 200 98112
203.0.113.12 - - [20/Oct/2026:10:00:03 +0000] "GET /api/v1/items?page=2 HTTP/2.0" 200 3311
203.0.113.12 - - [20/Oct/2026:10:00:03 +0000] "GET /api/v1/items.json HTTP/2.0" 200 3311
203.0.113.13 - - [20/Oct/2026:10:00:04 +0000] "GET /downloads/app-2.4.0.dmg HTTP/1.1" 200 88120334
203.0.113.13 - - [20/Oct/2026:10:00:05 +0000] "GET /downloads/app-2.4.0.tar.gz HTTP/1.1" 200 20331002
203.0.113.14 - - [20/Oct/2026:10:00:05 +0000] "GET /video/intro.mp4 HTTP/1.1" 206 1048576
203.0.113.14 - - [20/Oct/2026:10:00:06 +0000] "GET /video/intro.mp4 HTTP/1.1" 206 1048576
203.0.113.14 - - [20/Oct/2026:10:00:06 +0000] "GET /video/intro.vtt HTTP/1.1" 200 2201
203.0.113.15 - - [20/Oct/2026:10:00:07 +0000] "GET /favicon.ico HTTP/1.1" 404 153
203.0.113.15 - - [20/Oct/2026:10:00:07 +0000] "GET /robots.txt HTTP/1.1" 200 68
203.0.113.16 - - [20/Oct/2026:10:00:08 +0000] "GET /wp-login.php HTTP/1.1" 404 153
203.0.113.16 - - [20/Oct/2026:10:00:08 +0000] "GET /.env HTTP/1.1" 404 153
203.0.113.16 - - [20/Oct/2026:10:00:08 +0000] "GET /backup.sql.gz HTTP/1.1" 404 153
203.0.113.17 - - [20/Oct/2026:10:00:09 +0000] "GET /docs/guide.pdf#page=4 HTTP/1.1" 200 1203344
203.0.113.17 - - [20/Oct/2026:10:00:10 +0000] "GET /docs/ HTTP/1.1" 200 4401
203.0.113.18 - - [20/Oct/2026:10:00:11 +0000] "HEAD /index.html HTTP/1.1" 200 0
203.0.113.18 - - [20/Oct/2026:10:00:11 +0000] "GET /feed.rss HTTP/1.1" 304 0
203.0.113.19 - - [20/Oct/2026:10:00:12 +0000] "GET /audio/ep12.mp3 HTTP/1.1" 200 41203398
203.0.113.19 - - [20/Oct/2026:10:00:12 +0000] "GET /audio/ep12.m4a HTTP/1.1" 200 39002110
203.0.113.20 - - [20/Oct/2026:10:00:13 +0000] "garbage line without a request"
203.0.113.21 - - [20/Oct/2026:10:00:14 +0000] "GET https://example.com/img/x.gif HTTP/1.1" 200 43
""")

put("inventory/files.txt", """# every file in a shared drive, with its size in bytes
Projects/website/index.htm 4120
Projects/website/style.CSS 2210
Projects/website/logo.jpe 30122
Projects/website/logo.jpeg 30122
Projects/website/banner.tif 2210443
Projects/website/script.mjs 3301
Projects/budget/2026.xls 50102
Projects/budget/2026.xlsx 41022
Projects/budget/notes.text 812
Projects/budget/minutes.doc 30021
Photos/IMG_0001.JPG 3021442
Photos/IMG_0002.HEIC 2210331
Photos/IMG_0003.heif 2310201
Photos/scan.pbm 1203
Music/track01.mp3 6102331
Music/track02.mp2 5102331
Music/track03.flac 30120443
Music/cover.bmp 921654
Videos/clip.qt 1210442
Videos/clip.mov 1210442
Videos/old.mpe 8120332
Archive/2019.tgz 120334112
Archive/2020.tar.bz2 98120112
Archive/2021.taz 77120331
Archive/mail.mbox 4012331
Archive/thumbs.db 12288
Code/main.rs 4401
Code/main.go 3301
Code/main.kara 2201
Code/build.ninja 1204
Code/Dockerfile 811
""")

for path, text in FILES.items():
    full = os.path.join("data", path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="") as f:
        f.write(text)
