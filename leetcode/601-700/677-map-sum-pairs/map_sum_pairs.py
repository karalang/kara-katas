# LeetCode #677: Map Sum Pairs -- a map of the keys, scanned for each
# sum.
# Mirrors the ★ arm (map_sum_pairs.kara) and its test harness.


class MapSum:
    def __init__(self):
        self.values = {}

    def insert(self, key, val):
        self.values[key] = val

    def sum(self, prefix):
        total = 0
        for k, v in self.values.items():
            if k.startswith(prefix):
                total += v
        return total


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def run_all(script):
    m = MapSum()
    out = ["null"]
    for op in script.split(";"):
        parts = op.split(" ")
        if parts[0] == "insert":
            m.insert(parts[1], int(parts[2]))
            out.append("null")
        else:
            out.append(str(m.sum(parts[1])))
    return "[" + ",".join(out) + "]"


def random_word(rng, most, letters):
    n = 1 + rng.next() % most
    return "".join(chr(97 + rng.next() % letters) for _ in range(n))


def main():
    print(run_all("insert apple 3;sum ap;insert app 2;sum ap"))
    print(run_all("insert apple 3;sum apple;sum apples;insert apple 2;sum ap"))
    print(run_all("insert a 1;insert b 2;insert ab 3;sum a;sum b;sum c;sum ab"))
    print(run_all("insert aa 5;insert a 7;sum a;insert aa 1;sum a;sum aa;sum aaa"))
    print(run_all("sum a;insert z 1000;sum z;sum zz"))
    long = "y" * 50
    print(run_all(f"insert {long} 1000;insert {long[:49]} 999;sum y;sum {long};sum {long[:25]}"))
    rng = Rng(677)
    s = 0
    calls = 0
    for c in range(300):
        letters = 2 + c % 3
        most = 1 + c % 6
        m = MapSum()
        for _ in range(50):
            calls += 1
            if rng.next() % 2 == 0:
                m.insert(random_word(rng, most, letters), 1 + rng.next() % 1000)
            else:
                s = (s * 31 + m.sum(random_word(rng, most, letters))) % 1000000007
    print(f"{calls} random calls: checksum {s}")


main()
