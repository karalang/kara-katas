# LeetCode #2751: Robot Collisions -- the ★ arm in Python (robots.kara):
# the robots in order of position, those moving right on a stack, and
# each robot moving left meeting the stack's top in turn.


def survived_robots_healths(positions, healths, directions):
    n = len(positions)
    health = list(healths)
    order = sorted(range(n), key=lambda i: positions[i])
    rightward = []
    for i in order:
        if directions[i] == "R":
            rightward.append(i)
            continue
        while health[i] > 0 and rightward:
            top = rightward[-1]
            if health[top] < health[i]:
                health[top] = 0
                rightward.pop()
                health[i] -= 1
            elif health[top] > health[i]:
                health[top] -= 1
                health[i] = 0
            else:
                health[top] = 0
                rightward.pop()
                health[i] = 0
    return [h for h in health if h > 0]


seed = 2751


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_robots(n, far, strongest):
    taken = set()
    positions = []
    while len(positions) < n:
        p = (next_random() * 32768 + next_random()) % far + 1
        if p not in taken:
            taken.add(p)
            positions.append(p)
    healths = [next_random() % strongest + 1 for _ in range(n)]
    directions = "".join("L" if next_random() % 2 == 0 else "R" for _ in range(n))
    return positions, healths, directions


def fold(survivors, acc):
    acc[1] = (acc[1] * 31 + len(survivors)) % 1000000007
    for h in survivors:
        acc[0] += h
        acc[1] = (acc[1] * 31 + h) % 1000000007


def show(v):
    return "[" + ", ".join(map(str, v)) + "]"


def main():
    print(show(survived_robots_healths([5, 4, 3, 2, 1], [2, 17, 9, 15, 10], "RRRRR")))
    print(show(survived_robots_healths([3, 5, 2, 6], [10, 10, 15, 12], "RLRL")))
    print(show(survived_robots_healths([1, 2, 5, 6], [10, 10, 11, 11], "RLRL")))
    print(show(survived_robots_healths([7], [3], "L")))
    print(show(survived_robots_healths([1, 2], [5, 6], "LR")))
    print(show(survived_robots_healths([1, 2, 3, 4, 5], [10, 1, 1, 1, 1], "RLLLL")))
    acc = [0, 0]
    for _ in range(3000):
        n = next_random() % 12 + 1
        fold(survived_robots_healths(*random_robots(n, 30, 5)), acc)
    print(f"3000 small cases: healths sum to {acc[0]}, checksum {acc[1]}")
    acc = [0, 0]
    for _ in range(10):
        fold(survived_robots_healths(*random_robots(100000, 1000000000, 1000000000)), acc)
    print(f"10 cases of 100000 robots: healths sum to {acc[0]}, checksum {acc[1]}")


main()
