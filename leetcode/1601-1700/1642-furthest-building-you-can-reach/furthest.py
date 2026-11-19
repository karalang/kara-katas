# LeetCode #1642: Furthest Building You Can Reach -- the Python mirror of
# the ★ arm: the climbs ladders cover in a min-heap, the smallest paid for
# in bricks once there are more than ladders.

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


# ---- the harness: the same as every arm's ---------------------------------

seed = 1642


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, most, top):
    check = 0
    total = 0
    for _ in range(count):
        n = next_random() % most + 1
        heights = [next_random() % top + 1 for _ in range(n)]
        bricks = (next_random() * 32768 + next_random()) % (top * (n // 3 + 1))
        ladders = next_random() % (n // 10 + 2)
        furthest = furthest_building(heights, bricks, ladders)
        total += furthest
        check = (check * 31 + furthest + 1) % 1000000007
    print(f"{count} rows of up to {most} buildings: indices sum to {total}, checksum {check}")


print(furthest_building([4, 2, 7, 6, 9, 14, 12], 5, 1))
print(furthest_building([4, 12, 2, 7, 3, 18, 20, 3, 19], 10, 2))
print(furthest_building([14, 3, 19, 3], 17, 0))
print(furthest_building([5], 0, 0))
print(furthest_building([9, 7, 4, 1], 0, 0))
print(furthest_building([1, 2], 0, 0))
batch(3000, 8, 5)
batch(300, 1000, 1000000)
batch(5, 100000, 1000000)
