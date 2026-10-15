# LeetCode #682: Baseball Game -- a stack of the valid scores. Bench.


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


def main():
    count, rounds = 200, 30
    seed = 682

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def random_ops(n):
        limit = 1073741824
        record = []
        out = []
        while len(out) < n:
            k = len(record)
            pick = next_random() % 10
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
                x = next_random() % 60001 - 30000
                record.append(x)
                out.append(str(x))
        return out

    lists = [random_ops(5000) for _ in range(count)]
    total = 0
    for r in range(rounds):
        for k in range(count):
            at = (k * 7 + r) % count
            points = cal_points(lists[at])
            total = (total * 31 + points % 1000000007 + 1000000007) % 1000000007
    print(f"{count * rounds} games scored, checksum {total}")


main()
