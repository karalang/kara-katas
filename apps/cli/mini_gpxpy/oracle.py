# Runs the files mk.py writes through gpxpy 1.6.2 (the copy in gpxpy/)
# and wrote expected.out. Each file gets gpxinfo's report (the functions
# of gpxinfo.py, unchanged but for the arguments), its XML as gpxpy
# writes it, a second parse of that XML, the other GPX version, and a
# set of track operations.
import datetime, os, sys, types, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.modules["lxml"] = None  # gpxpy prefers lxml; the port follows the stdlib ElementTree

import gpxpy  # noqa: E402
import gpxpy.geo as geo  # noqa: E402
import gpxpy.gpx as gpx_mod  # noqa: E402

info = types.ModuleType("gpxinfo")
with open(os.path.join(HERE, "gpxinfo.py"), encoding="utf-8") as f:
    exec(compile(f.read().replace("if __name__ == '__main__':", "if False:"), "gpxinfo.py", "exec"), info.__dict__)

FULL_XML = 6000


def parse(path):
    with open(path, encoding="utf-8") as f:
        return gpxpy.parse(f)


def show_xml(label, xml):
    data = xml.encode("utf-8")
    lines = xml.split("\n")
    print(f"-- {label}: {len(lines)} lines, {len(data)} bytes, crc32 {zlib.crc32(data):08x}")
    if len(data) <= FULL_XML:
        for line in lines:
            print(f"   |{line}")


def opt(x):
    return "None" if x is None else f"{x}"


