# LeetCode #1642: Furthest Building You Can Reach -- the bench's Python
# mirror: the ★ arm on 50 random rows of 100000 buildings up to 10^4 high,
# each with up to 10^9 bricks and up to 5000 ladders, all drawn first.

import heapq


def furthest_building(heights, bricks, ladders):
    laddered = []
    for i in range(1, len(heights)):
        climb = heights[i] - heights[i - 1]
        if climb <= 0:
            continue
        heapq.heappush(laddered, climb)
        if len(laddered) > ladders:
            bricks -= heapq.heappop(laddered)
            if bricks < 0:
                return i - 1
    return len(heights) - 1


seed = 1642


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rows = []
    for _ in range(50):
        heights = [next_random() % 10000 + 1 for _ in range(100000)]
        bricks = (next_random() * 32768 + next_random()) % 1000000001
        ladders = next_random() % 5001
        rows.append((heights, bricks, ladders))
    check = 0
    total = 0
    for heights, bricks, ladders in rows:
        furthest = furthest_building(heights, bricks, ladders)
        total += furthest
        check = (check * 31 + furthest + 1) % 1000000007
    print(f"50 rows of 100000 buildings: indices sum to {total}, checksum {check}")


main()
