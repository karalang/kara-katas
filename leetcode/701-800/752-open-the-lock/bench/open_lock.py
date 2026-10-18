# LeetCode 752 — Open the Lock, bench: the ★ arm (breadth-first over
# numbers) against 500 dead ends that keep changing. Mirrors open_lock.kara.
from collections import deque


def open_lock(deadends, target):
    blocked = [False] * 10000
    for d in deadends:
        blocked[int(d)] = True
    goal = int(target)
    if blocked[0]:
        return -1
    dist = [-1] * 10000
    dist[0] = 0
    queue = deque([0])
    while queue:
        at = queue.popleft()
        if at == goal:
            return dist[at]
        place = 1
        for _ in range(4):
            digit = at // place % 10
            for step in (1, 9):
                nxt = at + ((digit + step) % 10 - digit) * place
                if not blocked[nxt] and dist[nxt] == -1:
                    dist[nxt] = dist[at] + 1
                    queue.append(nxt)
            place *= 10
    return -1


seed = 752


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def four(x):
    return f"{x // 1000}{x // 100 % 10}{x // 10 % 10}{x % 10}"


def main():
    rounds = 3000
    deadends = [four(1 + next_random() % 9999) for _ in range(500)]
    total = 0
    stuck = 0
    for _ in range(rounds):
        for _ in range(5):
            i = next_random() % 500
            deadends[i] = four(1 + next_random() % 9999)
        target = four(next_random() % 10000)
        turns = open_lock(deadends, target)
        if turns == -1:
            stuck += 1
        else:
            total += turns
    print(f"{rounds} locks with 500 dead ends: {stuck} cannot open, the rest take {total} turns in all")


main()
