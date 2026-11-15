# LeetCode #2177: Find Three Consecutive Integers That Sum to a Given
# Number -- the Python mirror of three.kara: the middle is the number's
# third, when 3 divides it.


def sum_of_three(num):
    if num % 3 != 0:
        return []
    x = num // 3
    return [x - 1, x, x + 1]


# ---- test harness ---------------------------------------------------------

seed = 2177


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(num):
    print(f"{num} -> [{', '.join(map(str, sum_of_three(num)))}]")


def fold(check, num, three):
    check = (check * 31 + num % 1000000007 + len(three)) % 1000000007
    for x in three:
        check = (check * 31 + x % 1000000007) % 1000000007
    return check


def main():
    show(33)
    show(4)
    show(0)
    show(3)
    show(1000000000000000)
    show(999999999999999)
    found = 0
    check = 0
    for rnd in range(2000):
        top = [11, 1001, 1000000000000001][rnd % 3]
        a = next_random()
        b = next_random()
        c = next_random()
        num = ((a * 32768 + b) * 32768 + c) % top
        three = sum_of_three(num)
        if three:
            found += 1
        check = fold(check, num, three)
    print(f"2000 numbers: {found} found, checksum {check}")
    every = 0
    found = 0
    for num in range(3001):
        three = sum_of_three(num)
        if three:
            found += 1
        every = fold(every, num, three)
    print(f"0 to 3000: {found} found, checksum {every}")


main()
