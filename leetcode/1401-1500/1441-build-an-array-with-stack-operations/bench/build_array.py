# The Python mirror of build_array.kara.


def build_array(target, n):
    ops = []
    nxt = 0
    for x in range(1, n + 1):
        if nxt == len(target):
            break
        ops.append("Push")
        if target[nxt] == x:
            nxt += 1
        else:
            ops.append("Pop")
    return ops


def main():
    seed = 1441
    targets = []
    for _ in range(1000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        keep = 1 + seed // 65536 % 100
        target = []
        for x in range(1, 101):
            seed = (seed * 1103515245 + 12345) % 2147483648
            if seed // 65536 % 100 < keep:
                target.append(x)
        if not target:
            target.append(100)
        targets.append(target)
    check = 0
    for _ in range(200):
        for target in targets:
            h = 0
            for op in build_array(target, 100):
                h = (h * 3 + (1 if op == "Push" else 2)) % 1000000007
            check = (check * 131 + h) % 1000000007
    print(f"2 * 10^5 targets: checksum {check}")


main()
