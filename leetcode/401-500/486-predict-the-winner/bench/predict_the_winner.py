# Benchmark for #486: Python mirror of the ★ arm (one row of leads); see
# predict_the_winner.kara.


def predict_the_winner(nums):
    n = len(nums)
    d = list(nums)
    i = n - 2
    while i >= 0:
        for j in range(i + 1, n):
            d[j] = max(nums[i] - d[j], nums[j] - d[j - 1])
        i -= 1
    return d[n - 1] >= 0


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    arrays = []
    seed = [486]
    for a in range(200):
        arrays.append([next_random(seed) * 32768 % 10000001 for _ in range(1000 + a % 2)])
    wins = 0
    checksum = 0
    for nums in arrays:
        win = 1 if predict_the_winner(nums) else 0
        wins += win
        checksum = (checksum * 31 + win * 7 + len(nums)) % 1000000007
    print(f"200 arrays of 1000 or 1001 numbers: player 1 wins {wins}, checksum {checksum}")


main()
