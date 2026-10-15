# LeetCode #649: Dota2 Senate -- Python mirror of the Kāra bench.
#
# The ★ arm over the same senates and rounds: a deque of each party's
# senators by when they vote, the front two meeting and the earlier
# going to the back `n` places later.

from collections import deque


def predict_party_victory(senate):
    n = len(senate)
    radiant = deque()
    dire = deque()
    for i, c in enumerate(senate):
        if c == "R":
            radiant.append(i)
        else:
            dire.append(i)
    while radiant and dire:
        r = radiant.popleft()
        d = dire.popleft()
        if r < d:
            radiant.append(r + n)
        else:
            dire.append(d + n)
    return "Radiant" if radiant else "Dire"


seed = 649


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    inputs = 20
    rounds = 500
    senates = []
    for _ in range(inputs):
        radiant = 45 + next_random() % 11
        senates.append("".join("R" if next_random() % 100 < radiant else "D" for _ in range(100000)))
    wins = 0
    checksum = 0
    for r in range(rounds):
        won = predict_party_victory(senates[(r * 7) % inputs]) == "Radiant"
        if won:
            wins += 1
        checksum = (checksum * 2 + (1 if won else 0)) % 1000000007
    print(f"{inputs} senates, {rounds} rounds: Radiant wins {wins}, checksum {checksum}")


main()
