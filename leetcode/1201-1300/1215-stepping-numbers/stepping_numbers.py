# LeetCode #1215: Stepping Numbers -- a Python mirror of the ★ arm: a
# breadth-first search from the digits 1 to 9, each number followed by
# itself with one more digit, its last digit one less or one more; the
# numbers come out sorted, and the search stops at the first past `high`.


def count_stepping_numbers(low, high):
    out = []
    if low == 0:
        out.append(0)
    queue = list(range(1, 10))
    head = 0
    while head < len(queue):
        n = queue[head]
        head += 1
        if n > high:
            break
        if n >= low:
            out.append(n)
        last = n % 10
        if last > 0:
            queue.append(n * 10 + last - 1)
        if last < 9:
            queue.append(n * 10 + last + 1)
    return out


seed = 1215


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fold(check, answer):
    for v in answer:
        check = (check * 131 + v % 1000000007) % 1000000007
    return (check * 131 + len(answer)) % 1000000007


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    cases = [(0, 21), (10, 15), (0, 0), (1, 9), (9, 10), (100, 120), (2000000000, 2000000000), (1234567898, 2000000000)]
    for low, high in cases:
        print(f"[{low}, {high}]: {show(count_stepping_numbers(low, high))}")
    found = 0
    check = 0
    for _ in range(1000):
        low = next_random() % 100000
        high = low + next_random() % 5000
        answer = count_stepping_numbers(low, high)
        found += len(answer)
        check = fold(check, answer)
    print(f"1000 small ranges: {found} found, checksum {check}")
    every = count_stepping_numbers(0, 2000000000)
    print(f"[0, 2000000000]: {len(every)} found, checksum {fold(0, every)}, the last {every[-1]}")
    upper = count_stepping_numbers(1000000000, 2000000000)
    print(f"[1000000000, 2000000000]: {len(upper)} found, the first {upper[0]}")
    wide = 0
    for _ in range(20):
        low = (next_random() * 32768 + next_random()) % 2000000001
        high = low + (next_random() * 32768 + next_random()) % (2000000001 - low)
        wide = fold(wide, count_stepping_numbers(low, high))
    print(f"20 random ranges up to 2000000000: checksum {wide}")


main()
