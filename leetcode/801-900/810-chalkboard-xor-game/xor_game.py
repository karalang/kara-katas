# LeetCode 810 — Chalkboard XOR Game, the XOR and the count (mirror of the ★ arm).


def xor_game(nums):
    x = 0
    for v in nums:
        x ^= v
    return x == 0 or len(nums) % 2 == 0


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def b(v):
    return "true" if v else "false"


def show(nums):
    print(f"nums = [{', '.join(map(str, nums))}] -> {b(xor_game(nums))}")


def main():
    global seed
    show([1, 1, 2])
    show([0, 1])
    show([1, 2, 3])
    show([5])
    show([0])
    show([7, 7, 7])
    show([3, 3])
    show([1, 2, 4, 8])
    show([1, 2, 3, 4, 5])
    big = [i * 7919 % 65536 for i in range(1000)]
    print(f"1000 numbers -> {b(xor_game(big))}")
    odd = []
    x = 0
    for i in range(999):
        odd.append(big[i])
        x ^= big[i]
    print(f"999 numbers, XOR {x} -> {b(xor_game(odd))}")
    zero = []
    x = 0
    for i in range(998):
        zero.append(big[i])
        x ^= big[i]
    zero.append(x)
    print(f"999 numbers, XOR 0 -> {b(xor_game(zero))}")
    seed = 810
    wins = 0
    check = 0
    for r in range(2000):
        n = 1 + next_random() % 9
        nums = [next_random() % 8 for _ in range(n)]
        win = 1 if xor_game(nums) else 0
        wins += win
        check = (check * 131 + win * (n + 1) + r) % 1000000007
    print(f"2000 random boards of 1 to 9 numbers: {wins} won by Alice, checksum {check}")


main()
