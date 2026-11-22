# LeetCode #2769: Find the Maximum Achievable Number -- the ★ arm in
# Python (achievable.kara): num + 2t.


def the_maximum_achievable_x(num, t):
    return num + 2 * t


def main():
    print(the_maximum_achievable_x(4, 1))
    print(the_maximum_achievable_x(3, 2))
    print(the_maximum_achievable_x(1, 1))
    print(the_maximum_achievable_x(50, 50))
    total = 0
    check = 0
    for num in range(1, 51):
        for t in range(1, 51):
            x = the_maximum_achievable_x(num, t)
            total += x
            check = (check * 31 + x) % 1000000007
    print(f"2500 pairs: answers sum to {total}, checksum {check}")


main()
