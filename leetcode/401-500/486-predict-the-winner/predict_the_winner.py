# LeetCode #486: Predict the Winner -- one row of leads.
# Mirrors predict_the_winner.kara (the ★ arm).


def predict_the_winner(nums):
    n = len(nums)
    d = list(nums)
    i = n - 2
    while i >= 0:
        for j in range(i + 1, n):
            d[j] = max(nums[i] - d[j], nums[j] - d[j - 1])
        i -= 1
    return d[n - 1] >= 0


def show(nums):
    print(f"[{', '.join(str(x) for x in nums)}] -> {'true' if predict_the_winner(nums) else 'false'}")


seed = 486


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show([1, 5, 2])
    show([1, 5, 233, 7])
    show([7])
    show([0])
    show([1, 2, 1])
    show([2, 4, 55, 6, 8])
    show([1, 1, 1, 2, 1])
    show([10000000] + [0] * 18 + [10000000])
    show([3, 9, 1, 2, 9, 7, 8, 4, 6, 5, 2, 8, 1, 7, 3, 6, 4, 9, 2])
    count = 300
    wins = 0
    checksum = 0
    for c in range(count):
        top = 10000001 if c % 5 == 0 else 21
        size = 1 + next_random() % 12
        nums = [next_random() * 32768 % top for _ in range(size)]
        win = 1 if predict_the_winner(nums) else 0
        wins += win
        checksum = (checksum * 31 + win * 7 + len(nums)) % 1000000007
    print(f"{count} random arrays: player 1 wins {wins}, checksum {checksum}")


main()
