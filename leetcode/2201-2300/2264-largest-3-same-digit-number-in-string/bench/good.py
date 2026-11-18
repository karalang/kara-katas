# LeetCode #2264: Largest 3-Same-Digit Number in String -- Python mirror
# of the ★ arm (good.kara) on the bench workload: one pass over the
# bytes, the largest digit seen three times running. Output is
# byte-identical to good.kara.


def largest_good_integer(num):
    b = num.encode()
    best = None
    for i in range(2, len(b)):
        if b[i - 2] == b[i] and b[i - 1] == b[i]:
            if best is None or b[i] > best:
                best = b[i]
    return "" if best is None else chr(best) * 3


# ---- bench harness ---------------------------------------------------------

seed = 2264


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for t in range(2000):
        digits = 4 if t % 2 == 0 else 10
        num = "".join(chr(48 + next_random() % digits) for _ in range(1000))
        good = largest_good_integer(num)
        score = 1000 if good == "" else int(good)
        check = (check * 31 + score) % 1000000007
    print(f"2000 numbers of 1000: checksum {check}")


main()
