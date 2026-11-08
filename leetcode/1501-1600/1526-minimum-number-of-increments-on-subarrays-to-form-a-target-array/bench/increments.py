# LeetCode #1526: Minimum Number of Increments on Subarrays to Form a
# Target Array -- bench: the ★ arm over 100 random arrays of 1 to 100000 numbers up to 10000, built once and answered 50 times.


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


def main():
    arrays = []
    for _ in range(100):
        n = (next_random() * 32768 + next_random()) % 100000 + 1
        arrays.append([(next_random() * 32768 + next_random()) % 10000 + 1 for _ in range(n)])
    check = 0
    for _ in range(50):
        for target in arrays:
            check = mix(check, min_number_operations(target))
    print(f"50 passes over 100 arrays of up to 100000 numbers: checksum {check}")


main()
