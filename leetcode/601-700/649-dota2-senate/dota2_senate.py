# LeetCode #649: Dota2 Senate -- a queue for each party.
# Mirrors the ★ arm (dota2_senate.kara) and its test harness.

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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(senate):
    print(f"{senate} -> {predict_party_victory(senate)}")


def random_senate(n, radiant):
    return "".join("R" if next_random() % 100 < radiant else "D" for _ in range(n))


def main():
    global seed
    for s in ["RD", "RDD", "R", "D", "DRR", "RRDDD", "DDRRR", "RRDDDD",
              "RDRDRDRD", "DRRDRDRDRDDRDRDR"]:
        show(s)
    seed = 649
    wins = 0
    checksum = 0
    for _ in range(300):
        n = 1 + next_random() % 30
        radiant = next_random() % 101
        won = predict_party_victory(random_senate(n, radiant)) == "Radiant"
        if won:
            wins += 1
        checksum = (checksum * 2 + (1 if won else 0)) % 1000000007
    print(f"300 random senates: Radiant wins {wins}, checksum {checksum}")
    for radiant in [50, 45, 55]:
        print(f"10000 senators at {radiant}%: {predict_party_victory(random_senate(10000, radiant))}")


main()
