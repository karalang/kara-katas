"""Writes the generated parts of mini_tinytag.kara to stdout: with the
argument `tables`, the lookup tables of tinytag's parser classes, read from
the copy in tinytag/; with none, the files under data/ (the binary ones as
hex, where a run of zero bytes is written Z<count>;)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
os.chdir(HERE)

from tinytag import tinytag as tt  # noqa: E402


def lit(s):
    out = []
    for ch in s:
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\t":
            out.append("\\t")
        elif ord(ch) < 32 or ord(ch) > 126:
            out.append("\\u{%x}" % ord(ch))
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


def key(k):
    return k.decode("latin-1") if isinstance(k, bytes) else k


def str_map(name, doc, d):
    print()
    print("// " + doc)
    print("fn %s(k: ref String) -> Option[String] {" % name)
    print("    match k {")
    for k, v in d.items():
        print("        %s => Some(%s.to_string())," % (lit(key(k)), lit(v)))
    print("        _ => None,")
    print("    }")
    print("}")


def str_set(name, doc, s):
    print()
    print("// " + doc)
    print("fn %s(k: ref String) -> bool {" % name)
    print("    match k {")
    for k in sorted(key(x) for x in s):
        print("        %s => true," % lit(k))
    print("        _ => false,")
    print("    }")
    print("}")


def int_set(name, doc, s):
    print()
    print("// " + doc)
    print("fn %s(n: i64) -> bool {" % name)
    print("    match n {")
    for k in sorted(s):
        print("        %d => true," % k)
    print("        _ => false,")
    print("    }")
    print("}")


def str_list(name, doc, items):
    print()
    print("// " + doc)
    print("const %s_LEN: i64 = %d;" % (name.upper(), len(items)))
    print()
    print("fn %s(i: i64) -> String {" % name)
    print("    match i {")
    for i, v in enumerate(items):
        print("        %d => %s.to_string()," % (i, lit(v)))
    print("        _ => String.new(),")
    print("    }")
    print("}")


def int_list(name, doc, items):
    print()
    print("// " + doc)
    print("fn %s(i: i64) -> i64 {" % name)
    print("    match i {")
    for i, v in enumerate(items):
        if v:
            print("        %d => %d," % (i, v))
    print("        _ => 0,")
    print("    }")
    print("}")


def ilst_tree():
    # _MP4's ilst subtree: each atom maps to {b'data': parser}, except
    # b'----', which is a parser itself.
    tree = tt._MP4._build_meta_data_tree()[b"moov"][b"udta"][b"meta"][b"ilst"]
    print()
    print("// _MP4's tree below ilst: for each atom, the parser of its data atom, as")
    print("// (kind, field, field): 0 _data_parser, 1 _nums_parser, 2 the genre, 3")
    print("// the cover; 4 is the '----' atom, parsed by _parse_custom_field itself.")
    print("fn ilst_entry(k: ref String) -> Option[(i64, String, String)] {")
    print("    match k {")
    for atom, sub in tree.items():
        if callable(sub):
            kind, a, b = 4, "", ""
        else:
            fn = sub[b"data"]
            fname = getattr(fn, "__name__", "")
            if fname == "_parse_data_atom":
                kind, a, b = 0, fn.__closure__[fn.__code__.co_freevars.index("fieldname")].cell_contents, ""
            elif fname == "_parse_nums":
                fv = fn.__code__.co_freevars
                cells = fn.__closure__
                kind = 1
                a = cells[fv.index("fieldname1")].cell_contents
                b = cells[fv.index("fieldname2")].cell_contents
            elif fname == "_parse_id3v1_genre":
                kind, a, b = 2, "", ""
            elif fname == "_parse_cover_image":
                kind, a, b = 3, "", ""
            else:
                raise SystemExit("unknown parser %r" % fname)
        print("        %s => Some((%d, %s.to_string(), %s.to_string()))," % (lit(key(atom)), kind, lit(a), lit(b)))
    print("        _ => None,")
    print("    }")
    print("}")


def tables():
    print("// ------------------------------------------------------------ tables")
    print()
    print("// tinytag's lookup tables, as gen_kara.py read them from its classes.")
    i = tt._ID3
    str_map("id3_field", "_ID3._ID3_MAPPING: frame id to field", i._ID3_MAPPING)
    str_map("id3_custom", "_ID3._ID3_MAPPING_CUSTOM", i._ID3_MAPPING_CUSTOM)
    str_set("id3_ignored", "_ID3._IGNORED_FRAME_IDS", i._IGNORED_FRAME_IDS)
    str_map("id3v22_image_format", "_ID3._ID3V2_2_IMAGE_FORMATS", i._ID3V2_2_IMAGE_FORMATS)
    str_list("genre_name", "_ID3._ID3V1_GENRES", i._ID3V1_GENRES)
    str_list("image_type", "_ID3._IMAGE_TYPES", i._IMAGE_TYPES)
    m = tt._MPEG
    int_list("mpeg_sample_rate", "_MPEG._SAMPLE_RATES, at mpeg_id * 3 + sr_id",
             [x for row in m._SAMPLE_RATES for x in row])
    int_list("mpeg_bitrate", "_MPEG._BITRATE_VERSION_LAYERS, at (mpeg_id * 4 + layer_id) * 16 + br_id",
             [x for row in m._BITRATE_VERSION_LAYERS for layer in row for x in layer])
    int_list("mpeg_samples_per_frame", "_MPEG._SAMPLES_PER_FRAME, at mpeg_id * 4 + layer_id",
             [x for row in m._SAMPLES_PER_FRAME for x in row])
    int_list("mpeg_slot_size", "_MPEG._SLOT_SIZES", m._SLOT_SIZES)
    int_list("mpeg_channels", "_MPEG._CHANNELS_PER_CHANNEL_MODE", m._CHANNELS_PER_CHANNEL_MODE)
    str_map("vorbis_field", "_Ogg._VORBIS_MAPPING", tt._Ogg._VORBIS_MAPPING)
    str_map("riff_field", "_Wave._RIFF_MAPPING", tt._Wave._RIFF_MAPPING)
    int_set("wav_lossless", "_Wave._LOSSLESS_FORMATS", tt._Wave._LOSSLESS_FORMATS)
    str_map("asf_field", "_ASF._ASF_MAPPING", tt._ASF._ASF_MAPPING)
    str_map("mp4_custom", "_MP4._CUSTOM_FIELD_NAME_MAPPING", tt._MP4._CUSTOM_FIELD_NAME_MAPPING)
    print()
    print("// _MP4._IMAGE_MIME_TYPES")
    print("fn mp4_image_mime(n: i64) -> Option[String] {")
    print("    match n {")
    for k, v in tt._MP4._IMAGE_MIME_TYPES.items():
        print("        %d => Some(%s.to_string())," % (k, lit(v)))
    print("        _ => None,")
    print("    }")
    print("}")
    str_set("mp4_lossless", "_MP4._LOSSLESS_CODECS", tt._MP4._LOSSLESS_CODECS)
    ilst_tree()
    str_map("aiff_field", "_Aiff._AIFF_MAPPING", tt._Aiff._AIFF_MAPPING)
    str_set("aiff_uncompressed", "_Aiff._UNCOMPRESSED_FORMATS", tt._Aiff._UNCOMPRESSED_FORMATS)
    print()
    print("// TinyTag._get_parser_for_filename: each extension and its class")
    print("fn ext_class(name: ref String) -> i64 {")
    print("    let n = name.to_lowercase();")
    classes = {tt._ID3: "K_ID3", tt._Ogg: "K_OGG", tt._Wave: "K_WAVE", tt._ASF: "K_ASF",
               tt._MP4: "K_MP4", tt._Aiff: "K_AIFF"}
    tt.TinyTag._get_parser_for_filename("x")
    for exts, cls in tt.TinyTag._file_extension_mapping.items():
        for e in exts:
            print("    if n.ends_with(%s) {" % lit(e))
            print("        return %s;" % classes[cls])
            print("    }")
    print("    0")
    print("}")


def is_text(b):
    try:
        s = b.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return all(c >= " " or c in "\n\t" for c in s)


def packed_hex(b):
    out = []
    i = 0
    while i < len(b):
        j = i
        while j < len(b) and b[j] == 0:
            j += 1
        if j - i >= 16:
            out.append("Z%d;" % (j - i))
            i = j
        else:
            out.append("%02x" % b[i])
            i += 1
    return "".join(out)


def datafiles():
    names = []
    for root, dirs, files in os.walk("data"):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), "data")
            if not rel.startswith("out" + os.sep):
                names.append(rel)
    names.sort()
    print("// ------------------------------------------------------------ data")
    print()
    print("// The files under data/, in path order. The binary ones are spelled in")
    print("// hex, with Z<count>; for a run of zero bytes.")
    print("fn data_files() -> Vec[DataFile] {")
    print("    let mut v: Vec[DataFile] = Vec.new();")
    for k in range(len(names)):
        print("    v.push(data_%d());" % k)
    print("    v")
    print("}")
    for k, n in enumerate(names):
        b = open(os.path.join("data", n), "rb").read()
        print()
        print("fn data_%d() -> DataFile {" % k)
        print("    let mut t = String.new();")
        if is_text(b):
            for line in b.decode("utf-8").splitlines(keepends=True):
                print("    t.push_str(%s);" % lit(line))
            print("    DataFile { path: %s.to_string(), body: t, hex: false }" % lit(n))
        else:
            h = packed_hex(b)
            for i in range(0, len(h), 96):
                print('    t.push_str("%s");' % h[i:i + 96])
            print("    DataFile { path: %s.to_string(), body: t, hex: true }" % lit(n))
        print("}")


if sys.argv[1:] == ["tables"]:
    tables()
else:
    datafiles()
