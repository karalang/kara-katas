# LeetCode #2511: Maximum Enemy Forts That Can Be Captured -- benchmark
# mirror of the ★ arm (forts.kara): 2000 lines of 1000 forts built once
# from its own generator, then the passes; each sets one fort of every
# line from the checksum so far, asks, and puts it back.


def capture_forts(forts):
    best = 0
    last = -1
    for i in range(len(forts)):
        if forts[i] != 0:
            if last >= 0 and forts[last] == -forts[i]:
                best = max(best, i - last - 1)
            last = i
    return best


seed = 2511


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lines = []
    for k in range(2000):
        zeros = k % 50 + 1
        line = []
        for _ in range(1000):
            r = next_random() % (zeros + 2)
            line.append(0 if r < zeros else (1 if r == zeros else -1))
        lines.append(line)
    passes = 115
    check = 0
    for p in range(passes):
        for line in lines:
            at = check % 1000
            kept = line[at]
            line[at] = (check + p) % 3 - 1
            check = (check * 31 + capture_forts(line) + p) % 1000000007
            line[at] = kept
    print(f"{passes} passes over 2000 lines of 1000 forts: checksum {check}")


main()
