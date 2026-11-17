# LeetCode #1598: Crawler Log Folder
# -- the bench in Python, mirroring crawler.kara: only the depth matters,
# on 2000 logs of 5000 operations, all drawn first.


def min_operations(logs):
    depth = 0
    for log in logs:
        if log == "../":
            depth = max(depth - 1, 0)
        elif log != "./":
            depth += 1
    return depth


def main():
    seed = 1598

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def one():
        r = next_random() % 8
        return "../" if r < 2 else "./" if r < 4 else f"d{r - 3}/"

    all_logs = [[one() for _ in range(5000)] for _ in range(2000)]
    check = 0
    total = 0
    for logs in all_logs:
        answer = min_operations(logs)
        total += answer
        check = (check * 31 + answer + 1) % 1000000007
    print(f"2000 logs of 5000 operations: total {total}, checksum {check}")


main()
