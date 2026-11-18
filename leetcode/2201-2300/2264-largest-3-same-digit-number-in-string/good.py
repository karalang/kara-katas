# LeetCode #2264: Largest 3-Same-Digit Number in String -- Python mirror
# of the ★ arm (good.kara): one pass over the bytes, the largest digit
# seen three times running, three times over, or "". Output is
# byte-identical to good.kara.


def largest_good_integer(num):
    b = num.encode()
    best = None
    for i in range(2, len(b)):
        if b[i - 2] == b[i] and b[i - 1] == b[i]:
            if best is None or b[i] > best:
                best = b[i]
    return "" if best is None else chr(best) * 3


# ---- test harness ---------------------------------------------------------

seed = 2264


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def number(length, digits):
    return "".join(chr(48 + next_random() % digits) for _ in range(length))


def score(good):
    return 1000 if good == "" else int(good)


def main():
    for num in ["6777133339", "2300019", "42352338", "1222", "55559", "1000", "123"]:
        print(f'{num} -> "{largest_good_integer(num)}"')
    check = 0
    none = 0
    for t in range(2000):
        length = next_random() % 38 + 3
        good = largest_good_integer(number(length, [2, 3, 4, 10][t % 4]))
        if good == "":
            none += 1
        check = (check * 31 + score(good)) % 1000000007
    print(f"2000 numbers ({none} with none): checksum {check}")
    rand = number(1000, 10)
    pairs = "1100" * 250
    last = "12" * 498 + "9999"
    answers = ", ".join(f'"{largest_good_integer(n)}"' for n in [rand, pairs, last])
    print(f"1000 digits: {answers}")


main()
