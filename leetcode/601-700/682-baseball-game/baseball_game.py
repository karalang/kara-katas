# LeetCode #682: Baseball Game -- a stack of the valid scores.
# Mirrors the ★ arm (baseball_game.kara) and its test harness.


def cal_points(operations):
    record = []
    for op in operations:
        if op == "+":
            record.append(record[-1] + record[-2])
        elif op == "D":
            record.append(record[-1] * 2)
        elif op == "C":
            record.pop()
        else:
            record.append(int(op))
    return sum(record)


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(text):
    print(f"[{text}] -> {cal_points(text.split(' '))}")


def random_ops(rng, n):
    limit = 1073741824
    record = []
    out = []
    while len(out) < n:
        k = len(record)
        pick = rng.next() % 10
        if pick == 0 and k >= 1:
            record.pop()
            out.append("C")
        elif pick == 1 and k >= 1 and abs(record[-1]) < limit // 2:
            record.append(record[-1] * 2)
            out.append("D")
        elif pick == 2 and k >= 2 and abs(record[-1] + record[-2]) < limit:
            record.append(record[-1] + record[-2])
            out.append("+")
        elif pick >= 3:
            x = rng.next() % 60001 - 30000
            record.append(x)
            out.append(str(x))
    return out


def main():
    for t in ["5 2 C D +", "5 -2 4 C D 9 + +", "1 C", "7", "-30000", "3 D D D D",
              "1 1 + + + + + +", "10 20 + C C C", "4 -4 + D C +",
              "30000 30000 + + + + D C"]:
        show(t)
    words = ["1", "-2", "+", "D", "C"]
    playable = 0
    total_sum = 0
    total = 1
    for n in range(1, 8):
        total *= 5
        for code in range(total):
            v = []
            c = code
            depth = 0
            ok = True
            for _ in range(n):
                w = words[c % 5]
                c //= 5
                if w == "+":
                    ok = ok and depth >= 2
                    depth += 1
                elif w == "C":
                    ok = ok and depth >= 1
                    depth -= 1
                elif w == "D":
                    ok = ok and depth >= 1
                    depth += 1
                else:
                    depth += 1
                v.append(w)
            if ok:
                playable += 1
                total_sum = (total_sum * 31 + cal_points(v) + 1000) % 1000000007
    print(f"lists of 1 to 7 over 1 -2 + D C: {playable} playable, checksum {total_sum}")
    rng = Rng(682)
    checksum = 0
    largest = 0
    zero = 0
    for _ in range(300):
        n = 1 + rng.next() % 1000
        answer = cal_points(random_ops(rng, n))
        largest = max(largest, abs(answer))
        if answer == 0:
            zero += 1
        checksum = (checksum * 31 + answer % 1000000007 + 1000000007) % 1000000007
    print(f"300 random lists: {zero} total 0, largest size {largest}, checksum {checksum}")


main()
