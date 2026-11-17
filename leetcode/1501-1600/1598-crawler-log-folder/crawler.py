# LeetCode #1598: Crawler Log Folder -- mirrors crawler.kara: only the
# depth matters.


def min_operations(logs):
    depth = 0
    for log in logs:
        if log == "../":
            depth = max(depth - 1, 0)
        elif log != "./":
            depth += 1
    return depth


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_logs(n, seed):
    out = []
    for _ in range(n):
        r = next_random(seed) % 8
        out.append("../" if r < 2 else "./" if r < 4 else f"d{r - 3}/")
    return out


def batch(count, most, seed):
    check = 0
    total = 0
    for _ in range(count):
        n = next_random(seed) % most + 1
        answer = min_operations(random_logs(n, seed))
        total += answer
        check = (check * 31 + answer + 1) % 1000000007
    print(f"{count} logs of up to {most} operations: total {total}, checksum {check}")


def main():
    examples = [
        ["d1/", "d2/", "../", "d21/", "./"],
        ["d1/", "d2/", "./", "d3/", "../", "d31/"],
        ["d1/", "../", "../", "../"],
        ["./"],
        ["../", "../", "x/"],
        ["a/"] * 1000,
    ]
    for logs in examples:
        shown = f'["a/"; {len(logs)}]' if len(logs) > 6 else "[" + ", ".join(logs) + "]"
        print(f"{shown} -> {min_operations(logs)}")
    seed = [1598]
    batch(3000, 8, seed)
    batch(300, 100, seed)
    batch(30, 1000, seed)


main()
