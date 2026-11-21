# LeetCode #2443: Sum of Number and Its Reverse -- Python mirror of the ★
# arm (sum.kara): every k from 0 to num tried, its digits reversed by % 10
# and // 10.


def reversed_digits(x):
    r = 0
    y = x
    while y > 0:
        r = r * 10 + y % 10
        y //= 10
    return r


def sum_of_number_and_reverse(num):
    for k in range(num + 1):
        if k + reversed_digits(k) == num:
            return True
    return False


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(b):
    return "true" if b else "false"


def main():
    global seed
    for num in (443, 63, 181, 0, 1, 10, 100000):
        print(f"{num}: {show(sum_of_number_and_reverse(num))}")
    count = 0
    check = 0
    for num in range(1001):
        if sum_of_number_and_reverse(num):
            count += 1
            check = (check * 31 + num) % 1000000007
    print(f"0 to 1000: {count} hold, checksum {check}")
    seed = 2443
    bits = 0
    for _ in range(30):
        a = next_random()
        num = (a * 32768 + next_random()) % 100001
        bits = bits * 2 + (1 if sum_of_number_and_reverse(num) else 0)
    print(f"30 random: verdicts {bits}")
    held = 0
    tried = 0
    while tried < 30:
        a = next_random()
        k = (a * 32768 + next_random()) % 50001
        r = reversed_digits(k)
        if k + r + 1 <= 100000:
            tried += 1
            if sum_of_number_and_reverse(k + r):
                held += 1
            if sum_of_number_and_reverse(k + r + 1):
                held += 1
    print(f"30 sums and 30 sums plus one: {held} hold")


main()
