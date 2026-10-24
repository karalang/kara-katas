# Benchmark: LeetCode #975 Odd Even Jump -- the stack arm (sorted order
# and a monotonic stack), on 20 arrays of 20000 random values. Mirrors
# odd_even_jumps.kara, .rs, .c and go-seq/.


def next_in(order, n):
    nxt = [-1] * n
    stack = []
    for i in order:
        while stack and stack[-1] < i:
            nxt[stack.pop()] = i
        stack.append(i)
    return nxt


def odd_even_jumps(arr):
    n = len(arr)
    up = sorted(range(n), key=lambda i: (arr[i], i))
    down = sorted(range(n), key=lambda i: (-arr[i], i))
    odd = next_in(up, n)
    even = next_in(down, n)
    higher = [False] * n
    lower = [False] * n
    higher[n - 1] = lower[n - 1] = True
    for i in range(n - 2, -1, -1):
        if odd[i] >= 0:
            higher[i] = lower[odd[i]]
        if even[i] >= 0:
            lower[i] = higher[even[i]]
    return sum(higher)


seed = 975


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds, count = 10, 20
    arrays = [[next_random() % 100000 for _ in range(20000)] for _ in range(count)]
    total = check = 0
    for r in range(rounds):
        for i in range(count):
            good = odd_even_jumps(arrays[(r + i) % count])
            total += good
            check = (check * 31 + good) % 1000000007
    print(f"{rounds} rounds over {count} arrays of 20000 values: "
          f"{total} good starts, checksum {check}")


main()
