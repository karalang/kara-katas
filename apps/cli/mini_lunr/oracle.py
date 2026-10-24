"""The oracle for mini_lunr: builds the documentation site's search index
with the vendored lunr.py 0.8.0, runs every query in data/queries.txt
against it, serializes it to JSON, loads that back and runs the queries
again, and prints what the port prints.

Run: python3 -I -B oracle.py > expected.out"""
import json
import os
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))

from lunr import lunr  # noqa: E402
from lunr.index import Index  # noqa: E402
from lunr.exceptions import BaseLunrException  # noqa: E402
from lunr.builder import Builder  # noqa: E402
from lunr.stemmer import stemmer  # noqa: E402
from lunr.trimmer import trimmer  # noqa: E402
from lunr.stop_word_filter import stop_word_filter  # noqa: E402


def load_docs():
    docs = []
    with open(os.path.join(HERE, "data", "docs.txt")) as f:
        for line in f.read().splitlines():
            ref, boost, title, tags, body = line.split("|")
            docs.append(({"id": ref, "title": title, "tags": tags, "body": body},
                         {"boost": int(boost)}))
    return docs


def builder():
    b = Builder()
    b.pipeline.add(trimmer, stop_word_filter, stemmer)
    b.search_pipeline.add(stemmer)
    b.metadata_whitelist = ["position"]
    return b


def show(n, q, idx, out):
    try:
        results = idx.search(q)
    except BaseLunrException as e:
        out.append("q%d %s: error: %s" % (n, json.dumps(q), e))
        return
    out.append("q%d %s: %d results" % (n, json.dumps(q), len(results)))
    for r in results[:5]:
        terms = sorted(r["match_data"].metadata.keys())
        out.append("  %s %.6f %s" % (r["ref"], r["score"], ",".join(terms)))
    if results:
        md = results[0]["match_data"].metadata
        for term in sorted(md.keys()):
            for field, meta in md[term].items():
                pos = meta.get("position", [])
                out.append("    %s %s %s" % (term, field, " ".join("%d+%d" % (p[0], p[1]) for p in pos)))


def main():
    docs = load_docs()
    with open(os.path.join(HERE, "data", "queries.txt")) as f:
        queries = f.read().splitlines()
    idx = lunr(ref="id", fields=[dict(field_name="title", boost=10), "tags", "body"],
               documents=docs, builder=builder())
    terms = len(idx.inverted_index)
    print("index: %d pages, %d terms, %d field vectors" % (len(docs), terms, len(idx.field_vectors)))
    out = []
    for n, q in enumerate(queries):
        show(n + 1, q, idx, out)
    print("\n".join(out))
    text = json.dumps(idx.serialize())
    data = text.encode()
    print("serialized: %d bytes, crc32 %08x" % (len(data), zlib.crc32(data)))
    path = "mini_lunr_index.json"
    with open(path, "w") as f:
        f.write(text)
    with open(path) as f:
        loaded = Index.load(f.read())
    os.remove(path)
    again = []
    for n, q in enumerate(queries):
        show(n + 1, q, loaded, again)
    same = sum(1 for a, b in zip(out, again) if a == b)
    print("loaded index: %d of %d lines agree" % (same, len(out)))


main()
