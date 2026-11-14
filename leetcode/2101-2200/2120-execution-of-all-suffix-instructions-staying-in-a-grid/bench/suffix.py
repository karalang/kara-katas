# LeetCode #2120: Execution of All Suffix Instructions Staying in a Grid
# -- the benchmark, the same algorithm as suffix.kara: each suffix
# simulated, 40 grids built once, 20 rounds with every start one row
# lower than in the round before.


def execute_instructions(n, start_pos, s):
    m = len(s)
    answer = []
    for i in range(m):
        row, col = start_pos[0], start_pos[1]
        count = 0
        for j in range(i, m):
            c = s[j]
            if c == "L":
                col -= 1
            elif c == "R":
                col += 1
            elif c == "U":
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


def main():
    seed = [2120]
    grids = []
    for _ in range(40):
        n = next_random(seed) % 401 + 100
        row = next_random(seed) % n
        col = next_random(seed) % n
        s = "".join("LRUD"[next_random(seed) % 4] for _ in range(500))
        grids.append((n, row, col, s))
    total = 0
    check = 0
    for rnd in range(20):
        for n, row, col, s in grids:
            for c in execute_instructions(n, [(row + rnd) % n, col], s):
                total += c
                check = (check * 31 + c) % 1000000007
    print(f"800 solves: {total} moves, checksum {check}")


main()
