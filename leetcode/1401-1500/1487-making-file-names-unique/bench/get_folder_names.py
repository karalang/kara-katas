# LeetCode #1487: Making File Names Unique -- bench, the Python twin of
# get_folder_names.kara.


def get_folder_names(names):
    nxt = {}
    out = []
    for name in names:
        if name not in nxt:
            nxt[name] = 1
            out.append(name)
            continue
        k = nxt[name]
        while f"{name}({k})" in nxt:
            k += 1
        made = f"{name}({k})"
        nxt[name] = k + 1
        nxt[made] = 1
        out.append(made)
    return out


seed = 1487


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def name_of(b, suffix):
    base = f"{chr(ord('a') + b % 26)}{b // 26}"
    return base if suffix == 0 else f"{base}({suffix})"


def main():
    names = []
    for _ in range(50000):
        b = next_random() % 3000
        s = next_random() % 9
        names.append(name_of(b, s + 1 if s < 3 else 0))
    check = 0
    for p in range(20):
        names[check % 50000] = name_of(check % 3000, check % 4)
        for f in get_folder_names(names):
            for b in f.encode():
                check = (check * 131 + b) % 1000000007
        check = (check + p) % 1000000007
    print(f"20 passes over 50000 names: checksum {check}")


main()
