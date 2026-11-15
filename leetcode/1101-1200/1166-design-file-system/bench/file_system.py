# LeetCode #1166: Design File System -- the ★ arm's bench in Python: one
# dict from a made path to its value.


class FileSystem:
    def __init__(self):
        self.paths = {}

    def create_path(self, path, value):
        if len(path) == 0 or path == "/" or path in self.paths:
            return False
        parent = path[:path.rfind("/")]
        if len(parent) > 0 and parent not in self.paths:
            return False
        self.paths[path] = value
        return True

    def get(self, path):
        return self.paths.get(path, -1)


seed = 1166


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    names = ["a", "b", "ab", "le", "leet", "code"]
    paths = []
    creates = []
    for _ in range(16):
        ps = []
        cs = []
        for _ in range(10000):
            parts = 1 + next_random() % 5
            p = ""
            for _ in range(parts):
                p = p + "/" + names[next_random() % 6]
            ps.append(p)
            cs.append(next_random() % 4 != 0)
        paths.append(ps)
        creates.append(cs)
    made = 0
    check = 0
    for _ in range(100):
        for k in range(16):
            start = next_random() % 5000
            fs = FileSystem()
            ps = paths[k]
            cs = creates[k]
            for i in range(start, 10000):
                if cs[i]:
                    a = 1 if fs.create_path(ps[i], i) else 0
                    made += a
                else:
                    a = fs.get(ps[i])
                check = (check * 31 + a + 2) % 1000000007
    print(f"100 rounds over 16 lists of 10^4 operations: made {made}, checksum {check}")


main()
