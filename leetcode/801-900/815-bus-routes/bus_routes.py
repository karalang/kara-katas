# LeetCode 815 — Bus Routes, breadth-first search over buses (mirror of the ★ arm).
from collections import deque


def num_buses_to_destination(routes, source, target):
    if source == target:
        return 0
    buses_at = {}
    for bus, route in enumerate(routes):
        for stop in route:
            buses_at.setdefault(stop, []).append(bus)
    if source not in buses_at:
        return -1
    taken = [False] * len(routes)
    queue = deque()
    for bus in buses_at[source]:
        taken[bus] = True
        queue.append((bus, 1))
    seen = set()
    while queue:
        bus, count = queue.popleft()
        for stop in routes[bus]:
            if stop == target:
                return count
            if stop in seen:
                continue
            seen.add(stop)
            for nxt in buses_at[stop]:
                if not taken[nxt]:
                    taken[nxt] = True
                    queue.append((nxt, count + 1))
    return -1


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_routes(n, longest, stops):
    routes = []
    for _ in range(n):
        length = 1 + next_random() % longest
        on = set()
        route = []
        while len(route) < length and len(route) < stops:
            stop = next_random() % stops
            if stop not in on:
                on.add(stop)
                route.append(stop)
        routes.append(route)
    return routes


def show(routes, source, target):
    text = f"{routes}"
    answer = num_buses_to_destination(routes, source, target)
    print(f"routes = {text}, {source} to {target} -> {answer}")


def main():
    global seed
    show([[1, 2, 7], [3, 6, 7]], 1, 6)
    show([[7, 12], [4, 5, 15], [6], [15, 19], [9, 12, 13]], 15, 12)
    show([[1, 2, 3]], 2, 2)
    show([[1, 2, 3]], 9, 9)
    show([[1, 2, 3]], 9, 2)
    show([[1, 2, 3]], 1, 3)
    show([[1, 2], [2, 3], [3, 4], [4, 5], [1, 5]], 1, 4)
    show([[0, 1, 2, 3, 4, 5], [5, 6], [2, 6]], 0, 6)
    show([[1, 2], [3, 4]], 1, 4)
    seed = 815
    routes = random_routes(500, 400, 1000000)
    source, target = routes[0][0], routes[499][len(routes[499]) - 1]
    answer = num_buses_to_destination(routes, source, target)
    print(f"500 random routes, {source} to {target} -> {answer}")
    chain = []
    for i in range(500):
        chain.append([(i + 1) * 1000 if j == 199 else i * 1000 + j * 5 for j in range(200)])
    print(f"a chain of 500 routes -> {num_buses_to_destination(chain, 0, 499990)}")
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 10
        stops = 2 + next_random() % 25
        routes = random_routes(n, 6, stops)
        source = next_random() % (stops + 2)
        target = next_random() % (stops + 2)
        answer = num_buses_to_destination(routes, source, target)
        total += answer
        check = (check * 131 + answer + 2) % 1000000007
    print(f"300 random rounds of 1 to 10 routes: total {total}, checksum {check}")


main()
