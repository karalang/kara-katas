# LeetCode #1520: Maximum Number of Non-Overlapping Substrings -- the
# Python mirror of the ★ arm (substrings.kara): each letter's span is grown
# until it holds every occurrence of every letter inside it, and dropped if
# it would have to grow left; a span starting after the last one taken is
# added, one starting inside it replaces it.


def max_num_of_substrings(s):
    b = s.encode()
    n = len(b)
    first = [n] * 26
    last = [-1] * 26
    for i in range(n):
        c = b[i] - 97
        first[c] = min(first[c], i)
        last[c] = i
    spans = []
    right = -1
    for i in range(n):
        c = b[i] - 97
        if i != first[c]:
            continue
        end = last[c]
        ok = True
        j = i
        while j <= end:
            d = b[j] - 97
            if first[d] < i:
                ok = False
                break
            end = max(end, last[d])
            j += 1
        if not ok:
            continue
        if i > right:
            spans.append((i, end))
        else:
            spans[-1] = (i, end)
        right = end
    return [s[a:e + 1] for a, e in spans]


class Seed:
    def __init__(self, v):
        self.v = v


def next_random(seed):
    seed.v = (seed.v * 1103515245 + 12345) % 2147483648
    return seed.v // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def show(s):
    parts = sorted(max_num_of_substrings(s))
    return "[" + ",".join(parts) + "]"


def batch(count, most, letters, seed):
    check = 0
    for _ in range(count):
        n = next_random(seed) % most + 1
        s = "".join(chr(97 + next_random(seed) % letters) for _ in range(n))
        for b in show(s).encode():
            check = mix(check, b)
    return check


def main():
    print(f"example 1, adefaddaccc -> {show('adefaddaccc')}")
    print(f"example 2, abbaccd -> {show('abbaccd')}")
    print(f"one letter, zzz -> {show('zzz')}")
    print(f"nested, abacbdcd -> {show('abacbdcd')}")
    seed = Seed(1520)
    print(f"3000 strings of 1 to 12 over 4 letters: checksum {batch(3000, 12, 4, seed)}")
    print(f"30 strings of 1 to 30000 over 26 letters: checksum {batch(30, 30000, 26, seed)}")


main()
