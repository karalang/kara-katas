# Runs the scripts mk.py writes through hpack 4.1.0 (the copy in hpack/)
# and wrote expected.out.
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from hpack import Decoder, Encoder, HeaderTuple, NeverIndexedHeaderTuple  # noqa: E402
from hpack.exceptions import HPACKError  # noqa: E402


def esc(s):
    out = []
    for c in s:
        o = ord(c)
        if o < 0x20 or o == 0x7F:
            out.append(f"\\x{o:02x}")
        else:
            out.append(c)
    return "".join(out)


def err_text(e):
    msg = re.sub(r"<memory at 0x[0-9a-fA-F]+>", "<memory>", str(e))
    return f"{type(e).__name__}: {msg}"


def show_table(t, indent="   "):
    entries = list(t.dynamic_entries)
    print(f"{indent}table: {len(entries)} entries, {t._current_size} of {t.maxsize} bytes")
    for i, (n, v) in enumerate(entries):
        print(f"{indent}  [{62 + i}] {esc(bytes(n).decode('utf-8', 'replace'))}: {esc(bytes(v).decode('utf-8', 'replace'))}")


def per_mille(num, den):
    if den == 0:
        return "-"
    r = num * 1000 // den
    return f"{r // 10}.{r % 10}%"


def run_stories(lines):
    i = 0
    enc = dec = None
    huffman = True
    closed = False
    total_raw = total_enc = 0

    def finish():
        if enc is not None:
            print(f"   connection: {total_raw} bytes of headers sent as {total_enc} ({per_mille(total_enc, total_raw)})")

    while i < len(lines):
        line = lines[i]
        i += 1
        if not line:
            continue
        word, _, rest = line.partition(" ")
        if word == "story":
            finish()
            print(f"== story: {rest}")
            enc, dec = Encoder(), Decoder()
            huffman, closed = True, False
            total_raw = total_enc = 0
        elif word == "huffman":
            huffman = rest == "on"
        elif word in ("encoder-table", "decoder-table", "decoder-max", "decoder-list-max"):
            n = int(rest)
            print(f"   {word} {n}")
            if word == "encoder-table":
                enc.header_table_size = n
            elif word == "decoder-table":
                dec.header_table_size = n
            elif word == "decoder-max":
                dec.max_allowed_table_size = n
            else:
                dec.max_header_list_size = n
        elif word in ("block", "dict"):
            headers = []
            while lines[i] != "end":
                kind, _, nv = lines[i].partition(" ")
                name, _, value = nv.partition("\t")
                headers.append((name, value, kind == "s"))
                i += 1
            i += 1
            if closed:
                print(f"-- {word} {rest}: not sent, the connection is closed")
                continue
            if word == "dict":
                given = {n: v for n, v, _ in headers}
                sent = sorted(headers, key=lambda h: not h[0].startswith(":"))
                data = enc.encode(given, huffman=huffman)
            else:
                given = [NeverIndexedHeaderTuple(n, v) if s else HeaderTuple(n, v) for n, v, s in headers]
                sent = headers
                data = enc.encode(given, huffman=huffman)
            raw = sum(len(n.encode()) + len(v.encode()) for n, v, _ in headers)
            total_raw += raw
            total_enc += len(data)
            print(f"-- {word} {rest}: {len(headers)} headers, {raw} bytes, encoded in {len(data)} "
                  f"({per_mille(len(data), raw)})")
            print(f"   {data.hex()}")
            try:
                got = dec.decode(data)
            except HPACKError as e:
                print(f"   decode error {err_text(e)}")
                print("   connection closed")
                closed = True
                continue
            want = [(n, v, s and word == "block") for n, v, s in sent]
            have = [(h[0], h[1], isinstance(h, NeverIndexedHeaderTuple)) for h in got]
            if have == want:
                print("   decoded the same headers")
            else:
                print("   decoded DIFFERENT headers:")
                for n, v, s in have:
                    print(f"     {'! ' if s else ''}{esc(n)}: {esc(v)}")
            same = list(enc.header_table.dynamic_entries) == list(dec.header_table.dynamic_entries)
            print("   tables agree" if same else "   tables DIFFER")
            show_table(dec.header_table)
    finish()


def run_vectors(lines):
    dec = None
    n = 0
    for line in lines:
        if not line:
            continue
        word, _, rest = line.partition(" ")
        if word == "case":
            print(f"== case: {rest}")
            dec = Decoder()
            n = 0
        elif word in ("decoder-table", "decoder-max", "decoder-list-max"):
            v = int(rest)
            print(f"   {word} {v}")
            if word == "decoder-table":
                dec.header_table_size = v
            elif word == "decoder-max":
                dec.max_allowed_table_size = v
            else:
                dec.max_header_list_size = v
        elif word == "hex":
            n += 1
            data = bytes.fromhex(rest)
            print(f"-- block {n}: {len(data)} bytes")
            try:
                got = dec.decode(data)
            except HPACKError as e:
                print(f"   error {err_text(e)}")
            else:
                for h in got:
                    mark = "! " if isinstance(h, NeverIndexedHeaderTuple) else ""
                    print(f"   {mark}{esc(h[0])}: {esc(h[1])}")
            show_table(dec.header_table)


def main():
    data = os.path.join(HERE, "data")
    with open(os.path.join(data, "stories.txt"), encoding="utf-8") as f:
        run_stories(f.read().split("\n"))
    with open(os.path.join(data, "vectors.txt"), encoding="utf-8") as f:
        run_vectors(f.read().split("\n"))


if __name__ == "__main__":
    main()
