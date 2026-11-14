# LeetCode #2120: Execution of All Suffix Instructions Staying in a Grid
# -- Python mirror of suffix.kara, each suffix simulated; same harness,
# same output.


def execute_instructions(n, start_pos, s):
    moves = s.encode()
    m = len(moves)
    answer = []
    for i in range(m):
        row, col = start_pos[0], start_pos[1]
        count = 0
        for j in range(i, m):
            c = moves[j]
            if c == ord("L"):
                col -= 1
            elif c == ord("R"):
                col += 1
            elif c == ord("U"):
                row -= 1
            else:
                row += 1
            if row < 0 or row >= n or col < 0 or col >= n:
                break
            count += 1
        answer.append(count)
    return answer


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    examples = [
        (3, [0, 1], "RRDDLU"),
        (2, [1, 1], "LURD"),
        (1, [0, 0], "LRUD"),
        (1, [0, 0], "R"),
        (4, [3, 3], "DRULUL"),
        (5, [0, 2], "LLLRRRRU"),
    ]
    for n, start, s in examples:
        print(f"n={n} start={show(start)} {s} -> {show(execute_instructions(n, start, s))}")
    seed = [2120]
    total = 0
    check = 0
    for _ in range(2000):
        n = next_random(seed) % 8 + 1
        start = [next_random(seed) % n, next_random(seed) % n]
        m = next_random(seed) % 30 + 1
        s = ""
        for _ in range(m):
            s += "LRUD"[next_random(seed) % 4]
        for c in execute_instructions(n, start, s):
            total += c
            check = (check * 31 + c) % 1000000007
    print(f"2000 grids: {total} moves, checksum {check}")
    rnd = "".join("RDLU"[k // 125] for k in range(500))
    big = execute_instructions(500, [250, 250], rnd)
    print(f"500 moves round a square: {sum(big)} moves, first {big[0]}, last {big[499]}")


main()
