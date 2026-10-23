#!/usr/bin/env python3
r"""Writes data/jobs.tsv: one job per line, a list of integer coordinates
already scaled by 1e5 (latitude and longitude times 100000), written as
space-separated `lat,lng` pairs. Keeping coordinates as integers means the port
needs no floating point: the library's _py2_round(coord * 1e5) just recovers the
same integer, so the encoded string is defined entirely by integer deltas.

For each line the job encodes the coordinates with Google's Encoded Polyline
Algorithm and decodes the result back, printing:

    enc <the polyline string>
    dec <lat,lng ... of the decoded coordinates>   (equals the input)

No polyline import here (only literal integer inputs); oracle.py replays each
line through the vendored library to produce expected.out. The lists cover a
single point, zero deltas, small and large deltas that cross the 5-bit chunk
boundary, negative coordinates and a multi-point route (the library's own
documentation example is the last)."""

JOBS = [
    [(0, 0)],
    [(0, 0), (100000, 0)],              # the (0,0) -> (1,0) doctest
    [(100000, 100000), (100000, 100000)],  # a repeated point (zero delta)
    [(4071280, -7400600)],              # New York, one point
    [(-3385230, 14937310)],             # Sydney, negative latitude
    [(5150740, -12760)],                # London, tiny longitude
    [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)],  # unit deltas around origin
    [(1234567, -7654321), (1234567, -7654321), (1300000, -7600000)],
    [(3850000, -12020000), (4070000, -12095000), (4325200, -12645300)],  # docs example
    [(4852000, 237000), (4855000, 235000), (4860000, 234000), (4858000, 236000)],  # a short Paris route
    [(9000000, 18000000), (-9000000, -18000000)],  # extreme span
    [(500000, 500000), (500050, 500050), (500100, 499950)],  # fine-grained walk
]


def main():
    import os
    os.makedirs("data", exist_ok=True)
    with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
        for job in JOBS:
            fh.write(" ".join("%d,%d" % (a, b) for (a, b) in job) + "\n")


main()
