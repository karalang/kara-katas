# Benchmark for #841: Keys and Rooms -- the ★ arm (a stack of rooms to open).
#
# Mirrors keys_and_rooms.kara: room 0 is open; every room opened is put
# on a stack, and a room taken off the stack gives up its keys, each key
# to a room not yet opened opening it.


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


seed = 841


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 64 cases drawn once, each LeetCode's most rooms, 1000: case g puts
    # 2000 keys, each to a random room, in random rooms, no room holding
    # two keys to the same room; when g is even it then threads the
    # rooms in a shuffled order, each holding a key to the next, so that
    # every room can be visited. Each round asks the next case.
    count = 64
    rounds = 36000
    n = 1000
    cases = []
    for g in range(count):
        rooms = [[] for _ in range(n)]
        for _ in range(2000):
            frm = next_random() % n
            to = next_random() % n
            if to not in rooms[frm]:
                rooms[frm].append(to)
        if g % 2 == 0:
            order = list(range(n))
            for i in range(n - 1, 1, -1):
                j = 1 + next_random() % i
                order[i], order[j] = order[j], order[i]
            for i in range(n - 1):
                if order[i + 1] not in rooms[order[i]]:
                    rooms[order[i]].append(order[i + 1])
        cases.append(rooms)
    yes = 0
    checksum = 0
    for round in range(rounds):
        a = can_visit_all_rooms(cases[round % count])
        if a:
            yes += 1
        checksum = (checksum * 31 + (round % 1000 if a else 7)) % 1000000007
    print(f"{rounds} rounds of {count} cases: {yes} with every room visited, checksum {checksum}")


main()
