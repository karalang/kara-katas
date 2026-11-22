# LeetCode #2747: Count Zero Request Servers -- the ★ arm in Python
# (servers.kara): the logs sorted by time, the queries in time order, and
# a window of logs [q - x, q] sliding forward with a count for each server.


def count_servers(n, logs, x, queries):
    by_time = sorted((log[1], log[0]) for log in logs)
    order = sorted(range(len(queries)), key=lambda i: queries[i])
    requests = [0] * (n + 1)
    busy = 0
    answers = [0] * len(queries)
    start = end = 0
    for i in order:
        q = queries[i]
        while end < len(by_time) and by_time[end][0] <= q:
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


def random_case(n, most, x, last):
    logs_count = next_random() % most + 1
    queries_count = next_random() % most + 1
    logs = []
    for _ in range(logs_count):
        server = next_random() % n + 1
        time = (next_random() * 32768 + next_random()) % last + 1
        logs.append([server, time])
    queries = [x + 1 + (next_random() * 32768 + next_random()) % max(last - x, 1) for _ in range(queries_count)]
    return logs, queries


def fold(answers, acc):
    for a in answers:
        acc[0] += a
        acc[1] = (acc[1] * 31 + a) % 1000000007


def main():
    print(count_servers(3, [[1, 3], [2, 6], [1, 5]], 5, [10, 11]))
    print(count_servers(3, [[2, 4], [2, 1], [1, 2], [3, 1]], 2, [3, 4]))
    print(count_servers(4, [[1, 5], [2, 10], [3, 4]], 5, [10, 11, 15, 16]))
    acc = [0, 0]
    for _ in range(1000):
        n = next_random() % 10 + 1
        x = next_random() % 10 + 1
        logs, queries = random_case(n, 20, x, 30)
        fold(count_servers(n, logs, x, queries), acc)
    print(f"1000 small cases: answers sum to {acc[0]}, checksum {acc[1]}")
    acc = [0, 0]
    for _ in range(3):
        x = (next_random() * 32768 + next_random()) % 100000 + 1
        logs, queries = random_case(1000, 3000, x, 1000000)
        fold(count_servers(1000, logs, x, queries), acc)
    print(f"3 cases of 3000 logs: answers sum to {acc[0]}, checksum {acc[1]}")


main()
