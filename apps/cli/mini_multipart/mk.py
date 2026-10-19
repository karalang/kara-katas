# Writes data/: request bodies, raw HTTP requests and the job list.
import base64, json, os, quopri, zlib

os.makedirs("data/bodies", exist_ok=True)
os.makedirs("data/requests", exist_ok=True)
jobs = []


def job(**kw):
    jobs.append(kw)


def body(name, b):
    open("data/bodies/" + name, "wb").write(b)
    return name


def part(headers, data):
    h = b"".join(k.encode("latin-1") + b": " + v.encode("latin-1") + b"\r\n" for k, v in headers)
    return h + b"\r\n" + data


def mp(boundary, parts, pre=b"", post=b"", close=True):
    b = boundary.encode()
    out = pre + b"--" + b + b"\r\n"
    out += (b"\r\n--" + b + b"\r\n").join(parts)
    if close:
        out += b"\r\n--" + b + b"--\r\n" + post
    return out


WK = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
CURL = "------------------------d74496d66958873e"
png = bytes.fromhex("89504e470d0a1a0a0000000d49484452") + bytes(range(256)) + b"\r\n--" + WK.encode()[:10] + b"\r\n-" + zlib.compress(b"kara" * 40)
cd = lambda n, f=None: ("Content-Disposition", 'form-data; name="%s"' % n + ("" if f is None else '; filename="%s"' % f))

