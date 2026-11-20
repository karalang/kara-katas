# LeetCode #1233: Remove Sub-Folders from the Filesystem -- Python mirror of
# the ★ arm: sorted, each folder kept unless it begins with the last kept
# folder and a `/`.


def remove_subfolders(folder):
    kept = []
    for f in sorted(folder):
        if not kept or not f.startswith(kept[-1] + "/"):
            kept.append(f)
    return kept


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def folders(count, depth, seed):
    names = ["a", "b", "ab", "ba"]
    seen = set()
    out = []
    for _ in range(count):
        d = next_random(seed) % depth + 1
        f = ""
        for _ in range(d):
            f = f + "/" + names[next_random(seed) % 4]
        if f not in seen:
            seen.add(f)
            out.append(f)
    return out


def show(v):
    return "[" + ", ".join(v) + "]"


def main():
    print(show(sorted(remove_subfolders(["/a", "/a/b", "/c/d", "/c/d/e", "/c/f"]))))
    print(show(sorted(remove_subfolders(["/a", "/a/b/c", "/a/b/d"]))))
    print(show(sorted(remove_subfolders(["/a/b/c", "/a/b/ca", "/a/b/d"]))))
    print(show(sorted(remove_subfolders(["/x"]))))
    seed = [1233]
    total = 0
    check = 0
    for _ in range(1000):
        count = next_random(seed) % 30 + 1
        kept = sorted(remove_subfolders(folders(count, 4, seed)))
        total += len(kept)
        for f in kept:
            for c in f:
                check = (check * 131 + ord(c)) % 1000000007
            check = (check * 131 + 7) % 1000000007
        check = (check * 131 + 9) % 1000000007
    print(f"1000 random lists: {total} kept, checksum {check}")
    letters = "abcdefgh"
    seen = set()
    many = []
    while len(many) < 40000:
        d = next_random(seed) % 4 + 1
        f = ""
        for level in range(d):
            f += "/"
            for _ in range(4 if level == 0 else 2):
                f += letters[next_random(seed) % 8]
        if f not in seen:
            seen.add(f)
            many.append(f)
    kept = sorted(remove_subfolders(many))
    print(f"40000 folders: {len(kept)} kept, the first {kept[0]} and the last {kept[-1]}")


main()
