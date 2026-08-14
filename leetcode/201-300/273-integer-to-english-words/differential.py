#!/usr/bin/env python3
"""LeetCode 273 — differential harness. Mirror of differential.kara.

Three solvers plus a shape oracle over 50,032 probes. Same generator, same
counters, same digest — line-for-line with the Kāra version so a divergence is a
compiler question, not a translation question.
"""


def small_name(n):
    return ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight",
            "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen",
            "Sixteen", "Seventeen", "Eighteen", "Nineteen"][n] if n < 20 else ""


def tens_name(t):
    return ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy",
            "Eighty", "Ninety"][t] if t < 10 else ""


def scale_name(s):
    return ["", "Thousand", "Million", "Billion"][s] if s < 4 else ""


def group_name(n):
    if n == 0:
        return ""
    if n < 20:
        return small_name(n)
    if n < 100:
        t = tens_name(n // 10)
        r = n % 10
        return t if r == 0 else t + " " + small_name(r)
    h = small_name(n // 100) + " Hundred"
    r = group_name(n % 100)
    return h if r == "" else h + " " + r


def chunker(n):
    if n == 0:
        return "Zero"
    out = ""
    rem, scale = n, 0
    while rem > 0:
        part = rem % 1000
        if part > 0:
            piece = group_name(part)
            if scale > 0:
                piece = piece + " " + scale_name(scale)
            out = piece if out == "" else piece + " " + out
        rem //= 1000
        scale += 1
    return out


def positional(n):
    if n == 0:
        return "Zero"
    digits = str(n).encode()
    length = len(digits)
    words = []
    group_nonempty = False
    i = 0
    while i < length:
        p = length - 1 - i
        place = p % 3
        scale = p // 3
        d = digits[i] - 48
        group_done = place == 0
        if place == 2:
            if d > 0:
                words.append(small_name(d))
                words.append("Hundred")
                group_nonempty = True
        if place == 1:
            if d == 1:
                u = digits[i + 1] - 48
                words.append(small_name(10 + u))
                group_nonempty = True
                i += 1
                group_done = True
            elif d >= 2:
                words.append(tens_name(d))
                group_nonempty = True
        if place == 0:
            if d > 0:
                words.append(small_name(d))
                group_nonempty = True
        if group_done:
            if group_nonempty and scale > 0:
                words.append(scale_name(scale))
            group_nonempty = False
        i += 1
    out = ""
    for w in words:
        if out != "":
            out += " "
        out += w
    return out


UNITS_T = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight",
           "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen",
           "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
TENS_T = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy",
          "Eighty", "Ninety"]
SCALE_T = ["", "Thousand", "Million", "Billion"]


def build_groups():
    g = []
    for i in range(20):
        g.append(UNITS_T[i])
    for d in range(2, 10):
        for r in range(10):
            g.append(TENS_T[d] if r == 0 else TENS_T[d] + " " + UNITS_T[r])
    for h in range(1, 10):
        for r in range(100):
            g.append(UNITS_T[h] + " Hundred" if r == 0
                     else UNITS_T[h] + " Hundred " + g[r])
    return g


def tabled(n, g, s):
    if n == 0:
        return "Zero"
    out = ""
    rem, div, scale = n, 1000000000, 3
    while div >= 1:
        part = rem // div
        if part > 0:
            if out != "":
                out += " "
            out += g[part]
            if scale > 0:
                out += " " + s[scale]
        rem %= div
        div //= 1000
        scale -= 1
    return out


def vocabulary():
    v = set(UNITS_T[1:]) | set(TENS_T[2:])
    v |= {"Hundred", "Thousand", "Million", "Billion", "Zero"}
    return v


def shape_ok(s, v):
    if s == "":
        return False
    for tok in s.split(" "):
        if tok == "" or tok not in v:
            return False
    return True


def has_zero_group(n):
    rem = n
    groups = []
    while rem > 0:
        groups.append(rem % 1000)
        rem //= 1000
    seen_nonzero_above = False
    for i in range(len(groups) - 1, -1, -1):
        if groups[i] == 0 and seen_nonzero_above:
            return True
        if groups[i] > 0:
            seen_nonzero_above = True
    return False


def main():
    g = build_groups()
    s = SCALE_T
    v = vocabulary()

    probes = list(range(0, 10001))
    pw = 1
    while pw <= 1000000000:
        probes += [pw - 1, pw, pw + 1]
        pw *= 10
    seed = 273273
    for _ in range(20000):
        seed = (seed * 1103515245 + 12345) & 2147483647
        probes.append(seed)
    for _ in range(20000):
        x, mag = 0, 1
        for gi in range(4):
            seed = (seed * 1103515245 + 12345) & 2147483647
            part = (seed // 256) % 1000
            seed = (seed * 1103515245 + 12345) & 2147483647
            if (seed // 256) % 3 == 0:
                part = 0
            if gi == 3:
                part %= 3
            x += part * mag
            mag *= 1000
        probes.append(x)
    probes.append(2147483647)

    mismatches = shape_bad = zero_group = teens = longest = digest = 0
    for x in probes:
        a = chunker(x)
        b = positional(x)
        c = tabled(x, g, s)
        if a != b or a != c:
            mismatches += 1
        if not shape_ok(a, v):
            shape_bad += 1
        if has_zero_group(x):
            zero_group += 1
        m = x % 100
        if 10 <= m <= 19:
            teens += 1
        if len(a) > longest:
            longest = len(a)
        for byte in a.encode():
            digest = (digest * 131 + byte) % 1000000007

    print(f"cases {len(probes)}")
    print(f"numbers with a ZERO GROUP below a nonzero one {zero_group}")
    print(f"numbers ending in a teen {teens}")
    print(f"longest spelling, bytes {longest}")
    print(f"shape violations {shape_bad}")
    print(f"digest {digest}")
    print(f"mismatches {mismatches}")


main()