bodies = {}
bodies["login"] = (WK, mp(WK, [part([cd("username")], b"ada"), part([cd("password")], b"s3cr3t pass"), part([cd("remember")], b"on")]))
bodies["upload"] = (WK, mp(WK, [
    part([cd("title")], b"Quarterly report"),
    part([cd("doc", "report.txt"), ("Content-Type", "text/plain")], b"line one\r\nline two\r\n\r\n--not a boundary\r\n--" + WK.encode()[:-1] + b"X\r\nend"),
    part([cd("image", "logo.png"), ("Content-Type", "image/png")], png),
]))
bodies["multi"] = (CURL, mp(CURL, [
    part([cd("files", "a.csv"), ("Content-Type", "text/csv")], b"id,name\n1,ada\n2,grace\n"),
    part([cd("files", "b.csv"), ("Content-Type", "text/csv")], b"id,name\n3,linus\n"),
    part([cd("files", "empty.txt"), ("Content-Type", "text/plain")], b""),
    part([cd("note")], b""),
]))
raw = bytes(range(200)) * 3
b64 = base64.encodebytes(raw).replace(b"\n", b"\r\n")
bodies["b64"] = (WK, mp(WK, [
    part([cd("blob", "blob.bin"), ("Content-Transfer-Encoding", "base64")], b64.rstrip(b"\r\n")),
    part([cd("flat"), ("Content-Transfer-Encoding", "BASE64")], base64.b64encode(b"flat base64 field!")),
]))
qp = quopri.encodestring("Grüße aus Köln — ça va? Line with = sign and a very long line that the encoder has to wrap at seventy six characters exactly.\n".encode("utf-8")).replace(b"\n", b"\r\n")
bodies["qp"] = (WK, mp(WK, [
    part([cd("letter"), ("Content-Transfer-Encoding", "quoted-printable"), ("Content-Type", "text/plain; charset=utf-8")], qp.rstrip(b"\r\n")),
    part([cd("odd"), ("Content-Transfer-Encoding", "quoted-printable")], b"a=3D=3d=zz=\r\nb==c=4"),
]))
bodies["cte"] = (WK, mp(WK, [part([cd("x"), ("Content-Transfer-Encoding", "x-uuencode")], b"begin 644 x\r\nend")]))
bodies["names"] = (WK, mp(WK, [
    part([("Content-Disposition", 'form-data; name="ie"; filename="C:\\Users\\me\\report.pdf"')], b"%PDF-1.4"),
    part([("Content-Disposition", 'form-data; name="unc"; filename="\\\\server\\share\\x.doc"')], b"doc"),
    part([("Content-Disposition", 'form-data; name="trav"; filename="../../etc/passwd"')], b"root:x:0:0"),
    part([("Content-Disposition", 'form-data; name="q"; filename="we \\"quote\\"; and; semis.txt"')], b"q"),
    part([("Content-Disposition", "form-data; name=\"star\"; filename*=UTF-8''na%C3%AFve.txt; filename=\"naive.txt\"")], b"star"),
    part([("CONTENT-DISPOSITION", "Form-Data;Name=plain ;  FileName = .bashrc")], b"alias ll='ls -l'"),
    part([("Content-Disposition", 'form-data; name="arch"; filename="backup.tar.gz"')], b"\x1f\x8b\x08\x00"),
]))
bodies["noname"] = (WK, mp(WK, [part([("Content-Disposition", "form-data")], b"x")]))
bodies["nodisp"] = (WK, mp(WK, [part([("Content-Type", "text/plain")], b"x")]))
bodies["manyheaders"] = (WK, mp(WK, [part([cd("h")] + [("X-H%d" % k, "v") for k in range(8)], b"x")]))
bodies["eightheaders"] = (WK, mp(WK, [part([cd("h")] + [("X-H%d" % k, "v") for k in range(7)], b"x")]))
bodies["bigheader"] = (WK, mp(WK, [part([cd("h"), ("X-Big", "y" * 4300)], b"x")]))
bodies["badheader"] = (WK, mp(WK, [part([cd("h"), ("Bad Name", "v")], b"x")]))
bodies["zeroheader"] = b"--" + WK.encode() + b"\r\n: v\r\n\r\nx\r\n--" + WK.encode() + b"--\r\n"
bodies["zeroheader"] = (WK, bodies["zeroheader"])
bodies["lf"] = (WK, ("--" + WK + "\ncontent-disposition: form-data; name=\"a\"\n\nb\n--" + WK + "--\n").encode())
bodies["preamble"] = (WK, mp(WK, [part([cd("a")], b"1")], pre=b"This is the preamble.\r\n"))
bodies["crlfpre"] = (WK, mp(WK, [part([cd("a")], b"1")], pre=b"\r\n\r\n"))
bodies["epilogue"] = (WK, mp(WK, [part([cd("a")], b"1")], post=b"epilogue text\r\n--" + WK.encode() + b"--\r\n"))
bodies["truncated"] = (WK, mp(WK, [part([cd("a")], b"1"), part([cd("b")], b"never closed")], close=False))
bodies["empty"] = (WK, ("--" + WK + "--\r\n").encode())
bodies["badend"] = (WK, ("--" + WK + "-x").encode())
bodies["noLF"] = (WK, ("--" + WK + "\r\ncontent-disposition: form-data; name=a\rX").encode())
bodies["nohdrLF"] = (WK, ("--" + WK + "\r\ncontent-disposition: form-data; name=a\r\n\rX").encode())
bodies["wrongb"] = (WK, ("--" + WK[:-3] + "zzz\r\n").encode())
bodies["spaces"] = (WK, ("--" + WK + "\r\ncontent-disposition:      form-data; name=sp\r\nx-empty:\r\n\r\nv\r\n--" + WK + "--\r\n").encode())
bodies["nearmiss"] = (WK, mp(WK, [part([cd("a")], b"\r\n--" + WK.encode() + b"x\r\n--" + WK.encode() + b"-y\r\n-\r\n--\r")]))
for name, (bnd, b) in bodies.items():
    body(name + ".bin", b)

# --------------------------------------------------------------- jobs
for name in ["login", "upload", "multi", "b64", "nearmiss", "spaces", "epilogue", "crlfpre"]:
    for ch in [1, 3, 7, 64, 1000000]:
        job(kind="mp", file=name + ".bin", boundary=bodies[name][0], chunk=ch)
for name in ["truncated", "empty", "badend", "noLF", "nohdrLF", "wrongb", "preamble", "lf",
             "badheader", "zeroheader", "manyheaders", "eightheaders", "bigheader", "noname"]:
    for ch in [2, 1000000]:
        job(kind="mp", file=name + ".bin", boundary=bodies[name][0], chunk=ch)
job(kind="mp", file="login.bin", boundary=WK, chunk=5, max_size=100)
job(kind="mp", file="upload.bin", boundary=WK, chunk=50, max_header_count=1)
job(kind="mp", file="upload.bin", boundary=WK, chunk=50, max_header_size=40)
job(kind="mp", file="login.bin", boundary="x" * 257, chunk=5)
job(kind="mp", file="login.bin", boundary="x" * 256, chunk=5)

