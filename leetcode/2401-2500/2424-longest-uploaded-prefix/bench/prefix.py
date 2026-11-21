# LeetCode #2424: Longest Uploaded Prefix -- the bench, the ★ arm: a flag
# for each video and the prefix so far, moved on by `longest` past every
# flag set beyond it.

seed = 2424


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


class LUPrefix:
    def __init__(self, n):
        self.uploaded = [False] * (n + 2)
        self.prefix = 0

    def upload(self, video):
        self.uploaded[video] = True

    def longest(self):
        while self.uploaded[self.prefix + 1]:
            self.prefix += 1
        return self.prefix


def main():
    n = 100000
    scripts = []
    for s in range(10):
        width = 1 << (s + 3)
        order = list(range(1, n + 1))
        start = 0
        while start < n:
            end = min(start + width, n)
            for i in range(end - 1, start, -1):
                j = start + (next_random() * 32768 + next_random()) % (i - start + 1)
                order[i], order[j] = order[j], order[i]
            start = end
        scripts.append(order)
    check = 0
    for p in range(50):
        for order in scripts:
            server = LUPrefix(n)
            for v in order:
                server.upload(v)
                check = (check * 31 + server.longest() + p) % 1000000007
    print(f"50 passes over 10 scripts of 10^5 uploads: checksum {check}")


main()
