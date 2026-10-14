# LeetCode #621: Task Scheduler -- Python mirror of the Kāra bench.
#
# The ★ arm's frame count over the same lists and rounds.


def least_interval(tasks, n):
    counts = [0] * 26
    for t in tasks:
        counts[ord(t) - 65] += 1
    most = 0
    for c in counts:
        if c > most:
            most = c
    tied = 0
    for c in counts:
        if c == most:
            tied += 1
    frame = (most - 1) * (n + 1) + tied
    return max(frame, len(tasks))


seed = 621


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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
    lists = 100
    rounds = 30000
    all_lists = []
    for i in range(lists):
        kinds = 1 + next_random() % 26
        all_lists.append(random_tasks(10000, kinds, i % 2 == 0))
    total = 0
    checksum = 0
    for r in range(rounds):
        answer = least_interval(all_lists[(r * 7) % lists], r % 101)
        total += answer
        checksum = (checksum * 31 + answer) % 1000000007
    print(f"{lists} lists, {rounds} rounds: total {total}, checksum {checksum}")


main()
