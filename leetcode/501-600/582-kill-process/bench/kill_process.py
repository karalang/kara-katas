# Benchmark for #582: Python mirror of the ★ arm (children lists, walked
# breadth first); see kill_process.kara.

from collections import deque


def kill_process(pid, ppid, kill):
    children = {}
    for i in range(len(pid)):
        children.setdefault(ppid[i], []).append(pid[i])
    killed = []
    queue = deque([kill])
    while queue:
        p = queue.popleft()
        killed.append(p)
        for k in children.get(p, []):
            queue.append(k)
    return killed


# ---- benchmark ----------------------------------------------------------------

seed = 582


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    high = next_random() * 32768
    return high + next_random()


def main():
    count = 20
    rounds = 30
    n = 50000
    pids = []
    ppids = []
    for _ in range(count):
        names = list(range(1, n + 1))
        for i in range(n - 1, 0, -1):
            j = wide() % (i + 1)
            names[i], names[j] = names[j], names[i]
        pid = []
        ppid = []
        for i in range(n):
            pid.append(names[i])
            ppid.append(0 if i == 0 else names[wide() % i])
        pids.append(pid)
        ppids.append(ppid)
    total = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            p = (rnd * 7 + g) % count
            kill = pids[p][0] if (rnd + g) % 4 == 0 else pids[p][wide() % n]
            got = kill_process(pids[p], ppids[p], kill)
            total += len(got)
            checksum = (checksum * 31 + sum(got)) % 1000000007
    print(f"{count} trees of 50000 processes, {rounds} rounds: {total} killed, checksum {checksum}")


main()