qs = ["a=1&b=2", "a=1&&b=2", "&a=1", "a&b=", "=x", "a=1&b", "a=b=c&d", "", "&", "&&",
      "name=Ada+Lovelace&email=ada%40example.com&tags=math&tags=poetry",
      "a=1;b=2", "x", "x&", "k=" + "v" * 40 + "&q"]
for s in qs:
    for ch in [1, 4, 1000]:
        job(kind="qs", body=s, chunk=ch)
    job(kind="qs", body=s, chunk=1000, strict=True)
    job(kind="qs", body=s, chunk=2, strict=True)
job(kind="qs", body="aaaa=bbbb&cccc=dddd", chunk=3, max_size=10)
job(kind="qs", body="aaaa=bbbb", chunk=3, max_size=0)
for s, ch, mx in [("hello octets", 5, None), ("", 4, None), ("0123456789", 3, 7), ("abc", 1, 1)]:
    j = dict(kind="octet", body=s, chunk=ch)
    if mx is not None:
        j["max_size"] = mx
    job(**j)

opts = ["", "text/plain", "  TEXT/HTML  ", "form-data; name=\"a\"", "form-data; name=a; filename=b.txt",
        "multipart/form-data; boundary=----x", "Multipart/Form-Data; Boundary=\"q;r\"; charset=utf-8",
        "form-data; name=\"a;b\"; filename=\"c\\\"d.txt\"", "form-data; filename*=UTF-8''x.txt; name=n",
        "form-data; name=\"x\"; filename=\"C:\\\\dir\\\\f.txt\"", "form-data; name=\"x\"; filename=\"C:\\dir\\f.txt\"",
        "form-data; name=\"x\"; filename=\"\\\\\\\\host\\\\f\"", "a;b;c", "a; =x", "a; x=", "a;;;b=1",
        "a; b=\"unterminated; c=2", "a; B = \"  spaced  \" ", "a; q=\"\"", "a; q=\"", "a; k=\"one\" two",
        "café; name=Zoë", "a; name=x; name=y"]
for o in opts:
    job(kind="options", value=o)

for chunks in [["Zm9v", "YmFy"], ["Zm9", "vYm", "Fy"], ["Zm9vYg=="], ["Zm9vYg"], ["Zm9vY"], ["Zm\r\n9v"],
               ["Zm9v\r\n", "YmFy"], ["Z!m9v"], ["Zg==Zm9v"], ["====", "Zm9v"], ["Zm9vYmFy\r\n"], [""],
               ["SGVsbG8sIHdvcmxkIQ=="], ["Zm9v", "Y", "m", "F", "y"], ["Zm9=v"]]:
    job(kind="b64", chunks=chunks)
for chunks in [["a=3Db"], ["a=", "3Db"], ["a=3", "Db"], ["line=\r\nnext"], ["soft=", "\r\nbreak"],
               ["=E2=82=AC"], ["=e2=82=ac"], ["bad=zz"], ["end="], ["x==y"], ["tail=4"], ["a=\rb\nc"],
               ["=", "=", "4", "1"], ["plain"], [""]]:
    job(kind="qp", chunks=chunks)

