# LeetCode #1054: Distant Barcodes -- Python mirror of bench/barcodes.kara.

seed = 1054


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def rearrange_barcodes(barcodes):
    n = len(barcodes)
    top = max(barcodes)
    counts = [0] * (top + 1)
    for b in barcodes:
        counts[b] += 1
    most = 0
    for v in range(1, top + 1):
        if counts[v] > counts[most]:
            most = v
    answer = [0] * n
    place = 0
    v = most
    nxt = 1
    for _ in range(n):
        while counts[v] == 0:
            v = nxt
            nxt += 1
        answer[place] = v
        counts[v] -= 1
        place += 2
        if place >= n:
            place = 1
    return answer


def main():
    count, n, rounds = 200, 20000, 25
    all_ = []
    for _ in range(count):
        common = next_random() % 10000 + 1
        copies = next_random() % 9000 + 1
        barcodes = [common] * copies
        for _ in range(copies, n):
            barcodes.append(next_random() % 10000 + 1)
        all_.append(barcodes)
    total = 0
    check = 0
    for _ in range(rounds):
        for barcodes in all_:
            answer = rearrange_barcodes(barcodes)
            h = 0
            for k in range(0, n, 97):
                h = (h * 10007 + answer[k]) % 1000000007
            total += answer[1]
            check = (check * 131 + h) % 1000000007
    print(f"{count} arrays of {n} barcodes, {rounds} rounds: total {total}, checksum {check}")


main()
