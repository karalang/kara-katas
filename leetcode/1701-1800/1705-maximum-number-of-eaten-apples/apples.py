# LeetCode #1705: Maximum Number of Eaten Apples -- the Python mirror of
# the ★ arm (apples.kara): each day one apple from the crop that rots
# soonest, by a heap of (rotting day, apples left).

import heapq


def eaten_apples(apples, days):
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


def batch(count, most, crop, life, seed):
    total = 0
    check = 0
    for _ in range(count):
        n = next_random(seed) % most + 1
        apples, days = [], []
        for _ in range(n):
            grown = next_random(seed) % (crop + 1)
            apples.append(grown)
            days.append(0 if grown == 0 else next_random(seed) % life + 1)
        answer = eaten_apples(apples, days)
        total += answer
        check = (check * 31 + answer + n) % 1000000007
    print(f"{count} trees of up to {most} days: answers sum to {total}, checksum {check}")


def main():
    # LeetCode's two examples, then one apple, nothing grown, and a crop
    # that outlasts the days it grows on
    print(eaten_apples([1, 2, 3, 5, 2], [3, 2, 1, 4, 2]))
    print(eaten_apples([3, 0, 0, 0, 0, 2], [3, 0, 0, 0, 0, 2]))
    print(eaten_apples([1], [1]))
    print(eaten_apples([0, 0], [0, 0]))
    print(eaten_apples([10, 1], [6, 1]))
    seed = [1705]
    batch(3000, 8, 5, 5, seed)
    batch(300, 1000, 100, 100, seed)
    batch(10, 20000, 20000, 20000, seed)


main()
