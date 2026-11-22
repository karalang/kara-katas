# LeetCode #2751: Robot Collisions -- the bench (robots.kara in Python):
# the robots in order of position, those moving right on a stack, and each
# robot moving left meeting the stack's top in turn.


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


def main():
    count, rounds, n = 10, 3, 100000
    cases = []
    for _ in range(count):
        positions = [i * 10000 + next_random() % 10000 + 1 for i in range(n)]
        for i in range(n - 1, 0, -1):
            j = (next_random() * 32768 + next_random()) % (i + 1)
            positions[i], positions[j] = positions[j], positions[i]
        healths = [(next_random() * 32768 + next_random()) % 1000000000 + 1 for _ in range(n)]
        directions = "".join("L" if next_random() % 2 == 0 else "R" for _ in range(n))
        cases.append((positions, healths, directions))
    total = check = 0
    for r in range(rounds):
        for positions, healths, directions in cases:
            survivors = survived_robots_healths(positions, healths, directions)
            check = (check * 31 + len(survivors) + r) % 1000000007
            for h in survivors:
                total += h
                check = (check * 31 + h) % 1000000007
    print(f"{count} cases of 100000 robots, {rounds} rounds: healths sum to {total}, checksum {check}")


main()
