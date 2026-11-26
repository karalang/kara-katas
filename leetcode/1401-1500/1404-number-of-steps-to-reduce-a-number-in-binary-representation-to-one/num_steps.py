# Mirror of num_steps.kara: the digits from the last up, with a carry.


def num_steps(s):
    steps = 0
    carry = 0
    for i in range(len(s) - 1, 0, -1):
        bit = (1 if s[i] == "1" else 0) + carry
        if bit == 1:
            steps += 2
            carry = 1
        else:
            steps += 1
    return steps + carry


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def drawn(n):
    s = "1"
    for _ in range(1, n):
        s += "0" if next_random() % 2 == 0 else "1"
    return s


def main():
    global seed
    print(" ".join(str(num_steps(s)) for s in ["1101", "10", "1", "1111", "1000", "1011"]))
    seed = 1404
    ones = "1" * 500
    power = "1" + "0" * 499
    big = drawn(500)
    print(f"500 digits: {num_steps(ones)} {num_steps(power)} {num_steps(big)}")
    check = 0
    total = 0
    for _ in range(2000):
        n = 1 + next_random() % 100
        steps = num_steps(drawn(n))
        total += steps
        check = (check * 131 + steps) % 1000000007
    print(f"2000 random numbers: {total} steps in all, checksum {check}")


main()
