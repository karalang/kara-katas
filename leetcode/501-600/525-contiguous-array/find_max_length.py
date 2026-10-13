# LeetCode #525: Contiguous Array -- Python mirror of the ★ arm (first
# index of each balance); see find_max_length.kara. Same algorithm, same
# harness, same output.


def find_max_length(nums):
    first = {0: -1}
    balance = 0
    best = 0
    for i in range(len(nums)):
        balance += 1 if nums[i] == 1 else -1
        if balance in first:
            best = max(best, i - first[balance])
        else:
            first[balance] = i
    return best


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    print(f"[{', '.join(map(str, nums))}]: {find_max_length(nums)}")


def main():
    global seed
    show([0, 1])
    show([0, 1, 0])
    show([0, 1, 1, 1, 1, 1, 0, 0, 0])
    show([0])
    show([1, 1])
    show([0, 0, 1, 1])
    show([1, 0, 1, 0, 1, 0])
    show([0, 0, 0, 1])
    show([1, 1, 0, 1, 1, 1, 0, 0])
    seed = 525
    total = 0
    checksum = 0
    for _ in range(3000):
        n = 1 + next_random() % 40
        q = 1 + next_random() % 4
        nums = [1 if next_random() % q == 0 else 0 for _ in range(n)]
        answer = find_max_length(nums)
        total += answer
        checksum = (checksum * 31 + answer) % 1000000007
    print(f"3000 random arrays: total {total}, checksum {checksum}")
    big = []
    halves = []
    for i in range(100000):
        big.append(next_random() % 2)
        halves.append(0 if i < 60000 else 1)
    print(f"100000 random bits: {find_max_length(big)}; 60000 0s then 40000 1s: {find_max_length(halves)}")


main()
