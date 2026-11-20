# LeetCode #1706: Where Will the Ball Fall -- the Python mirror of the ★
# arm (ball.kara): each ball followed down, a row at a time.


def find_ball(grid):
    n = len(grid[0])
    answer = []
    for start in range(n):
        c = start
        for row in grid:
            nxt = c + row[c]
            if nxt < 0 or nxt >= n or row[nxt] != row[c]:
                c = -1
                break
            c = nxt
        answer.append(c)
    return answer


def next_random(state):
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def batch(count, most, seed):
    out = 0
    check = 0
    for _ in range(count):
        m = next_random(seed) % most + 1
        n = next_random(seed) % most + 1
        lean = next_random(seed) % 11
        grid = [[1 if next_random(seed) % 10 < lean else -1 for _ in range(n)] for _ in range(m)]
        for a in find_ball(grid):
            if a >= 0:
                out += 1
            check = (check * 31 + a + 2) % 1000000007
    print(f"{count} boxes of up to {most} by {most}: {out} balls out, checksum {check}")


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    # LeetCode's three examples, then one cell each way and a V
    print(show(find_ball([[1, 1, 1, -1, -1], [1, 1, 1, -1, -1], [-1, -1, -1, 1, 1], [1, 1, 1, 1, -1], [-1, -1, -1, -1, -1]])))
    print(show(find_ball([[-1]])))
    print(show(find_ball([[1, 1, 1, 1, 1, 1], [-1, -1, -1, -1, -1, -1], [1, 1, 1, 1, 1, 1], [-1, -1, -1, -1, -1, -1]])))
    print(show(find_ball([[1, -1]])))
    print(show(find_ball([[-1, -1, 1, 1]])))
    seed = [1706]
    batch(3000, 6, seed)
    batch(300, 30, seed)
    batch(100, 100, seed)


main()
