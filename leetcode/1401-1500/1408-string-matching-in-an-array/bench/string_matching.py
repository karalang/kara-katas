# LeetCode #1408 bench, Python: the same check of every word against
# every other, workload and checksum as string_matching.kara.


def string_matching(words):
    return [w for w in words if any(o != w and w in o for o in words)]


def main():
    seed = 1408
    pool = []
    for _ in range(10000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        size = 1 + seed // 65536 % 12
        word = []
        for _ in range(size):
            seed = (seed * 1103515245 + 12345) % 2147483648
            word.append(chr(97 + seed // 65536 % 3))
        pool.append("".join(word))
    check = 0
    for r in range(2000):
        at = (check + r * 7919) % 9901
        words = []
        for w in pool[at:at + 100]:
            if w not in words:
                words.append(w)
        found = string_matching(words)
        letters = sum(len(w) for w in found)
        check = (check * 131 + len(found) * 1000 + letters) % 1000000007
    print(f"2000 windows of 100 words: checksum {check}")


main()
