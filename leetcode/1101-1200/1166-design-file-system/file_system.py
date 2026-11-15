# LeetCode #1166: Design File System -- the ★ arm and its harness in Python.
# `python3 file_system.py lit` runs the statement read literally instead:
# the made paths kept in a list, walked for every call.
import sys

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

class Lit:
    """The statement read literally: a list of (path, value) made so far,
    each check a walk of the whole list."""
    def __init__(self):
        self.made = []
    def has(self, p):
        for q, _ in self.made:
            if q == p:
                return True
        return False
    def create_path(self, path, value):
        parts = path.split("/")
        if parts[0] != "" or len(parts) < 2 or any(x == "" for x in parts[1:]):
            return False
        if self.has(path):
            return False
        if len(parts) > 2 and not self.has("/".join(parts[:-1])):
            return False
        self.made.append((path, value))
        return True
    def get(self, path):
        for q, v in self.made:
            if q == path:
                return v
        return -1

S = [0]
def nr():
    S[0] = (S[0] * 1103515245 + 12345) % 2147483648
    return S[0] // 65536

def run(ops, cls=FileSystem):
    fs = cls()
    out = []
    for op in ops:
        parts = op.split(" ")
        if parts[0] == "c":
            out.append(1 if fs.create_path(parts[1], int(parts[2])) else 0)
        else:
            out.append(fs.get(parts[1]))
    return out

def random_path(depth, k):
    names = ["a", "b", "c", "leet", "code", "x"]
    parts = 1 + nr() % depth
    p = ""
    for _ in range(parts):
        p = p + "/" + names[nr() % k]
    return p

def main(cls):
    def show(ops):
        a = run(ops, cls)
        print(f"{'; '.join(ops)} -> {' '.join(str(x) for x in a)}")
    show(["c /a 1", "g /a"])
    show(["c /leet 1", "c /leet/code 2", "g /leet/code", "c /c/d 1", "g /c"])
    show(["c /a 1", "c /a 2", "g /a"])
    show(["g /a"])
    show(["c /a/b 1", "c /a 2", "c /a/b 3", "g /a/b"])
    show(["c /le 1", "c /leet 2", "c /le/et 3", "g /le", "g /leet", "g /le/et", "g /leet/et"])
    S[0] = 1166
    made = 0; check = 0
    for _ in range(300):
        k = 1 + nr() % 6
        n = 1 + nr() % 60
        ops = []
        for i in range(n):
            p = random_path(4, k)
            ops.append(f"g {p}" if nr() % 3 == 0 else f"c {p} {i + 1}")
        for i, a in enumerate(run(ops, cls)):
            if ops[i].startswith("c"):
                made += a
            check = (check * 31 + a + 2) % 1000000007
    print(f"300 random runs: made {made}, checksum {check}")
    ops = []
    p = ""
    for i in range(33):
        p = p + "/" + f"d{i % 7}"
        ops.append(f"c {p} {i}")
    S[0] = 11662
    while len(ops) < 10000:
        q = random_path(3, 6)
        ops.append(f"c {q} {len(ops)}" if len(ops) % 2 == 0 else f"g {q}")
    answers = run(ops, cls)
    total = sum(1 for a in answers if a >= 0)
    print(f"10000 operations: {total} not -1, sum {sum(answers)}")

main(Lit if len(sys.argv) > 1 else FileSystem)
