# LeetCode #2443: Sum of Number and Its Reverse -- the bench, the ★ arm:
# every k from 0 to num tried, its digits reversed by % 10 and // 10.


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


seed = 2443


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for i in range(400):
        a = next_random()
        num = 90000 + (a * 32768 + next_random()) % 10001
        verdict = 1 if sum_of_number_and_reverse(num) else 0
        check = (check * 31 + num * 2 + verdict + i) % 1000000007
    print(f"400 nums near 10^5: checksum {check}")


main()
