# LeetCode #1705: Maximum Number of Eaten Apples -- the bench's Python
# mirror: the ★ arm on 50 random trees of 20000 days, all drawn first,
# each answered 10 times.

import heapq


def eaten_apples(apples, days):
    # each day the rotten crops dropped and one apple eaten from the soonest to rot
    n = len(apples)
    queue = []
    eaten = 0
    day = 0
    while day < n or queue:
        if day < n and apples[day] > 0:
            heapq.heappush(queue, (day + days[day], apples[day]))
        while queue and queue[0][0] <= day:
            heapq.heappop(queue)
        if queue:
            rot, left = heapq.heappop(queue)
            eaten += 1
            if left > 1:
                heapq.heappush(queue, (rot, left - 1))
        day += 1
    return eaten


def next_random(state):
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def main():
    count, rounds, n = 50, 10, 20000
    seed = [1705]
    trees = []
    for _ in range(count):
        apples, days = [], []
        for _ in range(n):
            # one day in four grows nothing
            grown = 0 if next_random(seed) % 4 == 0 else next_random(seed) % 20000 + 1
            apples.append(grown)
            days.append(0 if grown == 0 else next_random(seed) % 20000 + 1)
        trees.append((apples, days))
    total = 0
    check = 0
    for r in range(rounds):
        for apples, days in trees:
            answer = eaten_apples(apples, days)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} trees of {n} days, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
