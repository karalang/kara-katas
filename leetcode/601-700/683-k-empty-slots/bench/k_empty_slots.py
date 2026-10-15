# LeetCode #683: K Empty Slots -- a window over the days. Bench.


def k_empty_slots(bulbs, k):
    n = len(bulbs)
    days = [0] * n
    for d in range(n):
        days[bulbs[d] - 1] = d + 1
    best = -1
    left = 0
    right = k + 1
    i = 1
    while right < n:
        if i == right:
            day = days[left] if days[left] > days[right] else days[right]
            if best == -1 or day < best:
                best = day
            left = right
            right = left + k + 1
            i = left + 1
        elif days[i] < days[left] or days[i] < days[right]:
            left = i
            right = left + k + 1
            i = left + 1
        else:
            i += 1
    return best


def main():
    count, n, rounds = 100, 20000, 30
    seed = 683

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    orders = []
    for _ in range(count):
        v = list(range(1, n + 1))
        i = n - 1
        while i > 0:
            a = next_random()
            j = (a * 32768 + next_random()) % (i + 1)
            v[i], v[j] = v[j], v[i]
            i -= 1
        orders.append(v)
    total = 0
    none = 0
    for r in range(rounds):
        for c in range(count):
            k = (c * 7 + r) % 50
            day = k_empty_slots(orders[c], k)
            if day == -1:
                none += 1
            total = (total * 31 + day + 2) % 1000000007
    print(f"{count * rounds} answers: {none} without a day, checksum {total}")


main()
