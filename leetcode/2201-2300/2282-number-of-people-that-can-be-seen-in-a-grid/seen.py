# LeetCode #2282: Number of People That Can Be Seen in a Grid -- the
# Python mirror of the ★ arm, `seen.kara`.


def sightings(line):
    seen = [0] * len(line)
    stack = []
    for i in range(len(line) - 1, -1, -1):
        h = line[i]
        while stack and stack[-1] < h:
            stack.pop()
            seen[i] += 1
        if stack:
            seen[i] += 1
            if stack[-1] == h:
                stack.pop()
        stack.append(h)
    return seen


def see_people(heights):
    m, n = len(heights), len(heights[0])
    answer = [sightings(list(heights[i])) for i in range(m)]
    for j in range(n):
        down = sightings([heights[i][j] for i in range(m)])
        for i in range(m):
            answer[i][j] += down[i]
    return answer


# ---- test harness ---------------------------------------------------------

seed = 2282


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def grid(m, n, high):
    heights = []
    for _ in range(m):
        row = []
        for _ in range(n):
            top = next_random()
            row.append((top * 32768 + next_random()) % high + 1)
        heights.append(row)
    return heights


def total(answer):
    return sum(sum(row) for row in answer)


def show(v):
    return "[" + ", ".join(show(x) if isinstance(x, list) else str(x) for x in v) + "]"


def main():
    examples = [
        [[3, 1, 4, 2, 5]],
        [[5, 1], [3, 1], [4, 1]],
        [[7]],
        [[2, 2, 2]],
        [[5], [4], [3]],
        [[1, 2, 3]],
        [[5, 1, 1, 5]],
    ]
    for heights in examples:
        print(f"{show(heights)} -> {show(see_people(heights))}")
    check = 0
    for t in range(1000):
        m = next_random() % 8 + 1
        n = next_random() % 8 + 1
        heights = grid(m, n, [3, 10, 100000][t % 3])
        for row in see_people(heights):
            for a in row:
                check = (check * 31 + a) % 1000000007
    print(f"1000 grids: checksum {check}")
    random = grid(400, 400, 100000)
    alike = [[7] * 400 for _ in range(400)]
    rising = [list(range(1, 401)) for _ in range(400)]
    totals = [total(see_people(random)), total(see_people(alike)), total(see_people(rising))]
    print(f"400 by 400, people seen: {show(totals)}")


main()
