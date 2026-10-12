# LeetCode #403: Frog Jump -- mirror of frog_jump.kara (jump sizes per stone).


def can_cross(stones):
    jumps = {s: set() for s in stones}
    jumps[stones[0]].add(0)
    for s in stones:
        for k in sorted(jumps[s]):
            for step in (k - 1, k, k + 1):
                if step > 0 and s + step in jumps:
                    jumps[s + step].add(step)
    return len(jumps[stones[-1]]) > 0


seed = 403


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(stones):
    print(f"{stones}: {'true' if can_cross(stones) else 'false'}")


show([0, 1, 3, 5, 6, 8, 12, 17])
show([0, 1, 2, 3, 4, 8, 9, 11])
show([0, 1])
show([0, 2])
show([0, 1, 3, 6, 10, 15, 21])
show([0, 1, 3, 6, 10, 13, 14])
show([0, 1, 2, 4, 7, 11, 16, 22, 29])
show([0, 1, 3, 4, 5, 7, 9, 10, 12])
show([0, 1, 1000])
show([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
crossed = 0
checksum = 0
for case in range(2000):
    n = 2 + step() % 59
    stones = [0, 1]
    while len(stones) < n:
        stones.append(stones[-1] + 1 + step() % 4)
    if can_cross(stones):
        crossed += 1
        checksum = (checksum * 31 + case + 1) % 1000000007
print(f"2000 random rivers: {crossed} crossed, checksum {checksum}")
