# LeetCode #2061: Number of Spaces Cleaning Robot Cleaned -- Python mirror
# of the ★ arm's benchmark (robot.kara): 600 spiral rooms of 200 to 300 by
# 200 to 300, the robot walked one move at a time, states and cells kept
# in flat lists of booleans.

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


def spiral(m, n):
    room = [[0] * n for _ in range(m)]
    top, left, bottom, right = 0, 0, m - 1, n - 1
    while True:
        if top + 2 > bottom:
            break
        room[top + 1][left] = 1
        top += 2
        if left + 2 > right:
            break
        room[top][right - 1] = 1
        right -= 2
        if bottom - 2 < top:
            break
        room[bottom - 1][right] = 1
        bottom -= 2
        if right - 2 < left:
            break
        room[bottom][left + 1] = 1
        left += 2
    return room


def main():
    total = 0
    check = 0
    for _ in range(600):
        m = next_random() % 101 + 200
        n = next_random() % 101 + 200
        a = number_of_clean_rooms(spiral(m, n))
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"600 rooms: {total} cleaned, checksum {check}")


main()
