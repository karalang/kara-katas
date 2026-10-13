# LeetCode #507: Perfect Number -- Python mirror of the ★ arm (the
# divisors in pairs up to the square root); see check_perfect_number.kara.


def check_perfect_number(num):
    if num == 1:
        return False
    total = 1
    i = 2
    while i * i <= num:
        if num % i == 0:
            total += i
            if i * i != num:
                total += num // i
        i += 1
    return total == num


# ---- test harness ---------------------------------------------------------

seed = 507


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    for num in [28, 7, 1, 2, 6, 12, 496, 8128, 33550336, 33550337, 100000000]:
        print(f"{num} -> {'true' if check_perfect_number(num) else 'false'}")
    # Every number from 1 to 10,000.
    found = [num for num in range(1, 10001) if check_perfect_number(num)]
    print(f"perfect from 1 to 10000: [{', '.join(str(n) for n in found)}]")
    # 300 numbers: in turn a random one from 1 to 10^8, one of the five
    # perfect numbers in range, one of those plus or minus 1, and twice
    # one of those.
    known = [6, 28, 496, 8128, 33550336]
    count = 300
    perfect = 0
    checksum = 0
    for c in range(count):
        pick = known[next_random() % 5]
        if c % 4 == 0:
            hi = next_random()
            num = 1 + (hi * 32768 + next_random()) % 100000000
        elif c % 4 == 1:
            num = pick
        elif c % 4 == 2:
            num = pick - 1 if next_random() % 2 == 0 else pick + 1
        else:
            num = 2 * pick
        answer = check_perfect_number(num)
        if answer:
            perfect += 1
        checksum = (checksum * 31 + num % 1000 * 2 + int(answer)) % 1000000007
    print(f"{count} numbers: {perfect} perfect, checksum {checksum}")


main()
