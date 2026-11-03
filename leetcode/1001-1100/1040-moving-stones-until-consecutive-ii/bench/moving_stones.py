# Benchmark lane for LeetCode 1040 -- Python mirror of moving_stones.kara.


def moves(stones):
    s = sorted(stones)
    n = len(s)
    most = max(s[n - 1] - s[1] - n + 2, s[n - 2] - s[0] - n + 2)
    least = n
    i = 0
    for j in range(n):
        while s[j] - s[i] >= n:
            i += 1
        inside = j - i + 1
        if inside == n - 1 and s[j] - s[i] == n - 2:
            least = min(least, 2)
        else:
            least = min(least, n - inside)
    return least, most


seed = 1040


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(top):
    a = next_random()
    b = next_random()
    return (a * 32768 + b) % top


def main():
    count, size, rounds = 400, 10000, 5
    sets = []
    for c in range(count):
        widest = 100000 if c % 2 == 0 else 3
        stones = []
        at = 0
        for _ in range(size):
            at += draw(widest) + 1
            stones.append(at)
        i = size - 1
        while i > 0:
            j = draw(i + 1)
            stones[i], stones[j] = stones[j], stones[i]
            i -= 1
        sets.append(stones)
    total = 0
    check = 0
    for _ in range(rounds):
        for stones in sets:
            least, most = moves(stones)
            total += least + most
            check = (check * 131 + least * 1000003 + most) % 1000000007
    print(f"{count} sets of {size} stones, {rounds} rounds: total {total}, checksum {check}")


main()
