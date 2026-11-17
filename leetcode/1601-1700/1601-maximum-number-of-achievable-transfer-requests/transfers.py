# LeetCode #1601: Maximum Number of Achievable Transfer Requests
# -- mirrors transfers.kara: every subset of the requests as a bit mask.


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


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def batch(count, most_buildings, most_requests, seed):
    check = 0
    total = 0
    for _ in range(count):
        n = next_random(seed) % most_buildings + 1
        r = next_random(seed) % most_requests + 1
        requests = []
        for _ in range(r):
            a = next_random(seed) % n
            b = next_random(seed) % n
            requests.append([a, b])
        answer = maximum_requests(n, requests)
        total += answer
        check = (check * 31 + answer + 1) % 1000000007
    print(f"{count} problems of up to {most_buildings} buildings and {most_requests} requests: total {total}, checksum {check}")


def show(requests):
    return "[" + ", ".join(f"[{a}, {b}]" for a, b in requests) + "]"


def main():
    examples = [
        (5, [[0, 1], [1, 0], [0, 1], [1, 2], [2, 0], [3, 4]]),
        (3, [[0, 0], [1, 2], [2, 1]]),
        (4, [[0, 3], [3, 1], [1, 2], [2, 0]]),
        (1, [[0, 0]]),
        (2, [[0, 1]]),
        (20, [[i, (i + 1) % 16] for i in range(16)]),
    ]
    for n, requests in examples:
        shown = f"{len(requests)} requests in a ring" if len(requests) > 6 else show(requests)
        print(f"{n}, {shown} -> {maximum_requests(n, requests)}")
    seed = [1601]
    batch(3000, 4, 5, seed)
    batch(300, 8, 10, seed)
    batch(10, 20, 16, seed)


main()
