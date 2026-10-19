# LeetCode 798 -- Smallest Rotation with Highest Score: mirrors the
# harness of best_rotation.kara with the ★ arm's difference array.
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


def show(nums):
    print(f"nums = [{', '.join(str(x) for x in nums)}] -> {best_rotation(nums)}")


def main():
    show([2, 3, 1, 4, 0])
    show([1, 3, 0, 2, 4])
    show([0])
    show([0, 0, 0, 0, 0])
    show([4, 4, 4, 4, 4])
    show([0, 1, 2, 3, 4])
    show([4, 3, 2, 1, 0])
    show([1, 0])
    total = check = 0
    for i in range(300):
        n = 1 + next_random() % 60
        top = 1 + next_random() % n
        nums = [next_random() % top for _ in range(n)]
        k = best_rotation(nums)
        total += k
        check = (check * 131 + k + i) % 1000000007
    print(f"300 random arrays: rotations adding up to {total}, checksum {check}")


main()
