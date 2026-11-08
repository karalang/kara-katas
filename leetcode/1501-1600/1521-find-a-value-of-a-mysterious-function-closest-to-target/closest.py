# LeetCode #1521: Find a Value of a Mysterious Function Closest to Target
# -- the Python mirror of the ★ arm (closest.kara): the distinct ANDs of
# every range ending at each place, carried forward.


def closest_to_target(arr, target):
    best = abs(arr[0] - target)
    ends = []
    for x in arr:
        nxt = [x]
        for v in ends:
            w = v & x
            if w != nxt[-1]:
                nxt.append(w)
        for v in nxt:
            best = min(best, abs(v - target))
        ends = nxt
    return best


class Seed:
    def __init__(self, v):
        self.v = v


def next_random(seed):
    seed.v = (seed.v * 1103515245 + 12345) % 2147483648
    return seed.v // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, seed):
    check = 0
    for _ in range(count):
        n = next_random(seed) % most + 1
        base = next_random(seed) % 1000000 + 1
        arr = []
        for _ in range(n):
            if next_random(seed) % 2 == 0:
                x = base & (next_random(seed) * 32768 + next_random(seed))
            else:
                x = next_random(seed) * 32 % 1000000
            arr.append(max(x, 1))
        if next_random(seed) % 2 == 0:
            target = arr[next_random(seed) % n] + next_random(seed) % 7 - 3
        else:
            target = (next_random(seed) * 32768 + next_random(seed)) % 10000001
        check = mix(check, closest_to_target(arr, max(target, 0)))
    return check


def main():
    print(f"example 1, [9,12,3,7,15] to 5 -> {closest_to_target([9, 12, 3, 7, 15], 5)}")
    print(f"example 2, [1000000,1000000,1000000] to 1 -> {closest_to_target([1000000, 1000000, 1000000], 1)}")
    print(f"example 3, [1,2,4,8,16] to 0 -> {closest_to_target([1, 2, 4, 8, 16], 0)}")
    print(f"one number, [7] to 10000000 -> {closest_to_target([7], 10000000)}")
    seed = Seed(1521)
    print(f"3000 arrays of 1 to 12 numbers: checksum {batch(3000, 12, seed)}")
    print(f"20 arrays of 1 to 20000 numbers: checksum {batch(20, 20000, seed)}")


main()
