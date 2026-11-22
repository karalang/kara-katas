# LeetCode #2747: Count Zero Request Servers -- the bench (servers.kara in
# Python): the logs sorted by time, the queries in time order, and a
# window of logs sliding forward with a count for each server.


def count_servers(n, logs, x, queries):
    by_time = sorted((log[1], log[0]) for log in logs)
    order = sorted(range(len(queries)), key=lambda i: queries[i])
    requests = [0] * (n + 1)
    busy = 0
    answers = [0] * len(queries)
    start = end = 0
    total = len(by_time)
    for i in order:
        q = queries[i]
        while end < total and by_time[end][0] <= q:
            server = by_time[end][1]
            if requests[server] == 0:
                busy += 1
            requests[server] += 1
            end += 1
        while start < end and by_time[start][0] < q - x:
            server = by_time[start][1]
            requests[server] -= 1
            if requests[server] == 0:
                busy -= 1
            start += 1
        answers[i] = n - busy
    return answers


seed = 2747


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds, n = 10, 3, 100000
    cases = []
    for _ in range(count):
        x = (next_random() * 32768 + next_random()) % 100000 + 1
        logs = []
        for _ in range(100000):
            server = next_random() % n + 1
            time = (next_random() * 32768 + next_random()) % 1000000 + 1
            logs.append([server, time])
        queries = [x + 1 + (next_random() * 32768 + next_random()) % (1000000 - x) for _ in range(100000)]
        cases.append((logs, x, queries))
    total = check = 0
    for r in range(rounds):
        for logs, x, queries in cases:
            for a in count_servers(n, logs, x, queries):
                total += a
                check = (check * 31 + a + r) % 1000000007
    print(f"{count} cases of 100000 logs and queries, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
