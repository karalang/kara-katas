"""Write data/: the job script (data/jobs.tsv, one tab-separated command a
line), the place list and zones the index jobs query, and data/files.txt
listing the inputs for gen_kara.py.

Run from this directory: python3 -s -P -B mk.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

PLACES = [
    ("san_francisco", 37.7749, -122.4194),
    ("oakland", 37.8044, -122.2712),
    ("berkeley", 37.8715, -122.2730),
    ("palo_alto", 37.4419, -122.1430),
    ("san_jose", 37.3382, -121.8863),
    ("sausalito", 37.8591, -122.4853),
    ("los_angeles", 34.0522, -118.2437),
    ("seattle", 47.6062, -122.3321),
    ("vancouver", 49.2827, -123.1207),
    ("new_york", 40.7128, -74.0060),
    ("newark", 40.7357, -74.1724),
    ("boston", 42.3601, -71.0589),
    ("chicago", 41.8781, -87.6298),
    ("mexico_city", 19.4326, -99.1332),
    ("honolulu", 21.3069, -157.8583),
    ("anchorage", 61.2181, -149.9003),
    ("london", 51.5074, -0.1278),
    ("greenwich", 51.4769, 0.0005),
    ("paris", 48.8566, 2.3522),
    ("berlin", 52.5200, 13.4050),
    ("madrid", 40.4168, -3.7038),
    ("rome", 41.9028, 12.4964),
    ("reykjavik", 64.1466, -21.9426),
    ("cairo", 30.0444, 31.2357),
    ("nairobi", -1.2921, 36.8219),
    ("cape_town", -33.9249, 18.4241),
    ("dubai", 25.2048, 55.2708),
    ("mumbai", 19.0760, 72.8777),
    ("chennai", 13.0827, 80.2707),
    ("singapore", 1.3521, 103.8198),
    ("beijing", 39.9042, 116.4074),
    ("tokyo", 35.6762, 139.6503),
    ("yokohama", 35.4437, 139.6380),
    ("seoul", 37.5665, 126.9780),
    ("sydney", -33.8688, 151.2093),
    ("auckland", -36.8485, 174.7633),
    ("suva", -18.1248, 178.4501),
    ("apia", -13.8506, -171.7513),
    ("sao_paulo", -23.5505, -46.6333),
    ("buenos_aires", -34.6037, -58.3816),
    ("ushuaia", -54.8019, -68.3030),
    ("mcmurdo", -77.8419, 166.6863),
    ("longyearbyen", 78.2232, 15.6267),
    ("null_island", 0.0, 0.0),
    ("north_pole", 90.0, 0.0),
    ("south_pole", -90.0, 0.0),
]

ZONES = [
    ("bay_area", "rect", 37.2, -122.6, 38.0, -121.7),
    ("europe", "rect", 35.0, -10.0, 60.0, 30.0),
    ("dateline", "rect", -40.0, 170.0, -10.0, -170.0),
    ("tokyo_bay", "cap", 35.5, 139.8, 0.5),
    ("arctic", "cap", 90.0, 0.0, 23.5),
    ("face_cell", "cell", "1"),
]

SF = "37.7749\t-122.4194"
NY = "40.7128\t-74.0060"
LONDON = "51.5074\t-0.1278"
TOKYO = "35.6762\t139.6503"
SYDNEY = "-33.8688\t151.2093"

LEAF = "8085808c0a53f33b"   # a level-30 cell in San Francisco


def jobs():
    j = []
    a = j.append

    a("# cell ids from lat/lng")
    for lat, lng, lv in [
        ("37.7749", "-122.4194", "30"), ("37.7749", "-122.4194", "12"),
        ("37.7749", "-122.4194", "0"), ("40.7128", "-74.0060", "15"),
        ("51.5074", "-0.1278", "8"), ("35.6762", "139.6503", "20"),
        ("-33.8688", "151.2093", "5"), ("0", "0", "1"), ("90", "0", "3"),
        ("-90", "0", "3"), ("0", "180", "4"), ("0", "-180", "4"),
        ("45", "45", "2"), ("-45", "-135", "6"), ("1e-9", "1e-9", "29"),
        ("64.1466", "-21.9426", "10"), ("-77.8419", "166.6863", "7"),
        ("37.7749", "-122.4194", "31"), ("37.7749", "-122.4194", "-1"),
    ]:
        a("cell\t%s\t%s\t%s" % (lat, lng, lv))
    a("cell\t95\t200")
    a("cell\t-12.5\t-400")

    a("# tokens and raw ids")
    for t in ["89c25", "89c259", "1", "3", "5", "7", "9", "b", "47", LEAF,
              "0", "X", "", "fffffffffffffff", "ffffffffffffffff",
              "8085808c0a53f33", "1000000000000001", "c", "d",
              "2ef59bd352b93ac3"]:
        a("token\t%s" % t)
    for i in ["0", "1", "-1", "0x1000000000000000", "0xffffffffffffffff",
              "0x10000000000000000", "-0x1000000000000000",
              "0xc000000000000000", "12345678901234567890", "0x5"]:
        a("id\t%s" % i)

    a("# navigation")
    for t, op, *args in [
        ("89c25", "parent"), ("89c25", "parent", "3"), ("89c25", "parent", "12"),
        ("1", "parent"), (LEAF, "parent", "16"),
        ("89c25", "child", "0"), ("89c25", "child", "3"), (LEAF, "child", "0"),
        ("89c25", "children"), ("1", "children"), ("89c25", "children", "13"),
        ("89c25", "child_range"), ("89c25", "child_range", "11"),
        ("89c25", "child_range", "9"), (LEAF, "child_range"),
        ("89c25", "next"), ("89c25", "prev"), ("1", "prev"), ("b", "next"),
        ("1", "prev_wrap"), ("b", "next_wrap"), ("89c25", "next_wrap"),
        ("89c25", "advance", "10"), ("89c25", "advance", "-10"),
        ("89c25", "advance", "1000000"), ("89c25", "advance", "-1000000"),
        ("89c25", "advance", "0"), ("1", "advance", "7"),
        ("89c25", "advance_wrap", "1000000"),
        ("89c25", "advance_wrap", "-1000000"), ("1", "advance_wrap", "-1"),
        ("b", "advance_wrap", "13"), ("3", "advance_wrap", "-8"),
        ("89c25", "range"), (LEAF, "range"), ("1", "range"),
        ("89c25", "edge"), ("1", "edge"), ("5", "edge"), (LEAF, "edge"),
        ("89c25", "vertex", "10"), ("89c25", "vertex", "3"),
        ("1", "vertex", "0"), ("89c25", "vertex", "12"),
        ("89c25", "all", "12"), ("89c25", "all", "13"), ("1", "all", "1"),
        ("89c25", "all", "11"),
        ("89c25", "contains", "89c259"), ("89c259", "contains", "89c25"),
        ("89c25", "intersects", "89c259"), ("89c25", "intersects", "89c24"),
        ("89c25", "contains", "0"), ("89c25", "lt", "89c259"),
        ("89c25", "lt", "89c25"), ("89c25", "teleport"),
    ]:
        a("\t".join(["nav", t, op] + args))
    for lv in ["0", "1", "2"]:
        a("walk\t%s" % lv)

    a("# lat/lng and points")
    for args in [
        (SF, NY), (LONDON, TOKYO), (SYDNEY, "-33.8688\t-28.7907"),
        ("0\t0", "0\t180"), ("90\t0", "-90\t0"), ("45\t190", "45\t-170"),
        ("100\t0",), ("-91\t370",), ("0\t-180",), ("12.5\t540",),
        ("37.7749\t-122.4194", "37.7749\t-122.4194"),
    ]:
        a("\t".join(["latlng"] + list(args)))
    for p in ["1\t0\t0", "0\t0\t-2", "3\t-4\t12", "1\t1\t1", "-0.5\t0.5\t0.1",
              "0\t0\t0", "1e-300\t1e-300\t0", "0.3\t-0.9\t0.31"]:
        a("point\t%s" % p)

    a("# caps")
    a("cap\t%s\t1\t37.8044\t-122.2712\t40.7128\t-74.0060" % SF)
    a("cap\t%s\t0" % SF)
    a("cap\t90\t0\t30\t70\t10\t59\t0\t-60\t45")
    a("cap\t0\t0\t90\t0\t90\t0\t-90")
    a("cap\t0\t179\t5\t0\t-178\t0\t175")
    a("cap\t-33.8688\t151.2093\t179.9")
    a("cap\t10\t20\t180")
    a("cap\t10\t20\t-1")
    a("capop\t%s\t10\tcontains\t%s\t2" % (SF, SF))
    a("capop\t%s\t2\tcontains\t%s\t10" % (SF, SF))
    a("capop\t%s\t10\tintersects\t%s\t30" % (SF, NY))
    a("capop\t%s\t10\tintersects\t%s\t40" % (SF, NY))
    a("capop\t%s\t10\tinterior_intersects\t%s\t31.3" % (SF, NY))
    a("capop\t%s\t10\tapprox\t%s\t10" % (SF, SF))
    a("capop\t%s\t10\tslice\t%s\t10" % (SF, SF))
    a("capmisc\tempty")
    a("capmisc\tfull")
    a("capmisc\theight\t%s\t0.25" % LONDON)
    a("capmisc\tarea\t%s\t1.0" % TOKYO)
    a("capmisc\tgrow\t%s\t37.8044\t-122.2712\t37.3382\t-121.8863" % SF)
    a("capmisc\tgrow\t0\t0\t0\t180")
    a("capmisc\texpanded\t%s\t1\t2" % SF)
    a("capmisc\texpanded\t%s\t90\t100" % SF)
    a("capmisc\texpanded\t%s\t1\t-2" % SF)

    a("# lat/lng rects")
    a("rect\t37.2\t-122.6\t38.0\t-121.7\t37.7749\t-122.4194\t38.0\t-122.0\t40\t-74")
    a("rect\t-40\t170\t-10\t-170\t-18.1248\t178.4501\t-20\t-175\t-20\t160")
    a("rect\t10\t20\t10\t20\t10\t20")
    a("rect\t-90\t-180\t90\t180\t0\t0")
    a("rect\t60\t-10\t35\t30\t51.5074\t-0.1278")
    a("rect\t89\t0\t89.5\t180\t89.2\t90")
    for op, *args in [
        ("union", "40", "-80", "45", "-70"), ("intersection", "37.5", "-122", "39", "-120"),
        ("contains", "37.5", "-122.5", "37.8", "-122.2"), ("intersects", "38.1", "-122", "39", "-121"),
        ("interior", "37.2", "-122.6", "37.9", "-122"), ("approx", "37.2", "-122.6", "38.0", "-121.7"),
        ("eq", "38.0", "-121.7", "37.2", "-122.6"), ("intersection", "-10", "0", "0", "10"),
        ("expanded", "1", "2"), ("expanded", "0", "1"), ("convolve", "1"),
        ("cell", "808f"), ("cell", "8085"), ("cell", "89c25"), ("cell", "1"),
    ]:
        a("\t".join(["rectop", "37.2", "-122.6", "38.0", "-121.7", op] + args))
    a("rectop\t-40\t170\t-10\t-170\tunion\t-30\t-175\t-5\t-160")
    a("rectop\t-40\t170\t-10\t-170\tintersection\t-30\t-175\t-5\t-160")
    a("rectop\t-40\t170\t-10\t-170\tcontains\t-30\t175\t-15\t-175")
    a("rectop\t-40\t170\t-10\t-170\tconvolve\t5")
    a("rectop\t80\t-20\t89\t20\tconvolve\t5")
    a("rectop\t-40\t170\t-10\t-170\tcell\t7")

    a("# intervals")
    pi = "3.141592653589793"
    for args in [
        ("0", "1", "0.5", "2", "0.25"), ("3", "-3", "-2", "2", "0.1"),
        ("-%s" % pi, pi, "1", "-1", "0"), (pi, "-%s" % pi, "0", "1", "1"),
        ("1", "1", "1", "1", "3.2"), ("-%s" % pi, "0", "0", pi, "0.5"),
        ("2", "-2", "-2.5", "2.5", "0.5"), ("0", "1", "2", "3", "0.5"),
        ("1", "2"), ("4", "0"), ("0", "-%s" % pi),
    ]:
        a("\t".join(["sint"] + list(args)))
    for args in [
        ("0", "1", "0.5", "2", "0.25"), ("1", "0", "0", "1", "0.5"),
        ("-1", "1", "-0.5", "0.5", "0"), ("2", "3", "0", "1", "1"),
        ("0", "1", "0", "1", "-1"),
    ]:
        a("\t".join(["lint"] + list(args)))
    for x, y in [("7", "6.283185307179586"), ("-3.5", "2"), ("2.5", "1"),
                 ("3.5", "1"), ("-2.5", "1"), ("1e300", "3"), ("5", "0"),
                 ("0.1", "0.3")]:
        a("drem\t%s\t%s" % (x, y))

    a("# cells")
    for t in ["1", "5", "89c25", "8085", "1000000000000004", LEAF]:
        a("subdivide\t%s" % t)
    for args in [
        ("89c25", "contains", "89c259"), ("89c259", "contains", "89c25"),
        ("89c25", "point", "40.7128", "-74.0060"), ("89c25", "point", "37", "-122"),
        ("89c25", "may", "89c24"), ("1", "edges"), ("89c25", "edges"),
        ("89c25", "cap", "40.7", "-74", "1"), ("89c25", "cap", "40.7", "-74", "0.01"),
        ("89c25", "cap", "0", "0", "100"),
    ]:
        a("\t".join(["cellop"] + list(args)))
    for args in [
        (SF, "37.8044\t-122.2712", "37.3382\t-121.8863"),
        ("0\t0", "0\t90", "90\t0"),
        ("0\t0", "0\t1e-7", "1e-7\t0"),
        ("0\t0", "0\t0", "0\t0"),
        ("10\t10", "10\t10.0000001", "10.0000001\t10"),
        ("0\t0", "0\t180", "0\t90"),
    ]:
        a("\t".join(["area"] + [x for x in args]))
    a("crossing\t0\t-10\t0\t10\t-10\t0\t10\t0")
    a("crossing\t0\t-10\t0\t10\t5\t0\t10\t0")
    a("crossing\t0\t0\t0\t10\t0\t10\t0\t20")

    a("# region coverings")
    caps = ["cap\t%s\t0.1" % SF, "cap\t%s\t2" % NY, "cap\t90\t0\t10",
            "cap\t0\t180\t30"]
    rects = ["rect\t37.2\t-122.6\t38.0\t-121.7", "rect\t-40\t170\t-10\t-170",
             "rect\t-10\t-10\t10\t10"]
    for reg in caps + rects:
        a("cover\t0\t30\t8\t1\t%s" % reg)
        a("interior\t0\t16\t8\t1\t%s" % reg)
    a("cover\t4\t10\t20\t2\t%s" % caps[0])
    a("cover\t0\t12\t4\t1\t%s" % caps[1])
    a("cover\t0\t5\t20\t1\t%s" % rects[1])
    a("cover\t10\t10\t1\t1\t%s" % caps[0])
    a("cover\t0\t30\t3\t3\t%s" % rects[2])
    a("cover\t0\t30\t1\t1\tcap\t%s\t1" % LONDON)
    a("cover\t0\t30\t8\t1\tcell\t89c25")
    a("interior\t0\t30\t8\t1\tcell\t89c25")
    a("interior\t5\t8\t30\t1\t%s" % caps[1])
    a("interior\t0\t30\t8\t1\tcap\t%s\t0" % SF)
    a("cover\t0\t30\t8\t1\tcap\t%s\t-1" % SF)
    a("cover\t0\t30\t8\t1\tcap\t%s\t180" % SF)
    a("cover\t0\t30\t8\t1\tpolygon\t1\t2")
    a("cover\t0\t31\t8\t1\t%s" % caps[0])
    a("cover\t0\t30\t8\t4\t%s" % caps[0])
    a("simple\t%s\tcap\t%s\t0.1\t12" % (SF, SF))
    a("simple\t%s\trect\t37.7\t-122.5\t37.8\t-122.4\t13" % SF)
    a("simple\t%s\tcap\t%s\t0.1\t12" % (NY, SF))

    a("# cell unions")
    for args in [
        ("89c25,89c259,89c24",),
        ("89c254,89c25c,89c251,89c257",),
        ("89c2504,89c250c,89c2514,89c251c",),
        ("1,3,5,7,9,b",),
        ("5,1,3,7",),
        ("89c25,89c25",),
        ("-",),
        ("89c25,8085", "union", "89c24,808f"),
        ("89c25,8085", "intersection", "89c254,808f,80854"),
        ("89c25,8085", "intersection", "-"),
        ("89c25", "difference", "89c254"),
        ("89c25,8085", "difference", "8085,89c2504"),
        ("1", "difference", "1"),
        ("89c25,8085", "contains", "89c254,80854"),
        ("89c25,8085", "contains", "89c254,808f"),
        ("89c25,8085", "intersects", "808f,8084"),
        ("89c25,8085", "intersects", "808f,80854"),
        ("89c25,8085", "eq", "8085,89c25"),
        ("89c25,8085", "clip", "89c"),
        ("89c25,8085", "clip", "89c2504"),
        ("89c25,8085", "has", "89c2504"),
        ("89c25,8085", "has", "89c"),
        ("89c25,8085", "hits", "89c"),
        ("89c25,8085", "point", "40.7128", "-74.0060"),
        ("89c25,8085", "point", "0", "0"),
        ("89c25,8085", "denormalize", "10", "1"),
        ("89c25,8085", "denormalize", "12", "2"),
        ("89c25,1", "denormalize", "0", "3"),
        ("89c25,8085", "rect"),
        ("-", "rect"),
        ("89c25", "expand", "8"),
        ("89c25", "expand_angle", "1", "2"),
    ]:
        a("\t".join(["union"] + list(args)))

    a("# metrics")
    for m, v in [("min_width", "0.001"), ("max_diag", "0.5"),
                 ("avg_edge", "1e-6"), ("avg_area", "1e-10"),
                 ("min_area", "0.5"), ("max_area", "0"),
                 ("min_angle_span", "-1"), ("max_angle_span", "1e-20"),
                 ("tile", "1")]:
        a("metric\t%s\t%s" % (m, v))

    a("# the place index")
    for lv in ["2", "6"]:
        a("index\t%s" % lv)
    a("near\t%s\t60\t8\t30" % SF)
    a("near\t%s\t30\t16\t30" % SF)
    a("near\t%s\t400\t8\t16" % LONDON)
    a("near\t%s\t2000\t12\t12" % LONDON)
    a("near\t%s\t50\t8\t30" % TOKYO)
    a("near\t%s\t3000\t20\t10" % SYDNEY)
    a("near\t0\t180\t2500\t10\t10")
    a("near\t90\t0\t1500\t8\t30")
    a("near\t0\t0\t1\t8\t30")
    for z, mc, ml in [("bay_area", "12", "16"), ("europe", "20", "10"),
                      ("dateline", "16", "10"), ("tokyo_bay", "8", "14"),
                      ("arctic", "10", "8"), ("face_cell", "8", "4"),
                      ("atlantis", "8", "8")]:
        a("zone\t%s\t%s\t%s" % (z, mc, ml))
    return j


def main():
    if os.path.isdir(DATA):
        shutil.rmtree(DATA)
    os.makedirs(os.path.join(DATA, "out"))
    with open(os.path.join(DATA, "places.tsv"), "w", encoding="utf-8") as fh:
        fh.write("# name\tlat\tlng\n")
        for name, lat, lng in PLACES:
            fh.write("%s\t%r\t%r\n" % (name, lat, lng))
    with open(os.path.join(DATA, "zones.tsv"), "w", encoding="utf-8") as fh:
        fh.write("# name\tregion\n")
        for z in ZONES:
            fh.write("\t".join(str(x) for x in z) + "\n")
    with open(os.path.join(DATA, "jobs.tsv"), "w", encoding="utf-8") as fh:
        for line in jobs():
            fh.write(line + "\n")
    with open(os.path.join(DATA, "files.txt"), "w", encoding="utf-8") as fh:
        fh.write("places.tsv\nzones.tsv\n")


main()
