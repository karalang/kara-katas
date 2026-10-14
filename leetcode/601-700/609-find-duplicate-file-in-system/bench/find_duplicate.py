# Benchmark mirror for #609: the same workload and algorithm as
# find_duplicate.kara (a map from content to paths).


def find_duplicate(paths):
    by_content = {}
    for line in paths:
        parts = line.split(" ")
        d = parts[0]
        for f in parts[1:]:
            open_ = f.index("(")
            by_content.setdefault(f[open_ + 1:-1], []).append(d + "/" + f[:open_])
    return [g for g in by_content.values() if len(g) > 1]


seed = 609


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    systems = 10
    rounds = 300
    pool = []
    for _ in range(3000):
        size = 8 + step() % 13
        pool.append("".join(chr(97 + step() % 4) for _ in range(size)))
    every = []
    for s in range(systems):
        paths = []
        counter = 0
        for d in range(2000):
            line = f"root/s{s}/d{d}"
            for _ in range(1 + step() % 6):
                counter += 1
                line += f" f{counter}.txt({pool[step() % 3000]})"
            paths.append(line)
        every.append(paths)
    groups = files = checksum = 0
    for r in range(rounds):
        found = find_duplicate(every[(r * 3) % systems])
        groups += len(found)
        for g in found:
            files += len(g)
            length = sum(len(p) for p in g)
            checksum = (checksum + len(g) * length) % 1000000007
    print(f"{systems} systems, {rounds} rounds: {groups} groups, {files} files, checksum {checksum}")


main()
