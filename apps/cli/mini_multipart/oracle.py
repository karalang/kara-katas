# Runs data/jobs.jsonl through the real python-multipart 0.0.32
# (pip install python-multipart==0.0.32) and prints what mini_multipart
# prints. Run it after mk.py; its output is expected.out.
import io, json, os, sys

from python_multipart.multipart import (
    MultipartParser, QuerystringParser, OctetStreamParser, parse_options_header, create_form_parser,
)
from python_multipart.decoders import Base64Decoder, QuotedPrintableDecoder
from python_multipart.exceptions import ParseError

INF = float("inf")


def err_line(e):
    s = "%s: %s" % (type(e).__name__, e)
    if isinstance(e, ParseError):
        s += " offset=%d" % e.offset
    return s


class Recorder:
    def __init__(self, names):
        self.events = []
        self.cbs = {}
        for n in names:
            self.cbs["on_" + n] = self.make(n)

    def make(self, n):
        def f(*a):
            if a:
                data, start, end = a
                self.events.append((n, data[start:end]))
            else:
                self.events.append((n, None))
        return f

    def dump(self):
        k = 0
        ev = self.events
        while k < len(ev):
            n, d = ev[k]
            if d is None:
                print("  " + n)
                k += 1
                continue
            j = k
            buf = b""
            while j < len(ev) and ev[j][0] == n and ev[j][1] is not None:
                buf += ev[j][1]
                j += 1
            print("  %s %d %r" % (n, j - k, buf))
            k = j


MP_CBS = ["part_begin", "part_data", "part_end", "header_begin", "header_field", "header_value",
          "header_end", "headers_finished", "end"]
QS_CBS = ["field_start", "field_name", "field_data", "field_end", "end"]
OCTET_CBS = ["start", "data", "end"]


def chunks_of(b, n):
    return [b[k:k + n] for k in range(0, len(b), n)]


def run_parser(make, body, chunk, names):
    rec = Recorder(names)
    total = 0
    try:
        p = make(rec.cbs)
        for c in chunks_of(body, chunk):
            total += p.write(c)
        p.finalize()
    except Exception as e:
        rec.dump()
        print("  error " + err_line(e))
        return
    rec.dump()
    print("  wrote %d" % total)


class Collector:
    def write(self, data):
        print("  write %r" % data)
        return len(data)

    def finalize(self):
        print("  finalize")


def run_decoder(cls, chunks):
    d = cls(Collector())
    try:
        for c in chunks:
            d.write(c.encode())
        d.finalize()
    except Exception as e:
        print("  error " + err_line(e))


def show_file(f, cfg):
    print("  file %r size=%d in_memory=%s content_type=%r" % (f, f.size, f.in_memory, f.content_type))
    if cfg.get("UPLOAD_KEEP_FILENAME") and f.actual_file_name is not None:
        print("    saved %r" % f.actual_file_name)
    fo = f.file_object
    if f.in_memory:
        data = fo.getvalue()
    else:
        fo.seek(0)
        data = fo.read()
    more = " (+%d more)" % (len(data) - 60) if len(data) > 60 else ""
    print("    data %r%s" % (data[:60], more))


def handle_form(headers, stream, on_field, on_file, chunk_size, config):
    # python_multipart.parse_form, with a config passed to the parser.
    if chunk_size < 1:
        raise ValueError(f"chunk_size must be a positive number, not {chunk_size!r}")
    parser = create_form_parser(headers, on_field, on_file, config)
    content_length = headers.get("Content-Length")
    if content_length is not None:
        content_length = int(content_length)
        if content_length < 0:
            raise ValueError("Content-Length must be non-negative")
    else:
        content_length = INF
    bytes_read = 0
    while True:
        max_readable = int(min(content_length - bytes_read, chunk_size))
        buff = stream.read(max_readable)
        parser.write(buff)
        bytes_read += len(buff)
        if len(buff) != max_readable or bytes_read == content_length:
            break
    parser.finalize()


