# LeetCode #2259: Remove Digit From Number to Maximize Result -- Python
# mirror of the ★ arm (remove.kara) on the bench workload: the first
# occurrence followed by a larger digit, else the last occurrence. Output
# is byte-identical to remove.kara.


def remove_digit(number, digit):
    last = 0
    for i in range(len(number)):
        if number[i] == digit:
            last = i
            if i + 1 < len(number) and number[i + 1] > digit:
                break
    return number[:last] + number[last + 1:]


# ---- bench harness ---------------------------------------------------------

seed = 2259


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    pool = "".join(chr(ord("1") + next_random() % 9) for _ in range(1000000))
    check = 0
    for _ in range(1000000):
        hi = next_random()
        at = (hi * 32768 + next_random()) % (1000000 - 100)
        number = pool[at:at + 100]
        answer = remove_digit(number, number[50])
        for b in answer.encode():
            check = (check * 131 + b) % 1000000007
    print(f"10^6 numbers of 100 digits: checksum {check}")


main()
