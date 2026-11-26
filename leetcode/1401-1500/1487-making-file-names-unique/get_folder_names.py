# LeetCode #1487: Making File Names Unique -- the Python mirror of
# get_folder_names.kara: one dict from each name taken to the next suffix
# worth trying for it


def get_folder_names(names):
    nxt = {}
    out = []
    for name in names:
        if name not in nxt:
            nxt[name] = 1
            out.append(name)
        else:
            k = nxt[name]
            while f"{name}({k})" in nxt:
                k += 1
            made = f"{name}({k})"
            nxt[name] = k + 1
            nxt[made] = 1
            out.append(made)
    return out


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw_name(bases):
    b = next_random() % bases
    name = f"{chr(ord('a') + b % 26)}{b // 26}"
    for _ in range(2):
        if next_random() % 3 == 0:
            name = f"{name}({1 + next_random() % 3})"
    return name


def draw(n, bases):
    return [draw_name(bases) for _ in range(n)]


def fold(check, folders):
    h = check
    for f in folders:
        for b in f.encode():
            h = (h * 131 + b) % 1000000007
        h = (h * 131 + 7) % 1000000007
    return h


def main():
    global seed
    examples = [
        ["pes", "fifa", "gta", "pes(2019)"],
        ["gta", "gta(1)", "gta", "avalon"],
        ["onepiece", "onepiece(1)", "onepiece(2)", "onepiece(3)", "onepiece"],
        ["wano", "wano", "wano", "wano"],
        ["kaido", "kaido(1)", "kaido", "kaido(1)"],
    ]
    for names in examples:
        print(",".join(get_folder_names(names)))
    edges = [["a"], ["a(1)", "a(1)"], ["a", "a", "a(1)"], ["b"] * 11 + ["b(10)", "b"]]
    print(" | ".join(",".join(get_folder_names(e)) for e in edges))
    made = get_folder_names(["x"] * 50000)
    seed = 1487
    renamed = get_folder_names(draw(50000, 300))
    print(f"50000 names: last {made[49999]}, checksum {fold(0, made)} | checksum {fold(0, renamed)}")
    check = 0
    for _ in range(2000):
        n = 1 + next_random() % 30
        bases = 1 + next_random() % 6
        check = fold(check, get_folder_names(draw(n, bases)))
    print(f"2000 random lists: checksum {check}")


main()
