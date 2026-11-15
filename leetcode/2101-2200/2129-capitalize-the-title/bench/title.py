# LeetCode #2129: Capitalize the Title -- the benchmark, the same
# algorithm as title.kara.


def capitalize_title(title):
    words = []
    for w in title.split(" "):
        lower = w.lower()
        words.append(lower if len(lower) <= 2 else lower[:1].upper() + lower[1:])
    return " ".join(words)


seed = 2129


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    titles = []
    for _ in range(1000):
        t = bytearray()
        while True:
            n = next_random() % 6 + 1
            if len(t) + 1 + n > 100:
                break
            if t:
                t.append(32)
            for _ in range(n):
                k = next_random() % 52
                t.append(97 + k if k < 26 else 39 + k)
        titles.append(t)
    capitals = 0
    check = 0
    for rnd in range(200):
        for k in range(1000):
            t = titles[k]
            p = next_random() % len(t)
            if t[p] == 32:
                p -= 1
            t[p] ^= 32
            answer = capitalize_title(t.decode())
            for b in answer.encode():
                if 65 <= b <= 90:
                    capitals += 1
                check = (check * 31 + b + rnd) % 1000000007
    print(f"200000 titles: {capitals} capitals, checksum {check}")


main()
