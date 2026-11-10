# LeetCode #2103: Rings and Rods -- bench, Python mirror of rings.kara.


def count_points(rings):
    b = rings.encode()
    masks = [0] * 10
    i = 0
    while i < len(b):
        c = b[i]
        bit = 1 if c == 82 else 2 if c == 71 else 4
        masks[b[i + 1] - 48] |= bit
        i += 2
    return sum(1 for m in masks if m == 7)


seed = 2103


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


strings = []
for s in range(4096):
    rods = 10 if s % 2 == 0 else 3
    parts = []
    for _ in range(100):
        parts.append("RGB"[next_random() % 3])
        parts.append(chr(48 + next_random() % rods))
    strings.append("".join(parts))
total = 0
check = 0
for k in range(300000):
    got = count_points(strings[k * 7919 % 4096])
    total += got
    check = (check * 31 + got) % 1000000007
print(f"300000 counts: {total} rods with all three, checksum {check}")
