# LeetCode #2283: Check if Number Has Equal Digit Count and Digit Value
# -- the Python mirror of the ★ arm, `digits.kara`.


def digit_count(num):
    counts = [0] * 10
    for c in num:
        counts[int(c)] += 1
    for i, c in enumerate(num):
        if counts[i] != int(c):
            return False
    return True


# ---- test harness ---------------------------------------------------------

seed = 2283


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(b):
    return "true" if b else "false"


def main():
    examples = [
        "1210", "030", "2020", "21200", "3211000", "42101000", "521001000", "6210001000",
        "0", "1", "10", "1211", "2120", "6210001001",
    ]
    for num in examples:
        print(f"{num} -> {show(digit_count(num))}")
    check = 0
    held = 0
    for t in range(5000):
        n = next_random() % 10 + 1
        high = [3, min(n, 9) + 1, 10][t % 3]
        num = ""
        for _ in range(n):
            num += chr(ord("0") + next_random() % high)
        answer = digit_count(num)
        check = (check * 31 + (1 if answer else 0)) % 1000000007
        if answer:
            held += 1
    print(f"5000 strings: checksum {check}, {held} true")
    found = []
    for v in range(625):
        num = ""
        rest = v
        for _ in range(4):
            num += chr(ord("0") + rest % 5)
            rest //= 5
        if digit_count(num):
            found.append(num)
    print(f"4 digits below 5: [{', '.join(found)}]")


main()
