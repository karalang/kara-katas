# LeetCode #1215 bench, in Python: the ★ arm (a breadth-first search from
# the digits 1 to 9, each number followed by itself with one more digit,
# stopping at the first number past `high`) on 2000 random ranges inside
# 0 to 2 * 10^9, drawn once; then 20 rounds over the ranges, each answer's
# length and last number folded into a checksum.

seed = 1215


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def main():
    ranges = []
    for _ in range(2000):
        low = (next_random() * 32768 + next_random()) % 2000000001
        high = low + (next_random() * 32768 + next_random()) % (2000000001 - low)
        ranges.append((low, high))
    check = 0
    for rnd in range(20):
        for low, high in ranges:
            answer = count_stepping_numbers(low, high)
            # -1 when there is none, kept at -1 as the other languages'
            # remainder keeps it
            last = answer[-1] % 1000003 if answer else -1
            check = (check * 131 + len(answer) + last + rnd) % 1000000007
    print(f"20 rounds over 2000 ranges: checksum {check}")


main()
