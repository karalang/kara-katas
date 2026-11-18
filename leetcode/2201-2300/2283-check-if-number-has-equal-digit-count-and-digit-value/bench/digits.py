# LeetCode #2283: Check if Number Has Equal Digit Count and Digit Value
# -- the bench, the ★ arm.


def digit_count(num):
    counts = [0] * 10
    for c in num:
        counts[int(c)] += 1
    for i, c in enumerate(num):
        if counts[i] != int(c):
            return False
    return True


# ---- bench harness ---------------------------------------------------------

seed = 2283


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    known = ["1210", "2020", "21200", "3211000", "42101000", "521001000", "6210001000"]
    nums = []
    for k in range(100000):
        if k % 8 == 0:
            nums.append(known[next_random() % 7])
        else:
            n = next_random() % 10 + 1
            num = ""
            for _ in range(n):
                num += chr(ord("0") + next_random() % (min(n, 9) + 1))
            nums.append(num)
    check = 0
    for _ in range(100):
        held = 0
        for num in nums:
            if digit_count(num):
                held += 1
        check = (check * 31 + held) % 1000000007
    print(f"100 passes over 10^5 strings: checksum {check}")


main()
