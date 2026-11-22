# LeetCode #2769: Find the Maximum Achievable Number -- the bench in
# Python: the ★ arm over 10^6 random pairs, all drawn first, then each
# answered 50 times into a running checksum.


def the_maximum_achievable_x(num, t):
    return num + 2 * t


seed = 2769


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 1000000
    rounds = 50
    nums = []
    ts = []
    for _ in range(count):
        nums.append(next_random() % 50 + 1)
        ts.append(next_random() % 50 + 1)
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(count):
            x = the_maximum_achievable_x(nums[i], ts[i])
            total += x
            check = (check * 31 + x + r) % 1000000007
    print(f"{count} pairs, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
