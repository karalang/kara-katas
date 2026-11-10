# LeetCode #2061: Number of Spaces Cleaning Robot Cleaned -- Python mirror
# of the ★ arm (robot.kara): the robot walked one move at a time, each
# (cell, direction) state marked once, until a state comes round again.

DR = [0, 1, 0, -1]
DC = [1, 0, -1, 0]


def number_of_clean_rooms(room):
    m, n = len(room), len(room[0])
    seen = [False] * (m * n * 4)
    cleaned = [False] * (m * n)
    count = 0
    r, c, d = 0, 0, 0
    while not seen[(r * n + c) * 4 + d]:
        seen[(r * n + c) * 4 + d] = True
        if not cleaned[r * n + c]:
            cleaned[r * n + c] = True
            count += 1
        nr, nc = r + DR[d], c + DC[d]
        if 0 <= nr < m and 0 <= nc < n and room[nr][nc] == 0:
            r, c = nr, nc
        else:
            d = (d + 1) % 4
    return count


seed = 2061


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# an `m` by `n` room, each cell an object with chance `p` in 100, the
# top-left cell always empty
def room_of(m, n, p):
    room = [[1 if next_random() % 100 < p else 0 for _ in range(n)] for _ in range(m)]
    room[0][0] = 0
    return room


def show(room):
    return "[" + ", ".join("".join(str(x) for x in row) for row in room) + "]"


def main():
    examples = [
        [[0, 0, 0], [1, 1, 0], [0, 0, 0]],
        [[0, 1, 0], [1, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0]],
        [[0, 0, 1, 0]],
        [[0], [0], [0]],
        [[0, 1], [0, 0]],
        [[0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [1, 0, 0, 0]],
    ]
    for room in examples:
        print(f"{show(room)} -> {number_of_clean_rooms(room)}")
    # 500 rooms of 1 to 12 by 1 to 12, objects with chance 0 to 50 in 100
    total = 0
    check = 0
    for _ in range(500):
        m = next_random() % 12 + 1
        n = next_random() % 12 + 1
        p = next_random() % 51
        a = number_of_clean_rooms(room_of(m, n, p))
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"500 rooms: sum {total}, checksum {check}")
    # 4 rooms of 300 by 300, objects with chance 0, 1, 3 and 10 in 100
    for p in [0, 1, 3, 10]:
        print(f"300 x 300, {p} in 100 -> {number_of_clean_rooms(room_of(300, 300, p))}")


main()
