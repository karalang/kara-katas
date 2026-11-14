# LeetCode #1559: Detect Cycles in 2D Grid -- the Python mirror of
# cycles.kara, the ★ arm: a search on a stack, each cell with the cell it
# came from. Prints byte-identical output.


def contains_cycle(grid):
    rows = len(grid)
    cols = len(grid[0])
    seen = [False] * (rows * cols)
    for start in range(rows * cols):
        if seen[start]:
            continue
        seen[start] = True
        stack = [(start, -1)]
        while stack:
            cell, came = stack.pop()
            r, c = cell // cols, cell % cols
            for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                nr, nc = r + dr, c + dc
                if nr < 0 or nr >= rows or nc < 0 or nc >= cols or grid[nr][nc] != grid[r][c]:
                    continue
                nxt = nr * cols + nc
                if nxt == came:
                    continue
                if seen[nxt]:
                    return True
                seen[nxt] = True
                stack.append((nxt, cell))
    return False


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, letters):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    check = 0
    found = 0
    for _ in range(count):
        rows = next_random() % most + 1
        cols = next_random() % most + 1
        own = next_random() % letters + 1
        grid = [[alphabet[next_random() % own] for _ in range(cols)] for _ in range(rows)]
        cycle = contains_cycle(grid)
        if cycle:
            found += 1
        check = mix(check, rows * cols if cycle else 0)
    print(f"{count} grids of up to {most} by {most} over up to {letters} letters: {found} with a cycle, checksum {check}")


def main():
    global seed
    examples = [
        ["aaaa", "abba", "abba", "aaaa"],
        ["ccca", "cdcc", "ccec", "fccc"],
        ["abb", "bzb", "bba"],
        ["aa", "aa"],
        ["a"],
        ["ab", "ba"],
        ["aaa", "aba", "aaa"],
        ["aaa", "aba", "aab"],
        ["aaaa"],
    ]
    for rows in examples:
        print(f"[{', '.join(rows)}] -> {'true' if contains_cycle(rows) else 'false'}")
    seed = 1559
    batch(3000, 6, 3)
    batch(300, 60, 26)
    batch(30, 200, 26)


main()
