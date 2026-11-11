# LeetCode #2119: A Number After a Double Reversal -- Python mirror of
# reversed.kara, the last digit; same harness, same output.


def is_same_after_reversals(num):
    return num == 0 or num % 10 != 0


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(b):
    return "true" if b else "false"


def main():
    for num in [526, 1800, 0, 7, 101, 1000000, 120000]:
        print(f"{num} -> {show(is_same_after_reversals(num))}")
    seed = [2119]
    same = 0
    check = 0
    for _ in range(5000):
        num = next_random(seed) % 1000001
        if next_random(seed) % 3 == 0:
            num = num // 1000 * 10 ** (next_random(seed) % 4)
        got = is_same_after_reversals(num)
        if got:
            same += 1
        check = (check * 31 + (num % 1000 if got else 7)) % 1000000007
    print(f"5000 numbers: {same} the same, checksum {check}")


main()
