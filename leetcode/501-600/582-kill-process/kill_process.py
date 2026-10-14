# LeetCode #582: Kill Process -- children lists, walked breadth first.
#
# Python mirror of kill_process.kara (the starred arm): a map from parent
# to children, and a queue that starts with `kill`.

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


# ---- test harness -----------------------------------------------------------

seed = 582


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    high = step() * 32768
    return high + step()


def sorted_kill(pid, ppid, kill):
    return sorted(kill_process(pid, ppid, kill))


def show(pid, ppid, kill):
    print(f"{pid} under {ppid}, kill {kill}: {sorted_kill(pid, ppid, kill)}")


def random_tree(n, pid, ppid):
    names = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = wide() % (i + 1)
        names[i], names[j] = names[j], names[i]
    for i in range(n):
        pid.append(names[i])
        if i == 0:
            ppid.append(0)
        else:
            ppid.append(names[wide() % i])


def summary(label, killed):
    checksum = 0
    for k in killed:
        checksum = (checksum * 31 + k) % 1000000007
    print(f"{label}: {len(killed)} killed, checksum {checksum}")


def main():
    show([1, 3, 10, 5], [3, 0, 5, 3], 5)
    show([1], [0], 1)
    show([1, 3, 10, 5], [3, 0, 5, 3], 3)
    show([1, 3, 10, 5], [3, 0, 5, 3], 10)
    show([1, 2, 3, 4, 5], [0, 1, 2, 3, 4], 3)
    show([4, 5, 2, 3, 1], [2, 2, 1, 1, 0], 2)
    total = 0
    checksum = 0
    for _ in range(300):
        n = 1 + step() % 30
        pid = []
        ppid = []
        random_tree(n, pid, ppid)
        kill = pid[step() % n]
        got = sorted_kill(pid, ppid, kill)
        total += len(got)
        for k in got:
            checksum = (checksum * 31 + k) % 1000000007
        checksum = (checksum * 31 + 7) % 1000000007
    print(f"300 random trees: {total} killed, checksum {checksum}")
    pid = []
    ppid = []
    random_tree(50000, pid, ppid)
    summary("random tree, the root", sorted_kill(pid, ppid, pid[0]))
    summary("random tree, a process partway down", sorted_kill(pid, ppid, pid[40]))
    flat_pid = list(range(1, 50001))
    flat_ppid = [0 if i == 1 else 1 for i in range(1, 50001)]
    summary("one root, 49999 children", sorted_kill(flat_pid, flat_ppid, 1))
    chain_pid = list(range(1, 5001))
    chain_ppid = [i - 1 for i in range(1, 5001)]
    summary("a chain of 5000, the middle", sorted_kill(chain_pid, chain_ppid, 2500))


main()
