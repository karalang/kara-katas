# LeetCode #2282: Number of People That Can Be Seen in a Grid -- the
# bench, the ★ arm.


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


# ---- bench harness ---------------------------------------------------------

seed = 2282


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for _ in range(40):
        heights = []
        for _ in range(400):
            row = []
            for _ in range(400):
                top = next_random()
                row.append((top * 32768 + next_random()) % 100000 + 1)
            heights.append(row)
        answer = see_people(heights)
        seen = 0
        for row in answer:
            for a in row:
                seen += a
        check = (check * 31 + seen) % 1000000007
    print(f"40 grids of 400 by 400: checksum {check}")


main()
