# Benchmark: LeetCode #1093 Statistics from a Large Sample -- the ★ arm, two
# walks over the counts. Mirrors sample_stats.kara.

def sample_stats(count):
    low = -1
    high = 0
    total = 0
    s = 0
    mode = 0
    for k in range(len(count)):
        c = count[k]
        if c == 0:
            continue
        if low < 0:
            low = k
        high = k
        s += k * c
        total += c
        if c > count[mode]:
            mode = k
    left, right = (total - 1) // 2, total // 2
    seen = 0
    median_low = -1
    median_high = -1
    for k in range(len(count)):
        seen += count[k]
        if median_low < 0 and seen > left:
            median_low = k
        if seen > right:
            median_high = k
            break
    return [float(low), float(high), s / total, (median_low + median_high) / 2.0, float(mode)]


seed = 1093


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    samples = []
    for k in range(64):
        c = [0] * 256
        for _ in range(4 + k * 4):
            p = next_random() % 256
            c[p] = next_random() * 91 % 3000000 + 1
        samples.append(c)
    modes = 0
    check = 0
    for rnd in range(10000):
        for j in range(len(samples)):
            samples[j][(rnd * 7 + j * 13) % 256] += 1
            st = sample_stats(samples[j])
            modes += int(st[4])
            for x in st:
                check = (check * 31 + int(x * 1000000.0)) % 1000000007
    print(f"10000 rounds over 64 samples: modes sum to {modes}, checksum {check}")


main()