def make_config(c):
    cfg = dict(c)
    if "UPLOAD_DIR" in cfg:
        cfg["UPLOAD_DIR"] = cfg["UPLOAD_DIR"].encode()
    return cfg


def run_form(j):
    cfg = make_config(j["config"])
    body = open("data/bodies/" + j["file"], "rb").read()

    def on_field(f):
        print("  field %r content_type=%r" % (f, f.content_type))

    def on_file(f):
        show_file(f, cfg)

    try:
        handle_form(j["headers"], io.BytesIO(body), on_field, on_file, j["chunk"], cfg)
    except Exception as e:
        print("  error " + err_line(e))
        return
    print("  done")


def run_server(j):
    d = "data/" + j["dir"]
    cfg = {"UPLOAD_DIR": b"data/uploads", "UPLOAD_KEEP_FILENAME": True, "UPLOAD_KEEP_EXTENSIONS": True,
           "MAX_MEMORY_FILE_SIZE": 100}
    for name in sorted(os.listdir(d)):
        raw = open(os.path.join(d, name), "rb").read()
        head, _, body = raw.partition(b"\r\n\r\n")
        lines = head.decode("latin-1").split("\r\n")
        method, path, _ = lines[0].split(" ")
        headers = {}
        for line in lines[1:]:
            k, _, v = line.partition(":")
            headers[k.strip()] = v.strip()
        print("  %s %s %s (%s)" % (name, method, path, headers.get("Content-Type")))
        counts = [0, 0]

        def on_field(f):
            counts[0] += 1
            print("    field %s = %r" % (f.field_name.decode("latin-1"), f.value))

        def on_file(f):
            counts[1] += 1
            if f.in_memory:
                fname = os.path.basename(f.file_name) if f.file_name else b"upload.bin"
                where = os.path.join(b"data/uploads", fname)
                open(where, "wb").write(f.file_object.getvalue())
            else:
                where = f.actual_file_name
            print("    file %s %r %d bytes -> %s" % (f.field_name.decode("latin-1") if f.field_name else "-",
                                                      f.file_name, f.size, where.decode("latin-1")))

        try:
            handle_form(headers, io.BytesIO(body), on_field, on_file, 64, cfg)
        except ValueError as e:
            print("    400 " + err_line(e))
            continue
        except Exception as e:
            print("    500 " + err_line(e))
            continue
        print("    200 %d fields, %d files" % (counts[0], counts[1]))
    print("  uploads:")
    for name in sorted(os.listdir("data/uploads")):
        print("    %s %d" % (name, os.path.getsize(os.path.join("data/uploads", name))))


def main():
    os.makedirs("data/uploads", exist_ok=True)
    for name in os.listdir("data/uploads"):
        os.remove(os.path.join("data/uploads", name))
    for line in open("data/jobs.jsonl"):
        line = line.rstrip("\n")
        j = json.loads(line)
        print("== " + line)
        k = j["kind"]
        if k == "mp":
            body = open("data/bodies/" + j["file"], "rb").read()
            run_parser(lambda cbs: MultipartParser(j["boundary"].encode(), cbs, max_size=j.get("max_size", INF),
                                                   max_header_count=j.get("max_header_count", 8),
                                                   max_header_size=j.get("max_header_size", 4224)),
                       body, j["chunk"], MP_CBS)
        elif k == "qs":
            run_parser(lambda cbs: QuerystringParser(cbs, strict_parsing=j.get("strict", False),
                                                     max_size=j.get("max_size", INF)),
                       j["body"].encode(), j["chunk"], QS_CBS)
        elif k == "octet":
            run_parser(lambda cbs: OctetStreamParser(cbs, max_size=j.get("max_size", INF)),
                       j["body"].encode(), j["chunk"], OCTET_CBS)
        elif k == "options":
            print("  %r" % (parse_options_header(j["value"]),))
        elif k == "b64":
            run_decoder(Base64Decoder, j["chunks"])
        elif k == "qp":
            run_decoder(QuotedPrintableDecoder, j["chunks"])
        elif k == "form":
            run_form(j)
        elif k == "server":
            run_server(j)
    sys.stdout.flush()


main()
