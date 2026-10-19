# LeetCode 798 -- Smallest Rotation with Highest Score: the bench, in
# Python. Mirrors best_rotation.kara: a difference array over the
# rotations.
seed = 798


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def best_rotation(nums):
    n = len(nums)
    change = [0] * (n + 1)
    for i in range(n):
        first = (i + 1) % n
        last = (i - nums[i] + n) % n
        change[first] += 1
        change[last + 1] -= 1
        if first > last:
            change[0] += 1
            change[n] -= 1
    best, best_score, score = 0, -1, 0
    for k in range(n):
        score += change[k]
        if score > best_score:
            best_score, best = score, k
    return best


def main():
    n = 100000
    arrays = []
    for _ in range(16):
        top = 1 + (next_random() * 32768 + next_random()) % n
        arrays.append([(next_random() * 32768 + next_random()) % top for _ in range(n)])
    rounds = 4000
    total = check = 0
    for r in range(rounds):
        k = best_rotation(arrays[r % 16])
        total += k
        check = (check * 131 + k) % 1000000007
    print(f"{rounds} rounds of {n} numbers: rotations adding up to {total}, checksum {check}")


main()
