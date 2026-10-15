# LeetCode #683: K Empty Slots -- a window over the days.
# Mirrors the ★ arm (k_empty_slots.kara) and its test harness.


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
            day = max(days[left], days[right])
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


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(bulbs, k):
    print(f"[{', '.join(map(str, bulbs))}], k = {k} -> {k_empty_slots(bulbs, k)}")


def shuffled(rng, n):
    v = list(range(1, n + 1))
    i = n - 1
    while i > 0:
        j = (rng.next() * 32768 + rng.next()) % (i + 1)
        v[i], v[j] = v[j], v[i]
        i -= 1
    return v


def next_order(v):
    n = len(v)
    i = n - 2
    while i >= 0 and v[i] >= v[i + 1]:
        i -= 1
    if i < 0:
        return False
    j = n - 1
    while v[j] <= v[i]:
        j -= 1
    v[i], v[j] = v[j], v[i]
    v[i + 1:] = reversed(v[i + 1:])
    return True


def main():
    for b, k in [([1, 3, 2], 1), ([1, 2, 3], 1), ([6, 5, 8, 9, 7, 1, 10, 2, 3, 4], 2),
                 ([1], 0), ([1, 2], 0), ([2, 1], 0), ([3, 1, 2], 1), ([1, 4, 2, 3], 2),
                 ([5, 1, 4, 2, 3], 3), ([1, 5, 3, 2, 4], 3), ([4, 1, 3, 5, 2], 0)]:
        show(b, k)
    found = never = total = 0
    for n in range(1, 8):
        for k in range(n):
            v = list(range(1, n + 1))
            while True:
                day = k_empty_slots(v, k)
                if day == -1:
                    never += 1
                else:
                    found += 1
                total = (total * 31 + day + 2) % 1000000007
                if not next_order(v):
                    break
    print(f"every order of 1 to 7 bulbs, every k: {found} with a day, {never} without, checksum {total}")
    rng = Rng(683)
    checksum = 0
    none = 0
    for c in range(200):
        n = 1 + rng.next() % 1000
        k = rng.next() % 4 if c % 2 == 0 else rng.next() % n
        day = k_empty_slots(shuffled(rng, n), k)
        if day == -1:
            none += 1
        checksum = (checksum * 31 + day + 2) % 1000000007
    print(f"200 random orders: {none} without a day, checksum {checksum}")


main()
