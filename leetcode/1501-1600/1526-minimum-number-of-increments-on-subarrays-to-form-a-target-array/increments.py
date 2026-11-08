# LeetCode #1526: Minimum Number of Increments on Subarrays to Form a
# Target Array -- mirrors increments.kara, the ★ arm: the first number and
# every rise.


def min_number_operations(target):
    total = target[0]
    for i in range(1, len(target)):
        if target[i] > target[i - 1]:
            total += target[i] - target[i - 1]
    return total


seed = 1526


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, top):
    check = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 1
        target = [(next_random() * 32768 + next_random()) % top + 1 for _ in range(n)]
        check = mix(check, min_number_operations(target))
    print(f"{count} arrays of 1 to {most} numbers up to {top}: checksum {check}")


print(f"example 1, [1,2,3,2,1] -> {min_number_operations([1, 2, 3, 2, 1])}")
print(f"example 2, [3,1,1,2] -> {min_number_operations([3, 1, 1, 2])}")
print(f"example 3, [3,1,5,4,2] -> {min_number_operations([3, 1, 5, 4, 2])}")
print(f"100000 alternating 1 and 40000 -> {min_number_operations([1 if i % 2 == 0 else 40000 for i in range(100000)])}")
batch(3000, 12, 5)
batch(300, 1000, 1000)
batch(30, 100000, 10000)
