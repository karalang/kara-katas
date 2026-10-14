# LeetCode #621: Task Scheduler -- Python mirror of least_interval.kara.
#
# The same frame count and the same harness, printing the same lines.


def least_interval(tasks, n):
    counts = [0] * 26
    for t in tasks:
        counts[ord(t) - ord('A')] += 1
    most = max(counts)
    tied = sum(1 for c in counts if c == most)
    frame = (most - 1) * (n + 1) + tied
    return max(frame, len(tasks))


seed = 621


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(s, n):
    print(f"{s}, n = {n} -> {least_interval(list(s), n)}")


def random_tasks(size, kinds, skew):
    tasks = []
    weight = kinds * (kinds + 1) // 2 if skew else kinds
    for _ in range(size):
        r = next_random() % weight
        k = 0
        if skew:
            while r > k:
                r -= k + 1
                k += 1
        else:
            k = r
        tasks.append(chr(65 + k))
    return tasks


def main():
    show("AAABBB", 2)
    show("ACABDB", 1)
    show("AAABBB", 3)
    show("A", 100)
    show("AAAABBBCCD", 0)
    show("AAAA", 3)
    show("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 100)
    show("AAABBBCCCDD", 2)
    show("AAABCDE", 2)
    show("AAABCDEFG", 2)
    total = 0
    checksum = 0
    for _ in range(300):
        size = 1 + next_random() % 60
        kinds = 1 + next_random() % 26
        skew = next_random() % 2 == 0
        n = next_random() % 13
        tasks = random_tasks(size, kinds, skew)
        answer = least_interval(tasks, n)
        total += answer
        checksum = (checksum * 31 + answer) % 1000000007
    print(f"300 random lists: total {total}, checksum {checksum}")
    wide = random_tasks(10000, 26, True)
    print(f"10000 tasks of 26 letters, skewed, n = 100 -> {least_interval(wide, 100)}")
    narrow = random_tasks(10000, 3, False)
    print(f"10000 tasks of 3 letters, n = 100 -> {least_interval(narrow, 100)}")


main()
