# LeetCode #609: Find Duplicate File in System -- Python mirror of the ★
# arm (a map from content); see find_duplicate.kara.


def find_duplicate(paths):
    by_content = {}
    for line in paths:
        parts = iter(line.split(" "))
        d = next(parts)
        for file in parts:
            open_at = file.find("(")
            name = file[0:open_at]
            content = file[open_at + 1:len(file) - 1]
            by_content.setdefault(content, []).append(f"{d}/{name}")
    groups = []
    for group in by_content.values():
        if len(group) > 1:
            groups.append(group)
    return groups


# ---- test harness ---------------------------------------------------------

def step(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def canonical(groups):
    out = [sorted(g) for g in groups]
    out.sort(key=lambda g: g[0])
    return out


def written(items):
    return "[" + ", ".join(items) + "]"


def written_groups(groups):
    return "[" + ", ".join(written(g) for g in groups) + "]"


def show(paths):
    print(f"{written(paths)} -> {written_groups(canonical(find_duplicate(paths)))}")


def random_system(dirs, most, kinds, seed):
    pool = []
    for _ in range(kinds):
        c = ""
        size = 1 + step(seed) % 6
        for _ in range(size):
            c += chr(97 + step(seed) % 3)
        pool.append(c)
    paths = []
    counter = 0
    for d in range(dirs):
        line = "root" if d == 0 else f"root/d{d}"
        files = 1 + step(seed) % most
        for _ in range(files):
            counter += 1
            line += f" f{counter}.txt({pool[step(seed) % kinds]})"
        paths.append(line)
    return paths


def summary(groups):
    s = canonical(groups)
    files = 0
    h = 0
    for group in s:
        files += len(group)
        for path in group:
            for c in path:
                h = (h * 31 + ord(c)) % 1000000007
            h = (h * 31 + 32) % 1000000007
        h = (h * 31 + 59) % 1000000007
    return f"{len(s)} groups, {files} files, checksum {h}"


def main():
    show(["root/a 1.txt(abcd) 2.txt(efgh)", "root/c 3.txt(abcd)", "root/c/d 4.txt(efgh)", "root 4.txt(efgh)"])
    show(["root/a 1.txt(abcd) 2.txt(efgh)", "root/c 3.txt(abcd)", "root/c/d 4.txt(efgh)"])
    show(["root 1.txt(a) 2.txt(b)", "root/x 3.txt(c)"])
    show(["d f1(x) f2(x) f3(x)"])
    show(["a f(z)", "b f(z)", "a/b f(y)", "c f(z)"])
    show(["r a(ab) b(abc) c(ab) d(abcd) e(abc)"])
    show(["root 1.txt(123) 2.txt(1234)", "root/n 3.txt(123)"])
    seed = [609]
    groups = 0
    files = 0
    checksum = 0
    for _ in range(300):
        dirs = 1 + step(seed) % 8
        most = 1 + step(seed) % 4
        kinds = 1 + step(seed) % 10
        found = canonical(find_duplicate(random_system(dirs, most, kinds, seed)))
        groups += len(found)
        for group in found:
            files += len(group)
            for path in group:
                for c in path:
                    checksum = (checksum * 31 + ord(c)) % 1000000007
    print(f"300 random systems: {groups} groups, {files} files, checksum {checksum}")
    print(f"5000 directories: {summary(find_duplicate(random_system(5000, 6, 2000, seed)))}")


main()
