# Writes data/: the css-parsing-tests suites the run uses (copied from
# css-parsing-tests/) and the stylesheets of the audit (copied from
# sheets/, as bytes). The four 1500-case Lab, LCH, OKLab and OKLCH
# suites keep every third case, which keeps the interpreter's run short;
# the others are copied unchanged.
import json, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
SUITES = [
    "An+B.json", "blocks_contents.json", "color_function_4.json", "color_hexadecimal_3.json",
    "color_hexadecimal_4.json", "color_hsl_3.json", "color_hsl_4.json", "color_hwb_4.json",
    "color_keywords_3.json", "color_keywords_4.json", "color_lab_4.json", "color_lch_4.json",
    "color_oklab_4.json", "color_oklch_4.json", "component_value_list.json", "declaration_list.json",
    "one_component_value.json", "one_declaration.json", "one_rule.json", "rule_list.json",
    "stylesheet.json", "stylesheet_bytes.json",
]

THIRDS = ["color_lab_4.json", "color_lch_4.json", "color_oklab_4.json", "color_oklch_4.json"]


def main():
    os.makedirs(os.path.join(DATA, "sheets"), exist_ok=True)
    for name in SUITES:
        src = os.path.join(HERE, "css-parsing-tests", name)
        if name in THIRDS:
            with open(src, encoding="utf-8") as f:
                data = json.load(f)
            pairs = list(zip(data[::2], data[1::2]))[::3]
            with open(os.path.join(DATA, name), "w", encoding="utf-8") as f:
                f.write("[\n" + ",\n".join("%s, %s" % (json.dumps(a), json.dumps(b)) for a, b in pairs) + "\n]\n")
        else:
            shutil.copyfile(src, os.path.join(DATA, name))
    with open(os.path.join(HERE, "sheets", "sheets.tsv"), encoding="utf-8") as f:
        names = [l.split("\t")[0] for l in f if l.strip()]
    for name in names + ["sheets.tsv"]:
        shutil.copyfile(os.path.join(HERE, "sheets", name), os.path.join(DATA, "sheets", name))


main()
