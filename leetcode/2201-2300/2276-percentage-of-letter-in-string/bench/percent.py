# LeetCode #2276: Percentage of Letter in String -- the bench, the ★ arm.


def percentage_letter(s, letter):
    count = 0
    for c in s:
        if c == letter:
            count += 1
    return count * 100 // len(s)


# ---- bench harness ---------------------------------------------------------

seed = 2276


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for _ in range(100000):
        s = "".join(chr(97 + next_random() % 4) for _ in range(100))
        letter = chr(97 + next_random() % 4)
        check = (check * 31 + percentage_letter(s, letter)) % 1000000007
    print(f"100000 strings of 100: checksum {check}")


main()