def operations(path):
    g = parse(path)
    if g.get_track_points_no() == 0:
        return
    print("-- operations")
    b = g.get_bounds()
    print(f"   bounds: {opt(b.min_latitude)} {opt(b.max_latitude)} {opt(b.min_longitude)} {opt(b.max_longitude)}"
          if b else "   bounds: None")
    lo, hi = g.get_elevation_extremes()
    print(f"   elevation extremes: {opt(lo)} {opt(hi)}")
    print(f"   duration: {opt(g.get_duration())}")
    print(f"   has times: {g.has_times()}, has elevations: {g.has_elevations()}")
    data = g.get_points_data()
    print(f"   points data: {len(data)} points, the last {data[-1].distance_from_start} m from the start")
    data2 = g.get_points_data(distance_2d=True)
    print(f"   points data in 2D: the last {data2[-1].distance_from_start} m from the start")
    c = g.tracks[0].get_center()
    if c:
        n = g.get_nearest_location(c)
        print(f"   center of track 0: {c.latitude} {c.longitude}")
        print(f"   nearest to it: track {n.track_no} segment {n.segment_no} point {n.point_no} "
              f"at {n.location.latitude} {n.location.longitude}")
        near = g.get_nearest_locations(c, threshold_distance=0.05)
        print(f"   near it (5% of the length): {len(near)} passes")
    start, end = g.get_time_bounds()
    if start and end:
        mid = start + (end - start) / 2
        at = g.get_location_at(mid)
        print(f"   location at {mid}: " + ", ".join(f"{p.latitude} {p.longitude}" for p in at))
    seg = None
    for t in g.tracks:
        for s in t.segments:
            if len(s.points) >= 2 and seg is None:
                seg = s
    if seg is not None:
        p, q = seg.points[0], seg.points[1]
        print(f"   course from point 0 to 1: {p.course_between(q)} loxodromic, "
              f"{p.course_between(q, loxodromic=False)} great circle")
        print(f"   elevation angle: {opt(p.elevation_angle(q))}")
        speeds = [seg.get_speed(i) for i in range(len(seg.points))]
        known = [s for s in speeds if s is not None]
        print(f"   speeds: {len(known)} of {len(speeds)} known" +
              (f", fastest {max(known)} m/s" if known else ""))
        md = seg.get_moving_data()
        print(f"   first segment moving data: {md.moving_time} {md.stopped_time} {md.moving_distance} "
              f"{md.stopped_distance} {md.max_speed}")

    g = parse(path)
    g.simplify()
    print(f"   simplify(): {g.get_track_points_no()} points, {g.length_2d()} m in 2D")
    g = parse(path)
    g.reduce_points(min_distance=30)
    print(f"   reduce_points(min_distance=30): {g.get_track_points_no()} points")
    g = parse(path)
    g.reduce_points(max_points_no=20)
    print(f"   reduce_points(max_points_no=20): {g.get_track_points_no()} points")
    g = parse(path)
    g.smooth()
    up, down = g.get_uphill_downhill()
    print(f"   smooth(): uphill {up} downhill {down}")
    g = parse(path)
    g.smooth(vertical=True, horizontal=True, remove_extremes=True)
    print(f"   smooth(horizontal, remove_extremes): {g.get_track_points_no()} points, {g.length_2d()} m in 2D")

    g = parse(path)
    before = sum(1 for p in g.walk(only_points=True) if p.elevation is None)
    g.add_missing_elevations()
    after = sum(1 for p in g.walk(only_points=True) if p.elevation is None)
    if before:
        print(f"   add_missing_elevations(): {before} missing, {after} left")
    g = parse(path)
    before = sum(1 for p in g.walk(only_points=True) if p.time is None)
    g.add_missing_times()
    after = sum(1 for p in g.walk(only_points=True) if p.time is None)
    if before:
        print(f"   add_missing_times(): {before} missing, {after} left")
    g = parse(path)
    g.add_missing_speeds()
    print(f"   add_missing_speeds(): {sum(1 for p in g.walk(only_points=True) if p.speed is not None)} with a speed")

    g = parse(path)
    t0 = g.tracks[0]
    if t0.segments and len(t0.segments[0].points) >= 4:
        n = len(t0.segments[0].points)
        g.split(0, 0, n // 2)
        print(f"   split(0, 0, {n // 2}): {len(t0.segments)} segments of " +
              " ".join(str(len(s.points)) for s in t0.segments))
        t0.join(0)
        print(f"   join(0): {len(t0.segments)} segments, {len(t0.segments[0].points)} points in the first")

    g = parse(path)
    g.move(geo.LocationDelta(distance=1000, angle=45))
    p = next(g.walk(only_points=True))
    print(f"   moved 1000 m at 45 degrees: {p.latitude} {p.longitude}")
    g = parse(path)
    g.move(geo.LocationDelta(latitude_diff=-0.5, longitude_diff=0.25))
    p = next(g.walk(only_points=True))
    print(f"   moved by -0.5 and 0.25 degrees: {p.latitude} {p.longitude}")
    g = parse(path)
    g.adjust_time(datetime.timedelta(hours=1, seconds=30, microseconds=250), all=True)
    print(f"   adjust_time(1:00:30.000250): starts {g.get_time_bounds().start_time}")

    g = parse(path)
    if not g.has_times() and g.get_points_no() >= 2:
        start = datetime.datetime(2024, 5, 1, 9, 30, tzinfo=datetime.timezone.utc)
        g.fill_time_data_with_regular_intervals(start_time=start, end_time=start + datetime.timedelta(hours=2, seconds=7))
        print("   fill_time_data_with_regular_intervals(09:30 to 11:30:07):")
        info.args = types.SimpleNamespace(seconds=False, miles=False)
        info.print_gpx_part_info(g, indentation="     ")


def main():
    data = os.path.join(HERE, "data")
    for name in sorted(os.listdir(data)):
        path = os.path.join(data, name)
        print(f"== {name}")
        try:
            g = parse(path)
        except gpx_mod.GPXException as e:
            print(f"   {type(e).__name__}: {e}")
            continue
        info.args = types.SimpleNamespace(seconds=False, miles=False)
        info.print_gpx_info(g, name)
        if name in ("korita-zbevnica.gpx", "watch-run.gpx"):
            info.args = types.SimpleNamespace(seconds=True, miles=True)
            print("gpxinfo -s -m:")
            info.print_gpx_part_info(g)
        xml = g.to_xml()
        show_xml(f"to_xml() as GPX {g.version}", xml)
        again = gpxpy.parse(xml).to_xml()
        print("-- parsed again: " + ("the same XML" if again == xml else "DIFFERENT XML"))
        if again != xml:
            show_xml("the second XML", again)
        other = "1.0" if g.version == "1.1" else "1.1"
        show_xml(f"to_xml('{other}')", g.to_xml(other))
        show_xml("to_xml(prettyprint=False)", parse(path).to_xml(prettyprint=False))
        operations(path)


if __name__ == "__main__":
    main()
