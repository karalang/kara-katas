# LeetCode #1601: Maximum Number of Achievable Transfer Requests
# -- the bench in Python, mirroring transfers.kara: every subset of the
# requests as a bit mask, a subset no larger than the best skipped, on
# 100 problems of 16 requests among 6 buildings, all drawn first.


def maximum_requests(n, requests):
    r = len(requests)
    best = 0
    for mask in range(1 << r):
        size = bin(mask).count("1")
        if size <= best:
            continue
        net = [0] * n
        for i in range(r):
            if mask >> i & 1:
                net[requests[i][0]] -= 1
                net[requests[i][1]] += 1
        if all(d == 0 for d in net):
            best = size
    return best


def main():
    seed = 1601

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    problems = []
    for _ in range(100):
        requests = []
        for _ in range(16):
            a = next_random() % 6
            b = next_random() % 6
            requests.append([a, b])
        problems.append(requests)
    check = 0
    total = 0
    for requests in problems:
        answer = maximum_requests(6, requests)
        total += answer
        check = (check * 31 + answer + 1) % 1000000007
    print(f"100 problems of 16 requests among 6 buildings: total {total}, checksum {check}")


main()
