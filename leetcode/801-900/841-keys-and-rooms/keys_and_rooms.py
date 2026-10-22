# LeetCode #841: Keys and Rooms -- Python mirror of the ★ arm and its harness.


def can_visit_all_rooms(rooms):
    n = len(rooms)
    opened = [False] * n
    opened[0] = True
    count = 1
    stack = [0]
    while stack:
        room = stack.pop()
        for key in rooms[room]:
            if not opened[key]:
                opened[key] = True
                count += 1
                stack.append(key)
    return count == n


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_rooms(n, keys, thread):
    rooms = [[] for _ in range(n)]
    for _ in range(keys):
        frm = next_random() % n
        to = next_random() % n
        if to not in rooms[frm]:
            rooms[frm].append(to)
    if thread:
        order = list(range(n))
        for i in range(n - 1, 1, -1):
            j = 1 + next_random() % i
            order[i], order[j] = order[j], order[i]
        for i in range(n - 1):
            if order[i + 1] not in rooms[order[i]]:
                rooms[order[i]].append(order[i + 1])
    return rooms


def b(x):
    return "true" if x else "false"


def show(rooms):
    print(f"{rooms} -> {b(can_visit_all_rooms(rooms))}")


def main():
    global seed
    show([[1], [2], [3], []])
    show([[1, 3], [3, 0, 1], [2], [0]])
    show([[1], []])
    show([[], [0]])
    show([[3], [0], [1], [2]])
    show([[0], [1]])
    show([[1, 2, 3], [], [], []])
    show([[1], [0], [3], [2]])
    show([[2], [], [1]])
    show([[1], [2], [1], [0, 1, 2]])
    seed = 841
    chain = [[i + 1] if i < 999 else [] for i in range(1000)]
    print(f"1000 rooms in a chain: {b(can_visit_all_rooms(chain))}")
    backward = [[999]] + [[i - 1] for i in range(1, 1000)]
    print(f"1000 rooms in a chain read backwards: {b(can_visit_all_rooms(backward))}")
    for keys, thread in [(3000, False), (2000, True), (999, True)]:
        rooms = random_rooms(1000, keys, thread)
        held = sum(len(r) for r in rooms)
        print(f"1000 rooms, {held} keys, threaded {b(thread)}: {b(can_visit_all_rooms(rooms))}")
    yes = 0
    check = 0
    for case in range(300):
        n = 2 + next_random() % 30
        keys = next_random() % (2 * n)
        a = can_visit_all_rooms(random_rooms(n, keys, case % 3 == 0))
        if a:
            yes += 1
        check = (check * 31 + (case if a else 7)) % 1000000007
    print(f"300 random cases: {yes} with every room visited, checksum {check}")


main()
