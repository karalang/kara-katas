# LeetCode #1233 bench: the ★ arm in Python, over the same 10 lists of
# 4 · 10^4 folders and 10 passes as the Kāra bench.


def remove_subfolders(folder):
    kept = []
    for f in sorted(folder):
        if not kept or not f.startswith(kept[-1] + "/"):
            kept.append(f)
    return kept


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    letters = "abcdefgh"
    seed = [1233]
    lists = []
    for _ in range(10):
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
        lists.append(many)
    kept = 0
    for _ in range(10):
        for lst in lists:
            kept += len(remove_subfolders(lst))
    print(f"10 lists of 40000 folders, 10 passes: {kept} kept")


main()