forms = [
    ({"Content-Type": "multipart/form-data; boundary=" + WK}, "login.bin", 13, {}),
    ({"Content-Type": "multipart/form-data; boundary=\"" + WK + "\""}, "upload.bin", 100, {}),
    ({"Content-Type": "multipart/form-data; boundary=" + WK}, "upload.bin", 100, {"MAX_MEMORY_FILE_SIZE": 64}),
    ({"Content-Type": "multipart/form-data; boundary=" + CURL}, "multi.bin", 9, {"MAX_MEMORY_FILE_SIZE": 10, "UPLOAD_DIR": "data/uploads", "UPLOAD_KEEP_FILENAME": True, "UPLOAD_KEEP_EXTENSIONS": True}),
    ({"Content-Type": "multipart/form-data; boundary=" + WK}, "names.bin", 17, {"MAX_MEMORY_FILE_SIZE": 1, "UPLOAD_DIR": "data/uploads", "UPLOAD_KEEP_FILENAME": True, "UPLOAD_KEEP_EXTENSIONS": True}),
    ({"Content-Type": "multipart/form-data; boundary=" + WK}, "names.bin", 17, {"MAX_MEMORY_FILE_SIZE": 1, "UPLOAD_DIR": "data/uploads", "UPLOAD_KEEP_FILENAME": True}),
    ({"Content-Type": "multipart/form-data; boundary=" + WK}, "b64.bin", 7, {}),
    ({"Content-Type": "multipart/form-data; boundary=" + WK}, "b64.bin", 76, {}),
    ({"Content-Type": "multipart/form-data; boundary=" + WK}, "b64.bin", 78, {}),
    ({"Content-Type": "multipart/form-data; boundary=" + WK}, "b64.bin", 1000000, {}),
    ({"Content-Type": "multipart/form-data; boundary=" + WK}, "qp.bin", 11, {}),
    ({"Content-Type": "multipart/form-data; boundary=" + WK}, "cte.bin", 50, {}),
    ({"Content-Type": "multipart/form-data; boundary=" + WK}, "cte.bin", 50, {"UPLOAD_ERROR_ON_BAD_CTE": True}),
    ({"Content-Type": "multipart/form-data; boundary=" + WK}, "noname.bin", 50, {}),
    ({"Content-Type": "multipart/form-data; boundary=" + WK}, "nodisp.bin", 50, {}),
    ({"Content-Type": "multipart/form-data; boundary=" + WK, "Content-Length": "120"}, "login.bin", 50, {}),
    ({"Content-Type": "multipart/form-data; boundary=" + WK}, "login.bin", 50, {"MAX_BODY_SIZE": 200}),
    ({"Content-Type": "multipart/form-data"}, "login.bin", 50, {}),
    ({"Content-Type": "text/plain"}, "login.bin", 50, {}),
    ({}, "login.bin", 50, {}),
    ({"Content-Type": "application/x-www-form-urlencoded"}, "form.txt", 6, {}),
    ({"Content-Type": "application/x-url-encoded", "Content-Length": "20"}, "form.txt", 6, {}),
    ({"Content-Type": "application/x-www-form-urlencoded"}, "form.txt", 6, {"MAX_BODY_SIZE": 25}),
    ({"Content-Type": "application/octet-stream"}, "upload.bin", 333, {"MAX_MEMORY_FILE_SIZE": 500}),
    ({"Content-Type": "application/octet-stream", "Content-Length": "-1"}, "login.bin", 50, {}),
]
open("data/bodies/form.txt", "wb").write(b"q=kara+lang&page=2&flag&&empty=&x=1=2&last=end")
for headers, f, ch, cfg in forms:
    job(kind="form", headers=headers, file=f, chunk=ch, config=cfg)
job(kind="form", headers={"Content-Type": "multipart/form-data; boundary=" + WK}, file="login.bin", chunk=0, config={})


# --------------------------------------------------------------- uploads
def request(path, ctype, b, extra=()):
    head = "POST %s HTTP/1.1\r\nHost: files.example\r\nContent-Type: %s\r\nContent-Length: %d\r\n" % (path, ctype, len(b))
    for k, v in extra:
        head += "%s: %s\r\n" % (k, v)
    return head.encode() + b"\r\n" + b


reqs = [
    request("/upload", "multipart/form-data; boundary=" + WK, bodies["upload"][1]),
    request("/upload", "multipart/form-data; boundary=" + CURL, bodies["multi"][1], [("User-Agent", "curl/8.5.0")]),
    request("/avatar", "application/octet-stream", png[:300], [("X-File-Name", "me.png")]),
    request("/search", "application/x-www-form-urlencoded", b"q=multipart&lang=kara&lang=python"),
    request("/upload", "multipart/form-data; boundary=" + WK, bodies["names"][1]),
    request("/upload", "multipart/form-data; boundary=" + WK, bodies["badheader"][1]),
    request("/upload", "text/csv", b"a,b\n1,2\n"),
    request("/upload", "multipart/form-data; boundary=" + WK, bodies["b64"][1]),
]
for k, r in enumerate(reqs):
    open("data/requests/%02d.http" % k, "wb").write(r)
job(kind="server", dir="requests")

with open("data/jobs.jsonl", "w") as out:
    for j in jobs:
        out.write(json.dumps(j) + "\n")
print(len(jobs), "jobs")
