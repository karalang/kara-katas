# LeetCode #1066: Campus Bikes II -- the benchmark, the same table over
# the sets of bikes taken as campus_bikes.kara.
seed = 1066
INF = 1 << 62


def assign_bikes(workers, bikes):
    n, m = len(workers), len(bikes)
    best = [INF] * (1 << m)
    best[0] = 0
    answer = INF
    for mask in range(1 << m):
        if best[mask] == INF:
            continue
        w = bin(mask).count("1")
        if w == n:
            answer = min(answer, best[mask])
            continue
        wx, wy = workers[w]
        for b in range(m):
            if mask & (1 << b) == 0:
                nxt = mask | (1 << b)
                t = best[mask] + abs(wx - bikes[b][0]) + abs(wy - bikes[b][1])
                if t < best[nxt]:
                    best[nxt] = t
    return answer


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_points(n):
    ps = []
    for _ in range(n):
        x = next_random() % 1000
        ps.append((x, next_random() % 1000))
    return ps


def main():
    # 5000 problems of 8 to 10 workers and 10 bikes on a 1000 by 1000
    # grid, built once, then each answered
    problems = []
    for _ in range(5000):
        n = 8 + next_random() % 3
        workers = random_points(n)
        problems.append((workers, random_points(10)))
    calls = total = check = 0
    for workers, bikes in problems:
        answer = assign_bikes(workers, bikes)
        total += answer
        check = (check * 31 + answer) % 1000000007
        calls += 1
    print(f"{calls} calls: answers sum {total}, checksum {check}")


main()
