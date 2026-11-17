# LeetCode #1183: Maximum Number of Ones -- the ★ arm in Python: count the
# cells on each position of the side * side square and take the max_ones
# largest counts. Also checks the answer against the statement read
# literally (every 0/1 matrix, every square) on every small case.


def maximum_number_of_ones(width, height, side_length, max_ones):
    counts = []
    for i in range(side_length):
        for j in range(side_length):
            across = (width - i - 1) // side_length + 1
            down = (height - j - 1) // side_length + 1
            counts.append(across * down)
    counts.sort(reverse=True)
    return sum(counts[:max_ones])


def literal(width, height, side, max_ones):
    best = 0
    cells = width * height
    for mask in range(1 << cells):
        ones = bin(mask).count("1")
        if ones <= best:
            continue
        ok = True
        for r in range(height - side + 1):
            for c in range(width - side + 1):
                n = 0
                for dr in range(side):
                    for dc in range(side):
                        n += (mask >> ((r + dr) * width + c + dc)) & 1
                if n > max_ones:
                    ok = False
        if ok:
            best = ones
    return best


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


print(f"example 1: {maximum_number_of_ones(3, 3, 2, 1)}")
print(f"example 2: {maximum_number_of_ones(3, 3, 2, 2)}")
print(f"small 1: {maximum_number_of_ones(1, 1, 1, 0)}")
print(f"small 2: {maximum_number_of_ones(1, 1, 1, 1)}")
print(f"small 3: {maximum_number_of_ones(7, 2, 2, 4)}")
print(f"small 4: {maximum_number_of_ones(5, 8, 3, 2)}")
print(f"largest 1: {maximum_number_of_ones(100, 100, 1, 1)}")
print(f"largest 2: {maximum_number_of_ones(100, 100, 100, 10000)}")
print(f"largest 3: {maximum_number_of_ones(100, 99, 7, 20)}")
seed = 1183
checksum = 0
for t in range(3000):
    width = 1 + next_random() % 100
    height = 1 + next_random() % 100
    side = 1 + next_random() % min(width, height)
    max_ones = next_random() % (side * side + 1)
    checksum = (checksum * 31 + maximum_number_of_ones(width, height, side, max_ones) + t) % 1000000007
print(f"3000 random matrices: checksum {checksum}")

# every case with at most 12 cells, read literally
cases = 0
for width in range(1, 13):
    for height in range(1, 13):
        if width * height > 12:
            continue
        for side in range(1, min(width, height) + 1):
            for max_ones in range(side * side + 1):
                assert maximum_number_of_ones(width, height, side, max_ones) == literal(width, height, side, max_ones), (width, height, side, max_ones)
                cases += 1
import sys
print(f"{cases} small cases match the literal reading", file=sys.stderr)
